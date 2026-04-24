st.markdown("""
<style>
    /* ========= Global ========= */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", sans-serif;
        color: #0f172a;
    }

    p, li, div, span, label {
        font-size: 15px !important;
    }

    /* ========= Sidebar ========= */
    section[data-testid="stSidebar"] {
        background: #f5f7fb;
        border-right: 1px solid #d9e2ec;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .sidebar-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }

    .sidebar-subtext {
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 1rem;
    }

    .filter-card {
        background: #ffffff;
        border: 1px solid #d9e2ec;
        border-radius: 14px;
        padding: 14px 14px 10px 14px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }

    .filter-card-title {
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }

    .filter-card-subtext {
        font-size: 0.83rem;
        color: #94a3b8;
        margin-bottom: 0.65rem;
    }

    /* Sidebar multiselect container */
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #f8fafc !important;
        border: 1px solid #d8e0ea !important;
        border-radius: 10px !important;
        min-height: 44px !important;
        box-shadow: none !important;
    }

    /* Selected tags in sidebar -> light gray instead of red */
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background: #eef2f7 !important;
        border: 1px solid #d8e0ea !important;
        border-radius: 8px !important;
        color: #334155 !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
        color: #334155 !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
        fill: #64748b !important;
        color: #64748b !important;
    }

    section[data-testid="stSidebar"] input {
        color: #0f172a !important;
    }

    /* ========= Section Containers ========= */
    [data-testid="stVerticalBlock"] > div:has(.section-kicker) {
        margin-bottom: 1.2rem;
    }

    .section-shell {
        background: #ffffff;
        border: 1px solid #d9e2ec;
        border-radius: 18px;
        padding: 18px 18px 16px 18px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }

    .section-kicker {
        display: inline-block;
        padding: 6px 12px;
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #334155;
        background: #eef4ff;
        border: 1px solid #dbe7ff;
        border-radius: 999px;
        margin-bottom: 0.9rem;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 850;
        line-height: 1.1;
        color: #0b1f44;
        margin-bottom: 0.45rem;
    }

    .subtitle {
        font-size: 1.08rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.25rem;
    }

    .disclaimer {
        font-size: 0.96rem;
        color: #64748b;
        margin-bottom: 0.4rem;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.35rem;
    }

    .section-subtext {
        font-size: 0.98rem;
        color: #64748b;
        margin-bottom: 1rem;
        line-height: 1.5;
    }

    .subsection-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }

    .subsection-note {
        font-size: 0.96rem;
        color: #64748b;
        margin-bottom: 0.9rem;
        line-height: 1.45;
    }

    /* ========= Metric Cards ========= */
    .metric-card {
        background: #ffffff;
        border: 1px solid #d9e2ec;
        border-top: 4px solid #dbeafe;
        border-radius: 16px;
        padding: 18px 18px 16px 18px;
        min-height: 138px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }

    .metric-label {
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 0.9rem;
    }

    .metric-value {
        font-size: 2.25rem;
        font-weight: 850;
        color: #0b1f44;
        line-height: 1.1;
        margin-bottom: 0.65rem;
    }

    .metric-note {
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.45;
    }

    /* ========= Product Cards ========= */
    .product-card {
        background: #ffffff;
        border: 1px solid #d9e2ec;
        border-radius: 16px;
        padding: 16px;
        min-height: 220px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }

    .product-name {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }

    .product-sub {
        font-size: 0.97rem;
        color: #64748b;
        margin-bottom: 0.8rem;
        line-height: 1.45;
    }

    .product-price {
        font-size: 2rem;
        font-weight: 850;
        color: #0b1f44;
        margin-bottom: 0.8rem;
        line-height: 1.1;
    }

    .small-muted {
        font-size: 0.9rem;
        color: #94a3b8;
        line-height: 1.45;
        margin-top: 0.6rem;
    }

    /* ========= Badges ========= */
    .badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid transparent;
    }

    .badge-neutral {
        background: #f1f5f9;
        color: #334155;
        border-color: #dbe2ea;
    }

    .badge-up {
        background: #fee2e2;
        color: #b91c1c;
        border-color: #fecaca;
    }

    .badge-down {
        background: #dcfce7;
        color: #166534;
        border-color: #bbf7d0;
    }

    .badge-quality {
        background: #eef4ff;
        color: #1d4ed8;
        border-color: #dbeafe;
    }

    /* ========= Soft Note ========= */
    .soft-note {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
        border-radius: 12px;
        padding: 12px 14px;
        font-size: 0.96rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }

    /* ========= Buttons ========= */
    .stButton > button {
        background: #ffffff;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        font-weight: 650;
        padding: 0.45rem 1rem;
    }

    .stButton > button:hover {
        border-color: #94a3b8;
        background: #f8fafc;
        color: #0f172a;
    }

    /* ========= Tables ========= */
    [data-testid="stDataFrame"] {
        border: 1px solid #d9e2ec;
        border-radius: 12px;
        overflow: hidden;
    }

    /* ========= Tabs ========= */
    button[data-baseweb="tab"] {
        font-size: 1rem !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)
