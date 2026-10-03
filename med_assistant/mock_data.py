"""
Pre-loaded clinical cases, landmark research papers, and guidelines for MD Medicine specialists.
"""

SAMPLE_CASES = [
    {
        "id": "case-mda5",
        "title": "58M: Rapidly Progressive Dyspnea, Mechanics Hands, & Elevated Ferritin",
        "demographics": "58-year-old male, non-smoker, retired software engineer",
        "hpi": (
            "Patient presents with a 4-week history of rapidly deteriorating exertional dyspnea (NYHA Class I -> IV) "
            "and a dry non-productive cough. Over the preceding 2 months, he noted painful fissuring on the radial aspects "
            "of his fingers ('mechanic's hands'), erythematous violaceous papules over the MCP and PIP joints (Gottron papules), "
            "and mild proximal lower extremity weakness with difficulty rising from a low chair. Denies fever, hemoptysis, or chest pain."
        ),
        "vitals": "BP: 124/78 mmHg, HR: 98 bpm (sinus), RR: 28 breaths/min, SpO2: 86% on room air (92% on 4L nasal cannula), Temp: 37.4°C.",
        "physical_exam": (
            "Chest: Bilateral fine Velcro-like inspiratory crackles in mid-to-lower lung fields. No wheezing.\n"
            "Skin: Violaceous erythema on knuckles (Gottron papules), periungual telangiectasias, tender hyperkeratotic fissures on lateral digits.\n"
            "Neuromuscular: Proximal muscle strength 4/5 in bilateral quadriceps and deltoids. Normal sensation and deep tendon reflexes."
        ),
        "labs": (
            "CBC: Hb 13.2 g/dL, WBC 11,200/uL (Lymphopenia: 800/uL), Platelets 220,000/uL.\n"
            "Metabolic: Creatinine 0.9 mg/dL, eGFR >90 mL/min, ALT 84 U/L, AST 112 U/L.\n"
            "Inflammatory/Muscle: Ferritin 3,450 ng/mL (markedly elevated), CPK 380 U/L (mild elevation), Aldolase 14 U/L, CRP 42 mg/L, ESR 64 mm/hr.\n"
            "ABG (Room Air): pH 7.45, PaO2 54 mmHg, PaCO2 31 mmHg, HCO3 21 mEq/L (Alveolar-arterial gradient markedly widened)."
        ),
        "imaging": (
            "HRCT Chest: Extensive subpleural and peribronchovascular consolidations with ground-glass opacities, traction bronchiectasis, "
            "and rapidly progressive consolidation in bilateral lower lobes without honeycombing (consistent with acute interstitial pneumonia / rapidly progressive organizing pneumonia pattern)."
        )
    },
    {
        "id": "case-ttp-sle",
        "title": "34F: Fever, Malar Erythema, Thrombocytopenia, & Acute Confusion",
        "demographics": "34-year-old female with an established diagnosis of Systemic Lupus Erythematosus (SLE)",
        "hpi": (
            "Known SLE patient compliant with hydroxychloroquine presents with 5 days of severe generalized fatigue, unremitting low-grade fevers, "
            "diffuse purpuric skin lesions on lower extremities, and sudden onset fluctuating confusion and word-finding difficulty over the last 12 hours. "
            "Her family noted dark-tea-colored urine for 2 days. Denies recent bloody diarrhea or travel."
        ),
        "vitals": "BP: 154/96 mmHg, HR: 114 bpm, RR: 20 breaths/min, SpO2: 98% on room air, Temp: 38.6°C.",
        "physical_exam": (
            "General: Pale, mildly jaundiced sclera, lethargic but arousable, oriented only to person.\n"
            "Skin: Classic malar rash sparing nasolabial folds; scattered petechiae and ecchymoses on bilateral pretibial surfaces.\n"
            "Neuro: Fluctuating cognitive deficits, no focal motor weakness, cranial nerves intact, negative meningeal signs."
        ),
        "labs": (
            "CBC: Hb 7.1 g/dL (normocytic), WBC 8,900/uL, Platelets 14,000/uL (critical thrombocytopenia).\n"
            "Hemolysis Panel: Reticulocyte count 8.2%, Total Bilirubin 4.1 mg/dL, Direct Bilirubin 0.6 mg/dL, LDH 1,840 U/L (severely elevated), Haptoglobin <10 mg/dL.\n"
            "Peripheral Blood Smear: Markedly increased schistocytes (3-4% per high-power field), polychromasia, severely reduced platelets with no clumping.\n"
            "Coagulation: PT 12.4 s, INR 1.0, aPTT 31 s, Fibrinogen 340 mg/dL (Normal coagulation profile excluding overt DIC).\n"
            "Renal: Creatinine 2.4 mg/dL (baseline 0.8), BUN 48 mg/dL. Urinalysis: 3+ protein, 2+ blood, 15-20 dysmorphic RBCs/hpf."
        ),
        "imaging": "CT Brain (without contrast): No acute intracranial hemorrhage, territorial infarction, or mass effect."
    },
    {
        "id": "case-crs-hfref",
        "title": "67M: Acute Decompensated Heart Failure with Worsening Renal Function (CRS Type 1)",
        "demographics": "67-year-old male with ischemic cardiomyopathy (LVEF 25%), T2DM, and Stage 3b CKD",
        "hpi": (
            "Brought to the emergency department with 1 week of worsening orthopnea (sleeping on 4 pillows), paroxysmal nocturnal dyspnea, "
            "marked abdominal distension, and 8 kg weight gain over 10 days despite taking oral furosemide 80 mg BID at home. "
            "He reports reduced urine output (<400 mL in last 24h) and profound lethargy."
        ),
        "vitals": "BP: 102/68 mmHg, HR: 84 bpm (atrial fibrillation), RR: 26 breaths/min, SpO2: 88% on room air (94% on 6L O2 via facemask), Temp: 36.8°C.",
        "physical_exam": (
            "Cardiovascular: Jugular venous distension to the angle of the jaw (JVP >15 cm H2O) with prominent v-waves. Displaced, sustained apical impulse. S3 gallop present. Grade 3/6 holosystolic murmur at apex radiating to axilla.\n"
            "Respiratory: Bilateral coarse crackles ascending to mid-scapular level with bilateral dullness to percussion at lung bases.\n"
            "Abdomen/Extremities: Tender hepatomegaly (liver edge 4 cm below costal margin), positive hepatojugular reflux, 3+ pitting edema extending to mid-thighs with scrotal edema."
        ),
        "labs": (
            "Serum Chemistries: Sodium 128 mEq/L (dilutional hyponatremia), Potassium 5.4 mEq/L, Bicarbonate 20 mEq/L, Blood Urea Nitrogen 68 mg/dL, Serum Creatinine 3.4 mg/dL (baseline 1.8 mg/dL).\n"
            "Cardiac Biomarkers: NT-proBNP 18,600 pg/mL, Troponin-I 0.08 ng/mL (mild demand ischemia elevation).\n"
            "Urine Studies: Spot Urine Sodium 18 mEq/L, Fractional Excretion of Sodium (FENa) 0.6%."
        ),
        "imaging": (
            "Chest X-Ray: Cardiomegaly, bilateral alveolar pulmonary edema (batwing appearance), Kerley B lines, and moderate bilateral pleural effusions.\n"
            "Bedside POCUS: Dilated, non-collapsible IVC (diameter 2.6 cm, collapsibility index <10%), multiple bilateral lung B-lines (>5 per rib space in 8 zones)."
        )
    }
]

