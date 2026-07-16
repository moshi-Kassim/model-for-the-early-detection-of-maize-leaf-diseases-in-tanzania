"""User dashboard translations (English and Kiswahili)."""

from __future__ import annotations

LANGUAGES = {
    "en": "English",
    "sw": "Kiswahili",
}

TEXT = {
    "en": {
        "page_title": "Maize Leaf Care",
        "sidebar_title": "Maize Leaf Care",
        "sidebar_sub": "For farmers and field users",
        "language_label": "Language",
        "how_to_use_title": "How to use",
        "how_to_use_steps": (
            "1. Upload one or more clear maize leaf photos\n"
            "2. Wait for analysis\n"
            "3. Submit a help request if you need more advice\n"
            "4. View Community Help to see past requests and replies"
        ),
        "sidebar_note": "Only maize leaf images are accepted.",
        "user_banner": "User Portal — upload a leaf and view management advice only",
        "dashboard_title": "User Dashboard",
        "dashboard_subtitle": (
            "Upload maize leaf photos to see the detected disease and recommended management for each image."
        ),
        "upload_panel_title": "Upload leaf images",
        "upload_notice": (
            "Upload one or more clear photos of maize leaves. Only maize leaves are accepted."
        ),
        "upload_help": "Results appear automatically after upload. You can select multiple images.",
        "your_image": "Your image",
        "result_panel_title": "Diagnosis results",
        "empty_title": "No images uploaded yet",
        "empty_body": (
            "Upload one or more maize leaf photographs to receive a diagnosis "
            "and management advice for each image."
        ),
        "analyzing": "Analyzing your images...",
        "analyzing_one": "Analyzing image {current} of {total}...",
        "images_selected": "{count} image(s) selected",
        "result_for": "Result for",
        "reject_title": "Image not accepted",
        "top_prediction": "Top prediction",
        "detected_condition": "Detected condition",
        "confidence": "confidence",
        "recommended_management": "Recommended management",
        "nav_diagnose": "Diagnose",
        "nav_community": "Community Help",
        "help_request_title": "Need more help?",
        "help_request_subtitle": "Leave your phone number and comment so others can assist with education and advice.",
        "help_select_image": "Select diagnosed image",
        "help_phone_label": "Phone number",
        "help_comment_label": "Your comment or question",
        "help_comment_placeholder": "Describe your leaf problem or ask for advice...",
        "help_submit": "Submit help request",
        "help_phone_required": "Please enter your phone number.",
        "help_comment_required": "Please enter a comment or question.",
        "help_submit_success": "Your help request was submitted. Others can now view and reply.",
        "help_unknown_disease": "Unknown condition",
        "help_posted": "Posted",
        "help_replies": "Replies",
        "help_reply_action": "Reply to help this farmer",
        "help_reply_phone": "Your phone number",
        "help_reply_text": "Your reply",
        "help_reply_submit": "Send reply",
        "help_reply_success": "Reply posted successfully.",
        "help_admin_label": "Admin",
        "help_admin_reply_action": "Reply as admin",
        "help_admin_reply_success": "Admin reply posted.",
        "help_delete_post": "Delete request",
        "help_delete_reply": "Delete reply",
        "help_delete_success": "Deleted successfully.",
        "community_title": "Community Help History",
        "community_subtitle": "View past farmer requests and reply with advice or education.",
        "community_admin_title": "Community Help Requests",
        "community_admin_subtitle": "Review farmer help requests and post admin replies.",
        "community_empty_title": "No help requests yet",
        "community_empty_body": "When farmers submit questions after diagnosis, they will appear here.",
        "community_count": "{count} help request(s)",
    },
    "sw": {
        "page_title": "Kigundua Ugonjwa wa Majani ya Mahindi",
        "sidebar_title": "Kigundua Ugonjwa wa Mahindi",
        "sidebar_sub": "Kwa wakulima na watumiaji wa shambani",
        "language_label": "Lugha",
        "how_to_use_title": "Jinsi ya kutumia",
        "how_to_use_steps": (
            "1. Pakia picha moja au zaidi za majani ya mahindi\n"
            "2. Subiri uchambuzi\n"
            "3. Wasilisha ombi la msaada ikiwa unahitaji ushauri zaidi\n"
            "4. Tazama Msaada wa Jamii kuona maombi na majibu ya zamani"
        ),
        "sidebar_note": "Picha za majani ya mahindi pekee zinakubaliwa.",
        "user_banner": "Portal ya Mtumiaji — pakia jani na uone ushauri wa matibabu pekee",
        "dashboard_title": "Dashibodi ya Mtumiaji",
        "dashboard_subtitle": (
            "Pakia picha za majani ya mahindi kuona ugonjwa uliogunduliwa na ushauri wa matibabu kwa kila picha."
        ),
        "upload_panel_title": "Pakia picha za majani",
        "upload_notice": (
            "Pakia picha moja au zaidi za majani ya mahindi. Majani ya mahindi pekee yanakubaliwa."
        ),
        "upload_help": "Matokeo yanaonekana moja kwa moja baada ya kupakia. Unaweza kuchagua picha nyingi.",
        "your_image": "Picha yako",
        "result_panel_title": "Matokeo ya uchunguzi",
        "empty_title": "Hakuna picha zilizopakiwa bado",
        "empty_body": (
            "Pakia picha moja au zaidi za majani ya mahindi kupata uchunguzi "
            "na ushauri wa matibabu kwa kila picha."
        ),
        "analyzing": "Inachambua picha zako...",
        "analyzing_one": "Inachambua picha {current} kati ya {total}...",
        "images_selected": "Picha {count} zimechaguliwa",
        "result_for": "Matokeo ya",
        "reject_title": "Picha haikubaliwi",
        "top_prediction": "Utabiri wa juu",
        "detected_condition": "Hali iliyogunduliwa",
        "confidence": "uhakika",
        "recommended_management": "Ushauri wa matibabu",
        "nav_diagnose": "Chunguza",
        "nav_community": "Msaada wa Jamii",
        "help_request_title": "Unahitaji msaada zaidi?",
        "help_request_subtitle": "Acha nambari ya simu na maoni yako ili wengine waweze kusaidia kwa elimu na ushauri.",
        "help_select_image": "Chagua picha iliyochunguzwa",
        "help_phone_label": "Nambari ya simu",
        "help_comment_label": "Maoni au swali lako",
        "help_comment_placeholder": "Eleza tatizo la jani lako au uliza ushauri...",
        "help_submit": "Tuma ombi la msaada",
        "help_phone_required": "Tafadhali weka nambari ya simu.",
        "help_comment_required": "Tafadhali andika maoni au swali.",
        "help_submit_success": "Ombi lako la msaada limewasilishwa. Wengine wanaweza kuona na kujibu.",
        "help_unknown_disease": "Hali isiyojulikana",
        "help_posted": "Imechapishwa",
        "help_replies": "Majibu",
        "help_reply_action": "Jibu kumsaidia mkulima huyu",
        "help_reply_phone": "Nambari yako ya simu",
        "help_reply_text": "Jibu lako",
        "help_reply_submit": "Tuma jibu",
        "help_reply_success": "Jibu limewasilishwa.",
        "help_admin_label": "Msimamizi",
        "help_admin_reply_action": "Jibu kama msimamizi",
        "help_admin_reply_success": "Jibu la msimamizi limewasilishwa.",
        "help_delete_post": "Futa ombi",
        "help_delete_reply": "Futa jibu",
        "help_delete_success": "Imefutwa.",
        "community_title": "Historia ya Msaada wa Jamii",
        "community_subtitle": "Tazama maombi ya wakulima wa zamani na jibu kwa ushauri au elimu.",
        "community_admin_title": "Maombi ya Msaada wa Jamii",
        "community_admin_subtitle": "Kagua maombi ya wakulima na toa majibu ya msimamizi.",
        "community_empty_title": "Hakuna maombi ya msaada bado",
        "community_empty_body": "Wakulima wanapowasilisha maswali baada ya uchunguzi, yataonekana hapa.",
        "community_count": "Maombi {count} ya msaada",
    },
}

