-- =============================================================================
-- SMARTFLEX Web Projects Table
-- For managing portfolio projects on smartflex.com.ar
-- =============================================================================

CREATE TABLE IF NOT EXISTS web_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Basic info
    title VARCHAR(200) NOT NULL,
    description TEXT,
    short_description VARCHAR(500),

    -- Categorization
    category ENUM('construccion', 'vivienda', 'reforma', 'iot', 'industrial') NOT NULL DEFAULT 'construccion',
    tags VARCHAR(500),  -- JSON array: ["tag1", "tag2"]

    -- Image
    image_filename VARCHAR(255),  -- filename only, stored in /assets/images/projects/
    image_alt VARCHAR(200),

    -- Display settings
    is_featured BOOLEAN DEFAULT FALSE,  -- Show on homepage
    display_order INT DEFAULT 0,  -- Lower = first
    is_active BOOLEAN DEFAULT TRUE,

    -- Optional details
    location VARCHAR(200),
    year_completed YEAR,
    client_name VARCHAR(200),
    square_meters INT,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(100),

    -- Indexes
    INDEX idx_category (category),
    INDEX idx_featured (is_featured, is_active),
    INDEX idx_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert current projects as initial data
INSERT INTO web_projects (title, description, short_description, category, image_filename, image_alt, is_featured, display_order, is_active) VALUES
('Complejo Educativo', 'Construcción integral de instalaciones educativas modernas con aulas amplias, espacios de recreación y áreas administrativas. Proyecto desarrollado con los más altos estándares de calidad y seguridad.', 'Construcción integral de instalaciones educativas con espacios modernos y funcionales.', 'construccion', 'colegio-educativo.jpg', 'Complejo Educativo SMARTFLEX', TRUE, 1, TRUE),
('Residencia Moderna', 'Vivienda unifamiliar de diseño contemporáneo con amplios espacios, jardín y detalles de primera calidad. Incluye sistema de domótica integrado.', 'Diseño y construcción de vivienda unifamiliar con acabados de primera calidad.', 'vivienda', 'residencia-moderna.jpg', 'Residencia Moderna SMARTFLEX', TRUE, 2, TRUE),
('Casa Contemporánea', 'Proyecto residencial con diseño minimalista, materiales sustentables y amplio jardín con pileta. Orientación optimizada para aprovechamiento de luz natural.', 'Proyecto residencial con diseño contemporáneo y materiales sustentables.', 'vivienda', 'casa-contemporanea.jpg', 'Casa Contemporanea SMARTFLEX', TRUE, 3, TRUE);
