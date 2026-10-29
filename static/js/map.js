/* ============================================================
   SoilVision AI — Interactive Map Script
   Leaflet.js Agro-Ecological Soil Zones & Farm Location Pinning
   ============================================================ */
'use strict';

let map;
let customMarker = null;
let savedMarkers = [];
let zones = [];

// Custom marker icons
function makeMarkerIcon(color) {
  return L.divIcon({
    className: '',
    html: `<div style="
      width:14px;height:14px;
      background:${color};
      border:2px solid rgba(255,255,255,0.85);
      border-radius:50%;
      box-shadow:0 0 12px ${color}90;
    "></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7]
  });
}

function makeFarmIcon() {
  return L.divIcon({
    className: '',
    html: `<div style="
      background:#22c55e;color:#fff;
      border-radius:50% 50% 50% 0;
      width:30px;height:30px;
      display:flex;align-items:center;justify-content:center;
      font-size:13px;
      border:2px solid rgba(255,255,255,0.9);
      box-shadow:0 0 16px rgba(34,197,94,0.7);
      transform:rotate(-45deg);
    "><span style="transform:rotate(45deg)">🌱</span></div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 30]
  });
}

function makeSavedFarmIcon() {
  return L.divIcon({
    className: '',
    html: `<div style="
      background:#3b82f6;color:#fff;
      border-radius:50% 50% 50% 0;
      width:26px;height:26px;
      display:flex;align-items:center;justify-content:center;
      font-size:11px;
      border:2px solid rgba(255,255,255,0.9);
      box-shadow:0 0 12px rgba(59,130,246,0.6);
      transform:rotate(-45deg);
    "><span style="transform:rotate(45deg)">📍</span></div>`,
    iconSize: [26, 26],
    iconAnchor: [13, 26]
  });
}

// Initialize map
function initMap() {
  map = L.map('soilMap', {
    center: [21.5, 78.9],
    zoom: 5,
    zoomControl: true,
    attributionControl: true
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 18
  }).addTo(map);

  map.on('click', onMapClick);
}

function onMapClick(e) {
  const { lat, lng } = e.latlng;

  if (customMarker) { map.removeLayer(customMarker); }

  customMarker = L.marker([lat, lng], { icon: makeFarmIcon() })
    .addTo(map)
    .bindPopup(`<div style="color:#e2f5e2;font-size:0.82rem;"><strong>Pinned Farm Location</strong><br>Lat: ${lat.toFixed(5)}<br>Lng: ${lng.toFixed(5)}</div>`)
    .openPopup();

  // Show selected location card and populate form
  const card = document.getElementById('selectedLocationCard');
  const info = document.getElementById('selectedLocationInfo');
  const latInput = document.getElementById('locLat');
  const lngInput = document.getElementById('locLng');

  if (card && info) {
    card.style.display = 'block';
    if (latInput) latInput.value = lat.toFixed(6);
    if (lngInput) lngInput.value = lng.toFixed(6);

    info.innerHTML = `
      <div class="report-param-grid" style="grid-template-columns:1fr 1fr;">
        <div class="report-param-item">
          <div class="report-param-label">Latitude</div>
          <div class="report-param-value" style="font-size:1.1rem;color:var(--clr-primary-light);">${lat.toFixed(5)}° N</div>
        </div>
        <div class="report-param-item">
          <div class="report-param-label">Longitude</div>
          <div class="report-param-value" style="font-size:1.1rem;color:var(--clr-primary-light);">${lng.toFixed(5)}° E</div>
        </div>
      </div>`;
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

// Clear pin
const clearBtn = document.getElementById('clearLocationBtn');
if (clearBtn) {
  clearBtn.addEventListener('click', () => {
    if (customMarker) { map.removeLayer(customMarker); customMarker = null; }
    const card = document.getElementById('selectedLocationCard');
    if (card) card.style.display = 'none';
  });
}

// Save Location Form
const saveLocForm = document.getElementById('saveLocationForm');
if (saveLocForm) {
  saveLocForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('btnSaveLoc');
    const name = document.getElementById('locName').value.trim();
    const lat = document.getElementById('locLat').value;
    const lng = document.getElementById('locLng').value;
    const notes = document.getElementById('locNotes').value.trim();

    if (!name || !lat || !lng) return;

    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';

    try {
      const res = await fetch('/api/locations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          farm_name: name,
          latitude: parseFloat(lat),
          longitude: parseFloat(lng),
          notes: notes
        })
      });
      const data = await res.json();
      if (data.status === 'success') {
        saveLocForm.reset();
        document.getElementById('selectedLocationCard').style.display = 'none';
        if (customMarker) { map.removeLayer(customMarker); customMarker = null; }
        await loadSavedLocations();
      }
    } catch(err) {
      console.error('Error saving location:', err);
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-bookmark"></i> Save Farm Location';
    }
  });
}

