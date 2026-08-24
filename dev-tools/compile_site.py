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
    "villa-del-rosario": "Villa del Rosario",
    "sardinata": "Sardinata",
    "chinacota": "Chinácota"
}

# Zone mapping for interactive E.D.S. selector
MUNI_STATIONS = {
    "san-cayetano": {"name": "San Cayetano", "stations": [
        {"name": "EDS Parador De Occidente", "slug": "eds-parador-de-occidente"},
        {"name": "EDS El Eden Campestre", "slug": "eds-el-eden-campestre"},
        {"name": "EDS Peralonso", "slug": "eds-peralonso"},
        {"name": "EDS Zona San Isidro", "slug": "eds-zona-san-isidro"},
        {"name": "Zona Refrescante La Estación", "slug": "zona-refrescante-la-estacion"},
    ]},
    "cucuta": {"name": "Cúcuta", "stations": [
        {"name": "EDS La Javilla", "slug": "eds-la-javilla"},
        {"name": "Estacion De Servicio Rivera De Las Americas", "slug": "estacion-de-servicio-rivera-de-las-americas"},
        {"name": "Estación De Servicios Sol Del Oriente", "slug": "estacion-de-servicios-sol-del-oriente"},
        {"name": "Estación De Servicio Ventura", "slug": "estacion-de-servicio-ventura"},
        {"name": "EDS Tel Aviv", "slug": "eds-tel-aviv"},
        {"name": "E.D.S La Alejandra", "slug": "e-d-s-la-alejandra"},
        {"name": "EDS Patillales", "slug": "eds-patillales"},
        {"name": "EDS El Punto Camionero", "slug": "eds-el-punto-camionero"},
        {"name": "EDS El Peñon", "slug": "eds-el-penon"},
        {"name": "EDS Codirco", "slug": "eds-codirco"},
        {"name": "Estacion De Servicio Tecnipetrol", "slug": "estacion-de-servicio-tecnipetrol"},
        {"name": "EDS El Nuevo Terminal", "slug": "eds-el-nuevo-terminal"},
        {"name": "EDS El Paso Cucuta", "slug": "eds-el-paso-cucuta"},
        {"name": "Estacion De Servicios Aguaclara", "slug": "estacion-de-servicios-aguaclara"},
        {"name": "EDS Balconcitos", "slug": "eds-balconcitos"},
        {"name": "Cooperativa Agropecuaria Del Norte De Santander", "slug": "cooperativa-agropecuaria-del-norte-de-santander"},
        {"name": "Estacion De Servicio Puerto Via", "slug": "estacion-de-servicio-puerto-via"},
        {"name": "Estación De Servicio Riviera Plaza", "slug": "estacion-de-servicio-riviera-plaza"},
        {"name": "Estacion De Servicio Miraflores", "slug": "estacion-de-servicio-miraflores"},
        {"name": "EDS Gran Oripaya", "slug": "eds-gran-oripaya"},
        {"name": "E.D.S. El Gran Rancho Rey", "slug": "e-d-s-el-gran-rancho-rey"},
        {"name": "Estacion De Servicio Bogota", "slug": "estacion-de-servicio-bogota"},
    ]},
    "los-patios": {"name": "Los Patios", "stations": [
        {"name": "Estacion De Servicio EDS Llanitos", "slug": "estacion-de-servicio-eds-llanitos"},
        {"name": "Estacion De Servicio Parador Andino", "slug": "estacion-de-servicio-parador-andino"},
        {"name": "Estacion De Servicio Los Vados", "slug": "estacion-de-servicio-los-vados"},
    ]},
    "villa-del-rosario": {"name": "Villa del Rosario", "stations": [
        {"name": "E.D.S. La Internacional", "slug": "e-d-s-la-internacional"},
        {"name": "EDS La Frontera", "slug": "eds-la-frontera"},
        {"name": "EDS Los Samanes De Villa Del Rosario", "slug": "eds-los-samanes-de-villa-del-rosario"},
        {"name": "Estacion De Servicio Expendio De Acpm Y Lubricantes El Puente", "slug": "estacion-de-servicio-expendio-de-acpm-y-lubricantes-el-puente"},
    ]},
    "el-zulia": {"name": "El Zulia", "stations": [
        {"name": "Estacion De Servicio Cadriada", "slug": "estacion-de-servicio-cadriada"},
        {"name": "Estacion De Servicio Seycar", "slug": "estacion-de-servicio-seycar"},
        {"name": "Estación De Servicio Jonas", "slug": "estacion-de-servicio-jonas"},
        {"name": "Estación De Servicio Las Lomas", "slug": "estacion-de-servicio-las-lomas"},
        {"name": "Estación De Servicio La Plazoleta", "slug": "estacion-de-servicio-la-plazoleta"},
        {"name": "Estacion De Servicio Silvania Sas", "slug": "estacion-de-servicio-silvania-sas"},
        {"name": "Estacion De Servicio Borriqueros", "slug": "estacion-de-servicio-borriqueros"},
        {"name": "Estacion De Servicio Arrayanes", "slug": "estacion-de-servicio-arrayanes"},
        {"name": "Estacion De Servicio Los Rios", "slug": "estacion-de-servicio-los-rios"},
        {"name": "Estacion De Servicio La Ceiba Jo El Zulia", "slug": "estacion-de-servicio-la-ceiba-jo-el-zulia"},
        {"name": "E.D.S La Primavera S.A.S", "slug": "e-d-s-la-primavera-s-a-s"},
        {"name": "EDS Jesus De Nazaret", "slug": "eds-jesus-de-nazaret"},
        {"name": "E.D.S La Represa", "slug": "e-d-s-la-represa"},
        {"name": "EDS Zulinorte", "slug": "eds-zulinorte"},
        {"name": "EDS La Zuliana", "slug": "eds-la-zuliana"},
        {"name": "Estacion De Servicio Mia Cj", "slug": "estacion-de-servicio-mia-cj"},
        {"name": "Estacion De Servicio Los Sanchez", "slug": "estacion-de-servicio-los-sanchez"},
        {"name": "Estación De Servicio El Aventino", "slug": "estacion-de-servicio-el-aventino"},
        {"name": "Estacion De Servicio Risarlda Jose", "slug": "estacion-de-servicio-risarlda-jose"},
        {"name": "Estacion De Servicios La Gran Zuliana", "slug": "estacion-de-servicios-la-gran-zuliana"},
        {"name": "E.D.S. Torrasa El Zulia", "slug": "e-d-s-torrasa-el-zulia"},
        {"name": "Estacion De Servicio Israel", "slug": "estacion-de-servicio-israel"},
        {"name": "Estacion De Servicio Astilleros Ciro", "slug": "estacion-de-servicio-astilleros-ciro"},
        {"name": "Estacion De Servicio La Virgen", "slug": "estacion-de-servicio-la-virgen"},
    ]},
    "tibu": {"name": "Tibú", "stations": [
        {"name": "Estación De Servicio Km 23", "slug": "estacion-de-servicio-km-23"},
        {"name": "Estacion De Servicio La Nueva Florida", "slug": "estacion-de-servicio-la-nueva-florida"},
        {"name": "Estacion De Servicio Jardin Del Norte", "slug": "estacion-de-servicio-jardin-del-norte"},
        {"name": "EDS Altoviento", "slug": "eds-altoviento"},
        {"name": "Estacion De Servicio Castillo Alvarez", "slug": "estacion-de-servicio-castillo-alvarez"},
        {"name": "EDS La Gran Estación Fyc", "slug": "eds-la-gran-estacion-fyc"},
        {"name": "E.D.S Campo Dos", "slug": "e-d-s-campo-dos"},
        {"name": "E.D.S. La Gabarra Syo S.A.S.", "slug": "e-d-s-la-gabarra-syo-s-a-s"},
        {"name": "EDS Los Angeles F Y C", "slug": "eds-los-angeles-f-y-c"},
        {"name": "Estacion De Servicio Lagunitas", "slug": "estacion-de-servicio-lagunitas"},
        {"name": "Estación De Servicio Monterrey Fabio Y Ciro", "slug": "estacion-de-servicio-monterrey-fabio-y-ciro"},
        {"name": "Estacion De Servicio La Cuatro Acosta", "slug": "estacion-de-servicio-la-cuatro-acosta"},
    ]},
    "bucarasica": {"name": "Bucarasica", "stations": [
        {"name": "Estacion De Servicio El Oasis Acv", "slug": "estacion-de-servicio-el-oasis-acv"},
        {"name": "Estacion De Servicio El Poblado Net", "slug": "estacion-de-servicio-el-poblado-net"},
    ]},
    "sardinata": {"name": "Sardinata", "stations": [
        {"name": "EDS Gremon", "slug": "eds-gremon"},
        {"name": "E.D.S La Virgen Sr Sas", "slug": "e-d-s-la-virgen-sr-sas"},
    ]},
    "toledo": {"name": "Toledo", "stations": [
        {"name": "Estacion De Servicio Marnell S.A.S.", "slug": "estacion-de-servicio-marnell-s-a-s"},
        {"name": "E.D.S. Don Diego", "slug": "e-d-s-don-diego"},
        {"name": "Estacion De Servicio Santa Rita", "slug": "estacion-de-servicio-santa-rita"},
    ]},
    "ragonvalia": {"name": "Ragonvalia", "stations": [
        {"name": "Estacion De Servicio El Pedregal Ragonvalia", "slug": "estacion-de-servicio-el-pedregal-ragonvalia"},
        {"name": "Estacion De Servicio La Floresta Ragonvalia", "slug": "estacion-de-servicio-la-floresta-ragonvalia"},
    ]},
    "chinacota": {"name": "Chinácota", "stations": [
        {"name": "E.D.S Chitacomar 1", "slug": "e-d-s-chitacomar-1"},
    ]},
    "pamplona": {"name": "Pamplona", "stations": [
        {"name": "Estacion De Servicio Troco", "slug": "estacion-de-servicio-troco"},
    ]},
    "rio-de-oro": {"name": "Río de Oro", "stations": [
        {"name": "Estacion De Servicio La Labranza", "slug": "estacion-de-servicio-la-labranza"},
        {"name": "Estacion De Servicio Jm Peaje", "slug": "estacion-de-servicio-jm-peaje"},
    ]},
    "la-esperanza": {"name": "La Esperanza", "stations": [
        {"name": "Estacion De Servicio La Victoria 1", "slug": "estacion-de-servicio-la-victoria-1"},
        {"name": "EDS Cafe Corriendo", "slug": "eds-cafe-corriendo"},
        {"name": "Estacion De Servicio La Gran Silvana I", "slug": "estacion-de-servicio-la-gran-silvana-i"},
        {"name": "Estacion De Servicio Gedeon", "slug": "estacion-de-servicio-gedeon"},
        {"name": "Estacion De Servicio La Pedregosa", "slug": "estacion-de-servicio-la-pedregosa"},
    ]},
    "hacari": {"name": "Hacarí", "stations": [
        {"name": "Estacion De Servicio La Palma Hacari", "slug": "estacion-de-servicio-la-palma-hacari"},
        {"name": "EDS Duran", "slug": "eds-duran"},
        {"name": "Estacion De Servicio Quebraditas", "slug": "estacion-de-servicio-quebraditas"},
    ]},
    "la-playa": {"name": "La Playa", "stations": [
        {"name": "EDS El Tunal Sas", "slug": "eds-el-tunal-sas"},
    ]},
    "teorama": {"name": "Teorama", "stations": [
        {"name": "EDS San Jorge G", "slug": "eds-san-jorge-g"},
        {"name": "Estacion De Servicio San Pablo", "slug": "estacion-de-servicio-san-pablo"},
    ]},
    "ocana": {"name": "Ocaña", "stations": [
        {"name": "Estacion De Servicios Leomar", "slug": "estacion-de-servicios-leomar"},
        {"name": "Estación De Servicio Los Barbatuscos", "slug": "estacion-de-servicio-los-barbatuscos"},
        {"name": "Estacion De Servicio Patillal", "slug": "estacion-de-servicio-patillal"},
        {"name": "Estación De Servicio El Oasis Ocaña", "slug": "estacion-de-servicio-el-oasis-ocana"},
        {"name": "Estación De Servicio Ocañerita", "slug": "estacion-de-servicio-ocanerita"},
        {"name": "Servicentro Ocana", "slug": "servicentro-ocana"},
        {"name": "Estacion De Servicio Cootransunidos", "slug": "estacion-de-servicio-cootransunidos"},
        {"name": "Estacion De Servicio El Limon", "slug": "estacion-de-servicio-el-limon"},
        {"name": "Estacion De Servicio Rodeo", "slug": "estacion-de-servicio-rodeo"},
        {"name": "Estacion De Servicio Agua De La Virgen", "slug": "estacion-de-servicio-agua-de-la-virgen"},
        {"name": "Estacion De Servicio La Once", "slug": "estacion-de-servicio-la-once"},
        {"name": "Estacion De Servicio La Leonelda", "slug": "estacion-de-servicio-la-leonelda"},
        {"name": "Estacion De Servicio El Terminal De Ocaña", "slug": "estacion-de-servicio-el-terminal-de-ocana"},
        {"name": "Estacion De Servicio Cootranshacaritama", "slug": "estacion-de-servicio-cootranshacaritama"},
        {"name": "Estacion De Servicio Circunvalar", "slug": "estacion-de-servicio-circunvalar"},
        {"name": "Estación De Servicio Luis Fernando", "slug": "estacion-de-servicio-luis-fernando"},
        {"name": "Servicentro Avenida", "slug": "servicentro-avenida"},
    ]},
    "el-carmen": {"name": "El Carmen", "stations": [
        {"name": "E.D.S. La Villanueva", "slug": "e-d-s-la-villanueva"},
        {"name": "Estacion De Servicio La Troncal Del Carbon", "slug": "estacion-de-servicio-la-troncal-del-carbon"},
    ]},
    "convencion": {"name": "Convención", "stations": [
        {"name": "Estacion De Servicio Convencion", "slug": "estacion-de-servicio-convencion"},
        {"name": "Estacion De Gasolina Las Mercedes", "slug": "estacion-de-gasolina-las-mercedes"},
    ]},
    "cachira": {"name": "Cáchira", "stations": [
        {"name": "EDS Balmoral S.A.S", "slug": "eds-balmoral-s-a-s"},
        {"name": "EDS Las Marias S.A.S", "slug": "eds-las-marias-s-a-s"},
    ]},
    "abrego": {"name": "Ábrego", "stations": [
        {"name": "Estacion De Servicio Marien", "slug": "estacion-de-servicio-marien"},
        {"name": "Estacion De Servicio La Estrella De David", "slug": "estacion-de-servicio-la-estrella-de-david"},
        {"name": "Estacion De Servicio El Tun-tun", "slug": "estacion-de-servicio-el-tun-tun"},
        {"name": "Estacion De Servicio El Molino De Abrego", "slug": "estacion-de-servicio-el-molino-de-abrego"},
        {"name": "Estacion De Servicio La Cruz", "slug": "estacion-de-servicio-la-cruz"},
        {"name": "Estacion De Servicio Multiservicios Los Sauces", "slug": "estacion-de-servicio-multiservicios-los-sauces"},
        {"name": "Estacion De Servicio Oropoma", "slug": "estacion-de-servicio-oropoma"},
    ]},
}

