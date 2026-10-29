# Interactive Fake News Simulation & Game Theory Laboratory

> **Game Theory Project by:**  
> • **Shreshth Juneja** (2427030246)  
> • **Devaanshee Agarwal** (2427030504)

An interactive, web-native research dashboard modeling strategic deterrence between **Content Sharers** and **Social Media Platforms**, coupled with macroscopic epidemiological diffusion and network propagation.

Built with **HTML5, CSS3, Vanilla JavaScript, Vite, and GSAP**, with zero backend dependencies. Fully optimized for instant deployment on **Vercel**.

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+

### Install & Run Locally
```bash
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173).

### Production Build
```bash
npm run build
npm run preview
```
Production assets are bundled into `dist/`.

---

## ☁️ Deploying to Vercel

1. Push this repository to GitHub.
2. In [Vercel](https://vercel.com), import your repository (`shreshth-j/fake_news_cws_project_js`).
3. Vercel automatically detects the **Vite** framework preset:
   - **Build Command:** `vite build` (or `npm run build`)
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`
4. Click **Deploy**.

---

## 🧪 Laboratory Sections

1. **01 · Payoff Matrix & Strategy:** Interactive 2×2 normal-form strategic game with live Nash equilibria, strictly dominant strategies, best-response indicators, and dynamic payoff customization.
2. **02 · Diffusion Graph:** Real-time macroscopic logistic contagion model with interactive sliders ($N$, $I_0$, $\beta$, $m$, $T$), baseline comparisons, and live KPI metrics.
3. **04 · Theory:** Core Game Theory and Information Security concepts with active mathematical formulations and current parameter mappings.

---

## 📂 Project Structure

```
├── index.html              # Main single-page application entry
├── package.json            # Project dependencies and Vite scripts
├── public/                 # Static assets (including report.docx)
├── src/
│   ├── main.js             # Application controller, charts & DOM handlers
│   ├── model.js            # Game theory calculations & diffusion engine
│   └── style.css           # Styling with Dark and Light mode support
└── README.md
```
