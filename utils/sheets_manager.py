import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

def connect_sheets():
    """
    Connects to Google Sheets API.
    """
    try:
        # Check if secrets exist (Streamlit Cloud way) or local file
        creds_file = "credentials.json"
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, SCOPE)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"فشل الاتصال بـ Google Sheets: {e}")
        st.info("تأكد من وجود ملف credentials.json في المجلد الرئيسي.")
        return None

def get_or_create_sheet(client, spreadsheet_name="Commission_System_DB"):
    try:
        return client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        return client.create(spreadsheet_name)

def load_supervisors_data(client):
    try:
        sh = get_or_create_sheet(client)
        try:
            worksheet = sh.worksheet("المشرفون")
        except gspread.WorksheetNotFound:
            worksheet = sh.add_worksheet(title="المشرفون", rows=100, cols=10)
            worksheet.append_row(["اسم المشرف", "الفرع", "نسبة المشاركة"])
            
        # Use UNFORMATTED_VALUE to get actual numbers (e.g. 0.25) instead of formatted strings or rounded values
        data = worksheet.get_all_records(value_render_option='UNFORMATTED_VALUE')
        # Ensure we have a DF even if empty
        if not data:
            return pd.DataFrame(columns=["اسم المشرف", "الفرع", "نسبة المشاركة"])
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"خطأ في جلب بيانات المشرفين: {e}")
        return pd.DataFrame()

def update_supervisors(client, df):
    """
    Updates the Supervisors sheet with the provided DataFrame.
    """
    try:
        sh = get_or_create_sheet(client)
        try:
            worksheet = sh.worksheet("المشرفون")
        except gspread.WorksheetNotFound:
            worksheet = sh.add_worksheet(title="المشرفون", rows=100, cols=10)
        
        # Clear existing
        worksheet.clear()
        
        # Update with new data
        # Convert DF to list of lists
        df_clean = df.fillna("")
        values = [df_clean.columns.values.tolist()] + df_clean.values.tolist()
        
        # Use update with range (safer for newer gspread)
        worksheet.update(range_name='A1', values=values)
        return True
    except Exception as e:
        st.error(f"فشل تحديث المشرفين: {e}")
        return False

def export_results(client, df, sheet_name="النتائج"):
    try:
        sh = get_or_create_sheet(client)
        try:
            worksheet = sh.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=sheet_name, rows=100, cols=20)
        
        # Clear existing
        worksheet.clear()
        
        # Update with new data
        df_clean = df.fillna("")
        values = [df_clean.columns.values.tolist()] + df_clean.values.tolist()
        
        worksheet.update(range_name='A1', values=values)
        return True
    except Exception as e:
        st.error(f"فشل التصدير: {e}")
        return False
