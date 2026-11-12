"""Bahasa Indonesia service pages for ship operators and industrial clients."""

from dataclasses import dataclass
from html import escape

from fire_alarm import HEADING as FIRE_ALARM_HEADING, ROUTE as FIRE_ALARM_ROUTE


SHIP_REPAIR = 'perbaikan-kapal-surabaya-gresik'
ELECTRICAL = 'perbaikan-kelistrikan-kapal'
ENGINES = 'perbaikan-mesin-kapal'
RETROFIT = 'retrofit-kontrol-monitoring-kapal'
MANOEUVRING = 'perbaikan-kemudi-manuver-kapal'
CRANES = 'perbaikan-crane-kapal-industri'

ENGINE_ROOM = ('work-engine-room-800.webp', 800, 373, 'Tim Araya bekerja di ruang mesin kapal')
ENGINE_INSPECTION = ('marine-date-free.webp', 767, 883, 'Teknisi Araya memeriksa peralatan mesin kapal')
ELECTRICAL_PANEL = ('work-ship-electrical-960.webp', 960, 720, 'Teknisi Araya mengerjakan pengawatan panel listrik di kapal')
MONITORING_CONSOLE = ('work-ship-monitoring-960.webp', 960, 720, 'Tim Araya bekerja pada konsol pemantauan kapal')
MANOEUVRING_CONTROLS = ('work-ship-manoeuvring-960.webp', 960, 720, 'Tim Araya memeriksa rangkaian kontrol manuver kapal')


@dataclass(frozen=True)
class ServicePage:
    heading: str
    title: str
    description: str
    intro: str
    scopes: tuple[tuple[str, str], ...]
    contact_topic: str
    contact_hint: str
    image: tuple[str, int, int, str] | None = None
    related: tuple[str, ...] = (SHIP_REPAIR,)


PAGES = {
    SHIP_REPAIR: ServicePage(
        heading='Jasa Perbaikan Kapal di Surabaya & Gresik',
        title='Jasa Perbaikan Kapal Surabaya & Gresik',
        description='Jasa perawatan, perbaikan dan retrofit kapal di Surabaya dan Gresik. Kelistrikan, genset, sistem kontrol, kemudi, crane, dan fire alarm kapal.',
        intro='PT Araya Internusa menangani perawatan, perbaikan, dan retrofit sistem kapal di Surabaya dan Gresik. Kami juga melayani pekerjaan kapal di wilayah lain di Indonesia.',
        scopes=(
            ('Perawatan sistem kapal', 'Pemeriksaan sistem kelistrikan, mesin bantu, kontrol, dan pemantauan di kapal.'),
            ('Perbaikan gangguan', 'Penelusuran gangguan dan perbaikan peralatan kapal, termasuk panel, genset, dan kontrol kemudi.'),
            ('Retrofit peralatan', 'Penggantian peralatan usang serta integrasi panel, kontrol, atau instrumen baru.'),
            ('Pengujian fungsi', 'Pemeriksaan fungsi sistem yang diperbaiki atau diperbarui sesuai kebutuhan pekerjaan.'),
        ),
        contact_topic='perbaikan kapal',
        contact_hint='Kirim nama dan lokasi kapal, peralatan yang perlu ditangani, serta gangguan atau pekerjaan yang dibutuhkan.',
        image=ENGINE_ROOM,
        related=(ELECTRICAL, ENGINES, RETROFIT, MANOEUVRING, CRANES, FIRE_ALARM_ROUTE.rstrip('/')),
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
        image=ELECTRICAL_PANEL,
        related=(SHIP_REPAIR, ENGINES, RETROFIT),
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
        image=ENGINE_INSPECTION,
        related=(SHIP_REPAIR, ELECTRICAL, RETROFIT),
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
        image=MONITORING_CONSOLE,
        related=(SHIP_REPAIR, ELECTRICAL, MANOEUVRING),
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
        image=MANOEUVRING_CONTROLS,
        related=(SHIP_REPAIR, RETROFIT),
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
    ),
}


def related_label(slug):
    if slug == FIRE_ALARM_ROUTE.rstrip('/'):
        return FIRE_ALARM_HEADING
    return PAGES[slug].heading


def service_content(page, arrow):
    photo = ''
    hero_layout = 'service-guide-hero-copy'
    if page.image:
        filename, width, height, alt = page.image
        hero_layout = 'brand-landing-grid'
        photo = f'''
        <div class="hero-product hero-product-cover">
          <img src="../assets/images/{filename}" alt="{escape(alt, quote=True)}" width="{width}" height="{height}" fetchpriority="high">
        </div>'''
    scopes = ''.join(f'<div><h3>{escape(title)}</h3><p>{escape(body)}</p></div>'
                     for title, body in page.scopes)
    related = ''.join(f'<li><a class="text-link" href="../{slug}/">{escape(related_label(slug))} {arrow}</a></li>'
                      for slug in page.related)
    return f'''
<section class="brand-hero brand-landing service-guide-hero">
  <div class="container {hero_layout}">
    <div><h1>{escape(page.heading)}</h1><p class="brand-intro">{escape(page.intro)}</p></div>{photo}
  </div>
</section>
<section class="section" aria-labelledby="service-scope">
  <div class="container">
    <div class="section-heading"><h2 id="service-scope">Lingkup pekerjaan</h2></div>
    <div class="service-guide-scopes">{scopes}</div>
  </div>
</section>
<section class="section section-muted section-compact" aria-labelledby="related-services">
  <div class="container">
    <h2 id="related-services">Layanan terkait</h2>
    <ul class="service-guide-related">{related}</ul>
  </div>
</section>'''
