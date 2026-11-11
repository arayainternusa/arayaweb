// Basic consent mode: Google is not contacted until analytics is accepted.
(() => {
  'use strict';
  if (window.arayaMeasurementInstalled) return;
  window.arayaMeasurementInstalled = true;
  const key = 'araya_consent_v1';
  const measurementId = 'G-WMBDHTFPBJ';
  const production = document.currentScript?.dataset.measurement === 'production'
    && location.hostname === 'arayainternusa.co.id' && location.protocol === 'https:';
  const banner = document.getElementById('consent-banner');
  const status = document.getElementById('consent-status');
  const lifetime = 180 * 86400000;
  let accepted = false, loaded = false, returnFocus = null, storageUsable = true;
  window.dataLayer = window.dataLayer || [];
  function command() { window.dataLayer.push(arguments); }
  const denied = {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'};
  function validChoice(raw) {
    try {
      const value = JSON.parse(raw);
      return value?.version === 1 && typeof value.analytics === 'boolean'
        && Number.isFinite(value.at) && value.at <= Date.now()
        && Date.now() - value.at < lifetime ? value : null;
    } catch (_) { return null; }
  }
  function readChoice() {
    try { return validChoice(window.localStorage.getItem(key)); } catch (_) { storageUsable = false; return null; }
  }
  function clearCookies() {
    const domains = ['', location.hostname, '.' + location.hostname];
    document.cookie.split(';').forEach(item => {
      const name = item.split('=')[0].trim();
      if (!/^(_ga(?:_|$)|_gid$|_gat(?:_|$)|_gcl_)/.test(name)) return;
      domains.forEach(domain => {
        document.cookie = name + '=; Max-Age=0; Path=/; SameSite=Lax; Secure' + (domain ? '; Domain=' + domain : '');
      });
    });
  }
  function load() {
    if (!accepted || !production || loaded) return;
    loaded = true;
    command('consent', 'default', denied);
    command('set', 'allow_google_signals', false);
    command('set', 'allow_ad_personalization_signals', false);
    // Only approved campaign labels and bounded click IDs may enter Analytics.
    // Free-text UTMs can contain names, phone numbers or search terms.
    const clean = new URL(location.href);
    const campaignLabels = {
      utm_source: ['google', 'araya_audit'],
      utm_medium: ['cpc', 'diagnostic'],
      utm_campaign: ['araya_ej_services']
    };
    for (const name of [...clean.searchParams.keys()]) {
      const values = clean.searchParams.getAll(name);
      const value = values[0];
      const clickId = /^(gclid|gbraid|wbraid)$/.test(name)
        && /^[A-Za-z0-9_-]{16,256}$/.test(value) && /[A-Za-z]/.test(value);
      if (values.length !== 1 || !(clickId || campaignLabels[name]?.includes(value))) {
        clean.searchParams.delete(name);
      }
    }
    clean.hash = '';
    command('set', 'page_location', clean.href);
    command('set', 'page_referrer', document.referrer ? new URL(document.referrer).origin : '');
    command('consent', 'update', {...denied, analytics_storage:'granted'});
    window['ga-disable-' + measurementId] = false;
    window.dataLayer.push({'gtm.start':Date.now(),event:'gtm.js'});
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtm.js?id=GTM-NK3C3RVZ';
    document.head.appendChild(script);
  }
  function show() {
    if (!banner) return;
    banner.hidden = false;
    banner.dataset.choice = accepted ? 'accepted' : 'not-accepted';
    if (status) status.textContent = accepted
      ? (status.dataset?.accepted || 'Analytics is currently accepted.')
      : (status.dataset?.disabled || 'Optional analytics is currently off.');
  }
  function choose(value) {
    accepted = value;
    try { window.localStorage.setItem(key, JSON.stringify({version:1,analytics:value,at:Date.now()})); } catch (_) { storageUsable = false; /* Choice still applies to this page. */ }
    if (banner) banner.hidden = true;
    if (returnFocus) { returnFocus.focus(); returnFocus = null; }
    if (value) load();
    else {
      window['ga-disable-' + measurementId] = true;
      clearCookies();
      if (loaded) location.reload(); // Unload third-party listeners; no post-withdrawal analytics command.
    }
  }
  function methodFor(href) {
    try {
      const url = new URL(href, location.href);
      if (url.protocol === 'https:' && url.hostname === 'wa.me' && url.pathname === '/6281326396262' && !url.username && !url.password) return 'whatsapp';
      if (url.protocol === 'tel:' && url.pathname === '+62317877990') return 'phone';
      if (url.protocol === 'mailto:' && url.pathname.toLowerCase() === 'cs@arayainternusa.com') return 'email';
    } catch (_) { /* Non-web links are not measurement targets. */ }
    return null;
  }
  document.addEventListener('click', event => {
    const action = event.target.closest?.('[data-consent-action]');
    if (action) {
      const value = action.dataset.consentAction;
      if (value === 'accept') choose(true);
      else if (value === 'reject') choose(false);
      else if (value === 'open') { returnFocus = action; show(); banner?.querySelector?.('button')?.focus(); }
      return;
    }
    if (!accepted || !production || !loaded) return;
    if (storageUsable && !readChoice()?.analytics && storageUsable) return;
    const anchor = event.target.closest?.('a[href]');
    const method = anchor && methodFor(anchor.href);
    if (!method) return;
    const cta = anchor.dataset.contactLocation;
    const page = location.pathname.split('/').filter(Boolean)[0] || 'home';
    window.dataLayer.push({event:'contact_click',contact_method:method,
      cta_location:['hero','utility','contact','footer'].includes(cta) ? cta : 'unknown',
      page_group:['noris','comap','privacy'].includes(page) ? page : 'home'});
  });
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    const choice = validChoice(event.newValue);
    if (!choice?.analytics) {
      accepted = false;
      window['ga-disable-' + measurementId] = true;
      clearCookies();
      if (loaded) location.reload();
      else show();
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && returnFocus) { banner.hidden = true; returnFocus.focus(); returnFocus = null; }
  });
  const choice = readChoice();
  accepted = choice?.analytics === true;
  if (!choice) show();
  if (accepted) load();
})();
