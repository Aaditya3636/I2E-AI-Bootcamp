import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(layout="wide")

uploaded_file = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data.csv")

st.markdown("""
<style>
[data-testid="stMetric"] {
    background-color: #f6f9fc;
    border: 1px solid #d6dde6;
    border-radius: 10px;
    padding: 6px;
}

/* KPI label */
[data-testid="stMetric"] label {
    font-size: 12px !important;
}

/* KPI value */
[data-testid="stMetric"] div {
    font-size: 18px !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)
# Load data
df = pd.read_csv("data.csv")

# ✅ Sidebar (Enhanced Title)
st.sidebar.markdown(
    """
    <div style="
        font-size:20px;
        font-weight:700;
        text-align:center;
        padding:10px;
        background-color:#f0f2f6;
        border-radius:10px;
        margin-bottom:10px;
    ">
        Clinical Trial Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

# Filters
region_filter = st.sidebar.multiselect("Select Region", df["Region"].unique())
category_filter = st.sidebar.multiselect("Select Category", df["Category"].unique())
phase_filter = st.sidebar.multiselect("Select Phase", df["Phase"].unique())
status_filter = st.sidebar.multiselect("Select Status", df["Status"].unique())

# Apply filters
filtered_df = df.copy()

if region_filter:
    filtered_df = filtered_df[filtered_df["Region"].isin(region_filter)]

if category_filter:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]

if phase_filter:
    filtered_df = filtered_df[filtered_df["Phase"].isin(phase_filter)]

if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]


# ✅ KPI SECTION
st.markdown("## 📊 KPIs")

total_studies = len(filtered_df)
total_budget = filtered_df["Total Budget"].sum()
avg_allocation = filtered_df["Allocation %"].str.replace('%', '').astype(float).mean()

on_track = filtered_df[filtered_df["Status"] == "On Track"].shape[0]
on_track_pct = (on_track / total_studies) * 100 if total_studies > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("📌 Total Studies", total_studies)
col2.metric("💰 Total Budget ($)", f"{total_budget:,.0f}")
col3.metric("📊 Avg Allocation", f"{avg_allocation:.1f}%")
col4.metric("✅ On Track Studies", f"{on_track_pct:.1f}%")

st.markdown("---")

# ✅ CHARTS SECTION
st.markdown("## 📈 Study Insights")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):

        # Title
        st.markdown(
            """
            <div style="
                background-color:#eef3f8;
                padding:6px;
                border-radius:6px;
                text-align:center;
                font-weight:600;
                margin-bottom:4px;
            ">
                Study Status Distribution
            </div>
            """,
            unsafe_allow_html=True
        )

        # Data
        status_counts = filtered_df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]

        # Pie Chart
        fig = px.pie(
            status_counts,
            names="Status",
            values="Count",
            color="Status",
            color_discrete_map={
                "On Track": "#2ecc71",
                "At Risk": "#e74c3c",
                "Off Track": "#f39c12",
                "Completed": "#3498db"
            }
        )

        # Remove padding + hide legend
        fig.update_layout(
            margin=dict(t=5, b=5, l=5, r=5),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

with col2:
    with st.container(border=True):

        # ✅ Consistent light header (same as pie chart)
        st.markdown(
            """
            <div style="
                background-color:#eef3f8;
                padding:6px;
                border-radius:6px;
                text-align:center;
                font-weight:600;
                margin-bottom:4px;
            ">
                Study Distribution by Category
            </div>
            """,
            unsafe_allow_html=True
        )

        # ✅ Prepare data
        category_counts = filtered_df["Category"].value_counts().reset_index()
        category_counts.columns = ["Category", "Count"]

        # ✅ Plotly bar chart (light color)
        fig_cat = px.bar(
            category_counts,
            x="Category",
            y="Count",
            color="Category",
            color_discrete_sequence=["#85c1e9"]  # ✅ light soft blue
        )

        # ✅ Layout consistency
        fig_cat.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False
        )

        st.plotly_chart(fig_cat, use_container_width=True)

st.markdown("---")

with st.container(border=True):
    st.markdown("### 🔍 Key Insight")

    if total_studies > 0:
        st.write(
            f"{on_track_pct:.1f}% of studies are currently on track. "
            f"Focus is heavily on {filtered_df['Category'].mode()[0]} category."
        )


# ✅ TABLE SECTION
selected_columns = [
    "Study Id",
    "Product / Asset",
    "Region",
    "Phase",
    "Status",
    "Allocation %"
]

    
st.markdown("## 📋 Study Details")
st.dataframe(filtered_df[selected_columns], use_container_width=True)

st.info("This dashboard provides a high-level overview of clinical studies, including performance metrics, study distribution, and operational insights.")
