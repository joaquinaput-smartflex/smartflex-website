

# =============================================================================
# WEB PROJECTS - Portfolio Management for smartflex.com.ar
# =============================================================================

# --- Pydantic Models ---

class WebProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    category: str = "construccion"  # construccion, vivienda, reforma, iot, industrial
    tags: Optional[str] = None  # JSON array string
    image_filename: Optional[str] = None
    image_alt: Optional[str] = None
    is_featured: Optional[bool] = False
    display_order: Optional[int] = 0
    is_active: Optional[bool] = True
    location: Optional[str] = None
    year_completed: Optional[int] = None
    client_name: Optional[str] = None
    square_meters: Optional[int] = None

class WebProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    image_filename: Optional[str] = None
    image_alt: Optional[str] = None
    is_featured: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None
    location: Optional[str] = None
    year_completed: Optional[int] = None
    client_name: Optional[str] = None
    square_meters: Optional[int] = None


# --- Web Projects CRUD Endpoints ---

@router.get("/web-projects")
async def list_web_projects(
    active_only: bool = False,
    featured_only: bool = False,
    category: Optional[str] = None,
    user: dict = Depends(verify_token)
):
    """List all web projects for the portfolio."""
    try:
        conditions = []
        params = []

        if active_only:
            conditions.append("is_active = 1")
        if featured_only:
            conditions.append("is_featured = 1")
        if category:
            conditions.append("category = %s")
            params.append(category)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        query = f"""
            SELECT id, title, description, short_description, category, tags,
                   image_filename, image_alt, is_featured, display_order, is_active,
                   location, year_completed, client_name, square_meters,
                   created_at, updated_at, created_by
            FROM web_projects
            {where_clause}
            ORDER BY display_order ASC, created_at DESC
        """

        rows = execute_query(query, tuple(params) if params else None)

        if rows:
            for row in rows:
                if row.get('tags'):
                    try:
                        row['tags'] = json.loads(row['tags'])
                    except:
                        pass

        return {"projects": convert_datetime(rows) if rows else []}
    except Exception as e:
        logging.error(f"[WEB-PROJECTS] List error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/web-projects/{project_id}")
async def get_web_project(project_id: int, user: dict = Depends(verify_token)):
    """Get a single web project by ID."""
    row = execute_query(
        """SELECT id, title, description, short_description, category, tags,
                  image_filename, image_alt, is_featured, display_order, is_active,
                  location, year_completed, client_name, square_meters,
                  created_at, updated_at, created_by
           FROM web_projects WHERE id = %s""",
        (project_id,), "one"
    )
    if not row:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    if row.get('tags'):
        try:
            row['tags'] = json.loads(row['tags'])
        except:
            pass

    return convert_datetime(row)


@router.post("/web-projects")
async def create_web_project(project: WebProjectCreate, user: dict = Depends(verify_token)):
    """Create a new web project."""
    if user.get('role') not in ['superadmin', 'admin']:
        raise HTTPException(status_code=403, detail="No tiene permiso para crear proyectos")

    tags_json = project.tags
    if isinstance(project.tags, list):
        tags_json = json.dumps(project.tags)

    query = """
        INSERT INTO web_projects
        (title, description, short_description, category, tags, image_filename, image_alt,
         is_featured, display_order, is_active, location, year_completed, client_name,
         square_meters, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    result = execute_query(query, (
        project.title, project.description, project.short_description, project.category,
        tags_json, project.image_filename, project.image_alt, project.is_featured,
        project.display_order, project.is_active, project.location, project.year_completed,
        project.client_name, project.square_meters, user.get('sub', 'system')
    ), "commit")

    logging.info(f"[WEB-PROJECTS] Created: {project.title} by {user.get('sub')}")
    return {"success": True, "id": result["last_id"], "message": f"Proyecto '{project.title}' creado"}


@router.put("/web-projects/{project_id}")
async def update_web_project(project_id: int, project: WebProjectUpdate, user: dict = Depends(verify_token)):
    """Update an existing web project."""
    if user.get('role') not in ['superadmin', 'admin']:
        raise HTTPException(status_code=403, detail="No tiene permiso para modificar proyectos")

    updates, values = [], []
    for field, value in project.dict(exclude_unset=True).items():
        if value is not None:
            if field == 'tags' and isinstance(value, list):
                value = json.dumps(value)
            updates.append(f"{field} = %s")
            values.append(value)

    if not updates:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    values.append(project_id)
    result = execute_query(
        f"UPDATE web_projects SET {', '.join(updates)} WHERE id = %s",
        tuple(values), "commit"
    )

    if result["affected_rows"] == 0:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    logging.info(f"[WEB-PROJECTS] Updated ID {project_id} by {user.get('sub')}")
    return {"success": True, "message": "Proyecto actualizado"}


@router.delete("/web-projects/{project_id}")
async def delete_web_project(project_id: int, user: dict = Depends(verify_token)):
    """Delete a web project."""
    if user.get('role') not in ['superadmin', 'admin']:
        raise HTTPException(status_code=403, detail="No tiene permiso para eliminar proyectos")

    result = execute_query("DELETE FROM web_projects WHERE id = %s", (project_id,), "commit")

    if result["affected_rows"] == 0:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    logging.info(f"[WEB-PROJECTS] Deleted ID {project_id} by {user.get('sub')}")
    return {"success": True, "message": "Proyecto eliminado"}


@router.post("/web-projects/reorder")
async def reorder_web_projects(order: List[dict], user: dict = Depends(verify_token)):
    """Reorder web projects. Expects: [{"id": 1, "display_order": 0}, ...]"""
    if user.get('role') not in ['superadmin', 'admin']:
        raise HTTPException(status_code=403, detail="No tiene permiso para reordenar proyectos")

    for item in order:
        execute_query(
            "UPDATE web_projects SET display_order = %s WHERE id = %s",
            (item['display_order'], item['id']), "commit"
        )

    logging.info(f"[WEB-PROJECTS] Reordered {len(order)} projects by {user.get('sub')}")
    return {"success": True, "message": f"{len(order)} proyectos reordenados"}


# --- Public Endpoint (no auth) for smartflex.com.ar ---

@router.get("/public/web-projects")
async def public_list_web_projects(
    featured_only: bool = True,
    category: Optional[str] = None,
    limit: int = 10
):
    """Public endpoint for smartflex.com.ar to fetch featured projects."""
    try:
        conditions = ["is_active = 1"]
        params = []

        if featured_only:
            conditions.append("is_featured = 1")
        if category:
            conditions.append("category = %s")
            params.append(category)

        where_clause = f"WHERE {' AND '.join(conditions)}"

        query = f"""
            SELECT id, title, short_description, category,
                   image_filename, image_alt, location, year_completed
            FROM web_projects
            {where_clause}
            ORDER BY display_order ASC
            LIMIT %s
        """
        params.append(limit)

        rows = execute_query(query, tuple(params))
        return {"projects": rows if rows else []}
    except Exception as e:
        logging.error(f"[WEB-PROJECTS-PUBLIC] Error: {e}")
        raise HTTPException(status_code=500, detail="Error loading projects")