// Load Saved Locations
async function loadSavedLocations() {
  try {
    const res = await fetch('/api/locations');
    const locs = await res.json();
    renderSavedLocations(locs);
  } catch(e) {
    console.error('Could not load saved locations:', e);
  }
}

function renderSavedLocations(locs) {
  // Clear existing saved markers
  savedMarkers.forEach(m => map.removeLayer(m));
  savedMarkers = [];

  const countEl = document.getElementById('savedLocCount');
  const listEl = document.getElementById('savedLocationsList');

  if (countEl) countEl.textContent = locs.length;

  if (!locs || locs.length === 0) {
    if (listEl) listEl.innerHTML = '<div class="text-sm text-muted">No saved farm locations yet. Click anywhere on the map to pin and save your fields.</div>';
    return;
  }

  // Add markers to map
  locs.forEach(loc => {
    const marker = L.marker([loc.latitude, loc.longitude], { icon: makeSavedFarmIcon() })
      .addTo(map)
      .bindPopup(`
        <div style="color:#e2f5e2;font-size:0.82rem;">
          <strong style="color:#60a5fa;font-size:0.9rem;">📍 ${loc.farm_name}</strong><br>
          <span style="color:#7aaa7a;">${loc.notes || 'No notes'}</span><br>
          <span style="font-size:0.75rem;">Lat: ${loc.latitude.toFixed(4)}, Lng: ${loc.longitude.toFixed(4)}</span>
        </div>
      `);
    savedMarkers.push(marker);
  });

  // Render list
  if (listEl) {
    listEl.innerHTML = `
      <div style="display:flex;flex-direction:column;gap:var(--space-3);">
        ${locs.map(l => `
          <div class="card" style="padding:var(--space-3) var(--space-4);display:flex;justify-content:space-between;align-items:center;margin:0;">
            <div>
              <strong style="color:var(--clr-text);font-size:0.88rem;">${l.farm_name}</strong>
              <div class="text-xs text-muted">
                Lat: ${l.latitude.toFixed(4)}, Lng: ${l.longitude.toFixed(4)}
                ${l.notes ? ` &bull; ${l.notes}` : ''}
              </div>
            </div>
            <div style="display:flex;gap:var(--space-2);">
              <button class="btn btn-secondary btn-sm" onclick="flyToCoords(${l.latitude}, ${l.longitude})" title="View on map">
                <i class="fa-solid fa-crosshairs"></i>
              </button>
              <button class="btn btn-danger btn-sm" onclick="deleteLocation(${l.id})" title="Delete location">
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }
}

window.flyToCoords = function(lat, lng) {
  if (map) {
    map.flyTo([lat, lng], 10, { duration: 1.5 });
  }
};

window.deleteLocation = async function(id) {
  if (!confirm('Are you sure you want to delete this saved location?')) return;
  try {
    await fetch(`/api/locations/${id}/delete`, { method: 'POST' });
    await loadSavedLocations();
  } catch(e) {
    console.error('Failed to delete location', e);
  }
};

// Load zone data
async function loadZones() {
  try {
    const res  = await fetch('/api/map-data');
    const data = await res.json();
    zones = data.zones || [];
    renderZoneList(zones);
    addZoneMarkers(zones);
  } catch(e) {
    const zoneList = document.getElementById('zoneList');
    if (zoneList) zoneList.innerHTML = '<p class="text-sm text-muted text-center">Could not load zone data.</p>';
  }
}

