import streamlit as st
import pandas as pd
import plotly.express as px
from utils.file_loader import load_excel_file
from utils.cleaner import clean_member_df
from utils.filtering import apply_common_filters


st.title("👥 Member Insights")
# === File Upload with Session Persistence ===
# File upload
member_file = st.sidebar.file_uploader("Upload Member Records", type=["xlsx", "csv"])

if member_file is not None:
    df = load_excel_file(member_file)
    df = clean_member_df(df)
    st.session_state.members_eval_df = df
    st.sidebar.success("✅ Member data uploaded and cleaned.")

if "members_eval_df" not in st.session_state:
    st.session_state.member_eval_df = None
    st.info("⬆️ Upload a Member Records file to begin.")


elif st.session_state.members_eval_df is not None:
    df = st.session_state.members_eval_df
    st.sidebar.markdown("📂 Using previously uploaded file. [🔄 Upload a new one above to replace.]")

    # Optional: Allow reset
    if st.sidebar.button("❌ Clear File from Session"):
        st.session_state.member_eval_df = None
        st.experimental_rerun()

# Filter the data before generating visuals
    filtered_df = apply_common_filters(df)

    st.caption(f"🎯 Showing {len(filtered_df)} subscribers based on current filters.")

    # === TABS FOR INSIGHTS ===
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", "📍 Subscriber Breakdown", "🧒 Children Analysis", "📈 Branch Performance"
    ])

    # === Tab 1: Overview ===
    with tab1:
        st.subheader("Overview KPIs")
        total = len(filtered_df)
        active = filtered_df[filtered_df['Member Status'] == "Active"]
        retention = round((len(active) / total) * 100, 1) if total else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Subscribers", total)
        col2.metric("Active Subscribers", len(active))
        col3.metric("Retention Rate", f"{retention}%")

    # === Tab 2: Subscriber Breakdown ===
    with tab2:
        st.subheader("Subscribers by Branch")
        branch_data = filtered_df['Clinic Name'].value_counts().reset_index()
        branch_data.columns = ['Branch', 'Subscribers']
        st.plotly_chart(px.bar(branch_data, x='Branch', y='Subscribers'), use_container_width=True)

        st.subheader("Gender Distribution (Overall)")
        gender_data = filtered_df['Gender'].value_counts().reset_index()
        gender_data.columns = ['Gender', 'Count']
        st.plotly_chart(px.pie(gender_data, values='Count', names='Gender'), use_container_width=True)

        st.subheader("Gender by Branch")
        gender_branch = filtered_df.groupby(['Clinic Name', 'Gender']).size().reset_index(name='Count')
        fig = px.bar(
            gender_branch,
            x='Clinic Name',
            y='Count',
            color='Gender',
            barmode='stack',
            title='Gender Breakdown by Branch'
        )
        st.plotly_chart(fig, use_container_width=True)

    # === Tab 3: Children Analysis ===
    with tab3:
        st.subheader("Children Subscribers (<18)")
        children = filtered_df[filtered_df['Age'] < 18]
        child_branch = children['Clinic Name'].value_counts().reset_index()
        child_branch.columns = ['Branch', 'Children']
        st.plotly_chart(px.bar(child_branch, x='Branch', y='Children'), use_container_width=True)

    # === Tab 4: Branch Performance ===
    with tab4:
        st.subheader("Branch Performance Comparison")
        performance = (
            filtered_df.groupby('Clinic Name')['Member Status']
            .value_counts().unstack().fillna(0)
        )
        performance['Total'] = performance.sum(axis=1)
        performance['Active'] = performance.get('Active', 0)
        performance['Retention Rate'] = (performance['Active'] / performance['Total']) * 100
        performance = performance.reset_index()

        st.dataframe(performance[['Clinic Name', 'Total', 'Active', 'Retention Rate']], use_container_width=True)

        fig = px.bar(
            performance,
            x='Clinic Name',
            y=['Total', 'Active'],
            barmode='group',
            title='Total vs Active Subscribers by Branch'
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("⬆️ Upload a Member Records file to begin.")
