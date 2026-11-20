// Email: assembled in the browser so the plain address is not in the HTML.
document.querySelectorAll(".email").forEach((el) => {
  const addr = `${el.dataset.u}@${el.dataset.d}`;
  // shown as "user [at] domain" (下司 2026-11-20); the link still opens the mail app.
  el.innerHTML = `<a href="mailto:${addr}">${el.dataset.u} [at] ${el.dataset.d}</a>`;
});

// Publications filter (publications page only).
(() => {
  const q = document.getElementById("q");
  if (!q) return;
  const items = [...document.querySelectorAll(".pub")];
  const secs = [...document.querySelectorAll(".pubsec")];
  const tabs = [...document.querySelectorAll(".tabs button")];
  const bars = [...document.querySelectorAll(".bar")];
  const first = document.getElementById("f-first");
  const ref = document.getElementById("f-ref");
  const inv = document.getElementById("f-inv");
  const year = document.getElementById("f-year");
  const status = document.getElementById("status");
  let tab = "all";

  // Keep the original title HTML so highlighting can be reset.
  items.forEach((li) => {
    const t = li.querySelector(".title");
    if (t) t.dataset.raw = t.textContent;
  });

  const escRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const escHtml = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function apply() {
    const terms = q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    items.forEach((li) => {
      const d = li.dataset;
      const ok =
        (tab === "all" || d.kind === tab) &&
        (!first.checked || d.first === "1") &&
        (!ref.checked || d.ref === "1") &&
        (!inv.checked || d.inv === "1") &&
        (!year.value || d.year === year.value) &&
        terms.every((t) => d.text.includes(t));
      li.hidden = !ok;
      if (ok) shown++;
      const t = li.querySelector(".title");
      if (t) {
        const raw = escHtml(t.dataset.raw);
        t.innerHTML = terms.length
          ? raw.replace(new RegExp(`(${terms.map(escRe).join("|")})`, "gi"), "<mark>$1</mark>")
          : raw;
      }
    });
    secs.forEach((s) => {
      const vis = s.querySelectorAll(".pub:not([hidden])").length;
      s.hidden = vis === 0;
      s.querySelector(".count").textContent = vis;
    });
    bars.forEach((b) => b.classList.toggle("on", b.dataset.year === year.value));
    const tl = document.getElementById("tl");
    if (tl) { tl.dataset.tab = tab; tl.classList.toggle("picked", !!year.value); }
    status.textContent = `${shown} ${status.dataset.shown}`;
    const params = new URLSearchParams();
    if (q.value) params.set("q", q.value);
    if (tab !== "all") params.set("type", tab);
    if (year.value) params.set("year", year.value);
    try {
      history.replaceState(null, "", params.toString() ? `?${params}` : location.pathname);
    } catch (e) { /* e.g. inside the single-file preview */ }
  }

  tabs.forEach((b) =>
    b.addEventListener("click", () => {
      tab = b.dataset.tab;
      tabs.forEach((x) => x.classList.toggle("on", x === b));
      apply();
    })
  );
  bars.forEach((b) => {
    const pick = () => {
      year.value = year.value === b.dataset.year ? "" : b.dataset.year;
      apply();
    };
    b.addEventListener("click", pick);
    b.addEventListener("keydown", (e) => (e.key === "Enter" || e.key === " ") && (e.preventDefault(), pick()));
  });
  [q, first, ref, inv, year].forEach((el) => el.addEventListener("input", apply));

  // Restore state from the URL so filtered views can be linked.
  const p = new URLSearchParams(location.search);
  if (p.get("q")) q.value = p.get("q");
  if (p.get("year")) year.value = p.get("year");
  const t = p.get("type");
  if (t) tabs.find((b) => b.dataset.tab === t)?.click();
  apply();
})();

// Copy a reference (APA/JPA text or BibTeX). Falls back to selecting the text when the clipboard is blocked.
document.addEventListener("click", async (ev) => {
  const b = ev.target.closest(".cp");
  if (!b) return;
  const text = b.dataset.c;
  const done = () => {
    const old = b.textContent;
    b.textContent = document.body.dataset.copied || "Copied";
    setTimeout(() => (b.textContent = old), 1500);
  };
  try {
    await navigator.clipboard.writeText(text);
    done();
  } catch (e) {
    let box = b.parentElement.querySelector("textarea");
    if (!box) {
      box = document.createElement("textarea");
      box.readOnly = true;
      b.parentElement.appendChild(box);
    }
    box.value = text;
    box.rows = text.split("\n").length + 1;
    box.select();
    try { document.execCommand("copy") && done(); } catch (_) { /* text stays selected */ }
  }
});

// Home banner: a small, drifting network of nodes (a nod to network models of personality).
// Nodes move away from the pointer. Static when the user prefers reduced motion.
(() => {
  const cv = document.getElementById("net");
  if (!cv) return;
  const ctx = cv.getContext("2d");
  const css = getComputedStyle(document.documentElement);
  const c1 = css.getPropertyValue("--accent").trim(), c2 = css.getPropertyValue("--warm").trim();
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let W = 0, H = 0, dpr = 1, nodes = [], mouse = { x: -999, y: -999 };
  function size() {
    dpr = window.devicePixelRatio || 1;
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const n = Math.max(14, Math.round(W / 26));
    nodes = Array.from({ length: n }, (_, i) => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.35, vy: (Math.random() - 0.5) * 0.35,
      r: 2 + Math.random() * 3, warm: i % 5 === 0,
    }));
  }
  function draw() {
    ctx.clearRect(0, 0, W, H);
    for (let i = 0; i < nodes.length; i++) for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], b = nodes[j], d = Math.hypot(a.x - b.x, a.y - b.y);
      if (d < 110) {
        ctx.globalAlpha = (1 - d / 110) * 0.5;
        ctx.strokeStyle = c1; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      }
    }
    ctx.globalAlpha = 0.9;
    nodes.forEach((p) => { ctx.fillStyle = p.warm ? c2 : c1; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 7); ctx.fill(); });
    ctx.globalAlpha = 1;
  }
  function step() {
    nodes.forEach((p) => {
      const dx = p.x - mouse.x, dy = p.y - mouse.y, d = Math.hypot(dx, dy);
      if (d < 80) { p.vx += dx / d * 0.25; p.vy += dy / d * 0.25; }
      p.vx *= 0.985; p.vy *= 0.985;
      if (Math.hypot(p.vx, p.vy) < 0.15) { p.vx += (Math.random() - 0.5) * 0.1; p.vy += (Math.random() - 0.5) * 0.1; }
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      p.x = Math.min(Math.max(p.x, 0), W); p.y = Math.min(Math.max(p.y, 0), H);
    });
    draw();
    requestAnimationFrame(step);
  }
  cv.addEventListener("pointermove", (e) => { const r = cv.getBoundingClientRect(); mouse = { x: e.clientX - r.left, y: e.clientY - r.top }; });
  cv.addEventListener("pointerleave", () => (mouse = { x: -999, y: -999 }));
  addEventListener("resize", size);
  size();
  still ? draw() : step();
})();

