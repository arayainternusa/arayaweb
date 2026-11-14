"""Bahasa Indonesia service pages for ship operators and industrial clients."""

from dataclasses import dataclass
from html import escape

from fire_alarm import ROUTE as FIRE_ALARM_ROUTE


SHIP_REPAIR = 'perbaikan-kapal'
LEGACY_SHIP_REPAIR = 'perbaikan-kapal-surabaya-gresik'
ELECTRICAL = 'perbaikan-kelistrikan-kapal'
ENGINES = 'perbaikan-mesin-kapal'
RETROFIT = 'retrofit-kontrol-monitoring-kapal'
MANOEUVRING = 'perbaikan-kemudi-manuver-kapal'
CRANES = 'perbaikan-crane-kapal-industri'

FIRE_ALARM = FIRE_ALARM_ROUTE.rstrip('/')
SERVICE_LINKS = (
    (SHIP_REPAIR, 'Perbaikan Kapal'),
    (ELECTRICAL, 'Kelistrikan Kapal'),
    (ENGINES, 'Mesin Kapal (ME & AE)'),
    (RETROFIT, 'Otomasi & Monitoring Kapal'),
    (MANOEUVRING, 'Kemudi & Manuver Kapal'),
    (CRANES, 'Crane Kapal & Industri'),
    (FIRE_ALARM, 'Fire Alarm Kapal & Industri'),
)

ENGINE_ROOM = ('work-engine-room-1280.webp', 'Tim Araya bekerja di ruang mesin kapal')
ENGINE_INSPECTION = ('marine-date-free.webp', 'Teknisi Araya memeriksa peralatan mesin kapal')
ELECTRICAL_PANEL = ('work-ship-electrical-960.webp', 'Teknisi mengerjakan pengawatan panel KM Awu')
SWITCHBOARD = ('work-switchboard-date-free-800.webp', 'Tim Araya memeriksa switchboard kapal')
UMSINI_PANEL = ('work-umsini-panel.webp', 'Teknisi memeriksa panel listrik KM Umsini')
MONITORING_CONSOLE = ('work-ship-monitoring-960.webp', 'Tim bekerja pada konsol monitoring KM Binaiya')
CIREMAI_DIAGNOSTICS = ('work-control-room-diagnostics-900.webp', 'Teknisi melakukan diagnostik di ruang kontrol KM Ciremai')
LEUSER_CONTROL = ('work-ship-manoeuvring-960.webp', 'Teknisi memeriksa rangkaian kontrol manuver KM Leuser')
AWU_CONTROL = ('work-awu-manoeuvring.webp', 'Teknisi memperbaiki sistem kontrol manuver KM Awu')


@dataclass(frozen=True)
class ServicePage:
    heading: str
    title: str
    description: str
    intro: str
    scopes: tuple[tuple[str, str], ...]
    contact_topic: str
    contact_hint: str
    photos: tuple[tuple[str, str], ...]


