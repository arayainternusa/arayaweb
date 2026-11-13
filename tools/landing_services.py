"""Engineering services live on the company landing page."""
from html import escape
from fire_alarm import ROUTE as FIRE_ALARM_ROUTE
from ship_service_pages import CRANES, ELECTRICAL, ENGINES, MANOEUVRING, RETROFIT
from ui_components import DISCLOSURE_ICON, srcset


MARINE_SCOPE_LINKS = {
    'alarms': (
        (FIRE_ALARM_ROUTE.rstrip('/'), 'Instalasi dan perbaikan fire alarm'),
        (RETROFIT, 'Otomasi & monitoring kapal'),
    ),
    'engines': ((ENGINES, 'Perbaikan mesin kapal'),),
    'propulsion': ((MANOEUVRING, 'Perbaikan kemudi & manuver kapal'),),
    'automation': ((ELECTRICAL, 'Instalasi dan perbaikan kelistrikan kapal'),),
    'cranes': ((CRANES, 'Perbaikan crane kapal & industri'),),
}


def service_details(key, service):
    scope_links = MARINE_SCOPE_LINKS if key == 'marine' else {}
    rows = []
    for anchor, title, body in service['groups']:
        links = ''.join(f'<a href="./{route}/">{escape(label)}</a>'
                        for route, label in scope_links.get(anchor, ()))
        related = f'<div class="scope-page-links" lang="id">{links}</div>' if links else ''
        rows.append(f'<article class="scope-detail" id="{key}-{anchor}"><h4>{escape(title)}</h4>'
                    f'<p>{escape(body)}</p>{related}</article>')
    return f'''<article class="service-feature" id="{key}-services" aria-labelledby="{key}-heading">
    <div class="service-feature-intro"><figure class="service-photo"><img src="./assets/images/{service['card_image']}"{f' srcset="{srcset(service["card_variants"])}" sizes="(max-width: 680px) calc(100vw - 40px), (max-width: 1200px) calc(32vw - 35px), 360px"' if service.get('card_variants') else ''} alt="{escape(service['card_alt'], quote=True)}" width="{service['card_width']}" height="{service['card_height']}" loading="eager" fetchpriority="low" decoding="async"></figure>
    <div class="service-feature-copy"><h3 id="{key}-heading">{escape(service['name'])} services</h3><p>{escape(service['intro'])}</p></div></div>
    <details class="service-detail" id="{key}-details"><summary><span>View {escape(service['short'])} service details</span>{DISCLOSURE_ICON}</summary>
    <div class="service-detail-body" id="{key}-equipment"><div class="scope-details">{''.join(rows)}</div></div></details></article>'''


def legacy_targets(key, service):
    return {'': f'{key}-services', 'project-scopes': f'{key}-services',
            'equipment': f'{key}-equipment', 'contact': 'contact',
            **{anchor: f'{key}-{anchor}' for anchor, _, _ in service['groups']}}
