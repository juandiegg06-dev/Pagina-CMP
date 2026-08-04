import os
import re
import json

workspace_dir = r"c:\Users\Ing Sistemas\Downloads\Coomulpinort.com_test"
inventory_file = r"C:\Users\Ing Sistemas\.gemini\antigravity\scratch\page_inventory.json"

# Load page inventory
with open(inventory_file, "r", encoding="utf-8") as f:
    inventory = json.load(f)

# Maps for friendly names and Spanish accents
BREADCRUMB_MAP = {
    "about-us": "Quiénes Somos",
    "company": "Nuestra Cooperativa",
    "gallery": "Galería de Fotos",
    "team": "Nuestro Equipo",
    "asociados": "Asociados",
    "contact": "Contáctenos",
    "e-d-s": "E.D.S Metropolitana",
    "e-d-s-vinculadas": "E.D.S Vinculadas",
    "mas-e-d-s": "E.D.S Norte",
    "oriental": "E.D.S SurOriental",
    "sur-occidente": "E.D.S Sur Occidental",
    "occidental": "E.D.S Occidental",
    "blog": "Interés Social",
    "sarlaft": "Sarlaft",
    "tratamiento-de-datos": "Tratamiento de Datos",
    "codigo-buen-gobierno": "Código de Buen Gobierno",
    "asamblea-2025": "Asamblea 2025",
    "projects": "Responsabilidad Social",
    "project": "Proyectos",
    "correo-institucional": "Correo Institucional"
}

MUNI_MAP = {
    "abrego": "Ábrego",
    "bucarasica": "Bucarasica",
    "cachira": "Cáchira",
    "convencion": "Convención",
    "cucuta": "Cúcuta",
    "cucuta-2": "Cúcuta",
    "el-carmen": "El Carmen",
    "el-tarra": "El Tarra",
    "el-zulia": "El Zulia",
    "hacari": "Hacarí",
    "la-esperanza": "La Esperanza",
    "la-playa": "La Playa",
    "los-patios": "Los Patios",
    "ocana": "Ocaña",
    "pamplona": "Pamplona",
    "ragonvalia": "Ragonvalia",
    "rio-de-oro": "Río de Oro",
    "san-calixto": "San Calixto",
    "san-cayetano": "San Cayetano",
    "teorama": "Teorama",
    "tibu": "Tibú",
    "tibu-2": "Tibú",
    "toledo": "Toledo",
    "villa-del-rosario": "Villa del Rosario"
}

# Zone mapping for interactive E.D.S. selector
ZONE_STATIONS = {
    "metropolitana": [
        {"name": "San Cayetano", "path": "san-cayetano"},
        {"name": "Cúcuta", "path": "cucuta-2"},
        {"name": "Los Patios", "path": "los-patios"},
        {"name": "Villa del Rosario", "path": "villa-del-rosario"},
        {"name": "El Zulia", "path": "el-zulia"}
    ],
    "norte": [
        {"name": "Tibú", "path": "tibu-2"},
        {"name": "Bucarasica", "path": "bucarasica"},
        {"name": "El Tarra", "path": "el-tarra"}
    ],
    "suroriental": [
        {"name": "Toledo", "path": "toledo"},
        {"name": "Ragonvalia", "path": "ragonvalia"}
    ],
    "suroccidental": [
        {"name": "Pamplona", "path": "pamplona"}
    ],
    "occidental": [
        {"name": "Río de Oro", "path": "rio-de-oro"},
        {"name": "La Esperanza", "path": "la-esperanza"},
        {"name": "Hacarí", "path": "hacari"},
        {"name": "La Playa", "path": "la-playa"},
        {"name": "Teorama", "path": "teorama"},
        {"name": "San Calixto", "path": "san-calixto"},
        {"name": "Ocaña", "path": "ocana"},
        {"name": "El Carmen", "path": "el-carmen"},
        {"name": "Convención", "path": "convencion"},
        {"name": "Cáchira", "path": "cachira"},
        {"name": "Ábrego", "path": "abrego"}
    ]
}

