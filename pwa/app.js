const API_URL = "https://ijsboer-tracker-production.up.railway.app/api/location";
const INTERVAL_MS = 30000;

let actief = false;
let intervalId = null;
let wakeLock = null;

const btn = document.getElementById("toggle-btn");
const statusEl = document.getElementById("status");
const coordsEl = document.getElementById("coords");

function toggle() {
  if (!actief) {
    start();
  } else {
    stop();
  }
}

function start() {
  if (!navigator.geolocation) {
    statusEl.textContent = "GPS wordt niet ondersteund door deze browser.";
    return;
  }

  statusEl.textContent = "GPS ophalen…";

  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      actief = true;
      btn.textContent = "Stop";
      btn.classList.add("actief");
      statusEl.textContent = "Rit actief — laat dit scherm open.";

      await requestWakeLock();
      stuurLocatie(pos);

      intervalId = setInterval(() => {
        navigator.geolocation.getCurrentPosition(stuurLocatie, onGpsError, {
          enableHighAccuracy: true,
          timeout: 10000,
        });
      }, INTERVAL_MS);
    },
    onGpsError,
    { enableHighAccuracy: true, timeout: 15000 }
  );
}

function stop() {
  actief = false;
  clearInterval(intervalId);
  intervalId = null;

  releaseWakeLock();

  btn.textContent = "Start";
  btn.classList.remove("actief");
  coordsEl.textContent = "";
  statusEl.textContent = "Rit beëindigd.";

  fetch(API_URL + "/stop", { method: "POST" }).catch(() => {});
}

function stuurLocatie(pos) {
  const { latitude, longitude } = pos.coords;
  coordsEl.textContent = `${latitude.toFixed(5)}, ${longitude.toFixed(5)}`;

  const url = `${API_URL}?lat=${latitude}&lng=${longitude}`;
  fetch(url, { method: "POST", signal: AbortSignal.timeout(8000) })
    .then(() => {
      statusEl.textContent = "Rit actief — laat dit scherm open.";
    })
    .catch(() => {
      statusEl.textContent = "Signaal even weg — volgende poging over 30s.";
    });
}

function onGpsError(err) {
  statusEl.textContent = "GPS niet beschikbaar: " + err.message;
}

async function requestWakeLock() {
  if ("wakeLock" in navigator) {
    try {
      wakeLock = await navigator.wakeLock.request("screen");
    } catch (_) {
      // Niet beschikbaar of geweigerd — geen actie nodig
    }
  }
}

function releaseWakeLock() {
  if (wakeLock) {
    wakeLock.release();
    wakeLock = null;
  }
}

// Wanneer de ijsboer terugkomt naar Safari: wake lock hervragen + direct locatie sturen
document.addEventListener("visibilitychange", async () => {
  if (!document.hidden && actief) {
    await requestWakeLock();
    navigator.geolocation.getCurrentPosition(stuurLocatie, onGpsError, {
      enableHighAccuracy: true,
      timeout: 10000,
    });
  }
});