DISEASE_TEXT = {
    "en": {
        "Common_Rust": {
            "display_name": "Common Rust",
            "management": (
                "Plant resistant varieties, apply fungicides early, and remove infected debris."
            ),
        },
        "Blight": {
            "display_name": "Northern Leaf Blight",
            "management": (
                "Crop rotation, resistant hybrids, timely fungicide application at first sign."
            ),
        },
        "Healthy": {
            "display_name": "Healthy",
            "management": (
                "Continue good agronomic practices: balanced fertilization and field monitoring."
            ),
        },
        "Gray_Leaf_Spot": {
            "display_name": "Cercospora Leaf Spot",
            "management": (
                "Use tolerant varieties, rotate crops, and apply fungicides when needed."
            ),
        },
    },
    "sw": {
        "Common_Rust": {
            "display_name": "Rusi ya Kawaida",
            "management": (
                "Panda aina sugu, tumia dawa za kuua kuvu mapema, na ondoa mabaki yaliyoambukizwa."
            ),
        },
        "Blight": {
            "display_name": "Ugonjwa wa Madoa ya Kaskazini",
            "management": (
                "Badilisha mazao, tumia aina sugu, na tumia dawa za kuua kuvu mara moja unapoona dalili."
            ),
        },
        "Healthy": {
            "display_name": "Bichi / Haijaambukizwa",
            "management": (
                "Endelea na mazoea bora ya kilimo: mbolea sawa na ufuatiliaji wa shamba."
            ),
        },
        "Gray_Leaf_Spot": {
            "display_name": "Madoa ya Majani ya Cercospora",
            "management": (
                "Tumia aina zinazovumilia ugonjwa, badilisha mazao, na tumia dawa za kuua kuvu inapohitajika."
            ),
        },
    },
}

