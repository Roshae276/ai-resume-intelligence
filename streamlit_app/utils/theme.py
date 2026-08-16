"""
Shared Theme & UI Components
Import apply_theme() at the top of every page, then use the
helper components below wherever you'd normally use raw
st.success/st.error loops for a more polished look.

None of these helpers change any data flow — they only change
how existing data is rendered.
"""

import streamlit as st


# ============================================================
# Theme (inject once per page)
# ============================================================

def apply_theme():
    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Lexend:wght@500;600;700;800;900&display=swap');

        :root {
            --accent-1: #6366F1;
            --accent-2: #A855F7;
            --accent-3: #22D3EE;
            --accent-4: #EC4899;
            --success: #10B981;
            --danger: #F43F5E;
            --warning: #F59E0B;
            --surface: #FFFFFF;
            --surface-muted: #F8F9FC;
            --border: #E7E9F3;
            --text-primary: #14162B;
            --text-secondary: #676C87;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, sans-serif;
        }

        @keyframes floatBlob {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(20px, -25px) scale(1.06); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="block-container"] {
            animation: fadeInUp 0.45s ease-out;
            padding-top: 1.6rem !important;
        }

        /* ---------- App background: layered blurred color blobs ---------- */
        [data-testid="stAppViewContainer"] {
            background-color: #F6F7FD;
            background-image:
                radial-gradient(circle at 12% 8%, rgba(99, 102, 241, 0.16) 0%, rgba(99, 102, 241, 0) 32%),
                radial-gradient(circle at 88% 4%, rgba(236, 72, 153, 0.14) 0%, rgba(236, 72, 153, 0) 30%),
                radial-gradient(circle at 92% 60%, rgba(34, 211, 238, 0.14) 0%, rgba(34, 211, 238, 0) 30%),
                radial-gradient(circle at 6% 78%, rgba(168, 85, 247, 0.14) 0%, rgba(168, 85, 247, 0) 32%),
                radial-gradient(circle at 50% 50%, #FFFFFF 0%, #F6F7FD 70%);
            background-attachment: fixed;
        }

        [data-testid="stHeader"] {
            background: rgba(255,255,255,0);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(200deg, #14152A 0%, #1D1E3D 55%, #251C42 100%);
            border-right: 1px solid #2A2C42;
        }
        [data-testid="stSidebar"] * {
            color: #E5E7F5 !important;
        }
        [data-testid="stSidebar"] a {
            border-radius: 12px !important;
            transition: all 0.15s ease-in-out !important;
        }
        [data-testid="stSidebarNav"] a:hover,
        [data-testid="stSidebar"] a:hover {
            background: rgba(255,255,255,0.08) !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(90deg, rgba(99,102,241,0.35), rgba(168,85,247,0.15)) !important;
            border-left: 3px solid var(--accent-3) !important;
        }
        [data-testid="stSidebarUserContent"]::before {
            content: "✨ AI Resume Intelligence";
            display: block;
            font-family: 'Lexend', sans-serif;
            font-weight: 700;
            font-size: 1.05rem;
            color: #FFFFFF !important;
            padding: 0.4rem 0.2rem 1.1rem 0.2rem;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            margin-bottom: 0.8rem;
        }

        /* ---------- Titles ---------- */
        h1 {
            font-family: 'Lexend', 'Inter', sans-serif !important;
            font-weight: 800 !important;
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2) 55%, var(--accent-4));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
            padding-bottom: 2px;
        }

        h2, h3 {
            font-family: 'Lexend', 'Inter', sans-serif !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stCaptionContainer"] {
            font-size: 0.98rem !important;
            color: var(--text-secondary) !important;
        }

        /* ---------- Dividers ---------- */
        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--border) 20%, var(--border) 80%, transparent) !important;
            margin: 1.4rem 0 !important;
        }

        /* ---------- Buttons ---------- */
        .stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            padding: 0.65rem 1.3rem !important;
            transition: all 0.18s ease-in-out !important;
            border: 1px solid var(--border) !important;
            background: var(--surface) !important;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2) 55%, var(--accent-4)) !important;
            background-size: 200% auto !important;
            border: none !important;
            box-shadow: 0 8px 22px rgba(99, 102, 241, 0.35) !important;
            color: white !important;
        }

        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            background-position: right center !important;
            box-shadow: 0 12px 28px rgba(99, 102, 241, 0.45) !important;
        }

        .stButton > button:not([kind="primary"]):hover {
            border-color: var(--accent-1) !important;
            color: var(--accent-1) !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
        }

        /* ---------- Metrics: gradient icon-style cards with color variety ---------- */
        [data-testid="stMetric"] {
            position: relative;
            background: linear-gradient(160deg, #FFFFFF 0%, #FAFAFF 100%);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.2rem 1.4rem 1.3rem 1.4rem;
            box-shadow: 0 8px 24px rgba(30, 34, 60, 0.06);
            overflow: hidden;
        }
        [data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-1), var(--accent-3));
        }
        [data-testid="column"]:nth-of-type(2) [data-testid="stMetric"]::before {
            background: linear-gradient(90deg, var(--accent-2), var(--accent-4));
        }
        [data-testid="column"]:nth-of-type(3) [data-testid="stMetric"]::before {
            background: linear-gradient(90deg, var(--accent-3), var(--success));
        }
        [data-testid="stMetricLabel"] {
            font-weight: 600 !important;
            color: var(--text-secondary) !important;
        }
        [data-testid="stMetricValue"] {
            font-family: 'Lexend', sans-serif !important;
            font-weight: 800 !important;
            font-size: 2.1rem !important;
            color: var(--text-primary) !important;
        }

        /* ---------- Containers / cards ---------- */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 20px !important;
            border: 1px solid var(--border) !important;
            box-shadow: 0 10px 28px rgba(30, 34, 60, 0.07) !important;
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(10px);
            transition: box-shadow 0.2s ease-in-out, transform 0.2s ease-in-out !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            box-shadow: 0 14px 34px rgba(30, 34, 60, 0.11) !important;
        }

        /* ---------- Alerts ---------- */
        [data-testid="stAlertContentSuccess"],
        [data-testid="stAlertContentInfo"],
        [data-testid="stAlertContentWarning"],
        [data-testid="stAlertContentError"] {
            font-weight: 500 !important;
        }
        div[data-testid="stNotificationContentSuccess"],
        div[data-testid="stNotificationContentInfo"],
        div[data-testid="stNotificationContentWarning"],
        div[data-testid="stNotificationContentError"],
        .stAlert {
            border-radius: 12px !important;
        }

        /* ---------- Inputs ---------- */
        .stTextInput input, .stTextArea textarea, [data-baseweb="select"] {
            border-radius: 10px !important;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: var(--accent-1) !important;
            box-shadow: 0 0 0 1px var(--accent-1) !important;
        }

        /* ---------- File uploader ---------- */
        [data-testid="stFileUploaderDropzone"] {
            border-radius: 16px !important;
            border: 2px dashed var(--border) !important;
            background: var(--surface-muted) !important;
        }

        /* ---------- Progress bar ---------- */
        [data-testid="stProgress"] > div > div {
            background: linear-gradient(90deg, var(--accent-1), var(--accent-3)) !important;
            border-radius: 8px !important;
        }
        [data-testid="stProgress"] {
            border-radius: 8px !important;
            overflow: hidden;
        }

        /* ---------- Page links (nav cards) ---------- */
        [data-testid="stPageLink"] {
            border: 1px solid var(--border) !important;
            border-radius: 14px !important;
            padding: 0.55rem 0.9rem !important;
            background: var(--surface) !important;
            box-shadow: 0 4px 12px rgba(30, 34, 60, 0.04) !important;
            transition: all 0.15s ease-in-out !important;
        }
        [data-testid="stPageLink"]:hover {
            border-color: var(--accent-1) !important;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.15) !important;
            transform: translateY(-1px);
        }

        /* ---------- Custom hero banner ---------- */
        .hero-banner {
            position: relative;
            background: linear-gradient(120deg, #14152A 0%, #241F45 45%, #3B2064 85%, #5B2A72 100%);
            border-radius: 24px;
            padding: 2.4rem 2.6rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 16px 38px rgba(40, 20, 70, 0.30);
            overflow: hidden;
        }
        .hero-banner::before {
            content: "";
            position: absolute;
            top: -60px; right: -60px;
            width: 220px; height: 220px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(34,211,238,0.35), rgba(34,211,238,0) 70%);
            animation: floatBlob 7s ease-in-out infinite;
        }
        .hero-banner::after {
            content: "";
            position: absolute;
            bottom: -70px; left: 15%;
            width: 260px; height: 260px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(236,72,153,0.28), rgba(236,72,153,0) 70%);
            animation: floatBlob 9s ease-in-out infinite reverse;
        }
        .hero-banner h1 {
            position: relative;
            -webkit-text-fill-color: #FFFFFF !important;
            background: none !important;
            font-size: 2.15rem !important;
            margin-bottom: 0.4rem !important;
        }
        .hero-banner p {
            position: relative;
            color: #CBCEEF !important;
            font-size: 1.04rem;
            margin: 0;
            max-width: 640px;
        }

        /* ---------- Section title with icon chip ---------- */
        .section-title {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            font-family: 'Lexend', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
            color: var(--text-primary);
            margin: 0.3rem 0 0.9rem 0;
        }
        .section-title .chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 36px; height: 36px;
            border-radius: 11px;
            font-size: 1.1rem;
            background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
            box-shadow: 0 6px 14px rgba(99,102,241,0.35);
        }

        /* ---------- Badges / pills ---------- */
        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-bottom: 0.4rem;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.42rem 0.95rem;
            border-radius: 999px;
            font-size: 0.86rem;
            font-weight: 600;
            border: 1px solid transparent;
            box-shadow: 0 3px 8px rgba(30, 34, 60, 0.05);
            transition: transform 0.15s ease-in-out;
        }
        .badge:hover {
            transform: translateY(-2px);
        }
        .badge-matched {
            background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
            color: #047857;
            border-color: #A7F3D0;
        }
        .badge-matched::before { content: "✓"; }
        .badge-missing {
            background: linear-gradient(135deg, #FEF2F2, #FEE2E2);
            color: #B91C1C;
            border-color: #FECACA;
        }
        .badge-missing::before { content: "✕"; }
        .badge-neutral {
            background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
            color: #4338CA;
            border-color: #C7D2FE;
        }
        .badge-neutral::before { content: "●"; font-size: 0.6rem; }

        /* ---------- Rank badge ---------- */
        .rank-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-family: 'Lexend', sans-serif;
            font-weight: 700;
            font-size: 1.05rem;
            padding: 0.35rem 1rem;
            border-radius: 999px;
            background: linear-gradient(135deg, #FDE68A, #F59E0B);
            color: #78350F;
            box-shadow: 0 6px 16px rgba(245, 158, 11, 0.35);
        }

        /* ---------- Score pill (used inline in markdown) ---------- */
        .score-pill {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.85rem;
            background: linear-gradient(135deg, var(--accent-1), var(--accent-3));
            color: white;
        }

        /* ---------- Feature card ---------- */
        .feature-card {
            position: relative;
            background: linear-gradient(160deg, #FFFFFF 0%, #FAFAFF 100%);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1.4rem 1.5rem;
            box-shadow: 0 8px 22px rgba(30, 34, 60, 0.06);
            height: 100%;
            overflow: hidden;
            transition: transform 0.18s ease-in-out, box-shadow 0.18s ease-in-out;
        }
        .feature-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 5px; height: 100%;
            background: linear-gradient(180deg, var(--accent-1), var(--accent-2), var(--accent-4));
        }
        .feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 14px 32px rgba(30, 34, 60, 0.11);
        }
        .feature-card h4 {
            font-family: 'Lexend', sans-serif;
            font-weight: 700;
            font-size: 1.05rem;
            margin: 0 0 0.7rem 0;
            color: var(--text-primary);
        }
        .feature-card ul {
            margin: 0;
            padding-left: 1.15rem;
            color: var(--text-secondary);
        }
        .feature-card li {
            margin-bottom: 0.35rem;
            line-height: 1.4;
        }

        /* ---------- Hide Deploy button / toolbar clutter ---------- */
        [data-testid="stToolbarActions"],
        [data-testid="stAppDeployButton"],
        .stAppDeployButton,
        #MainMenu {
            display: none !important;
        }

        /* ---------- Footer ---------- */
        .app-footer {
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.85rem;
            padding: 1.2rem 0 0.5rem 0;
            border-top: 1px solid var(--border);
            margin-top: 1rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Reusable components
# ============================================================

def hero_banner(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="hero-banner">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(icon: str, text: str):
    st.markdown(
        f"""
        <div class="section-title">
            <span class="chip">{icon}</span>
            <span>{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge_row(items, kind: str = "neutral"):
    """Render a wrapping row of pill badges. Returns True if items were rendered."""
    if not items:
        return False

    html = '<div class="badge-row">' + "".join(
        f'<span class="badge badge-{kind}">{item}</span>' for item in items
    ) + "</div>"

    st.markdown(html, unsafe_allow_html=True)
    return True


def feature_card(title: str, bullets: list):
    items = "".join(f"<li>{b}</li>" for b in bullets)
    st.markdown(
        f"""
        <div class="feature-card">
            <h4>{title}</h4>
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def rank_badge(rank: int):
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "🏅")
    st.markdown(
        f'<span class="rank-badge">{medal} Rank #{rank}</span>',
        unsafe_allow_html=True,
    )


def app_footer(text: str):
    st.markdown(f'<div class="app-footer">{text}</div>', unsafe_allow_html=True)