function addZoneMarkers(zones) {
  zones.forEach(zone => {
    const marker = L.marker([zone.lat, zone.lng], { icon: makeMarkerIcon(zone.color) })
      .addTo(map);

    const popupHtml = `
      <div style="min-width:240px;color:#e2f5e2;">
        <div style="font-weight:700;font-size:0.9rem;margin-bottom:6px;color:#4ade80;">${zone.name}</div>
        <div style="font-size:0.77rem;color:#7aaa7a;margin-bottom:8px;">${zone.coverage}</div>
        <div style="font-size:0.77rem;"><strong style="color:#a3e635;">pH:</strong> ${zone.ph_range}</div>
        <div style="font-size:0.77rem;"><strong style="color:#a3e635;">Key Crops:</strong> ${zone.key_crops}</div>
        <div style="font-size:0.77rem;margin-top:4px;"><strong style="color:#fbbf24;">Threats:</strong> ${zone.major_threats}</div>
      </div>`;

    marker.bindPopup(popupHtml, { maxWidth: 280 });
    marker.on('click', () => showZoneDetail(zone));
  });
}

function renderZoneList(zones) {
  const zoneList = document.getElementById('zoneList');
  if (!zoneList) return;
  zoneList.innerHTML = zones.map(z => `
    <div class="zone-item" onclick="flyToZone('${z.id}')">
      <div class="zone-dot" style="background:${z.color};box-shadow:0 0 6px ${z.color}80;"></div>
      <div>
        <div class="zone-name">${z.name.split('(')[0].trim()}</div>
        <div class="zone-desc">${z.ph_range} pH</div>
      </div>
    </div>`).join('');
}

window.flyToZone = function(id) {
  const zone = zones.find(z => z.id === id);
  if (zone && map) {
    map.flyTo([zone.lat, zone.lng], 6, { duration: 1.5 });
    showZoneDetail(zone);
  }
};

function showZoneDetail(zone) {
  const card    = document.getElementById('zoneDetailCard');
  const nameEl  = document.getElementById('zoneDetailName');
  const content = document.getElementById('zoneDetailContent');
  if (!card) return;
  card.style.display = 'block';
  nameEl.innerHTML = `<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${zone.color};margin-right:6px;"></span>${zone.name.split('(')[0].trim()}`;
  content.innerHTML = `
    <div class="report-param-item" style="margin-bottom:8px;">
      <div class="report-param-label">Coverage</div>
      <div style="font-size:0.82rem;color:var(--clr-text-muted);">${zone.coverage}</div>
    </div>
    <div class="report-param-item" style="margin-bottom:8px;">
      <div class="report-param-label">pH Range</div>
      <div style="font-size:0.95rem;font-weight:700;color:var(--clr-text);">${zone.ph_range}</div>
    </div>
    <div class="report-param-item" style="margin-bottom:8px;">
      <div class="report-param-label">Texture</div>
      <div style="font-size:0.82rem;color:var(--clr-text-muted);">${zone.texture}</div>
    </div>
    <div class="report-param-item" style="margin-bottom:8px;">
      <div class="report-param-label">General Fertility</div>
      <div style="font-size:0.82rem;color:var(--clr-text-muted);">${zone.general_fertility}</div>
    </div>
    <div class="report-param-item" style="margin-bottom:8px;">
      <div class="report-param-label">Key Crops</div>
      <div style="font-size:0.82rem;color:var(--clr-text-muted);">${zone.key_crops}</div>
    </div>
    <div class="report-param-item" style="margin-bottom:8px;">
      <div class="report-param-label" style="color:#fbbf24;">Major Threats</div>
      <div style="font-size:0.82rem;color:var(--clr-text-muted);">${zone.major_threats}</div>
    </div>
    <div class="rec-tip">
      <i class="fa-solid fa-leaf"></i>
      <span><strong>Conservation:</strong> ${zone.conservation_priority}</span>
    </div>`;
  card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Boot
document.addEventListener('DOMContentLoaded', () => {
  initMap();
  loadZones();
  loadSavedLocations();
});