REJECTION_TEXT = {
    "en": {
        "other_plant": (
            "This image is from another plant, not a maize (corn) leaf. "
            "Leaves from mango, banana, sugarcane, sorghum, and other crops are not supported. "
            "Please upload a clear maize leaf photo."
        ),
        "symptom_mismatch": (
            "The model prediction does not match what is visible in the image. "
            "This may be a non-maize leaf (e.g. sugarcane or another crop). "
            "Please upload a clear maize leaf photo."
        ),
        "person": (
            "This image appears to contain a person or portrait. "
            "Please upload a clear photo of a maize (corn) leaf only."
        ),
        "fruit": (
            "This image looks like a fruit (e.g. mango, orange, banana), not a maize leaf. "
            "Please upload a maize (corn) leaf photo only."
        ),
        "non_maize_plant": (
            "This image appears to show fruit or a non-maize plant. "
            "This tool only accepts maize (corn) leaves."
        ),
        "object": (
            "This image appears to show an object, vehicle, or scene — not a plant leaf. "
            "Please upload a maize leaf photo."
        ),
        "not_maize_leaf": (
            "This does not look like a maize leaf. "
            "Upload a close-up photo of a single maize (corn) leaf with visible leaf tissue."
        ),
        "low_confidence": (
            "The model is not confident this is a maize leaf image. "
            "Please upload a clearer close-up of a maize leaf."
        ),
        "ambiguous": (
            "The image is ambiguous and may not be a maize leaf. "
            "Try a closer photo of one maize leaf against a plain background."
        ),
    },
    "sw": {
        "other_plant": (
            "Picha hii ni ya mmea mwingine, si jani la mahindi. "
            "Majani ya embe, ndizi, miwa, mtama na mazao mengine hayakubaliwi. "
            "Tafadhali pakia picha wazi ya jani la mahindi."
        ),
        "symptom_mismatch": (
            "Utabiri hauendani na kinachoonekana kwenye picha. "
            "Huenda hii si jani la mahindi (mf. miwa au zao lingine). "
            "Tafadhali pakia picha wazi ya jani la mahindi."
        ),
        "person": (
            "Picha hii inaonekana kuwa na mtu au picha ya uso. "
            "Tafadhali pakia picha wazi ya jani la mahindi pekee."
        ),
        "fruit": (
            "Picha hii inaonekana kuwa tunda (mf. embe, chungwa, ndizi), si jani la mahindi. "
            "Tafadhali pakia picha ya jani la mahindi pekee."
        ),
        "non_maize_plant": (
            "Picha hii inaonekana kuwa tunda au mmea usio mahindi. "
            "Chombo hiki kinakubali majani ya mahindi pekee."
        ),
        "object": (
            "Picha hii inaonekana kuwa kitu, gari, au mandhari — si jani la mmea. "
            "Tafadhali pakia picha ya jani la mahindi."
        ),
        "not_maize_leaf": (
            "Hii haionekani kama jani la mahindi. "
            "Pakia picha ya karibu ya jani moja la mahindi lenye tishu inayoonekana."
        ),
        "low_confidence": (
            "Mfumo hauko na uhakika kama hii ni picha ya jani la mahindi. "
            "Tafadhali pakia picha wazi zaidi ya jani la mahindi."
        ),
        "ambiguous": (
            "Picha hii si wazi na huenda si jani la mahindi. "
            "Jaribu picha ya karibu zaidi ya jani moja la mahindi kwenye mandharinyuma rahisi."
        ),
    },
}


def normalize_lang(lang: str | None) -> str:
    if lang in LANGUAGES:
        return lang
    return "en"


def t(key: str, lang: str, **kwargs) -> str:
    lang = normalize_lang(lang)
    text = TEXT[lang].get(key, TEXT["en"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text


def localize_disease(class_key: str, lang: str) -> dict[str, str]:
    lang = normalize_lang(lang)
    return DISEASE_TEXT[lang].get(class_key, DISEASE_TEXT["en"][class_key])


def translate_rejection(message: str, lang: str) -> str:
    lang = normalize_lang(lang)
    if lang == "en":
        return message.replace("**", "")

    lowered = message.lower()
    if "person or portrait" in lowered:
        key = "person"
    elif "looks like a fruit" in lowered:
        key = "fruit"
    elif "fruit or a non-maize plant" in lowered:
        key = "non_maize_plant"
    elif "object, vehicle, or scene" in lowered:
        key = "object"
    elif "does not look like a maize leaf" in lowered:
        key = "not_maize_leaf"
    elif "not confident this is a maize leaf" in lowered:
        key = "low_confidence"
    elif "ambiguous and may not be a maize leaf" in lowered:
        key = "ambiguous"
    elif "prediction does not match" in lowered:
        key = "symptom_mismatch"
    else:
        key = "other_plant"

    return REJECTION_TEXT[lang][key]
