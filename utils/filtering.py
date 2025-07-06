import pandas as pd
import streamlit as st

MONTH_MAP = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}
REVERSE_MONTH_MAP = {v: k for k, v in MONTH_MAP.items()}


def apply_common_filters(df: pd.DataFrame, date_column: str = "Created Date") -> pd.DataFrame:
    """
    Apply sidebar filters for branch, gender, status, age, and created date.
    Returns the filtered DataFrame.
    """
    st.sidebar.header("📌 Filter Options")

    # === Sanitize columns ===
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    df['Clinic Name'] = df['Clinic Name'].astype(str).str.strip().str.title()
    df['Gender'] = df['Gender'].astype(str).str.strip().str.capitalize()
    df['Member Status'] = df['Member Status'].astype(str).str.strip().str.capitalize()

    # === Quick Filters ===
    branches = sorted(df['Clinic Name'].dropna().unique())
    genders = sorted(df['Gender'].dropna().unique())
    statuses = sorted(df['Member Status'].dropna().unique())

    selected_branch = st.sidebar.multiselect("Filter by Branch", branches)
    selected_gender = st.sidebar.multiselect("Filter by Gender", genders)
    selected_status = st.sidebar.multiselect("Filter by Member Status", statuses)
    age_range = st.sidebar.slider("Filter by Age", 0, 100, (0, 100))

    filtered_df = df.copy()
    if selected_branch:
        filtered_df = filtered_df[filtered_df['Clinic Name'].isin(selected_branch)]
    if selected_gender:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_gender)]
    if selected_status:
        filtered_df = filtered_df[filtered_df['Member Status'].isin(selected_status)]

    filtered_df = filtered_df[
        (filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])
    ]

    # === Date Filters ===
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"📆 Filter by {date_column}")

    filtered_df['Year'] = filtered_df[date_column].dt.year
    filtered_df['Month'] = filtered_df[date_column].dt.month
    filtered_df['Month_Name'] = filtered_df['Month'].map(MONTH_MAP)

    use_advanced = st.sidebar.toggle("🔁 Use Advanced Date Filter", value=False)

    if use_advanced:
        min_date = df[date_column].min()
        max_date = df[date_column].max()
        start_date, end_date = st.sidebar.date_input("Date Range", (min_date, max_date), min_value=min_date, max_value=max_date)

        if isinstance(start_date, tuple):
            start_date, end_date = start_date

        filtered_df = filtered_df[
            (filtered_df[date_column] >= pd.to_datetime(start_date)) &
            (filtered_df[date_column] <= pd.to_datetime(end_date))
        ]
    else:
        years = sorted(filtered_df['Year'].dropna().unique())
        selected_year = st.sidebar.selectbox("Select Year", years, index=len(years) - 1)

        months = sorted(filtered_df[filtered_df['Year'] == selected_year]['Month'].dropna().unique())
        month_options = ["All Months"] + [MONTH_MAP[m] for m in months]
        selected_month = st.sidebar.selectbox("Select Month", month_options)

        if selected_month != "All Months":
            month_num = REVERSE_MONTH_MAP[selected_month]
            filtered_df = filtered_df[
                (filtered_df['Year'] == selected_year) &
                (filtered_df['Month'] == month_num)
            ]
        else:
            filtered_df = filtered_df[
                (filtered_df['Year'] == selected_year)
            ]

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"🔍 Showing **{len(filtered_df)} records** after all filters.")

    return filtered_df
