import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    layout="wide",
    page_title="Medical Affairs Study Dashboard"
)

# =====================================================
# GLOBAL CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
MAIN APP
===================================================== */

.stApp {
    background-color: #f5f7fb;
}

/* =====================================================
REDUCE MAIN PAGE SIDE PADDING (~70%)
===================================================== */

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 100% !important;
}

/* =====================================================
SIDEBAR WIDTH REDUCED (~25%)
===================================================== */

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] > div:first-child {
    width: 250px !important;
    padding-right: 0.10rem !important;
    padding-left: 0.55rem !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-right: 0.2rem !important;
    padding-left: 0.45rem !important;
}
section[data-testid="stSidebar"] .stMultiSelect {
    padding-right: 0rem !important;
}              

/* =====================================================
SIDEBAR HEADER
===================================================== */

.filter-header {
    font-size: 22px;
    font-weight: 600;
    color: #111827;
    margin-top: 10px;
    margin-bottom: 18px;
}

/* =====================================================
FILTER LABELS
===================================================== */

section[data-testid="stSidebar"] label {
    font-size: 12px !important;
    font-weight: 400 !important;
    color: #3B7597 !important;
}

/* =====================================================
SECTION TITLES
===================================================== */

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
}

.section-subtitle {
    font-size: 13px;
    color: #111827;
    margin-top: -10px;
    margin-bottom: 10px;
}

/* =====================================================
KPI CARDS
===================================================== */

.kpi-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 6px;
    margin-bottom: 10px;
}

.kpi-label {
    font-size: 12px;
    font-weight: 600;
    color: #093C5D;
    margin-bottom: 0px;
    padding-left: 10px;
}

.kpi-value {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    padding-left: 10px;
}

.kpi-sub {
    font-size: 12px;
    font-weight: 600;
    color: #3B7597;
    margin-top: 0px;
    padding-left: 10px;
}

/* =====================================================
CHART TITLE
===================================================== */

.card-title {
    font-size: 17px;
    font-weight: 500;
    color: #F5F5F5;
    background-color: #3B7597;
    padding: 4px 14px;
    margin: 0px;
    border-bottom: 1px solid #bfdbfe;
    border-radius: 10px 10px 0px 0px;
}


/* =====================================================
PAGE TABS
===================================================== */

button[data-baseweb="tab"] {
    padding-top: 12px !important;
    padding-bottom: 6px !important;
    margin-right: 24px !important;
    border-bottom: none !important;
}

/* TAB TEXT */
button[data-baseweb="tab"] p {
    font-size: 16px !important;
    font-weight: 400 !important;
    color: #6b7280 !important;
    margin: 0px !important;
}

/* HOVER */
button[data-baseweb="tab"]:hover p {
    color: #1d4ed8 !important;
}

/* ACTIVE TAB */
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #1d4ed8 !important;
    font-weight: 700 !important;
}

button[data-baseweb="tab"]:hover {
    color: #1d4ed8 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #1d4ed8 !important;
    font-weight: 700 !important;
    border-bottom: 3px solid #1d4ed8 !important;
}

/* REMOVE STREAMLIT DEFAULT RED LINE */
button[data-baseweb="tab"]::after {
    display: none !important;
}

/* ADD SPACE BETWEEN TITLE & TABS */
div[data-testid="stTabs"] {
    margin-top: 14px !important;
}

/* REMOVE DEFAULT STREAMLIT TAB BORDER */
div[data-testid="stTabs"] ul {
    border-bottom: transparent !important;
    box-shadow: none !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 24px;
    border-bottom: none !important;
    box-shadow: none !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background-color: transparent !important;
} 
/* REMOVE LINE BETWEEN TABS AND PAGE CONTENT */
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

.stTabs div[role="tabpanel"] {
    border-top: none !important;
}           

/* =====================================================
REMOVE EXTRA VERTICAL SPACING
===================================================== */

div[data-testid="stVerticalBlock"] > div {
    padding-top: 0rem;
    padding-bottom: 0rem;
}

/* =====================================================
GANTT NAVIGATION BUTTONS
===================================================== */

button[kind="secondary"] {
    border-radius: 8px !important;
}

div[data-testid="column"] button[kind="secondary"] {
    background-color: #e0f2fe !important;
    border: 1px solid #bae6fd !important;
    color: #0369a1 !important;
    height: 40px !important;
    min-height: 34px !important;
    padding: 0px !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    box-shadow: none !important;
}

