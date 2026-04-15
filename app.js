/* eslint-disable */
'use strict';

// =============================================
// NEXGEAR – app.js
// =============================================

// ---- DATA ----
const products = [
  /* ---- MOUSE ---- */
  {
    id: 1, category: 'mouse', brand: 'Razer',
    name: 'Razer DeathAdder V3 Pro', emoji: '🖱️',
    price: 1_890_000, oldPrice: 2_200_000,
    rating: 4.9, reviews: 842,
    badge: 'hot', isNew: false
  },
  {
    id: 2, category: 'mouse', brand: 'Logitech',
    name: 'Logitech G Pro X Superlight 2', emoji: '🖱️',
    price: 2_350_000, oldPrice: null,
    rating: 4.8, reviews: 613,
    badge: 'new', isNew: true
  },
  {
    id: 3, category: 'mouse', brand: 'ZOWIE',
    name: 'BenQ ZOWIE EC2-CW Wireless', emoji: '🖱️',
    price: 1_490_000, oldPrice: 1_700_000,
    rating: 4.7, reviews: 421,
    badge: 'sale', isNew: false
  },
  /* ---- KEYBOARD ---- */
  {
    id: 4, category: 'keyboard', brand: 'Corsair',
    name: 'Corsair K100 RGB Mechanical', emoji: '⌨️',
    price: 3_250_000, oldPrice: 3_800_000,
    rating: 4.9, reviews: 976,
    badge: 'hot', isNew: false
  },
  {
    id: 5, category: 'keyboard', brand: 'Razer',
    name: 'Razer Huntsman V3 Pro TKL', emoji: '⌨️',
    price: 2_990_000, oldPrice: null,
    rating: 4.8, reviews: 534,
    badge: 'new', isNew: true
  },
  {
    id: 6, category: 'keyboard', brand: 'HyperX',
    name: 'HyperX Alloy Origins 65 RGB', emoji: '⌨️',
    price: 1_750_000, oldPrice: 2_100_000,
    rating: 4.7, reviews: 389,
    badge: 'sale', isNew: false
  },
  /* ---- HEADSET ---- */
  {
    id: 7, category: 'headset', brand: 'SteelSeries',
    name: 'SteelSeries Arctis Nova Pro', emoji: '🎧',
    price: 4_200_000, oldPrice: 4_800_000,
    rating: 4.9, reviews: 1203,
    badge: 'hot', isNew: false
  },
  {
    id: 8, category: 'headset', brand: 'Razer',
    name: 'Razer BlackShark V2 Pro 2024', emoji: '🎧',
    price: 2_890_000, oldPrice: null,
    rating: 4.8, reviews: 712,
    badge: 'new', isNew: true
  },
  /* ---- MOUSEPAD ---- */
  {
    id: 9, category: 'mousepad', brand: 'Logitech',
    name: 'Logitech G840 XL Gaming Pad', emoji: '🎯',
    price: 450_000, oldPrice: 590_000,
    rating: 4.6, reviews: 2187,
    badge: 'sale', isNew: false
  },
  {
    id: 10, category: 'mousepad', brand: 'Corsair',
    name: 'Corsair MM700 RGB Extended', emoji: '🎯',
    price: 890_000, oldPrice: null,
    rating: 4.7, reviews: 863,
    badge: 'new', isNew: true
  },
  /* ---- MONITOR ---- */
  {
    id: 11, category: 'monitor', brand: 'ASUS ROG',
    name: 'ASUS ROG Swift PG27AQN 360Hz', emoji: '🖥️',
    price: 12_500_000, oldPrice: 14_000_000,
    rating: 4.9, reviews: 342,
    badge: 'hot', isNew: false
  },
  {
    id: 12, category: 'monitor', brand: 'LG',
    name: 'LG UltraGear 27GR95QE OLED', emoji: '🖥️',
    price: 9_800_000, oldPrice: null,
    rating: 4.8, reviews: 519,
    badge: 'new', isNew: true
  },
];

// ---- STATE ----
let cart = JSON.parse(localStorage.getItem('nexgear_cart') || '[]');
let currentFilter = 'all';
let wishlist = new Set(JSON.parse(localStorage.getItem('nexgear_wish') || '[]'));

// ---- FORMAT PRICE ----
function formatPrice(n) {
  return n.toLocaleString('uz-UZ') + ' so\'m';
}

// ---- STARS ----
function stars(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  return '★'.repeat(full) + (half ? '½' : '') + '☆'.repeat(empty);
}

