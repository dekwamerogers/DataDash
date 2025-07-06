import pandas as pd
from datetime import datetime

def clean_member_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Standardize casing
    df['Member Status'] = df['Member Status'].astype(str).str.strip().str.capitalize()
    df['Gender'] = df['Gender'].astype(str).str.strip().str.capitalize()
    df['Clinic Name'] = df['Clinic Name'].astype(str).str.strip().str.capitalize()

    # Parse dates
    df['DoB'] = pd.to_datetime(df['DoB'], errors='coerce')
    df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
    df['Activation Date'] = pd.to_datetime(df['Activation Date'], errors='coerce')

    # Calculate Age
    today = pd.to_datetime("today")
    df['Age'] = df['DoB'].apply(lambda dob: today.year - dob.year if pd.notnull(dob) else None)

    return df
