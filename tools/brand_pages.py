"""Shared layout for Araya's dedicated manufacturer guides."""
from html import escape
from ui_components import disclosure_summary


def hero_product_figure(data, prefix='../', *, alt=None):
    cover = ' hero-product-cover' if data.get('image_cover') else ''
    alt = escape(data['alt'] if alt is None else alt, quote=True)
    return f'<figure class="product-figure hero-product{cover}"><img src="{prefix}assets/images/{data["image"]}" alt="{alt}" width="{data["image_width"]}" height="{data["image_height"]}" fetchpriority="high"></figure>'



def portfolio_image(product, *, prefix='../', loading='eager'):
    """Optional local manufacturer image; never imply an Araya installation."""
    if 'image' not in product:
        return ''
    picture = product['image']
    return f'''<figure class="portfolio-picture"><img src="{prefix}assets/images/{escape(picture['file'], quote=True)}" alt="{escape(picture['alt'], quote=True)}" width="{picture['width']}" height="{picture['height']}" loading="{loading}" fetchpriority="low" decoding="async"></figure>'''


def diagram_figure(diagram, *, defer=True):
    loading = 'lazy' if defer else 'eager'
    return f'''<figure class="application-diagram"><a class="diagram-trigger" href="../assets/images/{diagram['file']}" target="_blank" rel="noopener" aria-label="Enlarge diagram: {escape(diagram['caption'], quote=True)}" data-diagram-caption="{escape(diagram['caption'], quote=True)}"><img src="../assets/images/{diagram['file']}" alt="{escape(diagram['alt'], quote=True)}" width="{diagram['width']}" height="{diagram['height']}" loading="{loading}" fetchpriority="low" decoding="async"><span class="diagram-enlarge" aria-hidden="true">Enlarge diagram ↗</span></a></figure>'''


def portfolio_system(product, heading="h4"):
    if 'diagram' not in product:
        return ''
    flow = ''.join(f'<li>{escape(step)}</li>' for step in product.get('flow', []))
    return f'''<div class="portfolio-system"><{heading}>How the system connects</{heading}><ol class="application-flow" aria-label="Conceptual system flow">{flow}</ol>{diagram_figure(product['diagram'], defer=False)}<p class="system-note">{escape(product['diagram_note'])}</p></div>'''


def diagram_viewer():
    return '''<dialog class="diagram-viewer" aria-labelledby="diagram-viewer-title"><div class="diagram-toolbar"><h2 id="diagram-viewer-title">Application diagram</h2><button type="button" class="diagram-close" autofocus aria-label="Close diagram">Close ×</button><div class="diagram-zoom" role="group" aria-label="Diagram zoom"><button type="button" data-zoom="out" aria-label="Zoom out">−</button><button type="button" data-zoom="reset">Fit</button><button type="button" data-zoom="in" aria-label="Zoom in">+</button><span class="diagram-zoom-status" aria-live="polite">100%</span></div></div><div class="diagram-stage" tabindex="0" aria-label="Diagram image. Scroll to explore when enlarged."><img alt="Enlarged manufacturer system diagram"></div><div class="diagram-viewer-footer"><span>Zoom in, then scroll to explore. Escape closes this view.</span></div></dialog>'''


def application_guide(groups, arrow):
    rendered = []
    for i, group in enumerate(groups, 1):
        diagram = group['diagram']
        flow = ''.join(f'<li>{escape(step)}</li>' for step in group['flow'])
        items = []
        for item_index, item in enumerate(group['items']):
            fields = ''.join(f'<div><dt>{label}</dt><dd>{escape(item[key])}</dd></div>' for label, key in [('Typical system', 'system'), ('What ComAp controls', 'control'), ('Example product families', 'families'), ('What to review with Araya', 'review')])
            diagrams = ''.join(diagram_figure(picture) for picture in item.get('diagrams', []))
            gallery = f'<div class="application-diagrams">{diagrams}</div>' if diagrams else ''
            items.append(f'''<details class="application-detail" id="{item['id']}">{disclosure_summary(item['title'], item['summary'], 'h4')}<div class="application-body"><dl>{fields}</dl>{gallery}</div></details>''')
        rendered.append(f'''<section class="application-group" id="{group['id']}" aria-labelledby="{group['id']}-heading"><div class="application-group-intro"><div><p class="eyebrow">APPLICATION GROUP 0{i}</p><h3 id="{group['id']}-heading">{escape(group['title'])}</h3><p>{escape(group['intro'])}</p><ol class="application-flow" aria-label="Conceptual system flow">{flow}</ol></div>{diagram_figure(diagram, defer=False)}</div><div class="application-details">{''.join(items)}</div></section>''')
    return f'''<section class="section application-guide" id="applications"><div class="container"><p class="eyebrow">COMAP APPLICATIONS</p><h2>Applications</h2><p class="lead application-guide-intro">Engine and power control for marine, power generation and smart energy systems. Open an application for its control functions and system diagrams; the final configuration depends on your project.</p>{''.join(rendered)}</div></section>{diagram_viewer()}'''


