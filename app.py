import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Clinical Trial Dashboard")

df = pd.read_csv("data.csv")
``

    region_filter = st.sidebar.multiselect("Select Region", df["Region"].unique())
    category_filter = st.sidebar.multiselect("Select Category", df["Category"].unique())
    phase_filter = st.sidebar.multiselect("Select Phase", df["Phase"].unique())
    status_filter = st.sidebar.multiselect("Select Status", df["Status"].unique())

    filtered_df = df.copy()

    if region_filter:
        filtered_df = filtered_df[filtered_df["Region"].isin(region_filter)]

    if category_filter:
        filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]

    if phase_filter:
        filtered_df = filtered_df[filtered_df["Phase"].isin(phase_filter)]

    if status_filter:
        filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]

    st.subheader("Key Metrics")

    total_studies = len(filtered_df)
    total_budget = filtered_df["Total Budget"].sum()
    total_allocated = filtered_df["Allocated Budget"].sum()
    avg_allocation = filtered_df["Allocation %"].str.replace('%','').astype(float).mean()

    on_track = filtered_df[filtered_df["Status"] == "On Track"].shape[0]
    on_track_pct = (on_track / total_studies) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Studies", total_studies)
    col2.metric("Total Budget", f"{total_budget:,.0f}")
    col3.metric("Avg Allocation %", f"{avg_allocation:.1f}%")
    col4.metric("On Track %", f"{on_track_pct:.1f}%")

    
    col1, col2 = st.columns(2)

    with col1:

    
        st.subheader("Status Distribution")

        

        status_counts = filtered_df["Status"].value_counts()

      

        st.bar_chart(status_counts, use_container_width=True)


    with col2:
        
        st.subheader("Category Distribution")

        category_counts = filtered_df["Category"].value_counts()

        st.bar_chart(category_counts, use_container_width=True)


    selected_columns = [
        "Study Id",
        "Product / Asset",
        "Region",
        "Phase",
        "Status",
        "Allocation %"
    ]

    st.subheader("Study Details")
    st.dataframe(filtered_df[selected_columns], use_container_width=True)



    
