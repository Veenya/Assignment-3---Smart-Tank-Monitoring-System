// Change this if your CUS runs elsewhere (e.g. another PC on LAN)
export const CUS_BASE_URL = "http://localhost:8000";

/**
 * Basic fetch helper:
 * - throws on HTTP errors
 * - returns parsed JSON
 */
async function fetchJson(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`HTTP ${res.status} ${res.statusText} ${text}`);
  }
  return res.json();
}

export function getState() {
  return fetchJson(`${CUS_BASE_URL}/api/state`);
}

export function getLevels(N) {
  return fetchJson(`${CUS_BASE_URL}/api/levels?N=${encodeURIComponent(N)}`);
}

export function setMode(mode) {
  return fetchJson(`${CUS_BASE_URL}/api/mode`, {
    method: "POST",
    body: JSON.stringify({ mode }),
  });
}

export function setValve(valve_percent) {
  return fetchJson(`${CUS_BASE_URL}/api/valve`, {
    method: "POST",
    body: JSON.stringify({ valve_percent }),
  });
}
