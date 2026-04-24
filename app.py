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
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* ===== General Typography ===== */
    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2px;
    }

    .subtitle {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 4px;
    }

    .disclaimer {
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 8px;
    }

    .section-kicker {
        display: inline-block;
        font-size: 11px;
        font-weight: 800;
        color: #334155;
        background: #eef2ff;
        border: 1px solid #dbeafe;
        border-radius: 999px;
        padding: 5px 10px;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .section-title {
        font-size: 22px;
        color: #0f172a;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .section-subtext {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 16px;
    }

    .subsection-title {
        font-size: 16px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 6px;
    }

    .subsection-note {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 12px;
    }

    /* ===== Main bordered containers ===== */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #dbe2ea !important;
        border-radius: 18px !important;
        background: #ffffff !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    /* ===== Metric Card ===== */
    .metric-card {
        background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
        border: 1px solid #dbe2ea;
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 126px;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
        position: relative;
    }

    .metric-card:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        height: 4px;
        width: 100%;
        border-radius: 16px 16px 0 0;
        background: #dbeafe;
    }

    .metric-label {
        font-size: 12px;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .metric-value {
        font-size: 34px;
        color: #0f172a;
        font-weight: 800;
        margin-top: 10px;
    }

    .metric-note {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 6px;
        line-height: 1.4;
    }

    /* ===== Product Cards ===== */
    .product-card {
        background: #ffffff;
        border: 1px solid #dbe2ea;
        border-radius: 16px;
        padding: 18px;
        min-height: 245px;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
    }

    .product-name {
        font-size: 16px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2px;
    }

    .product-sub {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 10px;
    }

    .product-price {
        font-size: 25px;
        color: #0f172a;
        font-weight: 800;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .badge {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        margin-top: 5px;
        margin-right: 5px;
    }

    .badge-green {
        background: #dcfce7;
        color: #166534;
    }

    .badge-red {
        background: #fee2e2;
        color: #991b1b;
    }

    .badge-gray {
        background: #f1f5f9;
        color: #475569;
    }

    .badge-blue {
        background: #dbeafe;
        color: #1d4ed8;
    }

    .small-muted {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 9px;
        line-height: 1.45;
    }

    .soft-note {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
        border-radius: 12px;
        padding: 12px 14px;
        font-size: 13px;
        margin-top: 10px;
        margin-bottom: 14px;
    }

    .helper-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }

    .helper-box-title {
        font-size: 13px;
        font-weight: 800;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 5px;
    }

    .helper-box-note {
        font-size: 12px;
        color: #64748b;
        line-height: 1.5;
    }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-title {
        font-size: 18px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2px;
    }

    .sidebar-sub {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 12px;
    }

    .filter-group-title {
        font-size: 12px;
        font-weight: 800;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 2px;
    }

    .filter-group-note {
        font-size: 11px;
        color: #94a3b8;
        margin-bottom: 10px;
    }

    /* buttons */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        color: #0f172a;
        font-weight: 600;
        background: #ffffff;
    }

    .stButton > button:hover {
        border-color: #2563eb;
        color: #2563eb;
        background: #f8fbff;
    }

    /* dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 24px 0;
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

    # variance $
    df["PREVIOUS PRICE"] = df.groupby("SKU KEY")["PRICE"].shift(1)
    df["VARIANCE $"] = df["PRICE"] - df["PREVIOUS PRICE"]

    # variance %
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
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate="%{x|%b %d, %Y %I:%M %p}<br>$%{y:.2f}<extra></extra>",
            name=product_label,
        )
    )

    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Date",
        yaxis_title="Price",
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        showlegend=False,
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#e5e7eb")

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
        '<div class="sidebar-sub">Use the filters below to narrow the SKU view.</div>',
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
# Section 1: Overview
# =========================
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

# =========================
# Section 2: Top Price Movers
# =========================
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
                with st.container(border=True):
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

                    if st.button("View Trend", key=f"trend_card_{row['SKU KEY']}"):
                        st.session_state.selected_sku = row["SKU KEY"]
                        st.rerun()

# =========================
# Section 3: All Products
# =========================
with st.container(border=True):
    st.markdown('<div class="section-kicker">Browse</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">All Tracked Products</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtext">Browse all currently tracked products. Select one product to inspect detailed price history below.</div>',
        unsafe_allow_html=True
    )

    if filtered_latest.empty:
        st.info("No products match the selected filters.")
    else:
        selection_df = filtered_latest.copy()
        selection_df["DISPLAY LABEL"] = (
            selection_df["PRODUCT NAME"]
            + " | "
            + selection_df["BRAND"]
            + " | "
            + selection_df["RETAILER"]
        )

        with st.container(border=True):
            st.markdown('<div class="subsection-title">Product Selector</div>', unsafe_allow_html=True)
            st.markdown('<div class="subsection-note">Choose one product and open the product-level trend detail.</div>', unsafe_allow_html=True)

            selector_col, button_col = st.columns([5, 1])

            with selector_col:
                selected_label = st.selectbox(
                    "Select a product to inspect trend",
                    selection_df.sort_values("DISPLAY LABEL")["DISPLAY LABEL"].tolist(),
                    index=0,
                    label_visibility="collapsed"
                )

            with button_col:
                st.write("")
                if st.button("View Selected Trend"):
                    selected_key = selection_df.loc[
                        selection_df["DISPLAY LABEL"] == selected_label,
                        "SKU KEY"
                    ].iloc[0]
                    st.session_state.selected_sku = selected_key
                    st.rerun()

        with st.container(border=True):
            st.markdown('<div class="subsection-title">Current Product Table</div>', unsafe_allow_html=True)
            st.markdown('<div class="subsection-note">Latest available price record for each tracked SKU under the current filters.</div>', unsafe_allow_html=True)

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
# Section 4: Product Detail Trend
# =========================
if st.session_state.selected_sku:
    selected_sku = st.session_state.selected_sku

    if selected_sku not in filtered_history["SKU KEY"].unique():
        with st.container(border=True):
            st.warning("The selected product is no longer available under the current filters.")
    else:
        selected_history = filtered_history[
            filtered_history["SKU KEY"] == selected_sku
        ].sort_values("DATE")

        selected_latest = selected_history.tail(1).iloc[0]

        product_label = (
            selected_latest["PRODUCT NAME"]
            + " | "
            + selected_latest["BRAND"]
            + " | "
            + selected_latest["RETAILER"]
        )

        with st.container(border=True):
            st.markdown('<div class="section-kicker">Deep Dive</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Product Trend Detail</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="section-subtext">{product_label}</div>',
                unsafe_allow_html=True
            )

            # Snapshot block
            with st.container(border=True):
                st.markdown('<div class="subsection-title">Snapshot</div>', unsafe_allow_html=True)
                st.markdown('<div class="subsection-note">Current view of price, variance, and pricing-data quality for the selected product.</div>', unsafe_allow_html=True)

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

            # Trend chart block
            with st.container(border=True):
                st.markdown('<div class="subsection-title">Historical Trend</div>', unsafe_allow_html=True)
                st.markdown('<div class="subsection-note">Trend line of the selected product based on historical pulls.</div>', unsafe_allow_html=True)

                if selected_history.shape[0] < 2:
                    st.markdown(
                        '<div class="soft-note">Baseline captured. Trend will become more meaningful after additional daily pulls.</div>',
                        unsafe_allow_html=True
                    )

                st.plotly_chart(
                    make_detail_chart(selected_history, product_label),
                    use_container_width=True
                )

            # Historical table block
            with st.container(border=True):
                st.markdown('<div class="subsection-title">Historical Price Records</div>', unsafe_allow_html=True)
                st.markdown('<div class="subsection-note">Record-level history for the selected SKU.</div>', unsafe_allow_html=True)

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

            bottom_col1, bottom_col2 = st.columns([1, 6])
            with bottom_col1:
                if st.button("Hide Trend Detail"):
                    st.session_state.selected_sku = None
                    st.rerun()

else:
    with st.container(border=True):
        st.markdown('<div class="section-kicker">Deep Dive</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Product Trend Detail</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtext">Select a product from Top Price Movers or All Tracked Products to inspect product-level price history.</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="helper-box">
                <div class="helper-box-title">How to use this section</div>
                <div class="helper-box-note">
                    1) Review the overview and top movers above.<br>
                    2) Click “View Trend” on a mover card, or choose a product from the selector.<br>
                    3) The selected product’s snapshot, trend chart, and price history will appear here.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
