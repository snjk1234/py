import pandas as pd
import numpy as np

def calculate_commissions(df, supervisor_df=None):
    """
    Performs the commission calculations.
    df: Merged DataFrame with 'Sales_2025', 'Sales_2024', 'Deferred_Sales'
    supervisor_df: DataFrame with supervisor assignments (اسم المشرف, الفرع, نسبة المشاركة)
    """
    if df is None or df.empty:
        return df

    # 1. Sales Difference (2025 - 2024)
    df['Difference'] = df['Sales_2025'] - df['Sales_2024']

    # 2. Growth Ratio: (Sales 2025 / Sales 2024) - 1
    # Handle division by zero
    df['Ratio'] = df.apply(
        lambda row: (row['Sales_2025'] / row['Sales_2024'] - 1) if row['Sales_2024'] != 0 else 0, 
        axis=1
    )
    
    df['Ratio_Percent'] = (df['Ratio'] * 100).round(2)

    # 3. Commission Percentage Logic
    def get_commission_rate(ratio_val):
        # ratio_val is in percentage (e.g., 5.5 for 5.5%)
        if ratio_val < 0:
            return 0.0
        elif 0 <= ratio_val <= 9.99:
            return 0.01
        elif 10 <= ratio_val <= 19.99:
            return 0.02
        elif 20 <= ratio_val <= 29.99:
            return 0.025
        elif ratio_val >= 30:
            return 0.03
        else:
            return 0.0

    df['Commission_Rate'] = df['Ratio_Percent'].apply(get_commission_rate)

    # 4. Branch Commission = Commission Rate * Sales 2025 (changed from Deferred Sales)
    df['Branch_Commission'] = df['Commission_Rate'] * df['Sales_2025']

    # 5. Supervisor Commission calculation
    # First, calculate base 10% of branch commission
    df['Supervisor_Commission_Base'] = df['Branch_Commission'] * 0.10
    
    # 6. Add Supervisor Names and distribute commission based on participation
    if supervisor_df is not None and not supervisor_df.empty:
        # Merge with supervisor data based on branch name
        supervisor_lookup = supervisor_df[['الفرع', 'اسم المشرف', 'نسبة المشاركة']].copy()
        supervisor_lookup.columns = ['Branch', 'Supervisor_Name', 'Participation_Rate']
        
        # Merge to add supervisor names and participation rates
        df = df.merge(supervisor_lookup, on='Branch', how='left')
        
        # Calculate actual supervisor commission based on participation rate
        df['Supervisor_Commission'] = df['Supervisor_Commission_Base'] * df['Participation_Rate'].fillna(1.0)
        
        # Fill missing supervisor names with "غير محدد"
        df['Supervisor_Name'] = df['Supervisor_Name'].fillna('غير محدد')
        
        # Drop the base commission column as it's no longer needed
        df = df.drop(columns=['Supervisor_Commission_Base', 'Participation_Rate'])
    else:
        # If no supervisor data, use the base commission and add default supervisor name
        df['Supervisor_Commission'] = df['Supervisor_Commission_Base']
        df['Supervisor_Name'] = 'غير محدد'
        df = df.drop(columns=['Supervisor_Commission_Base'])
    
    # Drop Ratio column (keep only Ratio_Percent for internal use)
    df = df.drop(columns=['Ratio'])

    return df