PAGES = {
    SHIP_REPAIR: ServicePage(
        heading='Jasa Perbaikan Kapal di Indonesia',
        title='Jasa Perbaikan Kapal di Indonesia',
        description='Jasa perawatan, perbaikan, dan retrofit kapal di berbagai kota di Indonesia seperti Surabaya, Gresik, Semarang, Jakarta, Samarinda, Balikpapan, dan Makassar.',
        intro='PT Araya Internusa melayani perbaikan kapal di berbagai kota di Indonesia seperti Surabaya, Gresik, Semarang, Jakarta, Samarinda, Balikpapan, dan Makassar. Layanan kami mencakup perawatan, perbaikan, dan retrofit mesin, kelistrikan, serta sistem kontrol kapal.',
        scopes=(
            ('Perawatan sistem kapal', 'Pemeriksaan sistem kelistrikan, mesin bantu, kontrol, dan pemantauan di kapal.'),
            ('Perbaikan gangguan', 'Penelusuran gangguan dan perbaikan peralatan kapal, termasuk panel, genset, dan kontrol kemudi.'),
            ('Retrofit peralatan', 'Penggantian peralatan usang serta integrasi panel, kontrol, atau instrumen baru.'),
            ('Pengujian fungsi', 'Pemeriksaan fungsi sistem yang diperbaiki atau diperbarui sesuai kebutuhan pekerjaan.'),
        ),
        contact_topic='perbaikan kapal',
        contact_hint='Kirim nama dan lokasi kapal, peralatan yang perlu ditangani, serta gangguan atau pekerjaan yang dibutuhkan.',
        photos=(
            ENGINE_ROOM,
            ('work-ship-water-treatment.webp', 'Tim mengerjakan sistem pengolahan air di kapal'),
            ELECTRICAL_PANEL, SWITCHBOARD, ENGINE_INSPECTION, MONITORING_CONSOLE,
            CIREMAI_DIAGNOSTICS, LEUSER_CONTROL, AWU_CONTROL, UMSINI_PANEL,
        ),
    ),
    ELECTRICAL: ServicePage(
        heading='Instalasi dan Perbaikan Kelistrikan Kapal',
        title='Jasa Instalasi dan Perbaikan Kelistrikan Kapal',
        description='Instalasi dan perbaikan kelistrikan kapal, termasuk panel listrik, switchboard, kabel, dan distribusi daya di Surabaya, Gresik, dan seluruh Indonesia.',
        intro='PT Araya Internusa memasang instalasi listrik baru dan memperbaiki gangguan kelistrikan di kapal. Pekerjaan mencakup panel listrik, switchboard, kabel, dan distribusi daya.',
        scopes=(
            ('Panel Listrik & Switchboard Kapal', 'Pemasangan dan pemeriksaan panel, pemutus sirkuit, kontaktor, relai, dan rangkaian kontrol.'),
            ('Distribusi daya', 'Penelusuran gangguan pada jalur distribusi dan suplai ke peralatan kapal.'),
            ('Instalasi kabel & sambungan', 'Pemasangan jalur kabel, terminasi, dan perbaikan sambungan listrik yang bermasalah.'),
            ('Perbaikan & retrofit panel', 'Penggantian komponen panel dan penyesuaian rangkaian pada instalasi yang ada.'),
        ),
        contact_topic='kelistrikan kapal',
        contact_hint='Kirim lokasi kapal, jenis panel, serta kebutuhan instalasi atau gejala gangguan. Sertakan foto panel atau diagram satu garis jika tersedia.',
        photos=(ELECTRICAL_PANEL, SWITCHBOARD, UMSINI_PANEL),
    ),
    ENGINES: ServicePage(
        heading='Jasa Perbaikan Mesin Kapal (ME & AE)',
        title='Jasa Perbaikan Mesin Kapal (ME & AE)',
        description='Jasa perbaikan mesin diesel kapal, termasuk motor induk (ME), motor bantu (AE), safety device, kontrol mesin, sinkronisasi, dan load sharing.',
        intro='PT Araya Internusa menangani perbaikan mesin diesel kapal, meliputi motor induk (ME) dan motor bantu (AE). Kami juga menangani kontrol mesin serta gangguan sinkronisasi dan pembagian beban pada sistem daya kapal.',
        scopes=(
            ('Motor Induk (ME)', 'Penelusuran gangguan dan perbaikan sistem motor induk kapal.'),
            ('Motor Bantu (AE)', 'Perawatan, perbaikan, dan overhaul motor bantu sesuai lingkup pekerjaan.'),
            ('Safety Device & Kontrol Mesin', 'Penelusuran gangguan kontrol start/stop, sensor, alarm, dan sistem shutdown.'),
            ('Sinkronisasi & load sharing', 'Penelusuran gangguan sinkronisasi dan pembagian beban pada sistem daya kapal.'),
        ),
        contact_topic='perbaikan mesin kapal (ME & AE)',
        contact_hint='Kirim lokasi kapal, jenis dan model mesin, serta gejala gangguan. Sertakan foto pelat nama atau kode alarm jika tersedia.',
        photos=(
            ENGINE_INSPECTION, ENGINE_ROOM,
            ('work-awu-generator-panel.webp', 'Teknisi memeriksa panel generator darurat KM Awu'),
        ),
    ),
    RETROFIT: ServicePage(
        heading='Otomasi & Monitoring Kapal',
        title='Jasa Otomasi & Monitoring Kapal',
        description='Perbaikan dan retrofit otomasi dan monitoring kapal, termasuk General Alarm Kapal, Alarm Monitoring System (AMS), PLC, HMI, SCADA, dan sensor.',
        intro='Araya memperbaiki dan melakukan retrofit sistem otomasi dan monitoring kapal, termasuk general alarm dan Alarm Monitoring System (AMS). Kami mengintegrasikan panel dan perangkat kontrol baru dengan peralatan yang masih digunakan.',
        scopes=(
            ('General Alarm Kapal', 'Perbaikan dan retrofit general alarm, termasuk panel, tombol aktivasi, dan perangkat notifikasi.'),
            ('Alarm Monitoring System (AMS)', 'Perbaikan dan retrofit sistem alarm dan monitoring mesin serta peralatan kapal.'),
            ('PLC, HMI & SCADA', 'Penggantian kontrol usang, penyesuaian program, dan pembaruan tampilan operator.'),
            ('Instrumentasi & sensor', 'Integrasi sensor dan modul I/O untuk pemantauan mesin, tangki, dan peralatan kapal.'),
        ),
        contact_topic='otomasi dan monitoring kapal',
        contact_hint='Kirim lokasi kapal, jenis sistem, dan gejala gangguan atau fungsi yang ingin diperbarui. Sertakan model panel, diagram, atau daftar I/O jika tersedia.',
        photos=(
            MONITORING_CONSOLE,
            ('work-binaiya-monitoring-cabinet.webp', 'Teknisi bekerja pada kabinet monitoring KM Binaiya'),
            CIREMAI_DIAGNOSTICS,
        ),
    ),
    MANOEUVRING: ServicePage(
        heading='Perbaikan Sistem Kemudi & Manuver Kapal',
        title='Jasa Perbaikan Sistem Kemudi & Manuver Kapal',
        description='Perbaikan dan retrofit sistem kemudi dan manuver kapal, termasuk kontrol CPP, bow thruster, panel, dan sinyal umpan balik.',
        intro='Araya menangani perbaikan dan retrofit sistem kemudi dan manuver kapal, termasuk gangguan pada panel, perintah operasi, dan sinyal umpan balik.',
        scopes=(
            ('Kontrol kemudi', 'Penelusuran gangguan perintah kemudi, indikator, alarm, dan umpan balik posisi.'),
            ('Kontrol manuver kapal', 'Pemeriksaan antarmuka kontrol antara anjungan, ruang mesin, dan stasiun lokal.'),
            ('Kontrol CPP', 'Perbaikan rangkaian kontrol dan umpan balik pada sistem controllable-pitch propeller.'),
            ('Kontrol bow thruster', 'Penelusuran gangguan panel, sinyal, dan kontrol pengoperasian bow thruster.'),
        ),
        contact_topic='sistem kemudi dan manuver kapal',
        contact_hint='Kirim lokasi kapal, jenis sistem kemudi atau manuver, dan gejala gangguan. Sertakan model kontrol dan alarm yang muncul jika tersedia.',
        photos=(
            ('work-binaiya-bridge.webp', 'Teknisi bekerja pada konsol anjungan KM Binaiya'),
            LEUSER_CONTROL, AWU_CONTROL,
            ('work-awu-manoeuvring-manifold.webp', 'Teknisi memeriksa rangkaian kontrol manuver KM Awu'),
        ),
    ),
    CRANES: ServicePage(
        heading='Jasa Perbaikan Crane Kapal & Industri',
        title='Jasa Perbaikan Crane Kapal & Industri',
        description='Perbaikan deck crane kapal dan crane industri, termasuk overhead dan portal crane, panel kontrol, serta sistem kelistrikan dan otomasi.',
        intro='PT Araya Internusa menangani perbaikan deck crane kapal dan crane industri, termasuk gangguan pada panel, rangkaian kelistrikan, dan sistem kontrol.',
        scopes=(
            ('Deck crane kapal', 'Perbaikan deck crane dan sistem kontrol yang digunakan untuk pengoperasiannya.'),
            ('Crane industri', 'Perbaikan overhead crane, portal crane, dan crane di fasilitas industri.'),
            ('Kelistrikan & panel kontrol', 'Penelusuran gangguan panel, suplai listrik, dan rangkaian kontrol crane.'),
            ('Kontrol & otomasi', 'Perbaikan atau retrofit perangkat kontrol sesuai tipe dan instalasi crane.'),
        ),
        contact_topic='perbaikan crane kapal atau industri',
        contact_hint='Kirim lokasi crane, tipe, kapasitas, dan gejala gangguan. Sertakan foto pelat nama, panel, atau pesan alarm jika tersedia.',
        photos=(('work-crane-pendant.webp', 'Teknisi mengerjakan pengawatan pendant crane'),),
    ),
}


