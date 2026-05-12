/* ============================================================
   map.js — Leaflet map initialisation + HTMX trigger on click
   ============================================================ */

let map;
let markers = {};

document.addEventListener("DOMContentLoaded", () => {
  initMap();
});

function initMap() {
  // Dark tile layer from CartoDB
  map = L.map("map", {
    center: [20, 0],
    zoom: 2,
    minZoom: 2,
    maxZoom: 10,
    zoomControl: true,
  });

  L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    {
      attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
      subdomains: "abcd",
      maxZoom: 19,
    }
  ).addTo(map);

  // Place markers for each city
  if (window.CITIES) {
    window.CITIES.forEach(addCityMarker);
  }

  // Re-poll: refresh open modal every 30s via HTMX
  setInterval(refreshOpenModal, 30_000);
}

function addCityMarker(city) {
  const icon = L.divIcon({
    className: "custom-marker",
    iconSize: [14, 14],
    iconAnchor: [7, 7],
    popupAnchor: [0, -10],
  });

  const marker = L.marker([city.lat, city.lon], { icon })
    .addTo(map)
    .bindTooltip(`<strong>${city.name}</strong><br/>${city.country}`, {
      permanent: false,
      direction: "top",
      className: "city-tooltip",
    });

  marker.on("click", () => openCityModal(city));
  markers[city.id] = marker;
}

function openCityModal(city) {
  // Highlight sidebar item
  document
    .querySelectorAll(".city-item")
    .forEach((el) => el.classList.remove("active"));
  const sidebarItem = document.getElementById(`sidebar-${city.id}`);
  if (sidebarItem) sidebarItem.classList.add("active");

  // Show spinner inside modal
  const overlay = document.getElementById("modal-overlay");
  const content = document.getElementById("modal-content");
  overlay.classList.remove("hidden");
  content.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:center;padding:4rem;gap:1rem;">
      <div class="spinner"></div>
      <span style="color:var(--text-muted)">Loading ${city.name}...</span>
    </div>`;
  document.body.style.overflow = "hidden";

  // Trigger HTMX fetch
  htmx.ajax("GET", `/city/${city.id}/modal`, {
    target: "#modal-content",
    swap: "innerHTML",
  });
}

function focusCity(cityId, lat, lon) {
  map.setView([lat, lon], 6, { animate: true });
  openCityModal({ id: cityId, lat, lon, name: cityId });
}

function closeModal(event) {
  // Only close if clicking backdrop (not inner modal)
  if (event && event.target !== document.getElementById("modal-overlay")) return;
  _closeModal();
}

function _closeModal() {
  document.getElementById("modal-overlay").classList.add("hidden");
  document.getElementById("modal-content").innerHTML = "";
  document.body.style.overflow = "";
  document.querySelectorAll(".city-item").forEach((el) =>
    el.classList.remove("active")
  );
}

// Allow ESC to close modal
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") _closeModal();
});

// Called from modal HTML close button
window.closeModal = function (event) {
  if (!event) return _closeModal();
  if (event.target === document.getElementById("modal-overlay")) _closeModal();
};

// Re-trigger HTMX on the currently open modal (30s auto-refresh)
let _openCityId = null;
htmx.on("htmx:afterSettle", (e) => {
  const match = e.detail.requestConfig?.path?.match(/\/city\/([^/]+)\/modal/);
  if (match) _openCityId = match[1];
});

function refreshOpenModal() {
  if (!_openCityId) return;
  const overlay = document.getElementById("modal-overlay");
  if (overlay.classList.contains("hidden")) return; // modal is closed
  htmx.ajax("GET", `/city/${_openCityId}/modal`, {
    target: "#modal-content",
    swap: "innerHTML",
  });
}

// Tab active state helper (called from modal HTML)
window.setActiveTab = function (btn) {
  btn.closest(".trend-tabs")
    .querySelectorAll(".trend-tab")
    .forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
};

// Toast helper (can be used from anywhere)
window.showToast = function (msg, duration = 3000) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.remove("hidden");
  setTimeout(() => t.classList.add("hidden"), duration);
};
