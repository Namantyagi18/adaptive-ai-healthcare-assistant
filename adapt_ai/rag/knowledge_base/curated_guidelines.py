"""Curated authoritative medical guideline corpus for ADAPT-AI RAG knowledge base.

Covers all 12 clinical specialty and safety categories based on guidelines from
WHO, CDC, NICE, USPSTF, ACC/AHA, and ADA.
"""

from typing import List
from adapt_ai.models.schemas import IngestionItem


CURATED_MEDICAL_GUIDELINES: List[IngestionItem] = [
    # 1. Common Symptoms
    IngestionItem(
        title="NICE Guideline: Assessment and Initial Management of Fever in Adults and Children",
        source="NICE (National Institute for Health and Care Excellence)",
        category="Common Symptoms",
        content=(
            "Fever is defined as a body temperature of 38.0 C (100.4 F) or higher. "
            "In adults, most acute fevers are self-limiting viral illnesses requiring rest, oral hydration, "
            "and antipyretics like paracetamol or ibuprofen for symptomatic relief. "
            "Warning signs requiring immediate medical evaluation include stiff neck, non-blanching purpuric rash, "
            "new confusion, shortness of breath, severe focal abdominal pain, or fever persisting beyond 3 days. "
            "In infants under 3 months, any temperature of 38.0 C or above is considered a medical emergency "
            "warranting urgent hospital evaluation to rule out serious bacterial infection."
        ),
        version="2024.1",
        url="https://www.nice.org.uk/guidance/ng143"
    ),
    IngestionItem(
        title="CDC Clinical Guidance: Evaluation of Acute Cough and Bronchitis",
        source="CDC (Centers for Disease Control and Prevention)",
        category="Common Symptoms",
        content=(
            "Acute cough lasting less than 3 weeks is most commonly caused by viral upper respiratory tract infections. "
            "Routine antibiotic prescribing for uncomplicated acute bronchitis in healthy adults is not recommended, "
            "as greater than 90% of cases are viral and antibiotics do not shorten disease duration. "
            "Supportive care includes honey (for individuals over 1 year of age), adequate hydration, and humidified air. "
            "Red flag symptoms warranting urgent clinical evaluation include hemoptysis (coughing up blood), "
            "stridor, severe dyspnea, resting pulse > 100 bpm, oxygen saturation < 95%, or focal consolidation on lung exam."
        ),
        version="2023.2",
        url="https://www.cdc.gov/antibiotic-use/bronchitis.html"
    ),

    # 2. Infectious Diseases
    IngestionItem(
        title="CDC & WHO Guidelines: Influenza Diagnosis and Antiviral Indications",
        source="CDC / WHO",
        category="Infectious Diseases",
        content=(
            "Influenza presents acutely with high fever, myalgias, headache, non-productive cough, and severe malaise. "
            "Antiviral treatment with neuraminidase inhibitors (e.g., oseltamivir) provides the greatest clinical benefit "
            "when initiated within 48 hours of symptom onset. "
            "Antiviral therapy is strongly recommended regardless of duration for hospitalized patients, individuals with severe, "
            "complicated, or progressive illness, and high-risk groups including adults aged 65+, pregnant women, "
            "and individuals with chronic cardiopulmonary, metabolic, or immunosuppressive conditions."
        ),
        version="2024.1",
        url="https://www.cdc.gov/flu/professionals/antivirals/"
    ),
    IngestionItem(
        title="WHO Consolidated Guidelines on Tuberculosis: Clinical Presentation and Diagnostic Testing",
        source="WHO (World Health Organization)",
        category="Infectious Diseases",
        content=(
            "Pulmonary tuberculosis (TB) characteristically presents with a persistent cough lasting 3 weeks or longer, "
            "drenching night sweats, unexplained weight loss, hemoptysis, and low-grade evening fevers. "
            "Prompt diagnostic evaluation includes rapid molecular testing (Xpert MTB/RIF) and sputum acid-fast bacilli smear/culture. "
            "Patients with suspected active TB should be evaluated in negative-pressure respiratory isolation where feasible. "
            "Standard first-line curative therapy consists of a 6-month regimen: rifampicin, isoniazid, pyrazinamide, and ethambutol."
        ),
        version="2024.2",
        url="https://www.who.int/publications/i/item/9789240058767"
    ),

    # 3. Cancer-Related Questions
    IngestionItem(
        title="USPSTF Breast Cancer and Colorectal Cancer Screening Recommendations",
        source="USPSTF (US Preventive Services Task Force)",
        category="Cancer Screening",
        content=(
            "The USPSTF recommends biennial screening mammography for women aged 40 to 74 years at average risk of breast cancer. "
            "For colorectal cancer, the USPSTF recommends routine screening for all adults starting at age 45 and continuing to age 75. "
            "Recommended screening strategies include high-sensitivity colonoscopy every 10 years, annual fecal immunochemical testing (FIT), "
            "or stool DNA-FIT test every 3 years. "
            "Any positive non-invasive stool test requires a prompt diagnostic colonoscopy to evaluate for precancerous polyps or malignancy."
        ),
        version="2024.1",
        url="https://www.uspreventiveservicestaskforce.org"
    ),
    IngestionItem(
        title="NICE Clinical Guideline: Suspected Cancer Recognition and Referral Red Flags",
        source="NICE",
        category="Cancer Red Flags",
        content=(
            "Key 'red flag' clinical presentations warranting urgent 2-week cancer referral include: "
            "unexplained palpable breast lump in adults; persistent hoarseness or dysphagia lasting > 3 weeks; "
            "unexplained iron deficiency anemia; painless hematuria (blood in urine); persistent change in bowel habit; "
            "new or rapidly changing pigmented skin lesions following the ABCDE rule (Asymmetry, Border, Color, Diameter > 6mm, Evolution); "
            "and drenching 'B-symptoms' (fever, night sweats, > 10% unintentional body weight loss in 6 months)."
        ),
        version="2023.3",
        url="https://www.nice.org.uk/guidance/ng12"
    ),

    # 4. Blood Disorders
    IngestionItem(
        title="ASH Guidelines: Investigation and Management of Iron Deficiency Anemia",
        source="ASH (American Society of Hematology)",
        category="Blood Disorders",
        content=(
            "Iron deficiency anemia is characterized by low hemoglobin, low MCV (microcytosis < 80 fL), and serum ferritin < 30 ng/mL. "
            "Clinical symptoms include fatigue, exertional pallor, cold intolerance, pica (ice chewing), and restless legs syndrome. "
            "In adult men and postmenopausal women, iron deficiency anemia is considered gastrointestinal bleeding until proven otherwise, "
            "mandating endoscopic investigation (esophagogastroduodenoscopy and colonoscopy). "
            "First-line treatment is oral ferrous sulfate, gluconate, or fumarate, or intravenous iron if oral is poorly tolerated or malabsorbed."
        ),
        version="2023.1",
        url="https://www.hematology.org"
    ),

    # 5. Cardiovascular & Respiratory
    IngestionItem(
        title="ACC/AHA Guideline for the Prevention, Detection, and Management of High Blood Pressure",
        source="ACC / AHA (American College of Cardiology / American Heart Association)",
        category="Cardiovascular",
        content=(
            "Blood pressure is categorized into Normal (<120/<80 mmHg), Elevated (120-129/<80 mmHg), "
            "Stage 1 Hypertension (130-139 / 80-89 mmHg), and Stage 2 Hypertension (>= 140 / >= 90 mmHg). "
            "First-line non-pharmacological interventions include DASH diet, sodium reduction (<1500-2300 mg/day), regular aerobic exercise, "
            "and moderation of alcohol. "
            "First-line pharmacological classes include thiazide diuretics, calcium channel blockers (CCBs), ACE inhibitors, or ARBs. "
            "Hypertensive crisis (BP > 180/120 mmHg) with symptoms of acute end-organ damage (chest pain, shortness of breath, blurry vision, "
            "severe headache) is a life-threatening medical emergency requiring immediate emergency department care."
        ),
        version="2024.1",
        url="https://www.acc.org/guidelines"
    ),
    IngestionItem(
        title="GINA Global Strategy for Asthma Management and Prevention",
        source="GINA (Global Initiative for Asthma)",
        category="Respiratory",
        content=(
            "Asthma is a chronic inflammatory disorder characterized by variable expiratory airflow limitation and respiratory symptoms "
            "(wheeze, shortness of breath, chest tightness, and dry cough). "
            "GINA fundamental safety principle: treatment with short-acting beta-agonists (SABA) alone without inhaled corticosteroids (ICS) "
            "is strongly contraindicated due to increased risk of severe exacerbations and asthma-related death. "
            "First-line controller therapy involves low-dose inhaled corticosteroid-formoterol as both maintenance and reliever. "
            "Emergency asthma attack signs include silent chest, inability to speak full sentences, cyanosis, and peak flow < 50% predicted."
        ),
        version="2024.1",
        url="https://ginasthma.org"
    ),

    # 6. Diabetes and Chronic Conditions
    IngestionItem(
        title="ADA Standards of Medical Care in Diabetes: Diagnosis and Glycemic Targets",
        source="ADA (American Diabetes Association)",
        category="Endocrine & Diabetes",
        content=(
            "Diagnostic criteria for diabetes mellitus include: fasting plasma glucose >= 126 mg/dL (7.0 mmol/L), "
            "or 2-hour 75g oral glucose tolerance test >= 200 mg/dL, or glycated hemoglobin (HbA1c) >= 6.5% (48 mmol/mol), "
            "or random plasma glucose >= 200 mg/dL accompanied by classic hyperglycemic symptoms (polyuria, polydipsia, weight loss). "
            "For most non-pregnant adults, the standard glycemic target is HbA1c < 7.0% (< 53 mmol/mol). "
            "Metformin represents standard initial monotherapy combined with comprehensive lifestyle modification. "
            "Warning sign: Diabetic Ketoacidosis (DKA) presents with nausea, vomiting, abdominal pain, Kussmaul respirations, fruity breath, "
            "and requires emergent emergency medical care and intravenous fluid resuscitation."
        ),
        version="2024.1",
        url="https://diabetesjournals.org/care"
    ),

    # 7. Children's and Women's Health
    IngestionItem(
        title="AAP Guideline: Management of Febrile Seizures in Pediatric Patients",
        source="AAP (American Academy of Pediatrics)",
        category="Pediatric Health",
        content=(
            "Simple febrile seizures occur in children aged 6 to 60 months in the setting of fever > 38.0 C, "
            "are generalized tonic-clonic, last under 15 minutes, and do not recur within 24 hours. "
            "They do not cause permanent neurological deficit, brain damage, or intellectual impairment. "
            "During an acute seizure: place the child on their side (recovery position), do not place anything in the mouth, "
            "and time the seizure. "
            "Seek immediate emergency medical care if the seizure lasts longer than 5 minutes, if the child has difficulty breathing, "
            "or if the child does not regain alertness."
        ),
        version="2023.2",
        url="https://www.aap.org"
    ),
    IngestionItem(
        title="ACOG Practice Bulletin: Gestational Hypertension and Preeclampsia",
        source="ACOG (American College of Obstetricians and Gynecologists)",
        category="Women's Health",
        content=(
            "Preeclampsia is diagnosed when systolic BP >= 140 mmHg or diastolic BP >= 90 mmHg on two occasions after 20 weeks gestation "
            "in a previously normotensive woman, accompanied by proteinuria (>300 mg/24 hr or protein/creatinine ratio >= 0.3) "
            "or evidence of maternal organ dysfunction (thrombocytopenia, renal insufficiency, impaired liver function). "
            "Preeclampsia with severe features includes BP >= 160/110 mmHg, persistent severe headache unresponsive to medication, "
            "visual scotomata, or severe persistent right upper quadrant/epigastric pain. "
            "Severe features constitute an obstetric emergency requiring immediate hospital admission to prevent eclampsia and stroke."
        ),
        version="2024.1",
        url="https://www.acog.org"
    ),

    # 8. Medical Terminology and Report Explanations
    IngestionItem(
        title="Clinical Laboratory Reference Range Guide: CBC, Renal and Hepatic Panels",
        source="NHS & Mayo Clinic Laboratories",
        category="Medical Terminology & Diagnostics",
        content=(
            "Complete Blood Count (CBC) standard adult reference ranges: "
            "Hemoglobin: 13.8 - 17.2 g/dL (men), 12.1 - 15.1 g/dL (women). Low indicates anemia. "
            "White Blood Cell (WBC): 4,500 - 11,000 cells/mcL. Elevated (leukocytosis) often reflects bacterial infection or inflammation. "
            "Platelets: 150,000 - 450,000 /mcL. Low (thrombocytopenia) increases bleeding risk. "
            "Comprehensive Metabolic Panel: "
            "Serum Creatinine: 0.7 - 1.3 mg/dL. Elevated creatinine or estimated GFR (eGFR) < 60 mL/min/1.73m2 suggests renal impairment. "
            "Liver transaminases (ALT: 7-56 U/L, AST: 10-40 U/L): Marked elevation indicates hepatocellular injury or viral hepatitis."
        ),
        version="2024.1",
        url="https://www.nhs.uk/conditions/blood-tests/"
    ),

    # 9. Emergency Red Flag Conditions
    IngestionItem(
        title="AHA/ASA Stroke Guidelines: FAST Protocol and Time-Critical Thrombolysis",
        source="AHA / ASA (American Stroke Association)",
        category="Emergency Medicine",
        content=(
            "Acute ischemic stroke is a medical emergency where rapid identification saves brain tissue. "
            "Use the FAST protocol: "
            "F - Face Drooping (one side of face droops or is numb; ask to smile). "
            "A - Arm Weakness (one arm drifts downward when raised). "
            "S - Speech Difficulty (slurred speech, inability to repeat simple sentence). "
            "T - Time to call 911 / Emergency Services immediately. "
            "Intravenous thrombolysis (alteplase/tenecteplase) must be administered within a strict 4.5-hour window from last known well time. "
            "Do NOT give aspirin, food, or liquids before formal hospital dysphagia and imaging screening."
        ),
        version="2024.1",
        url="https://www.stroke.org"
    ),
    IngestionItem(
        title="AHA Emergency Cardiovascular Care: Acute Coronary Syndrome and Anaphylaxis",
        source="AHA / ERC Emergency Care",
        category="Emergency Medicine",
        content=(
            "Acute Coronary Syndrome (Myocardial Infarction / Heart Attack) presents with retrosternal pressure, fullness, squeezing, or pain "
            "lasting more than a few minutes, radiating to the jaw, neck, back, or left arm, accompanied by cold sweats, dyspnea, or lightheadedness. "
            "Immediate action: Call emergency medical services (911/999/112). "
            "Anaphylaxis is an acute, life-threatening systemic hypersensitivity reaction affecting airways, breathing, or circulation. "
            "Symptoms include stridor, wheeze, lip/tongue swelling, generalized urticaria, and hypotension. "
            "First-line definitive treatment is intramuscular epinephrine (adrenaline) injected immediately into the anterolateral mid-thigh."
        ),
        version="2024.1",
        url="https://cpr.heart.org"
    ),

    # 10. Evolving / Contradictory Clinical Evidence
    IngestionItem(
        title="USPSTF Guideline: Aspirin Use to Prevent Cardiovascular Disease in Adults",
        source="USPSTF",
        category="Contradictory & Evolving Evidence",
        content=(
            "For primary prevention of cardiovascular disease in adults aged 40 to 59 years with a 10% or greater 10-year CVD risk, "
            "the decision to initiate low-dose aspirin is individualized, as the net benefit is small. "
            "In adults aged 60 years or older, the USPSTF recommends against initiating low-dose aspirin for primary prevention "
            "because the increased risk of gastrointestinal and intracranial bleeding outweighs cardiovascular prevention benefits. "
            "In contrast, for secondary prevention (patients with established prior myocardial infarction or stroke), "
            "antiplatelet therapy remains strongly recommended."
        ),
        version="2023.1",
        url="https://www.uspreventiveservicestaskforce.org"
    ),
    IngestionItem(
        title="NICE Guideline on Hormone Replacement Therapy (HRT): Benefits and Risks",
        source="NICE",
        category="Contradictory & Evolving Evidence",
        content=(
            "HRT is highly effective for vasomotor menopausal symptoms (hot flushes, night sweats) and prevents osteoporosis. "
            "However, clinical evidence indicates contrasting risk profiles: combined estrogen-progestogen HRT is associated with a small "
            "increased risk of breast cancer and venous thromboembolism (VTE). "
            "Estrogen-only HRT (in women who have had a hysterectomy) carries little or no increased risk of breast cancer. "
            "Because benefits and risks vary significantly based on age, time since menopause, and individual cardiovascular risk factors, "
            "NICE guidelines state treatment must be individually tailored following shared clinical decision-making."
        ),
        version="2024.1",
        url="https://www.nice.org.uk/guidance/ng23"
    ),

    # 11. Multilingual Support Context (Spanish, French, Hindi)
    IngestionItem(
        title="Multilingual Clinical Triage Glossary: Spanish, French, Hindi Emergency Equivalents",
        source="WHO Multilingual Health Terminology",
        category="Multilingual Healthcare",
        content=(
            "Spanish health terminology: 'Dolor en el pecho' (chest pain), 'dificultad para respirar' (difficulty breathing), "
            "'derrame cerebral' (stroke), 'llame al servicio de emergencias' (call emergency services), 'azúcar alta en sangre' (high blood sugar). "
            "French health terminology: 'Douleur thoracique' (chest pain), 'essoufflement' (shortness of breath), "
            "'accident vasculaire cérébral / AVC' (stroke), 'appelez les urgences le 15 ou 112' (call emergency services). "
            "Hindi health terminology: 'Seene mein dard' (chest pain), 'saans lene mein takleef' (shortness of breath), "
            "'lakwa / stroke' (paralysis / stroke), 'turant emergency ambulance ko call karein' (call emergency ambulance immediately)."
        ),
        version="2024.1",
        url="https://www.who.int/terminology"
    ),

    # 12. Nutritional, Bone & Metabolic Health (Vitamin D Deficiency)
    IngestionItem(
        title="NICE & Endocrine Society Clinical Guidelines: Vitamin D Deficiency in Adults and Children",
        source="NICE / Endocrine Society",
        category="Endocrine & Metabolic",
        content=(
            "Vitamin D deficiency is defined biochemically by serum 25-hydroxyvitamin D [25(OH)D] levels: "
            "deficiency is typically < 25-30 nmol/L (< 10-12 ng/mL), insufficiency is 30-50 nmol/L (12-20 ng/mL), "
            "and sufficiency is > 50 nmol/L (> 20 ng/mL), with optimal skeletal levels between 75-125 nmol/L. "
            "Clinical symptoms of vitamin D deficiency in adults include chronic fatigue, general malaise, "
            "diffuse bone pain (notably in the lower back, hips, pelvis, and legs), arthralgias, and proximal muscle weakness "
            "(difficulty rising from a chair or climbing stairs, waddling gait). "
            "Severe prolonged deficiency causes osteomalacia in adults and rickets in children (bowed legs, cranial softening, "
            "growth delay, and hypocalcemia). "
            "First-line management for confirmed deficiency involves high-dose oral cholecalciferol (Vitamin D3) replacement "
            "(e.g., 50,000 IU weekly or daily equivalent for 6 to 8 weeks) followed by ongoing maintenance therapy "
            "(800 to 2000 IU daily), combined with adequate dietary calcium intake and sensible sunlight exposure. "
            "Toxicity risk: Excessive supplementation can cause hypercalcemia presenting with nausea, vomiting, confusion, "
            "polydipsia, polyuria, and renal calculi."
        ),
        version="2024.1",
        url="https://www.nice.org.uk/guidance/ng28"
    )
]

