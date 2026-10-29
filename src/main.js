import "@fontsource-variable/geist";
import "@fontsource-variable/geist-mono";
import "@fontsource-variable/newsreader/opsz.css";
import "@fontsource-variable/newsreader/opsz-italic.css";
import "./style.css";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import {
  DEFAULTS, BASE_PAYOFFS, SCENARIO_PRESETS, CELL_LOGIC, CELL_SUBTITLES, SUSC, EXPO, MODR,
  validationErrors, logistic, analyse, deviations, tippingM, makeGraph, runNetwork,
} from "./model.js";

gsap.registerPlugin(ScrollTrigger);

const $ = (s) => document.querySelector(s);
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

// Canvas colours from active theme CSS variables
let C = {};
const readColors = () => {
  const s = getComputedStyle(document.documentElement), v = (k) => s.getPropertyValue(k).trim();
  C = {
    accent: v("--accent") || "#00F0FF",
    bg2: v("--bg-2") || "#0F172A",
    cool: v("--cool") || "#38BDF8",
    fg: v("--fg-rgb") || "255, 255, 255",
    acc: v("--accent-rgb") || "0, 240, 255",
    coral: v("--coral") || "#F43F5E",
    emerald: v("--emerald") || "#10B981",
  };
};

const easeOutBack = (x) => 1 + 2.7 * (x - 1) ** 3 + 1.7 * (x - 1) ** 2;
const int = (v) => Math.round(v).toLocaleString("en-IN");
const num = (v) => (Number.isInteger(v) ? String(v) : v.toFixed(2)).replace("-", "−");
const compact = (v) => (v >= 1000 ? `${+(v / 1000).toFixed(1)}k` : String(v));
const WORD = { S: "spread", N: "stay quiet", W: "weak moderation", M: "strong moderation" };
const words = (k) => `${WORD[k[0]]} / ${WORD[k[1]]}`;

const S = {
  p: { ...DEFAULTS },
  model: "logistic",
  hoverT: null,
  P: structuredClone(BASE_PAYOFFS),
  profile: "NM",
  highlightMode: "All Elements",
};

const run = (p) => logistic(p);

/* ---------------------------------------------------------------- Top Hero KPI Cards */
function renderHeroKPIs() {
  const p = S.p, N = p.population;
  const mine = run(p);
  const base = run({ ...p, moderation: 0 });
  const final = mine.at(-1);
  const peak = Math.max(...mine);
  const baseFinal = base.at(-1);
  const basePeak = Math.max(...base);
  const reductionPct = baseFinal > 0 ? Math.max(0, ((baseFinal - final) / baseFinal) * 100) : 0;
  const savedUsers = Math.max(0, baseFinal - final);
  const finalPct = N > 0 ? (final / N) * 100 : 0;

  const an = analyse(S.P);
  let eqLabel = "No Pure Eq";
  let eqChip = "Cycling Dynamics";
  if (an.nash.length > 0) {
    eqLabel = an.nash.map((k) => `Profile (${k[0]}, ${k[1]})`).join(" & ");
    const k0 = an.nash[0];
    eqChip = `(${S.P[k0][0]}, ${S.P[k0][1]}) Payoffs`;
  } else if (an.mixed.exists) {
    eqLabel = "Mixed Strategy Eq";
    eqChip = `p*=${an.mixed.p.toFixed(2)}, q*=${an.mixed.q.toFixed(2)}`;
  }

  const elFinal = $("#kpi-final"), elFinalSub = $("#kpi-final-sub");
  if (elFinal) elFinal.textContent = int(final);
  if (elFinalSub) elFinalSub.textContent = `${finalPct.toFixed(1)}% of population`;

  const elPeak = $("#kpi-peak"), elPeakSub = $("#kpi-peak-sub");
  if (elPeak) elPeak.textContent = int(peak);
  if (elPeakSub) elPeakSub.textContent = `Baseline was ${int(basePeak)}`;

  const elRed = $("#kpi-reduction"), elRedSub = $("#kpi-reduction-sub");
  if (elRed) elRed.textContent = `${reductionPct.toFixed(1)}%`;
  if (elRedSub) elRedSub.textContent = `Saved ${int(savedUsers)} users`;

  const elEq = $("#kpi-eq"), elEqSub = $("#kpi-eq-sub");
  if (elEq) elEq.textContent = eqLabel;
  if (elEqSub) elEqSub.textContent = eqChip;
}

