import streamlit as st

def apply_custom_style(theme="light"):
    """
    Applies custom CSS for RTL support, fonts, and modern styling.
    theme: 'light' or 'dark'
    """
    
    # Define colors based on theme
    if theme == "dark":
        bg_color = "#5a5a5a"  # 35% black instead of full black
        text_color = "#fafafa"
        card_bg = "#6e6e73"  # Lighter card background
        header_color = "#fafafa"
        sidebar_bg = "#4a4a4f"
        metric_bg_1 = "#7e7e83"
        metric_bg_2 = "#8e8e93"
        metric_bg_3 = "#9e9ea3"
    else:
        bg_color = "#ffffff"
        text_color = "#2c3e50"
        card_bg = "#f0f2f6"
        header_color = "#2c3e50"
        sidebar_bg = "#f8f9fa"
        metric_bg_1 = "#e3f2fd"
        metric_bg_2 = "#e8f5e9"
        metric_bg_3 = "#fff3e0"

    st.markdown(f"""
        <style>
        /* Import Tajawal Font */
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
        }}
        
        /* Force Theme Colors */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {sidebar_bg} 0%, {card_bg} 100%);
            direction: rtl;
            text-align: right;
            border-left: 3px solid #1976d2;
        }}
        
        /* Sidebar Title */
        section[data-testid="stSidebar"] h1 {{
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 900;
            font-size: 1.5rem;
            background: linear-gradient(135deg, #1976d2 0%, #2196f3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 1rem 0;
            margin-bottom: 1.5rem;
            text-align: center;
        }}
        
        /* Radio Buttons (Navigation) */
        div[role="radiogroup"] {{
            gap: 0.5rem;
        }}
        
        div[role="radiogroup"] label {{
            background-color: {card_bg};
            border-radius: 12px;
            padding: 0.8rem 1.2rem;
            margin: 0.3rem 0;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            cursor: pointer;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        div[role="radiogroup"] label:hover {{
            background-color: {sidebar_bg};
            transform: translateX(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-color: #1976d2;
        }}
        
        div[role="radiogroup"] label[data-checked="true"] {{
            background: linear-gradient(135deg, #1976d2 0%, #2196f3 100%);
            color: white !important;
            font-weight: 700;
            transform: translateX(-8px);
            box-shadow: 0 6px 12px rgba(25, 118, 210, 0.3);
        }}
        
        div[role="radiogroup"] label[data-checked="true"] span {{
            color: white !important;
        }}

        /* Headers */
        h1, h2, h3 {{
            font-family: 'Tajawal', sans-serif !important;
            font-weight: 700;
            color: {header_color} !important;
        }}
        
        /* Custom Buttons */
        .stButton > button {{
            font-family: 'Tajawal', sans-serif !important;
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.6rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            min-height: 2.8rem;
        }}
        .stButton > button:hover {{
            background-color: #45a049;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        
        /* Primary Button Style */
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #1976d2 0%, #2196f3 100%);
            font-weight: 700;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #1565c0 0%, #1976d2 100%);
            box-shadow: 0 6px 12px rgba(25, 118, 210, 0.3);
        }}
        
        /* Metrics Section - Individual Colors */
        div[data-testid="stMetricValue"] {{
            font-family: 'Tajawal', sans-serif !important;
            direction: ltr;
            font-weight: 700;
        }}
        
        div[data-testid="metric-container"] {{
            background: linear-gradient(135deg, {metric_bg_1} 0%, {card_bg} 100%);
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
            border: 1px solid rgba(25, 118, 210, 0.1);
            transition: all 0.3s ease;
        }}
        
        div[data-testid="metric-container"]:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }}
        
        /* Different colors for each metric */
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="metric-container"] {{
            background: linear-gradient(135deg, {metric_bg_1} 0%, {card_bg} 100%);
            border-color: #1976d2;
        }}
        
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="metric-container"] {{
            background: linear-gradient(135deg, {metric_bg_2} 0%, {card_bg} 100%);
            border-color: #2e7d32;
        }}
        
        div[data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="metric-container"] {{
            background: linear-gradient(135deg, {metric_bg_3} 0%, {card_bg} 100%);
            border-color: #f57c00;
        }}

        /* Tables */
        .dataframe {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
        }}
        
        /* Streamlit Dataframe - Force RTL */
        div[data-testid="stDataFrame"] {{
            direction: rtl;
        }}
        
        div[data-testid="stDataFrame"] table {{
            font-family: 'Tajawal', sans-serif !important;
            direction: rtl;
            text-align: right;
        }}
        
        div[data-testid="stDataFrame"] th,
        div[data-testid="stDataFrame"] td {{
            font-family: 'Tajawal', sans-serif !important;
            text-align: right !important;
            direction: rtl;
        }}
        
        /* Cards/Containers */
        div[data-testid="stExpander"] {{
            background-color: {card_bg};
            border-radius: 12px;
            border: 1px solid rgba(25, 118, 210, 0.1);
        }}
        
        /* Text Inputs */
        input, textarea {{
            font-family: 'Tajawal', sans-serif !important;
        }}
        
        /* Supervisor Card Style */
        .sup-card {{
            font-family: 'Tajawal', sans-serif !important;
            background: linear-gradient(135deg, {card_bg} 0%, {sidebar_bg} 100%);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 20px;
            transition: all 0.3s ease;
            border: 1px solid rgba(25, 118, 210, 0.1);
        }}
        .sup-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            border-color: #1976d2;
        }}
        .sup-card h4 {{
            font-family: 'Tajawal', sans-serif !important;
            margin: 0 0 10px 0;
            color: {header_color};
            font-size: 1.2rem;
            font-weight: 700;
        }}
        .sup-card p {{
            font-family: 'Tajawal', sans-serif !important;
            margin: 5px 0;
            font-size: 0.95rem;
            opacity: 0.8;
        }}
        .sup-card .tag {{
            font-family: 'Tajawal', sans-serif !important;
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            margin-top: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .tag-primary {{ 
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            color: #1976d2;
        }}
        .tag-success {{ 
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            color: #2e7d32;
        }}
        </style>
    """, unsafe_allow_html=True)