RETAINED_STATIONS = [
    {"muni_slug": "cucuta-2", "name": "Cúcuta (Zona Urbana)"},
    {"muni_slug": "tibu-2", "name": "Tibú (Zona Urbana)"},
    {"muni_slug": "el-tarra", "name": "El Tarra"},
    {"muni_slug": "san-calixto", "name": "San Calixto"},
]

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
                        <li><a href="{prefix}estaciones/sardinata/" class="dropdown-item-link">Sardinata</a></li>
                    </ul>
                </li>
                <li class="dropdown-submenu">
                    <a href="{prefix}estaciones/oriental/" class="dropdown-item-link">E.D.S SurOriental <i class="fa-solid fa-chevron-right" style="font-size: 0.65rem; float: right; margin-top: 0.25rem;"></i></a>
                    <ul class="dropdown-submenu-menu">
                        <li><a href="{prefix}estaciones/toledo/" class="dropdown-item-link">Toledo</a></li>
                        <li><a href="{prefix}estaciones/ragonvalia/" class="dropdown-item-link">Ragonvalia</a></li>
                        <li><a href="{prefix}estaciones/chinacota/" class="dropdown-item-link">Chinácota</a></li>
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

# Generate E.D.S Municipio Finder Grid HTML (grouped by municipio, with headings)
zone_grid_html = ""
eds_tabs_html = '<button class="eds-tab-btn tab-active" data-muni-target="all">Todas</button>\n'
for muni_slug, muni_data in MUNI_STATIONS.items():
    muni_name = muni_data["name"]
    muni_stations = muni_data["stations"]
    eds_tabs_html += f'                    <button class="eds-tab-btn" data-muni-target="{muni_slug}">{muni_name}</button>\n'
    zone_grid_html += f"""
        <div class="zone-muni-heading" data-muni="{muni_slug}">{muni_name} <span class="zone-muni-count">({len(muni_stations)})</span></div>
        """
    for station in muni_stations:
        zone_grid_html += f"""
        <div class="station-card" data-muni="{muni_slug}">
            <div class="station-icon">
                <i class="fa-solid fa-gas-pump"></i>
            </div>
            <h4>{station['name']}</h4>
            <a href="./estaciones/{station['slug']}/" class="station-link-btn">Ver Estación</a>
        </div>
        """

for retained in RETAINED_STATIONS:
    muni_slug = retained["muni_slug"]
    name = retained["name"]
    eds_tabs_html += f'                    <button class="eds-tab-btn" data-muni-target="{muni_slug}">{name}</button>\n'
    zone_grid_html += f"""
        <div class="zone-muni-heading" data-muni="{muni_slug}">{name} <span class="zone-muni-count">(1)</span></div>
        <div class="station-card" data-muni="{muni_slug}">
            <div class="station-icon">
                <i class="fa-solid fa-gas-pump"></i>
            </div>
            <h4>{name}</h4>
            <a href="./estaciones/{muni_slug}/" class="station-link-btn">Ver Estación</a>
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
                    {eds_tabs_html}                </div>
                
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