/* ---------------------------------------------------------------- SVG Line Chart */
function lineChart(svg, c) {
  const vb = svg.viewBox.baseVal, W = vb.width, H = vb.height;
  const m = { l: 60, r: c.right ?? 24, t: 24, b: 36 };
  const sx = (v) => m.l + ((v - c.x0) / (c.x1 - c.x0)) * (W - m.l - m.r);
  const sy = (v) => H - m.b - ((v - c.y0) / (c.y1 - c.y0)) * (H - m.t - m.b);
  let s = "";

  // Grid lines & Y tick labels
  for (const v of c.yTicks) {
    s += `<line class="grid" x1="${m.l}" x2="${W - m.r}" y1="${sy(v)}" y2="${sy(v)}"/>
          <text x="${m.l - 10}" y="${sy(v) + 4}" text-anchor="end">${c.yFmt(v)}</text>`;
  }

  // X ticks
  for (const v of c.xTicks) {
    s += `<text x="${sx(v)}" y="${H - 12}" text-anchor="middle">${c.xFmt?.(v) ?? v}</text>`;
  }

  // Shaded area if provided
  if (c.shadedArea) {
    s += `<path class="area-saved" d="${c.shadedArea.pts.map(([x, y], i) => `${i ? "L" : "M"}${sx(x).toFixed(1)} ${sy(y).toFixed(1)}`).join(" ")} Z"/>`;
  }

  // Ceiling reference line (Population N)
  if (c.ceiling != null) {
    const cy = sy(c.ceiling);
    s += `<line class="line-ceiling" x1="${m.l}" x2="${W - m.r}" y1="${cy}" y2="${cy}"/>
          <text x="${W - m.r - 8}" y="${cy - 6}" text-anchor="end" fill="#94A3B8" font-size="10">Total Network N = ${int(c.ceiling)}</text>`;
  }

  // Axes
  s += `<line class="ax" x1="${m.l}" x2="${W - m.r}" y1="${sy(c.y0)}" y2="${sy(c.y0)}"/>`;
  if (c.y0 < 0) s += `<line class="ax" x1="${m.l}" x2="${W - m.r}" y1="${sy(0)}" y2="${sy(0)}"/>`;

  // Vertical guidelines (hover or critical threshold)
  for (const v of c.vlines ?? []) {
    s += `<line class="vl" x1="${sx(v.x)}" x2="${sx(v.x)}" y1="${m.t}" y2="${sy(c.y0)}"/>`;
    if (v.label) s += `<text class="vl-t" x="${sx(v.x) + 6}" y="${m.t + 12}">${v.label}</text>`;
  }

  // Series curves
  const ends = [];
  for (const l of c.series) {
    const d = l.pts.map(([x, y], i) => `${i ? "L" : "M"}${sx(x).toFixed(1)} ${sy(y).toFixed(1)}`).join("");
    s += `<path class="line ${l.cls}" d="${d}"/>`;
    if (l.label) ends.push({ y: sy(l.pts.at(-1)[1]), label: l.label, cls: l.lcls ?? "" });

    // Render data point dots along active line
    if (l.showMarkers) {
      for (const [x, y] of l.pts) {
        s += `<circle class="pt" cx="${sx(x)}" cy="${sy(y)}" r="3"/>`;
      }
    }
  }

  ends.sort((a, b) => a.y - b.y);
  ends.forEach((e, i) => { if (i && e.y - ends[i - 1].y < 14) e.y = ends[i - 1].y + 14; });
  for (const e of ends) s += `<text class="end ${e.cls}" x="${W - m.r + 8}" y="${e.y + 4}">${e.label}</text>`;

  // Annotations (Inflection & Peak)
  for (const a of c.annotations ?? []) {
    const ax = sx(a.x), ay = sy(a.y);
    s += `<g class="annotation">
      <circle cx="${ax}" cy="${ay}" r="5" fill="${a.color}" stroke="#0A0F1E" stroke-width="2"/>
      <rect x="${ax - 50}" y="${ay + (a.dy || -26)}" width="100" height="20" rx="4" fill="#0F172A" stroke="${a.color}" stroke-width="1" opacity="0.9"/>
      <text x="${ax}" y="${ay + (a.dy || -26) + 14}" text-anchor="middle" fill="${a.color}" font-weight="700" font-size="10">${a.text}</text>
    </g>`;
  }

  // Standalone marker dots
  for (const d of c.dots ?? []) s += `<circle class="pt" cx="${sx(d.x)}" cy="${sy(d.y)}" r="6"/>`;

  svg.innerHTML = s;
  return {
    inv: (clientX) => {
      const r = svg.getBoundingClientRect();
      return c.x0 + (((clientX - r.left) * W) / r.width - m.l) / (W - m.l - m.r) * (c.x1 - c.x0);
    },
  };
}