// =====================
// RENDER PRODUCTS
// =====================
function renderProducts(filter = 'all') {
  const grid = document.getElementById('productsGrid');
  if (!grid) return;
  const filtered = filter === 'all' ? products : products.filter(p => p.category === filter);

  grid.innerHTML = filtered.map((p, i) => `
    <div class="product-card" data-id="${p.id}" style="animation-delay:${i * 0.05}s">
      ${p.badge ? `<div class="product-badge badge-${p.badge}">${p.badge === 'new' ? 'Yangi' : p.badge === 'hot' ? '🔥 Hot' : '% Sale'}</div>` : ''}
      <div class="product-img-wrap" onclick="quickView(${p.id})">
        <div class="product-emoji">${p.emoji}</div>
      </div>
      <div class="product-info">
        <div class="product-brand">${p.brand}</div>
        <div class="product-name">${p.name}</div>
        <div class="product-rating">
          <span class="stars">${stars(p.rating)}</span>
          <span class="rating-count">(${p.reviews.toLocaleString()})</span>
        </div>
        <div class="product-price-row">
          <span class="product-price">${formatPrice(p.price)}</span>
          ${p.oldPrice ? `<span class="product-old-price">${formatPrice(p.oldPrice)}</span>` : ''}
        </div>
        <div class="product-footer">
          <button class="btn-cart" onclick="addToCart(${p.id})" id="cart-btn-${p.id}">
            🛒 Savatga
          </button>
          <button class="btn-wish ${wishlist.has(p.id) ? 'active' : ''}" onclick="toggleWish(${p.id})" id="wish-btn-${p.id}" aria-label="Sevimlilar">
            ${wishlist.has(p.id) ? '❤️' : '🤍'}
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

// =====================
// FILTER
// =====================
function initFilter() {
  const tabs = document.getElementById('filterTabs');
  if (!tabs) return;
  tabs.addEventListener('click', e => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    tabs.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderProducts(currentFilter);
  });

  // Category cards are now handled by initCatalog()

}

// =====================
// CART
// =====================
function saveCart() {
  localStorage.setItem('nexgear_cart', JSON.stringify(cart));
}

function addToCart(id) {
  const product = products.find(p => p.id === id);
  if (!product) return;

  const existing = cart.find(i => i.id === id);
  if (existing) {
    existing.qty++;
  } else {
    cart.push({ ...product, qty: 1 });
  }
  saveCart();
  updateCartUI();
  showToast(`✅ ${product.name} savatga qo'shildi!`);

  // animate button
  const btn = document.getElementById(`cart-btn-${id}`);
  if (btn) {
    btn.textContent = '✓ Qo\'shildi!';
    btn.style.background = '#5bff3a';
    setTimeout(() => {
      btn.textContent = '🛒 Savatga';
      btn.style.background = '';
    }, 1500);
  }
}

function removeFromCart(id) {
  cart = cart.filter(i => i.id !== id);
  saveCart();
  updateCartUI();
}

function changeQty(id, delta) {
  const item = cart.find(i => i.id === id);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) removeFromCart(id);
  else { saveCart(); updateCartUI(); }
}

function updateCartUI() {
  const count = cart.reduce((s, i) => s + i.qty, 0);
  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  const savings = cart.reduce((s, i) => i.oldPrice ? s + (i.oldPrice - i.price) * i.qty : s, 0);
  const countEl = document.getElementById('cartCount');
  const itemsEl = document.getElementById('cartItems');
  const footerEl = document.getElementById('cartFooter');

  // Badge
  if (countEl) {
    countEl.textContent = count;
    countEl.classList.toggle('show', count > 0);
  }

  // Items
  if (itemsEl) {
    if (cart.length === 0) {
      itemsEl.innerHTML = `
        <div class="cart-empty">
          <div class="empty-icon">🛒</div>
          <p>Savatingiz bo'sh</p>
        </div>`;
      if (footerEl) footerEl.style.display = 'none';
    } else {
      itemsEl.innerHTML = cart.map(item => `
        <div class="cart-item">
          <div class="cart-item-emoji">${item.emoji}</div>
          <div class="cart-item-info">
            <div class="cart-item-name">${item.name}</div>
            <div class="cart-item-price">${formatPrice(item.price)} × ${item.qty} = <strong>${formatPrice(item.price * item.qty)}</strong></div>
            <div class="cart-item-qty">
              <button class="qty-btn" onclick="changeQty(${item.id}, -1)">−</button>
              <span class="qty-val">${item.qty}</span>
              <button class="qty-btn" onclick="changeQty(${item.id}, 1)">+</button>
            </div>
          </div>
          <button class="cart-item-del" onclick="removeFromCart(${item.id})" aria-label="O'chirish">🗑️</button>
        </div>`).join('');

      if (footerEl) {
        footerEl.style.display = 'block';
        // Build detailed total section
        const cartTotalDiv = document.querySelector('.cart-total');
        if (cartTotalDiv) {
          let html = `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
            <span style="font-size:.78rem;color:var(--text-muted)">Jami:</span>
            <span style="font-family:var(--font-head);font-size:1.1rem;color:var(--green);font-weight:900">${formatPrice(total)}</span>
          </div>`;
          if (savings > 0) {
            html += `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
              <span style="font-size:.74rem;color:var(--text-muted)">Tejash:</span>
              <span style="font-size:.78rem;color:#facc15;font-weight:700">−${formatPrice(savings)}</span>
            </div>`;
          }
          html += `<div style="display:flex;justify-content:space-between;align-items:center;padding-top:8px;border-top:1px solid var(--border-dim)">
            <span style="font-size:.72rem;color:var(--text-muted)">Mahsulotlar soni:</span>
            <span style="font-size:.78rem;color:#fff;font-weight:700">${count} ta</span>
          </div>`;
          cartTotalDiv.innerHTML = html;
        }
      }
    }
  }
}


