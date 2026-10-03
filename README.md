# 🩺 Medical Research Assistant
> **Specialist Clinical Intelligence & Decision Support Platform for MD Medicine**

An advanced, evidence-based medical research assistant tailored for MD Medicine specialists (Internal Medicine, Critical Care, and Sub-specialties). The application synthesizes complex multimorbid clinical presentations, extracts statistical metrics and practice-changing insights from landmark clinical trials, and navigates structured international clinical guidelines.

Designed with a **dual-engine architecture** supporting both high-performance local/cloud backend execution (FastAPI + Python 3.14) and 100% serverless, zero-cost deployment on **GitHub Pages** (Pyodide WebAssembly Python).

---

## 🌟 Key Capabilities

### 1. Complex Patient Case Study Processor
* **Problem Representation**: Synthesizes unstructured clinical text (demographics, HPI, vitals, exam, lab biomarkers, imaging) into standard MD-level problem summaries.
* **Hemodynamic & Biomarker Alerts**: Flags hypoxemia thresholds, shock states (MAP < 65 mmHg), severe thrombocytopenia (<20k/uL), hyperferritinemia (>3k ng/mL), and schistocytes/MAHA.
* **3-Tier Differential Diagnoses**:
  * **Tier 1 (High Probability / Leading Diagnoses)**: Correlated with primary syndrome complex.
  * **Tier 2 (Cannot-Miss Emergencies)**: Rapidly fatal conditions requiring urgent exclusion (e.g., aTTP, Acute Interstitial Pneumonia, Tamponade).
  * **Tier 3 (Rare Conditions / Zebras)**: Atypical presentations and autoimmune mimics.
* **Targeted Diagnostic Workup**: Prioritized by urgency (Stat, Confirmatory, Biomarkers, Advanced Imaging).
* **Evidence-Based Initial Management**: Specific pharmacological regimens, hemodynamic targets, and critical red flags.

### 2. Medical Research Paper Summarizer
* **PICO Framework Extraction**: Automatically parses Population (P), Intervention (I), Comparison (C), and Primary/Secondary Outcomes (O).
* **Statistical Rigor & Clinical Magnitude**: Calculates and presents Hazard Ratios (HR), Relative Risks (RR), 95% Confidence Intervals, Absolute Risk Reduction (ARR), and Number Needed to Treat (NNT).
* **Methodological Evaluation**: Evaluates trial design (Phase 3 RCTs, platform trials), sample size power, follow-up completeness, strengths, and clinical limitations.
* **MD Practice-Changing Takeaways**: Delivers actionable takeaways referencing guideline classes (e.g. Class 1A) and clinical applicability.

### 3. Clinical Practice Guidelines Explorer
* **Cardiology (AHA / ACC / HFSA 2024)**: 4-Pillar Guideline-Directed Medical Therapy (GDMT) for HFrEF (ARNi, Beta-blocker, MRA, SGLT2i), target doses, and device indications (ICD/CRT).
* **Nephrology (KDIGO 2024)**: Evaluation and management of CKD (RAS blockade, SGLT2i, nonsteroidal MRA Finerenone, standardized BP targets).
* **Critical Care & Infectious Disease (Surviving Sepsis Campaign 2026)**: Hour-1 resuscitation bundles, balanced crystalloids, norepinephrine/vasopressin protocols, and steroid triggers.
* **Pulmonology (GOLD 2026)**: COPD Group A/B/E strategy, dual bronchodilation (LABA+LAMA), triple therapy (ICS) indications by eosinophil thresholds, and acute exacerbation management.

---

## 🏗️ Dual-Engine Architecture

| Feature | Mode 1: FastAPI Server | Mode 2: GitHub Pages (Pyodide Wasm) |
| :--- | :--- | :--- |
| **Runtime** | Python 3.14 (Server-side) | Python 3.12+ (WebAssembly in-browser) |
| **Hosting Cost** | Standard server/container cost | **100% Free on GitHub Pages** |
| **API Endpoints** | RESTful `/api/...` with Swagger `/docs` | Client-side virtual Python execution |
| **Data Privacy** | Hospital/private network | Completely private (no data leaves browser) |
| **Switching** | Automatic or manual toggle in UI | Automatic fallback when server unavailable |

---

## 🚀 Quickstart: Local Server Execution

### 1. Prerequisites
- Python 3.10+ installed

### 2. Clone and Setup
```bash
git clone https://github.com/<username>/med-research-assistant.git
cd med-research-assistant
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python3 app.py
```
Open your browser to:
```
http://localhost:8000
```
API Documentation (Swagger UI):
```
http://localhost:8000/docs
```

---

## 🌐 Deploying to GitHub Pages (100% Free Hosting)

The repository includes a ready-to-run GitHub Actions workflow (`.github/workflows/deploy.yml`).

1. Push your repository to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initialize Medical Research Assistant"
   git remote add origin https://github.com/<username>/<repo-name>.git
   git branch -M main
   git push -u origin main
   ```
2. On GitHub, navigate to **Settings** > **Pages**.
3. Under **Build and deployment** > **Source**, select **GitHub Actions**.
4. The workflow will automatically deploy the site. Your app will be live at:
   ```
   https://<username>.github.io/<repo-name>/
   ```
5. When loaded on GitHub Pages, the app automatically initializes Pyodide WebAssembly, running the exact same Python clinical intelligence engine in your browser without any server needed!

---

## 📁 Repository Structure

```
med-research-assistant/
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Pages deployment workflow
├── med_assistant/
│   ├── __init__.py               # Package exports
│   ├── case_processor.py         # Clinical reasoning & differential engine
│   ├── paper_summarizer.py       # PICO & trial statistical summarizer
│   ├── guidelines.py             # Guidelines search & retrieval engine
│   └── mock_data.py              # Pre-loaded clinical vignettes & trials
├── static/
│   ├── css/
│   │   └── style.css             # Specialist dark obsidian UI theme
│   ├── js/
│   │   ├── samples.js            # Offline clinical dataset presets
│   │   ├── pyodide_runner.js     # WebAssembly Python execution bridge
│   │   └── app.js                # UI controller & engine coordinator
│   └── index.html                # Web application dashboard
├── app.py                        # FastAPI REST server & static file host
├── index.html                    # Root index for GitHub Pages direct serving
├── requirements.txt              # Python server dependencies
└── README.md                     # Comprehensive documentation
```

---

## 🧪 Testing the Engine

Run the built-in test suite to verify all Python modules:
```bash
python3 -c "
import med_assistant
from med_assistant import CaseStudyProcessor, PaperSummarizer, GuidelineEngine, SAMPLE_CASES, SAMPLE_PAPERS, GUIDELINES_DATA

cp = CaseStudyProcessor()
print('Case Processor:', len(cp.analyze_case(SAMPLE_CASES[0]['hpi'])['differentials']), 'differentials')

ps = PaperSummarizer()
print('Paper Summarizer:', ps.summarize(SAMPLE_PAPERS[0]['abstract'])['trial_acronym'])

ge = GuidelineEngine()
print('Guideline Engine:', len(ge.get_all_guidelines()), 'guidelines loaded')
"
```

---

## ⚖️ Clinical Disclaimer
This application is designed as a clinical decision support and educational research synthesizer for healthcare practitioners and MD Medicine trainees. It is not an autonomous diagnostic device. All clinical guidance and drug dosing must be correlated with individualized patient factors and official drug product characteristics.
