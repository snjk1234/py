import pandas as pd
from utils.calculations import calculate_commissions

def test_calculations():
    print("Testing Calculations...")
    
    # Mock Data
    data = {
        'Branch': ['A', 'B', 'C', 'D'],
        'Sales_2024': [1000, 1000, 1000, 1000],
        'Sales_2025': [1050, 1150, 1250, 1350], # 5%, 15%, 25%, 35% growth
        'Deferred_Sales': [500, 500, 500, 500]
    }
    df = pd.DataFrame(data)
    
    # Expected Ratios: 5%, 15%, 25%, 35%
    # Expected Rates: 1%, 2%, 2.5%, 3%
    
    result = calculate_commissions(df)
    
    print(result[['Branch', 'Ratio_Percent', 'Commission_Rate', 'Branch_Commission']])
    
    # Assertions
    assert result.loc[0, 'Commission_Rate'] == 0.01, f"Expected 0.01, got {result.loc[0, 'Commission_Rate']}"
    assert result.loc[1, 'Commission_Rate'] == 0.02, f"Expected 0.02, got {result.loc[1, 'Commission_Rate']}"
    assert result.loc[2, 'Commission_Rate'] == 0.025, f"Expected 0.025, got {result.loc[2, 'Commission_Rate']}"
    assert result.loc[3, 'Commission_Rate'] == 0.03, f"Expected 0.03, got {result.loc[3, 'Commission_Rate']}"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_calculations()