function openCart() {
  document.getElementById('cartSidebar').classList.add('open');
  document.getElementById('cartOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeCart() {
  document.getElementById('cartSidebar').classList.remove('open');
  document.getElementById('cartOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

// =====================
// WISHLIST
// =====================
function saveWish() { localStorage.setItem('nexgear_wish', JSON.stringify([...wishlist])); }

function toggleWish(id) {
  const product = products.find(p => p.id === id);
  if (wishlist.has(id)) {
    wishlist.delete(id);
    showToast('💔 Sevimlilardan olib tashlandi');
  } else {
    wishlist.add(id);
    showToast(`❤️ ${product?.name} sevimliylarga qo'shildi!`);
  }
  saveWish();
  const btn = document.getElementById(`wish-btn-${id}`);
  if (btn) {
    btn.classList.toggle('active', wishlist.has(id));
    btn.textContent = wishlist.has(id) ? '❤️' : '🤍';
  }
}

// =====================
// QUICK VIEW
// =====================
function quickView(id) {
  const p = products.find(x => x.id === id);
  if (!p) return;
  showToast(`👀 ${p.name} — ${p.brand}`);
}

// =====================
// TOAST
// =====================
let toastTimer;
function showToast(msg) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}

// =====================
// NAVBAR SCROLL
// =====================
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const backTop = document.getElementById('backTop');
  const links = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    navbar.classList.toggle('scrolled', y > 40);
    if (backTop) backTop.classList.toggle('show', y > 500);

    // Active link on scroll
    const sections = ['home', 'categories', 'products', 'brands', 'contact'];
    sections.forEach(id => {
      const sec = document.getElementById(id);
      if (!sec) return;
      const rect = sec.getBoundingClientRect();
      if (rect.top <= 100 && rect.bottom >= 100) {
        links.forEach(l => l.classList.remove('active'));
        const active = document.querySelector(`.nav-link[href="#${id}"]`);
        if (active) active.classList.add('active');
      }
    });
  });

  backTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// =====================
// SEARCH
// =====================
function initSearch() {
  const btn = document.getElementById('searchBtn');
  const bar = document.getElementById('searchBar');
  const closeBtn = document.getElementById('searchClose');
  const input = document.getElementById('searchInput');

  btn?.addEventListener('click', () => {
    bar.classList.toggle('open');
    if (bar.classList.contains('open')) input?.focus();
  });
  closeBtn?.addEventListener('click', () => bar.classList.remove('open'));

  input?.addEventListener('input', e => {
    const q = e.target.value.trim().toLowerCase();
    if (!q) { renderProducts(currentFilter); return; }
    const filtered = products.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.brand.toLowerCase().includes(q) ||
      p.category.toLowerCase().includes(q)
    );
    const grid = document.getElementById('productsGrid');
    if (grid) {
      grid.innerHTML = filtered.map((p, i) => `
        <div class="product-card" data-id="${p.id}" style="animation-delay:${i * 0.05}s">
          ${p.badge ? `<div class="product-badge badge-${p.badge}">${p.badge === 'new' ? 'Yangi' : p.badge === 'hot' ? '🔥 Hot' : '% Sale'}</div>` : ''}
          <div class="product-img-wrap">
            <div class="product-emoji">${p.emoji}</div>
          </div>
          <div class="product-info">
            <div class="product-brand">${p.brand}</div>
            <div class="product-name">${p.name}</div>
            <div class="product-rating">
              <span class="stars">${stars(p.rating)}</span>
              <span class="rating-count">(${p.reviews.toLocaleString()})</span>
            </div>
            <div class="product-price-row">
              <span class="product-price">${formatPrice(p.price)}</span>
              ${p.oldPrice ? `<span class="product-old-price">${formatPrice(p.oldPrice)}</span>` : ''}
            </div>
            <div class="product-footer">
              <button class="btn-cart" onclick="addToCart(${p.id})" id="cart-btn-${p.id}">🛒 Savatga</button>
              <button class="btn-wish ${wishlist.has(p.id) ? 'active' : ''}" onclick="toggleWish(${p.id})" id="wish-btn-${p.id}">
                ${wishlist.has(p.id) ? '❤️' : '🤍'}
              </button>
            </div>
          </div>
        </div>
      `).join('') || '<div style="grid-column:1/-1;text-align:center;color:var(--text-muted);padding:40px">Hech narsa topilmadi 😕</div>';
    }
    document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' });
  });
}

// =====================
// MOBILE MENU
// =====================
function initMobileMenu() {
  const toggle = document.getElementById('menuToggle');
  const links = document.getElementById('navLinks');

  toggle?.addEventListener('click', () => {
    links?.classList.toggle('open');
    toggle.classList.toggle('open');
  });

  links?.addEventListener('click', e => {
    if (e.target.classList.contains('nav-link')) {
      links.classList.remove('open');
    }
  });
}

// =====================
// COUNTER ANIMATION
// =====================
function animateCounters() {
  const nums = document.querySelectorAll('.stat-num');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = +el.dataset.target;
      const dur = 1500;
      const start = performance.now();
      const tick = now => {
        const t = Math.min((now - start) / dur, 1);
        el.textContent = Math.floor(t * target).toLocaleString();
        if (t < 1) requestAnimationFrame(tick);
        else el.textContent = target.toLocaleString();
      };
      requestAnimationFrame(tick);
      observer.unobserve(el);
    });
  }, { threshold: .5 });
  nums.forEach(n => observer.observe(n));
}