SAMPLE_PAPERS = [
    {
        "id": "paper-dapa-hf",
        "title": "Dapagliflozin in Patients with Heart Failure and Reduced Ejection Fraction (DAPA-HF)",
        "journal": "The New England Journal of Medicine (NEJM)",
        "doi": "10.1056/NEJMoa1911303",
        "year": "2019",
        "abstract": (
            "BACKGROUND: In patients with type 2 diabetes, SGLT2 inhibitors reduce the risk of hospitalization for heart failure. "
            "However, the effects of dapagliflozin in patients with established heart failure and a reduced ejection fraction (HFrEF), "
            "regardless of the presence or absence of type 2 diabetes, have not been evaluated.\n\n"
            "METHODS: In this phase 3, placebo-controlled trial, we randomly assigned 4,744 patients with NYHA class II, III, or IV "
            "heart failure and an ejection fraction of 40% or less to receive either dapagliflozin (at a dose of 10 mg once daily) "
            "or matching placebo, in addition to standard recommended guideline-directed medical therapy. The primary composite outcome "
            "was worsening heart failure (hospitalization or an urgent visit resulting in intravenous therapy for heart failure) or death from cardiovascular causes.\n\n"
            "RESULTS: Over a median follow-up of 18.2 months, the primary outcome occurred in 386 of 2,373 patients (16.3%) in the dapagliflozin group "
            "and in 502 of 2,371 patients (21.2%) in the placebo group (hazard ratio, 0.74; 95% confidence interval [CI], 0.65 to 0.85; P<0.001). "
            "A first worsening heart failure event occurred in 237 patients (10.0%) in the dapagliflozin group and in 326 patients (13.7%) in the placebo group (HR, 0.70; 95% CI, 0.59 to 0.83). "
            "Death from cardiovascular causes occurred in 227 patients (9.6%) in the dapagliflozin group and in 273 (11.5%) in the placebo group (HR, 0.82; 95% CI, 0.69 to 0.98). "
            "Findings in patients with diabetes were similar to those in patients without diabetes. Adverse events related to volume depletion, renal dysfunction, and hypoglycemia were infrequent and balanced between groups."
        )
    },
    {
        "id": "paper-recovery",
        "title": "Dexamethasone in Hospitalized Patients with COVID-19 (RECOVERY Trial)",
        "journal": "The New England Journal of Medicine (NEJM)",
        "doi": "10.1056/NEJMoa2021436",
        "year": "2021",
        "abstract": (
            "BACKGROUND: Coronavirus disease 2019 (COVID-19) is associated with diffuse lung damage and dysregulated systemic inflammation. "
            "The therapeutic efficacy of glucocorticoids in hospitalized patients with acute hypoxemic respiratory failure required rigorous randomized trial verification.\n\n"
            "METHODS: In this controlled, open-label trial, 2,104 hospitalized patients with confirmed or suspected COVID-19 were randomly assigned to receive "
            "oral or intravenous dexamethasone (at a dose of 6 mg once daily) for up to 10 days, and 4,321 patients were assigned to receive usual care alone. "
            "The primary outcome was 28-day all-cause mortality.\n\n"
            "RESULTS: Overall, 482 patients (22.9%) in the dexamethasone group and 1,110 patients (25.7%) in the usual care group died within 28 days "
            "(age-adjusted rate ratio, 0.83; 95% CI, 0.75 to 0.93; P<0.001). The proportional and absolute benefits varied markedly according to the level of respiratory support at randomization: "
            "in the group of patients receiving invasive mechanical ventilation, dexamethasone reduced 28-day mortality by one-third (29.3% vs. 41.4%; rate ratio, 0.64; 95% CI, 0.51 to 0.81). "
            "Among patients receiving supplemental oxygen without mechanical ventilation, mortality was reduced by one-fifth (23.3% vs. 26.2%; rate ratio, 0.82; 95% CI, 0.72 to 0.94). "
            "However, among patients who were not receiving any respiratory support at randomization, there was no clear benefit and potential trend toward harm (17.8% vs. 14.0%; rate ratio, 1.19; 95% CI, 0.91 to 1.55)."
        )
    },
    {
        "id": "paper-fidelio",
        "title": "Effect of Finerenone on Chronic Kidney Disease Outcomes in Type 2 Diabetes (FIDELIO-DKD)",
        "journal": "The New England Journal of Medicine (NEJM)",
        "doi": "10.1056/NEJMoa2025845",
        "year": "2020",
        "abstract": (
            "BACKGROUND: Finerenone, a selective nonsteroidal mineralocorticoid receptor antagonist (MRA), has demonstrated anti-inflammatory and antifibrotic effects "
            "in preclinical models. Its renal and cardiovascular protective outcomes in patients with CKD and type 2 diabetes were evaluated in a randomized phase 3 trial.\n\n"
            "METHODS: In this double-blind trial, 5,734 patients with chronic kidney disease (urinary albumin-to-creatinine ratio [UACR] 30 to 5000 mg/g and eGFR 25 to 75 mL/min/1.73m2) "
            "treated with maximum tolerated doses of renin-angiotensin system (RAS) inhibitors were randomly assigned to receive finerenone or placebo. "
            "The primary composite outcome was kidney failure, a sustained decrease of at least 40% in eGFR from baseline, or death from renal causes. "
            "The key secondary composite outcome was death from cardiovascular causes, nonfatal myocardial infarction, nonfatal stroke, or hospitalization for heart failure.\n\n"
            "RESULTS: Over a median follow-up of 2.6 years, a primary outcome event occurred in 504 of 2,833 patients (17.8%) in the finerenone group and in 600 of 2,841 (21.1%) in the placebo group "
            "(hazard ratio, 0.82; 95% CI, 0.73 to 0.93; P=0.001; NNT=29). The key secondary cardiovascular composite outcome occurred in 367 patients (13.0%) in the finerenone group and in 420 (14.8%) in the placebo group "
            "(hazard ratio, 0.86; 95% CI, 0.75 to 0.99; P=0.03). Hyperkalemia-related discontinuation occurred in 2.3% of finerenone patients vs. 0.9% of placebo patients, with no hyperkalemia-associated deaths."
        )
    }
]

