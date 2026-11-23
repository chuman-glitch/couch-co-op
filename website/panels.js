/* Couch Co-Op · content windows + booking (used by the collage page)
   Everything you might want to change for Phase 1 lives in CONFIG. */
const CONFIG = {
  email: "hi@novocollective.org",
  calendly: "",            // Jerry's Calendly link, e.g. "https://calendly.com/…". Empty = the "Book a call" button stays hidden.
  blockHours: 2,           // rentals are sold in 2-hour blocks
  blockPrice: 15,          // USD per block, for the whole room
  maxBlocks: 2,            // longest single booking (2 blocks = 4 hours)
  maxGuests: 6,
  daysAhead: 21,           // how far ahead people can book
  // The room is open for free play 10am–10pm every day (0 = Sunday). null = closed that day.
  hours: { 0: [10, 22], 1: [10, 22], 2: [10, 22], 3: [10, 22], 4: [10, 22], 5: [10, 22], 6: [10, 22] },
  // Private bookings. Each entry is the START hour of a booked 2-hour block, by date.
  // A booked block closes open play for that time and can't be booked again.
  // Example: { "2026-12-05": [18, 20] } = booked 6–8pm and 8–10pm on Dec 5.
  // Replace with a real booking backend later.
  booked: {},
};

const PANELS = {
  // order = numbering in the index
  dropin:     { num: "01", label: "Drop in",         note: "Free, 10am – 10pm" },
  book:       { num: "02", label: "Book the room",   note: "$15 / 2 hours" },
  program:    { num: "03", label: "Program",         note: "What's on" },
  vision:     { num: "04", label: "Our vision",      note: "Shoes off" },
  setup:      { num: "05", label: "The setup",       note: "2 consoles · 4–6 players" },
  visit:      { num: "06", label: "Visit us",        note: "POST Houston" },
  publishers: { num: "07", label: "For publishers",  note: "Your game here" },
  sidescreen: { num: "08", label: "Side screen",     note: "More to play" },
  featured:   { num: "10", label: "Featured screen", note: "Now featuring" },
};

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const fmtHour = h => { const hh = h % 24; const s = hh >= 12 ? "pm" : "am"; return `${hh % 12 || 12}${s}`; };
const ymd = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;

/* ---------- overlay windows ---------- */
const overlay = $("#overlay");
const win = $(".window", overlay);
const winBody = $("#winBody");
const winTitle = $("#winTitle");
let lastFocus = null;

function openPanel(id, { fromHash = false } = {}) {
  const tpl = document.getElementById(`panel-${id}`);
  if (!tpl) return;
  if (overlay.hidden) lastFocus = document.activeElement;
  winTitle.textContent = tpl.dataset.title;
  $("#winNum").textContent = PANELS[id] ? PANELS[id].num : "";
  win.classList.toggle("wide", id === "book");
  winBody.replaceChildren(tpl.content.cloneNode(true));
  winBody.scrollTop = 0;
  overlay.hidden = false;
  document.body.classList.add("explored");

  if (!fromHash && location.hash !== `#${id}`) history.replaceState(null, "", `#${id}`);
  const init = INIT[id];
  if (init) init(winBody);
  $$("[data-cfg]", winBody).forEach(el => (el.textContent = CONFIG[el.dataset.cfg]));
  requestAnimationFrame(() => win.focus());
}

function closePanel() {
  overlay.hidden = true;
  history.replaceState(null, "", location.pathname + location.search);
  if (lastFocus && document.contains(lastFocus)) lastFocus.focus();
}

document.addEventListener("click", e => {
  const opener = e.target.closest("[data-open]");
  if (opener) { e.preventDefault(); openPanel(opener.dataset.open); return; }
  if (e.target.closest("[data-close]")) closePanel();
});
document.addEventListener("keydown", e => {
  if (e.key === "Escape" && !overlay.hidden) closePanel();
  if (e.key === "Tab" && !overlay.hidden) trapFocus(e);
});
function trapFocus(e) {
  const f = $$("button, a[href], input, select, textarea, [tabindex]:not([tabindex='-1'])", win).filter(el => !el.disabled && el.offsetParent !== null);
  if (!f.length) return;
  const first = f[0], last = f[f.length - 1];
  if (e.shiftKey && (document.activeElement === first || document.activeElement === win)) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
}
window.addEventListener("hashchange", () => {
  const id = location.hash.slice(1);
  if (PANELS[id] || id === "menu") openPanel(id, { fromHash: true });
});

