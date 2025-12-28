import { CUS_BASE_URL, getState, getLevels, setMode, setValve } from "./api.js";
import { createLevelChart } from "./chart.js";

const el = (id) => document.getElementById(id);

const statusBadge = el("statusBadge");
const levelValue = el("levelValue");
const valveValue = el("valveValue");
const lastUpdate = el("lastUpdate");
const cusUrlLabel = el("cusUrlLabel");

const btnAuto = el("btnAuto");
const btnManual = el("btnManual");
const btnRefresh = el("btnRefresh");

const valveSlider = el("valveSlider");
const manualValveLabel = el("manualValveLabel");
const btnSendValve = el("btnSendValve");
const manualHint = el("manualHint");

const nInput = el("nInput");

const chart = createLevelChart(el("levelChart"));

cusUrlLabel.textContent = CUS_BASE_URL;

let currentSystemState = "NOT AVAILABLE";

function setBadge(state) {
  statusBadge.textContent = state;
  statusBadge.className = "badge"; // reset
  if (state === "AUTOMATIC") statusBadge.classList.add("badgeAuto");
  else if (state === "MANUAL") statusBadge.classList.add("badgeManual");
  else if (state === "UNCONNECTED") statusBadge.classList.add("badgeUnconnected");
  else statusBadge.classList.add("badgeNA");
}

function setManualControlsEnabled(enabled) {
  valveSlider.disabled = !enabled;
  btnSendValve.disabled = !enabled;
  manualHint.textContent = enabled ? "Manual control enabled." : "Enabled only in MANUAL mode.";
}

function setNotAvailableUI() {
  currentSystemState = "NOT AVAILABLE";
  setBadge("NOT AVAILABLE");
  levelValue.textContent = "—";
  valveValue.textContent = "—";
  lastUpdate.textContent = "—";
  setManualControlsEnabled(false);
  chart.setData([]);
}

async function refreshAll() {
  try {
    const state = await getState();

    currentSystemState = state.system_state ?? "NOT AVAILABLE";
    setBadge(currentSystemState);

    levelValue.textContent = (state.last_level_cm ?? "—");
    valveValue.textContent = (state.valve_percent ?? "—");

    if (state.last_update_ts) {
      lastUpdate.textContent = new Date(state.last_update_ts * 1000).toLocaleString();
    } else {
      lastUpdate.textContent = "—";
    }

    setManualControlsEnabled(currentSystemState === "MANUAL");

    const N = Number(nInput.value || 50);
    const levelsResp = await getLevels(N);
    chart.setData(levelsResp.levels ?? []);
  } catch (err) {
    console.warn(err);
    setNotAvailableUI();
  }
}

btnAuto.addEventListener("click", async () => {
  try {
    await setMode("AUTOMATIC");
    await refreshAll();
  } catch {
    alert("Failed to set AUTOMATIC (CUS not reachable?)");
  }
});

btnManual.addEventListener("click", async () => {
  try {
    await setMode("MANUAL");
    await refreshAll();
  } catch {
    alert("Failed to set MANUAL (CUS not reachable?)");
  }
});

valveSlider.addEventListener("input", () => {
  manualValveLabel.textContent = valveSlider.value;
});

btnSendValve.addEventListener("click", async () => {
  if (currentSystemState !== "MANUAL") return;
  const v = Number(valveSlider.value);

  try {
    await setValve(v);
    await refreshAll();
  } catch {
    alert("Failed to send valve value (CUS not reachable?)");
  }
});

btnRefresh.addEventListener("click", refreshAll);

// Initial + periodic refresh
refreshAll();
setInterval(refreshAll, 1000);
