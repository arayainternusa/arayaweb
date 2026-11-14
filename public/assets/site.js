// The `js` class is set inline in <head> so the collapsed mobile menu is styled before first paint.
// Service and application links reveal their explanation, including nested deep links.
const revealApplication = (hash) => {
  if (!hash || hash === '#') return;
  let id;
  try { id = decodeURIComponent(hash.slice(1)); } catch (_) { return; }
  const target = document.getElementById(id);
  let disclosure = target?.closest('details');
  while (disclosure) {
    disclosure.open = true;
    disclosure = disclosure.parentElement?.closest('details');
  }
};
revealApplication(window.location.hash);
window.addEventListener('hashchange', () => revealApplication(window.location.hash));
document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href]');
  if (link && link.origin === location.origin &&
      link.pathname.replace(/index\.html$/, '') === location.pathname.replace(/index\.html$/, '')) {
    revealApplication(link.hash);
  }
});
const diagramViewer = document.querySelector('.diagram-viewer');
if (diagramViewer && typeof diagramViewer.showModal === 'function') {
  const image = diagramViewer.querySelector('.diagram-stage img');
  const stage = diagramViewer.querySelector('.diagram-stage');
  const zoomOut = diagramViewer.querySelector('[data-zoom="out"]');
  const zoomIn = diagramViewer.querySelector('[data-zoom="in"]');
  let trigger, zoom = 1, imageWidth = 900, imageHeight = 506;
  const resizeDiagram = () => {
    const fitWidth = Math.min(imageWidth, Math.max(1, stage.clientWidth - 32), Math.max(1, stage.clientHeight - 32) * imageWidth / imageHeight);
    image.style.width = `${fitWidth * zoom}px`;
    diagramViewer.querySelector('.diagram-zoom-status').textContent = `${Math.round(zoom * 100)}%`;
    zoomOut.disabled = zoom <= 1;
    zoomIn.disabled = zoom >= 3;
  };
  document.querySelectorAll('.diagram-trigger').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      trigger = link;
      const thumbnail = link.querySelector('img');
      image.src = link.href;
      image.alt = thumbnail.alt;
      imageWidth = Number(thumbnail.getAttribute('width'));
      imageHeight = Number(thumbnail.getAttribute('height'));
      diagramViewer.querySelector('#diagram-viewer-title').textContent = link.dataset.diagramCaption;
      zoom = 1;
      diagramViewer.showModal();
      document.body.classList.add('diagram-view-open');
      resizeDiagram();
      stage.scrollTop = stage.scrollLeft = 0;
    });
  });
  diagramViewer.querySelector('.diagram-close').addEventListener('click', () => diagramViewer.close());
  diagramViewer.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const controls = [...diagramViewer.querySelectorAll('button:not(:disabled), a[href], [tabindex="0"]')];
    const first = controls[0], last = controls[controls.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
  diagramViewer.querySelectorAll('[data-zoom]').forEach(button => {
    button.addEventListener('click', () => {
      zoom = button.dataset.zoom === 'reset' ? 1 : Math.max(1, Math.min(3, zoom + (button.dataset.zoom === 'in' ? .5 : -.5)));
      resizeDiagram();
      if (zoom === 1) stage.scrollTop = stage.scrollLeft = 0;
    });
  });
  diagramViewer.addEventListener('click', event => {
    if (event.target !== diagramViewer) return;
    const box = diagramViewer.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) diagramViewer.close();
  });
  diagramViewer.addEventListener('close', () => {
    document.body.classList.remove('diagram-view-open');
    trigger?.focus({preventScroll:true});
  });
  window.addEventListener('resize', () => { if (diagramViewer.open) resizeDiagram(); });
}
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-navigation');
const brandMenu = document.querySelector('.brand-menu');
if (brandMenu) {
  document.addEventListener('click', (event) => {
    if (!brandMenu.contains(event.target)) brandMenu.open = false;
  });
  brandMenu.addEventListener('focusout', (event) => {
    if (event.relatedTarget && !brandMenu.contains(event.relatedTarget)) brandMenu.open = false;
  });
}
if (menuButton && navigation) {
  const setMenu = (open) => {
    menuButton.setAttribute('aria-expanded', String(open));
    navigation.dataset.open = String(open);
    menuButton.querySelector('span').textContent = open ? 'Close' : 'Menu';
    if (!open && brandMenu) brandMenu.open = false;
    document.dispatchEvent(new Event('navigation-layout'));
  };
  menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
  navigation.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    if (brandMenu && brandMenu.open) {
      brandMenu.open = false;
      brandMenu.querySelector('summary').focus();
    } else if (menuButton.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      menuButton.focus();
    }
  });
  window.matchMedia('(min-width: 981px)').addEventListener('change', () => setMenu(false));
}
// Shared header and main navigation. Independent of optional contents components.
(() => {
  const header = document.querySelector('.site-header');
  const nav = document.querySelector('#main-navigation');
  if (!header || !nav) return;
  const normalize = path => path.replace(/index\.html$/, '').replace(/\/$/, '');
  const path = normalize(location.pathname);
  const links = [...nav.querySelectorAll('a')];
  const pageLink = links.find(link => !link.hash && normalize(link.pathname) === path);
  const brandSummary = document.querySelector('.brand-menu summary');
  const brandPage = Boolean(pageLink?.closest('.brand-menu'));
  const sections = links.filter(link => link.hash && normalize(link.pathname) === path)
    .map(link => ({control:link, target:document.getElementById(link.hash.slice(1))}))
    .filter(item => item.target);
  const brands = document.getElementById('brands');
  if (brands && brandSummary) sections.push({control:brandSummary, target:brands});
  let pending = false;
  const update = () => {
    pending = false;
    const edge = Math.max(0, header.getBoundingClientRect().bottom);
    document.documentElement.style.setProperty('--header-edge', `${edge}px`);
    // Anchor destinations use the settled sticky height, even when the utility bar is visible.
    if (typeof getComputedStyle === 'function') {
      const stickyTop = parseFloat(getComputedStyle(header).top) || 0;
      const settledEdge = Math.max(0, header.getBoundingClientRect().height + stickyTop);
      document.documentElement.style.setProperty('--anchor-header', `${settledEdge}px`);
    }
    document.documentElement.style.setProperty('--index-height', '0px');
    // Include the upper reading area, not only the exact sticky-header boundary.
    const threshold = edge + Math.min(180, Math.max(0, (window.innerHeight - edge) / 3));
    const reached = sections.filter(item => item.target.getBoundingClientRect().top <= threshold);
    reached.sort((a, b) => a.target.getBoundingClientRect().top - b.target.getBoundingClientRect().top);
    let current = reached[reached.length - 1]?.control;
    const atEnd = window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4;
    const contact = sections.find(item => item.control.hash === '#contact');
    if (atEnd && contact && contact.target.getBoundingClientRect().top < window.innerHeight) current = contact.control;
    links.forEach(link => link.removeAttribute('aria-current'));
    brandSummary?.removeAttribute('aria-current');
    if (current) current.setAttribute('aria-current', 'location');
    else pageLink?.setAttribute('aria-current', 'page');
    if (brandSummary) brandSummary.dataset.current = brandPage ? 'page' : '';
  };
  const schedule = () => {
    if (!pending) { pending = true; requestAnimationFrame(update); }
  };
  window.addEventListener('scroll', schedule, {passive:true});
  ['resize', 'hashchange', 'popstate', 'load'].forEach(event => window.addEventListener(event, schedule));
  // Menu collapse must publish its smaller offset before the browser follows an anchor.
  document.addEventListener('navigation-layout', update);
  if ('ResizeObserver' in window || typeof ResizeObserver !== 'undefined') new ResizeObserver(schedule).observe(header);
  update();
})();