/* ---------- per-panel setup ---------- */
const INIT = {
  menu(root) {
    const list = $("#menuList", root);
    Object.entries(PANELS).filter(([id]) => id !== "featured").forEach(([id, p]) => {
      const li = document.createElement("li");
      li.innerHTML = `<button data-open="${id}"><span class="num">${p.num}</span><span class="lbl">${p.label}</span><small>${p.note}</small></button>`;
      list.appendChild(li);
    });
  },

  dropin(root) {
    const list = $("#openHoursList", root);
    const today = new Date();
    for (let i = 0; i < 3; i++) {
      const d = new Date(today); d.setDate(today.getDate() + i);
      const h = CONFIG.hours[d.getDay()];
      const booked = (CONFIG.booked[ymd(d)] || []).slice().sort((a, b) => a - b);
      const name = i === 0 ? "Today" : i === 1 ? "Tomorrow" : d.toLocaleDateString("en", { weekday: "long" });
      const row = document.createElement("div");
      row.innerHTML = !h ? `<span>${name}</span><b>Closed</b>`
        : `<span>${name}</span><b>${fmtHour(h[0])} – ${fmtHour(h[1])}${booked.length ? `<em class="priv">Private: ${booked.map(s => `${fmtHour(s)}–${fmtHour(s + CONFIG.blockHours)}`).join(", ")}</em>` : ""}</b>`;
      list.appendChild(row);
    }
  },

  publishers(root) {
    const subject = encodeURIComponent("Couch Co-Op · publisher placement");
    const body = encodeURIComponent("Hi Couch Co-Op,\n\nWe'd like to place a game in the pilot room.\n\nStudio / publisher:\nGame:\nPackage (Standard $3,000 / Premium $7,000):\nPreferred dates:\nPlatform / console:\n\nThanks!");
    $("#pubMail", root).href = `mailto:${CONFIG.email}?subject=${subject}&body=${body}`;
    const cal = $("#calLink", root);
    if (cal && CONFIG.calendly) { cal.href = CONFIG.calendly; cal.hidden = false; }
  },

  book(root) {
    const state = { date: null, start: null, end: null };
    const daysEl = $("#days", root), slotsEl = $("#slots", root), summary = $("#summary", root);
    const guests = $("#guests", root), form = $("#bookingForm", root), msg = $("#formMsg", root);

    for (let n = 2; n <= CONFIG.maxGuests; n++) guests.add(new Option(`${n} people`, n));
    guests.value = "4";

    const today = new Date(); today.setHours(0, 0, 0, 0);
    const dates = [];
    for (let i = 0; i < CONFIG.daysAhead; i++) {
      const d = new Date(today); d.setDate(today.getDate() + i);
      if (CONFIG.hours[d.getDay()]) dates.push(d);
    }

    const B = CONFIG.blockHours;
    const blockState = (d, h) => {
      if ((CONFIG.booked[ymd(d)] || []).includes(h)) return "taken";
      const now = new Date();
      if (ymd(d) === ymd(now) && h <= now.getHours()) return "past";
      return "free";
    };

    function renderDays() {
      daysEl.replaceChildren(...dates.map(d => {
        const b = document.createElement("button");
        b.type = "button"; b.className = "day"; b.setAttribute("role", "radio");
        b.setAttribute("aria-checked", String(state.date && ymd(state.date) === ymd(d)));
        b.innerHTML = `<small>${DAYS[d.getDay()]}</small><b>${d.getDate()}</b><small>${d.toLocaleString("en", { month: "short" })}</small>`;
        b.onclick = () => { state.date = d; state.start = state.end = null; renderDays(); renderSlots(); renderSummary(); };
        return b;
      }));
    }

    function renderSlots() {
      if (!state.date) { slotsEl.innerHTML = `<p class="small">Pick a day first.</p>`; return; }
      const [o, c] = CONFIG.hours[state.date.getDay()];
      const btns = [];
      for (let h = o; h + B <= c; h += B) {
        const t = blockState(state.date, h);
        const b = document.createElement("button");
        b.type = "button"; b.className = `hslot ${t === "free" ? "" : t}`;
        b.innerHTML = `${fmtHour(h)}–${fmtHour(h + B)}<small>${t === "taken" ? "Booked" : t === "past" ? "Passed" : `$${CONFIG.blockPrice}`}</small>`;
        b.disabled = t !== "free";
        b.setAttribute("aria-label", `${fmtHour(h)} to ${fmtHour(h + B)}, ${t === "free" ? "available" : t === "taken" ? "already booked" : "passed"}`);
        if (state.start !== null && h >= state.start && h < state.end) { b.classList.add("sel"); b.setAttribute("aria-pressed", "true"); }
        b.onclick = () => pick(h);
        btns.push(b);
      }
      slotsEl.replaceChildren(...btns);
    }

    function pick(h) {
      if (state.start === h && state.end === h + B) { state.start = state.end = null; }          // tap again to clear
      else if (state.start !== null && state.end === h && (h + B - state.start) / B <= CONFIG.maxBlocks) { state.end = h + B; } // next block extends
      else { state.start = h; state.end = h + B; }
      renderSlots(); renderSummary();
    }

    const blocksOf = () => (state.end - state.start) / B;
    function renderSummary() {
      if (!state.date || state.start === null) { summary.textContent = "Pick a time block to see your total."; return; }
      const when = state.date.toLocaleDateString("en", { weekday: "long", month: "long", day: "numeric" });
      summary.innerHTML = `${when} · ${fmtHour(state.start)}–${fmtHour(state.end)} · ${blocksOf() * B} hours<br>Total <b>$${blocksOf() * CONFIG.blockPrice}</b> for the whole room (up to ${CONFIG.maxGuests} people).`;
    }

    form.addEventListener("submit", e => {
      e.preventDefault();
      msg.className = "formmsg err";
      if (!state.date || state.start === null) { msg.textContent = "Pick a day and a time block."; return; }
      if (!form.name.value.trim()) { msg.textContent = "Add your name."; form.name.focus(); return; }
      if (!form.email.checkValidity() || !form.email.value) { msg.textContent = "Add a valid email so we can confirm."; form.email.focus(); return; }
      const hrs = state.end - state.start;
      const when = state.date.toLocaleDateString("en", { weekday: "long", month: "long", day: "numeric", year: "numeric" });
      const subject = encodeURIComponent(`Room booking request · ${when}`);
      const body = encodeURIComponent(
        `Hi Couch Co-Op,\n\nI'd like to book the room.\n\nDate: ${when}\nTime: ${fmtHour(state.start)} – ${fmtHour(state.end)} (${hrs}h)\nGroup size: ${guests.value}\nName: ${form.name.value.trim()}\nEmail: ${form.email.value.trim()}\n\nTotal: $${blocksOf() * CONFIG.blockPrice}\n\nThanks!`
      );
      window.location.href = `mailto:${CONFIG.email}?subject=${subject}&body=${body}`;
      msg.className = "formmsg ok";
      msg.textContent = "Your email app should open with the request filled in. Send it and we'll confirm your slot by email.";
    });

    // preselect the first day
    state.date = dates.find(d => {
      const [o, c] = CONFIG.hours[d.getDay()];
      for (let h = o; h + B <= c; h += B) if (blockState(d, h) === "free") return true;
      return false;
    }) || dates[0] || null;
    renderDays(); renderSlots(); renderSummary();
  },
};

/* deep links: /#book, /#publishers … */
if (location.hash) {
  const id = location.hash.slice(1);
  if (PANELS[id] || id === "menu") openPanel(id, { fromHash: true });
}