// =====================
// PARTICLES
// =====================
function createParticles() {
  const wrap = document.getElementById('particles');
  if (!wrap) return;
  const colors = ['#44d62c', '#2d9e1c', '#8fff79', '#ffffff'];
  for (let i = 0; i < 25; i++) {
    const el = document.createElement('div');
    el.className = 'particle';
    const size = Math.random() * 4 + 1;
    el.style.cssText = `
      width:${size}px; height:${size}px;
      left:${Math.random() * 100}%;
      background:${colors[Math.floor(Math.random() * colors.length)]};
      animation-duration:${Math.random() * 18 + 10}s;
      animation-delay:${Math.random() * 12}s;
      box-shadow: 0 0 ${size * 3}px currentColor;
    `;
    wrap.appendChild(el);
  }
}

// =====================
// NEWSLETTER
// =====================
function initNewsletter() {
  document.getElementById('nlForm')?.addEventListener('submit', e => {
    e.preventDefault();
    const email = document.getElementById('nlEmail')?.value;
    if (email) {
      showToast(`🎉 ${email} manzili bilan obuna bo'ldingiz!`);
      document.getElementById('nlEmail').value = '';
    }
  });
}

// =====================
// INIT
// =====================
// (Initialization moved to bottom of file — see EXTENDED INIT)
// =====================


// =====================
// CATALOG PAGES
// =====================
const catalogMeta = {
  mouse: { label: 'Sichqoncha', icon: '🖱️' },
  keyboard: { label: 'Klaviatura', icon: '⌨️' },
  headset: { label: 'Headset', icon: '🎧' },
  monitor: { label: 'Monitor', icon: '🖥️' },
  chair: { label: 'Gaming Stul', icon: '🪑' },
  mousepad: { label: 'Mousepad', icon: '🎯' },
};

