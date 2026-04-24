import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

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
# Your Google Sheet:
# https://docs.google.com/spreadsheets/d/1tomybUYyC7rAa7O7VGpyrxdWOjYLnFmheFvKk04sSDc/edit?usp=sharing
#
# This assumes the data is on the first tab / gid=0.
# If your data is on another tab, replace gid=0 with the correct gid.
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
    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .title {
        font-size: 34px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 4px;
    }

    .disclaimer {
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 24px;
    }

    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        min-height: 120px;
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
        margin-top: 4px;
    }

    .section-title {
        font-size: 20px;
        color: #0f172a;
        font-weight: 800;
        margin-top: 24px;
        margin-bottom: 12px;
    }

    .product-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        min-height: 270px;
    }

    .product-name {
        font-size: 15px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2px;
    }

    .product-sub {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 8px;
    }

    .product-price {
        font-size: 24px;
        color: #0f172a;
        font-weight: 800;
        margin-top: 6px;
    }

    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        margin-top: 6px;
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
        margin-top: 6px;
    }

    .filter-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
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

    # Clean column names
    df.columns = [c.strip().upper() for c in df.columns]

    # Required fields fallback
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

    # Parse date
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

    # Clean price
    df["PRICE"] = (
        df["PRICE"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["PRICE"] = pd.to_numeric(df["PRICE"], errors="coerce")

    # Drop bad rows
    df = df.dropna(subset=["DATE", "PRODUCT NAME", "RETAILER", "PRICE"])

    # Standard text fields
    for col in ["BRAND", "PRODUCT NAME", "RETAILER", "CATEGORY", "PRICE TYPE", "LOCATION STATUS"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Unique product key
    df["SKU KEY"] = (
        df["PRODUCT NAME"].astype(str)
        + " | "
        + df["RETAILER"].astype(str)
        + " | "
        + df["BRAND"].astype(str)
    )

    # Sort for variance calculation
    df = df.sort_values(["SKU KEY", "DATE"])

    # If variance columns already exist, use them.
    # Otherwise calculate variance from previous price for the same SKU KEY.
    if "VARIANCE $" not in df.columns:
        df["PREVIOUS PRICE"] = df.groupby("SKU KEY")["PRICE"].shift(1)
        df["VARIANCE $"] = df["PRICE"] - df["PREVIOUS PRICE"]
    else:
        df["VARIANCE $"] = pd.to_numeric(df["VARIANCE $"], errors="coerce")
        df["PREVIOUS PRICE"] = df["PRICE"] - df["VARIANCE $"]

    if "VARIANCE %" not in df.columns:
        df["VARIANCE %"] = df["VARIANCE $"] / df["PREVIOUS PRICE"]
    else:
        df["VARIANCE %"] = (
            df["VARIANCE %"]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.strip()
        )
        df["VARIANCE %"] = pd.to_numeric(df["VARIANCE %"], errors="coerce")

        # If the sheet stores 5.1 instead of 0.051, normalize it.
        if df["VARIANCE %"].dropna().abs().max() is not None:
            if df["VARIANCE %"].dropna().abs().max() > 1:
                df["VARIANCE %"] = df["VARIANCE %"] / 100

    return df


def get_latest_rows(df):
    latest = (
        df.sort_values("DATE")
        .groupby("SKU KEY", as_index=False)
        .tail(1)
        .sort_values(["RETAILER", "BRAND", "PRODUCT NAME"])
    )
    return latest


def format_currency(value):
    if pd.isna(value):
        return "—"
    return f"${value:,.2f}"


def format_variance_dollar(value):
    if pd.isna(value):
        return "New"
    sign = "+" if value > 0 else ""
    return f"{sign}${value:,.2f}"


def format_variance_percent(value):
    if pd.isna(value):
        return ""
    sign = "+" if value > 0 else ""
    return f"{sign}{value * 100:.1f}%"


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


def make_mini_chart(history_df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["DATE"],
            y=history_df["PRICE"],
            mode="lines+markers",
            line=dict(width=2),
            marker=dict(size=5),
            hovertemplate="%{x|%b %d, %Y}<br>$%{y:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        height=110,
        margin=dict(l=0, r=0, t=5, b=5),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    return fig


def make_detail_chart(history_df, product_label):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["DATE"],
            y=history_df["PRICE"],
            mode="lines+markers",
            line=dict(width=3),
            marker=dict(size=7),
            hovertemplate="%{x|%b %d, %Y %I:%M %p}<br>$%{y:.2f}<extra></extra>",
            name=product_label,
        )
    )

    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Date",
        yaxis_title="Price",
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
    )

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

# =========================
# Header
# =========================
st.markdown('<div class="title">Retail Pricing Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Live dashboard connected to Google Sheets</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="disclaimer">Target reflects selected store pricing; Walmart currently reflects online pricing unless location is confirmed.</div>',
    unsafe_allow_html=True
)

last_sync = df["DATE"].max()
st.caption(f"Last updated from sheet: {last_sync.strftime('%Y-%m-%d %H:%M') if pd.notna(last_sync) else 'Unknown'}")

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# Sidebar filters
# =========================
st.sidebar.header("Refine Data")

category_options = sorted(latest["CATEGORY"].dropna().unique().tolist())
retailer_options = sorted(latest["RETAILER"].dropna().unique().tolist())
brand_options = sorted(latest["BRAND"].dropna().unique().tolist())
price_type_options = sorted(latest["PRICE TYPE"].dropna().unique().tolist())

selected_categories = st.sidebar.multiselect("Category", category_options, default=category_options)
selected_retailers = st.sidebar.multiselect("Retailer", retailer_options, default=retailer_options)
selected_brands = st.sidebar.multiselect("Brand", brand_options, default=brand_options)
selected_price_types = st.sidebar.multiselect("Price Type", price_type_options, default=price_type_options)

filtered_latest = latest[
    latest["CATEGORY"].isin(selected_categories)
    & latest["RETAILER"].isin(selected_retailers)
    & latest["BRAND"].isin(selected_brands)
    & latest["PRICE TYPE"].isin(selected_price_types)
].copy()

filtered_keys = filtered_latest["SKU KEY"].unique().tolist()
filtered_history = df[df["SKU KEY"].isin(filtered_keys)].copy()

# =========================
# KPI Cards
# =========================
tracked_skus = filtered_latest["SKU KEY"].nunique()
avg_price = filtered_latest["PRICE"].mean()

price_increases = filtered_latest[filtered_latest["VARIANCE $"] > 0]["SKU KEY"].nunique()
price_decreases = filtered_latest[filtered_latest["VARIANCE $"] < 0]["SKU KEY"].nunique()

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
            <div class="metric-note">Across selection</div>
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
            <div class="metric-note">Vs previous pull</div>
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
            <div class="metric-note">Vs previous pull</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# Top Movers
# =========================
st.markdown('<div class="section-title">Top Price Movers</div>', unsafe_allow_html=True)

movers = filtered_latest.copy()
movers["ABS VARIANCE"] = movers["VARIANCE $"].abs()
movers = movers.sort_values("ABS VARIANCE", ascending=False)

# If no variance yet, show latest products instead
if movers["ABS VARIANCE"].notna().sum() == 0:
    movers = filtered_latest.sort_values("DATE", ascending=False).head(4)
else:
    movers = movers.head(4)

if movers.empty:
    st.info("No products available under the current filters.")
else:
    card_cols = st.columns(4)

    for idx, (_, row) in enumerate(movers.iterrows()):
        with card_cols[idx % 4]:
            history = filtered_history[filtered_history["SKU KEY"] == row["SKU KEY"]].sort_values("DATE")

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

            st.plotly_chart(make_mini_chart(history), use_container_width=True)

# =========================
# Product Detail Trend
# =========================
st.markdown('<div class="section-title">Product Detail Trend</div>', unsafe_allow_html=True)

product_options = (
    filtered_latest.assign(
        DISPLAY_LABEL=lambda x: x["PRODUCT NAME"] + " | " + x["BRAND"] + " | " + x["RETAILER"]
    )
    .sort_values("DISPLAY_LABEL")
)

if product_options.empty:
    st.info("No product detail available under the current filters.")
else:
    selected_label = st.selectbox(
        "Select a product to view historical trend",
        product_options["DISPLAY_LABEL"].tolist()
    )

    selected_key = product_options.loc[
        product_options["DISPLAY_LABEL"] == selected_label,
        "SKU KEY"
    ].iloc[0]

    selected_history = filtered_history[
        filtered_history["SKU KEY"] == selected_key
    ].sort_values("DATE")

    selected_latest = selected_history.tail(1).iloc[0]

    detail_col1, detail_col2, detail_col3 = st.columns([1, 1, 2])

    with detail_col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Current Price</div>
                <div class="metric-value">{format_currency(selected_latest["PRICE"])}</div>
                <div class="metric-note">{selected_latest["PRODUCT NAME"]}</div>
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

    st.plotly_chart(make_detail_chart(selected_history, selected_label), use_container_width=True)

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

# =========================
# Full Detail Table
# =========================
st.markdown('<div class="section-title">Price Detail Table</div>', unsafe_allow_html=True)

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