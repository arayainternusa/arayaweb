"""Shared consent UI and factual privacy notice for the static site."""

def banner(prefix, language='en'):
    if language == 'id':
        return f'''<section class="consent-banner" id="consent-banner" aria-labelledby="consent-heading" hidden>
  <h2 id="consent-heading">Pilihan privasi Anda</h2>
  <p>Dengan izin Anda, kami menggunakan Google Analytics untuk memahami kunjungan dan klik pada tautan kontak. Analitik opsional hanya aktif setelah Anda menyetujuinya. Situs dan tautan kontak tetap dapat digunakan.</p>
  <p><a href="{prefix}privacy/">Pemberitahuan privasi (English)</a> · <span id="consent-status" role="status" data-accepted="Analitik saat ini diizinkan." data-disabled="Analitik opsional saat ini nonaktif."></span></p>
  <div class="consent-actions"><button type="button" data-consent-action="reject">Tolak analitik</button><button type="button" data-consent-action="accept">Izinkan analitik</button></div>
</section>'''
    return f'''<section class="consent-banner" id="consent-banner" aria-labelledby="consent-heading" hidden>
  <h2 id="consent-heading">Your privacy choices</h2>
  <p>With your permission, we use Google Analytics to understand website visits and clicks on our contact links. Optional analytics stays off until you accept. You can use the website and contact us either way.</p>
  <p><a href="{prefix}privacy/">Privacy notice</a> · <span id="consent-status" role="status"></span></p>
  <div class="consent-actions"><button type="button" data-consent-action="reject">Reject optional</button><button type="button" data-consent-action="accept">Accept analytics</button></div>
</section>'''

def privacy_content():
    return '''<section class="section"><div class="container privacy-notice"><p class="eyebrow">PT ARAYA INTERNUSA</p><h1>Privacy notice</h1><p>Updated 23 October 2026.</p>
<p>This notice describes information used when you visit arayainternusa.co.id or contact PT Araya Internusa.</p>
<h2>Your choice comes first</h2><p>Optional Google measurement is off until you choose Accept analytics. Reject optional keeps it off without preventing navigation or contact. Use Privacy choices in the footer to change your choice. We remember it in your browser for up to 180 days; clearing browser storage removes it.</p>
<h2>Website analytics</h2><p>If you accept, Google Tag Manager loads Google Analytics to measure page views, scrolling and clicks on our WhatsApp and email links. Reports help us understand website use and the sources of visits, including Google Ads. A contact click does not tell us whether you sent a message or became a customer.</p><p>Analytics can use browser identifiers and cookies and process information about your device, browser, approximate location and referring source. Our contact events send only contact method, page category and button location. We do not send the contents of your messages, nameplate photos, email address or telephone number in these events. Automatic form-interaction tracking is disabled.</p>
<p>This setup does not enable advertising personalisation, Google Signals or user-provided data collection. The Google Ads connection supports measurement; it does not itself start advertisements. Google processes measurement data on its infrastructure, which may be outside Indonesia. Read <a href="https://policies.google.com/technologies/partner-sites">how Google uses information from sites using its services</a> and <a href="https://policies.google.com/privacy">Google’s privacy policy</a>.</p>
<h2>Changing or withdrawing consent</h2><p>Choose Reject optional in Privacy choices to stop optional measurement. We remove accessible Google measurement cookies and reload the page to unload Google scripts. Withdrawal affects future collection; it does not automatically erase reports already processed by Google. Browser controls and content blockers may also limit collection.</p>
<h2>When you contact us</h2><p>WhatsApp and email links open the relevant service or application. Information you choose to send is used to respond to your enquiry and discuss your requirements. Please share only information needed for the work. These services have their own privacy terms. Our website has no enquiry form or customer database.</p>
<h2>Hosting and necessary storage</h2><p>Our hosting provider processes connection information needed to serve and protect the website. The consent preference is necessary to remember your choice and contains no name, email address or telephone number.</p>
<h2>Questions and requests</h2><p>For privacy questions, requests about information you have supplied or to discuss retention, email <a href="mailto:cs@arayainternusa.com">cs@arayainternusa.com</a>. Include enough context for us to identify the enquiry, and avoid sending sensitive documents unless needed.</p>
</div></section>'''
