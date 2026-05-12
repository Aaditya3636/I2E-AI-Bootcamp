import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    layout="wide",
    page_title="Medical Affairs Analytics"
)

# =========================
# GLOBAL STYLING
# =========================
st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.stApp {
    background-color: #f5f7fb;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
}

.section-subtitle {
    font-size: 13px;
    color: #6b7280;
    margin-top: -25px;
    margin-bottom: 0px;
}

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

.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 2px;
}

.card-title {
    font-size: 17px;
    font-weight: 700;
    color: #F5F5F5;
    background-color: #3B7597;
    padding: 10px 14px 10px 14px;
    margin: 0px;
    border-bottom: 1px solid #bfdbfe;
}

/* =========================
PAGE TABS STYLING
========================= */

div[data-baseweb="radio"] > div {
    gap: 12px;
}

div[data-baseweb="radio"] label {
    background-color: #dbeafe;
    padding: 6px 14px;
    border-radius: 8px;
    border: 1px solid #93c5fd;
}

div[data-baseweb="radio"] label:hover {
    background-color: #bfdbfe;
}

div[data-baseweb="radio"] input:checked + div {
    color: #1d4ed8 !important;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data.csv")

# =========================
# DATE PARSING
# =========================

for col in ["Study Start", "Study End", "Readout"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

filtered_df = df.copy()

# =========================
# SIDEBAR
# =========================

# =========================
# DASHBOARD HEADER
# =========================

st.markdown(
    """
    <div style="
        font-size:30px;
        font-weight:700;
        color:#1d4ed8;
        margin-top:24px;
        margin-bottom:-40px;
    ">
        Medical Affairs Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

page_top = st.radio(
    "",
    [
        "Executive Overview",
        "Portfolio Schedule"
    ],
    horizontal=True
)

# =========================
# ACTIVE PAGE
# =========================

page = page_top

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.markdown("---")
st.sidebar.markdown("### Study Filters")

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

# =========================
# FILTER LOGIC
# =========================

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

# =========================
# KPI FUNCTION
# =========================

def kpi(col, label, value, sub=""):

    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# EXECUTIVE OVERVIEW PAGE
# =====================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="section-subtitle">Portfolio-wide clinical study performance and financial health metrics.</div>',
        unsafe_allow_html=True
    )

    total_studies = len(filtered_df)

    total_budget = filtered_df[
        "Total Budget"
    ].sum()

    avg_allocation = (
        filtered_df[
            "Allocation %"
        ]
        .astype(str)
        .str.replace('%', '')
        .astype(float)
        .mean()
    )

    on_track = filtered_df[
        filtered_df["Status"] == "On Track"
    ].shape[0]

    active_regions = filtered_df[
        "Region"
    ].nunique()

    k1, k2, k3, k4 = st.columns(4)

    kpi(
        k1,
        "TOTAL BUDGET",
        f"${total_budget/1e6:.1f}M",
        "+4.2% vs last quarter"
    )

    kpi(
        k2,
        "AVG ALLOCATION",
        f"{avg_allocation:.0f}%",
        "Target: 75% utilization"
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

    # =========================
    # CHARTS
    # =========================

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            '<div class="card-title">Study Status</div>',
            unsafe_allow_html=True
        )

        status_counts = filtered_df[
            "Status"
        ].value_counts().reset_index()

        status_counts.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            status_counts,
            names="Status",
            values="Count",
            hole=0.62
        )

        fig.update_layout(
            margin=dict(
                t=20,
                b=40,
                l=20,
                r=20
            ),
            height=280,
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        st.markdown(
            '<div class="card-title">Studies by Region</div>',
            unsafe_allow_html=True
        )

        region_counts = filtered_df[
            "Region"
        ].value_counts().reset_index()

        region_counts.columns = [
            "Region",
            "Count"
        ]

        fig_bar = px.bar(
            region_counts,
            x="Region",
            y="Count",
            color_discrete_sequence=["#1f4e79"]
        )

        fig_bar.update_traces(
            width=0.35
        )

        fig_bar.update_layout(
            margin=dict(
                t=20,
                b=40,
                l=20,
                r=20
            ),
            height=300,
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )



    # =========================
    # HIGH PRIORITY STUDIES
    # =========================

    st.markdown("### High Priority Studies")

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
        border-radius:10px;
        height:310px;
        overflow-y:auto;
        box-sizing:border-box;
    ">

        <!-- HEADER -->
        <div style="
            display:grid;
            grid-template-columns: 2fr 1.4fr 2.2fr 1.2fr;
            align-items:center;
            padding:12px;
            font-size:11px;
            font-weight:600;
            color:#6b7280;
            border-bottom:1px solid #e5e7eb;
            background:#ffffff;
            position:sticky;
            top:0;
            z-index:10;
        ">

            <div>STUDY ID</div>
            <div>LEAD INDICATION</div>
            <div>BUDGET ALLOCATION</div>
            <div>STATUS</div>

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
            grid-template-columns: 2fr 1.4fr 2.2fr 1.2fr;
            align-items:center;
            padding:12px;
            border-bottom:1px solid #f1f5f9;
            box-sizing:border-box;
        ">

            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                min-width:0;
            ">

                <div style="
                    background:#1f4e79;
                    color:white;
                    font-size:10px;
                    padding:5px 7px;
                    border-radius:6px;
                    flex-shrink:0;
                ">
                    {str(i + 1).zfill(2)}
                </div>

                <div style="min-width:0;">

                    <div style="
                        font-size:13px;
                        font-weight:600;
                        white-space:nowrap;
                        overflow:hidden;
                        text-overflow:ellipsis;
                    ">
                        {row['Study Id']}
                    </div>

                    <div style="
                        font-size:11px;
                        color:#6b7280;
                    ">
                        {row['Phase']}
                    </div>

                </div>

            </div>

            <div style="
                font-size:13px;
                padding-right:10px;
                min-width:0;
            ">
                {row['Category']}
            </div>

            <div style="
                padding-right:12px;
            ">

                <div style="
                    font-size:12px;
                    margin-bottom:4px;
                ">
                    ${row['Total Budget']:,.0f}
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
                ">
                    {row['Status'].upper()}
                </span>

            </div>

        </div>
        """

    html += """
    </div>
    """

    components.html(
        html,
        height=340,
        scrolling=False
    )

# =====================================================
# PORTFOLIO SCHEDULE PAGE
# =====================================================

elif page == "Portfolio Schedule":
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0.2rem;
            padding-bottom: 0rem;
        }
        div[data-testid="stVerticalBlock"] > div {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-subtitle">Multi-year roadmap for active clinical trials.</div>',
        unsafe_allow_html=True
    )

    portfolio_total = len(filtered_df)

    active_timelines = filtered_df[
        filtered_df["Status"] != "Completed"
    ].shape[0]

    upcoming_readouts = filtered_df[
        filtered_df["Readout"] >= pd.Timestamp.today()
    ].shape[0]

    # ==================================
    # ENROLLMENT PROGRESS
    # ==================================

    # ==================================
    # ENROLLMENT PROGRESS
    # ==================================

    # ==================================
    # ENROLLMENT PROGRESS
    # ==================================

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


    # ==================================
    # OVERDUE STUDIES
    # ==================================

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

    # ==================================
    # KPI LAYOUT
    # ==================================

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

    st.markdown("<br>", unsafe_allow_html=True)

    # Revised Gantt Section

    # -----------------------------
    # DATA PREP
    # -----------------------------
    df_gantt = filtered_df.copy()

    for col in ["Study Start", "Study End", "Readout"]:
        df_gantt[col] = pd.to_datetime(df_gantt[col], errors="coerce")

    # Sort properly (S1, S2 ... S10)
    df_gantt["Study Sort Key"] = (
        df_gantt["Study Id"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(float)
    )

    df_gantt = df_gantt.sort_values("Study Sort Key", ascending=True)

    # -----------------------------
    # STATE INIT
    # -----------------------------
    if "start_idx" not in st.session_state:
        st.session_state.start_idx = 0

    ROWS_VISIBLE = 10
    total_rows = len(df_gantt)
    max_start = max(0, total_rows - ROWS_VISIBLE)


    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# HEADER ROW (TITLE + NOTE + ARROWS)
# -----------------------------
    st.markdown("<div style='margin-top:-12px; margin-bottom:-12px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([8, 2])

    # LEFT SIDE → Title + Note
    with col1:
        st.markdown(
            f"""
            <div style="
                font-weight:700;
                font-size:17px;
                display:flex;
                align-items:center;
            ">
                <span>Portfolio Gantt View</span>
                <span style="
                    font-size:12px;
                    margin-left:6px;
                ">
                    (Showing studies {st.session_state.start_idx + 1} 
                    to {min(st.session_state.start_idx + ROWS_VISIBLE, total_rows)} 
                    of {total_rows})
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # RIGHT SIDE → Buttons (tight, right aligned)
    with col2:
        c1, c2, c3 = st.columns([6, 1, 1])  

        with c1:
            st.empty()   # pushes arrows to right

        with c2:
            if st.button("▲"):
                st.session_state.start_idx = max(0, st.session_state.start_idx - 1)

        with c3:
            if st.button("▼"):
                st.session_state.start_idx = min(max_start, st.session_state.start_idx + 1)

    # -----------------------------
    # APPLY WINDOW
    # -----------------------------
    start_idx = st.session_state.start_idx
    end_idx = start_idx + ROWS_VISIBLE

    df_visible = df_gantt.iloc[start_idx:end_idx].copy()
    # -----------------------------
    # COLOR MAP
    # -----------------------------
    status_colors = {
        "On Track": "#3b82f6",
        "At Risk": "#f59e0b",
        "Off Track": "#ef4444",
        "Completed": "#6b7280",
        "Planning": "#93c5fd"
    }

    df_visible["Color"] = df_visible["Status"].map(
        lambda x: status_colors.get(x, "#93c5fd")
    )

    # -----------------------------
    # FIGURE
    # -----------------------------
    fig = go.Figure()

    for _, row in df_visible.iterrows():

        # Gantt bar
        fig.add_trace(go.Scatter(
            x=[row["Study Start"], row["Study End"]],
            y=[row["Study Id"], row["Study Id"]],
            mode="lines",
            line=dict(color=row["Color"], width=16),
            showlegend=False,
            hovertemplate=(
                f"Study: {row['Study Id']}<br>"
                f"Start: {row['Study Start']}<br>"
                f"End: {row['Study End']}"
            )
        ))

        # Readout marker
        if pd.notna(row["Readout"]):
            fig.add_trace(go.Scatter(
                x=[row["Readout"]],
                y=[row["Study Id"]],
                mode="markers",
                marker=dict(size=12, color="black", symbol="diamond"),
                showlegend=False,
                hovertemplate="Readout: %{x}"
            ))

    # -----------------------------
    # QUARTER AXIS (FULL RANGE)
    # -----------------------------
    quarter_range = pd.date_range(
        start=df_gantt["Study Start"].min(),
        end=df_gantt["Study End"].max(),
        freq="QS"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=quarter_range,
        ticktext=[
            f"Q{((d.month - 1)//3) + 1} {d.year}"
            for d in quarter_range
        ],
        showgrid=False,
        side="top",
        ticks="outside",
        linecolor="#93c5fd"
    )

    # -----------------------------
    # QUARTER LINES
    # -----------------------------
    for q in quarter_range:
        fig.add_vline(
            x=q,
            line_width=1,
            line_dash="dot",
            line_color="#d1d5db"
        )
    # Xaxes labels
    fig.update_xaxes(
        tickmode="array",
        tickvals=quarter_range,
        ticktext=[
            f"Q{((d.month - 1)//3) + 1} {d.year}"
            for d in quarter_range
        ],
        showgrid=False,
        side="top",
        ticks="outside",
        linecolor="#93c5fd",
        tickfont=dict(
            size=12,
            color="#111827"   
        )
    )

    # -----------------------------
    # LAYOUT
    # -----------------------------
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=15, b=20),
        plot_bgcolor="#f8fbff",
        paper_bgcolor="#f8fbff",
        hovermode="closest",

        # ✅ KEEP hover style HERE (correct place)
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            font_color="#111827"
        ),

        yaxis=dict(
            title=dict(
                text="Study Id",
                font=dict(
                    size=13,
                    color="#111827"
                )
            ),
            autorange="reversed",
            automargin=True,
            categoryorder="array",
            categoryarray=df_visible["Study Id"].tolist(),
            tickfont=dict(
                size=12,
                color="#111827"
            )
        ),

        xaxis_title=dict(
            text="Timeline (Quarterly View)",
            font=dict(
                size=13,
                color="#111827"
            )
        )
    )



    # -----------------------------
    # RENDER
    # -----------------------------
    st.plotly_chart(fig, use_container_width=True)
    