/* ---------------------------------------------------------------- Hero Network Canvas */
function drawNet(canvas, g, state, r0 = 3, fx = {}) {
  const dpr = devicePixelRatio || 1, w = canvas.clientWidth, h = canvas.clientHeight;
  if (!w || !h) return;
  if (canvas.width !== Math.round(w * dpr)) {
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
  }
  const { prev = null, p = 1, t = 0 } = fx, ctx = canvas.getContext("2d"), pad = 24;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);
  const P = g.pos.map(([x, y]) => [pad + x * (w - 2 * pad), pad + y * (h - 2 * pad)]);
  const fresh = (i) => prev && state[i] === EXPO && prev[i] === SUSC;
  const calmed = (i) => prev && state[i] === MODR && prev[i] === EXPO;
  const circle = (x, y, r) => { ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832); };

  // Background network graph edges
  ctx.strokeStyle = "rgba(255, 255, 255, 0.10)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  for (const [i, j] of g.edges) { ctx.moveTo(...P[i]); ctx.lineTo(...P[j]); }
  ctx.stroke();

  // Active transmission pulses
  ctx.strokeStyle = C.coral || "#F43F5E";
  ctx.lineWidth = 1.8;
  ctx.lineCap = "round";
  ctx.beginPath();
  const reach = Math.min(1, p * 2.8);
  for (const [i, j] of g.edges) {
    const a = fresh(j) && prev[i] === EXPO ? i : fresh(i) && prev[j] === EXPO ? j : -1;
    if (a < 0) continue;
    const b = a === i ? j : i;
    ctx.moveTo(...P[a]);
    ctx.lineTo(P[a][0] + (P[b][0] - P[a][0]) * reach, P[a][1] + (P[b][1] - P[a][1]) * reach);
  }
  ctx.stroke();

  // Nodes
  for (let i = 0; i < g.n; i++) {
    const r = r0 + Math.sqrt(g.deg[i]) * r0 * 0.5, [x, y] = P[i], q = Math.max(0, (p - 0.3) / 0.7);
    if (state[i] === SUSC || (fresh(i) && p < 0.3)) {
      circle(x, y, r);
      ctx.fillStyle = "#1E293B";
      ctx.fill();
      ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
      ctx.lineWidth = 1.2;
      ctx.stroke();
    } else if (state[i] === EXPO) {
      const born = fresh(i), k = born ? easeOutBack(q) : 1 + 0.08 * Math.sin(t / 380 + i);
      if (born && q < 1) {
        circle(x, y, r * (1 + q * 3.4));
        ctx.strokeStyle = `rgba(${C.acc}, ${0.75 * (1 - q)})`;
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }
      ctx.shadowColor = C.coral || "#F43F5E";
      ctx.shadowBlur = 12;
      circle(x, y, r * k);
      ctx.fillStyle = C.coral || "#F43F5E";
      ctx.fill();
      ctx.shadowBlur = 0;
    } else {
      const close = calmed(i) ? (1 - p) * 10 : 0;
      circle(x, y, r);
      ctx.fillStyle = C.accent || "#00F0FF";
      ctx.fill();
      circle(x, y, r + 3 + close);
      ctx.strokeStyle = C.accent || "#00F0FF";
      ctx.globalAlpha = 0.9 - close * 0.05;
      ctx.lineWidth = 1.4;
      ctx.stroke();
      ctx.globalAlpha = 1;
    }
  }
}

function netView(canvas, frame, r0) {
  let last = -1, t0 = 0, fwd = false, raf = 0;
  const paint = (now) => {
    const f = frame();
    if (f.step !== last) { fwd = last >= 0 && f.step > last; last = f.step; t0 = now; }
    const live = fwd && !reduceMotion;
    drawNet(canvas, f.g, f.state, r0, { prev: live ? f.prev : null, p: live ? Math.min(1, (now - t0) / 900) : 1, t: now });
  };
  addEventListener("themechange", () => paint(performance.now()));
  if (reduceMotion) {
    new ResizeObserver(() => paint(performance.now())).observe(canvas);
    return { kick: () => paint(performance.now()) };
  }
  const runLoop = (now) => { paint(now); raf = requestAnimationFrame(runLoop); };
  new IntersectionObserver(([e]) => {
    cancelAnimationFrame(raf);
    if (e.isIntersecting) raf = requestAnimationFrame(runLoop);
  }).observe(canvas);
  return { kick() {} };
}

/* ---------------------------------------------------------------- Game Taxonomy */
function gameKind(an) {
  const P = an.P;
  if (an.sharerDom === "S" && an.platformDom === "W" && P.NM[0] > P.SW[0] && P.NM[1] > P.SW[1]) return "Prisoner's Dilemma";
  if (an.platformDom === "M" && an.brS.M.length === 1 && an.brS.M[0] === "N") return "Deterrence Game";
  if (an.nash.length >= 2) return "Coordination Game";
  if (!an.nash.length) return "Inspection Game";
  return "Stable Equilibrium Game";
}

const setOf = (a) => `{${a.join(", ")}}`;
const cmp = (a, b) => (a > b ? ">" : a < b ? "<" : "=");
const pair = (k, P) => `(${num(P[k][0])}, ${num(P[k][1])})`;

