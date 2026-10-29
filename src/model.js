export const DEFAULTS = { population: 10000, initialExposed: 100, beta: 0.35, moderation: 0.50, steps: 30 };

export const SCENARIO_PRESETS = {
  "Default Course Baseline": {
    pop: 10000, seed: 100, beta: 0.35, mod: 0.50, steps: 30,
    payoffs: { SW: [5, -4], SM: [-2, 3], NW: [1, 0], NM: [0, 2] },
  },
  "Highly Viral Outbreak (Low Moderation)": {
    pop: 15000, seed: 250, beta: 0.65, mod: 0.15, steps: 35,
    payoffs: { SW: [7, -6], SM: [-1, 2], NW: [1, 0], NM: [0, 1.5] },
  },
  "Strict Platform Deterrence": {
    pop: 10000, seed: 50, beta: 0.25, mod: 0.85, steps: 30,
    payoffs: { SW: [4, -3], SM: [-3, 4], NW: [1, 0], NM: [0, 2.5] },
  },
  "Zero Moderation (Laissez-Faire)": {
    pop: 10000, seed: 100, beta: 0.40, mod: 0.00, steps: 30,
    payoffs: { SW: [5, -4], SM: [-2, 3], NW: [1, 0], NM: [0, 2] },
  },
};

export const CELL_LOGIC = {
  SW: "Weak moderation allows fake news to spread unhindered. Sharer reaps maximum engagement (+5), while platform brand suffers severe advertiser damage (-4).",
  SM: "Platform filters and sanctions active misinformation (+3). Penalties and shadowbans eliminate virality gains, leaving the sharer with a net loss (-2).",
  NW: "Users post organic truthful content (+1). Platform maintains low operating overhead with neutral baseline utility (0).",
  NM: "Sharer complies with platform rules (0). Platform preserves a clean, trustworthy community (+2), minus steady automated filter infrastructure costs."
};

export const CELL_SUBTITLES = {
  SW: "Viral Exploitation",
  SM: "Active Deterrence",
  NW: "Laissez-Faire Baseline",
  NM: "Enforced Compliance"
};

const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

/* ------------------------------------------------------------ diffusion */
export function validationErrors(p) {
  const e = [];
  if (!(p.population > 0)) e.push("Population must be positive.");
  if (p.initialExposed < 0 || p.initialExposed > p.population) e.push("Initial seeds must be between 0 and the population.");
  if (p.beta < 0) e.push("Sharing rate cannot be negative.");
  if (p.moderation < 0 || p.moderation > 1) e.push("Moderation must be between 0 and 1.");
  return e;
}

// Logistic: I' = I + beta (1 - m) I (1 - I/N), clamped to [0, N].
export function logistic(p) {
  const N = p.population, k = p.beta * (1 - p.moderation);
  const I = [Math.min(N, p.initialExposed)];
  for (let t = 0; t < p.steps; t++) {
    const x = I[t];
    I.push(clamp(x + k * x * (1 - x / N), 0, N));
  }
  return I;
}

/* ------------------------------------------------------------ the game */
// Rows: Sharer (S spread / N stay quiet). Columns: Platform (W weak / M strong).
export const BASE_PAYOFFS = { SW: [5, -4], SM: [-2, 3], NW: [1, 0], NM: [0, 2] };
const near = (a, b) => Math.abs(a - b) < 1e-9;

// m* where the sharer's payoff for spreading under strong moderation hits zero.
export function tippingM(beta, pen = 4, viral = 5) {
  const r = viral * (beta / 0.35);
  return r + pen > 0 ? clamp(r / (r + pen), 0, 1) : 0.5;
}

export function analyse(P) {
  const u = (s, p) => P[s + p];
  const brSharer = (p) => { const [a, b] = [u("S", p)[0], u("N", p)[0]]; return near(a, b) ? ["S", "N"] : a > b ? ["S"] : ["N"]; };
  const brPlatform = (s) => { const [w, m] = [u(s, "W")[1], u(s, "M")[1]]; return near(w, m) ? ["W", "M"] : m > w ? ["M"] : ["W"]; };
  const brS = { W: brSharer("W"), M: brSharer("M") }, brP = { S: brPlatform("S"), N: brPlatform("N") };
  const nash = [];
  for (const s of "SN") for (const p of "WM") if (brS[p].includes(s) && brP[s].includes(p)) nash.push(s + p);

  // Strict dominance
  const sharerDom = u("S", "W")[0] > u("N", "W")[0] && u("S", "M")[0] > u("N", "M")[0] ? "S"
    : u("N", "W")[0] > u("S", "W")[0] && u("N", "M")[0] > u("S", "M")[0] ? "N" : null;
  const platformDom = u("S", "M")[1] > u("S", "W")[1] && u("N", "M")[1] > u("N", "W")[1] ? "M"
    : u("S", "W")[1] > u("S", "M")[1] && u("N", "W")[1] > u("N", "M")[1] ? "W" : null;

  // Mixed: p* = P(sharer spreads), q* = P(platform weak)
  const dp = (u("S", "W")[1] - u("S", "M")[1]) - (u("N", "W")[1] - u("N", "M")[1]);
  const dq = (u("S", "W")[0] - u("S", "M")[0]) - (u("N", "W")[0] - u("N", "M")[0]);
  let mixed = { exists: false, p: null, q: null };
  if (!near(dp, 0) && !near(dq, 0)) {
    const p = (u("N", "M")[1] - u("N", "W")[1]) / dp, q = (u("N", "M")[0] - u("S", "M")[0]) / dq;
    mixed = { exists: p > 1e-7 && p < 1 - 1e-7 && q > 1e-7 && q < 1 - 1e-7, p, q };  // raw p, q kept so the page can show why it fails
  }

  const keys = ["SW", "SM", "NW", "NM"];
  const pareto = keys.filter((a) => !keys.some((b) => b !== a &&
    P[b][0] >= P[a][0] && P[b][1] >= P[a][1] && (P[b][0] > P[a][0] || P[b][1] > P[a][1])));

  return { P, brS, brP, nash, sharerDom, platformDom, mixed, pareto };
}