def all_services(current, arrow):
    links = []
    for slug, label in SERVICE_LINKS:
        selected = ' aria-current="page"' if slug == current else ''
        icon = '' if selected else arrow
        links.append(f'<li><a class="text-link" href="../{slug}/"{selected}><span>{escape(label)}</span>{icon}</a></li>')
    return f'''
<section class="section section-compact section-muted" aria-labelledby="all-services">
  <div class="container">
    <h2 id="all-services">Semua layanan</h2>
    <ul class="service-guide-related">{''.join(links)}</ul>
  </div>
</section>'''


def hero_photos(photos):
    images = []
    for index, (filename, alt) in enumerate(photos):
        priority = 'loading="lazy" fetchpriority="low" decoding="async"' if index else 'fetchpriority="high"'
        position = ' class="service-photo-focus"' if filename == ENGINE_INSPECTION[0] else ''
        images.append(f'<img{position} src="../assets/images/{filename}" alt="{escape(alt, quote=True)}" {priority}>')
    if len(images) == 1:
        return f'<div class="hero-product hero-product-cover">{images[0]}</div>'

    return f'''
    <div class="hero-product hero-product-cover service-photo-slider" role="group" aria-label="Foto pekerjaan" data-service-photo-slider>
      <div class="service-photo-track" tabindex="0" aria-label="Geser untuk melihat foto pekerjaan">{''.join(images)}</div>
      <div class="service-photo-controls" hidden>
        <button type="button" data-photo-step="-1" aria-label="Foto sebelumnya"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 6-6 6 6 6"/></svg></button>
        <span aria-live="polite" aria-atomic="true">1 / {len(images)}</span>
        <button type="button" data-photo-step="1" aria-label="Foto berikutnya"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg></button>
      </div>
    </div>'''


def service_content(page):
    scopes = ''.join(f'<div><h3>{escape(title)}</h3><p>{escape(body)}</p></div>'
                     for title, body in page.scopes)
    return f'''
<section class="brand-hero brand-landing service-guide-hero">
  <div class="container brand-landing-grid">
    <div><h1>{escape(page.heading)}</h1><p class="brand-intro">{escape(page.intro)}</p></div>{hero_photos(page.photos)}
  </div>
</section>
<section class="section" aria-labelledby="service-scope">
  <div class="container">
    <div class="section-heading"><h2 id="service-scope">Lingkup pekerjaan</h2></div>
    <div class="service-guide-scopes">{scopes}</div>
  </div>
</section>'''
