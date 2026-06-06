import streamlit as st
import pickle
import numpy as np
import gdown
import os

st.set_page_config(
    page_title="⚽ Player Value Predictor",
    page_icon="⚽",
    layout="centered",
)

# ============================================================
# NIKE.COM DESIGN SYSTEM — CSS INJECTION
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:ital,wght@0,300;0,400;0,600;0,700;0,900;1,300&family=Barlow+Condensed:wght@300;400;600;700;900&display=swap');

/* ── TOKENS ──────────────────────────────────────────────── */
:root {
    --n-black:  #111111;
    --n-white:  #FFFFFF;
    --n-orange: #FA5400;
    --n-mid:    #2A2A2A;
    --n-dim:    #1C1C1C;
    --n-muted:  #888888;
    --n-border: #2E2E2E;
}

/* ── HIDE STREAMLIT CHROME ───────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"]          { display: none !important; }
[data-testid="stDecoration"]       { display: none !important; }
[data-testid="stStatusWidget"]     { display: none !important; }

/* ── BACKGROUND ──────────────────────────────────────────── */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"],
.main { background-color: var(--n-black) !important; }

.block-container {
    padding: 1.5rem 2rem 5rem !important;
    max-width: 860px !important;
}

/* ── BASE TEXT ───────────────────────────────────────────── */
*, body {
    font-family: 'Barlow', sans-serif !important;
    color: #CCCCCC;
}

h1, h2, h3, h4 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--n-white) !important;
}

/* Streamlit's native h3 subheader */
[data-testid="stHeadingWithActionElements"] h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.7rem !important;
    letter-spacing: 3px !important;
    color: var(--n-white) !important;
    border-top: 1px solid var(--n-border);
    padding-top: 1.2rem;
    margin-top: 0.5rem;
}

/* Caption */
[data-testid="stCaptionContainer"] p,
.stCaption p {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.65rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: var(--n-muted) !important;
}

/* ── WIDGET LABELS ───────────────────────────────────────── */
[data-testid="stWidgetLabel"] p,
label p {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.62rem !important;
    font-weight: 700 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: #999 !important;
}

/* ── TEXT / NUMBER INPUTS ────────────────────────────────── */
input[type="number"],
input[type="text"] {
    background-color: var(--n-dim) !important;
    border: 1px solid var(--n-border) !important;
    border-radius: 0 !important;
    color: var(--n-white) !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.55rem 0.9rem !important;
    transition: border-color 0.18s ease !important;
}

input[type="number"]:focus,
input[type="text"]:focus {
    border-color: var(--n-orange) !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stNumberInput"] button {
    background-color: #222 !important;
    border-color: var(--n-border) !important;
    border-radius: 0 !important;
    color: #999 !important;
}

[data-testid="stNumberInput"] button:hover {
    background-color: var(--n-orange) !important;
    color: var(--n-white) !important;
}

/* ── SELECTBOX ───────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    background-color: var(--n-dim) !important;
    border: 1px solid var(--n-border) !important;
    border-radius: 0 !important;
    color: var(--n-white) !important;
}

[data-testid="stSelectbox"] svg { color: var(--n-orange) !important; }

/* ── SLIDER ──────────────────────────────────────────────── */
[data-testid="stSlider"] [class*="Track"] {
    border-radius: 0 !important;
}

[data-testid="stSlider"] [role="slider"] {
    background-color: var(--n-orange) !important;
    border: 2px solid var(--n-white) !important;
    border-radius: 0 !important;
    width: 14px !important;
    height: 14px !important;
}

[data-testid="stSlider"] p {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    color: #aaa !important;
}

/* ── PRIMARY BUTTON ─────────────────────────────────────── */
.stButton > button {
    background-color: var(--n-white) !important;
    color: var(--n-black) !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.25rem !important;
    letter-spacing: 4px !important;
    padding: 0.85rem 2rem !important;
    text-transform: uppercase !important;
    transition: background-color 0.18s ease, color 0.18s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    background-color: var(--n-orange) !important;
    color: var(--n-white) !important;
}

