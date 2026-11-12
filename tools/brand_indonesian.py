"""Buyer guides in Bahasa Indonesia using the existing brand catalogue images."""
from html import escape

from brand_pages import hero_product_figure, portfolio_image
from brand_profiles import BRANDS

GUIDES = {
    'noris': {
        'description': 'PT Araya Internusa adalah distributor resmi tunggal NORIS di Indonesia. Tanyakan sensor, instrumen, noriMos, noriStar, dan noriNet.',
        'hero_alt': 'Panel anjungan noriStar NORIS dengan dua layar dan dua tuas kontrol propulsi',
        'groups': (
            ('Sensor dan instrumen', (
                ('speed-sensors', 'Sensor putaran NORIS FAH13 dan FAJ13', 'Mengukur putaran mesin atau poros. Untuk mencari pengganti, kirim kode lengkap, foto sensor, jenis pemasangan, dan sinyal keluarannya jika diketahui.'),
                ('temperature-sensors', 'Sensor suhu NORIS TA.81 dan TA.82', 'Untuk pengukuran suhu pada mesin dan sistem kapal. Pemilihan sensor bergantung pada media, rentang suhu, panjang probe, dan sambungan.'),
                ('pressure-sensors', 'Sensor tekanan NORIS PAX9 dan VD61', 'Mengirimkan hasil pengukuran tekanan ke indikator atau sistem kontrol. Periksa rentang, jenis tekanan, sambungan proses, dan sinyal keluaran.'),
                ('instruments', 'Indikator noriMeter NIQ3', 'Indikator analog untuk panel mesin atau anjungan. Untuk penggantian, sertakan foto skala, ukuran panel, dan sinyal masukan.'),
                ('signal-processing', 'Modul pengolah sinyal', 'Modul seperti VF5 dan VP5/VPT5 mengolah sinyal frekuensi atau suhu untuk instrumen dan sistem otomasi.'),
            )),
            ('Sistem otomasi kapal', (
                ('alarm-monitoring', 'Sistem alarm dan monitoring noriMos', 'Memantau peralatan kapal dan menampilkan alarm serta status pada stasiun operator. Untuk retrofit, sertakan daftar sinyal dan gambar panel jika tersedia.'),
                ('propulsion-control', 'Kontrol propulsi noriStar', 'Mengendalikan propulsi dari anjungan dan stasiun kontrol lain. Konfigurasi disesuaikan dengan mesin, jenis propulsi, dan antarmuka kapal.'),
                ('norinet', 'Monitoring kapal dari darat dengan noriNet', 'Menampilkan data kapal yang terhubung untuk pemantauan armada dan analisis kinerja. Ketersediaan data bergantung pada sistem di kapal dan koneksi ke darat.'),
            )),
        ),
    },
    'comap': {
        'description': 'PT Araya Internusa adalah distributor resmi ComAp di Indonesia untuk kontrol mesin, sinkronisasi genset, load sharing, dan manajemen daya kapal.',
        'hero_alt': 'Modul kontrol genset paralel ComAp InteliGen 500 G2',
        'applications': (
            ('Sinkronisasi genset kapal dan industri', 'Saat beberapa genset diparalelkan, controller mengatur sinkronisasi, pemutus sirkuit, dan pembagian beban. Pemilihan modul mempertimbangkan jumlah genset, daya, governor, AVR, dan diagram satu garis.'),
            ('Manajemen daya dan kontrol mesin kapal', 'Sistem manajemen daya mengatur koordinasi sumber listrik di kapal. Kontrol mesin menangani perintah operasi, alarm, dan proteksi untuk mesin propulsi atau mesin bantu.'),
            ('Genset cadangan dan pemantauan', 'Untuk genset tunggal, controller AMF dapat menangani urutan start/stop saat pasokan utama padam. SCADA dan pemantauan jarak jauh dapat ditambahkan sesuai perangkat dan konektivitas.'),
        ),
        'groups': (
            ('Modul kontrol dan perangkat lunak', (
                ('generator-synchronisation', 'InteliGen 500 G2', 'Controller untuk sinkronisasi dan load sharing pada genset paralel. Dapat digunakan pada sistem terhubung jaringan atau sistem yang beroperasi mandiri.'),
                ('marine-power-management', 'InteliGen 1000 Marine', 'Controller untuk koordinasi sumber daya di kapal. Dukungan konfigurasi AC atau DC bergantung pada opsi perangkat lunak dan rancangan sistem.'),
                ('engine-control', 'InteliDrive 700 Marine', 'Controller untuk pemantauan, alarm, dan proteksi mesin kapal, termasuk mesin propulsi, mesin bantu, dan mesin darurat.'),
                ('single-generator', 'InteliLite 4 AMF 25', 'Controller genset tunggal untuk operasi cadangan atau utama, dengan pemantauan pasokan utama dan start/stop otomatis.'),
                ('local-monitoring', 'InteliSCADA', 'Perangkat lunak untuk menampilkan status, pengukuran, dan riwayat operasi genset pada komputer di lokasi.'),
                ('remote-monitoring', 'WebSupervisor', 'Pemantauan jarak jauh untuk status, alarm, dan data perangkat yang terhubung. Fitur bergantung pada kompatibilitas, koneksi, dan langganan.'),
            )),
        ),
    },
}