/* ---------------------------------------------------------------- 01: Payoff Matrix */
function renderMatrix(box, explainEl, P, { profile, onPick } = {}) {
  const an = analyse(P);
  const mode = S.highlightMode;

  const taxonomy = gameKind(an);
  const taxBadge = $("#game-taxonomy-badge");
  if (taxBadge) taxBadge.textContent = `🛡️ ${taxonomy}`;

  const domSharer = an.sharerDom;
  const domPlatform = an.platformDom;

  const badgeW = domPlatform === "W" ? " ⭐ STRICTLY DOMINANT" : domPlatform === "M" ? " (Strictly Dominated)" : "";
  const badgeM = domPlatform === "M" ? " ⭐ STRICTLY DOMINANT" : domPlatform === "W" ? " (Strictly Dominated)" : "";

  let html = "";

  // Row 0: Top platform headers
  html += `<div style="grid-column: 1;"></div>`;
  html += `
    <div class="matrix-col-header ${domPlatform === 'W' ? 'is-dominant' : ''}">
      <div class="col-header-title">Platform: Weak Moderation (W)</div>
      <div class="col-header-sub">Low Operating Cost / Slack Filters <span style="color: var(--amber); font-weight:700;">${badgeW}</span></div>
    </div>
    <div class="matrix-col-header ${domPlatform === 'M' ? 'is-dominant' : ''}">
      <div class="col-header-title col-header-title--m">Platform: Strong Moderation (M) <span style="color: var(--emerald); font-weight:700;">${badgeM}</span></div>
      <div class="col-header-sub" style="color: var(--emerald); font-weight:600;">Active Enforcement (Sanctions &amp; Downranking)</div>
    </div>
  `;

  // Rows 1 & 2: Sharer S & N
  const rows = [
    { key: "S", title: "Sharer: Spread (S)", color: "var(--coral)", desc: "Viral Misinformation Seeding" },
    { key: "N", title: "Sharer: Do Not Spread (N)", color: "var(--emerald)", desc: "Organic Honest Sharing" },
  ];

  rows.forEach(({ key: s, title, color, desc }) => {
    html += `
      <div class="matrix-row-header">
        <div class="row-header-title" style="color: ${color};">${title}</div>
        <div class="row-header-sub">${desc}</div>
      </div>
    `;

    for (const p of ["W", "M"]) {
      const k = s + p;
      const [us, up] = P[k];
      const eq = an.nash.includes(k);
      const b1 = an.brS[p].includes(s);
      const b2 = an.brP[s].includes(p);
      const surplus = us + up;

      const showNash = eq && (mode === "All Elements" || mode === "Nash Equilibrium Only");
      const showSBr = b1 && (mode === "All Elements" || mode === "Best Responses Only");
      const showPBr = b2 && (mode === "All Elements" || mode === "Best Responses Only");
      const showDom = mode === "Strict Dominance Only" && ((s === domSharer) || (p === domPlatform));

      const glowClass = showNash ? "nash-cell-glow" : "";
      const selectedClass = k === profile ? "is-selected" : "";

      const badges = [];
      if (showNash) badges.push('<span class="badge-nash">🏆 NASH EQUILIBRIUM</span>');
      if (showSBr) badges.push('<span class="badge-sharer-br">🎯 Sharer Best Response</span>');
      if (showPBr) badges.push('<span class="badge-platform-br">🛡️ Platform Best Response</span>');
      if (showDom) badges.push('<span class="kpi-chip chip-amber">Dominant Strategy</span>');

      const badgeBlock = badges.length ? badges.join("") : '<span style="font-size:0.75rem;color:var(--text-muted);">No Strategic Extremum</span>';
      const cellSub = CELL_SUBTITLES[k] || "Strategy Profile";
      const logicText = CELL_LOGIC[k] || "";

      html += `
        <div class="matrix-cell ${glowClass} ${selectedClass}" data-k="${k}">
          <div>
            <div class="cell-top-bar">
              <span class="cell-profile-label">Profile (${s}, ${p}) — ${cellSub}</span>
              <span class="kpi-chip chip-slate">Surplus: <b>${surplus >= 0 ? "+" : ""}${surplus}</b></span>
            </div>
            <div class="cell-tuple-row">
              (${num(us)}, ${num(up)})
              <span class="cell-tuple-sub">(Sharer, Platform)</span>
            </div>
            <div class="cell-badges-row">${badgeBlock}</div>
          </div>
          <div class="cell-logic-desc">${logicText}</div>
        </div>
      `;
    }
  });

  box.innerHTML = html;

  const explain = (k) => {
    const moves = deviations(P, k).filter((d) => d.gain > 1e-9);
    explainEl.innerHTML = `<strong>Profile (${k[0]}, ${k[1]}): ${words(k)}.</strong> ` + (moves.length
      ? moves.map((d) => `The ${d.who.toLowerCase()} has an incentive to unilaterally switch to ${WORD[d.to]} for a +${num(d.gain)} gain.`).join(" ")
      : "Neither player has an incentive to deviate unilaterally. Each strategy is a mutual best response, confirming this profile as a pure-strategy Nash equilibrium.");
    box.querySelectorAll(".matrix-cell").forEach((c) => c.classList.toggle("is-selected", c.dataset.k === k));
  };

  box.querySelectorAll(".matrix-cell").forEach((c) => {
    c.addEventListener("click", () => { explain(c.dataset.k); onPick?.(c.dataset.k); });
    c.addEventListener("mouseenter", () => explain(c.dataset.k));
  });

  explain(profile ?? (an.nash[0] ?? "NM"));
  return an;
}