// Home on the current page returns to the top without reloading or replaying entrances.
document.addEventListener('click', event => {
  const link = event.target.closest('a[href]');
  if (!link || event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
  const normalize = path => path.replace(/index\.html$/, '').replace(/\/$/, '');
  if (link.origin !== location.origin || normalize(link.pathname) !== normalize(location.pathname) || link.hash || link.search !== location.search) return;
  if (!link.closest('.navigation')) return;
  event.preventDefault();
  history.pushState(null, '', link.pathname + link.search);
  window.scrollTo({top:0, behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches ? 'instant' : 'smooth'});
});

// Short text-only entrances: pictures and large sections never wait for a fade.
const motionPreference = window.matchMedia('(prefers-reduced-motion:reduce)');
if ('IntersectionObserver' in window && typeof Element.prototype.animate === 'function') {
  const running = new Set();
  const entranceObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entranceObserver.unobserve(entry.target);
      if (motionPreference.matches) return;
      const animation = entry.target.animate(
        [{transform:'translateY(8px)'}, {transform:'translateY(0)'}],
        {duration:entry.target.closest('.hero-content,.brand-landing-grid') ? 950 : 600, easing:'cubic-bezier(.22,.61,.36,1)'});
      running.add(animation);
      animation.finished.catch(() => {}).finally(() => running.delete(animation));
    });
  }, {threshold:.12});
  document.querySelectorAll('.hero-content>.eyebrow,.hero-content>h1,.hero-description,.brand-landing-grid>div>.eyebrow,.brand-landing-grid>div>h1,.brand-intro,.section-heading,.service-body>h3,.brand-panel>h3,.brand-toc-heading,.portfolio-group-title,.application-group-intro h3,.enquiry-list h3')
    .forEach(element => entranceObserver.observe(element));
  motionPreference.addEventListener('change', () => {
    if (motionPreference.matches) running.forEach(animation => animation.cancel());
  });
}

