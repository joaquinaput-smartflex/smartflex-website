# SMARTFLEX Website

Sitio web corporativo de SMARTFLEX SAS - Construcción, Reforma e IoT

## Arquitectura

### Frontend
- HTML5 estático
- CSS3 (variables, grid, flexbox)
- JavaScript vanilla
- Font Awesome icons
- Google Fonts (Inter)

### Backend (FastAPI)
```
fastapi>=0.104.0
uvicorn>=0.24.0
mysql-connector-python>=8.2.0
python-dotenv>=1.0.0
pyjwt>=2.8.0
reportlab>=4.0.0
python-multipart>=0.0.6
pydantic[email]>=2.0.0
```

### Infraestructura
- **Servidor**: Google Cloud VPS (`smartflex-prod`)
- **IP**: 35.198.14.142
- **Dominio**: smartflex.com.ar
- **Proxy**: Apache (reverse proxy a FastAPI)

## Estructura del Proyecto

```
smartflex-website/
├── index.html              # Landing page principal
├── assets/
│   ├── images/            # Imágenes del sitio
│   │   ├── logo.png
│   │   ├── projects/      # Fotos de proyectos
│   │   └── hero/          # Imágenes del hero
│   ├── css/
│   │   └── styles.css     # Estilos (extraer del HTML)
│   └── js/
│       └── main.js        # JavaScript (extraer del HTML)
├── backend/
│   ├── main.py            # FastAPI app
│   ├── routes/
│   ├── .env.example
│   └── requirements.txt
└── README.md
```

---

## ROADMAP DE DESARROLLO

### Fase 1: Setup Inicial
- [x] Crear repositorio GitHub
- [x] Descargar sitio actual del servidor
- [ ] **Obtener imágenes originales** (logo, fotos proyectos)
- [ ] Crear estructura de carpetas
- [ ] Separar CSS del HTML (archivo externo)
- [ ] Separar JS del HTML (archivo externo)

### Fase 2: Arreglar Imágenes Rotas
- [ ] Logo SMARTFLEX (favicon y navbar)
- [ ] Foto hero (colegio_panoramica)
- [ ] Proyecto 1: Complejo Educativo
- [ ] Proyecto 2: Residencia Moderna
- [ ] Proyecto 3: Casa Contemporánea
- [ ] Foto sección "Nosotros" (planos)

### Fase 3: Mejoras de Contenido
- [ ] Actualizar textos y descripciones
- [ ] Agregar más proyectos reales
- [ ] Agregar sección de clientes/testimonios
- [ ] Optimizar SEO (meta tags, schema.org)
- [ ] Agregar Google Analytics

### Fase 4: Funcionalidades Backend
- [ ] Formulario de contacto funcional
- [ ] Envío de emails (SMTP/SendGrid)
- [ ] Integración WhatsApp API
- [ ] Admin para gestionar contenido
- [ ] Base de datos para proyectos/blog

### Fase 5: Sección IoT
- [ ] Página dedicada a servicios IoT
- [ ] Demo interactivo del sistema SMARTFLEX
- [ ] Documentación técnica
- [ ] Portal de acceso clientes (link a wa.smartflex.com.ar)

### Fase 6: Performance y SEO
- [ ] Optimizar imágenes (WebP, lazy loading)
- [ ] Minificar CSS/JS
- [ ] Configurar cache headers
- [ ] SSL/HTTPS (ya configurado)
- [ ] Sitemap.xml y robots.txt
- [ ] Structured data (JSON-LD)

### Fase 7: Deploy y CI/CD
- [ ] Script de deploy automático
- [ ] GitHub Actions para CI/CD
- [ ] Backup automático
- [ ] Monitoreo uptime

---

## Imágenes Necesarias

| Archivo | Uso | Estado |
|---------|-----|--------|
| `SMARTFLEX2-150x150.png` | Logo/Favicon | ❌ Faltante |
| `colegio_panoramica_3-1-2000x1200.jpg` | Hero section | ❌ Faltante |
| `colegio_panoramica-scaled.jpg` | Proyecto 1 | ❌ Faltante |
| `lote141-2000x1200.jpg` | Proyecto 2 | ❌ Faltante |
| `lote252-6-2048x1379.jpg` | Proyecto 3 | ❌ Faltante |
| `web_planos_colegio-2000x1200.png` | Sección Nosotros | ❌ Faltante |
| `smartflex_header_bg.jpg` | Alternativa hero IoT | ✅ Disponible |

---

## Comandos

### Desarrollo Local
```bash
# Servir archivos estáticos
python -m http.server 8080

# Backend FastAPI
cd backend
uvicorn main:app --reload --port 8000
```

### Deploy a Producción
```bash
# Subir archivo HTML
gcloud compute scp index.html smartflex-prod:/tmp/ --zone=southamerica-east1-c
gcloud compute ssh smartflex-prod --zone=southamerica-east1-c --command="sudo cp /tmp/index.html /var/www/html/"

# Subir imágenes
gcloud compute scp assets/images/* smartflex-prod:/tmp/ --zone=southamerica-east1-c
gcloud compute ssh smartflex-prod --zone=southamerica-east1-c --command="sudo mkdir -p /var/www/html/assets/images && sudo cp /tmp/*.{jpg,png} /var/www/html/assets/images/"
```

---

## URLs

| URL | Descripción |
|-----|-------------|
| https://smartflex.com.ar | Sitio corporativo |
| https://wa.smartflex.com.ar/admin | Panel admin IoT |
| https://wa.smartflex.com.ar/monitor | Monitor dispositivos |
| https://wa.smartflex.com.ar/dashboard | Dashboard sensores |

---

## Contacto

- **WhatsApp**: +54 9 11 3692-7440
- **Email**: info@smartflex.com.ar
- **Ubicación**: Buenos Aires, Argentina
