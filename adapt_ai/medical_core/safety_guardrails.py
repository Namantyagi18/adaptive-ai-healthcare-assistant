"""Clinical Safety Guardrails and Emergency Triage System.

Enforces strict clinical boundaries:
1. Immediate detection of life-threatening emergency warning signs:
   - Acute Coronary Syndrome / Heart Attack (crushing chest pain, radiating pain, diaphoresis)
   - Stroke / Acute Cerebrovascular Event (FAST protocol, unilateral numbness, slurred speech)
   - Severe Airway Obstruction & Respiratory Distress (stridor, cyanosis, gasping)
   - Severe Anaphylaxis (rapid lip/tongue/throat swelling, allergic airway collapse)
   - Severe Sepsis & Septic Shock (mottled skin, confusion with rigors, non-blanching rash)
   - Pediatric Red Flags (infant fever under 3 months, cyanosis, prolonged seizures > 5 min, unresponsiveness)
   - Mental Health Crisis & Self-Harm (suicidal ideation, intent, lethal means)
2. Support for English, Indian English, and Hinglish symptom descriptions.
3. Configurable country-specific emergency guidance (India 112/108 & Tele-MANAS 14416, US 911/988, UK 999/111).
4. Safe differentiation between active emergency symptoms and purely educational / conceptual questions.
5. Multi-pattern detection for prescription and definitive diagnosis demands preventing phrasing bypass.
6. Detection of adversarial jailbreak and safety-override attempts.

Important Clinical Notice:
Automated keyword and rule-based screening identifies potential life-threatening warning signs
to trigger rapid clinical referral. It NEVER diagnoses diseases, recommends personalized medication
regimens, or replaces direct in-person evaluation by licensed medical professionals.
"""

import re
from typing import Tuple, Optional, List, Dict, Any
from adapt_ai.config import settings
from adapt_ai.models.schemas import TriageLevel