function renderProof(an, P) {
  const br1 = ["W", "M"].map((p) => `u₁(S,${p}) = ${num(P["S" + p][0])} ${cmp(P["S" + p][0], P["N" + p][0])} u₁(N,${p}) = ${num(P["N" + p][0])}  ⇒  BR₁(${p}) = <b>${setOf(an.brS[p])}</b>`);
  const br2 = ["S", "N"].map((s) => `u₂(${s},W) = ${num(P[s + "W"][1])} ${cmp(P[s + "W"][1], P[s + "M"][1])} u₂(${s},M) = ${num(P[s + "M"][1])}  ⇒  BR₂(${s}) = <b>${setOf(an.brP[s])}</b>`);
  const domLine = (name, d, a, b) => `${name}: ${a} ; ${b}  ⇒  ` + (d ? `<b>${WORD[d]} is strictly dominant</b>` : "<b>no strictly dominant strategy</b>");
  const checks = ["SW", "SM", "NW", "NM"].map((k) => {
    const [s, p] = k, ok1 = an.brS[p].includes(s), ok2 = an.brP[s].includes(p);
    return `(${s},${p}): ${s} ∈ BR₁(${p}) ${ok1 ? "✓" : "✗"}   ${p} ∈ BR₂(${s}) ${ok2 ? "✓" : "✗"}  ⇒  ${ok1 && ok2 ? `<b>Nash equilibrium ${pair(k, P)}</b>` : "<em>not an equilibrium</em>"}`;
  });
  const m = an.mixed, nashPareto = an.nash.length && an.nash.every((k) => an.pareto.includes(k));
  const items = [
    ["Best Responses", "For each choice of the opponent, identify the reply that maximizes individual utility: BR(s₋ᵢ) = argmaxₛ uᵢ(s, s₋ᵢ).", [...br1, ...br2]],
    ["Dominant Strategies", "A strategy is strictly dominant if it yields strictly higher payoffs than alternatives regardless of opponent action.",
      [domLine("Sharer", an.sharerDom, `BR₁(W) = ${setOf(an.brS.W)}`, `BR₁(M) = ${setOf(an.brS.M)}`), domLine("Platform", an.platformDom, `BR₂(S) = ${setOf(an.brP.S)}`, `BR₂(N) = ${setOf(an.brP.N)}`)]],
    ["Nash Equilibrium", "A profile (s*, p*) is in equilibrium when each player plays a mutual best response, eliminating unilateral deviation incentives.",
      [...checks, an.nash.length ? `Result: <b>${an.nash.map((k) => `Profile (${k[0]}, ${k[1]})`).join(" and ")}</b> pure Nash equilibrium.` : "Result: <b>No pure-strategy equilibrium</b>."]],
    ["Pareto Efficiency & Mixing", "An outcome is Pareto efficient if no alternative improves one party without harming another. Mixed equilibrium derives indifference probabilities.",
      [`Pareto efficient: <b>${an.pareto.map((k) => `(${k[0]},${k[1]})`).join(", ")}</b>`,
        an.nash.length ? `Equilibrium is ${nashPareto ? "<b>Pareto efficient</b>" : "<b>Pareto suboptimal</b>"}` : "",
        `Indifference gives p* = P(S) = <b>${m.p == null ? "undefined" : m.p.toFixed(2)}</b>, q* = P(W) = <b>${m.q == null ? "undefined" : m.q.toFixed(2)}</b>  ⇒  ` + (m.exists ? "<b>Interior mixed equilibrium exists</b>" : "<b>Outside (0, 1): No interior mixed equilibrium</b>")].filter(Boolean)],
  ];
  $("#proof").innerHTML = items.map(([h, d, lines]) => `<li><div><h4>${h}</h4><p>${d}</p></div><div class="eqs">${lines.join("<br>")}</div></li>`).join("");
}

