"""Build the homepage, service pages and brand guides using a shared shell."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json
import hashlib
import argparse
import shutil
from datetime import datetime, timezone, timedelta
from brand_profiles import BRANDS
from brand_pages import brand_content
from brand_indonesian import GUIDES, indonesian_content, indonesian_title
import fire_alarm
from ship_service_pages import (
    LEGACY_SHIP_REPAIR, PAGES as SHIP_SERVICE_PAGES, SHIP_REPAIR,
    all_services, service_content,
)
from site_content import SERVICES, CLIENTS, BRAND_GROUPS, LEADERSHIP
from landing_services import service_details, legacy_targets
from ui_components import srcset
from measurement import banner, privacy_content

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CURRENT_YEAR = datetime.now(timezone(timedelta(hours=7))).year
COMPANY_AGE = CURRENT_YEAR - 2009
BASE = "https://arayainternusa.github.io/arayaweb/"
PRODUCTION = "https://arayainternusa.co.id/araya/"
ROBOTS = "noindex, nofollow"
BUILD_TARGET = 'preview'
GOOGLE_SITE_VERIFICATION = '70qqB0I6r7SYsg7viSNXPY0CvKvSHzHTRO7Wj3n6r-Y'
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 5l7 7-7 7"/></svg>'
def asset_version(name):
    # Normalise line endings so Windows (CRLF) and Linux checkouts produce identical output.
    return hashlib.sha256((PUBLIC / 'assets' / name).read_bytes().replace(b'\r\n', b'\n')).hexdigest()[:10]

CSS_VERSION = asset_version('site.css')
JS_VERSION = asset_version('site.js')
DATE_VERSION = asset_version('company-date.js')
REDIRECT_VERSION = asset_version('service-redirect.js')
EMAIL = "cs@arayainternusa.com"
MAP = "https://www.google.com/maps/search/?api=1&query=" + quote("Gateway Citra Harmoni RKG 32-33, Taman, Sidoarjo")
JAKARTA_MAP = "https://www.google.com/maps/search/?api=1&query=" + quote("Townhouse PIK, Jakarta")


def whatsapp(topic="a project", language="en"):
    message = f"Halo Araya, saya ingin bertanya tentang {topic}." if language == 'id' else f"Hello Araya, I would like to discuss {topic}."
    return "https://wa.me/6281326396262?text=" + quote(message)


def organization():
    return {
        "@type": "ProfessionalService", "@id": BASE + "#organization",
        "name": "PT Araya Internusa", "alternateName": "Araya Internusa", "url": PRODUCTION,
        "logo": BASE + "assets/images/araya-icon.svg", "image": BASE + "assets/images/og-araya.jpg",
        "description": "Marine, industrial and automation engineering company serving Indonesia: supply, repair, modification, upgrade and retrofit.",
        "email": EMAIL, "telephone": "+6281326396262", "foundingDate": "2009",
        "founder": {"@type": "Person", "name": "Arif Fatkur Rohman"},
        "address": {"@type": "PostalAddress", "streetAddress": "Gateway Citra Harmoni RKG 32–33", "addressLocality": "Taman, Sidoarjo",
                    "addressRegion": "Jawa Timur", "postalCode": "61257", "addressCountry": "ID"},
        "location": [{"@type": "Place", "name": "Surabaya office — Sidoarjo", "address": {"@type": "PostalAddress", "streetAddress": "Gateway Citra Harmoni RKG 32–33", "addressLocality": "Taman, Sidoarjo", "addressRegion": "Jawa Timur", "postalCode": "61257", "addressCountry": "ID"}},
                     {"@type": "Place", "name": "Jakarta branch office — Townhouse PIK", "address": {"@type": "PostalAddress", "streetAddress": "Townhouse PIK", "addressLocality": "Jakarta", "addressCountry": "ID"}}],
        "areaServed": {"@type": "Country", "name": "Indonesia"},
        "knowsAbout": ["Marine automation", "Alarm monitoring systems", "Ship electrical systems", "Engine overhaul and control", "Generator synchronisation and load sharing", "Water-level and cargo monitoring", "PLC and SCADA", "Industrial machinery repair", "Crane repair", "Hazardous-area electrical equipment", "Noris", "ComAp"],
    }


def breadcrumb(route, name, language='en'):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Beranda" if language == 'id' else "Home", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": name, "item": BASE + route}]}


def service_metadata(route, name, description, areas):
    return [breadcrumb(route, name, 'id'), {
        '@type': 'Service', 'name': name, 'description': description, 'url': BASE + route,
        'provider': {'@id': BASE + '#organization'}, 'areaServed': areas,
    }]


def shell(title, description, content, route="", schema=(), *, language='en', contact_topic=None, contact_hint=None):
    prefix = "../" * route.count('/') if route else "./"
    home = prefix + "index.html"
    def ui(english, indonesian):
        return indonesian if language == 'id' else english
    brand_suffix = ui('', 'id/')
    brand_links = ''.join(f'<li><a href="{prefix}{key}/{brand_suffix}">{escape(data["name"])}</a></li>' for key, data in BRANDS.items())
    brand_footer_links = ''.join(f'<a href="{prefix}{key}/{brand_suffix}">{escape(data["name"])}</a>' for key, data in BRANDS.items())
    service_names = {'marine': 'Layanan kapal', 'industrial': 'Layanan industri', 'automation': 'Otomasi'}
    service_footer_links = ''.join(f'<a href="{home}#{key}-services">{escape(ui(data["name"], service_names[key]))}</a>' for key, data in SERVICES.items())
    if not route:
        service_footer_links += f'<a lang="id" href="./{SHIP_REPAIR}/">Perbaikan kapal</a>'
    route_key = route.split('/')[0]
    hero_brand = BRANDS.get(route_key)
    contact_topic = contact_topic or (hero_brand or SERVICES.get(route_key) or {}).get("name", "a project")
    contact_hint = contact_hint or ui(
        'Send the equipment model, a nameplate photo and the problem or change you need.',
        'Kirim model peralatan, foto pelat nama, serta kendala atau perubahan yang Anda perlukan.',
    )
    alternate_links = ''
    language_switch = ''
    if hero_brand:
        versions = {'en': (f'{route_key}/', 'English'), 'id': (f'{route_key}/id/', 'Bahasa Indonesia')}
        alternate_links = ''.join(f'\n  <link rel="alternate" hreflang="{lang}" href="{BASE}{path}">' for lang, (path, _) in versions.items())
        choices = []
        for lang, (path, label) in versions.items():
            if lang == language:
                choices.append(f'<span lang="{lang}" aria-current="page">{label}</span>')
            else:
                choices.append(f'<a href="{prefix}{path}" lang="{lang}" hreflang="{lang}">{label}</a>')
        language_switch = f'<div class="brand-language"><nav class="container" aria-label="{ui("Language", "Bahasa")}">{"".join(choices)}</nav></div>'
    tracking_target = BUILD_TARGET if route.strip('/') not in SERVICES else 'off'
    image_preload = ''
    if hero_brand:
        image_preload = f'<link rel="preload" as="image" href="{prefix}assets/images/{hero_brand["image"]}" fetchpriority="high">'
    elif not route:
        image_preload = f'<link rel="preload" as="image" href="./assets/images/ship-1400.webp" imagesrcset="{srcset((("ship-800.webp", 800), ("ship-1400.webp", 1400)))}" imagesizes="100vw" fetchpriority="high">'
    verification = ''
    if BUILD_TARGET == 'production' and not route:
        verification = f'\n  <meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">'
    def nav(label, target):
        return f'<a href="{home}{target}">{label}</a>'
    return f'''<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.documentElement.classList.add('js')</script>
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="robots" content="{ROBOTS}">{verification}
  <meta name="theme-color" content="#1e2023">
  <link rel="canonical" href="{BASE}{route}">{alternate_links}
  <meta property="og:site_name" content="PT Araya Internusa">
  <meta property="og:title" content="{escape(title, quote=True)}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:type" content="website"><meta property="og:url" content="{BASE}{route}">
  <meta property="og:image" content="{BASE}assets/images/og-araya.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" sizes="64x64" href="{prefix}assets/images/favicon.png?v={asset_version("images/favicon.png")}">
  <link rel="icon" type="image/svg+xml" sizes="any" href="{prefix}assets/images/araya-icon.svg?v={asset_version("images/araya-icon.svg")}">
  <link rel="preload" href="{prefix}assets/fonts/space-grotesk.woff2" as="font" type="font/woff2" crossorigin>
{"  " + image_preload if image_preload else ""}
  <link rel="stylesheet" href="{prefix}assets/site.css?v={CSS_VERSION}">
  <link rel="stylesheet" href="{prefix}assets/measurement.css?v={asset_version('measurement.css')}">
  <script src="{prefix}assets/company-date.js?v={DATE_VERSION}" defer></script>
  <script src="{prefix}assets/site.js?v={JS_VERSION}" defer></script>
  <script src="{prefix}assets/measurement.js?v={asset_version('measurement.js')}" data-measurement="{tracking_target}" defer></script>
  <script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": [organization(), *schema]}, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip-link" href="#main">{ui('Skip to content', 'Langsung ke konten')}</a>
{banner(prefix, language)}
<header class="site-header">
  <div class="utility"><div class="container utility-inner"><span>{ui('Surabaya &amp; Jakarta Offices', 'Kantor Surabaya &amp; Jakarta')}</span><a data-contact-location="utility" href="mailto:{EMAIL}">{EMAIL}</a><a data-contact-location="utility" href="{whatsapp(ui('a project', 'proyek saya'), language)}">WhatsApp: +62 813 2639 6262</a></div></div>
  <div class="container navigation">
    <a class="brand" href="{home}" aria-label="{ui('PT Araya Internusa home', 'Beranda PT Araya Internusa')}"><img src="{prefix}assets/images/araya-logo.svg" alt="PT Araya Internusa" width="4165" height="961"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-navigation"><span>Menu</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    <nav class="main-nav" id="main-navigation" aria-label="{ui('Main navigation', 'Navigasi utama')}">
      {nav(ui('Home', 'Beranda'), '')}{nav(ui('About Us', 'Tentang Kami'), '#about')}{nav(ui('Our Services', 'Layanan'), '#services')}{nav(ui('Our Clients', 'Klien Kami'), '#clients')}<details class="brand-menu"><summary>{ui('Brand Partners', 'Mitra Merek')}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><ul class="brand-dropdown">{brand_links}</ul></details>
      <a class="nav-contact" href="#contact">{ui('Contact Us', 'Hubungi Kami')} {ARROW}</a>
    </nav>
  </div>
</header>
{language_switch}
<main id="main">{content}</main>
<section class="contact" id="contact" aria-labelledby="contact-heading">
  <div class="container contact-intro"><div><p class="eyebrow">{ui('GET IN TOUCH', 'HUBUNGI KAMI')}</p><h2 id="contact-heading">{ui('Let’s find the right solution.', 'Diskusikan kebutuhan Anda')}</h2><p>{escape(contact_hint)}</p></div><div class="contact-actions"><a class="button" data-contact-location="contact" href="{whatsapp(contact_topic, language)}">{ui('Chat on WhatsApp', 'Hubungi via WhatsApp')} {ARROW}</a><a class="button button-outline" data-contact-location="contact" href="mailto:{EMAIL}">{ui('Email our team', 'Kirim email')} {ARROW}</a></div></div>
  <div class="container footer-grid">
    <div class="footer-company"><img src="{prefix}assets/images/araya-logo.svg" alt="PT Araya Internusa" width="4165" height="961" loading="lazy"><p><span class="company-age-copy"><span data-company-age>{COMPANY_AGE}</span> {ui('years of ', 'tahun pengalaman dalam ')}</span>{ui('marine, industrial and automation engineering across Indonesia.', 'rekayasa kapal, industri, dan otomasi di seluruh Indonesia.')}</p></div>
    <div><h3>{ui('Explore Araya', 'Jelajahi Araya')}</h3><a href="{home}#about">{ui('About Us', 'Tentang Kami')}</a>{service_footer_links}{brand_footer_links}<a href="{home}#clients">{ui('Our Clients', 'Klien Kami')}</a></div>
    <div><h3>{ui('Branch Offices', 'Kantor Cabang')}</h3><p><strong>{ui('Surabaya office', 'Kantor Surabaya')}</strong><a href="{MAP}">Gateway Citra Harmoni RKG 32–33<br>Taman, Sidoarjo<br>Jawa Timur 61257, Indonesia</a></p><p><strong>Jakarta</strong><a href="{JAKARTA_MAP}">Townhouse PIK<br>Jakarta, Indonesia</a></p></div>
    <div><h3>{ui('Contact Us', 'Hubungi Kami')}</h3><a data-contact-location="footer" href="mailto:{EMAIL}">{EMAIL}</a><a data-contact-location="footer" href="{whatsapp(contact_topic, language)}">WhatsApp: +62 813 2639 6262</a><p class="contact-note">{ui('Share your system details with our team.', 'Sampaikan detail sistem Anda kepada tim kami.')}</p></div>
  </div>
</section>
<footer class="copyright"><div class="container"><span>© <span class="company-age-copy" data-current-year>{CURRENT_YEAR}</span> PT Araya Internusa.</span><div class="privacy-links"><a href="{prefix}privacy/">{ui('Privacy notice', 'Pemberitahuan privasi (English)')}</a><button class="privacy-choice" type="button" data-consent-action="open">{ui('Privacy choices', 'Pilihan privasi')}</button></div></div></footer>
</body></html>'''


def home():
    service_sections = ''.join(service_details(key, service) for key, service in SERVICES.items())
    leadership = ''.join(f'<figure class="leadership-card"><img src="./assets/images/{person["image"]}-720.webp" srcset="{srcset(((person["image"] + "-400.webp", 400), (person["image"] + "-720.webp", 720)))}" sizes="(max-width: 680px) calc(100vw - 40px), (max-width: 1200px) calc((100vw - 116px) / 3), 341px" alt="{escape(person["name"], quote=True)}" width="720" height="{person["height"]}" loading="lazy" fetchpriority="low" decoding="async"><figcaption><h3>{escape(person["name"])}</h3><p>{escape(person["role"])}</p></figcaption></figure>' for person in LEADERSHIP)
    # Not lazy-loaded: logos clipped sideways inside the scrolling strip would never load.
    clients = ''.join(f'<li><img{' class="is-emblem"' if c.get("emblem") else ''} src="./assets/images/{c["logo"]}" alt="{escape(c["name"], quote=True)}" width="{c["width"]}" height="{c["height"]}" fetchpriority="low" decoding="async"></li>' for c in CLIENTS)
    groups = ''.join(f'<div><h4>{escape(title)}</h4><p>{escape(" · ".join(brands))}</p></div>' for title, brands in BRAND_GROUPS)
    return f'''
<section class="hero" aria-labelledby="hero-heading">
  <img class="hero-photo" src="./assets/images/ship-1400.webp" srcset="{srcset((("ship-800.webp", 800), ("ship-1400.webp", 1400)))}" sizes="100vw" alt="PELNI passenger vessel alongside a quay, from Araya’s marine project photographs" width="1400" height="784" fetchpriority="high">
  <div class="hero-shade"></div>
  <div class="container hero-content"><h1 id="hero-heading">Marine, industrial &amp;<br>automation engineering<br><span>across Indonesia.</span></h1><p class="hero-description">Supply, repair, modification, upgrade and retrofit for marine equipment, industrial systems and automation.</p><div class="hero-actions"><a class="button" data-contact-location="hero" href="{whatsapp()}">Discuss your project {ARROW}</a><a class="button button-outline" href="#services">Our services {ARROW}</a></div></div>
  <div class="hero-index" aria-hidden="true"><span data-count="1500" data-count-suffix="+">1,500+</span> / PROJECTS <span class="company-age-copy">OVER <span class="company-age" data-count data-company-age>{COMPANY_AGE}</span> YEARS</span></div>
</section>
<section class="section about" id="about"><div class="container about-grid">
  <div class="about-heading"><p class="eyebrow">ABOUT PT ARAYA INTERNUSA</p><h2><span class="company-age-copy"><span data-count data-company-age>{COMPANY_AGE}</span> years of<br></span>professional engineering.</h2></div>
  <div class="about-media"><img src="./assets/images/team.webp" alt="Araya technicians working together in a vessel’s engine room" width="600" height="600" loading="eager" fetchpriority="low" decoding="async"><div class="since"><strong>2009</strong><span>Where our story began</span></div></div>
  <div class="about-copy"><p class="lead">Professional engineering for marine and industrial systems, backed by certification and international technical expertise.</p><p>Founded in 2009 by Arif Fatkur Rohman, PT Araya Internusa brings together repair, modification, upgrade and retrofit experience. International technical backing includes HIT (Haven- und Industrietechnik GmbH), Noris Automation and ComAp.</p><p>Araya serves projects across Sumatra, Jawa, Kalimantan, Sulawesi and Papua, with offices in Surabaya and Jakarta. We also extend the life of obsolete or end-of-sale equipment with practical, reliable solutions.</p><div class="scope-list"><span>Marine</span><span>Industrial</span><span>Automation &amp; electrical</span></div><p class="working-practice"><strong>Certified &amp; experienced</strong><br>Professional engineering experience, backed by certification and international technical support.</p></div>
</div></section>
<section class="section section-muted" id="services"><div class="container">
  <div class="section-heading"><div><p class="eyebrow">WHAT WE DO</p><h2>Our services</h2></div><p>Supply, repair, upgrade and retrofit for marine and industrial systems.</p></div>
  <div class="landing-services">{service_sections}</div>
</div></section>
<section class="section projects" id="clients"><div class="container">
  <div class="section-heading"><div><p class="eyebrow">OUR CLIENTS</p><h2>Clients who<br>trust Araya.</h2></div><p>Organisations that trust PT Araya Internusa with their engineering and automation work.</p></div>
  <div class="project-reach"><div class="project-total"><strong data-count="1500" data-count-suffix="+">1,500+</strong><span>projects across Indonesia</span></div><div class="project-coverage"><h3>Across the archipelago</h3><ul><li>Sumatra</li><li>Jawa</li><li>Kalimantan</li><li>Sulawesi</li><li>Papua</li></ul></div></div>
  <div class="client-marquee"><ul class="client-track" aria-label="Selected clients">{clients}</ul><ul class="client-track" aria-hidden="true">{clients}</ul></div>
</div></section>
<section class="section" id="brands"><div class="container">
  <div class="section-heading"><div><p class="eyebrow">BRAND PARTNERS &amp; EQUIPMENT</p><h2>Specialist partners.<br>Multi-brand expertise.</h2></div><p>In Indonesia, PT Araya Internusa is the sole authorised distributor for NORIS and an authorised distributor for ComAp. We supply equipment and provide engineering support for both brands.</p></div>
  <div class="brand-grid">
    <article class="brand-panel"><div class="brand-name">NORIS<span>{escape(BRANDS["noris"]["legal_name"])}</span></div><h3>Instruments &amp; sensors.<br>Marine automation.</h3><p>{escape(BRANDS['noris']['home_summary'])}</p><a class="text-link" href="./noris/id/" lang="id">{indonesian_title('noris')} {ARROW}</a></article>
    <article class="brand-panel"><div class="brand-name">ComAp<span>{escape(BRANDS["comap"]["legal_name"])}</span></div><h3>Engine control.<br>Power management.<br>Load sharing.</h3><p>{escape(BRANDS['comap']['home_summary'])}</p><a class="text-link" href="./comap/id/" lang="id">{indonesian_title('comap')} {ARROW}</a></article>
  </div>
  <div class="equipment-brands"><h3>We also work on equipment from</h3><div class="equipment-brand-grid">{groups}</div><p class="equipment-more">and many more...</p></div>
</div></section>
<section class="section leadership" id="leadership" aria-labelledby="leadership-heading"><div class="container"><div class="section-heading"><div><p class="eyebrow">OUR PEOPLE</p><h2 id="leadership-heading">Leadership &amp; management.</h2></div></div><div class="leadership-grid">{leadership}</div></div></section>'''


def legacy_service_page(key, service):
    target = f'../index.html#{key}-services'
    content = f'<section class="section"><div class="container"><h1>{escape(service["name"])} services</h1><p class="lead">Our engineering services are on the main Araya page.</p><a class="button" href="{target}">View {escape(service["short"])} services {ARROW}</a></div></section>'
    html = shell(service['title'], service['description'], content, key + '/')
    html = html.replace(f'<link rel="canonical" href="{BASE}{key}/">', f'<link rel="canonical" href="{BASE}">')
    if ROBOTS == 'index, follow':
        html = html.replace('content="index, follow"', 'content="noindex, follow"')
    config = json.dumps(legacy_targets(key, service))
    return html.replace('</body>', f'<script type="application/json" id="legacy-service-targets">{config}</script><script src="../assets/service-redirect.js?v={REDIRECT_VERSION}" defer></script></body>')


def write(route, html):
    folder = PUBLIC / route if route else PUBLIC
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(html, encoding="utf-8")


def main():
    global PUBLIC, BASE, PRODUCTION, ROBOTS, BUILD_TARGET
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=('preview', 'production'), default='preview')
    args = parser.parse_args()
    BUILD_TARGET = args.target
    if args.target == 'production':
        BASE = PRODUCTION = 'https://arayainternusa.co.id/'
        ROBOTS = 'index, follow'
        source = PUBLIC / 'assets'
        PUBLIC = ROOT / 'dist/production'
        if (not PUBLIC.resolve().is_relative_to(ROOT.resolve()) or PUBLIC.parent.is_symlink()
                or PUBLIC.is_symlink() or source.is_symlink()
                or any(p.is_symlink() for p in source.rglob('*'))
                or any(p.is_symlink() for p in PUBLIC.rglob('*'))):
            raise ValueError('Build paths must not contain symlinks')
        PUBLIC.mkdir(parents=True, exist_ok=True)
        (PUBLIC / LEGACY_SHIP_REPAIR / 'index.html').unlink(missing_ok=True)
        shutil.copytree(source, PUBLIC / 'assets', dirs_exist_ok=True)
    routes = [""]
    website = {"@type": "WebSite", "@id": BASE + "#website", "name": "PT Araya Internusa", "url": BASE, "publisher": {"@id": BASE + "#organization"}}
    service_schema = [{"@type": "Service", "name": service["name"] + " engineering services", "serviceType": service["name"], "url": BASE + "#" + key + "-services", "provider": {"@id": BASE + "#organization"}, "areaServed": {"@type": "Country", "name": "Indonesia"}, "description": service["description"]} for key, service in SERVICES.items()]
    write("", shell("Marine & Industrial Automation Indonesia | Araya Internusa",
                    "Ship maintenance, repair and retrofit across Indonesia. Surabaya and Jakarta offices. Sole authorised NORIS distributor and authorised ComAp distributor.",
                    home(), schema=[website, *service_schema]))
    for key, service in SERVICES.items():
        write(key, legacy_service_page(key, service))
    for key, data in BRANDS.items():
        # Keep the visible FAQs. Google retired FAQ rich results in May 2026.
        write(key, shell(data['title'], data['description'], brand_content(key, data, ARROW), key + '/', [breadcrumb(key + '/', data['name'])]))
        routes.append(key + '/')
        route = f'{key}/id/'
        title = indonesian_title(key)
        write(route, shell(f'{title} | Araya Internusa', GUIDES[key]['description'],
                           indonesian_content(key, '../../'), route, [breadcrumb(route, title, 'id')], language='id'))
        routes.append(route)
    local_service_areas = [{'@type': 'City', 'name': 'Surabaya'},
                           {'@type': 'AdministrativeArea', 'name': 'Gresik'},
                           {'@type': 'City', 'name': 'Jakarta'}]
    route = fire_alarm.ROUTE
    fire_content = fire_alarm.fire_alarm_content() + all_services(route.rstrip('/'), ARROW)
    write(route, shell(fire_alarm.TITLE, fire_alarm.DESCRIPTION, fire_content, route,
                       service_metadata(route, fire_alarm.HEADING, fire_alarm.DESCRIPTION, local_service_areas),
                       language='id', contact_topic='sistem fire alarm', contact_hint=fire_alarm.CONTACT_HINT))
    routes.append(route)
    ship_service_areas = [*local_service_areas, {'@type': 'Country', 'name': 'Indonesia'}]
    for slug, page in SHIP_SERVICE_PAGES.items():
        route = f'{slug}/'
        content = service_content(page) + all_services(slug, ARROW)
        write(route, shell(f'{page.title} | Araya', page.description, content, route,
                           service_metadata(route, page.heading, page.description, ship_service_areas),
                           language='id', contact_topic=page.contact_topic, contact_hint=page.contact_hint))
        routes.append(route)
    if args.target == 'preview':
        target = f'../{SHIP_REPAIR}/'
        write(LEGACY_SHIP_REPAIR, f'''<!doctype html>
<html lang="id"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0;url={target}">
<link rel="canonical" href="{BASE}{SHIP_REPAIR}/">
<title>Jasa Perbaikan Kapal | Araya</title></head>
<body><main><h1>Jasa Perbaikan Kapal</h1><p><a href="{target}">Buka halaman perbaikan kapal</a></p></main></body></html>''')
    write('privacy', shell('Privacy notice | PT Araya Internusa', 'How PT Araya Internusa handles website analytics, your privacy choices and contact enquiries.', privacy_content(), 'privacy/', [breadcrumb('privacy/', 'Privacy notice')]))
    routes.append('privacy/')
    urls = ''.join(f'<url><loc>{BASE}{route}</loc><lastmod>{datetime.now(timezone(timedelta(hours=7))).date().isoformat()}</lastmod></url>' for route in routes)
    (PUBLIC / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    # Crawlers must be able to read the preview's noindex meta tags.
    robots = f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n' if args.target == 'production' else 'User-agent: *\nAllow: /\n'
    (PUBLIC / 'robots.txt').write_text(robots, encoding='utf-8')
    print(f"Built {args.target}: {len(routes)} content pages, compatibility redirects, sitemap.xml and robots.txt.")


if __name__ == "__main__":
    main()