.stButton > button:active {
    background-color: #d14800 !important;
}

/* ── METRICS ─────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--n-dim) !important;
    border: 1px solid var(--n-border) !important;
    border-top: 2px solid var(--n-orange) !important;
    border-radius: 0 !important;
    padding: 1rem 1.25rem !important;
}

[data-testid="stMetricLabel"] > div,
[data-testid="stMetricLabel"] p {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.6rem !important;
    font-weight: 700 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: var(--n-muted) !important;
}

[data-testid="stMetricValue"] > div {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.9rem !important;
    letter-spacing: 1px !important;
    color: var(--n-white) !important;
}

/* ── ALERTS ──────────────────────────────────────────────── */
[data-testid="stAlert"] {
    background-color: var(--n-dim) !important;
    border-radius: 0 !important;
    border: 1px solid var(--n-border) !important;
    border-left: 3px solid var(--n-orange) !important;
}

[data-testid="stAlert"][kind="success"],
div.stSuccess > div {
    border-left-color: #00C853 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div {
    color: var(--n-white) !important;
    font-family: 'Barlow', sans-serif !important;
}

/* ── EXPANDER ────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background-color: var(--n-dim) !important;
    border: 1px solid var(--n-border) !important;
    border-radius: 0 !important;
}

details summary {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: #bbb !important;
    padding: 0.75rem 1rem !important;
}

details summary:hover { color: var(--n-orange) !important; }

details summary svg { color: var(--n-orange) !important; }

/* ── DIVIDER ─────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--n-border) !important;
    margin: 2rem 0 !important;
}

/* ── PROGRESS BAR ────────────────────────────────────────── */
[data-testid="stProgressBar"] {
    border-radius: 0 !important;
    height: 5px !important;
}

[data-testid="stProgressBar"] > div {
    background-color: var(--n-mid) !important;
    border-radius: 0 !important;
    height: 5px !important;
}

[data-testid="stProgressBar"] > div > div {
    background-color: var(--n-orange) !important;
    border-radius: 0 !important;
    transition: width 0.4s ease !important;
}

/* ── SCROLLBAR ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: var(--n-black); }
::-webkit-scrollbar-thumb { background: var(--n-orange); }

/* ── COLUMN GAPS ─────────────────────────────────────────── */
[data-testid="column"] { padding: 0 0.5rem !important; }
</style>

<!-- ═══════════════════════════════════════════════════════
     NIKE-STYLE HERO HEADER
     ═══════════════════════════════════════════════════════ -->
<div style="
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid #2A2A2A;
    margin-bottom: 1.5rem;
    position: relative;
">
    <!-- Swoosh-inspired accent line -->
    <div style="
        position: absolute;
        top: 0; left: 0;
        width: 48px; height: 3px;
        background: #FA5400;
    "></div>

    <!-- Eyebrow -->
    <p style="
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #FA5400;
        margin: 0 0 0.6rem;
    ">PERFORMANCE ANALYTICS · FOOTBALL INTELLIGENCE</p>

    <!-- Main headline -->
    <div style="
        font-family: 'Bebas Neue', sans-serif;
        font-size: clamp(2.8rem, 7vw, 4.8rem);
        line-height: 0.92;
        color: #FFFFFF;
        letter-spacing: 3px;
        margin-bottom: 1rem;
    ">
        PLAYER MARKET<br>
        <span style="color:#FA5400;">VALUE</span>
        PREDICTOR
    </div>

    <!-- Sub-line -->
    <p style="
        font-family: 'Barlow', sans-serif;
        font-weight: 300;
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #666;
        margin: 0;
    ">ML Model &nbsp;·&nbsp; Real Player Data &nbsp;·&nbsp; Kaggle Dataset</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# LOAD MODEL FROM GOOGLE DRIVE USING GDOWN