def indonesian_title(key):
    if key == 'noris':
        return 'Distributor Resmi Tunggal NORIS di Indonesia'
    return f'Distributor Resmi {BRANDS[key]["name"]} di Indonesia'


def system_figure(diagram, alt, prefix):
    return f'''<figure class="application-diagram"><img src="{prefix}assets/images/{diagram['file']}"
      width="{diagram['width']}" height="{diagram['height']}" alt="{escape(alt, quote=True)}" loading="lazy" decoding="async"></figure>'''


def indonesian_content(key, prefix):
    brand = BRANDS[key]
    guide = GUIDES[key]
    title = indonesian_title(key)
    products = {product['id']: product for product in brand['products']}
    applications = ''.join(
        f'<article class="scope-detail"><h3>{escape(heading)}</h3><p>{escape(body)}</p></article>'
        for heading, body in guide.get('applications', ())
    )
    application_section = ''
    if applications:
        diagram = system_figure(brand['application_groups'][0]['diagram'],
                                'Susunan genset, busbar, dan suplai listrik dari darat', prefix)
        application_section = (
            f'<section class="section" id="applications"><div class="container"><h2>Aplikasi ComAp</h2>'
            f'<div class="application-group-intro"><div class="scope-details">{applications}</div>{diagram}</div></div></section>'
        )
    groups = []
    for heading, items in guide['groups']:
        rows = []
        for anchor, label, body in items:
            product = products[anchor]
            image = {**product['image'], 'alt': label}
            figure = portfolio_image({**product, 'image': image}, prefix=prefix, loading='lazy')
            if anchor == 'norinet':
                figure += system_figure(product['diagram'],
                                        'Aliran data dari sistem di kapal melalui unit antarmuka ke layanan pemantauan di darat',
                                        prefix)
            rows.append(f'<article class="portfolio-row" id="{anchor}"><div>{figure}</div>'
                        f'<div><h4>{escape(label)}</h4><p>{escape(body)}</p></div></article>')
        groups.append(f'<section class="portfolio-group"><h3 class="portfolio-group-title">{escape(heading)}</h3>'
                      f'{"".join(rows)}</section>')
    enquiry = ('Sertakan model controller, foto pelat nama (nameplate), jumlah dan daya genset, serta diagram satu garis jika tersedia.'
               if key == 'comap' else
               'Sertakan nomor komponen, foto pelat nama (nameplate), jumlah yang dibutuhkan, serta lokasi kapal atau proyek.')
    return f'''<section class="brand-hero brand-landing"><div class="container">
      <div class="brand-landing-grid"><div><p class="eyebrow">{escape(brand['legal_name'])}</p><h1>{title}</h1>
      <p class="brand-intro">{escape(guide['description'])} Kami melayani pengadaan dan dukungan teknis dari kantor Surabaya dan Jakarta untuk proyek di seluruh Indonesia.</p></div>
      {hero_product_figure(brand, prefix, alt=guide['hero_alt'])}</div>
    </div></section>
{application_section}
    <section class="section section-muted" id="portfolio"><div class="container"><h2>Produk {escape(brand['name'])}</h2><div class="portfolio-list">{"".join(groups)}</div></div></section>
    <section class="section section-compact brand-enquiry" id="araya-support"><div class="container">
      <div class="section-heading"><div><h2>Permintaan penawaran</h2></div><p>{escape(enquiry)} Jelaskan kebutuhan pengadaan, penggantian, atau retrofit agar tim kami dapat memeriksa kecocokan perangkat.</p></div>
    </div></section>'''