class SafetyGuardrails:
    """Pre-inference and post-inference clinical safety and emergency triage engine."""

    # Verified emergency contact reference data
    EMERGENCY_CONTACTS: Dict[str, Dict[str, str]] = {
        "IN": {
            "country_name": "India",
            "emergency_number": "112 (National Emergency Helpline) or 108 (Ambulance)",
            "ambulance": "108",
            "maternal_infant": "102",
            "suicide_helplines": "Tele-MANAS at 14416 or 1800-891-4416 (24/7 toll-free), or KIRAN at 1800-599-0019",
            "hospital_dept": "nearest hospital Emergency Department / Casualty"
        },
        "US": {
            "country_name": "United States",
            "emergency_number": "911",
            "suicide_helplines": "988 (Suicide & Crisis Lifeline - call or text 24/7)",
            "hospital_dept": "nearest hospital Emergency Department"
        },
        "GB": {
            "country_name": "United Kingdom",
            "emergency_number": "999",
            "suicide_helplines": "111 (NHS mental health services) or 116 123 (Samaritans)",
            "hospital_dept": "nearest hospital A&E (Accident & Emergency)"
        },
        "CA": {
            "country_name": "Canada",
            "emergency_number": "911",
            "suicide_helplines": "988 (Suicide Crisis Helpline)",
            "hospital_dept": "nearest hospital Emergency Department"
        },
        "AU": {
            "country_name": "Australia",
            "emergency_number": "000",
            "suicide_helplines": "13 11 14 (Lifeline)",
            "hospital_dept": "nearest hospital Emergency Department"
        }
    }

    # Life-threatening emergency symptom patterns (English, Indian English, Hinglish, Spanish, French)
    EMERGENCY_PATTERNS = [
        # 1. Acute Coronary Syndrome / Heart Attack
        (
            re.compile(
                r'\b(?:'
                r'chest pain|crushing chest|chest pressure|chest tightness|chest heaviness|squeezing chest|'
                r'heart attack|myocardial infarction|infarto|douleur thoracique|dolor (?:en|de) el pecho|'
                r'(?:seene|chhati) mein (?:[a-z]+ ){0,3}(?:dard|dabav|jalan|bhari|pressure)|'
                r'dil ka daura|heart attack aa raha|'
                r'pain radiating to (?:left arm|bayen hath|jaw|neck|back)|'
                r'chest pain with (?:cold sweat|shortness of breath|sweating|vomiting)|'
                r'sinking feeling in (?:my )?chest'
                r')\b',
                re.IGNORECASE
            ),
            "Potential Acute Coronary Syndrome / Heart Attack warning signs detected."
        ),
        # 2. Stroke / FAST Protocol
        (
            re.compile(
                r'\b(?:'
                r'slurred speech|face drooping|facial droop|facial numbness|arm weakness|arm drift|'
                r'sudden numbness|sudden weakness|one side paralyzed|hemiplegia|stroke|apoplejía|'
                r'derrame cerebral|avc|lakwa|falij|chehra tedha|muh tedha|bol nahi pa rah[aei]|'
                r'awaaz ladkhada|zuban ladkhada|ek taraf ka sharir sunn|ek side kamzor|'
                r'haath utha nahi pa rah[aei]|sudden inability to speak|sudden loss of vision|'
                r'thunderclap headache'
                r')\b',
                re.IGNORECASE
            ),
            "Time-critical acute stroke symptoms (FAST protocol) detected."
        ),
        # 3. Anaphylaxis (Severe Allergic Reaction - Checked before general dyspnea)
        (
            re.compile(
                r'\b(?:'
                r'anaphylaxis|anaphylactic shock|severe allergic reaction|'
                r'throat (?:is |are )?(?:rapidly )?swelling|swelling (?:of )?(?:the )?(?:throat|lips|tongue)|'
                r'throat closing up|tongue (?:is )?swelling|swollen tongue and throat|'
                r'swollen lips and (?:throat|tongue)|garganta hinchada|gala soojh gaya|'
                r'jeebh soojh gayi|hoth soojh gaye|allergy se gala band|'
                r'gale mein sujan aur saans'
                r')\b',
                re.IGNORECASE
            ),
            "Acute anaphylaxis or severe allergic reaction warning signs detected."
        ),
        # 4. Acute Airway Obstruction & Severe Breathing Difficulties
        (
            re.compile(
                r'\b(?:'
                r'can(?:\'t| not| barely) breathe|trouble breathing|difficulty breathing|'
                r'struggling (?:for breath|to breathe)|gasping for (?:air|breath)|'
                r'severe breathlessness|acute asthma attack|choking|étouffement|'
                r'dificultad para respirar|falta de aire|saans nahi aa rahi|'
                r'saans lene mein (?:bohot |bahut )?takleef|saans phool rahi|dam ghut raha|'
                r'gala ghut raha|saans atak rahi|lips turning blue|turning blue|'
                r'intercostal retractions|stridor'
                r')\b',
                re.IGNORECASE
            ),
            "Acute airway compromise or severe respiratory distress warning signs detected."
        ),
        # 5. Severe Sepsis / Septic Shock
        (
            re.compile(
                r'\b(?:'
                r'septic shock|sepsis|mottled skin|clammy skin and confusion|'
                r'uncontrollable shivering with (?:high )?fever|confusion and high fever|'
                r'non-blanching rash|purple spots not fading|glass tumbler test rash|'
                r'tez bukhar ke sath behoshi|shareer thanda pad gaya bukhar mein|'
                r'neele ya baingani nishan shareer par|rigors with confusion'
                r')\b',
                re.IGNORECASE
            ),
            "Potential severe sepsis or septic shock warning signs detected."
        ),
        # 6. Severe Pediatric Red Flags
        (
            re.compile(
                r'\b(?:'
                r'baby (?:not breathing|turning blue|unresponsive|limp|floppy|grunting)|'
                r'(?:infant|baby|child|newborn).*(?:unresponsive|limp|floppy|not breathing|turning blue)|'
                r'infant (?:under 3 months|fever 38|seizure|convulsion)|'
                r'(?:infant|newborn).*(?:fever of 38|fever (?:above|>|>=) ?38)|'
                r'child (?:not breathing|turning blue|unresponsive)|'
                r'(?:child|infant|pediatric) seizure lasting (?:more than 5 minutes|> ?5 min)|'
                r'convulsion lasting (?:more than 5 minutes|> ?5 min)|'
                r'bulging fontanelle|severe chest indrawing|'
                r'bachha saans nahi le raha|bachha neela pad raha|bachha behosh|'
                r'chhota bachha jag nahi raha|bachha floppy ho gaya|'
                r'bachhe ko (?:continuous |lagaatar )?daura'
                r')\b',
                re.IGNORECASE
            ),
            "High-risk pediatric emergency warning signs detected."
        ),
        # 7. Suicidal Ideation / Mental Health Crisis
        (
            re.compile(
                r'\b(?:'
                r'kill myself|want to die|commit suicide|end my life|end it all|'
                r'suicidal ideation|suicidal thoughts|slit (?:my )?wrists|'
                r'overdose on (?:pills|medication|drugs)|suicidio|suicide|'
                r'khudkushi|aatmahatya|marne ka man kar raha|jaan dena chahta|'
                r'jeena nahi chahta|zindagi khatam karna|khud ko nuksan|zeher kha liya'
                r')\b',
                re.IGNORECASE
            ),
            "Mental health crisis / self-harm emergency detected."
        )
    ]

    # Attempts to demand definitive prescription drugs, dosages, or scripts
    PRESCRIPTION_PATTERNS = [
        re.compile(
            r'\b(?:prescribe|write (?:me )?(?:a )?script|prescription (?:for|de do|banao|likho))\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\b(?:what (?:is|are)?|what\'s|suggest|calculate|recommend|give me|tell me) (?:the )?(?:exact |correct |right )?(?:dose|dosage|amount|mg|milligrams?|tablets?|pills?|drops?|injections?)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\bhow (?:many|much) (?:mg|milligrams?|tablets?|pills?|drops?|doses?)(?: of [a-z0-9\-]+)? (?:should|can|do|must) (?:i|we|my [a-z]+) (?:take|give|swallow|use|inject|drink)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\b(?:which|what) (?:antibiotic|medicine|medication|drug|pill|syrup) (?:should|can) (?:i|we) (?:take|buy|use) for\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\b(?:kitni|kitna) (?:goli|tablets?|dose|dawa|dawahi) (?:khani|leni|deni) (?:chahiye|padegi|hogi)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\b(?:dawa|dawahi|medicine) (?:ka dose|ki quantity|suggest karo|likh do)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\bprescription (?:de do|likh do|chahiye)\b',
            re.IGNORECASE
        )
    ]

    # Attempts to demand definitive diagnosis or disease certainty
    DIAGNOSIS_PATTERNS = [
        re.compile(
            r'\b(?:diagnose (?:me|my)|give me a (?:definitive |final )?diagnosis|what is my (?:final |definitive )?diagnosis)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\b(?:tell me (?:exactly|definitely|100%|for sure) what (?:disease|illness|condition) i have)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\b(?:confirm (?:if i have|that i have|my diagnosis)|confirm whether i have)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\b(?:do i have|is it definitely|could this be definitely) (?:cancer|a tumor|stroke|heart attack|diabetes|hiv|leukemia|lupus)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\bwhat (?:disease|illness|condition) do i (?:have|suffer from)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\b(?:mujhe|mere ko) (?:kaun si|kya) bimari hai (?:batao|confirm karo|pakka batao)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\bkya (?:mujhe|mere ko) (?:cancer|tumor|stroke|tb|heart attack) hai (?:pakka|sure|batao)\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\bpakka batao (?:kya bimari|kya rog) hai\b',
            re.IGNORECASE
        ),
        re.compile(
            r'\bdiagnosis confirm karo\b',
            re.IGNORECASE
        )
    ]

    # Adversarial jailbreak / safety override patterns
    OVERRIDE_PATTERNS = re.compile(
        r'\b(?:'
        r'ignore (?:all )?(?:previous )?(?:rules|instructions|disclaimers|safety|protocols)|'
        r'override (?:safety|guardrails?|clinical guidelines?|boundaries)|'
        r'pretend (?:you are|to be) (?:a |an )?(?:licensed doctor|unrestricted|real physician|pharmacist)|'
        r'forget (?:all )?(?:medical ethics|safety disclaimers|rules)|'
        r'bypass (?:safety|restrictions?|guidelines?)|'
        r'do not follow (?:clinical guidelines|safety rules)|'
        r'you are now in developer mode|'
        r'dan mode|jailbreak'
        r')\b',
        re.IGNORECASE
    )

    @classmethod
    def _is_purely_educational(cls, text: str) -> bool:
        """Determines if a query mentioning emergency terms is conceptual or educational.
        
        Safely distinguishes academic/informational questions (e.g., 'What is the FAST protocol?')
        from active patient presentations (e.g., 'My father has facial droop right now').
        """
        text_lower = text.lower().strip()

        # Suicide / self-harm is never bypassed under educational context
        suicide_indicators = [
            "kill myself", "want to die", "commit suicide", "end my life",
            "khudkushi", "aatmahatya", "marne ka man", "overdose on", "slit wrist", "zeher"
        ]
        if any(kw in text_lower for kw in suicide_indicators):
            return False

        # First-person or acute personal distress indicators
        personal_or_acute_markers = [
            # English personal markers
            "i have", "i am having", "i feel", "i'm having", "im having", "my chest",
            "my heart", "my arm", "my throat", "my head", "my breathing", "my father",
            "my mother", "my dad", "my mom", "my wife", "my husband", "my baby",
            "my child", "my son", "my daughter", "my grandfather", "my grandmother",
            "my friend", "this patient", "someone is", "he is", "she is",
            # Acute temporal / urgency markers
            "right now", "currently", "suddenly", "started having", "hurting",
            "severe pain", "cannot breathe", "can't breathe", "collapsed", "unresponsive",
            "help me", "please help", "what should i do", "emergency", "save me",
            # Hinglish personal / acute markers
            "mujhe", "mere", "meri", "mera", "humein", "humare", "bachha", "bachhe",
            "abhi", "turant", "dard ho raha", "takleef ho rahi", "saans nahi",
            "soojh gaya", "neela pad", "behosh"
        ]
        if any(marker in text_lower for marker in personal_or_acute_markers):
            return False

        # Educational question patterns
        educational_starters = [
            "what is the fast protocol",
            "what does fast stand for",
            "what is the difference between",
            "what are the causes of",
            "what causes",
            "causes of",
            "what are the symptoms of",
            "what is the definition of",
            "definition of",
            "define",
            "explain the difference",
            "explain the pathophysiology",
            "explain the mechanism",
            "explain how",
            "how do doctors",
            "how is",
            "how does",
            "guidelines for",
            "what are the guidelines",
            "risk factors for",
            "what are the risk factors",
            "overview of",
            "statistics on",
            "history of",
            "tell me about the history",
            # Hinglish educational patterns
            "kya hota hai",
            "kise kehte hain",
            "ke lakshan kya hote hain",
            "ke lakshan kya hain",
            "ke karan kya hain",
            "ka matlab kya hai"
        ]

        return any(pattern in text_lower for pattern in educational_starters)

    @classmethod
    def evaluate_emergency(
        cls,
        user_text: str,
        country_code: Optional[str] = None
    ) -> Tuple[bool, Optional[str], Optional[TriageLevel]]:
        """Scans input for life-threatening medical emergencies with country-specific routing."""
        # 1. Distinguish purely educational questions to avoid false emergency alerts
        if cls._is_purely_educational(user_text):
            return False, None, None

        # Resolve country code from parameter
        target_country = (country_code or "").strip().upper()

        for pattern, reason in cls.EMERGENCY_PATTERNS:
            if pattern.search(user_text):
                is_mental_health = ("self-harm" in reason or "suicid" in reason or "mental health" in reason.lower())
                
                # Format country-specific guidance
                guidance_msg = cls._format_emergency_guidance(
                    reason=reason,
                    is_mental_health=is_mental_health,
                    country_code=target_country
                )
                return True, guidance_msg, TriageLevel.EMERGENCY_IMMEDIATE

        return False, None, None

    @classmethod
    def _format_emergency_guidance(
        cls,
        reason: str,
        is_mental_health: bool,
        country_code: str
    ) -> str:
        """Constructs verified emergency response instructions based on user jurisdiction."""
        disclaimer = (
            "\n[CLINICAL BOUNDARY NOTICE: Automated screening detects potential emergency warning signs "
            "and does not constitute a clinical diagnosis. Immediate evaluation by healthcare professionals is required.]"
        )

        if country_code == "IN":
            contacts = cls.EMERGENCY_CONTACTS["IN"]
            if is_mental_health:
                return (
                    "If you or someone you know is going through a crisis or having thoughts of self-harm, "
                    "please know that compassionate, confidential support is available right now.\n"
                    f"In India, reach out immediately to {contacts['suicide_helplines']}, "
                    f"or proceed directly to your {contacts['hospital_dept']}."
                    + disclaimer
                )
            return (
                f"CRITICAL MEDICAL ALERT: {reason}\n"
                "This requires IMMEDIATE EMERGENCY MEDICAL ATTENTION.\n"
                f"In India, immediately call {contacts['emergency_number']}, "
                f"or proceed directly to the {contacts['hospital_dept']}.\n"
                "Do not drive yourself if you are alone."
                + disclaimer
            )

        if country_code == "US":
            contacts = cls.EMERGENCY_CONTACTS["US"]
            if is_mental_health:
                return (
                    "If you or someone you know is struggling or in crisis, help is available right now. "
                    f"Call or text {contacts['suicide_helplines']}, "
                    f"or proceed immediately to your {contacts['hospital_dept']}."
                    + disclaimer
                )
            return (
                f"CRITICAL MEDICAL ALERT: {reason}\n"
                "This requires IMMEDIATE EMERGENCY MEDICAL ATTENTION.\n"
                f"Please call {contacts['emergency_number']} immediately "
                f"or proceed to the {contacts['hospital_dept']}."
                + disclaimer
            )

        if country_code in ("GB", "UK"):
            contacts = cls.EMERGENCY_CONTACTS["GB"]
            if is_mental_health:
                return (
                    "If you or someone you know is in distress or experiencing a mental health crisis, support is available. "
                    f"In the UK, call {contacts['suicide_helplines']}, "
                    f"or proceed immediately to your {contacts['hospital_dept']}."
                    + disclaimer
                )
            return (
                f"CRITICAL MEDICAL ALERT: {reason}\n"
                "This requires IMMEDIATE EMERGENCY MEDICAL ATTENTION.\n"
                f"In the UK, immediately call {contacts['emergency_number']} "
                f"or proceed to the {contacts['hospital_dept']}."
                + disclaimer
            )

        # Multi-region / International standard guidance (default fallback)
        if is_mental_health:
            return (
                "If you or someone you know is struggling, in crisis, or having thoughts of self-harm, help is available right now:\n"
                "- In India: Call Tele-MANAS at 14416 or 1800-891-4416 (24/7 toll-free), or KIRAN at 1800-599-0019.\n"
                "- In the United States and Canada: Call or text 988 (Suicide & Crisis Lifeline).\n"
                "- In the UK: Call 111 (NHS) or 116 123 (Samaritans).\n"
                "- In other countries: Contact your local emergency services (such as 112) or the nearest hospital crisis center."
                + disclaimer
            )

        return (
            f"CRITICAL MEDICAL ALERT: {reason}\n"
            "This requires IMMEDIATE EMERGENCY MEDICAL ATTENTION.\n"
            "Please call your local emergency services immediately: "
            "112 or 108 in India, 911 in the US/Canada, 999 in the UK, or 112 in Europe, "
            "or proceed immediately to the nearest hospital Emergency Department (A&E/Casualty)."
            + disclaimer
        )

    @classmethod
    def detect_safety_override(cls, user_text: str) -> bool:
        """Detects malicious or adversarial attempts to disable safety guardrails."""
        return bool(cls.OVERRIDE_PATTERNS.search(user_text))

    @classmethod
    def detect_prescription_or_diagnostic_demand(cls, user_text: str) -> Tuple[bool, Optional[str]]:
        """Identifies requests for prescribing drugs or definitive diagnoses in English & Hinglish."""
        # 1. Prescription demands
        for pat in cls.PRESCRIPTION_PATTERNS:
            if pat.search(user_text):
                return (
                    True,
                    "ADAPT-AI cannot prescribe medications, issue medical prescriptions, or calculate individualized drug dosages. "
                    "Medication selection, dosing, and administration require licensed clinical evaluation, organ function review (e.g. renal and hepatic clearance), and contraindication screening."
                )

        # 2. Definitive diagnosis demands
        for pat in cls.DIAGNOSIS_PATTERNS:
            if pat.search(user_text):
                return (
                    True,
                    "ADAPT-AI cannot definitively diagnose medical conditions from self-reported symptoms or descriptions alone. "
                    "Accurate clinical diagnosis requires an in-person physical examination, objective diagnostic testing (such as blood tests and imaging), and comprehensive clinical evaluation by a licensed healthcare professional."
                )

        return False, None

    @classmethod
    def classify_triage_level(cls, user_text: str, is_emergency: bool = False) -> TriageLevel:
        """Determines clinical triage tier based on symptom severity keywords in English and Hinglish."""
        if is_emergency:
            return TriageLevel.EMERGENCY_IMMEDIATE

        text_lower = user_text.lower()

        # Urgent care indicators (English & Hinglish)
        urgent_keywords = [
            # English
            "high fever", "vomiting blood", "severe pain", "dehydration", "asthma attack",
            "blood in stool", "blood in urine", "can't keep fluids down", "swollen joint",
            "burn", "deep cut", "head injury", "severe abdominal pain", "acute pain",
            # Hinglish
            "tez bukhar", "khoon ki ulti", "bohot tez dard", "bahut tez dard",
            "pakhane mein khoon", "pet mein tez dard", "chakkar aur ulti"
        ]
        if any(kw in text_lower for kw in urgent_keywords):
            return TriageLevel.URGENT_CARE

        # Ambiguous / uncertain indicators
        ambiguous_keywords = [
            # English
            "feel weird", "unwell", "dizzy sometimes", "tired lately", "strange feeling",
            "body hurts", "something wrong", "feeling off", "not feeling good",
            # Hinglish
            "ajeeb lag raha", "theek nahi lag raha", "chakkar aa rahe", "sust lag raha"
        ]
        if any(kw in text_lower for kw in ambiguous_keywords) and len(user_text.split()) < 10:
            return TriageLevel.UNCERTAIN_AMBIGUOUS

        # Routine clinical vs Self-care education
        routine_keywords = [
            # English
            "rash", "mild headache", "chronic", "blood pressure", "diabetes check",
            "back pain", "screening", "cholesterol", "knee pain", "routine checkup",
            # Hinglish
            "khujli", "halka sar dard", "purana dard", "sugar check", "bp check"
        ]
        if any(kw in text_lower for kw in routine_keywords):
            return TriageLevel.ROUTINE_CLINICAL

        return TriageLevel.SELF_CARE_EDUCATION