div[data-testid="column"] button[kind="secondary"]:hover {
    background-color: #bae6fd !important;
    border: 1px solid #7dd3fc !important;
}         

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("data.csv")


# =====================================================
# DATE PARSING
# =====================================================

for col in ["Study Start", "Study End", "Readout"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div style="
        font-size:30px;
        font-weight:700;
        color:#1d4ed8;
        margin-top:20px;
        margin-bottom:-40px;
    ">
        Medical Affairs Study Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# =====================================================
# PAGE NAVIGATION
# =====================================================

tab1, tab2 = st.tabs([
    "Executive Overview",
    "Portfolio Schedule"
])

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:20px;
        font-weight:600;
        color:#093C5D;
        letter-spacing:0.3px;
        margin-top:-6px;
        margin-bottom:10px;
        padding-bottom:6px;
        border-bottom:1px solid #dbe4ee;
    ">
        Filter Section
    </div>
    """,
    unsafe_allow_html=True
)

region_filter = st.sidebar.multiselect(
    "Regions",
    sorted(df["Region"].dropna().unique())
)

category_filter = st.sidebar.multiselect(
    "Indications",
    sorted(df["Category"].dropna().unique())
)

phase_filter = st.sidebar.multiselect(
    "Phase",
    sorted(df["Phase"].dropna().unique())
)

status_filter = st.sidebar.multiselect(
    "Status",
    sorted(df["Status"].dropna().unique())
)

# =====================================================
# FILTER LOGIC
# =====================================================

filtered_df = df.copy()

if region_filter:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(region_filter)
    ]

if category_filter:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(category_filter)
    ]

if phase_filter:
    filtered_df = filtered_df[
        filtered_df["Phase"].isin(phase_filter)
    ]

if status_filter:
    filtered_df = filtered_df[
        filtered_df["Status"].isin(status_filter)
    ]

# =====================================================
# KPI FUNCTION
# =====================================================

def kpi(col, label, value, sub=""):

    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# PAGE CONTAINER
# Prevents flash while switching pages
# =====================================================


# =====================================================
# EXECUTIVE OVERVIEW
# =====================================================
with tab1:

        st.markdown(
            '<div class="section-subtitle">Portfolio-wide clinical study performance and financial health metrics.</div>',
            unsafe_allow_html=True
        )

        total_studies = len(filtered_df)

        total_budget = filtered_df["Total Budget"].sum()

        total_allocated = filtered_df["Allocated Budget"].sum()

        percent_allocated = (
            (total_allocated / total_budget) * 100
            if total_budget > 0 else 0
        )

        on_track = filtered_df[
            filtered_df["Status"] == "On Track"
        ].shape[0]

        active_regions = filtered_df["Region"].nunique()

        k1, k2, k3, k4 = st.columns(4)

        kpi(
            k1,
            "TOTAL BUDGET",
            f"${total_budget/1e6:.1f}M",
            "+4.2% vs last quarter"
        )

        kpi(
            k2,
            "ALLOCATED BUDGET",
            f"${total_allocated/1_000_000:.1f}M",
            f"{percent_allocated:.0f}% of total"
        )

        kpi(
            k3,
            "TOTAL STUDIES",
            total_studies,
            f"{on_track} On Track"
        )

        kpi(
            k4,
            "ACTIVE REGIONS",
            active_regions,
            "Global operations"
        )

        # =====================================================
        # CHARTS
        # =====================================================

        c1, c2 = st.columns(2)

        # =====================================================
        # DONUT CHART
        # =====================================================

        with c1:

            st.markdown(
                '<div class="card-title">Studies by Status</div>',
                unsafe_allow_html=True
            )

            status_counts = (
                filtered_df["Status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "Status",
                "Count"
            ]

            # ✅ SAME COLOR MAP AS REGION CHART
            status_color_map = {
                "On Track": "#3b82f6",
                "At Risk": "#f59e0b",
                "Off Track": "#ef4444",
                "Completed": "#6b7280",
                "Planning": "#93c5fd"
            }

            fig = px.pie(
                status_counts,
                names="Status",
                values="Count",
                hole=0.62,
                color="Status",
                color_discrete_map=status_color_map   # ✅ THIS FIXES IT
            )


            fig.update_traces(
                textinfo="percent",
                texttemplate="%{percent} (%{value})",

                # ✅ THIS CONTROLS HOVER
                hovertemplate="%{label}<extra></extra>"
            )


            fig.update_layout(
                margin=dict(t=20, b=40, l=20, r=20),
                height=300,
                paper_bgcolor="#ffffff",
                plot_bgcolor="#ffffff"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # =====================================================
        # REGION CHART
        # =====================================================

        with c2:

            st.markdown(
                '<div class="card-title">Studies by Region</div>',
                unsafe_allow_html=True
            )

            region_status_counts = (
                filtered_df
                .groupby(["Region", "Status"])
                .size()
                .reset_index(name="Count")
            )

            fig_bar = px.bar(
                region_status_counts,
                x="Region",
                y="Count",
                color="Status",
                text="Count",
                color_discrete_map={
                    "On Track": "#3b82f6",
                    "At Risk": "#f59e0b",
                    "Off Track": "#ef4444",
                    "Completed": "#6b7280",
                    "Planning": "#93c5fd"
                }
            )

            fig_bar.update_traces(
                width=0.45,
                textposition="inside",
                textfont=dict(
                    size=11,
                    color="white"
                ),
                hovertemplate=(
                    "Region: %{x}<br>"
                    "Status: %{fullData.name}"
                    "<extra></extra>"
                )
            )

            fig_bar.update_layout(
                barmode="stack",
                margin=dict(t=20, b=40, l=20, r=20),
                height=300,
                paper_bgcolor="#ffffff",
                plot_bgcolor="#ffffff",
                legend_title="Status"
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )

        # =====================================================
        # HIGH PRIORITY TITLE
        # =====================================================

        st.markdown(
            '<div class="card-title" style="margin-top:10px;">High Priority Studies</div>',
            unsafe_allow_html=True
        )

        # =====================================================
        # TABLE
        # =====================================================

        table_df = filtered_df.reset_index(drop=True)

        def get_status_color(status):
            return {
                "On Track": "#3b82f6",
                "At Risk": "#f59e0b",
                "Off Track": "#ef4444",
                "Planning": "#9ca3af",
                "Completed": "#6b7280"
            }.get(status, "#9ca3af")

        html = """
        <div style="
            font-family: Arial, sans-serif;
            background:#ffffff;
            border:1px solid #e5e7eb;
            border-top:none;
            border-radius:0px 0px 10px 10px;
            height:330px;
            overflow:hidden;
            box-sizing:border-box;
        ">

            <div style="
                height:330px;
                overflow-y:auto;
                box-sizing:border-box;
            ">

                <div style="
                    display:grid;
                    grid-template-columns: 1.45fr 1fr 1.35fr 1.35fr 1.8fr 1fr;
                    align-items:center;
                    padding:10px 12px;
                    font-size:14px;
                    font-weight:600;
                    color:#6b7280;
                    border-bottom:1px solid #e5e7eb;
                    background:#ffffff;
                    position:sticky;
                    top:0;
                    z-index:10;
                    gap:6px;
                ">

                    <div>Study ID</div>
                    <div>Strategic Imperative</div>
                    <div>Product</div>
                    <div>Indication</div>                    
                    <div>Budget Allocation</div>
                    <div>Status</div>

                </div>
        """

        for i, row in table_df.iterrows():

            status_color = get_status_color(row["Status"])

            alloc = float(
                str(row["Allocation %"]).replace("%", "")
            )

            html += f"""
                <div style="
                    display:grid;
                    grid-template-columns: 1.45fr 1fr 1.35fr 1.35fr 1.8fr 1fr;
                    align-items:center;
                    padding:12px;
                    border-bottom:1px solid #f1f5f9;
                    box-sizing:border-box;
                    gap:6px;
                ">

                    <div style="
                        display:flex;
                        align-items:flex-start;
                        gap:6px;
                        min-width:0;
                    ">

                        <div style="
                            background:#1f4e79;
                            color:white;
                            font-size:10px;
                            padding:5px 7px;
                            border-radius:6px;
                            flex-shrink:0;
                            margin-top:2px;
                        ">
                            {str(i + 1).zfill(2)}
                        </div>

                        <div style="min-width:0;">

                            <div style="
                                font-size:13px;
                                font-weight:600;
                                line-height:1.3;
                                word-break:break-word;
                            ">
                                {row['Study Id']}
                            </div>

                            <div style="
                                font-size:11px;
                                color:#6b7280;
                                margin-top:2px;
                            ">
                                {row['Phase']}
                            </div>

                        </div>

                    </div>

                    <div style="
                        font-size:12px;
                        line-height:1.4;
                        word-break:break-word;
                    ">
                        {row['Strategic Imperative']}
                    </div>

                    <div style="
                        font-size:12px;
                        line-height:1.4;
                        word-break:break-word;
                    ">
                        {row['Product']}
                    </div>

                    <div style="
                        font-size:12px;
                        line-height:1.4;
                        word-break:break-word;
                    ">
                        {row['Indication']}
                    </div>

                    <div style="
                        padding-right:4px;
                    ">

                        <div style="
                            font-size:12px;
                            margin-bottom:4px;
                        ">
                            ${row['Allocated Budget']:,.0f} ({alloc:.0f}%)
                        </div>

                        <div style="
                            background:#e5e7eb;
                            height:6px;
                            border-radius:4px;
                            overflow:hidden;
                        ">

                            <div style="
                                width:{alloc}%;
                                background:#1f4e79;
                                height:6px;
                                border-radius:4px;
                            ">
                            </div>

                        </div>

                    </div>

                    <div>

                        <span style="
                            background:{status_color}20;
                            color:{status_color};
                            padding:4px 8px;
                            border-radius:12px;
                            font-size:11px;
                            font-weight:600;
                            display:inline-block;
                            text-align:center;
                        ">
                            {row['Status'].upper()}
                        </span>

                    </div>

                </div>
            """

        html += """
            </div>
        </div>
        """

        components.html(
            html,
            height=340,
            scrolling=False
        )

    # =====================================================
    # PORTFOLIO SCHEDULE
    # =====================================================

with tab2:

        st.markdown(
            '<div class="section-subtitle">Multi-year roadmap for clinical trials.</div>',
            unsafe_allow_html=True
        )

        portfolio_total = len(filtered_df)

        active_timelines = filtered_df[
            filtered_df["Status"] != "Completed"
        ].shape[0]

        upcoming_readouts = filtered_df[
            filtered_df["Readout"] >= pd.Timestamp.today()
        ].shape[0]

        total_enrolled = pd.to_numeric(
            filtered_df["Enrolled"],
            errors="coerce"
        ).fillna(0).sum()

        total_target = pd.to_numeric(
            filtered_df["Patient"],
            errors="coerce"
        ).fillna(0).sum()

        enrollment_progress = round(
            (
                total_enrolled
                /
                max(total_target, 1)
            ) * 100,
            1
        )

        today = pd.Timestamp.today()

        overdue_studies = filtered_df[
            (
                filtered_df["Study End"] < today
            )
            &
            (
                filtered_df["Status"] != "Completed"
            )
        ].shape[0]

        # =====================================================
        # KPI ROW
        # =====================================================

        k1, k2, k3, k4 = st.columns(4)

        kpi(
            k1,
            "ACTIVE TIMELINES",
            f"{active_timelines} / {portfolio_total}",
            "Studies currently active"
        )

        kpi(
            k2,
            "UPCOMING READOUTS",
            upcoming_readouts,
            "Upcoming expected readouts"
        )

        kpi(
            k3,
            "ENROLLMENT PROGRESS",
            f"{enrollment_progress}%",
            "Current portfolio enrollment"
        )

        kpi(
            k4,
            "OVERDUE STUDIES",
            overdue_studies,
            "Past planned completion date"
        )

        # =====================================================
        # REDUCED GAP ABOVE GANTT HEADER
        # =====================================================

        st.markdown(
            "<div style='height:4px'></div>",
            unsafe_allow_html=True
        )

        # =====================================================
        # DATA PREP
        # =====================================================

        df_gantt = filtered_df.copy()

        for col in ["Study Start", "Study End", "Readout"]:
            df_gantt[col] = pd.to_datetime(
                df_gantt[col],
                errors="coerce"
            )

        df_gantt["Study Sort Key"] = (
            df_gantt["Study Id"]
            .astype(str)
            .str.extract(r"(\\d+)")
            .astype(float)
        )

        df_gantt = df_gantt.sort_values(
            "Study Sort Key",
            ascending=True
        )

        # =====================================================
        # SESSION STATE
        # =====================================================

        if "start_idx" not in st.session_state:
            st.session_state.start_idx = 0

        ROWS_VISIBLE = 10

        total_rows = len(df_gantt)

        max_start = max(
            0,
            total_rows - ROWS_VISIBLE
        )

        # =====================================================
        # GANTT HEADER
        # =====================================================
        st.markdown(
            """
            <div style='
                background-color:#3B7597;
                padding:5px 7px;
                border-radius:6px;
                font-size:20px;
                font-weight:500;
                color:#F5F5F5;
                margin-bottom:6px;
            '>
                Portfolio Gantt View
            </div>
            """,
            unsafe_allow_html=True
        )

        # =====================================================
        # MINIMAL GAP
        # =====================================================
        st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)

        # =====================================================
        # WINDOWING
        # =====================================================
        start_idx = st.session_state.start_idx
        end_idx = start_idx + ROWS_VISIBLE
        df_visible = df_gantt.iloc[start_idx:end_idx].copy()

        # =====================================================
        # COLORS
        # =====================================================
        status_colors = {
            "On Track": "#3b82f6",
            "At Risk": "#f59e0b",
            "Off Track": "#ef4444",
            "Completed": "#6b7280"
        }

        df_visible["Color"] = df_visible["Status"].map(
            lambda x: status_colors.get(x, "#93c5fd")
        )

        # =====================================================
        # GANTT FIGURE
        # =====================================================
        fig = go.Figure()

        for _, row in df_visible.iterrows():

            # Main Gantt bar
            fig.add_trace(
                go.Scatter(
                    x=[row["Study Start"], row["Study End"]],
                    y=[row["Study Id"], row["Study Id"]],
                    mode="lines",
                    line=dict(color=row["Color"], width=16),
                    showlegend=False,
                    hovertemplate=(
                        f"Study: {row['Study Id']}<br>"
                        f"Start: {pd.to_datetime(row['Study Start']).strftime('%Y-%m-%d')}<br>"
                        f"End: {pd.to_datetime(row['Study End']).strftime('%Y-%m-%d')}"
                    )
                )
            )

            # Readout marker
            if pd.notna(row["Readout"]):
                fig.add_trace(
                    go.Scatter(
                        x=[row["Readout"]],
                        y=[row["Study Id"]],
                        mode="markers",
                        marker=dict(size=12, color="black", symbol="diamond"),
                        showlegend=False,
                        hovertemplate="Readout: %{x|%Y-%m-%d}"
                    )
                )

        # =====================================================
        # ✅ LEGEND (FIXED)
        # =====================================================
        for status, color in status_colors.items():
            fig.add_trace(
                go.Scatter(
                    x=[None],
                    y=[None],
                    mode="lines",
                    line=dict(color=color, width=10),
                    name=status,
                    showlegend=True
                )
            )

        # =====================================================
        # QUARTERS
        # =====================================================
        quarter_range = pd.date_range(
            start=df_gantt["Study Start"].min(),
            end=df_gantt["Study End"].max(),
            freq="QS"
        )

        fig.update_xaxes(
            tickmode="array",
            tickvals=quarter_range,
            ticktext=[f"Q{((d.month - 1)//3) + 1} {d.year}" for d in quarter_range],
            showgrid=False,
            side="top",
            ticks="outside",
            linecolor="#93c5fd",
            tickfont=dict(size=12, color="#111827")
        )

        for q in quarter_range:
            fig.add_vline(x=q, line_width=1, line_dash="dot", line_color="#d1d5db")

        # =====================================================
        # LAYOUT
        # =====================================================
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=120, t=8, b=20),  # space for legend
            plot_bgcolor="#f8fbff",
            paper_bgcolor="#f8fbff",
            hovermode="closest",

            legend=dict(
                title="Status",
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),

            yaxis=dict(
                title=dict(text="Study Id", font=dict(size=13, color="#111827")),
                autorange="reversed",
                automargin=True,
                categoryorder="array",
                categoryarray=df_visible["Study Id"].tolist(),
                tickfont=dict(size=12, color="#111827")
            ),

            xaxis_title=dict(
                text="Timeline (Quarterly View)",
                font=dict(size=13, color="#111827")
            )
        )
        st.markdown("""
        <style>
        div.stButton > button {
            font-size: 22px !important;
            height: 45px !important;
            width: 45px !important;
            border-radius: 8px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        # =====================================================
        # GANTT NAVIGATION
        # =====================================================
        nav_col1, nav_col2, nav_col3 = st.columns([20, 1, 1])

        with nav_col1:
            st.empty()

        with nav_col2:
            if st.button("⬆️", key="gantt_up"):
                st.session_state.start_idx = max(
                    0, st.session_state.start_idx - 1
                )

        with nav_col3:
            if st.button("⬇️", key="gantt_down"):
                st.session_state.start_idx = min(
                    max_start, st.session_state.start_idx + 1
                )
        

        # =====================================================
        # RENDER
        # =====================================================
        st.plotly_chart(fig, use_container_width=True)
    