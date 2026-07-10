DISEASE_COLORS = {
    "Healthy": "#2d6a4f",
    "Common_Rust": "#bc6c25",
    "Blight": "#5c4d7a",
    "Gray_Leaf_Spot": "#4a5568",
}

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
    }

    .block-container {
        padding-top: 2.25rem;
        padding-bottom: 2.5rem;
        max-width: 1120px;
        animation: pageIn 0.45s ease-out;
    }

    @keyframes pageIn {
        from { opacity: 0; transform: translateY(6px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .page-header {
        border-bottom: 1px solid #dce5dc;
        padding-bottom: 1rem;
        margin-bottom: 1.75rem;
        position: relative;
    }
    .page-header::after {
        content: '';
        position: absolute;
        bottom: -1px;
        left: 0;
        width: 72px;
        height: 2px;
        background: #3d6b4f;
        border-radius: 2px;
        transition: width 0.35s ease;
    }
    .page-header:hover::after {
        width: 110px;
    }
    .page-header h1 {
        font-family: 'Source Serif 4', Georgia, 'Times New Roman', serif;
        font-size: 1.85rem;
        font-weight: 700;
        color: #152515;
        margin: 0 0 0.35rem 0;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    .page-header p {
        margin: 0;
        color: #5a6b5a;
        font-size: 0.97rem;
        font-weight: 400;
        line-height: 1.5;
    }

    .panel {
        background: #ffffff;
        border: 1px solid #e4ebe4;
        border-radius: 10px;
        padding: 1.35rem 1.45rem;
        box-shadow:
            0 1px 2px rgba(21, 37, 21, 0.04),
            0 4px 16px rgba(21, 37, 21, 0.05);
        transition: box-shadow 0.3s ease, transform 0.3s ease, border-color 0.3s ease;
    }
    .panel:hover {
        box-shadow:
            0 2px 6px rgba(21, 37, 21, 0.06),
            0 10px 28px rgba(21, 37, 21, 0.08);
        transform: translateY(-2px);
        border-color: #d0ddd0;
    }
    .panel-title {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: #5a6b5a;
        margin-bottom: 1.1rem;
    }

    .result-panel {
        border: 1px solid #e4ebe4;
        border-left-width: 5px;
        border-radius: 10px;
        padding: 1.35rem 1.45rem;
        background: #ffffff;
        margin-bottom: 1.1rem;
        box-shadow:
            0 2px 8px rgba(21, 37, 21, 0.06),
            0 8px 24px rgba(21, 37, 21, 0.05);
        animation: riseIn 0.5s cubic-bezier(0.22, 1, 0.36, 1);
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    .result-panel:hover {
        box-shadow:
            0 4px 12px rgba(21, 37, 21, 0.08),
            0 12px 32px rgba(21, 37, 21, 0.07);
        transform: translateY(-1px);
    }
    @keyframes riseIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .result-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #5a6b5a;
        margin-bottom: 0.4rem;
    }
    .result-disease {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #152515;
        margin: 0 0 0.2rem 0;
        letter-spacing: -0.02em;
    }
    .result-scientific {
        font-size: 0.92rem;
        color: #5a6b5a;
        margin: 0 0 0.85rem 0;
        font-style: italic;
    }
    .result-confidence {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 2rem;
        font-weight: 700;
        color: #152515;
        margin: 0;
        letter-spacing: -0.03em;
    }
    .result-confidence span {
        font-family: 'Source Sans 3', sans-serif;
        font-size: 0.88rem;
        font-weight: 500;
        color: #5a6b5a;
        letter-spacing: 0;
    }

    .reject-panel {
        border: 1px solid #f0dcc0;
        border-left: 5px solid #b45309;
        border-radius: 10px;
        padding: 1.2rem 1.35rem;
        background: linear-gradient(135deg, #fffdf8 0%, #fff8eb 100%);
        box-shadow: 0 2px 10px rgba(180, 83, 9, 0.08);
        animation: riseIn 0.45s ease-out;
    }
    .reject-panel h3 {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #92400e;
        margin: 0 0 0.45rem 0;
    }
    .reject-panel p {
        margin: 0;
        color: #78350f;
        font-size: 0.93rem;
        line-height: 1.55;
    }

    .notice {
        font-size: 0.88rem;
        color: #4b5563;
        background: #f6f8f6;
        border: 1px solid #e2ebe2;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        line-height: 1.5;
        margin-bottom: 1rem;
        box-shadow: inset 0 1px 2px rgba(21, 37, 21, 0.03);
        transition: background 0.25s ease, border-color 0.25s ease;
    }
    .notice:hover {
        background: #f2f5f2;
        border-color: #d5e0d5;
    }

    .empty-state {
        text-align: center;
        padding: 2.75rem 1.25rem;
        color: #6b7280;
        font-size: 0.94rem;
        line-height: 1.55;
    }
    .empty-state strong {
        color: #374151;
        font-weight: 600;
    }

    .prob-row {
        margin-bottom: 0.75rem;
        animation: fadeIn 0.4s ease-out backwards;
    }
    .prob-row:nth-child(1) { animation-delay: 0.05s; }
    .prob-row:nth-child(2) { animation-delay: 0.12s; }
    .prob-row:nth-child(3) { animation-delay: 0.19s; }
    .prob-row:nth-child(4) { animation-delay: 0.26s; }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-6px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    .prob-row-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: #374151;
        margin-bottom: 0.3rem;
        font-weight: 500;
    }
    .prob-row-header strong {
        color: #152515;
        font-weight: 600;
    }
    .prob-track {
        background: #e8ede8;
        height: 7px;
        border-radius: 4px;
        overflow: hidden;
        box-shadow: inset 0 1px 2px rgba(21, 37, 21, 0.06);
    }
    .prob-fill {
        height: 100%;
        border-radius: 4px;
        transform-origin: left center;
        animation: barGrow 0.85s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    }
    @keyframes barGrow {
        from { transform: scaleX(0); }
        to   { transform: scaleX(1); }
    }

    .sidebar-title {
        font-family: 'Source Serif 4', Georgia, serif;
        font-size: 1.12rem;
        font-weight: 700;
        color: #152515;
        margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
        line-height: 1.3;
    }
    .sidebar-sub {
        font-size: 0.78rem;
        color: #6b7280;
        margin-bottom: 0.65rem;
        line-height: 1.45;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8faf8 0%, #f3f6f3 100%);
        border-right: 1px solid #e2e9e2;
        box-shadow: 2px 0 16px rgba(21, 37, 21, 0.04);
    }

    div[data-testid="stSidebar"] .stRadio > div {
        gap: 0.35rem;
    }
    div[data-testid="stSidebar"] .stRadio label {
        font-size: 0.93rem;
        font-weight: 500;
        padding: 0.55rem 0.75rem;
        border-radius: 8px;
        transition: background 0.2s ease, color 0.2s ease, padding-left 0.2s ease;
    }
    div[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(61, 107, 79, 0.08);
    }
    div[data-testid="stSidebar"] .stRadio label[data-checked="true"],
    div[data-testid="stSidebar"] .stRadio div[aria-checked="true"] label {
        background: rgba(61, 107, 79, 0.12);
        color: #2d5a3d;
        font-weight: 600;
    }

    div[data-testid="stSidebar"] [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e4ebe4;
        border-radius: 8px;
        padding: 0.5rem 0.65rem;
        box-shadow: 0 1px 4px rgba(21, 37, 21, 0.05);
        transition: box-shadow 0.25s ease, transform 0.25s ease;
    }
    div[data-testid="stSidebar"] [data-testid="stMetric"]:hover {
        box-shadow: 0 3px 10px rgba(21, 37, 21, 0.08);
        transform: translateY(-1px);
    }

    div[data-testid="column"] [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e8ede8;
        border-radius: 10px;
        padding: 0.65rem 0.85rem;
        box-shadow: 0 2px 8px rgba(21, 37, 21, 0.05);
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    div[data-testid="column"] [data-testid="stMetric"]:hover {
        box-shadow: 0 4px 14px rgba(21, 37, 21, 0.09);
        transform: translateY(-2px);
    }

    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-family: 'Source Sans 3', sans-serif !important;
        transition: all 0.22s ease !important;
        box-shadow: 0 1px 3px rgba(21, 37, 21, 0.08) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(61, 107, 79, 0.18) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    div[data-testid="stFileUploader"] {
        border-radius: 10px;
        transition: box-shadow 0.25s ease;
    }
    div[data-testid="stFileUploader"]:hover {
        box-shadow: 0 2px 12px rgba(21, 37, 21, 0.06);
    }

    div[data-testid="stImage"] img {
        border-radius: 8px;
        box-shadow: 0 2px 12px rgba(21, 37, 21, 0.1);
        transition: transform 0.35s ease, box-shadow 0.35s ease;
    }
    div[data-testid="stImage"]:hover img {
        transform: scale(1.015);
        box-shadow: 0 6px 22px rgba(21, 37, 21, 0.13);
    }

    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(21, 37, 21, 0.05);
    }

    div[data-testid="stExpander"] {
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(21, 37, 21, 0.04);
        transition: box-shadow 0.25s ease;
    }
    div[data-testid="stExpander"]:hover {
        box-shadow: 0 3px 10px rgba(21, 37, 21, 0.07);
    }

    h1, h2, h3 {
        font-family: 'Source Serif 4', Georgia, serif !important;
        letter-spacing: -0.02em;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(8px);
        border-bottom: 1px solid #e5ebe5;
        box-shadow: 0 1px 6px rgba(21, 37, 21, 0.04);
    }

    .stApp {
        background: #f3f6f3;
    }
</style>
"""