document.querySelectorAll('[data-service-photo-slider]').forEach(slider => {
  const track = slider.querySelector('.service-photo-track');
  const controls = slider.querySelector('.service-photo-controls');
  const status = controls.querySelector('span');
  const count = track.children.length;
  let current = 0;
  let next = null;

  const move = step => {
    const from = next ?? current;
    next = (from + step + count) % count;
    const wrapped = Math.abs(next - from) > 1;
    track.scrollTo({
      left: next * track.clientWidth,
      behavior: motionPreference.matches || wrapped ? 'instant' : 'smooth',
    });
  };

  track.addEventListener('scroll', () => {
    const index = Math.round(track.scrollLeft / track.clientWidth);
    if (index === current || index < 0 || index >= count) return;
    current = index;
    status.textContent = `${current + 1} / ${count}`;
  }, {passive:true});
  track.addEventListener('scrollend', () => { next = null; });
  track.addEventListener('pointerdown', () => { next = null; });
  track.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    move(event.key === 'ArrowLeft' ? -1 : 1);
  });
  controls.querySelectorAll('[data-photo-step]').forEach(button => {
    button.addEventListener('click', () => move(Number(button.dataset.photoStep)));
  });
  controls.hidden = false;
});

// Metric counters: text only, once per metric, with no extra network request.
(() => {
  const metrics = [...document.querySelectorAll('[data-count]')];
  if (!metrics.length) return;
  const preference = window.matchMedia('(prefers-reduced-motion:reduce)');
  if (preference.matches || !('IntersectionObserver' in window)) return;
  const format = new Intl.NumberFormat('en-US');
  const active = new Map();
  const counted = new WeakSet();
  const finish = (element, state) => {
    cancelAnimationFrame(state.frame);
    element.textContent = format.format(state.target) + state.suffix;
    active.delete(element);
  };
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const element = entry.target;
      observer.unobserve(element);
      if (counted.has(element)) return;
      counted.add(element);
      if (preference.matches) return;
      const target = Number(element.dataset.count || element.textContent.replace(/[^0-9]/g, ''));
      if (!Number.isFinite(target) || target < 0) return;
      const largeCounter = target >= 1000;
      const duration = largeCounter ? 2000 : 800;
      const state = {target, suffix:element.dataset.countSuffix || '', start:null, frame:0};
      const step = now => {
        if (!active.has(element)) return;
        if (state.start === null) state.start = now;
        const progress = (now - state.start) / duration;
        if (progress >= 1) {
          finish(element, state);
          return;
        }
        if (largeCounter) {
          // Hold a steady pace for the first 30%, then ease to a stop.
          const steadyUntil = 0.3;
          const slowdownDuration = 1 - steadyUntil;
          const slowdownElapsed = Math.max(0, progress - steadyUntil);
          const distance = progress - slowdownElapsed ** 2 / (2 * slowdownDuration);
          const totalDistance = steadyUntil + slowdownDuration / 2;
          element.textContent = format.format(Math.floor(target * distance / totalDistance)) + state.suffix;
        } else {
          element.textContent = format.format(Math.round(target * (1 - (1 - progress) ** 3))) + state.suffix;
        }
        state.frame = requestAnimationFrame(step);
      };
      active.set(element, state);
      state.frame = requestAnimationFrame(step);
    });
  }, {threshold:0.4});
  metrics.forEach(element => observer.observe(element));
  const finishAll = () => active.forEach((state, element) => finish(element, state));
  preference.addEventListener('change', () => { if (preference.matches) finishAll(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) finishAll(); });
  document.addEventListener('company-date-updated', event => {
    active.forEach((state, element) => {
      if (element.hasAttribute('data-company-age')) {
        state.target = event.detail.age;
        finish(element, state);
      }
    });
  });
})();
