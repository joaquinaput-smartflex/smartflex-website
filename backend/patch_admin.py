#!/usr/bin/env python3
"""
Patch admin.html to add Web Projects section
"""
import re

# Read current admin.html
with open('/home/smartflex/smartflex_chatbot/static/admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add sidebar section before </aside>
sidebar_code = '''                    <div class="sidebar-section" id="sidebarWebProjects">
                        <button class="sidebar-toggle" onclick="toggleSubmenu(this)">
                            Sitio Web <span class="arrow">&#9660;</span>
                        </button>
                        <div class="sidebar-submenu">
                            <button class="btn btn-info btn-sm" onclick="showWebProjects()">Proyectos</button>
                            <button class="btn btn-success btn-sm" onclick="openWebProjectModal()">+ Nuevo Proyecto</button>
                        </div>
                    </div>
                </aside>'''

content = content.replace('</aside>', sidebar_code, 1)

# 2. Add content section before first </script>
# Find a good place - before the main script block ends
content_section = '''
<!-- Web Projects Section -->
<div id="webProjectsSection" style="display:none;">
    <div class="section-header">
        <h2>Proyectos del Sitio Web</h2>
        <p>Gestiona los proyectos que se muestran en smartflex.com.ar</p>
    </div>
    <div style="margin-bottom: 20px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
        <button class="btn btn-success" onclick="openWebProjectModal()">+ Nuevo Proyecto</button>
        <select id="filterProjectCategory" onchange="loadWebProjects()" style="padding: 8px; border-radius: 6px; border: 1px solid #ddd;">
            <option value="">Todas las categorias</option>
            <option value="construccion">Construccion</option>
            <option value="vivienda">Vivienda</option>
            <option value="reforma">Reforma</option>
            <option value="iot">IoT</option>
            <option value="industrial">Industrial</option>
        </select>
        <label style="display: flex; align-items: center; gap: 5px;">
            <input type="checkbox" id="filterFeaturedOnly" onchange="loadWebProjects()"> Solo destacados
        </label>
    </div>
    <div id="webProjectsGrid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;"></div>
</div>

<!-- Web Project Modal -->
<div id="webProjectModal" class="modal" style="display:none;">
    <div class="modal-content" style="max-width: 700px;">
        <span class="close" onclick="closeWebProjectModal()">&times;</span>
        <h2 id="webProjectModalTitle">Nuevo Proyecto</h2>
        <form id="webProjectForm" onsubmit="saveWebProject(event)">
            <input type="hidden" id="webProjectId">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div class="form-group" style="grid-column: 1 / -1;">
                    <label>Titulo *</label>
                    <input type="text" id="webProjectTitle" required class="form-control">
                </div>
                <div class="form-group">
                    <label>Categoria *</label>
                    <select id="webProjectCategory" required class="form-control">
                        <option value="construccion">Construccion</option>
                        <option value="vivienda">Vivienda</option>
                        <option value="reforma">Reforma</option>
                        <option value="iot">IoT</option>
                        <option value="industrial">Industrial</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Orden</label>
                    <input type="number" id="webProjectOrder" value="0" min="0" class="form-control">
                </div>
                <div class="form-group" style="grid-column: 1 / -1;">
                    <label>Descripcion corta</label>
                    <textarea id="webProjectShortDesc" rows="2" class="form-control" maxlength="500"></textarea>
                </div>
                <div class="form-group" style="grid-column: 1 / -1;">
                    <label>Descripcion completa</label>
                    <textarea id="webProjectDesc" rows="3" class="form-control"></textarea>
                </div>
                <div class="form-group">
                    <label>Imagen (nombre archivo)</label>
                    <input type="text" id="webProjectImage" class="form-control" placeholder="proyecto.jpg">
                </div>
                <div class="form-group">
                    <label>Alt imagen</label>
                    <input type="text" id="webProjectImageAlt" class="form-control">
                </div>
                <div class="form-group">
                    <label>Ubicacion</label>
                    <input type="text" id="webProjectLocation" class="form-control">
                </div>
                <div class="form-group">
                    <label>Ano</label>
                    <input type="number" id="webProjectYear" class="form-control" min="2000" max="2030">
                </div>
                <div class="form-group">
                    <label>Cliente</label>
                    <input type="text" id="webProjectClient" class="form-control">
                </div>
                <div class="form-group">
                    <label>m2</label>
                    <input type="number" id="webProjectSqm" class="form-control" min="0">
                </div>
                <div class="form-group">
                    <label><input type="checkbox" id="webProjectFeatured"> Destacado</label>
                </div>
                <div class="form-group">
                    <label><input type="checkbox" id="webProjectActive" checked> Activo</label>
                </div>
            </div>
            <div style="margin-top: 20px; display: flex; gap: 10px; justify-content: flex-end;">
                <button type="button" class="btn btn-secondary" onclick="closeWebProjectModal()">Cancelar</button>
                <button type="submit" class="btn btn-primary">Guardar</button>
            </div>
        </form>
    </div>
</div>

    <script>
'''

# Find the first <script> tag and insert before it
content = content.replace('<script>', content_section, 1)

# 3. Add JavaScript functions before </script></body>
js_functions = '''

// =====================
// WEB PROJECTS MANAGEMENT
// =====================

async function showWebProjects() {
    hideAllSections();
    document.getElementById('webProjectsSection').style.display = 'block';
    await loadWebProjects();
}

async function loadWebProjects() {
    const grid = document.getElementById('webProjectsGrid');
    grid.innerHTML = '<p style="text-align:center; padding: 40px;">Cargando...</p>';
    try {
        const category = document.getElementById('filterProjectCategory')?.value || '';
        const featuredOnly = document.getElementById('filterFeaturedOnly')?.checked || false;
        let url = '/admin/api/web-projects?';
        if (category) url += 'category=' + category + '&';
        if (featuredOnly) url += 'featured_only=true&';
        const response = await api(url);
        const projects = response.projects || [];
        if (projects.length === 0) {
            grid.innerHTML = '<p style="text-align:center; padding: 40px; color: #666;">No hay proyectos</p>';
            return;
        }
        grid.innerHTML = projects.map(p => `
            <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="height: 160px; background: #f5f5f5; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                    ${p.image_filename ? '<img src="https://smartflex.com.ar/assets/images/projects/' + p.image_filename + '" style="width:100%;height:100%;object-fit:cover;" onerror="this.style.display=\\'none\\'">' : '<span style="color:#999">Sin imagen</span>'}
                </div>
                <div style="padding: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="background: ${getCategoryColor(p.category)}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px;">${p.category}</span>
                        <span>${p.is_featured ? '★' : ''} ${!p.is_active ? '(inactivo)' : ''}</span>
                    </div>
                    <h4 style="margin: 0 0 8px 0;">${p.title}</h4>
                    <p style="margin: 0 0 12px 0; font-size: 13px; color: #666;">${p.short_description || ''}</p>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn btn-sm btn-primary" onclick="editWebProject(${p.id})">Editar</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteWebProject(${p.id}, '${p.title.replace("'", "\\'")}')">Eliminar</button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error:', error);
        grid.innerHTML = '<p style="color:red;text-align:center;padding:40px;">Error al cargar</p>';
    }
}

function getCategoryColor(cat) {
    const c = {construccion:'#1a73e8', vivienda:'#34a853', reforma:'#ea4335', iot:'#9c27b0', industrial:'#ff9800'};
    return c[cat] || '#666';
}

function openWebProjectModal(project) {
    const modal = document.getElementById('webProjectModal');
    document.getElementById('webProjectForm').reset();
    document.getElementById('webProjectId').value = '';
    document.getElementById('webProjectActive').checked = true;
    if (project) {
        document.getElementById('webProjectModalTitle').textContent = 'Editar Proyecto';
        document.getElementById('webProjectId').value = project.id;
        document.getElementById('webProjectTitle').value = project.title || '';
        document.getElementById('webProjectCategory').value = project.category || 'construccion';
        document.getElementById('webProjectOrder').value = project.display_order || 0;
        document.getElementById('webProjectShortDesc').value = project.short_description || '';
        document.getElementById('webProjectDesc').value = project.description || '';
        document.getElementById('webProjectImage').value = project.image_filename || '';
        document.getElementById('webProjectImageAlt').value = project.image_alt || '';
        document.getElementById('webProjectLocation').value = project.location || '';
        document.getElementById('webProjectYear').value = project.year_completed || '';
        document.getElementById('webProjectClient').value = project.client_name || '';
        document.getElementById('webProjectSqm').value = project.square_meters || '';
        document.getElementById('webProjectFeatured').checked = project.is_featured || false;
        document.getElementById('webProjectActive').checked = project.is_active !== false;
    } else {
        document.getElementById('webProjectModalTitle').textContent = 'Nuevo Proyecto';
    }
    modal.style.display = 'flex';
}

function closeWebProjectModal() {
    document.getElementById('webProjectModal').style.display = 'none';
}

async function editWebProject(id) {
    try {
        const project = await api('/admin/api/web-projects/' + id);
        openWebProjectModal(project);
    } catch (e) { alert('Error al cargar'); }
}

async function saveWebProject(event) {
    event.preventDefault();
    const id = document.getElementById('webProjectId').value;
    const data = {
        title: document.getElementById('webProjectTitle').value,
        category: document.getElementById('webProjectCategory').value,
        display_order: parseInt(document.getElementById('webProjectOrder').value) || 0,
        short_description: document.getElementById('webProjectShortDesc').value || null,
        description: document.getElementById('webProjectDesc').value || null,
        image_filename: document.getElementById('webProjectImage').value || null,
        image_alt: document.getElementById('webProjectImageAlt').value || null,
        location: document.getElementById('webProjectLocation').value || null,
        year_completed: parseInt(document.getElementById('webProjectYear').value) || null,
        client_name: document.getElementById('webProjectClient').value || null,
        square_meters: parseInt(document.getElementById('webProjectSqm').value) || null,
        is_featured: document.getElementById('webProjectFeatured').checked,
        is_active: document.getElementById('webProjectActive').checked
    };
    try {
        if (id) {
            await api('/admin/api/web-projects/' + id, 'PUT', data);
        } else {
            await api('/admin/api/web-projects', 'POST', data);
        }
        closeWebProjectModal();
        loadWebProjects();
    } catch (e) { alert('Error: ' + e.message); }
}

async function deleteWebProject(id, title) {
    if (!confirm('Eliminar "' + title + '"?')) return;
    try {
        await api('/admin/api/web-projects/' + id, 'DELETE');
        loadWebProjects();
    } catch (e) { alert('Error al eliminar'); }
}

</script>
</body>
'''

content = content.replace('</script>\n</body>', js_functions, 1)

# If that didn't work, try another pattern
if '</script>\n</body>' not in content:
    content = content.replace('</script></body>', js_functions.replace('\n</body>', '</body>'), 1)

# Backup and save
with open('/home/smartflex/smartflex_chatbot/static/admin.html.backup', 'w', encoding='utf-8') as f:
    f.write(content)

with open('/home/smartflex/smartflex_chatbot/static/admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully!")