function openCatalog(filter) {
  // create section if not exists
  let sec = document.getElementById('catalogSection');
  if (!sec) {
    sec = document.createElement('section');
    sec.id = 'catalogSection';
    sec.className = 'catalog-section';
    // insert right before #products
    const prodSec = document.getElementById('products');
    prodSec.parentNode.insertBefore(sec, prodSec);
  }

  const meta = catalogMeta[filter] || { label: filter, icon: '📦' };
  const items = products.filter(p => p.category === filter);

  sec.innerHTML = `
    <div class="container">
      <div class="catalog-header">
        <button class="catalog-back" onclick="closeCatalog()">← Orqaga</button>
        <div class="catalog-title">${meta.icon} <span>${meta.label}</span> Katalogi</div>
        <div style="font-size:.8rem;color:var(--text-muted);margin-left:auto">${items.length} mahsulot</div>
      </div>
      <div class="products-grid" id="catalogGrid">
        ${items.map((p, i) => `
          <div class="product-card" data-id="${p.id}" style="animation-delay:${i * 0.06}s">
            ${p.badge ? `<div class="product-badge badge-${p.badge}">${p.badge === 'new' ? 'Yangi' : p.badge === 'hot' ? '🔥 Hot' : '% Sale'}</div>` : ''}
            <div class="product-img-wrap" onclick="quickView(${p.id})">
              <div class="product-emoji">${p.emoji}</div>
            </div>
            <div class="product-info">
              <div class="product-brand">${p.brand}</div>
              <div class="product-name">${p.name}</div>
              <div class="product-rating">
                <span class="stars">${stars(p.rating)}</span>
                <span class="rating-count">(${p.reviews.toLocaleString()})</span>
              </div>
              <div class="product-price-row">
                <span class="product-price">${formatPrice(p.price)}</span>
                ${p.oldPrice ? `<span class="product-old-price">${formatPrice(p.oldPrice)}</span>` : ''}
              </div>
              <div class="product-footer">
                <button class="btn-cart" onclick="addToCart(${p.id})" id="cart-btn-${p.id}">🛒 Savatga</button>
                <button class="btn-wish ${wishlist.has(p.id) ? 'active' : ''}" onclick="toggleWish(${p.id})" id="wish-btn-${p.id}">${wishlist.has(p.id) ? '❤️' : '🤍'}</button>
              </div>
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  `;

  sec.classList.add('active');
  sec.scrollIntoView({ behavior: 'smooth' });
}

function closeCatalog() {
  const sec = document.getElementById('catalogSection');
  if (sec) {
    sec.classList.remove('active');
    document.getElementById('categories')?.scrollIntoView({ behavior: 'smooth' });
  }
}

function initCatalog() {
  document.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('click', () => {
      const filter = card.dataset.filter;
      openCatalog(filter);
    });
  });
}

// =====================
// THEME TOGGLE (Day / Night)
// =====================
function initTheme() {
  const saved = localStorage.getItem('nexgear_theme') || 'dark';
  applyTheme(saved);

  document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);
  document.getElementById('adminToggleTheme')?.addEventListener('click', toggleTheme);
}

function toggleTheme() {
  const isLight = document.body.classList.contains('light-mode');
  applyTheme(isLight ? 'dark' : 'light');
}

function applyTheme(mode) {
  const isLight = mode === 'light';
  document.body.classList.toggle('light-mode', isLight);
  localStorage.setItem('nexgear_theme', mode);

  // Update theme icons
  const themeIcon = document.querySelector('.theme-icon');
  if (themeIcon) themeIcon.textContent = isLight ? '🌙' : '☀️';

  const adminThemeBtn = document.getElementById('adminToggleTheme');
  if (adminThemeBtn) adminThemeBtn.textContent = isLight ? '☀️ Kunduzgi' : '🌙 Tungi';
}

// =====================
// ADMIN PANEL
// =====================
let adminProductsList = [...products]; // editable copy

function openAdmin() {
  document.getElementById('adminPanel').classList.add('open');
  document.getElementById('adminOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
  renderAdminProducts();
  updateAdminStats();
}

function closeAdmin() {
  document.getElementById('adminPanel').classList.remove('open');
  document.getElementById('adminOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

function initAdminTabs() {
  document.querySelectorAll('.admin-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.admin-tab-pane').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(`tab-${tab.dataset.tab}`)?.classList.add('active');
      if (tab.dataset.tab === 'stats') updateAdminStats();
    });
  });
}

function renderAdminProducts(filter = '') {
  const tbody = document.getElementById('adminProductsTbody');
  if (!tbody) return;

  const filtered = filter
    ? adminProductsList.filter(p =>
      p.name.toLowerCase().includes(filter) ||
      p.brand.toLowerCase().includes(filter) ||
      p.category.toLowerCase().includes(filter)
    )
    : adminProductsList;

  const catMap = { mouse: 'Sichqoncha', keyboard: 'Klaviatura', headset: 'Headset', monitor: 'Monitor', mousepad: 'Mousepad', chair: 'Stul' };

  tbody.innerHTML = filtered.map(p => `
    <tr>
      <td><code style="color:var(--green);font-size:.7rem">#${p.id}</code></td>
      <td style="font-size:1.3rem">${p.emoji}</td>
      <td style="max-width:180px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${p.name}</td>
      <td>${p.brand}</td>
      <td><span style="background:var(--green-soft);color:var(--green);padding:2px 8px;border-radius:3px;font-size:.7rem;font-weight:700;text-transform:uppercase">${catMap[p.category] || p.category}</span></td>
      <td style="color:var(--green);font-weight:700">${formatPrice(p.price)}</td>
      <td>${p.badge ? `<span class="product-badge badge-${p.badge}" style="position:static;display:inline-block">${p.badge}</span>` : '—'}</td>
      <td>
        <button class="admin-edit-btn" onclick="editProduct(${p.id})">✏️ Tahrir</button>
        <button class="admin-del-btn" onclick="deleteProduct(${p.id})">🗑️ O'chirish</button>
      </td>
    </tr>
  `).join('') || `<tr><td colspan="8" style="text-align:center;color:var(--text-muted);padding:30px">Hech narsa topilmadi</td></tr>`;
}

function updateAdminStats() {
  const totalItems = cart.reduce((s, i) => s + i.qty, 0);
  const totalVal = cart.reduce((s, i) => s + i.price * i.qty, 0);

  const el = id => document.getElementById(id);
  if (el('statProducts')) el('statProducts').textContent = adminProductsList.length;
  if (el('statCartItems')) el('statCartItems').textContent = totalItems;
  if (el('statWishlist')) el('statWishlist').textContent = wishlist.size;
  if (el('statRevenue')) el('statRevenue').textContent = formatPrice(totalVal);
}

function editProduct(id) {
  const p = adminProductsList.find(x => x.id === id);
  if (!p) return;

  document.getElementById('formProductId').value = p.id;
  document.getElementById('formName').value = p.name;
  document.getElementById('formBrand').value = p.brand;
  document.getElementById('formCategory').value = p.category;
  document.getElementById('formBadge').value = p.badge || '';
  document.getElementById('formPrice').value = p.price;
  document.getElementById('formOldPrice').value = p.oldPrice || '';
  document.getElementById('formRating').value = p.rating;
  document.getElementById('formReviews').value = p.reviews;
  document.getElementById('productFormTitle').textContent = 'Mahsulotni Tahrirlash';
  document.getElementById('productFormOverlay').classList.add('open');
}

function deleteProduct(id) {
  if (!confirm('Bu mahsulotni o\'chirmoqchimisiz?')) return;
  const idx = adminProductsList.findIndex(p => p.id === id);
  const pIdx = products.findIndex(p => p.id === id);
  if (idx > -1) adminProductsList.splice(idx, 1);
  if (pIdx > -1) products.splice(pIdx, 1);
  renderAdminProducts();
  renderProducts(currentFilter);
  showToast('🗑️ Mahsulot o\'chirildi');
}

function saveProductForm() {
  const id = parseInt(document.getElementById('formProductId').value);
  const name = document.getElementById('formName').value.trim();
  const brand = document.getElementById('formBrand').value.trim();
  const category = document.getElementById('formCategory').value;
  const badge = document.getElementById('formBadge').value;
  const price = parseInt(document.getElementById('formPrice').value);
  const oldPrice = parseInt(document.getElementById('formOldPrice').value) || null;
  const rating = parseFloat(document.getElementById('formRating').value);
  const reviews = parseInt(document.getElementById('formReviews').value);

  if (!name || !brand || !price) {
    showToast('⚠️ Iltimos, majburiy maydonlarni to\'ldiring!');
    return;
  }

  const catEmoji = { mouse: '🖱️', keyboard: '⌨️', headset: '🎧', monitor: '🖥️', mousepad: '🎯', chair: '🪑' };

  if (id) {
    // Edit existing
    const p = adminProductsList.find(x => x.id === id);
    const pOrig = products.find(x => x.id === id);
    const updated = { ...p, name, brand, category, badge: badge || null, price, oldPrice, rating, reviews, emoji: catEmoji[category] || '📦' };
    if (p) Object.assign(p, updated);
    if (pOrig) Object.assign(pOrig, updated);
    showToast('✅ Mahsulot yangilandi!');
  } else {
    // Add new
    const newId = Math.max(...adminProductsList.map(x => x.id), 0) + 1;
    const newProduct = {
      id: newId, category, brand, name,
      emoji: catEmoji[category] || '📦',
      price, oldPrice, rating: rating || 4.5,
      reviews: reviews || 0,
      badge: badge || null, isNew: badge === 'new'
    };
    adminProductsList.push(newProduct);
    products.push(newProduct);
    showToast(`✅ ${name} qo'shildi!`);
  }

  renderAdminProducts();
  renderProducts(currentFilter);
  closeProductForm();
}

