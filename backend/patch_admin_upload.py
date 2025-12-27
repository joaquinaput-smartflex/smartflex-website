#!/usr/bin/env python3
"""
Patch admin.html to add image upload functionality to web projects
"""

# Read current admin.html
with open('/home/smartflex/smartflex_chatbot/static/admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the image input field to add upload button
old_image_field = '''<div class="form-group">
                    <label>Imagen (nombre archivo)</label>
                    <input type="text" id="webProjectImage" class="form-control" placeholder="proyecto.jpg">
                </div>'''

new_image_field = '''<div class="form-group">
                    <label>Imagen</label>
                    <div style="display: flex; gap: 8px;">
                        <input type="text" id="webProjectImage" class="form-control" placeholder="proyecto.jpg" style="flex:1;">
                        <label class="btn btn-info btn-sm" style="margin:0; cursor:pointer;">
                            Subir <input type="file" id="webProjectImageFile" accept="image/*" onchange="uploadProjectImage(this)" style="display:none;">
                        </label>
                    </div>
                    <div id="uploadProgress" style="display:none; margin-top:5px; color:#666; font-size:12px;">Subiendo...</div>
                </div>'''

content = content.replace(old_image_field, new_image_field)

# Add upload function before </script></body>
upload_function = '''
async function uploadProjectImage(input) {
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];
    if (file.size > 10 * 1024 * 1024) {
        alert('Imagen muy grande (max 10MB)');
        return;
    }
    const progress = document.getElementById('uploadProgress');
    progress.style.display = 'block';
    progress.textContent = 'Subiendo...';
    try {
        const formData = new FormData();
        formData.append('file', file);
        const token = localStorage.getItem('adminToken');
        const response = await fetch('/admin/api/web-projects/upload-image', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + token },
            body: formData
        });
        const result = await response.json();
        if (response.ok && result.filename) {
            document.getElementById('webProjectImage').value = result.filename;
            progress.textContent = 'Subido: ' + result.filename;
            progress.style.color = 'green';
        } else {
            throw new Error(result.detail || 'Error al subir');
        }
    } catch (e) {
        progress.textContent = 'Error: ' + e.message;
        progress.style.color = 'red';
    }
    input.value = '';
}

</script>
</body>'''

content = content.replace('</script>\n</body>', upload_function)

# Save
with open('/home/smartflex/smartflex_chatbot/static/admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Upload patch applied!")