function renderConcepts(an, P) {
  const CONCEPTS = [
    ["Normal-form game", "Γ = ⟨N, (Sᵢ), (uᵢ)⟩", "A simultaneous 2-player strategic matrix mapping player decisions to utility payoffs.", () => "2 strategic players (Content Sharer, Platform) with 2 actions each."],
    ["Payoff (utility)", "uᵢ(s₁, s₂)", "Cardinal or ordinal scores ranking strategic outcomes for each player.", () => `Unchecked viral sharing pays Sharer ${P.SW[0]} while damaging Platform by ${P.SW[1]}.`],
    ["Best response", "BRᵢ(s₋ᵢ) = argmax uᵢ(s, s₋ᵢ)", "Optimal decision against any fixed choice of the counterparty.", () => `BR₁(W) = ${setOf(an.brS.W)}, BR₁(M) = ${setOf(an.brS.M)}; BR₂(S) = ${setOf(an.brP.S)}, BR₂(N) = ${setOf(an.brP.N)}.`],
    ["Dominant strategy", "uᵢ(s, s₋ᵢ) > uᵢ(s′, s₋ᵢ) for all s₋ᵢ", "A strategy strictly superior across all counterparty responses.", () => [an.sharerDom && `Sharer: ${WORD[an.sharerDom]}`, an.platformDom && `Platform: ${WORD[an.platformDom]}`].filter(Boolean).join("; ") || "Neither player has a dominant strategy."],
    ["Nash equilibrium", "uᵢ(s*ᵢ, s*₋ᵢ) ≥ uᵢ(sᵢ, s*₋ᵢ) for all sᵢ", "Stable profile where no player has unilateral incentives to deviate.", () => an.nash.length ? `${an.nash.map((k) => `Profile (${k[0]}, ${k[1]}) with payoffs ${pair(k, P)}`).join("; ")}.` : "No pure-strategy equilibrium."],
    ["Pareto efficiency", "no s′ with uᵢ(s′) ≥ uᵢ(s), one strict", "System-level efficiency where neither party can gain without hurting the other.", () => `Efficient profiles: ${an.pareto.map((k) => `(${k[0]},${k[1]})`).join(", ")}.`],
    ["Logistic Contagion", "Iₜ₊₁ = Iₜ + β(1 − m) Iₜ (1 − Iₜ/N)", "Epidemiological diffusion damped by platform moderation parameter m.", () => `Active β = ${S.p.beta}, m = ${S.p.moderation}: Net rate ${(S.p.beta * (1 - S.p.moderation)).toFixed(2)}.`],
    ["Tipping Point", "m* = r / (r + c)", "Moderation threshold at which viral sharing ceases to yield positive expected utility.", () => `Critical tipping threshold m* = ${tippingM(S.p.beta).toFixed(2)} at β = ${S.p.beta}.`],
  ];
  $("#concepts-list").innerHTML = CONCEPTS.map(([n, f, d, here]) =>
    `<div class="concept" role="row"><div role="cell"><h3>${n}</h3><p class="formula">${f}</p></div><div role="cell"><p>${d}</p></div><div class="here" role="cell"><small>Current State</small>${here()}</div></div>`).join("");
}

function renderGame() {
  const an = renderMatrix($("#matrix-wrapper"), $("#matrix-explain"), S.P, {
    profile: S.profile,
    onPick: (k) => { S.profile = k; },
  });
  const P = S.P, eq = an.nash;
  $("#payoff-now").textContent = eq.length ? `Nash: ${eq.map((k) => `(${k[0]}, ${k[1]})`).join(", ")}` : "No pure Nash equilibrium";
  renderProof(an, P);
  renderConcepts(an, P);
  renderHeroKPIs();
}

function initPayoffFields() {
  const keys = [
    ["SW", "Profile (S, W) [Viral]"],
    ["SM", "Profile (S, M) [Deterred]"],
    ["NW", "Profile (N, W) [Laissez-Faire]"],
    ["NM", "Profile (N, M) [Compliant]"],
  ];
  $("#payoff-fields").innerHTML = keys.map(([k, label]) => `
    <div class="payoff-card-editor">
      <h4>${label}</h4>
      <label class="num">
        <span>Sharer Payoff:</span>
        <input type="number" step="0.5" data-k="${k}" data-i="0" value="${S.P[k][0]}" />
      </label>
      <label class="num">
        <span>Platform Payoff:</span>
        <input type="number" step="0.5" data-k="${k}" data-i="1" value="${S.P[k][1]}" />
      </label>
    </div>
  `).join("");

  const fields = [...document.querySelectorAll("#payoff-fields input")];
  const sync = () => fields.forEach((f) => { f.value = S.P[f.dataset.k][f.dataset.i]; });

  fields.forEach((f) => f.addEventListener("input", () => {
    const bad = fields.filter((x) => x.value.trim() === "" || !Number.isFinite(+x.value));
    $("#payoff-error").textContent = bad.length ? "All payoff values must be valid numbers." : "";
    if (bad.length) return;
    fields.forEach((x) => (S.P[x.dataset.k][x.dataset.i] = +x.value));
    renderGame();
  }));

  $("#payoff-reset").addEventListener("click", () => {
    S.P = structuredClone(BASE_PAYOFFS);
    sync();
    $("#payoff-error").textContent = "";
    renderGame();
  });
}