// What each side would gain by switching alone from a profile (sharer: row, platform: column).
export function deviations(P, profile) {
  const [s, p] = profile, s2 = s === "S" ? "N" : "S", p2 = p === "W" ? "M" : "W";
  return [
    { who: "Sharer", to: s2, gain: P[s2 + p][0] - P[s + p][0] },
    { who: "Platform", to: p2, gain: P[s + p2][1] - P[s + p][1] },
  ];
}

/* ------------------------------------------------------------ network */
export function rng(seed) {                       // mulberry32
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function makeGraph(kind, n, seed) {
  const r = rng(seed), edges = new Set();
  const add = (i, j) => i !== j && edges.add(i < j ? `${i}-${j}` : `${j}-${i}`);
  if (kind === "scale-free") {
    const bag = [0, 1]; add(0, 1);
    for (let v = 2; v < n; v++) {
      const picks = new Set();
      while (picks.size < Math.min(2, v)) picks.add(bag[Math.floor(r() * bag.length)]);
      picks.forEach((u) => { add(v, u); bag.push(v, u); });
    }
  } else {
    const p = Math.min(1, Math.max(0.04, 3.2 / n));
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) if (r() < p) add(i, j);
  }
  const E = [...edges].map((e) => e.split("-").map(Number));
  const adj = Array.from({ length: n }, () => []);
  E.forEach(([i, j]) => { adj[i].push(j); adj[j].push(i); });

  // Fruchterman-Reingold, run once so the picture stays still while the news moves.
  const pos = Array.from({ length: n }, () => [r(), r()]);
  const k = 0.9 / Math.sqrt(n);
  for (let it = 0; it < 160; it++) {
    const temp = 0.12 * (1 - it / 160) + 0.004;
    const disp = pos.map(() => [0, 0]);
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      const dx = pos[i][0] - pos[j][0], dy = pos[i][1] - pos[j][1], d = Math.hypot(dx, dy) || 0.001;
      const f = (k * k) / d;
      disp[i][0] += (dx / d) * f; disp[i][1] += (dy / d) * f;
      disp[j][0] -= (dx / d) * f; disp[j][1] -= (dy / d) * f;
    }
    for (const [i, j] of E) {
      const dx = pos[i][0] - pos[j][0], dy = pos[i][1] - pos[j][1], d = Math.hypot(dx, dy) || 0.001;
      const f = (d * d) / k;
      disp[i][0] -= (dx / d) * f; disp[i][1] -= (dy / d) * f;
      disp[j][0] += (dx / d) * f; disp[j][1] += (dy / d) * f;
    }
    for (let i = 0; i < n; i++) {
      const d = Math.hypot(...disp[i]) || 0.001, s = Math.min(d, temp) / d;
      pos[i][0] += disp[i][0] * s; pos[i][1] += disp[i][1] * s;
    }
  }
  const xs = pos.map((p) => p[0]), ys = pos.map((p) => p[1]);
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  pos.forEach((p) => { p[0] = (p[0] - x0) / (x1 - x0 || 1); p[1] = (p[1] - y0) / (y1 - y0 || 1); });
  return { n, edges: E, adj, pos, deg: adj.map((a) => a.length) };
}

export const SUSC = 0, EXPO = 1, MODR = 2;

// Same rules as run_full_network_simulation; seeds are the highest-degree nodes.
export function runNetwork(g, { seeds, spread, moderation, steps, seed }) {
  const r = rng(seed), pTrans = clamp(spread * (1 - moderation), 0, 1);
  const order = [...g.deg.keys()].sort((a, b) => g.deg[b] - g.deg[a]);
  let st = new Array(g.n).fill(SUSC);
  order.slice(0, seeds).forEach((i) => (st[i] = EXPO));
  const count = (s, v) => s.filter((x) => x === v).length;
  const rec = (s, fresh) => ({ state: s, exposed: g.n - count(s, SUSC), active: count(s, EXPO), moderated: count(s, MODR), fresh });
  const hist = [rec(st, seeds)];
  for (let t = 0; t < steps; t++) {
    const next = [...st], hit = new Set();
    const active = st.flatMap((v, i) => (v === EXPO ? [i] : []));
    for (const a of active) for (const nb of g.adj[a]) if (st[nb] === SUSC && !hit.has(nb) && r() < pTrans) hit.add(nb);
    hit.forEach((i) => (next[i] = EXPO));
    for (const a of active) if (r() < moderation) next[a] = MODR;
    st = next;
    hist.push(rec(st, hit.size));
  }
  return hist;
}
