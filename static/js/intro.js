/* =============================================
   NEXGEAR – Cybersport Intro Animation
   intro.js
   ============================================= */
'use strict';

(function () {
  /* ---- CONFIG ---- */
  const TOTAL_DUR   = 3800; // ms before auto-exit
  const GREEN       = '#44d62c';
  const GREEN_DIM   = '#1a5c10';
  const GREEN_BRIGHT= '#8fff79';

  let animId, loadInterval, glitchInterval, sparksId;
  let started = false;

  /* ---- MATRIX RAIN ---- */
  function initMatrix() {
    const canvas = document.getElementById('matrixCanvas');
    if (!canvas) return;
    const ctx  = canvas.getContext('2d');

    function resize() {
      canvas.width  = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const chars  = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+-=[]{}|;:<>?,./~`\\\'\"';
    const fontSize = 14;
    let cols = Math.floor(window.innerWidth / fontSize);
    let drops = Array(cols).fill(0).map(() => Math.random() * -50);

    function drawMatrix() {
      cols = Math.floor(canvas.width / fontSize);
      while (drops.length < cols) drops.push(Math.random() * -50);

      ctx.fillStyle = 'rgba(0,0,0,0.055)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < cols; i++) {
        const ch = chars[Math.floor(Math.random() * chars.length)];
        const y  = drops[i] * fontSize;

        // Bright head
        ctx.fillStyle = '#ffffff';
        ctx.font = `bold ${fontSize}px monospace`;
        ctx.fillText(ch, i * fontSize, y);

        // Trail – varying green brightness
        const brightness = Math.random();
        if (brightness > 0.92) {
          ctx.fillStyle = GREEN_BRIGHT;
        } else if (brightness > 0.5) {
          ctx.fillStyle = GREEN;
        } else {
          ctx.fillStyle = GREEN_DIM;
        }
        ctx.font = `${fontSize}px monospace`;
        ctx.fillText(chars[Math.floor(Math.random() * chars.length)], i * fontSize, y - fontSize);

        if (y > canvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i] += 0.5 + Math.random() * 0.5;
      }

      animId = requestAnimationFrame(drawMatrix);
    }
    drawMatrix();
  }

  /* ---- SPARKS / PARTICLES ---- */
  function createSpark() {
    const overlay = document.getElementById('introOverlay');
    if (!overlay) return;

    const spark = document.createElement('div');
    spark.className = 'intro-spark';

    const x    = Math.random() * 100;
    const y    = Math.random() * 100;
    const size = Math.random() * 4 + 1;
    const dur  = Math.random() * 2000 + 800;
    const hue  = Math.random() > 0.7
      ? `hsl(${Math.random() * 40 + 100}, 100%, 70%)`   // green-yellow
      : (Math.random() > 0.5 ? '#ffffff' : GREEN_BRIGHT);

    Object.assign(spark.style, {
      left:     `${x}%`,
      top:      `${y}%`,
      width:    `${size}px`,
      height:   `${size}px`,
      background: hue,
      boxShadow: `0 0 ${size * 4}px ${hue}`,
      animationDuration: `${dur}ms`,
    });

    overlay.appendChild(spark);
    setTimeout(() => spark.remove(), dur + 200);
  }

  /* ---- LOADING BAR ---- */
  const loadMessages = [
    'INITIALIZING...',
    'LOADING ASSETS...',
    'CALIBRATING RGB...',
    'SYNCING DATABASE...',
    'BOOTING NEXGEAR...',
    'READY.',
  ];

  function animateLoad() {
    const bar  = document.getElementById('introBar');
    const txt  = document.getElementById('introLoadText');
    if (!bar || !txt) return;

    let pct = 0;
    let msgIdx = 0;

    loadInterval = setInterval(() => {
      const step = Math.random() * 18 + 4;
      pct = Math.min(100, pct + step);
      bar.style.width = pct + '%';

      // update message
      const newIdx = Math.floor((pct / 100) * (loadMessages.length - 1));
      if (newIdx !== msgIdx) {
        msgIdx = newIdx;
        txt.style.opacity = '0';
        setTimeout(() => {
          txt.textContent = loadMessages[msgIdx];
          txt.style.opacity = '1';
        }, 120);
      }

      if (pct >= 100) {
        clearInterval(loadInterval);
        txt.textContent = loadMessages[loadMessages.length - 1];
        txt.style.color = GREEN_BRIGHT;
        setTimeout(exitIntro, 400);
      }
    }, 220);
  }

  /* ---- GLITCH EFFECT ---- */
  function startGlitch() {
    const logo = document.querySelector('.intro-logo');
    if (!logo) return;

    glitchInterval = setInterval(() => {
      if (Math.random() > 0.75) {
        logo.classList.add('glitching');
        setTimeout(() => logo.classList.remove('glitching'), 120 + Math.random() * 200);
      }
    }, 400);
  }

  /* ---- CHROMATIC BURST (color flash on exit) ---- */
  function chromaticBurst() {
    const overlay = document.getElementById('introOverlay');
    if (!overlay) return;

    const burst = document.createElement('div');
    burst.className = 'intro-burst';
    overlay.appendChild(burst);

    // Force reflow then animate
    burst.getBoundingClientRect();
    burst.classList.add('burst-go');
    setTimeout(() => burst.remove(), 800);
  }

  /* ---- EXIT ---- */
  function exitIntro() {
    if (started) return;
    started = true;

    clearInterval(loadInterval);
    clearInterval(glitchInterval);
    cancelAnimationFrame(animId);
    clearInterval(sparksId);

    chromaticBurst();

    const overlay = document.getElementById('introOverlay');
    if (!overlay) return;

    setTimeout(() => {
      overlay.classList.add('intro-exit');
      setTimeout(() => {
        overlay.style.display = 'none';
        document.body.style.overflow = '';
      }, 900);
    }, 250);
  }

  /* ---- BOOT ---- */
  function boot() {
    document.body.style.overflow = 'hidden';

    initMatrix();
    animateLoad();
    startGlitch();

    // Sparks burst
    sparksId = setInterval(createSpark, 80);

    // Auto exit
    setTimeout(exitIntro, TOTAL_DUR);

    // Skip button
    document.getElementById('introSkip')?.addEventListener('click', () => {
      const bar = document.getElementById('introBar');
      if (bar) bar.style.width = '100%';
      setTimeout(exitIntro, 50);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
