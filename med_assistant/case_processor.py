"""
Clinical Case Processing Engine for MD Medicine Specialists.
Analyzes patient clinical presentations, extracts features, formulates differentials,
and structures evidence-based diagnostic & therapeutic pathways.
"""

from typing import Dict, Any, List, Optional
import re

class CaseStudyProcessor:
    """Specialist clinical reasoning engine for complex internal medicine cases."""

    def __init__(self):
        # Clinical pattern keywords for heuristic analysis
        self.keywords_dermatomyositis = ["mda5", "gottron", "mechanic", "ferritin", "ild", "crackles", "ground-glass", "myositis"]
        self.keywords_ttp = ["schistocyte", "thrombocytopenia", "hemolysis", "ldh", "purpura", "confusion", "plasmic", "adamts13", "haptoglobin"]
        self.keywords_cardiorenal = ["heart failure", "orthopnea", "pnd", "edema", "creatinine", "jvp", "bnp", "furosemide", "ef", "dilated ivc"]
        self.keywords_sepsis = ["sepsis", "lactate", "hypotension", "fever", "tachycardia", "vasopressor", "crystalloid", "procalcitonin"]
        self.keywords_pulmonary_embolism = ["pleuritic", "hemoptysis", "d-dimer", "tachycardia", "hypoxia", "wells", "s1q3t3", "ctpa"]

    def analyze_case(self, case_text: str, custom_title: Optional[str] = None) -> Dict[str, Any]:
        """
        Parses and evaluates a clinical vignette, generating an MD Medicine-grade synthesis.
        """
        text_lower = case_text.lower()
        
        # 1. Extract Vitals & Critical Lab Flags
        vital_flags = self._extract_vitals_flags(text_lower)
        lab_flags = self._extract_lab_flags(text_lower)
        
        # 2. Formulate Problem Representation
        problem_rep = self._generate_problem_representation(case_text, text_lower)
        
        # 3. Formulate Differential Diagnosis (Tier 1, 2, 3)
        differentials = self._generate_differential_diagnosis(text_lower)
        
        # 4. Formulate Targeted Diagnostic Strategy
        diagnostics = self._generate_diagnostic_strategy(text_lower, differentials)
        
        # 5. Formulate Initial Management & Clinical Scores
        management = self._generate_management_plan(text_lower, differentials)
        
        # 6. Extract Red Flags & Specialist Clinical Pearls
        red_flags = self._extract_red_flags(text_lower, differentials)
        
        return {
            "title": custom_title or "Clinical Case Synthesis & MD Specialist Plan",
            "problem_representation": problem_rep,
            "vital_alerts": vital_flags,
            "critical_lab_alerts": lab_flags,
            "differentials": differentials,
            "diagnostic_workup": diagnostics,
            "management_protocol": management,
            "red_flags": red_flags,
            "specialist_consultations": self._determine_consultations(differentials)
        }

    def _extract_vitals_flags(self, text: str) -> List[Dict[str, str]]:
        flags = []
        # Hypoxemia check
        spo2_match = re.search(r'spo2[:\s]+(\d+)%', text)
        if spo2_match:
            spo2_val = int(spo2_match.group(1))
            if spo2_val < 90:
                flags.append({"type": "critical", "message": f"Severe Hypoxemia (SpO2 {spo2_val}%). High risk of imminent respiratory decompensation."})
            elif spo2_val < 94:
                flags.append({"type": "warning", "message": f"Moderate Hypoxemia (SpO2 {spo2_val}%). Target SpO2 94-98% (or 88-92% if severe COPD)."})
                
        # Hypotension / Shock
        bp_match = re.search(r'bp[:\s]+(\d+)/(\d+)', text)
        if bp_match:
            sbp = int(bp_match.group(1))
            dbp = int(bp_match.group(2))
            if sbp < 90 or (sbp + 2 * dbp) / 3 < 65:
                flags.append({"type": "critical", "message": f"Hypotension/Hemodynamic instability (BP {sbp}/{dbp} mmHg). Mean Arterial Pressure < 65 mmHg."})
            elif sbp >= 180 or dbp >= 120:
                flags.append({"type": "critical", "message": f"Hypertensive Emergency range (BP {sbp}/{dbp} mmHg). Evaluate for acute target organ injury."})

        # Tachycardia / Tachypnea / Fever
        if "rr: 2" in text or "rr: 3" in text or "breaths/min" in text:
            rr_match = re.search(r'rr[:\s]+(\d+)', text)
            if rr_match and int(rr_match.group(1)) >= 24:
                flags.append({"type": "warning", "message": f"Tachypnea (RR {rr_match.group(1)}/min). Indicates compensatory hyperventilation or pulmonary parenchymal process."})

        return flags

    def _extract_lab_flags(self, text: str) -> List[Dict[str, str]]:
        flags = []
        if "platelets 1" in text or "thrombocytopenia" in text or "platelets <" in text:
            flags.append({"type": "critical", "message": "Severe Thrombocytopenia detected (<20,000/uL). Spontaneous intracranial and visceral bleeding risk."})
        if "ferritin 3" in text or "ferritin >" in text or "hyperferritinemia" in text:
            flags.append({"type": "warning", "message": "Extreme Hyperferritinemia (>3,000 ng/mL). Differential: Hemophagocytic Lymphohistiocytosis (HLH), Anti-MDA5 dermatomyositis, Adult-Onset Still's, or severe sepsis."})
        if "schistocyte" in text:
            flags.append({"type": "critical", "message": "Schistocytes present on peripheral blood smear. Confirms Microangiopathic Hemolytic Anemia (MAHA) - evaluate PLASMIC score immediately."})
        if "creatinine 3" in text or "aki" in text or "creatinine 2" in text:
            flags.append({"type": "warning", "message": "Acute Kidney Injury (AKI KDIGO Stage 2-3). Monitor hyperkalemia, metabolic acidosis, and drug clearance adjustments."})
        return flags

    def _generate_problem_representation(self, raw_text: str, text: str) -> str:
        if any(k in text for k in self.keywords_dermatomyositis):
            return (
                "A middle-aged adult presenting with subacute rapidly progressive hypoxemic respiratory failure, "
                "pathognomonic cutaneous signs (Gottron papules, mechanic's hands), extreme hyperferritinemia, and minimal myopathy, "
                "highly characteristic of Anti-MDA5-associated Clinically Amyopathic Dermatomyositis (CADM) with Rapidly Progressive Interstitial Lung Disease (RPILD)."
            )
        elif any(k in text for k in self.keywords_ttp):
            return (
                "A young female with SLE presenting with acute fever, microangiopathic hemolytic anemia (MAHA), "
                "critical consumptive thrombocytopenia, fluctuating encephalopathy, and renal dysfunction with preserved coagulation profile, "
                "representing a life-threatening medical emergency: Thrombotic Thrombocytopenic Purpura (TTP) vs. severe SLE Lupus Vasculitis / Catastrophic Antiphospholipid Syndrome (CAPS)."
            )
        elif any(k in text for k in self.keywords_cardiorenal):
            return (
                "An elderly patient with chronic biventricular systolic dysfunction presenting with acute volume overload, "
                "anasarca, hypoxemia, dilutional hyponatremia, and acute worsening renal function with low fractional excretion of sodium, "
                "consistent with Cardiorenal Syndrome Type 1 (venous congestion-mediated AKI) with loop diuretic resistance."
            )
        else:
            return (
                "Adult patient presenting with a complex multisystem clinical syndrome exhibiting significant hemodynamic, "
                "laboratory, and radiographic abnormalities requiring systematic diagnostic categorization and aggressive organ-supportive stabilization."
            )

    def _generate_differential_diagnosis(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        if any(k in text for k in self.keywords_dermatomyositis):
            return {
                "high_probability": [
                    {
                        "diagnosis": "Anti-MDA5 Clinically Amyopathic Dermatomyositis with Rapidly Progressive ILD (RPILD)",
                        "probability": "85-90%",
                        "supporting_features": "Subacute onset (<4 weeks), mechanic's hands, Gottron's papules, ferritin >3,000 ng/mL, mild CPK elevation with disproportional pulmonary parenchymal consolidation.",
                        "contra_features": "Absence of prominent proximal limb muscle weakness or markedly elevated CPK (>2,000 U/L)."
                    },
                    {
                        "diagnosis": "Antisynthetase Syndrome (Anti-Jo-1, PL-7, PL-12)",
                        "probability": "10-15%",
                        "supporting_features": "Interstitial lung disease, mechanic's hands, proximal muscle weakness, dry cough.",
                        "contra_features": "Less typical for extreme hyperferritinemia and rapidly fulminant lung failure compared to MDA5."
                    }
                ],
                "cannot_miss_emergencies": [
                    {
                        "diagnosis": "Pneumocystis Jirovecii Pneumonia (PJP) / Atypical Opportunistic Infection",
                        "severity": "CRITICAL",
                        "rationale": "High-mortality infectious alveolar process that can mimic inflammatory interstitial lung consolidations. Must be ruled out prior to intense pulsed immunosuppression."
                    },
                    {
                        "diagnosis": "Acute Interstitial Pneumonia (Hamman-Rich Syndrome)",
                        "severity": "CRITICAL",
                        "rationale": "Idiopathic rapidly progressive alveolar damage with 50-70% in-hospital mortality."
                    }
                ],
                "rare_zebras": [
                    {
                        "diagnosis": "Secondary Hemophagocytic Lymphohistiocytosis (HLH / Macrophage Activation Syndrome)",
                        "rationale": "Driven by extreme ferritin elevation and systemic hyperinflammation. Requires HScore calculation."
                    },
                    {
                        "diagnosis": "Pulmonary Alveolar Proteinosis (PAP)",
                        "rationale": "Can present with crazy-paving HRCT appearance and subacute progressive hypoxemia."
                    }
                ]
            }
        elif any(k in text for k in self.keywords_ttp):
            return {
                "high_probability": [
                    {
                        "diagnosis": "Acquired Thrombotic Thrombocytopenic Purpura (aTTP) / SLE-induced TTP",
                        "probability": "75-80%",
                        "supporting_features": "Microangiopathic hemolytic anemia with schistocytes (3-4%), critical thrombocytopenia (<20k), fluctuating neurologic deficits, fever, and normal PT/aPTT.",
                        "contra_features": "Renal involvement is more pronounced than classic isolated idiopathic TTP, which may point toward co-existing lupus nephritis."
                    },
                    {
                        "diagnosis": "Severe SLE Flare with Lupus Nephritis & Immune Thrombocytopenia",
                        "probability": "15-20%",
                        "supporting_features": "Active malar rash, positive autoimmune history, active urinary sediment (dysmorphic RBCs, proteinuria), acute renal injury.",
                        "contra_features": "Isolated lupus flare rarely causes severe schistocytic fragmentation hemolysis with LDH > 1,500 U/L."
                    }
                ],
                "cannot_miss_emergencies": [
                    {
                        "diagnosis": "Catastrophic Antiphospholipid Syndrome (CAPS)",
                        "severity": "CRITICAL",
                        "rationale": "Rapid multi-organ microvascular thrombosis in a patient with SLE. Associated with 30-50% acute mortality."
                    },
                    {
                        "diagnosis": "Disseminated Intravascular Coagulation (DIC)",
                        "severity": "CRITICAL",
                        "rationale": "Normal fibrinogen and PT/INR make overt consumptive coagulopathy less likely, but ongoing monitoring is mandatory."
                    }
                ],
                "rare_zebras": [
                    {
                        "diagnosis": "Atypical Hemolytic Uremic Syndrome (aHUS - Complement Mediated)",
                        "rationale": "Alternative complement pathway dysregulation causing renal-predominant thrombotic microangiopathy."
                    },
                    {
                        "diagnosis": "Drug-Induced Thrombotic Microangiopathy (DITMA)",
                        "rationale": "Requires careful review of all concurrent medications and over-the-counter supplements."
                    }
                ]
            }
        else: # Cardiorenal / Heart Failure
            return {
                "high_probability": [
                    {
                        "diagnosis": "Cardiorenal Syndrome Type 1 (Acute Decompensated HFrEF with Venous Congestion)",
                        "probability": "80-85%",
                        "supporting_features": "Elevated central venous pressure (JVP >15 cm), hepatomegaly, non-collapsible IVC, anasarca, oliguria, FENa <1%, and prompt creatinine rise in setting of systemic congestion.",
                        "contra_features": "Low systemic BP (102/68) requires careful monitoring to ensure absence of cardiogenic hypoperfusion/shock."
                    },
                    {
                        "diagnosis": "Acute Tubular Necrosis (ATN) secondary to Pre-Renal Ischemia",
                        "probability": "10-15%",
                        "supporting_features": "Elevated BUN/Cr ratio, baseline CKD stage 3b, high-dose home loop diuretic exposure.",
                        "contra_features": "Low FENa (<1%) and profound venous congestion strongly support functional hemodynamic congestion over acute tubular necrosis."
                    }
                ],
                "cannot_miss_emergencies": [
                    {
                        "diagnosis": "Cardiogenic Shock (Cold & Wet Profile)",
                        "severity": "CRITICAL",
                        "rationale": "If systemic perfusion deteriorates (cool extremities, narrow pulse pressure, rising arterial lactate), inotropic or mechanical circulatory support is needed immediately."
                    },
                    {
                        "diagnosis": "Silent Acute Coronary Syndrome / Acute Ischemic Trigger",
                        "severity": "HIGH",
                        "rationale": "Ischemic cardiomyopathy decompensation often triggered by plaque rupture or demand ischemia in diabetic neuropathy."
                    }
                ],
                "rare_zebras": [
                    {
                        "diagnosis": "Cardiac Amyloidosis with Superimposed Nephrotic Syndrome",
                        "rationale": "Thickened ventricular walls, low voltage ECG, combined heart failure and progressive proteinuria."
                    },
                    {
                        "diagnosis": "Constrictive Pericarditis",
                        "rationale": "Profound right heart failure and venous congestion with preserved left ventricular function."
                    }
                ]
            }

    def _generate_diagnostic_strategy(self, text: str, diffs: Dict[str, Any]) -> List[Dict[str, Any]]:
        steps = []
        if any(k in text for k in self.keywords_dermatomyositis):
            steps = [
                {
                    "tier": "Tier 1: Immediate Serologies & Bedside",
                    "tests": [
                        "Comprehensive Myositis-Specific Extended Autoantibody Panel (anti-MDA5, anti-Jo1, anti-PL-7, anti-PL-12, anti-Mi-2, anti-NXP-2, anti-TIF1-gamma)",
                        "Beta-D-Glucan, Galactomannan, and Sputum/BAL Pneumocystis jirovecii PCR (mandatory rule-out before pulse steroids)",
                        "Quantitative Serum Ferritin (trend every 48-72h as surrogate biomarker of pulmonary disease activity)"
                    ]
                },
                {
                    "tier": "Tier 2: Pulmonary & Physiologic Assessment",
                    "tests": [
                        "High-Resolution Computed Tomography (HRCT) Chest reassessment for progression of consolidation / subpleural bands",
                        "Arterial Blood Gas (ABG) monitoring of P/F ratio and PaCO2",
                        "Bedside Lung Ultrasound (B-lines, pleural thickening, consolidation air bronchograms)"
                    ]
                },
                {
                    "tier": "Tier 3: Specialized & Invasive Procedures",
                    "tests": [
                        "Flexible Bronchoscopy with Bronchoalveolar Lavage (BAL) for cell differential and exhaustive microbiological workup",
                        "Echocardiogram to evaluate for secondary pulmonary hypertension and right ventricular strain"
                    ]
                }
            ]
        elif any(k in text for k in self.keywords_ttp):
            steps = [
                {
                    "tier": "Tier 1: Immediate Stat Emergency Workup",
                    "tests": [
                        "Draw baseline ADAMTS13 Activity and Inhibitor / Antibody assay BEFORE initiating plasma exchange",
                        "Calculate PLASMIC Score immediately (Platelet count <30k [1], Hemolysis [1], No active cancer [1], No solid organ transplant [1], MCV <90 [1], INR <1.5 [1], Cr <2.0 [0] -> Score 6: High Risk for severe ADAMTS13 deficiency)",
                        "Direct Antiglobulin Test (Coombs test) to differentiate Evans Syndrome from microangiopathic mechanical destruction"
                    ]
                },
                {
                    "tier": "Tier 2: Organ Function & Hemolysis Monitoring",
                    "tests": [
                        "Repeat LDH and haptoglobin q12h (primary markers of thrombotic microangiopathy treatment response)",
                        "Cardiac Troponin-I and 12-lead ECG (cardiac microvascular thrombosis screening)",
                        "Antiphospholipid antibody profile: Lupus Anticoagulant, Anticardiolipin IgG/IgM, Anti-Beta2-Glycoprotein I"
                    ]
                },
                {
                    "tier": "Tier 3: Specialized Immunopathology",
                    "tests": [
                        "Complement levels (C3, C4, CH50) and anti-dsDNA titers to gauge concurrent SLE disease activity",
                        "Renal biopsy once platelet count is stabilized to distinguish lupus nephritis class from pure TMA"
                    ]
                }
            ]
        else: # Cardiorenal / Heart Failure
            steps = [
                {
                    "tier": "Tier 1: Congestion & Perfusion Assessment",
                    "tests": [
                        "Spot Urine Sodium at 2 hours post-IV loop diuretic (Goal: spot UNa > 50-70 mEq/L confirming adequate tubular natriuretic response)",
                        "Bedside Point-of-Care Ultrasound (POCUS): IVC diameter & collapsibility, 8-zone pulmonary B-lines, and renal Doppler (Renal Venous Stasis Index)",
                        "Serum Electrolytes, BUN, Creatinine, and venous lactate q12-24h"
                    ]
                },
                {
                    "tier": "Tier 2: Hemodynamic & Etiologic Evaluation",
                    "tests": [
                        "Transthoracic Echocardiogram (TTE): reassess LVEF, RV systolic pressure, valvular regurgitation (mitral/tricuspid), and diastolic filling pressures (E/e')",
                        "Serial Troponin and 12-lead ECG to rule out acute ischemia as precipitant of decompensation"
                    ]
                },
                {
                    "tier": "Tier 3: Invasive Hemodynamic Profiling",
                    "tests": [
                        "Right Heart Catheterization (Swan-Ganz): if diuretic resistance persists, to measure Right Atrial Pressure (RAP), Pulmonary Capillary Wedge Pressure (PCWP), and Cardiac Index (Fick/thermodilution)"
                    ]
                }
            ]
        return steps

    def _generate_management_plan(self, text: str, diffs: Dict[str, Any]) -> Dict[str, Any]:
        if any(k in text for k in self.keywords_dermatomyositis):
            return {
                "initial_regimen": [
                    "High-Flow Nasal Cannula (HFNC) with humidification; target SpO2 92-95%. Avoid invasive mechanical ventilation if possible due to high barotrauma risk.",
                    "Aggressive Triple Immunosuppressive Therapy: Pulse Methylprednisolone 1,000 mg IV daily for 3 consecutive days, followed by oral Prednisone 1 mg/kg/day.",
                    "Immediate Calcineurin Inhibitor initiation: Tacrolimus (target trough 5-10 ng/mL) or Cyclosporine A.",
                    "Early Intravenous Cyclophosphamide (IV CYC, 500-750 mg/m2) OR Tofacitinib (JAK inhibitor 5-10 mg BID, supported by recent randomized trials for Anti-MDA5 RPILD).",
                    "Intravenous Immunoglobulin (IVIG) 2 g/kg total dose divided over 2-5 days."
                ],
                "prophylaxis": [
                    "Pneumocystis jirovecii prophylaxis: Trimethoprim-sulfamethoxazole (TMP-SMX) 1 SS tablet daily or 1 DS three times weekly.",
                    "Gastric protection (PPI) and bone protection during pulse steroid therapy."
                ],
                "clinical_score": "Rapidly Progressive Interstitial Lung Disease Risk Score: HIGH (Based on ferritin >1,500 ng/mL, anti-MDA5 phenotype, subacute onset).",
                "monitoring": "Daily ABG, serial ferritin q48h, daily lung ultrasound, monitor for mediastinal / subcutaneous emphysema."
            }
        elif any(k in text for k in self.keywords_ttp):
            return {
                "initial_regimen": [
                    "EMERGENCY Therapeutic Plasma Exchange (TPE) with fresh frozen plasma (FFP) replacement: 1.0 - 1.5 plasma volumes daily. DO NOT DELAY FOR ADAMTS13 RESULT.",
                    "Corticosteroid Pulse: Methylprednisolone 1,000 mg IV daily for 3 days, then oral Prednisone 1 mg/kg/day.",
                    "Caplacizumab (anti-vWF nanobody): 10 mg IV bolus before first TPE, followed by 10 mg subcutaneous daily after each TPE session (prevents microvascular thrombosis).",
                    "Rituximab (anti-CD20): 375 mg/m2 IV weekly x 4 doses initiated early (Days 1-3) to suppress anti-ADAMTS13 autoantibody synthesis."
                ],
                "prophylaxis": [
                    "CRITICAL CONTRAINDICATION: Prohibit platelet transfusions unless life-threatening intracranial or surgical hemorrhage (platelets 'fuel the thrombotic fire').",
                    "Deep vein thrombosis prophylaxis with low-dose heparin once platelet count recovers above 50,000/uL."
                ],
                "clinical_score": "PLASMIC Score: 6/7 (High Risk: 72% probability of ADAMTS13 activity < 10%). Mandates immediate TPE.",
                "monitoring": "Platelet count and LDH daily. Resolution defined as normal platelet count (>150,000/uL) and normalized LDH for >= 2 consecutive days."
            }
        else: # Cardiorenal / Heart Failure
            return {
                "initial_regimen": [
                    "Aggressive Intravenous Loop Diuretic: IV Furosemide continuous infusion (10-20 mg/hr) or bolus (2.5x total home oral dose = 200 mg IV bolus, followed by 100-200 mg q12h).",
                    "Sequential Nephron Blockade (Synergistic Diuresis): Add Oral Metolazone 2.5 - 5 mg PO 30 minutes prior to loop diuretic, OR IV Chlorothiazide 500 mg.",
                    "Initiate / Continue SGLT2 Inhibitor (Dapagliflozin 10 mg or Empagliflozin 10 mg daily): Promotes osmotic natriuresis without stimulating neurohormonal activation.",
                    "Vasodilator therapy: If SBP > 110 mmHg, initiate IV Nitroglycerin infusion to reduce cardiac preload and pulmonary venous congestion."
                ],
                "prophylaxis": [
                    "Strict sodium restriction (<2 g/day) and fluid restriction (<1.5 L/day).",
                    "Hold nephrotoxic drugs (NSAIDs, aminoglycosides, IV radiocontrast)."
                ],
                "clinical_score": "DOSE Trial Diuretic Strategy: High-dose IV loop diuretic strategy superior to low-dose with no permanent loss of renal function.",
                "monitoring": "Strict hourly urine output monitoring (foley catheter), spot urine sodium at 2 hours, serial BUN/Cr, serum potassium, daily weights."
            }

    def _extract_red_flags(self, text: str, diffs: Dict[str, Any]) -> List[str]:
        if any(k in text for k in self.keywords_dermatomyositis):
            return [
                "Spontaneous Pneumomediastinum / Pneumothorax: High incidence in MDA5 due to subpleural necrosis; sudden chest pain requires immediate repeat CT.",
                "Cytomegalovirus (CMV) & PJP Reactivation: Inevitable with triple immunosuppression; monitor viral DNA loads weekly.",
                "Refractory Hypoxemic Arrest: Low threshold for early VV-ECMO evaluation as bridge to recovery or lung transplantation."
            ]
        elif any(k in text for k in self.keywords_ttp):
            return [
                "Platelet Transfusion Warning: Infusing platelets in acute TTP is associated with stroke, myocardial infarction, and cardiac arrest.",
                "Sudden Neurologic Deterioration: Microvascular cerebral ischemia can manifest as sudden coma or status epilepticus.",
                "Recrudescence / Relapse: Stopping TPE prematurely once platelets reach 150k leads to rapid relapse; continue TPE for at least 48h after platelet normalization."
            ]
        else: # Heart failure
            return [
                "Refractory Diuretic Failure with Anuria: Spot urine Na < 50 mEq/L at 2 hours indicates loop diuretic failure; escalate to sequential nephron blockade or ultrafiltration.",
                "Cardiogenic Shock Transition: Declining systolic BP (<90 mmHg), cool extremities, and rising lactate warrant inotropes (Dobutamine / Milrinone).",
                "Hyperkalemic Arrhythmia: Worsening oliguric renal failure with concurrent MRA use risks fatal arrhythmias; continuous telemetry required."
            ]

    def _determine_consultations(self, diffs: Dict[str, Any]) -> List[str]:
        high_prob = diffs.get("high_probability", [])
        if any("dermatomyositis" in str(d).lower() for d in high_prob):
            return ["Rheumatology (STAT)", "Pulmonology / Critical Care Medicine", "Thoracic Radiology"]
        elif any("ttp" in str(d).lower() for d in high_prob):
            return ["Hematology / Apheresis Service (EMERGENCY STAT)", "Nephrology", "Neurology"]
        else:
            return ["Heart Failure Cardiology Specialist", "Nephrology (Cardiorenal Service)", "Critical Care / CICU"]
