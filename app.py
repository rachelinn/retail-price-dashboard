import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Retail Pricing Intelligence",
    page_icon="📊",
    layout="wide"
)

# =========================
# Google Sheet CSV URL
# =========================
SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1tomybUYyC7rAa7O7VGpyrxdWOjYLnFmheFvKk04sSDc"
    "/export?format=csv&gid=0"
)

# =========================
# Styling
# =========================
st.markdown(
    """
    <style>
    /* ========= Global ========= */
    .stApp {
        background: #FEFBF7;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", sans-serif;
        color: #1f2937;
    }

    p, li, div, span, label {
        font-size: 15px !important;
    }

    /* ========= Sidebar ========= */
    section[data-testid="stSidebar"] {
        background: #FAF6F1;
        border-right: 1px solid #EEE5DC;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .sidebar-title {
        font-size: 1.45rem !important;
        font-weight: 850;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }

    .sidebar-subtext {
        font-size: 0.92rem !important;
        color: #6b7280;
        margin-bottom: 1rem;
        line-height: 1.4;
    }

    .filter-group-title {
        font-size: 0.78rem !important;
        font-weight: 850;
        color: #3f3328;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.2rem;
    }

    .filter-group-note {
        font-size: 0.82rem !important;
        color: #9ca3af;
        margin-bottom: 0.65rem;
    }

    section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid #EEE5DC !important;
        border-radius: 14px !important;
        box-shadow: 0 1px 3px rgba(80, 50, 20, 0.025);
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #DDD6CC !important;
        border-radius: 10px !important;
        min-height: 44px !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background: #F1EEE9 !important;
        border: 1px solid #DDD6CC !important;
        border-radius: 8px !important;
        color: #4B5563 !important;
        font-weight: 650 !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
        color: #4B5563 !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
        fill: #64748b !important;
        color: #64748b !important;
    }

    section[data-testid="stSidebar"] input {
        color: #1f2937 !important;
    }

    /* ========= Section Containers ========= */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #EEE5DC !important;
        border-radius: 18px !important;
        background: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(80, 50, 20, 0.025);
    }

    .section-kicker {
        display: inline-block;
        padding: 6px 12px;
        font-size: 0.72rem !important;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9A6B45;
        background: #FFF1E4;
        border: 1px solid #F6DDC6;
        border-radius: 999px;
        margin-bottom: 0.9rem;
    }

    .main-title {
        font-size: 2.45rem !important;
        font-weight: 900;
        line-height: 1.1;
        color: #1f2937;
        margin-bottom: 0.45rem;
    }

    .subtitle {
        font-size: 1.02rem !important;
        font-weight: 650;
        color: #374151;
        margin-bottom: 0.25rem;
    }

    .disclaimer {
        font-size: 0.92rem !important;
        color: #6b7280;
        margin-bottom: 0.4rem;
    }

    .section-title {
        font-size: 1.75rem !important;
        font-weight: 850;
        color: #1f2937;
        margin-bottom: 0.35rem;
    }

    .section-subtext {
        font-size: 0.96rem !important;
        color: #6b7280;
        margin-bottom: 1rem;
        line-height: 1.5;
    }

    .subsection-title {
        font-size: 1.22rem !important;
        font-weight: 850;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }

    .subsection-note {
        font-size: 0.92rem !important;
        color: #6b7280;
        margin-bottom: 0.9rem;
        line-height: 1.45;
    }

    /* ========= Metric Cards ========= */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #EEE5DC;
        border-top: 4px solid #F1C9A5;
        border-radius: 16px;
        padding: 18px 18px 16px 18px;
        min-height: 138px;
        box-shadow: 0 1px 3px rgba(80, 50, 20, 0.025);
    }

    .metric-label {
        font-size: 0.82rem !important;
        font-weight: 850;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #7c6a58;
        margin-bottom: 0.9rem;
    }

    .metric-value {
        font-size: 2.25rem !important;
        font-weight: 900;
        color: #1f2937;
        line-height: 1.1;
        margin-bottom: 0.65rem;
    }

    .metric-note {
        font-size: 0.9rem !important;
        color: #9ca3af;
        line-height: 1.45;
    }

    /* ========= Product Cards ========= */
    .product-card {
        background: #FFFFFF;
        border: 1px solid #EEE5DC;
        border-radius: 16px;
        padding: 16px;
        min-height: 220px;
        box-shadow: 0 1px 3px rgba(80, 50, 20, 0.025);
    }

    .product-name {
        font-size: 1.22rem !important;
        font-weight: 850;
        color: #1f2937;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }

    .product-sub {
        font-size: 0.9rem !important;
        color: #6b7280;
        margin-bottom: 0.8rem;
        line-height: 1.45;
    }

    .product-price {
        font-size: 1.9rem !important;
        font-weight: 900;
        color: #1f2937;
        margin-bottom: 0.8rem;
        line-height: 1.1;
    }

    .small-muted {
        font-size: 0.82rem !important;
        color: #9ca3af;
        line-height: 1.45;
        margin-top: 0.6rem;
    }

    /* ========= Badges ========= */
    .badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.78rem !important;
        font-weight: 750;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid transparent;
    }

    .badge-green {
        background: #E6F4EA;
        color: #166534;
        border-color: #cce8d4;
    }

    .badge-red {
        background: #FCE7E7;
        color: #9f1239;
        border-color: #f3c5c5;
    }

    .badge-gray {
        background: #F1EEE9;
        color: #4B5563;
        border-color: #DDD6CC;
    }

    .badge-blue {
        background: #FFF1E4;
        color: #9A6B45;
        border-color: #F6DDC6;
    }

    /* ========= Soft Note ========= */
    .soft-note {
        background: #FFF7EF;
        border: 1px solid #F6DDC6;
        color: #9A6B45;
        border-radius: 12px;
        padding: 12px 14px;
        font-size: 0.94rem !important;
        font-weight: 500;
        margin-bottom: 1rem;
    }

    /* ========= Buttons ========= */
    .stButton > button {
        background: #ffffff;
        color: #1f2937;
        border: 1px solid #D8CABB;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.45rem 1rem;
    }

    .stButton > button:hover {
        border-color: #D5A77F;
        background: #FFF7EF;
        color: #9A6B45;
    }

    /* ========= Tables ========= */
    [data-testid="stDataFrame"] {
        border: 1px solid #EEE5DC;
        border-radius: 12px;
        overflow: hidden;
    }

    /* ========= Tabs ========= */
    button[data-baseweb="tab"] {
        font-size: 1rem !important;
        font-weight: 800 !important;
        color: #4b5563 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #9A6B45 !important;
        border-bottom-color: #F1C9A5 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Data loading
# =========================
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(SHEET_CSV_URL)

    df.columns = [c.strip().upper() for c in df.columns]

    required_cols = [
        "DATE",
        "BRAND",
        "PRODUCT NAME",
        "RETAILER",
        "CATEGORY",
        "PRICE",
        "PRICE TYPE",
        "LOCATION STATUS",
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

    df["PRICE"] = (
        df["PRICE"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["PRICE"] = pd.to_numeric(df["PRICE"], errors="coerce")

    df = df.dropna(subset=["DATE", "PRODUCT NAME", "RETAILER", "PRICE"])

    for col in ["BRAND", "PRODUCT NAME", "RETAILER", "CATEGORY", "PRICE TYPE", "LOCATION STATUS"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    df["SKU KEY"] = (
        df["PRODUCT NAME"].astype(str)
        + " | "
        + df["BRAND"].astype(str)
        + " | "
        + df["RETAILER"].astype(str)
    )

    df = df.sort_values(["SKU KEY", "DATE"])

    df["PREVIOUS PRICE"] = df.groupby("SKU KEY")["PRICE"].shift(1)
    df["VARIANCE $"] = df["PRICE"] - df["PREVIOUS PRICE"]
    df["VARIANCE %"] = df["VARIANCE $"] / df["PREVIOUS PRICE"]

    return df


def get_latest_rows(df):
    return (
        df.sort_values("DATE")
        .groupby("SKU KEY", as_index=False)
        .tail(1)
        .sort_values(["RETAILER", "BRAND", "PRODUCT NAME"])
    )


def format_currency(value):
    if pd.isna(value):
        return "—"
    return f"${value:,.2f}"


def format_variance_dollar(value):
    if pd.isna(value):
        return "New"
    if value > 0:
        return f"+${value:,.2f}"
    if value < 0:
        return f"-${abs(value):,.2f}"
    return "$0.00"


def format_variance_percent(value):
    if pd.isna(value):
        return ""
    if value > 0:
        return f"+{value * 100:.1f}%"
    if value < 0:
        return f"-{abs(value) * 100:.1f}%"
    return "0.0%"


def variance_badge_html(var_dollar, var_pct):
    if pd.isna(var_dollar):
        return '<span class="badge badge-gray">New baseline</span>'

    pct_text = format_variance_percent(var_pct)
    dollar_text = format_variance_dollar(var_dollar)

    if var_dollar > 0:
        return f'<span class="badge badge-red">↑ {dollar_text} ({pct_text})</span>'
    elif var_dollar < 0:
        return f'<span class="badge badge-green">↓ {dollar_text} ({pct_text})</span>'
    else:
        return '<span class="badge badge-gray">No change</span>'


def price_type_badge_html(price_type):
    pt = str(price_type).strip()

    if "Store-specific" in pt:
        return f'<span class="badge badge-blue">{pt}</span>'
    elif "Not Confirmed" in pt or "not confirmed" in pt:
        return f'<span class="badge badge-gray">{pt}</span>'
    else:
        return f'<span class="badge badge-gray">{pt}</span>'


def make_detail_chart(history_df, product_label):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["DATE"],
            y=history_df["PRICE"],
            mode="lines+markers",
            line=dict(width=3, color="#D5A77F"),
            marker=dict(size=8, color="#D5A77F"),
            hovertemplate="%{x|%b %d, %Y %I:%M %p}<br>$%{y:.2f}<extra></extra>",
            name=product_label,
        )
    )

    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Date",
        yaxis_title="Price",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        hovermode="x unified",
        showlegend=False,
        font=dict(color="#4b5563"),
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#EEE5DC")

    return fig


# =========================
# Load data
# =========================
try:
    df = load_data()
except Exception as e:
    st.error("Could not load data from Google Sheets.")
    st.write(e)
    st.stop()

if df.empty:
    st.warning("No data found in the Google Sheet.")
    st.stop()

latest = get_latest_rows(df)

if "selected_sku" not in st.session_state:
    st.session_state.selected_sku = None

# =========================
# Sidebar filters
# =========================
with st.sidebar:
    st.markdown('<div class="sidebar-title">Refine Data</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-subtext">Use the filters below to narrow the SKU view.</div>',
        unsafe_allow_html=True
    )

    category_options = sorted(latest["CATEGORY"].dropna().unique().tolist())
    retailer_options = sorted(latest["RETAILER"].dropna().unique().tolist())
    brand_options = sorted(latest["BRAND"].dropna().unique().tolist())
    price_type_options = sorted(latest["PRICE TYPE"].dropna().unique().tolist())

    with st.container(border=True):
        st.markdown('<div class="filter-group-title">Category</div>', unsafe_allow_html=True)
        st.markdown('<div class="filter-group-note">Filter by product category</div>', unsafe_allow_html=True)
        selected_categories = st.multiselect(
            "Category",
            category_options,
            default=category_options,
            label_visibility="collapsed",
            key="filter_category"
        )

    with st.container(border=True):
        st.markdown('<div class="filter-group-title">Retailer</div>', unsafe_allow_html=True)
        st.markdown('<div class="filter-group-note">Filter by retailer</div>', unsafe_allow_html=True)
        selected_retailers = st.multiselect(
            "Retailer",
            retailer_options,
            default=retailer_options,
            label_visibility="collapsed",
            key="filter_retailer"
        )

    with st.container(border=True):
        st.markdown('<div class="filter-group-title">Brand</div>', unsafe_allow_html=True)
        st.markdown('<div class="filter-group-note">Filter by brand</div>', unsafe_allow_html=True)
        selected_brands = st.multiselect(
            "Brand",
            brand_options,
            default=brand_options,
            label_visibility="collapsed",
            key="filter_brand"
        )

    with st.container(border=True):
        st.markdown('<div class="filter-group-title">Price Type</div>', unsafe_allow_html=True)
        st.markdown('<div class="filter-group-note">Filter by data quality / price source</div>', unsafe_allow_html=True)
        selected_price_types = st.multiselect(
            "Price Type",
            price_type_options,
            default=price_type_options,
            label_visibility="collapsed",
            key="filter_price_type"
        )

# =========================
# Apply filters
# =========================
filtered_latest = latest[
    latest["CATEGORY"].isin(selected_categories)
    & latest["RETAILER"].isin(selected_retailers)
    & latest["BRAND"].isin(selected_brands)
    & latest["PRICE TYPE"].isin(selected_price_types)
].copy()

filtered_keys = filtered_latest["SKU KEY"].unique().tolist()
filtered_history = df[df["SKU KEY"].isin(filtered_keys)].copy()

# =========================
# KPI values
# =========================
tracked_skus = filtered_latest["SKU KEY"].nunique()
avg_price = filtered_latest["PRICE"].mean()
price_increases = filtered_latest[filtered_latest["VARIANCE $"] > 0]["SKU KEY"].nunique()
price_decreases = filtered_latest[filtered_latest["VARIANCE $"] < 0]["SKU KEY"].nunique()
last_sync = df["DATE"].max()

# =========================
# Main Layout: Tabs
# =========================
overview_tab, detail_tab = st.tabs(["Overview Dashboard", "Product Detail Trend"])

# =========================
# Tab 1: Overview Dashboard
# =========================
with overview_tab:
    with st.container(border=True):
        st.markdown('<div class="section-kicker">Overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="main-title">Retail Pricing Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Live dashboard connected to Google Sheets</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="disclaimer">Target reflects selected store pricing; Walmart currently reflects online pricing unless location is confirmed.</div>',
            unsafe_allow_html=True
        )
        st.caption(
            f"Last updated from sheet: {last_sync.strftime('%Y-%m-%d %H:%M') if pd.notna(last_sync) else 'Unknown'}"
        )

        st.markdown("")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Tracked SKUs</div>
                    <div class="metric-value">{tracked_skus}</div>
                    <div class="metric-note">Active listings</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Average Current Price</div>
                    <div class="metric-value">{format_currency(avg_price)}</div>
                    <div class="metric-note">Across current selection</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Price Increases</div>
                    <div class="metric-value">{price_increases}</div>
                    <div class="metric-note">SKUs up vs previous pull</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Price Decreases</div>
                    <div class="metric-value">{price_decreases}</div>
                    <div class="metric-note">SKUs down vs previous pull</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with st.container(border=True):
        st.markdown('<div class="section-kicker">Watchlist</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Top Price Movers</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtext">Products showing the largest price movement versus the previous pull. If no history is available, latest tracked products are shown as baselines.</div>',
            unsafe_allow_html=True
        )

        movers = filtered_latest.copy()
        movers["ABS VARIANCE"] = movers["VARIANCE $"].abs()

        if movers["ABS VARIANCE"].notna().sum() == 0:
            movers = filtered_latest.sort_values("DATE", ascending=False).head(4)
        else:
            movers = movers.sort_values("ABS VARIANCE", ascending=False).head(4)

        if movers.empty:
            st.info("No products available under the current filters.")
        else:
            card_cols = st.columns(4)

            for idx, (_, row) in enumerate(movers.iterrows()):
                with card_cols[idx % 4]:
                    st.markdown(
                        f"""
                        <div class="product-card">
                            <div class="product-name">{row["PRODUCT NAME"]}</div>
                            <div class="product-sub">{row["BRAND"]} · {row["RETAILER"]} · {row["CATEGORY"]}</div>
                            <div class="product-price">{format_currency(row["PRICE"])}</div>
                            {variance_badge_html(row["VARIANCE $"], row["VARIANCE %"])}
                            <br>
                            {price_type_badge_html(row["PRICE TYPE"])}
                            <div class="small-muted">{row["LOCATION STATUS"]}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button("Open Detail", key=f"trend_card_{row['SKU KEY']}"):
                        st.session_state.selected_sku = row["SKU KEY"]
                        st.success("Product selected. Open the 'Product Detail Trend' tab to view the trend.")

    with st.container(border=True):
        st.markdown('<div class="section-kicker">Browse</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">All Tracked Products</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtext">Browse all currently tracked products under the selected filters.</div>',
            unsafe_allow_html=True
        )

        if filtered_latest.empty:
            st.info("No products match the selected filters.")
        else:
            display_table = filtered_latest[
                [
                    "PRODUCT NAME",
                    "BRAND",
                    "RETAILER",
                    "CATEGORY",
                    "PRICE",
                    "VARIANCE $",
                    "VARIANCE %",
                    "PRICE TYPE",
                    "LOCATION STATUS",
                    "DATE",
                ]
            ].copy()

            display_table["DATE"] = display_table["DATE"].dt.strftime("%Y-%m-%d %H:%M")
            display_table["PRICE"] = display_table["PRICE"].map(format_currency)
            display_table["VARIANCE $"] = display_table["VARIANCE $"].map(format_variance_dollar)
            display_table["VARIANCE %"] = display_table["VARIANCE %"].map(format_variance_percent)

            st.dataframe(display_table, use_container_width=True, hide_index=True)

# =========================
# Tab 2: Product Detail Trend
# =========================
with detail_tab:
    with st.container(border=True):
        st.markdown('<div class="section-kicker">Deep Dive</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Product Detail Trend</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtext">Select one product to inspect product-level price history and variance.</div>',
            unsafe_allow_html=True
        )

        if filtered_latest.empty:
            st.info("No products available under the current filters.")
            st.stop()

        selection_df = filtered_latest.copy()
        selection_df["DISPLAY LABEL"] = (
            selection_df["PRODUCT NAME"]
            + " | "
            + selection_df["BRAND"]
            + " | "
            + selection_df["RETAILER"]
        )

        label_list = selection_df.sort_values("DISPLAY LABEL")["DISPLAY LABEL"].tolist()

        default_index = 0
        if st.session_state.selected_sku:
            selected_label_from_card = selection_df.loc[
                selection_df["SKU KEY"] == st.session_state.selected_sku,
                "DISPLAY LABEL"
            ]
            if not selected_label_from_card.empty:
                selected_label_value = selected_label_from_card.iloc[0]
                if selected_label_value in label_list:
                    default_index = label_list.index(selected_label_value)

        selected_label = st.selectbox(
            "Select product",
            label_list,
            index=default_index
        )

        selected_key = selection_df.loc[
            selection_df["DISPLAY LABEL"] == selected_label,
            "SKU KEY"
        ].iloc[0]

        st.session_state.selected_sku = selected_key

    selected_history = filtered_history[
        filtered_history["SKU KEY"] == st.session_state.selected_sku
    ].sort_values("DATE")

    if selected_history.empty:
        st.warning("No historical records found for the selected product under the current filters.")
    else:
        selected_latest = selected_history.tail(1).iloc[0]

        product_label = (
            selected_latest["PRODUCT NAME"]
            + " | "
            + selected_latest["BRAND"]
            + " | "
            + selected_latest["RETAILER"]
        )

        with st.container(border=True):
            st.markdown('<div class="subsection-title">Snapshot</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="subsection-note">Current price, variance, and pricing-data quality for the selected product.</div>',
                unsafe_allow_html=True
            )

            detail_col1, detail_col2, detail_col3 = st.columns([1, 1, 2])

            with detail_col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Current Price</div>
                        <div class="metric-value">{format_currency(selected_latest["PRICE"])}</div>
                        <div class="metric-note">{selected_latest["BRAND"]} · {selected_latest["RETAILER"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with detail_col2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Variance</div>
                        <div class="metric-value">{format_variance_dollar(selected_latest["VARIANCE $"])}</div>
                        <div class="metric-note">{format_variance_percent(selected_latest["VARIANCE %"]) or "New baseline"}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with detail_col3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Data Quality</div>
                        <div style="margin-top:10px;">{price_type_badge_html(selected_latest["PRICE TYPE"])}</div>
                        <div class="metric-note" style="margin-top:10px;">{selected_latest["LOCATION STATUS"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with st.container(border=True):
            st.markdown('<div class="subsection-title">Historical Trend</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="subsection-note">{product_label}</div>',
                unsafe_allow_html=True
            )

            if selected_history.shape[0] < 2:
                st.markdown(
                    '<div class="soft-note">Baseline captured. Trend will become more meaningful after additional daily pulls.</div>',
                    unsafe_allow_html=True
                )

            st.plotly_chart(
                make_detail_chart(selected_history, product_label),
                use_container_width=True
            )

        with st.container(border=True):
            st.markdown('<div class="subsection-title">Historical Price Records</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="subsection-note">Record-level price history for the selected SKU.</div>',
                unsafe_allow_html=True
            )

            history_table = selected_history[
                [
                    "DATE",
                    "PRODUCT NAME",
                    "BRAND",
                    "RETAILER",
                    "CATEGORY",
                    "PRICE",
                    "VARIANCE $",
                    "VARIANCE %",
                    "PRICE TYPE",
                    "LOCATION STATUS",
                ]
            ].copy()

            history_table["DATE"] = history_table["DATE"].dt.strftime("%Y-%m-%d %H:%M")
            history_table["PRICE"] = history_table["PRICE"].map(format_currency)
            history_table["VARIANCE $"] = history_table["VARIANCE $"].map(format_variance_dollar)
            history_table["VARIANCE %"] = history_table["VARIANCE %"].map(format_variance_percent)

            st.dataframe(history_table, use_container_width=True, hide_index=True)
