📊 Membership Analysis Dashboard

A smart, flexible internal dashboard built with Streamlit for analyzing subscriber and agent performance using uploaded Excel files. Designed for a growing clinic with multiple branches in Accra to automate and visualize critical HR, IT, and Board-level reports.
🚀 Features

    Upload and analyze membership and agent data (CSV/XLSX)

    Dynamic filtering by:

        Year / Month

        Subscriber status

        Agent name

    Clean, responsive dashboards with:

        Bar graphs

        Pie charts

        Tabular summaries

    Agent drill-down with:

        Subscriber details

        Status pie charts

        Data export

    📂 File upload is stored in session so it doesn’t reset on page refresh

📁 Project Structure

membership-dashboard/
│
├── app.py                     # Entry point (Hello/Landing Page)
├── utils/
│   └── file_loader.py         # Excel file handling and cleaning
│
├── pages/
│   ├── 1_Member_Insights.py   # Dashboard for member analytics
│   └── 2_Agent_Insights.py    # Dashboard for agent evaluations
│
└── README.md                  # You’re here.

📦 Requirements

    Python 3.8+

    Streamlit

    Pandas

    Plotly

    openpyxl (for .xlsx files)

Install dependencies:

pip install -r requirements.txt

    Or manually install:

pip install streamlit pandas plotly openpyxl

▶️ Running the App

streamlit run app.py

Navigate through the sidebar to access Member or Agent insights.
📥 File Formats
✅ Agent Evaluation File:
Agent Name	Firstname	Surname	Subscriber Name	Status	Date
✅ Member Records File (Used on Member Insights page):

| Clinic Name | Package | Agent Name | Firstname | Surname | Gender | Membership No. | ... |
📸 Screenshots

    Coming Soon: Include dashboard screenshots or GIFs for demo

🧠 Future Features

    Natural Language Query with OpenAI/Gemini (LLM)

    Multi-file persistent storage & session caching

    PDF Report generation for board presentation

    User login & file history

🙌 Credits

Built by Dre under Dretek Innovations 🚀
For impact-driven organizations seeking clarity through data.