def brand_contents(data):
    """A single, simple index; information is not repeated in action rows."""
    if data.get('application_groups'):
        return '<section class="brand-toc" id="contents"><div class="container"><h2>Contents</h2><ol class="brand-outline"><li><a href="#applications">Applications</a><p>Marine, power generation and smart energy management.</p></li><li><a href="#portfolio">Products</a><p>Engine controllers, generator controllers and monitoring modules.</p></li></ol></div></section>'
    products = {p['id']: p for p in data['products']}
    groups = data.get('contents_product_groups', [('Products & systems', list(products))])
    rendered = []
    for title, anchors in groups:
        items = ''.join(f'<li><a href="#{anchor}">{escape(products[anchor]["short"])}</a></li>' for anchor in anchors)
        rendered.append(f'<div class="brand-toc-group brand-product-group"><h3>{escape(title)}</h3><ul>{items}</ul></div>')
    return f'<section class="brand-toc" id="contents"><div class="container"><div class="brand-toc-heading"><div><p class="eyebrow">EXPLORE {escape(data["name"].upper())}</p><h2>{escape(data["name"])} products</h2></div></div><nav aria-label="{escape(data["name"])} product groups"><div class="brand-toc-groups">{"".join(rendered)}</div></nav></div></section>'


def brand_content(key, data, arrow):
    name = escape(data['name'])
    has_guide = bool(data.get('application_groups'))
    product_heading = 'h4' if data.get('contents_product_groups') else 'h3'
    facts = ''.join(f'<div><dt>{escape(label)}</dt><dd>{escape(value)}</dd></div>' for label, value in data['facts'])
    portfolio_rows = {product['id']: f'''<article class="portfolio-row" id="{product['id']}">
      <div><span class="portfolio-number">{i:02}</span><{product_heading}>{escape(product['title'])}</{product_heading}><p class="family-name">{escape(product['family'])}</p>{portfolio_image(product)}</div>
      <div><p>{escape(product['body'])}</p><dl><div><dt>Applications</dt><dd>{escape(product['application'])}</dd></div><div><dt>Selection details</dt><dd>{escape(product['selection'])}</dd></div></dl></div>
{portfolio_system(product, 'h5' if product_heading == 'h4' else 'h4')}
    </article>''' for i, product in enumerate(data['products'], 1)}
    portfolio = ''.join(portfolio_rows.values())
    if data.get('contents_product_groups'):
        portfolio = ''.join(f'<section class="portfolio-group" aria-label="{escape(title, quote=True)}"><h3 class="portfolio-group-title">{escape(title)}</h3>{"".join(portfolio_rows[anchor] for anchor in anchors)}</section>' for title, anchors in data['contents_product_groups'])
    application_section = application_guide(data['application_groups'], arrow) if has_guide else ''
    enquiry = ''.join(f'<li><h3>{escape(title)}</h3><p>{escape(body)}</p></li>' for title, body in data['enquiry'])
    faqs = ''.join(f'<details>{disclosure_summary(question)}<p>{escape(answer)}</p></details>' for question, answer in data['faqs'])
    return f'''<section class="brand-hero brand-landing"><div class="container">
      <div class="brand-landing-grid"><div><p class="eyebrow">{escape(data['label'])}</p><h1>{data['heading']}</h1><p class="brand-intro">{escape(data['intro'])}</p></div>
      {hero_product_figure(data)}</div>
    </div></section>
    <section class="section section-compact" id="about-brand"><div class="container"><div class="brand-profile"><div><p class="eyebrow">THE MANUFACTURER</p><h2>About {name}</h2></div><div><p>{escape(data['profile'])}</p><p>{escape(data['local'])}</p></div></div><dl class="brand-facts">{facts}</dl></div></section>
    {brand_contents(data)}
{application_section}
    <section class="section section-muted" id="portfolio"><div class="container"><p class="eyebrow">{name.upper()} TECHNOLOGY</p><h2>Products{' &amp; systems' if key == 'noris' else ''}</h2><p class="portfolio-intro">Product families and example models. Selection depends on the operating requirements, interfaces and installation.</p><div class="portfolio-list">{portfolio}</div></div></section>
{diagram_viewer() if not has_guide and any('diagram' in product for product in data['products']) else ''}
    <section class="section section-compact" id="brand-faq"><div class="container brand-faq"><div><p class="eyebrow">{name.upper()} GUIDE</p><h2>Common questions</h2></div><div class="faq-list">{faqs}</div></div></section>
    <section class="section section-compact brand-enquiry" id="araya-support"><div class="container"><div class="section-heading"><div><p class="eyebrow">BEFORE YOU CONTACT US</p><h2>Equipment details</h2></div><p>These details help us assess {name} supply, replacement or integration requirements.</p></div><ol class="enquiry-list">{enquiry}</ol></div></section>
'''