function openAddProductForm() {
  document.getElementById('formProductId').value = '';
  document.getElementById('formName').value = '';
  document.getElementById('formBrand').value = '';
  document.getElementById('formCategory').value = 'mouse';
  document.getElementById('formBadge').value = '';
  document.getElementById('formPrice').value = '';
  document.getElementById('formOldPrice').value = '';
  document.getElementById('formRating').value = '4.5';
  document.getElementById('formReviews').value = '0';
  document.getElementById('productFormTitle').textContent = 'Mahsulot Qo\'shish';
  document.getElementById('productFormOverlay').classList.add('open');
}

function closeProductForm() {
  document.getElementById('productFormOverlay').classList.remove('open');
}



// =====================
// HERO SWIPER CAROUSEL
// =====================
function initHeroSwiper() {
  if (typeof Swiper === 'undefined') return;

  const AUTOPLAY_DELAY = 5000; // 5 seconds per slide

  const heroSwiper = new Swiper('.heroSwiper', {
    // Core
    loop: true,
    speed: 900,
    grabCursor: true,

    // Effect – smooth fade-slide hybrid
    effect: 'slide',

    // Autoplay
    autoplay: {
      delay: AUTOPLAY_DELAY,
      disableOnInteraction: false,
      pauseOnMouseEnter: true,
    },

    // Pagination dots
    pagination: {
      el: '.hs-pagination',
      clickable: true,
      dynamicBullets: false,
    },

    // Custom navigation arrows
    navigation: {
      nextEl: '#hsNext',
      prevEl: '#hsPrev',
    },

    // Keyboard control
    keyboard: { enabled: true },

    // Accessibility
    a11y: {
      prevSlideMessage: 'Oldingi slayd',
      nextSlideMessage: 'Keyingi slayd',
    },
  });

  // ── Slide counter ──
  const currentEl = document.getElementById('hsCurrent');
  const updateCounter = () => {
    if (!currentEl) return;
    const real = heroSwiper.realIndex + 1;
    currentEl.textContent = String(real).padStart(2, '0');
  };
  heroSwiper.on('slideChange', updateCounter);
  updateCounter();

  // ── Progress bar ──
  const bar = document.getElementById('hsProgressBar');
  if (bar) {
    let prog = null;
    const startProgress = () => {
      bar.style.transition = 'none';
      bar.style.width = '0%';
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          bar.style.transition = `width ${AUTOPLAY_DELAY}ms linear`;
          bar.style.width = '100%';
        });
      });
    };
    heroSwiper.on('autoplayStart', startProgress);
    heroSwiper.on('slideChange', startProgress);
    heroSwiper.on('autoplayStop', () => {
      bar.style.transition = 'none';
      bar.style.width = '0%';
    });
    startProgress();
  }

  // ── Content animation on slide change ──
  const animateSlide = (swiper) => {
    const activeSlide = swiper.slides[swiper.activeIndex];
    if (!activeSlide) return;
    const content = activeSlide.querySelector('.hs-content');
    const visual  = activeSlide.querySelector('.hs-visual');
    if (content) {
      content.style.animation = 'none';
      void content.offsetWidth; // reflow
      content.style.animation = 'hs-content-in .7s cubic-bezier(.4,0,.2,1) forwards';
    }
    if (visual) {
      visual.style.animation = 'none';
      void visual.offsetWidth;
      visual.style.animation = 'hs-visual-in .7s cubic-bezier(.4,0,.2,1) .1s forwards';
    }
  };
  heroSwiper.on('slideChangeTransitionStart', animateSlide);
}