def get_path_prefix(rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    depth = len(parts) - 1
    if depth == 0:
        return "./"
    else:
        return "../" * depth

def clean_content(html_str):
    # Find main content container
    start_idx = html_str.find('class="wpb-content-wrapper"')
    if start_idx != -1:
        div_start = html_str.rfind('<div', 0, start_idx)
        start_idx = div_start
    else:
        start_idx = html_str.find('id="content"')
        if start_idx != -1:
            div_start = html_str.rfind('<div', 0, start_idx)
            start_idx = div_start
        else:
            body_start = html_str.find('<body')
            if body_start == -1: return ""
            start_idx = html_str.find('>', body_start) + 1
            body_end = html_str.find('</body>')
            return html_str[start_idx:body_end]
            
    # Count open/close divs
    open_divs = 0
    i = start_idx
    content_html = ""
    while i < len(html_str):
        if html_str[i:i+4].lower() == '<div':
            open_divs += 1
            i += 4
        elif html_str[i:i+6].lower() == '</div':
            open_divs -= 1
            if open_divs == 0:
                content_html = html_str[start_idx:i+6]
                break
            i += 6
        else:
            i += 1
            
    if not content_html:
        content_html = html_str[start_idx:start_idx+10000] # Fallback
        
    # Strip WordPress share boxes and metadata that we don't want
    content_html = re.sub(r'<div class="single-share-box">.*?</div>', '', content_html, flags=re.DOTALL)
    content_html = re.sub(r'<div class="paginator filter-decorations.*?</article>\s*</div>\s*</div>', '', content_html, flags=re.DOTALL) # remove duplicate blog feeds
    
    # Modernize any tables by stripping inline WordPress styling
    content_html = re.sub(r'<table[^>]*>', '<table>', content_html)
    content_html = re.sub(r'<tr[^>]*>', '<tr>', content_html)
    content_html = re.sub(r'<td[^>]*>', '<td>', content_html)
    content_html = re.sub(r'<th[^>]*>', '<th>', content_html)
    
    # Replace absolute domain links with relative paths
    content_html = content_html.replace("https://coomulpinort.com/", "/")
    
    # Strip some specific elementor/WP style tag attributes to let our clean CSS rule
    content_html = re.sub(r'style="[^"]*font-size:[^"]*"', '', content_html)
    content_html = re.sub(r'style="[^"]*font-family:[^"]*"', '', content_html)
    
    return content_html

def generate_breadcrumbs(url_path):
    if url_path == "/":
        return ""
    
    parts = [p for p in url_path.strip("/").split("/") if p]
    breadcrumbs = ['<a href="/">Inicio</a>']
    
    current_url = "/"
    for idx, part in enumerate(parts):
        current_url += part + "/"
        
        # Determine name
        name = BREADCRUMB_MAP.get(part, MUNI_MAP.get(part, part.replace("-", " ").capitalize()))
        
        if idx == len(parts) - 1:
            breadcrumbs.append(f'<span class="separator">/</span> <span>{name}</span>')
        else:
            breadcrumbs.append(f'<span class="separator">/</span> <a href="{current_url}">{name}</a>')
            
    return '<div class="breadcrumbs-container">' + " ".join(breadcrumbs) + "</div>"

def generate_banner(url_path, title):
    if url_path == "/":
        return ""
    
    breadcrumbs = generate_breadcrumbs(url_path)
    clean_title = title.split("–")[0].split("|")[0].strip()
    return f"""
    <section class="page-banner">
        <h1>{clean_title}</h1>
        {breadcrumbs}
    </section>
    """

def generate_menu_html(prefix, current_path, is_mobile=False):
    # Active class helper
    def active_class(pattern):
        if pattern == "/" and current_path == "/":
            return "menu-item-active" if not is_mobile else "active"
        if pattern != "/" and current_path.startswith(pattern):
            return "menu-item-active" if not is_mobile else "active"
        return ""

    if is_mobile:
        return f"""
        <li><a href="{prefix}" class="mobile-menu-item-link">Inicio</a></li>
        <li><a href="{prefix}about-us/company/" class="mobile-menu-item-link">Quiénes Somos</a></li>
        <li>
            <a href="{prefix}estaciones/e-d-s-vinculadas/" class="mobile-menu-item-link">E.D.S. Vinculadas</a>
            <ul class="mobile-submenu-items">
                <li><a href="{prefix}estaciones/e-d-s/" class="mobile-submenu-item-link">E.D.S Metropolitana</a></li>
                <li><a href="{prefix}estaciones/mas-e-d-s/" class="mobile-submenu-item-link">E.D.S Norte</a></li>
                <li><a href="{prefix}estaciones/oriental/" class="mobile-submenu-item-link">E.D.S SurOriental</a></li>
                <li><a href="{prefix}estaciones/pamplona/" class="mobile-submenu-item-link">E.D.S Sur Occidental</a></li>
                <li><a href="{prefix}estaciones/occidental/" class="mobile-submenu-item-link">E.D.S Occidental</a></li>
            </ul>
        </li>
        <li><a href="{prefix}projects/" class="mobile-menu-item-link">Responsabilidad Social</a></li>
        <li><a href="{prefix}asociados/" class="mobile-menu-item-link">Asociados</a></li>
        <li>
            <a href="{prefix}blog/" class="mobile-menu-item-link">Interés Social</a>
            <ul class="mobile-submenu-items">
                <li><a href="{prefix}sarlaft/" class="mobile-submenu-item-link">Sarlaft</a></li>
                <li><a href="{prefix}tratamiento-de-datos/" class="mobile-submenu-item-link">Tratamiento de Datos</a></li>
                <li><a href="{prefix}codigo-buen-gobierno/" class="mobile-submenu-item-link">Código Buen Gobierno</a></li>
                <li><a href="{prefix}asamblea-2025/" class="mobile-submenu-item-link">Asamblea 2025</a></li>
            </ul>
        </li>
        <li>
            <a href="{prefix}contact/" class="mobile-menu-item-link">Contáctenos</a>
            <ul class="mobile-submenu-items">
                <li><a href="{prefix}correo-institucional/" class="mobile-submenu-item-link">Correo Institucional</a></li>
            </ul>
        </li>
        """
    else:
        return f"""
        <li class="menu-item {active_class('/')}"><a href="{prefix}" class="menu-item-link">Inicio</a></li>
        <li class="menu-item {active_class('/about-us/')}"><a href="{prefix}about-us/company/" class="menu-item-link">Quiénes Somos</a></li>
        <li class="menu-item menu-item-has-dropdown {active_class('/estaciones/e-d-s-vinculadas/') or active_class('/estaciones/e-d-s/') or active_class('/estaciones/occidental/') or active_class('/estaciones/oriental/') or active_class('/estaciones/mas-e-d-s/')}">
            <a href="{prefix}estaciones/e-d-s-vinculadas/" class="menu-item-link">E.D.S. Vinculadas <i class="fa-solid fa-chevron-down" style="font-size: 0.7rem;"></i></a>
            <ul class="menu-dropdown">
                <li class="dropdown-submenu">
                    <a href="{prefix}estaciones/e-d-s/" class="dropdown-item-link">E.D.S Metropolitana <i class="fa-solid fa-chevron-right" style="font-size: 0.65rem; float: right; margin-top: 0.25rem;"></i></a>
                    <ul class="dropdown-submenu-menu">
                        <li><a href="{prefix}estaciones/san-cayetano/" class="dropdown-item-link">San Cayetano</a></li>
                        <li><a href="{prefix}estaciones/cucuta-2/" class="dropdown-item-link">Cúcuta</a></li>
                        <li><a href="{prefix}estaciones/los-patios/" class="dropdown-item-link">Los Patios</a></li>
                        <li><a href="{prefix}estaciones/villa-del-rosario/" class="dropdown-item-link">Villa del Rosario</a></li>
                        <li><a href="{prefix}estaciones/el-zulia/" class="dropdown-item-link">El Zulia</a></li>
                    </ul>
                </li>
                <li class="dropdown-submenu">
                    <a href="{prefix}estaciones/mas-e-d-s/" class="dropdown-item-link">E.D.S Norte <i class="fa-solid fa-chevron-right" style="font-size: 0.65rem; float: right; margin-top: 0.25rem;"></i></a>
                    <ul class="dropdown-submenu-menu">
                        <li><a href="{prefix}estaciones/tibu-2/" class="dropdown-item-link">Tibú</a></li>
                        <li><a href="{prefix}estaciones/bucarasica/" class="dropdown-item-link">Bucarasica</a></li>
                        <li><a href="{prefix}estaciones/el-tarra/" class="dropdown-item-link">El Tarra</a></li>
                    </ul>
                </li>
                <li class="dropdown-submenu">
                    <a href="{prefix}estaciones/oriental/" class="dropdown-item-link">E.D.S SurOriental <i class="fa-solid fa-chevron-right" style="font-size: 0.65rem; float: right; margin-top: 0.25rem;"></i></a>
                    <ul class="dropdown-submenu-menu">
                        <li><a href="{prefix}estaciones/toledo/" class="dropdown-item-link">Toledo</a></li>
                        <li><a href="{prefix}estaciones/ragonvalia/" class="dropdown-item-link">Ragonvalia</a></li>
                    </ul>
                </li>
                <li><a href="{prefix}estaciones/pamplona/" class="dropdown-item-link">E.D.S Sur Occidental</a></li>
                <li class="dropdown-submenu">
                    <a href="{prefix}estaciones/occidental/" class="dropdown-item-link">E.D.S Occidental <i class="fa-solid fa-chevron-right" style="font-size: 0.65rem; float: right; margin-top: 0.25rem;"></i></a>
                    <ul class="dropdown-submenu-menu">
                        <li><a href="{prefix}estaciones/rio-de-oro/" class="dropdown-item-link">Río de Oro</a></li>
                        <li><a href="{prefix}estaciones/la-esperanza/" class="dropdown-item-link">La Esperanza</a></li>
                        <li><a href="{prefix}estaciones/hacari/" class="dropdown-item-link">Hacarí</a></li>
                        <li><a href="{prefix}estaciones/la-playa/" class="dropdown-item-link">La Playa</a></li>
                        <li><a href="{prefix}estaciones/teorama/" class="dropdown-item-link">Teorama</a></li>
                        <li><a href="{prefix}estaciones/san-calixto/" class="dropdown-item-link">San Calixto</a></li>
                        <li><a href="{prefix}estaciones/ocana/" class="dropdown-item-link">Ocaña</a></li>
                        <li><a href="{prefix}estaciones/el-carmen/" class="dropdown-item-link">El Carmen</a></li>
                        <li><a href="{prefix}estaciones/convencion/" class="dropdown-item-link">Convención</a></li>
                        <li><a href="{prefix}estaciones/cachira/" class="dropdown-item-link">Cáchira</a></li>
                        <li><a href="{prefix}estaciones/abrego/" class="dropdown-item-link">Ábrego</a></li>
                    </ul>
                </li>
            </ul>
        </li>
        <li class="menu-item {active_class('/projects/')}"><a href="{prefix}projects/" class="menu-item-link">Responsabilidad Social</a></li>
        <li class="menu-item {active_class('/asociados/')}"><a href="{prefix}asociados/" class="menu-item-link">Asociados</a></li>
        <li class="menu-item menu-item-has-dropdown {active_class('/blog/') or active_class('/sarlaft/') or active_class('/tratamiento-de-datos/') or active_class('/codigo-buen-gobierno/') or active_class('/asamblea-2025/')}">
            <a href="{prefix}blog/" class="menu-item-link">Interés Social <i class="fa-solid fa-chevron-down" style="font-size: 0.7rem;"></i></a>
            <ul class="menu-dropdown">
                <li><a href="{prefix}sarlaft/" class="dropdown-item-link">Sarlaft</a></li>
                <li><a href="{prefix}tratamiento-de-datos/" class="dropdown-item-link">Tratamiento de Datos</a></li>
                <li><a href="{prefix}codigo-buen-gobierno/" class="dropdown-item-link">Código Buen Gobierno</a></li>
                <li><a href="{prefix}asamblea-2025/" class="dropdown-item-link">Asamblea 2025</a></li>
            </ul>
        </li>
        <li class="menu-item menu-item-has-dropdown {active_class('/contact/') or active_class('/correo-institucional/')}">
            <a href="{prefix}contact/" class="menu-item-link">Contáctenos <i class="fa-solid fa-chevron-down" style="font-size: 0.7rem;"></i></a>
            <ul class="menu-dropdown">
                <li><a href="{prefix}correo-institucional/" class="dropdown-item-link">Correo Institucional</a></li>
            </ul>
        </li>
        """

# 1. Compile Blog Posts to build dynamic home page and catalog list
blog_posts = []
for page in inventory:
    path = page["url_path"]
    
    # Identify specific blog posts
    is_blog_post = False
    if re.match(r"^/(2020|2021|2022|2023|2024|2025|2026)(/|$)", path):
        parts = path.strip("/").split("/")
        if len(parts) > 3: # /YYYY/MM/DD/post-name
            is_blog_post = True
            
    if is_blog_post:
        # Extract title and excerpt
        clean_title = page["title"].split("–")[0].split("|")[0].strip()
        date_str = "/".join(path.strip("/").split("/")[:3]) # YYYY/MM/DD
        
        # Scrape featured image if present in snippet/raw content
        file_path = os.path.join(workspace_dir, page["rel_path"])
        with open(file_path, "r", encoding="utf-8", errors="ignore") as pf:
            raw_html = pf.read()
            
        img_match = re.search(r'src="(/wp-content/uploads/[^"]+)"', raw_html)
        feat_img = img_match.group(1) if img_match else "/wp-content/uploads/2021/06/Estacion_samanes.jpg"
        
        # Get brief text snippet
        text_content = re.sub(r'<[^>]+>', ' ', clean_content(raw_html))
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        excerpt = text_content[:200] + "..." if len(text_content) > 200 else text_content
        
        blog_posts.append({
            "title": clean_title,
            "url_path": path,
            "date": date_str,
            "feat_img": feat_img,
            "excerpt": excerpt
        })

# Sort blog posts by date descending
blog_posts.sort(key=lambda x: x["date"], reverse=True)

# Generate Home Page Blog Cards
blog_cards_html = ""
for post in blog_posts[:3]: # Take 3 most recent posts
    # Re-format date (e.g. 2026/02/12 -> 12 de febrero de 2026)
    date_parts = post["date"].split("/")
    months = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    formatted_date = f"{int(date_parts[2])} de {months[int(date_parts[1])]} de {date_parts[0]}"
    
    blog_cards_html += f"""
    <div class="blog-card">
        <div class="blog-card-image-wrap">
            <span class="blog-card-category">Eventos</span>
            <img src="{post['feat_img']}" alt="{post['title']}">
        </div>
        <div class="blog-card-body">
            <div class="blog-card-meta">
                <span><i class="fa-regular fa-calendar"></i> {formatted_date}</span>
                <span><i class="fa-regular fa-user"></i> admin</span>
            </div>
            <h3><a href="{post['url_path']}">{post['title']}</a></h3>
            <p class="excerpt">{post['excerpt']}</p>
            <a href="{post['url_path']}" class="blog-card-more-btn">Leer Más <i class="fa-solid fa-arrow-right"></i></a>
        </div>
    </div>
    """

# Generate E.D.S Zone Finder Grid HTML
zone_grid_html = ""
for zone, stations in ZONE_STATIONS.items():
    for station in stations:
        zone_grid_html += f"""
        <div class="station-card" data-zone="{zone}">
            <div class="station-icon">
                <i class="fa-solid fa-gas-pump"></i>
            </div>
            <h4>E.D.S. {station['name']}</h4>
            <a href="/estaciones/{station['path']}/" class="station-link-btn">Ver Estación</a>
        </div>
        """

# Modern layout templates
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="icon" href="{prefix}wp-content/uploads/2022/01/cropped-logopeq-32x32.jpg" sizes="32x32">
    <!-- FontAwesome for Premium Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Modern Stylesheet -->
    <link rel="stylesheet" href="{prefix}modern.css">
</head>
<body>
    <!-- Top Details Bar -->
    <div class="top-bar">
        <div class="top-bar-content">
            <div class="top-bar-info">
                <span><i class="fa-solid fa-phone"></i> 3154148812 / (037) 5720321</span>
                <span><i class="fa-solid fa-location-dot"></i> AV. 0B N° 21-09 Barrio Blanco, Cúcuta</span>
            </div>
            <div class="top-bar-socials">
                <a href="https://www.facebook.com/Coomulpinort/" target="_blank"><i class="fa-brands fa-facebook"></i></a>
                <a href="https://www.instagram.com/coomulpinort/" target="_blank"><i class="fa-brands fa-instagram"></i></a>
                <a href="https://twitter.com/coomulpinort" target="_blank"><i class="fa-brands fa-twitter"></i></a>
                <a href="http://wa.me/573154148812" target="_blank"><i class="fa-brands fa-whatsapp"></i></a>
            </div>
        </div>
    </div>

    <!-- Glassmorphic Site Header -->
    <header class="site-header">
        <div class="nav-container">
            <a href="{prefix}" class="branding-logo">
                <img src="{prefix}wp-content/uploads/2022/01/logopeq.jpg" alt="Logo Coomulpinort">
                <div class="branding-text">
                    <span class="site-title-text">Coomulpinort</span>
                    <span class="site-desc-text">Cooperativa Multiactiva</span>
                </div>
            </a>
            
            <button class="mobile-menu-toggle" aria-label="Abrir Menú">
                <i class="fa-solid fa-bars"></i>
            </button>
            
            <nav class="desktop-navigation">
                <ul class="main-navigation-menu">
                    {navigation_menu}
                </ul>
            </nav>
        </div>
    </header>

    <!-- Mobile Navigation Drawer -->
    <div class="drawer-overlay"></div>
    <div class="mobile-nav-drawer">
        <div class="drawer-header">
            <span class="site-title-text">Menú</span>
            <button class="drawer-close-btn" aria-label="Cerrar Menú">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
        <ul class="mobile-menu-items">
            {mobile_navigation_menu}
        </ul>
    </div>

    <!-- Hero / Banner Section -->
    {banner_section}

    <!-- Main Wrapper -->
    <main class="main-wrapper">
        {main_content}
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="footer-top">
            <div class="footer-column">
                <h3>Coomulpinort</h3>
                <p>Cooperativa Multiactiva de Pimpineros del Norte. Nacida en 2009 para liderar la reconversión socio-laboral, comercialización y distribución mayorista de combustibles en Norte de Santander.</p>
                <div class="footer-social-links">
                    <a href="https://www.facebook.com/Coomulpinort/" target="_blank"><i class="fa-brands fa-facebook-f"></i></a>
                    <a href="https://www.instagram.com/coomulpinort/" target="_blank"><i class="fa-brands fa-instagram"></i></a>
                    <a href="https://twitter.com/coomulpinort" target="_blank"><i class="fa-brands fa-twitter"></i></a>
                    <a href="http://wa.me/573154148812" target="_blank"><i class="fa-brands fa-whatsapp"></i></a>
                </div>
            </div>
            
            <div class="footer-column">
                <h3>Enlaces Rápidos</h3>
                <ul>
                    <li><a href="{prefix}"><i class="fa-solid fa-chevron-right"></i> Inicio</a></li>
                    <li><a href="{prefix}about-us/company/"><i class="fa-solid fa-chevron-right"></i> Quiénes Somos</a></li>
                    <li><a href="{prefix}estaciones/e-d-s-vinculadas/"><i class="fa-solid fa-chevron-right"></i> E.D.S. Vinculadas</a></li>
                    <li><a href="{prefix}projects/"><i class="fa-solid fa-chevron-right"></i> Responsabilidad Social</a></li>
                    <li><a href="{prefix}asociados/"><i class="fa-solid fa-chevron-right"></i> Asociados</a></li>
                    <li><a href="{prefix}contact/"><i class="fa-solid fa-chevron-right"></i> Contáctenos</a></li>
                </ul>
            </div>
            
            <div class="footer-column">
                <h3>Contacto</h3>
                <div class="footer-contact-item">
                    <i class="fa-solid fa-location-dot"></i>
                    <span>Av. 0B N° 21-09 Barrio Blanco, Cúcuta, Norte de Santander</span>
                </div>
                <div class="footer-contact-item">
                    <i class="fa-solid fa-phone"></i>
                    <span>3154148812 / (037) 5720321</span>
                </div>
                <div class="footer-contact-item">
                    <i class="fa-solid fa-envelope"></i>
                    <span>Coomulpinort@hotmail.com</span>
                </div>
                <div class="footer-contact-item">
                    <i class="fa-solid fa-clock"></i>
                    <span>Lun - Vie: 8AM-12PM / 2PM-6PM<br>Sáb: 8AM-12PM</span>
                </div>
            </div>
            
            <div class="footer-column">
                <h3>Políticas y Control</h3>
                <ul>
                    <li><a href="{prefix}sarlaft/"><i class="fa-solid fa-shield-halved"></i> Sarlaft</a></li>
                    <li><a href="{prefix}tratamiento-de-datos/"><i class="fa-solid fa-user-lock"></i> Tratamiento de Datos</a></li>
                    <li><a href="{prefix}codigo-buen-gobierno/"><i class="fa-solid fa-scale-balanced"></i> Código de Buen Gobierno</a></li>
                    <li><a href="{prefix}asamblea-2025/"><i class="fa-solid fa-users"></i> Asamblea 2025</a></li>
                </ul>
            </div>
        </div>
        
        <div class="footer-bottom">
            <div class="footer-bottom-content">
                <span>Coomulpinort &copy; 2026 | Cúcuta - Colombia. Todos los derechos reservados.</span>
                <span>Cooperativa Multiactiva de Pimpineros del Norte</span>
            </div>
        </div>
    </footer>

    <!-- Modern Script -->
    <script src="{prefix}modern.js"></script>
</body>
</html>
"""

# Compile each file in the inventory
for page in inventory:
    url_path = page["url_path"]
    rel_path = page["rel_path"]
    title = page["title"]
    
    file_path = os.path.join(workspace_dir, rel_path)
    prefix = get_path_prefix(rel_path)
    
    # Read original raw HTML
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        original_html = f.read()
        
    # Get navigation HTML
    nav_html = generate_menu_html(prefix, url_path, is_mobile=False)
    mobile_nav_html = generate_menu_html(prefix, url_path, is_mobile=True)
    
    if url_path == "/":
        # Homepage specific layout
        banner_section = f"""
        <!-- Homepage Hero Banner Slider -->
        <section class="hero-slider-container">
            <div class="slide slide-active">
                <img src="{prefix}wp-content/uploads/2025/12/navida1-100-1.jpg" alt="Navidad" class="slide-img">
                <div class="slide-overlay"></div>
                <div class="slide-content">
                    <h2>Asamblea General Ordinaria</h2>
                    <p>Convocatoria Oficial Nro. XXII para nuestra Asamblea General de Asociados Coomulpinort.</p>
                    <div style="display: flex; gap: 1rem;">
                        <a href="{prefix}asamblea-2025/" class="btn btn-primary">Ver Convocatoria</a>
                        <a href="{prefix}about-us/company/" class="btn btn-secondary" style="background-color: transparent; color: white; border-color: rgba(255,255,255,0.4)">Quiénes Somos</a>
                    </div>
                </div>
            </div>
            
            <div class="slide">
                <img src="{prefix}wp-content/uploads/2022/07/portada2julio.png" alt="Crecimiento" class="slide-img">
                <div class="slide-overlay"></div>
                <div class="slide-content">
                    <h2>Seguimos Creciendo para Nuestra Región</h2>
                    <p>Incrementamos beneficios y brindamos apoyo continuo en capacitación para nuestros asociados y sus familias.</p>
                    <div style="display: flex; gap: 1rem;">
                        <a href="{prefix}asociados/" class="btn btn-primary">Beneficios de Asociados</a>
                        <a href="{prefix}projects/" class="btn btn-secondary" style="background-color: transparent; color: white; border-color: rgba(255,255,255,0.4)">Responsabilidad Social</a>
                    </div>
                </div>
            </div>
            
            <div class="slide">
                <img src="{prefix}wp-content/uploads/2021/02/DSC_0254-1-scaled.jpg" alt="Distribuidor" class="slide-img">
                <div class="slide-overlay"></div>
                <div class="slide-content">
                    <h2>Distribuidor Mayorista de Combustibles</h2>
                    <p>Líderes y referentes en el manejo y comercialización de combustibles en el Norte de Santander y sur de Cesar.</p>
                    <div style="display: flex; gap: 1rem;">
                        <a href="{prefix}estaciones/e-d-s-vinculadas/" class="btn btn-primary">E.D.S. Vinculadas</a>
                        <a href="{prefix}contact/" class="btn btn-secondary" style="background-color: transparent; color: white; border-color: rgba(255,255,255,0.4)">Escríbenos</a>
                    </div>
                </div>
            </div>
            
            <div class="slider-controls">
                <button class="slider-btn slider-btn-prev" aria-label="Anterior"><i class="fa-solid fa-chevron-left"></i></button>
                <button class="slider-btn slider-btn-next" aria-label="Siguiente"><i class="fa-solid fa-chevron-right"></i></button>
            </div>
        </section>
        """
        
        main_content = f"""
        <!-- Interactive Service Stations Zone Filter Finder -->
        <section class="content-section">
            <h2 class="home-section-title">Nuestras Estaciones de Servicio</h2>
            <p style="text-align: center; max-width: 700px; margin: 0 auto 2.5rem auto; color: var(--text-muted);">
                Contamos con más de 100 estaciones de servicio vinculadas en todo el departamento de Norte de Santander. Filtra las estaciones por zona geográfica para encontrar su ubicación y detalles.
            </p>
            
            <div class="eds-zones-widget">
                <div class="eds-tabs">
                    <button class="eds-tab-btn tab-active" data-zone-target="metropolitana">Metropolitana</button>
                    <button class="eds-tab-btn" data-zone-target="norte">Norte</button>
                    <button class="eds-tab-btn" data-zone-target="suroriental">Sur Oriental</button>
                    <button class="eds-tab-btn" data-zone-target="suroccidental">Sur Occidental</button>
                    <button class="eds-tab-btn" data-zone-target="occidental">Occidental</button>
                </div>
                
                <div class="eds-stations-grid">
                    {zone_grid_html}
                </div>
            </div>
        </section>
        
        <!-- Video and Map Gallery Showcase -->
        <section class="card-grid">
            <div class="card" style="padding: 2rem;">
                <h3 style="border-bottom: 2px solid var(--primary); padding-bottom: 0.5rem; margin-bottom: 1.5rem;">Coomulpinort en Video</h3>
                <div class="video-container">
                    <iframe src="https://www.youtube.com/embed/zOwuA-k-vBc" title="Video Institucional Coomulpinort" allowfullscreen></iframe>
                </div>
            </div>
            
            <div class="card" style="padding: 2rem;">
                <h3 style="border-bottom: 2px solid var(--primary); padding-bottom: 0.5rem; margin-bottom: 1.5rem;">Nuestra Ubicación Principal</h3>
                <iframe src="https://maps.google.com/maps?q=planta%20petromil%20agualinda&t=m&z=12&output=embed&iwloc=near" title="Planta Petromil Agualinda Map" style="height: 310px; margin: 0;"></iframe>
            </div>
        </section>
        
        <!-- Dynamic News Feed Section -->
        <section class="home-blog-section">
            <h2 class="home-section-title">Interés y Social y Noticias</h2>
            <div class="blog-grid">
                {blog_cards_html}
            </div>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="{prefix}blog/" class="btn btn-primary">Ver Todas las Publicaciones</a>
            </div>
        </section>
        """
    else:
        # Inner Page layout
        banner_section = generate_banner(url_path, title)
        inner_content = clean_content(original_html)
        
        # Check if the page is a specific blog post
        is_post_page = re.match(r"^/(2020|2021|2022|2023|2024|2025|2026)(/|$)", url_path) and len(url_path.strip("/").split("/")) > 3
        
        if is_post_page:
            # Wrap blog post inside a premium reading container
            date_val, cat_val = "", "Eventos"
            # Get meta details
            date_match = re.search(r'<time class="entry-date[^"]*"[^>]*>(.*?)</time>', original_html)
            if date_match:
                date_val = date_match.group(1).strip()
            
            cat_match = re.search(r'href="/category/([^/]+)/"', original_html)
            if cat_match:
                cat_val = cat_match.group(1).capitalize()
                
            main_content = f"""
            <article class="content-section" style="max-width: 800px; margin: 0 auto;">
                <div class="blog-card-meta" style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; font-size: 0.9rem;">
                    <span><i class="fa-regular fa-calendar"></i> {date_val}</span>
                    <span><i class="fa-regular fa-folder-open"></i> {cat_val}</span>
                    <span><i class="fa-regular fa-user"></i> admin</span>
                </div>
                <div class="blog-post-content-body">
                    {inner_content}
                </div>
                <div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between;">
                    <a href="{prefix}blog/" class="btn btn-secondary"><i class="fa-solid fa-arrow-left"></i> Volver a Noticias</a>
                    <a href="http://wa.me/573154148812" class="btn btn-primary" target="_blank"><i class="fa-brands fa-whatsapp"></i> Consultar por WhatsApp</a>
                </div>
            </article>
            """
        else:
            # Standard page wrapper
            main_content = f"""
            <section class="content-section">
                {inner_content}
            </section>
            """

    # Format page
    compiled_html = HTML_TEMPLATE.format(
        page_title=title,
        prefix=prefix,
        navigation_menu=nav_html,
        mobile_navigation_menu=mobile_nav_html,
        banner_section=banner_section,
        main_content=main_content
    )
    
    # Save the updated modernized HTML file back
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(compiled_html)
        # print(f"Compiled: {url_path}")
    except Exception as e:
        print(f"Error compiling {file_path}: {e}")

print("Site compilation finished successfully!")
