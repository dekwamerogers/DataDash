import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from utils.file_loader import load_excel_file

st.set_page_config(page_title="Agent Insights", page_icon="🧑‍💼", layout="wide")
st.title("🧑‍💼 Agent Insights")

# === File Upload with Session Persistence ===
if "agent_eval_df" not in st.session_state:
    st.session_state.agent_eval_df = None

uploaded_file = st.sidebar.file_uploader("Upload Agent Evaluation File", type=["csv", "xlsx"])

# Load and store in session
if uploaded_file is not None:
    df = load_excel_file(uploaded_file)
    st.session_state.agent_eval_df = df


# Use stored data
if st.session_state.agent_eval_df is not None:
    df = st.session_state.agent_eval_df
    st.sidebar.markdown("📂 Using previously uploaded file. [🔄 Upload a new one above to replace.]")

    # Optional: Allow reset
    if st.sidebar.button("❌ Clear File from Session"):
        st.session_state.agent_eval_df = None
        st.experimental_rerun()

    df.columns = [col.strip().title().replace("_", " ") for col in df.columns]
    df = df.rename(columns={
        "Name Of Agents": "Agent Name",
        "Name Of Subscribers": "Subscriber Name",
        "Subscriber Status": "Status"
    })

    # === Basic Clean Up ===
    df['Agent Name'] = df['Agent Name'].astype(str).str.strip().str.title()
    df['Status'] = df['Status'].astype(str).str.strip().str.capitalize()

    # === Date Filter Setup ===
    df['Date'] = pd.to_datetime(df.get("Date", pd.Timestamp.now()), errors='coerce')  # fallback if no Date
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    month_map = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    df['Month Name'] = df['Month'].map(month_map)

    # === Sidebar Filters ===
    st.sidebar.header("🔍 Filter Options")

    available_years = sorted(df['Year'].dropna().unique())
    selected_year = st.sidebar.selectbox("Select Year", available_years, index=len(available_years) - 1)

    available_months = df[df['Year'] == selected_year]['Month Name'].dropna().unique().tolist()
    selected_month = st.sidebar.selectbox("Select Month", ["All Months"] + sorted(available_months))

    available_statuses = sorted(df['Status'].dropna().unique())
    selected_statuses = st.sidebar.multiselect("Filter by Subscriber Status", available_statuses)

    # === Apply Filters ===
    filtered_df = df[df['Year'] == selected_year]

    if selected_month != "All Months":
        filtered_df = filtered_df[filtered_df['Month Name'] == selected_month]
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['Status'].isin(selected_statuses)]

    st.sidebar.markdown(f"🎯 Showing **{len(filtered_df)}** records")

    # === Summary Table ===
    st.subheader("📊 Agent Performance Summary")

    subscriber_count = filtered_df.groupby("Agent Name")["Subscriber Name"].nunique().reset_index(name="Total Subscribers")
    status_breakdown = filtered_df.groupby(["Agent Name", "Status"]).size().reset_index(name="Count")
    pivot_df = status_breakdown.pivot(index="Agent Name", columns="Status", values="Count").fillna(0).astype(int)

    summary_df = subscriber_count.merge(pivot_df, on="Agent Name", how="left").fillna(0)
    st.dataframe(summary_df, use_container_width=True)

    # === Export Button ===
    buffer = BytesIO()
    summary_df.to_excel(buffer, index=False)
    st.download_button("⬇️ Download Summary as Excel", data=buffer.getvalue(), file_name="agent_summary.xlsx", mime="application/vnd.ms-excel")

    st.divider()
    
    
    st.subheader("📊 Agent Performance Charts")

    # === 1. Top 5 Agents by Total Subscribers
    top_agents_df = summary_df.sort_values(by="Total Subscribers", ascending=False).head(5)
    bar_chart = px.bar(
        top_agents_df,
        x="Total Subscribers",
        y="Agent Name",
        title="Top 5 Agents by Subscribers",
        color="Total Subscribers",
        color_continuous_scale="blues"
    )
    st.plotly_chart(bar_chart, use_container_width=True)

    # === 2. Stacked Bar: Agent vs Status Breakdown
    stacked_df = summary_df.set_index("Agent Name").drop(columns="Total Subscribers")
    stacked_df = stacked_df.loc[:, (stacked_df != 0).any(axis=0)]  # remove empty status cols

    stacked_chart = px.bar(
        stacked_df,
        title="Agent-wise Subscriber Status Breakdown",
        barmode='stack',
        orientation = 'h'
    )
    st.plotly_chart(stacked_chart, use_container_width=True)

    # === 3. Pie Chart: Overall Status Distribution
    overall_status_counts = filtered_df["Status"].value_counts().reset_index()
    overall_status_counts.columns = ["Status", "Count"]

    pie_chart = px.pie(
        overall_status_counts,
        values="Count",
        names="Status",
        title="Overall Subscriber Status Distribution"
    )
    st.plotly_chart(pie_chart, use_container_width=True)

    st.divider()
    st.subheader("🔎 Agent Drill-down Viewer")

    agents = sorted(filtered_df["Agent Name"].unique())
    agent_selected = st.selectbox("Choose an Agent", agents)

    drill_df = filtered_df[filtered_df["Agent Name"] == agent_selected]
    st.write(f"Showing **{len(drill_df)}** subscriber records for **{agent_selected}**")
    st.dataframe(drill_df, use_container_width=True)

    # === Status Pie Chart for Selected Agent
    pie_status_df = drill_df["Status"].value_counts().reset_index()
    pie_status_df.columns = ["Status", "Count"]

    if not pie_status_df.empty:
        pie_chart = px.pie(
            pie_status_df,
            values="Count",
            names="Status",
            title=f"Status Distribution for {agent_selected}",
            hole=0.3
        )
        st.plotly_chart(pie_chart, use_container_width=True)
    else:
        st.warning("No status data available for this agent.")

    # === Download Agent's Records
    drill_buffer = BytesIO()
    drill_df.to_excel(drill_buffer, index=False)
    st.download_button(
        f"⬇️ Download {agent_selected}'s Subscriber Details",
        data=drill_buffer.getvalue(),
        file_name=f"{agent_selected}_details.xlsx",
        mime="application/vnd.ms-excel"
    )


else:
    st.info("📥 Please upload the **Agent Evaluation file** to get started.")