// =====================
// EXTENDED INIT
// =====================
document.addEventListener('DOMContentLoaded', () => {
  renderProducts();
  initFilter();
  initNavbar();
  initSearch();
  initMobileMenu();
  animateCounters();
  createParticles();
  initNewsletter();
  updateCartUI();
  initCatalog();
  initTheme();
  initAdminTabs();
  initHeroSwiper();

  // Cart toggle
  document.getElementById('cartBtn')?.addEventListener('click', openCart);
  document.getElementById('cartClose')?.addEventListener('click', closeCart);
  document.getElementById('cartOverlay')?.addEventListener('click', closeCart);

  // Admin panel toggle
  document.getElementById('adminBtn')?.addEventListener('click', openAdmin);
  document.getElementById('adminClose')?.addEventListener('click', closeAdmin);
  document.getElementById('adminOverlay')?.addEventListener('click', closeAdmin);

  // Admin product search
  document.getElementById('adminProductSearch')?.addEventListener('input', e => {
    renderAdminProducts(e.target.value.trim().toLowerCase());
  });

  // Add product button
  document.getElementById('addProductBtn')?.addEventListener('click', openAddProductForm);

  // Product form
  document.getElementById('productFormSave')?.addEventListener('click', saveProductForm);
  document.getElementById('productFormClose')?.addEventListener('click', closeProductForm);
  document.getElementById('productFormCancel')?.addEventListener('click', closeProductForm);

  // Clear cart from admin
  document.getElementById('clearCartAdmin')?.addEventListener('click', () => {
    if (cart.length === 0) { showToast('Savatcha allaqachon bo\'sh'); return; }
    if (confirm('Savatchani tozalashni xohlaysizmi?')) {
      cart = [];
      saveCart();
      updateCartUI();
      showToast('🗑️ Savatcha tozalandi');
    }
  });

  // Nav links smooth active
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
      link.classList.add('active');
    });
  });

  // ================================================================
  //  PRODUCT DETAIL MODAL
  // ================================================================
  const productDetailData = {
    mouse: {
      image: 'assets/slide1.png',
      brand: 'RAZER · DeathAdder V3 Pro',
      category: '🖱️ Gaming Mouse',
      name: 'Razer DeathAdder V3 Pro',
      desc: 'Razer DeathAdder V3 Pro — professional kibersport musobaqalari uchun maxsus ishlab chiqilgan simsiz gaming sichqonchasi. Focus Pro 30K sensori, HyperSpeed simsiz texnologiyasi va zamonaviy ergonomik dizayni bilan u bozoridagi eng yaxshi tanlovdir. Ultra yengil 63g og\'irligi bilan uzoq vaqt o\'yinda charchash sezilmaydi.',
      price: '1 890 000 so\'m',
      oldPrice: '2 200 000 so\'m',
      discount: '−14%',
      accentColor: '#44d62c',
      specs: [
        { val: '30,000', label: 'DPI Sensor' },
        { val: '63g', label: 'Og\'irlik' },
        { val: '70 soat', label: 'Batareya umri' },
        { val: '0.2ms', label: 'Javob vaqti' },
        { val: '750 IPS', label: 'Tracking' },
        { val: 'USB-C', label: 'Zaryadlash' }
      ],
      features: [
        'Focus Pro 30K optik sensori — 99.8% aniqlik',
        'HyperSpeed simsiz texnologiya — 0.2ms kechikish',
        'Razer Mechanical Gen-3 tugmalari — 90 million bosish',
        'Ergonomik shakl — o\'ng qo\'l uchun optimallashtirilgan',
        '100% PTFE sichqoncha oyoqlari — silliq harakatlanish',
        'Bluetooth + 2.4GHz dual wireless rejimi',
        'RGB Chroma — 16.8 million rang',
        'On-board xotira — 5 profil saqlash'
      ]
    },
    keyboard: {
      image: 'assets/slide2.png',
      brand: 'CORSAIR · K100 RGB Mechanical',
      category: '⌨️ Mexanik Klaviatura',
      name: 'Corsair K100 RGB',
      desc: 'Corsair K100 RGB — premium mexanik gaming klaviaturasi. OPX optik-mexanik switchlari 0.2ms javob vaqtini ta\'minlaydi va 100 million bosishga chidamli. iCUE boshqaruvi orqali per-key RGB yoritilishni to\'liq sozlash mumkin. Alüminium ramka mustahkamlik va premium ko\'rinishni beradi.',
      price: '2 990 000 so\'m',
      oldPrice: '3 500 000 so\'m',
      discount: '−15%',
      accentColor: '#c084fc',
      specs: [
        { val: 'OPX', label: 'Switch turi' },
        { val: '0.2ms', label: 'Javob vaqti' },
        { val: 'Per-Key', label: 'RGB rejimi' },
        { val: '100M', label: 'Kalit umri' },
        { val: '4000Hz', label: 'Polling rate' },
        { val: 'Alüminium', label: 'Korpus' }
      ],
      features: [
        'OPX optik-mexanik switch — 1.0mm aktiv nuqta',
        'AXON texnologiyasi — 4000Hz hyper-polling',
        'Per-key RGB LED — iCUE bilan to\'liq boshqarish',
        'Alüminium okvir — premium sifat va mustahkamlik',
        'iCUE Control Wheel — media va profil boshqaruvi',
        'N-Key Rollover — barcha tugmalar bir vaqtda',
        'USB passthrough port — qurilma ulash uchun',
        'Detachable palm rest — qo\'l qulay joylashishi'
      ]
    },
    headset: {
      image: 'assets/slide3.png',
      brand: 'STEELSERIES · Arctis Nova Pro',
      category: '🎧 Gaming Headset',
      name: 'SteelSeries Arctis Nova Pro',
      desc: 'SteelSeries Arctis Nova Pro Wireless — audiophile darajadagi gaming garniturasi. Hi-Res Audio sertifikatlangan 40mm custom drayverlar bilan ajoyib ovoz sifati. 360° Spatial Audio va ANC texnologiyalari bilan siz o\'yinga to\'liq cho\'masiz. Dual batareya tizimi — hech qachon zaryadlash uchun kutmayasiz.',
      price: '4 200 000 so\'m',
      oldPrice: '4 800 000 so\'m',
      discount: '−13%',
      accentColor: '#22d3ee',
      specs: [
        { val: '40mm', label: 'Neodimium driver' },
        { val: '7.1', label: 'Surround Sound' },
        { val: 'ANC', label: 'Noise Cancel' },
        { val: '50 soat', label: 'Batareya umri' },
        { val: 'Hi-Res', label: 'Audio sifati' },
        { val: 'USB-C', label: 'Zaryadlash' }
      ],
      features: [
        'Premium Hi-Res Audio sertifikatlangan drayverlar',
        '360° Spatial Audio — Tempest 3D va Dolby Atmos',
        '4-darajali Active Noise Cancellation (ANC)',
        'Dual batareya tizimi — uzluksiz o\'yin',
        'Retractable boom mikrofon — ClearCast texnologiyasi',
        'Multi-platform qo\'llab-quvvatlash — PC, PS5, Switch',
        'OLED displeyli DAC — real vaqt sozlamalari',
        'ComfortMAX tizimi — aylanuvchi quloq yostiqlari'
      ]
    },
    monitor: {
      image: 'assets/slide4.png',
      brand: 'ASUS ROG · Swift PG27AQN 360Hz',
      category: '🖥️ Gaming Monitor',
      name: 'ASUS ROG Swift OLED PG27AQN',
      desc: 'ASUS ROG Swift PG27AQN — dunyodagi eng tezkor 360Hz OLED gaming monitori. 27" 4K QD-OLED paneli 0.03ms javob vaqti bilan ultra-silliq tasvirni ta\'minlaydi. HDR10 va 1000 nit yorqinlik bilan ranglar jonli ko\'rinadi. NVIDIA G-SYNC compatible texnologiyasi tearing va stuttering muammolarini bartaraf etadi.',
      price: '12 500 000 so\'m',
      oldPrice: '14 000 000 so\'m',
      discount: '−11%',
      accentColor: '#fb923c',
      specs: [
        { val: '360Hz', label: 'Yangilanish tezligi' },
        { val: '4K', label: 'QD-OLED panel' },
        { val: '0.03ms', label: 'Javob vaqti (GTG)' },
        { val: 'HDR10', label: 'HDR standarti' },
        { val: '1000nit', label: 'Yorqinlik' },
        { val: 'DP 2.1', label: 'DisplayPort' }
      ],
      features: [
        '27" 4K QD-OLED panel — to\'yingan ranglar',
        '360Hz yangilanish tezligi — ultra smooth gameplay',
        '0.03ms GTG javob vaqti — ghosting yo\'q',
        'NVIDIA G-SYNC Compatible — tearing bartaraf',
        'HDR10 + 1000 nit — cinematic tajriba',
        'DisplayPort 2.1 + HDMI 2.1 portlari',
        'ROG ergonomik stend — bo\'yini, burchagi sozlanadi',
        '10-bit rang chuqurligi — 1.07 milliard rang'
      ]
    }
  };

  // Open modal
  function openProductDetail(productId) {
    const data = productDetailData[productId];
    if (!data) return;

    const modal   = document.getElementById('pdModal');
    const overlay = document.getElementById('pdOverlay');

    document.getElementById('pdImage').src = data.image;
    document.getElementById('pdImage').alt = data.name;
    document.getElementById('pdBrand').textContent = data.brand;
    document.getElementById('pdCategory').textContent = data.category;
    document.getElementById('pdCategory').style.color = data.accentColor;
    document.getElementById('pdCategory').style.borderColor = data.accentColor;
    document.getElementById('pdName').textContent = data.name;
    document.getElementById('pdDesc').textContent = data.desc;
    document.getElementById('pdPrice').textContent = data.price;
    document.getElementById('pdPrice').style.color = data.accentColor;
    document.getElementById('pdOldPrice').textContent = data.oldPrice;
    document.getElementById('pdDiscountTag').textContent = data.discount;
    document.getElementById('pdDiscountTag').style.color = data.accentColor;
    document.getElementById('pdDiscountTag').style.background = data.accentColor + '20';

    // Specs
    const specsEl = document.getElementById('pdSpecs');
    specsEl.innerHTML = data.specs.map(s => `
      <div class="pd-spec-card">
        <span class="pd-spec-val" style="color:${data.accentColor}">${s.val}</span>
        <span class="pd-spec-label">${s.label}</span>
      </div>
    `).join('');

    // Features
    const featEl = document.getElementById('pdFeatures');
    featEl.innerHTML = `
      <div class="pd-features-title">Xususiyatlari</div>
      <ul class="pd-feat-list">
        ${data.features.map(f => `<li style="--accent:${data.accentColor}">${f}</li>`).join('')}
      </ul>
    `;

    // Cart button color
    const cartBtn = document.getElementById('pdCartBtn');
    cartBtn.style.background = data.accentColor;
    cartBtn.style.boxShadow = `0 0 28px ${data.accentColor}55`;
    cartBtn.onclick = () => {
      showToast(`✅ ${data.name} savatchaga qo'shildi!`);
    };

    // Show
    overlay.classList.add('active');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeProductDetail() {
    document.getElementById('pdModal').classList.remove('active');
    document.getElementById('pdOverlay').classList.remove('active');
    document.body.style.overflow = '';
  }

  // Event listeners
  document.querySelectorAll('.hs-detail-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      openProductDetail(btn.dataset.product);
    });
  });

  document.getElementById('pdClose')?.addEventListener('click', closeProductDetail);
  document.getElementById('pdBackBtn')?.addEventListener('click', closeProductDetail);
  document.getElementById('pdOverlay')?.addEventListener('click', closeProductDetail);

  // ESC to close
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && document.getElementById('pdModal')?.classList.contains('active')) {
      closeProductDetail();
    }
  });

});
