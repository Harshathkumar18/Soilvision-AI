/* ============================================================
   SoilVision AI — Main JavaScript
   Navigation, AI Chat, Scroll effects, Language toggle
   ============================================================ */
'use strict';

// ── Sticky Header ──────────────────────────────────────────
const header = document.getElementById('siteHeader');
if (header) {
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });
}

// ── Mobile Navigation ──────────────────────────────────────
const mobileToggle = document.getElementById('mobileNavToggle');
const navMenu      = document.getElementById('siteNavMenu');
if (mobileToggle && navMenu) {
  mobileToggle.addEventListener('click', () => {
    navMenu.classList.toggle('mobile-open');
    const icon = mobileToggle.querySelector('i');
    icon.className = navMenu.classList.contains('mobile-open')
      ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
  });
  // Close on outside click
  document.addEventListener('click', e => {
    if (!header.contains(e.target)) {
      navMenu.classList.remove('mobile-open');
      const icon = mobileToggle.querySelector('i');
      if (icon) icon.className = 'fa-solid fa-bars';
    }
  });
}

// ── Language Toggle ────────────────────────────────────────
const btnLang = document.getElementById('btnLangToggle');
if (btnLang) {
  btnLang.addEventListener('click', async () => {
    const current  = btnLang.dataset.lang || 'en';
    const newLang  = current === 'en' ? 'te' : 'en';
    try {
      await fetch('/set-language', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: newLang })
      });
      location.reload();
    } catch (e) { console.warn('Language switch failed', e); }
  });
}

// ── AI Chat Drawer ─────────────────────────────────────────
const aiFloatingBtn = document.getElementById('aiFloatingBtn');
const aiDrawer      = document.getElementById('aiDrawer');
const aiCloseBtn    = document.getElementById('aiCloseBtn');
const aiChatBody    = document.getElementById('aiChatBody');
const aiChatInput   = document.getElementById('aiChatInput');
const aiSendBtn     = document.getElementById('aiSendBtn');

function openDrawer()  { if (aiDrawer) aiDrawer.classList.add('open'); }
function closeDrawer() { if (aiDrawer) aiDrawer.classList.remove('open'); }

if (aiFloatingBtn) aiFloatingBtn.addEventListener('click', openDrawer);
if (aiCloseBtn)    aiCloseBtn.addEventListener('click', closeDrawer);

function appendChatBubble(text, role) {
  const div = document.createElement('div');
  div.className = `chat-bubble ${role}`;
  div.innerHTML = text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  aiChatBody.appendChild(div);
  aiChatBody.scrollTop = aiChatBody.scrollHeight;
  return div;
}

function showTyping() {
  const t = document.createElement('div');
  t.className = 'chat-typing'; t.id = 'typingIndicator';
  t.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
  aiChatBody.appendChild(t);
  aiChatBody.scrollTop = aiChatBody.scrollHeight;
}
function hideTyping() {
  const t = document.getElementById('typingIndicator');
  if (t) t.remove();
}

async function sendChat() {
  const msg = aiChatInput ? aiChatInput.value.trim() : '';
  if (!msg) return;
  aiChatInput.value = '';
  appendChatBubble(msg, 'user');
  showTyping();
  try {
    const res  = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    hideTyping();
    appendChatBubble(data.reply || 'Sorry, I could not generate a response.', 'bot');
  } catch (e) {
    hideTyping();
    appendChatBubble('Network error — please check your connection and try again.', 'bot');
  }
}

if (aiSendBtn)   aiSendBtn.addEventListener('click', sendChat);
if (aiChatInput) {
  aiChatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); }
  });
}

// ── Scroll-reveal (for pages that use .fade-up) ────────────
const fadeObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      fadeObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.fade-up').forEach(el => fadeObserver.observe(el));

// ── Education Card Toggles ─────────────────────────────────
document.querySelectorAll('.edu-card-header').forEach(header => {
  header.addEventListener('click', () => {
    const card = header.closest('.edu-card');
    card.classList.toggle('open');
  });
});

// ── Problem Card Toggles ───────────────────────────────────
document.querySelectorAll('.problem-card-header').forEach(h => {
  h.addEventListener('click', () => {
    const card = h.closest('.problem-card');
    const isOpen = card.classList.contains('open');
    document.querySelectorAll('.problem-card.open').forEach(c => c.classList.remove('open'));
    if (!isOpen) card.classList.add('open');
  });
});

// ── Auto-open problem from hash ────────────────────────────
function openProblemFromHash() {
  const hash = window.location.hash.slice(1);
  if (hash) {
    const target = document.getElementById(hash);
    if (target && target.classList.contains('problem-card')) {
      target.classList.add('open');
      setTimeout(() => target.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
    }
  }
}
openProblemFromHash();
window.addEventListener('hashchange', openProblemFromHash);
