

# =============================================================================
# IMAGE UPLOAD ENDPOINT for Web Projects
# =============================================================================

import os
import shutil
from fastapi import File, UploadFile

UPLOAD_DIR = "/var/www/html/assets/images/projects"

@router.post("/web-projects/upload-image")
async def upload_project_image(
    file: UploadFile = File(...),
    user: dict = Depends(verify_token)
):
    """Upload an image for a web project."""
    if user.get('role') not in ['superadmin', 'admin']:
        raise HTTPException(status_code=403, detail="No tiene permiso para subir imagenes")

    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Tipo de archivo no permitido: {file.content_type}")

    # Validate file size (max 10MB)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Archivo demasiado grande (max 10MB)")

    # Sanitize filename
    import re
    filename = file.filename.lower()
    filename = re.sub(r'[^a-z0-9._-]', '-', filename)
    filename = re.sub(r'-+', '-', filename)

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save file
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(contents)

    logging.info(f"[WEB-PROJECTS] Image uploaded: {filename} by {user.get('sub')}")
    return {
        "success": True,
        "filename": filename,
        "url": f"/assets/images/projects/{filename}",
        "message": f"Imagen '{filename}' subida correctamente"
    }


@router.get("/web-projects/images")
async def list_project_images(user: dict = Depends(verify_token)):
    """List all images in the projects folder."""
    try:
        if not os.path.exists(UPLOAD_DIR):
            return {"images": []}

        images = []
        for f in os.listdir(UPLOAD_DIR):
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                filepath = os.path.join(UPLOAD_DIR, f)
                images.append({
                    "filename": f,
                    "url": f"/assets/images/projects/{f}",
                    "size": os.path.getsize(filepath)
                })

        return {"images": sorted(images, key=lambda x: x['filename'])}
    except Exception as e:
        logging.error(f"[WEB-PROJECTS] Error listing images: {e}")
        raise HTTPException(status_code=500, detail=str(e))
