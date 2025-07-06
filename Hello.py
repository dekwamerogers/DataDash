import streamlit as st

st.set_page_config(page_title="DataDash", page_icon="📊", layout="wide")

# Welcome Section
st.markdown("""
# 👋 Welcome to the DataDash

This internal tool was built to help analyze and visualize **subscriber and agent performance** across all clinic branches in a faster, smarter way.

---

### 🔍 What you can do:
- Upload member and agent Excel files
- Automatically generate charts, summaries, and key insights
- Filter by date, gender, branch, and more
- Export data for board presentations
- Ask questions using natural language *(Coming soon)*

---

### 🗂️ Sections Available:
- **👥 Member Insights** – Full breakdown of subscribers by gender, age, branch, and status
- **🧑‍💼 Agent Insights** – Track agent activity and evaluate performance
- **📋 Evaluation Reports** – See how agents and subscribers interact across statuses

---

### ⚠️ Before you start:
Make sure your uploaded files include:
1. **Member Records**
2. **Agent Status Records**
3. **Agent Evaluation Records**

*Only Excel or CSV files are supported.*

---

### 🚀 Get Started
Use the left sidebar to navigate to the insights you need.

> Need help? Contact the product admin or IT support team.

""")