function initPresetsAndFilters() {
  const sel = $("#scenario-selector");
  if (sel) {
    sel.addEventListener("change", (e) => {
      const chosen = e.target.value;
      const preset = SCENARIO_PRESETS[chosen];
      if (preset) {
        S.p.population = preset.pop;
        S.p.initialExposed = preset.seed;
        S.p.beta = preset.beta;
        S.p.moderation = preset.mod;
        S.p.steps = preset.steps;
        S.P = structuredClone(preset.payoffs);

        // Sync slider inputs
        for (const k of ["population", "initialExposed", "beta", "moderation", "steps"]) {
          const el = $(`#${k}`);
          if (el) el.value = S.p[k];
        }

        // Sync payoff number inputs
        document.querySelectorAll("#payoff-fields input").forEach((inp) => {
          inp.value = S.P[inp.dataset.k][inp.dataset.i];
        });

        renderGame();
        renderSpread();
        renderHeroKPIs();
      }
    });
  }

  // Highlight Filter Mode
  const modeGroup = $("#highlight-mode-group");
  if (modeGroup) {
    modeGroup.addEventListener("click", (e) => {
      const btn = e.target.closest(".radio-btn");
      if (!btn) return;
      modeGroup.querySelectorAll(".radio-btn").forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      S.highlightMode = btn.dataset.mode;
      renderGame();
    });
  }
}

/* ---------------------------------------------------------------- 02: Diffusion Graph */
function renderSpread() {
  const p = S.p, errs = validationErrors(p);
  $("#spread-error").textContent = errs.join(" ");
  if (errs.length) return;

  for (const k of Object.keys(DEFAULTS)) {
    const o = $(`#o-${k}`);
    if (o) o.textContent = k === "population" ? int(p[k]) : k === "moderation" ? p[k].toFixed(2) : p[k];
  }

  const T = p.steps, N = p.population;
  const mine = run(p);
  const base = run({ ...p, moderation: 0 });

  // Compute inflection point on active curve (d²I/dt² = 0)
  let inflStep = null;
  const diffs = mine.slice(1).map((v, i) => v - mine[i]);
  if (diffs.length > 0 && Math.max(...diffs) > 0) {
    inflStep = diffs.indexOf(Math.max(...diffs)) + 1;
  }

  // Peak on active curve
  const peakVal = Math.max(...mine);
  const peakStep = mine.indexOf(peakVal);

  // Build shaded polygon between baseline and active curve (Users Saved)
  const shadedPts = [
    ...base.map((v, t) => [t, v]),
    ...mine.slice().reverse().map((v, idx) => [T - idx, v]),
  ];

  const series = [
    {
      label: "Baseline (m = 0.00)",
      cls: "line--baseline",
      pts: base.map((v, t) => [t, v]),
      showMarkers: false,
    },
    {
      label: `Policy (m = ${p.moderation.toFixed(2)})`,
      cls: "line--active",
      pts: mine.map((v, t) => [t, v]),
      showMarkers: true,
    },
  ];

  const annotations = [];
  if (inflStep != null && inflStep < T) {
    annotations.push({
      x: inflStep,
      y: mine[inflStep],
      text: `Inflection: Step ${inflStep}`,
      color: "#F59E0B",
      dy: 24,
    });
  }
  if (peakStep != null) {
    annotations.push({
      x: peakStep,
      y: peakVal,
      text: `Peak: ${int(peakVal)}`,
      color: "#00F0FF",
      dy: -32,
    });
  }

  const tick = Math.ceil(T / 5 / 5) * 5;
  const chart = lineChart($("#spread-chart"), {
    x0: 0,
    x1: T,
    y0: 0,
    y1: N * 1.05,
    ceiling: N,
    right: 140,
    series,
    shadedArea: { pts: shadedPts },
    annotations,
    xTicks: Array.from({ length: Math.floor(T / tick) + 1 }, (_, i) => i * tick),
    yTicks: [0, N * 0.25, N * 0.5, N * 0.75, N].map(Math.round),
    yFmt: compact,
    vlines: S.hoverT == null ? [] : [{ x: S.hoverT }],
  });

  // Update Bottom Stats Triplet Panel
  const finalBase = base.at(-1);
  const finalMine = mine.at(-1);
  const savedUsers = Math.max(0, finalBase - finalMine);

  const elBase = $("#stat-baseline");
  if (elBase) elBase.textContent = `${int(finalBase)} exposed`;

  const elMod = $("#stat-moderated");
  if (elMod) elMod.textContent = `${int(finalMine)} exposed`;

  const elSaved = $("#stat-saved");
  if (elSaved) elSaved.textContent = `${int(savedUsers)} Prevented`;

  const t = S.hoverT;
  $("#spread-read").textContent = t == null
    ? "Hover or touch the chart to inspect step exposure across both curves."
    : `Step ${t}  ·  Active Policy: ${int(mine[t])} exposed (${((mine[t] / N) * 100).toFixed(1)}%)  ·  Baseline (m=0): ${int(base[t])} exposed  ·  Infections Prevented: ${int(Math.max(0, base[t] - mine[t]))}`;

  $("#spread-chart").onpointermove = (e) => {
    const v = Math.max(0, Math.min(T, Math.round(chart.inv(e.clientX))));
    if (v !== S.hoverT) { S.hoverT = v; renderSpread(); }
  };
  $("#spread-chart").onpointerleave = () => { S.hoverT = null; renderSpread(); };

  renderHeroKPIs();
}