GUIDELINES_DATA = [
    {
        "id": "gd-hfref",
        "specialty": "Cardiology",
        "society": "AHA / ACC / HFSA",
        "name": "Guideline-Directed Medical Therapy (GDMT) for Heart Failure with Reduced Ejection Fraction (HFrEF <= 40%)",
        "version": "2024 Clinical Update",
        "pillars": [
            {
                "drug_class": "ARNi (Sacubitril/Valsartan) or ACEi / ARB",
                "recommendation": "Class 1A",
                "starting_dose": "Sacubitril/Valsartan 24/26 mg or 49/51 mg PO BID",
                "target_dose": "97/103 mg PO BID",
                "pearls": "Requires 36-hour washout when switching from ACE inhibitors to avoid severe angioedema. Check potassium and renal function at 1-2 weeks."
            },
            {
                "drug_class": "Evidence-Based Beta-Blocker",
                "recommendation": "Class 1A",
                "starting_dose": "Carvedilol 3.125 mg BID, Metoprolol Succinate 12.5-25 mg daily, or Bisoprolol 1.25 mg daily",
                "target_dose": "Carvedilol 25-50 mg BID, Metoprolol Succinate 200 mg daily, Bisoprolol 10 mg daily",
                "pearls": "Initiate only when patient is euvolemic. Do NOT withdraw during mild acute decompensation; titrate upward every 2-4 weeks."
            },
            {
                "drug_class": "Mineralocorticoid Receptor Antagonist (MRA)",
                "recommendation": "Class 1A",
                "starting_dose": "Spironolactone 12.5-25 mg daily or Eplerenone 25 mg daily",
                "target_dose": "Spironolactone 25-50 mg daily, Eplerenone 50 mg daily",
                "pearls": "Contraindicated if baseline K+ > 5.0 mEq/L or eGFR < 30 mL/min/1.73m2. Monitor potassium at day 3, 7, and monthly for first 3 months."
            },
            {
                "drug_class": "SGLT2 Inhibitor (Dapagliflozin or Empagliflozin)",
                "recommendation": "Class 1A",
                "starting_dose": "Dapagliflozin 10 mg daily OR Empagliflozin 10 mg daily",
                "target_dose": "10 mg daily (no titration required)",
                "pearls": "Effective regardless of diabetic status. Can be initiated in patients with eGFR down to 20 mL/min/1.73m2. Minimal blood pressure lowering effect."
            }
        ],
        "device_therapy": "ICD indicated for primary prevention if LVEF <= 35% after >= 3 months of optimal GDMT with NYHA Class II-III symptoms. CRT-D indicated if LVEF <= 35%, sinus rhythm, LBBB with QRS >= 150 ms."
    },
    {
        "id": "gd-kdigo-ckd",
        "specialty": "Nephrology",
        "society": "KDIGO (Kidney Disease: Improving Global Outcomes)",
        "name": "Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease",
        "version": "2024 Practice Guideline",
        "pillars": [
            {
                "drug_class": "RAS Blockade (ACEi or ARB)",
                "recommendation": "Grade 1A for CKD with UACR > 300 mg/g; Grade 2B for UACR 30-300 mg/g",
                "starting_dose": "Titrate to maximum approved or tolerated dose",
                "target_dose": "Max tolerated dose",
                "pearls": "Up to 30% increase in serum creatinine within 4 weeks of initiation is expected and acceptable hemodynamically; do NOT discontinue unless creatinine rise > 30% or refractory hyperkalemia."
            },
            {
                "drug_class": "SGLT2 Inhibitors",
                "recommendation": "Grade 1A",
                "starting_dose": "Dapagliflozin 10 mg or Empagliflozin 10 mg daily",
                "target_dose": "10 mg daily",
                "pearls": "Initiate in patients with eGFR 20-60 mL/min/1.73m2 or UACR >= 200 mg/g. Once initiated, continue until renal replacement therapy is required."
            },
            {
                "drug_class": "Nonsteroidal MRA (Finerenone)",
                "recommendation": "Grade 1A for T2DM with eGFR > 25 and UACR > 30 mg/g",
                "starting_dose": "10 mg daily if eGFR 25-59; 20 mg daily if eGFR >= 60",
                "target_dose": "20 mg daily",
                "pearls": "Significantly reduces albuminuria and slows CKD progression with lower hyperkalemia risk than spironolactone. Baseline K+ must be <= 4.8 mEq/L."
            },
            {
                "drug_class": "Blood Pressure Target",
                "recommendation": "Grade 1B",
                "starting_dose": "Target systolic blood pressure < 120 mmHg standardized",
                "target_dose": "< 120 mmHg SBP",
                "pearls": "Using standardized office BP measurement to attenuate both cardiovascular events and progressive loss of kidney function."
            }
        ],
        "device_therapy": "Referral to multidisciplinary nephrology care when eGFR < 30 mL/min/1.73m2 (CKD Stage G4/G5) or rapid progression (>5 mL/min/year)."
    },
    {
        "id": "gd-sepsis",
        "specialty": "Critical Care / Infectious Disease",
        "society": "Surviving Sepsis Campaign (SSC)",
        "name": "International Guidelines for Management of Sepsis and Septic Shock",
        "version": "2026 Consensus Guidelines",
        "pillars": [
            {
                "drug_class": "Initial Resuscitation Bundle (Hour-1)",
                "recommendation": "Best Practice Statement",
                "starting_dose": "Crystalloid fluid at 30 mL/kg within first 3 hours for sepsis-induced hypoperfusion or lactate >= 4 mmol/L",
                "target_dose": "Dynamic hemodynamic measures (stroke volume variation, passive leg raise, bedside echo)",
                "pearls": "Use balanced crystalloids (Plasma-Lyte or Lactated Ringer's) over normal saline to prevent hyperchloremic metabolic acidosis and acute renal injury."
            },
            {
                "drug_class": "Vasopressor Therapy in Septic Shock",
                "recommendation": "Grade 1A",
                "starting_dose": "Norepinephrine as first-line agent, titrating to MAP >= 65 mmHg",
                "target_dose": "Add Vasopressin at fixed 0.03 units/min if norepinephrine escalating > 0.25 mcg/kg/min",
                "pearls": "Add Epinephrine as third-line agent. Add IV Hydrocortisone (200 mg/day as 50 mg IV q6h or continuous infusion) if vasopressor requirement persists >= 4 hours."
            },
            {
                "drug_class": "Antimicrobial Administration",
                "recommendation": "Grade 1A",
                "starting_dose": "Administer broad-spectrum IV antimicrobials immediately, ideally within 1 hour of recognition",
                "target_dose": "Tailor to suspected source, local antibiogram, and prior colonization",
                "pearls": "Obtain blood cultures prior to antibiotics only if it does not delay antimicrobial start by >45 minutes. Daily de-escalation assessment based on procalcitonin and cultures."
            }
        ],
        "device_therapy": "Place arterial catheter as soon as practical in patients requiring vasopressors. Use lung-protective mechanical ventilation (tidal volume 6 mL/kg predicted body weight, plateau pressure < 30 cm H2O) if ARDS develops."
    },
    {
        "id": "gd-copd",
        "specialty": "Pulmonology",
        "society": "Global Initiative for Chronic Obstructive Lung Disease (GOLD)",
        "name": "Global Strategy for Diagnosis, Management, and Prevention of COPD",
        "version": "2026 Strategy Report",
        "pillars": [
            {
                "drug_class": "Initial Pharmacotherapy for Stable COPD (Group A, B, E Classification)",
                "recommendation": "Evidence Level A",
                "starting_dose": "Group E (Exacerbation history >= 2 or >= 1 hospitalization): Initial therapy with LABA + LAMA combination",
                "target_dose": "Dual long-acting bronchodilator (e.g., Tiotropium/Olodaterol, Umeclidinium/Vilanterol)",
                "pearls": "LABA/LAMA is superior to LABA/ICS in preventing exacerbations and improves FEV1 and dyspnea scores without pneumonia risk."
            },
            {
                "drug_class": "Inhaled Corticosteroids (Triple Therapy: LABA + LAMA + ICS)",
                "recommendation": "Evidence Level A",
                "starting_dose": "Add ICS if blood eosinophils >= 300 cells/uL or >= 100 cells/uL with >= 2 moderate exacerbations/year",
                "target_dose": "Single-inhaler triple therapy (e.g., Fluticasone furoate/Umeclidinium/Vilanterol)",
                "pearls": "ICS is NOT recommended if blood eosinophils < 100 cells/uL or history of recurrent severe mycobacterial or fungal pneumonias."
            },
            {
                "drug_class": "Management of Acute Exacerbations",
                "recommendation": "Evidence Level A",
                "starting_dose": "Oral Prednisone 40 mg daily for 5 days + Short-acting bronchodilator (SABA/SAMA)",
                "target_dose": "5-day corticosteroid course (longer duration conveys no additional benefit and increases adverse events)",
                "pearls": "Antibiotics indicated if patient has all 3 cardinal symptoms: increased dyspnea, sputum volume, and sputum purulence (or purulence + 1 other)."
            }
        ],
        "device_therapy": "Non-invasive positive pressure ventilation (NIV/BiPAP) is the first-line ventilatory support in acute hypercapnic respiratory failure (pH < 7.35 and PaCO2 > 45 mmHg), reducing intubation rate by 65%."
    }
]
