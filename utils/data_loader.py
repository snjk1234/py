import pandas as pd
import streamlit as st

def load_excel(file):
    """
    Loads the Excel file and returns a dictionary of DataFrames.
    """
    try:
        xls = pd.ExcelFile(file)
        sheets = {}
        # Load sheets, assuming names might vary slightly, but strictly looking for 2024/2025
        if "2024" in xls.sheet_names:
            sheets["2024"] = pd.read_excel(xls, "2024")
        if "2025" in xls.sheet_names:
            sheets["2025"] = pd.read_excel(xls, "2025")
        
        if not sheets:
            st.error("لم يتم العثور على أوراق العمل '2024' أو '2025' في الملف.")
            return None
            
        return sheets
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل الملف: {e}")
        return None

def process_data(sheets):
    """
    Merges 2024 and 2025 data based on Branch Name.
    Assumes Column 2 is Branch Name and Column 3 is Sales.
    """
    df24 = sheets.get("2024")
    df25 = sheets.get("2025")

    if df24 is None or df25 is None:
        return None

    # Clean and standardize column names (assuming positional if names differ)
    # User said: Column 2 = Branch Name, Column 3 = Sales.
    # Pandas is 0-indexed, so Col 1 and Col 2.
    
    # Helper to prepare DF
    def prepare_df(df, suffix):
        # Select relevant columns by index to be safe
        # We need Branch Name (1) and Sales (2). 
        # We also need "Deferred Sales" from 2025 if it exists.
        
        # Let's try to identify columns by index
        if df.shape[1] < 3:
            st.error(f"البيانات في ورقة {suffix} غير كافية (عدد الأعمدة أقل من 3).")
            return None
            
        # Rename for clarity
        df.rename(columns={df.columns[1]: 'Branch', df.columns[2]: 'Sales'}, inplace=True)
        
        # Ensure numeric sales
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
        
        return df[['Branch', 'Sales']]

    df24_clean = prepare_df(df24.copy(), "2024")
    df25_clean = prepare_df(df25.copy(), "2025")
    
    if df24_clean is None or df25_clean is None:
        return None

    # Merge on Branch
    merged = pd.merge(df25_clean, df24_clean, on='Branch', how='outer', suffixes=('_2025', '_2024'))
    
    # Fill NaNs
    merged.fillna(0, inplace=True)
    
    # If 2025 has "Deferred Sales" (المبيعات الآجلة), we need to capture it.
    # User confirmed: "مبيعات آ + ن" is the deferred sales column
    # Let's look for it in the original df25
    deferred_col = None
    for col in df25.columns:
        col_str = str(col).strip()
        if any(pattern in col_str for pattern in ["آجلة", "اجلة", "Deferred", "آ + ن", "آ+ن", "مبيعات آ"]):
            deferred_col = col
            break
    
    if deferred_col:
        # Merge deferred sales
        df25_deferred = df25[[df25.columns[1], deferred_col]].copy()
        df25_deferred.rename(columns={df25.columns[1]: 'Branch', deferred_col: 'Deferred_Sales'}, inplace=True)
        df25_deferred['Deferred_Sales'] = pd.to_numeric(df25_deferred['Deferred_Sales'], errors='coerce').fillna(0)
        merged = pd.merge(merged, df25_deferred, on='Branch', how='left')
    else:
        # Fallback if not found (or maybe Sales IS Deferred? Prompt implies distinct)
        # For now, initialize as 0 or equal to Sales if user confirms. 
        # Let's set to 0 and warn.
        merged['Deferred_Sales'] = 0
        st.warning("لم يتم العثور على عمود 'المبيعات الآجلة'. تم تعيين القيمة إلى 0.")

    return merged