function initSpread() {
  for (const k of Object.keys(DEFAULTS)) {
    const el = $(`#${k}`);
    if (!el) continue;
    el.value = S.p[k];
    el.addEventListener("input", () => {
      S.p[k] = +el.value;
      renderSpread();
    });
  }

  // Model segmented control (Logistic)
  const modelSeg = $("#model-seg");
  if (modelSeg) {
    modelSeg.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      S.model = b.dataset.v || "logistic";
      modelSeg.querySelectorAll("button").forEach((x) => x.classList.toggle("is-active", x === b));
      renderSpread();
    });
  }

  // Reset simulation controls to defaults
  $("#spread-reset").addEventListener("click", () => {
    S.p = { ...DEFAULTS };
    for (const k of Object.keys(DEFAULTS)) {
      if ($(`#${k}`)) $(`#${k}`).value = S.p[k];
    }
    renderSpread();
  });
}

/* ---------------------------------------------------------------- Theme */
function initTheme() {
  const root = document.documentElement;
  const apply = (t) => {
    root.dataset.theme = t;
    $("#theme-name").textContent = t === "night" ? "Light" : "Dark";
    $('meta[name="theme-color"]').content = t === "night" ? "#0A0F1E" : "#F8FAFC";
    readColors();
    dispatchEvent(new Event("themechange"));
  };
  apply(root.dataset.theme === "paper" ? "paper" : "night");
  $("#theme").addEventListener("click", () => {
    const t = root.dataset.theme === "night" ? "paper" : "night";
    apply(t);
    try { localStorage.setItem("theme", t); } catch {}
  });
}

/* ---------------------------------------------------------------- Hero Animation & Ticker */
function initHero() {
  const canvas = $("#hero-net");
  if (!canvas) return;
  const g = makeGraph("scale-free", 70, 11);
  const h = runNetwork(g, { seeds: 3, spread: 0.55, moderation: 0.12, steps: 14, seed: 5 });
  let i = reduceMotion ? 14 : 0, timer = null;
  const view = netView(canvas, () => ({ g, state: h[i].state, prev: i ? h[i - 1].state : null, step: i }), 3.2);
  const label = () => {
    const el = $("#hero-step");
    if (el) el.textContent = `Step ${i} · ${h[i].exposed} of ${g.n} nodes exposed`;
  };
  const tick = () => {
    i = i >= 14 ? 0 : i + 1;
    label();
    view.kick();
    timer = setTimeout(tick, i === 14 ? 2800 : 950);
  };
  label();
  view.kick();
  if (!reduceMotion) {
    new IntersectionObserver(([e]) => {
      clearTimeout(timer);
      if (e.isIntersecting) timer = setTimeout(tick, 900);
    }).observe(canvas);
  }
}

function initTicker() {
  const p = DEFAULTS, an = analyse(BASE_PAYOFFS);
  const pct = (m) => Math.round((logistic({ ...p, moderation: m }).at(-1) / p.population) * 100);
  const items = [
    `Nash Equilibrium: <b>${an.nash.map(words).join(" or ")}</b>`,
    `Unmitigated Outbreak: <b>${pct(0)}%</b> exposed in ${p.steps} steps`,
    `Institutional Moderation (m = 0.85): Only <b>${pct(0.85)}%</b> exposed`,
    `Critical Tipping Point: <b>m* = ${tippingM(p.beta).toFixed(2)}</b> at β = ${p.beta}`,
    `Viral Payoff: <b>+${BASE_PAYOFFS.SW[0]}</b> vs weak platform, <b>${num(BASE_PAYOFFS.SM[0])}</b> when penalized`,
  ].map((t) => `<span>${t}</span>`).join("");
  $("#ticker").innerHTML = items + items;
}

function initMotion() {
  const here = new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting) {
      document.querySelectorAll(".mast__links a").forEach((a) => {
        a.classList.toggle("is-here", a.getAttribute("href") === `#${e.target.id}`);
      });
    }
  }), { rootMargin: "-40% 0px -55% 0px" });
  document.querySelectorAll("main section[id], .hero").forEach((s) => here.observe(s));

  if (reduceMotion) return;

  if (matchMedia("(pointer: fine)").matches) {
    const mx = gsap.quickTo("#glow", "x", { duration: 0.9, ease: "power3" });
    const my = gsap.quickTo("#glow", "y", { duration: 0.9, ease: "power3" });
    gsap.set("#glow", { x: innerWidth * 0.6, y: innerHeight * 0.3 });
    addEventListener("pointermove", (e) => { mx(e.clientX); my(e.clientY); });
  }

  gsap.to(".hero__fig", { yPercent: -5, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });
}

/* ---------------------------------------------------------------- Boot */
initTheme();
initHero();
initTicker();
initPresetsAndFilters();
initPayoffFields();
renderGame();
initSpread();
renderSpread();
initMotion();
renderHeroKPIs();
