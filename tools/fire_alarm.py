"""Bahasa Indonesia copy for the fire alarm installation and repair service."""

from html import escape

ROUTE = 'instalasi-fire-alarm/'
TITLE = 'Jasa Instalasi & Perbaikan Fire Alarm Surabaya dan Gresik | Araya'
DESCRIPTION = (
    'Jasa instalasi, perbaikan, dan retrofit fire alarm kapal, pabrik, dan gudang '
    'di Surabaya dan Gresik. PT Araya Internusa menangani sistem berbagai merek.'
)
HEADING = 'Instalasi dan Perbaikan Fire Alarm Kapal & Industri'
CONTACT_HINT = (
    'Kirim lokasi kapal atau fasilitas, jenis sistem, serta kebutuhan instalasi atau gejala gangguan. '
    'Sertakan merek dan model panel jika tersedia.'
)


def fire_alarm_content():
    return f'''
<section class="brand-hero brand-landing fire-hero">
  <div class="container brand-landing-grid">
    <div>
      <h1>{escape(HEADING)}</h1>
      <p class="brand-intro">PT Araya Internusa melayani instalasi, perbaikan, dan retrofit fire alarm serta sistem pemadaman tetap untuk kapal, pabrik, dan gudang di Surabaya dan Gresik.</p>
    </div>
    <div class="hero-product hero-product-cover">
      <img src="../assets/images/work-fire-alarm-800.webp" alt="Teknisi Araya mengerjakan kabel sistem fire alarm di kapal" width="800" height="599" fetchpriority="high">
    </div>
  </div>
</section>
<section class="section" aria-labelledby="fire-alarm-scope">
  <div class="container">
    <div class="section-heading">
      <h2 id="fire-alarm-scope">Layanan untuk kapal dan industri</h2>
      <p>Kami menangani Consilium dan sistem berbagai merek, sesuai kebutuhan kapal atau fasilitas Anda.</p>
    </div>
    <div class="fire-service-grid">
      <div id="fire-alarm-kapal">
        <h3>Kapal</h3>
        <p>Instalasi dan perbaikan fire alarm untuk ruang mesin dan area lain di kapal, termasuk integrasi dengan sistem pemadaman tetap.</p>
      </div>
      <div id="fire-alarm-industri">
        <h3>Pabrik dan gudang</h3>
        <p>Pemasangan dan pengujian alarm kebakaran, penelusuran gangguan panel dan kabel, serta penggantian komponen pada sistem yang terpasang.</p>
      </div>
    </div>
    <dl class="fire-service-types">
      <div><dt>Instalasi &amp; pengujian</dt><dd>Pemasangan panel, detektor, tombol alarm manual, dan perangkat notifikasi.</dd></div>
      <div><dt>Perbaikan</dt><dd>Penelusuran gangguan pada panel, detektor, kabel, dan antarmuka sistem.</dd></div>
      <div><dt>Retrofit</dt><dd>Penggantian peralatan usang dan integrasi dengan sistem yang masih digunakan.</dd></div>
    </dl>
  </div>
</section>
<section class="section section-muted" aria-labelledby="fire-system-types">
  <div class="container">
    <div class="section-heading">
      <h2 id="fire-system-types">Deteksi dan pemadaman kebakaran</h2>
      <p>Contoh peralatan dari katalog produsen. Jenis sistem disesuaikan dengan kapal atau fasilitas.</p>
    </div>
    <div class="fire-system-grid">
      <figure class="fire-system">
        <div class="fire-system-media"><img src="../assets/images/fire-detection-consilium.png" alt="Diagram Consilium yang menghubungkan panel, detektor dan tombol alarm" width="518" height="292" loading="lazy" decoding="async"></div>
        <figcaption><h3>Deteksi dan fire alarm</h3><p>Panel utama, panel repeater, detektor, tombol alarm manual, dan perangkat notifikasi.</p></figcaption>
      </figure>
      <figure class="fire-system">
        <div class="fire-system-media fire-system-photo"><img src="../assets/images/fire-co2-bsky.png" alt="Deretan tabung CO₂ pada sistem pemadaman tetap BSKY" width="265" height="180" loading="lazy" decoding="async"></div>
        <figcaption><h3>Sistem CO₂ tetap</h3><p>Rangkaian tabung, katup, dan panel pelepas untuk sistem pemadaman tetap.</p></figcaption>
      </figure>
      <figure class="fire-system">
        <div class="fire-system-media"><img src="../assets/images/fire-water-mist-bsky.png" alt="Unit pompa sistem water mist BSKY" width="265" height="240" loading="lazy" decoding="async"></div>
        <figcaption><h3>Sistem water mist</h3><p>Unit pompa, panel kontrol, dan nosel kabut air untuk pemadaman setempat.</p></figcaption>
      </figure>
      <figure class="fire-system">
        <div class="fire-system-media"><img src="../assets/images/fire-foam-bsky.jpg" alt="Peralatan sistem pemadaman busa tetap BSKY" width="400" height="406" loading="lazy" decoding="async"></div>
        <figcaption><h3>Sistem pemadaman busa</h3><p>Sistem busa ekspansi rendah untuk perlindungan area seperti dek kapal.</p></figcaption>
      </figure>
    </div>
  </div>
</section>'''