# ============================================================
@st.cache_resource
def load_model_from_drive():
    """Load model from Google Drive using gdown"""
    FILE_ID = "1oCRt4TUlgqzGyx236v0MzU5-khRvvS_1"
    FILE_PATH = "player_value_model.pkl"

    try:
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, FILE_PATH, quiet=False)

        with open(FILE_PATH, 'rb') as f:
            artifacts = pickle.load(f)

        st.success(f"✅ Model loaded: {artifacts['model_name']}")
        return artifacts

    except Exception as e:
        st.error(f"Failed to load model from Drive: {e}")
        st.info("Make sure the file is shared as 'Anyone with the link'")
        return None

# Load model
artifacts = load_model_from_drive()

if artifacts:
    model = artifacts["model"]
    le_position    = artifacts["le_position"]
    le_sub_position = artifacts["le_sub_position"]
    le_foot        = artifacts["le_foot"]

    with st.expander("ℹ️ Model Information"):
        m = artifacts["metrics"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Model",    artifacts["model_name"])
        col2.metric("R² Score", f"{m.get('r2', 0):.4f}")
        col3.metric("MAE",      f"€{m.get('mae_eur', 0)/1e6:.2f}M")

    st.divider()
    st.subheader("📋 Player Profile")

    col_a, col_b = st.columns(2)

    with col_a:
        age        = st.slider("Age", 15, 45, 24)
        height_cm  = st.number_input("Height (cm)", 150, 215, 180)
        position   = st.selectbox("Position",
                        ["Attack", "Midfield", "Defender", "Goalkeeper"])
        sub_position = st.selectbox("Sub-position",
                        ["Centre-Forward", "Winger", "Midfielder",
                         "Defender", "Goalkeeper"])
        foot       = st.selectbox("Preferred Foot", ["right", "left", "both"])

    with col_b:
        highest_mv   = st.number_input("Highest Ever Market Value (€)",
                            0, 200_000_000, 5_000_000, step=500_000)
        total_apps   = st.number_input("Career Appearances",  0, 1000, 80)
        total_goals  = st.number_input("Career Goals",        0,  500, 20)
        total_assists= st.number_input("Career Assists",      0,  500, 15)
        avg_mins     = st.slider("Avg Minutes Played / Game", 0, 95, 75)
        yellow_cards = st.number_input("Total Yellow Cards",  0,  300,  8)
        red_cards    = st.number_input("Total Red Cards",     0,   50,  1)
        seasons      = st.slider("Seasons Active", 1, 20, 5)

    def safe_encode(encoder, value):
        try:
            return int(encoder.transform([value])[0])
        except (ValueError, AttributeError):
            return 0

    def predict():
        goals_pg   = total_goals   / (total_apps + 1)
        assists_pg  = total_assists / (total_apps + 1)

        X = np.array([[
            age, height_cm,
            safe_encode(le_position,     position),
            safe_encode(le_sub_position, sub_position),
            safe_encode(le_foot,         foot),
            highest_mv, total_apps, total_goals, total_assists,
            avg_mins, goals_pg, assists_pg,
            yellow_cards, red_cards, seasons
        ]])

        log_pred  = model.predict(X)[0]
        value_eur = float(np.expm1(log_pred))
        value_M   = value_eur / 1_000_000
        return value_M, value_eur

    st.divider()

    if st.button("🔮 Predict Market Value", type="primary", use_container_width=True):
        value_M, value_eur = predict()

        st.success(f"### 💰 Predicted Market Value: **€{value_M:.2f}M**")
        st.progress(min(value_M / 200, 1.0), text=f"€{value_M:.1f}M / €200M scale")

        if value_M >= 80:
            st.info("🌟 World-class player")
        elif value_M >= 30:
            st.info("⭐ Top-tier player")
        elif value_M >= 10:
            st.info("🔵 Quality first-team player")
        elif value_M >= 2:
            st.info("🟡 Rotation / squad player")
        else:
            st.info("🟤 Development / fringe player")

    st.divider()
    st.caption("Built with 🐍 Streamlit | Model trained on Kaggle player dataset")

else:
    st.warning("⚠️ Model not loaded. Please check Google Drive link is correct and file is shared.")
