import streamlit as st
import pandas as pd
import io
from utils import style, data_loader, calculations, sheets_manager
# Page Configuration
st.set_page_config(
    page_title="نظام عمولة المشرفين",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'theme' not in st.session_state:
    st.session_state.theme = "light"
if 'data_processed' not in st.session_state:
    st.session_state.data_processed = None
if 'sheets_client' not in st.session_state:
    st.session_state.sheets_client = sheets_manager.connect_sheets()
if 'supervisors_df' not in st.session_state:
    st.session_state.supervisors_df = None

# Load supervisors data immediately when the app starts
if st.session_state.sheets_client and st.session_state.supervisors_df is None:
    with st.spinner("جاري تحميل بيانات المشرفين..."):
        st.session_state.supervisors_df = sheets_manager.load_supervisors_data(st.session_state.sheets_client)
elif not st.session_state.sheets_client and st.session_state.supervisors_df is None:
    # Use local data if no connection
    st.session_state.supervisors_df = pd.DataFrame({
        "اسم المشرف": ["أحمد محمد", "سارة علي", "خالد عبدالله", "منى سعيد"],
        "الفرع": ["الرياض - العليا", "جدة - التحلية", "الدمام - الشاطئ", "الخبر - الكورنيش"],
        "نسبة المشاركة": [1.0, 0.5, 1.0, 0.5]
    })

# Apply Styles
style.apply_custom_style(theme=st.session_state.theme)

# Sidebar Navigation
st.sidebar.title("القائمة الرئيسية")
page = st.sidebar.radio(
    "انتقل إلى",
    ["لوحة التحكم", "النتائج", "المشرفون", "التقارير", "الإعدادات"],
    index=0
)

# --- DASHBOARD ---
if page == "لوحة التحكم":
    st.title("📊 نظام عمولة مشرفين الفروع")
    
    # File Uploader
    uploaded_file = st.file_uploader("تحميل ملف Excel (يحتوي على ورقتي 2024 و 2025)", type=['xlsx'])
    
    if uploaded_file:
        with st.spinner('جاري معالجة الملف...'):
            sheets = data_loader.load_excel(uploaded_file)
            if sheets:
                # Show raw data side-by-side
                st.subheader("معاينة البيانات (2024 vs 2025)")
                col1, col2 = st.columns(2)
                with col1:
                    st.info("بيانات 2024")
                    st.dataframe(sheets.get("2024"), use_container_width=True, height=300)
                with col2:
                    st.info("بيانات 2025")
                    st.dataframe(sheets.get("2025"), use_container_width=True, height=300)
                
                # Process Data
                merged_df = data_loader.process_data(sheets)
                if merged_df is not None:
                    # Get supervisor data if available
                    supervisor_df = st.session_state.get('supervisors_df', None)
                    results_df = calculations.calculate_commissions(merged_df, supervisor_df)
                    
                    # Drop unwanted columns
                    columns_to_drop = ['Deferred_Sales']
                    results_df = results_df.drop(columns=[col for col in columns_to_drop if col in results_df.columns], errors='ignore')
                    
                    # Translate column names to Arabic
                    results_df = results_df.rename(columns={
                        'Branch': 'الفرع',
                        'Supervisor_Name': 'اسم المشرف',
                        'Sales_2024': 'مبيعات 2024',
                        'Sales_2025': 'مبيعات 2025',
                        'Difference': 'الفرق',
                        'Ratio_Percent': 'نسبة النمو %',
                        'Commission_Rate': 'نسبة العمولة',
                        'Branch_Commission': 'عمولة الفرع',
                        'Supervisor_Commission': 'عمولة المشرف'
                    })
                    
                    st.session_state.data_processed = results_df
                    
                    st.success("✅ تمت المعالجة والحساب بنجاح!")
                    st.info("📊 انتقل إلى صفحة 'النتائج' لعرض التفاصيل الكاملة")

# --- RESULTS ---
elif page == "النتائج":
    st.title("📈 نتائج العمولات")
    
    if st.session_state.data_processed is not None:
        results_df = st.session_state.data_processed
        
        # Search Filter - expanded to include supervisor names
        search_term = st.text_input("🔍 بحث عن فرع أو مشرف...", "")
        if search_term:
            # Search in both الفرع and اسم المشرف columns
            mask = (
                results_df['الفرع'].astype(str).str.contains(search_term, case=False, na=False)
            )
            if 'اسم المشرف' in results_df.columns:
                mask = mask | results_df['اسم المشرف'].astype(str).str.contains(search_term, case=False, na=False)
            display_df = results_df[mask]
        else:
            display_df = results_df
        
        # Info message about multiple supervisors
        st.info("ℹ️ **ملاحظة:** في حال تشارك عدة مشرفين في إدارة فرع واحد، سيظهر الفرع في عدة صفوف (بخلفية ملونة)، كل صف يحتوي على اسم المشرف وعمولته حسب نسبة مشاركته.")
        
        # Add print-specific CSS
        st.markdown("""
        <style>
        @media print {
            /* Hide Streamlit UI elements when printing */
            header, footer, .stApp > header, [data-testid="stSidebar"] {
                display: none !important;
            }
            
            /* Ensure table prints properly */
            .dataframe {
                page-break-inside: avoid;
            }
            
            /* Better print layout */
            body {
                margin: 20px;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Identify branches with multiple supervisors
        if 'الفرع' in display_df.columns:
            branch_counts = display_df['الفرع'].value_counts()
            shared_branches = branch_counts[branch_counts > 1].index.tolist()
            
            # Function to highlight shared branch rows
            def highlight_shared_branches(row):
                if row['الفرع'] in shared_branches:
                    return ['background-color: #fff3e0'] * len(row)  # Light orange background
                return [''] * len(row)
            
            # Apply styling
            styled_df = display_df.style.apply(highlight_shared_branches, axis=1).format({
                'مبيعات 2024': "{:,.2f}",
                'مبيعات 2025': "{:,.2f}",
                'الفرق': "{:,.2f}",
                'نسبة النمو %': "{:.2f}%",
                'نسبة العمولة': "{:.2%}",
                'عمولة الفرع': "{:,.2f}",
                'عمولة المشرف': "{:,.2f}"
            })
        else:
            # If no branch column, just format
            styled_df = display_df.style.format({
                'مبيعات 2024': "{:,.2f}",
                'مبيعات 2025': "{:,.2f}",
                'الفرق': "{:,.2f}",
                'نسبة النمو %': "{:.2f}%",
                'نسبة العمولة': "{:.2%}",
                'عمولة الفرع': "{:,.2f}",
                'عمولة المشرف': "{:,.2f}"
            })
            
        st.dataframe(
            styled_df, 
            use_container_width=True,
            height=500
        )
        
        # Actions
        col_act1, col_act2 = st.columns(2)
        
        with col_act1:
            # Export to Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                results_df.to_excel(writer, index=False, sheet_name='النتائج')
            
            st.download_button(
                label="📥 تصدير إلى Excel",
                data=buffer,
                file_name="commissions_results.xlsx",
                mime="application/vnd.ms-excel"
            )
        
        with col_act2:
            # Print Button with JavaScript
            st.markdown("""
            <button onclick="window.print()" style="
                background-color: #4CAF50;
                color: white;
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 0.5rem;
                cursor: pointer;
                font-size: 1rem;
                width: 100%;
                margin-top: 1.5rem;
            ">
                🖨️ طباعة النتائج
            </button>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ لا توجد نتائج متاحة. يرجى تحميل ملف Excel من صفحة 'لوحة التحكم' أولاً.")

# --- SUPERVISORS ---
# --- SUPERVISORS ---
elif page == "المشرفون":
    st.title("👥 إدارة المشرفين")
    
    # Helper function to clean supervisor data
    def clean_supervisor_data(df):
        """Clean and normalize the 'نسبة المشاركة' column"""
        if df is None or df.empty:
            return df
        
        if 'نسبة المشاركة' in df.columns:
            # Force to string first, then clean
            df['نسبة المشاركة'] = df['نسبة المشاركة'].astype(str).str.replace('%', '', regex=False)
            df['نسبة المشاركة'] = pd.to_numeric(df['نسبة المشاركة'], errors='coerce')
            # If values are > 1 (like 100), assume they are percentages and divide by 100
            if df['نسبة المشاركة'].max() > 1.0:
                df['نسبة المشاركة'] = df['نسبة المشاركة'] / 100.0
            # Fill NaNs with 0
            df['نسبة المشاركة'] = df['نسبة المشاركة'].fillna(0)
        
        return df
    
    # Helper function to clean supervisor data
    def clean_supervisor_data(df):
        """Clean and normalize the 'نسبة المشاركة' column safely"""
        if df is None or df.empty:
            return df
        
        if 'نسبة المشاركة' in df.columns:
            # 1. Convert to numeric, coercing errors to NaN
            def clean_val(x):
                if isinstance(x, str):
                    x = x.replace('%', '').strip()
                    if ',' in x and '.' not in x:
                        x = x.replace(',', '.')
                return pd.to_numeric(x, errors='coerce')
            
            df['نسبة المشاركة'] = df['نسبة المشاركة'].apply(clean_val)
            
            # 2. Handle scales row-by-row
            def normalize_share(x):
                if pd.isna(x):
                    return 1.0 
                if x == 0:
                    return 0.0
                if x > 1.0:
                    return x / 100.0
                return x
                
            df['نسبة المشاركة'] = df['نسبة المشاركة'].apply(normalize_share)
            
        return df

    # Initialize session state for supervisors if not present
    if 'supervisors_df' not in st.session_state:
        st.session_state.supervisors_df = None

    # Check connection
    connected = False
    if st.session_state.sheets_client:
        connected = True
        if st.session_state.supervisors_df is None:
            with st.spinner("جاري تحميل بيانات المشرفين..."):
                st.session_state.supervisors_df = sheets_manager.load_supervisors_data(st.session_state.sheets_client)
    else:
        st.warning("⚠️ لم يتم العثور على ملف الاتصال (credentials.json). أنت الآن في وضع **العرض المحلي**.")
        if st.session_state.supervisors_df is None:
            st.session_state.supervisors_df = pd.DataFrame({
                "اسم المشرف": ["أحمد محمد", "سارة علي", "خالد عبدالله", "منى سعيد"],
                "الفرع": ["الرياض - العليا", "جدة - التحلية", "الدمام - الشاطئ", "الخبر - الكورنيش"],
                "نسبة المشاركة": [1.0, 0.5, 1.0, 0.5]
            })

    # Clean and prepare data
    if st.session_state.supervisors_df is not None:
        # Apply cleaning directly to session state using the helper function
        st.session_state.supervisors_df = clean_supervisor_data(st.session_state.supervisors_df)
        df = st.session_state.supervisors_df

        # Top Stats
        st.markdown("### 📊 نظرة عامة")
        c1, c2, c3 = st.columns(3)
        c1.metric("عدد المشرفين", df['اسم المشرف'].nunique() if 'اسم المشرف' in df.columns else 0)
        c2.metric("عدد الفروع المغطاة", df['الفرع'].nunique() if 'الفرع' in df.columns else 0)
        c3.metric("متوسط نسبة المشاركة", f"{df['نسبة المشاركة'].mean():.1%}" if 'نسبة المشاركة' in df.columns else "0%")
        
        st.markdown("---")
        
        # Controls
        col_add, col_search, col_refresh = st.columns([2, 3, 1])
        
        with col_add:
            if st.button("➕ إضافة مشرف جديد", use_container_width=True, type="primary"):
                st.session_state.show_add_dialog = True

        with col_search:
            search_query = st.text_input("🔍 بحث...", placeholder="اسم المشرف أو الفرع...", label_visibility="collapsed")
        
        with col_refresh:
            if st.button("🔄", help="تحديث البيانات"):
                st.session_state.supervisors_df = None
                st.rerun()

        # --- DIALOGS (Custom Implementation using Expander/Container for compatibility) ---
        if st.session_state.get('show_add_dialog', False):
            with st.expander("📝 إضافة مشرف جديد", expanded=True):
                with st.form("add_supervisor_form"):
                    new_name = st.text_input("اسم المشرف")
                    new_branches = st.text_area("الفروع (فرع واحد في كل سطر)")
                    new_share = st.number_input("نسبة المشاركة (%)", min_value=0.0, max_value=100.0, value=100.0, step=1.0)
                    
                    submitted = st.form_submit_button("حفظ البيانات")
                    if submitted:
                        if new_name and new_branches:
                            branches_list = [b.strip() for b in new_branches.split('\n') if b.strip()]
                            share_val = new_share / 100.0
                            
                            new_rows = []
                            for br in branches_list:
                                new_rows.append({
                                    "اسم المشرف": new_name,
                                    "الفرع": br,
                                    "نسبة المشاركة": share_val
                                })
                            
                            new_df = pd.DataFrame(new_rows)
                            updated_df = pd.concat([df, new_df], ignore_index=True)
                            
                            # Save to Sheets
                            if connected:
                                with st.spinner("جاري الحفظ..."):
                                    if sheets_manager.update_supervisors(st.session_state.sheets_client, updated_df):
                                        st.success("تمت الإضافة بنجاح!")
                                        st.session_state.supervisors_df = clean_supervisor_data(updated_df)
                                        st.session_state.show_add_dialog = False
                                        st.rerun()
                            else:
                                st.warning("وضع العرض المحلي: تم التحديث مؤقتاً.")
                                st.session_state.supervisors_df = clean_supervisor_data(updated_df)
                                st.session_state.show_add_dialog = False
                                st.rerun()
                        else:
                            st.error("يرجى إدخال الاسم وفرع واحد على الأقل.")
                
                if st.button("إلغاء", key="cancel_add"):
                    st.session_state.show_add_dialog = False
                    st.rerun()

        # Filter Data
        if search_query:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df

        # --- CARDS VIEW (MAIN) ---
        if not filtered_df.empty:
            # Group by Supervisor Name
            # We want to aggregate branches and shares
            # Assuming 'اسم المشرف' is the key
            required_cols = ['اسم المشرف', 'الفرع', 'نسبة المشاركة']
            missing_cols = [col for col in required_cols if col not in filtered_df.columns]
            
            if not missing_cols:
                grouped = filtered_df.groupby('اسم المشرف').agg({
                    'الفرع': lambda x: list(x),
                    'نسبة المشاركة': lambda x: list(x)
                }).reset_index()
                
                cols = st.columns(3) # Grid of 3
                cols = st.columns(3) # Grid of 3
                for idx, row in grouped.iterrows():
                    with cols[idx % 3]:
                        supervisor_name = row['اسم المشرف']
                        branches = row['الفرع']
                        shares = row['نسبة المشاركة']
                        
                        # 1. Determine Main Share (Mode or Max)
                        # Assuming fixed share, we take the first one or max
                        main_share = max(shares) if shares else 0
                        share_display = f"{main_share:.0%}"
                        tag_class = "tag-success" if main_share >= 1.0 else "tag-primary"

                        # 2. Limit Branches
                        max_branches_show = 3
                        visible_branches = branches[:max_branches_show]
                        remaining_count = len(branches) - max_branches_show
                        
                        # Build branches HTML
                        branches_html = ""
                        for br in visible_branches:
                            branches_html += f"<div style='margin-bottom:4px; padding-bottom:4px; border-bottom:1px solid #f0f0f0;'>🏢 {br}</div>"
                        
                        if remaining_count > 0:
                            branches_html += f"<div style='margin-top:8px; font-size:0.85em; color:#1976d2; font-weight:bold;'>+ {remaining_count} فروع أخرى...</div>"

                        # Create a container for the card with buttons
                        card_col, btn_col = st.columns([5, 1])
                        
                        with card_col:
                            st.markdown(f"""
                            <div class="sup-card" style="position: relative;">
                                <div style="display: flex; justify_content: space-between; align_items: start;">
                                    <h4 style="margin:0;">👤 {supervisor_name}</h4>
                                    <div class="{tag_class} tag" style="margin:0;">{share_display}</div>
                                </div>
                                <hr style="margin: 10px 0; opacity: 0.2;">
                                <div style="min-height: 80px;">
                                    {branches_html}
                                </div>
                                <div style="margin-top:10px; font-size:0.8em; color:#888; text-align: left;">
                                    الإجمالي: {len(branches)}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with btn_col:
                            st.write("")  # Spacer to align with card top
                            if st.button("✏️", key=f"edit_{idx}", help="تعديل", use_container_width=True):
                                st.session_state.edit_target = supervisor_name
                                st.session_state.edit_branches = "\n".join(branches)
                                st.session_state.edit_share = float(main_share * 100)
                                st.rerun()
                            
                            if st.button("🗑️", key=f"del_{idx}", help="حذف", use_container_width=True):
                                # Delete Logic
                                if connected:
                                    # Filter out this supervisor
                                    new_df = df[df['اسم المشرف'] != supervisor_name]
                                    if sheets_manager.update_supervisors(st.session_state.sheets_client, new_df):
                                        st.success(f"تم حذف {supervisor_name}")
                                        st.session_state.supervisors_df = clean_supervisor_data(new_df)
                                        st.rerun()
                                else:
                                    st.warning("حذف محلي فقط.")
                                    st.session_state.supervisors_df = clean_supervisor_data(df[df['اسم المشرف'] != supervisor_name])
                                    st.rerun()


                # --- EDIT DIALOG ---
                if 'edit_target' in st.session_state and st.session_state.edit_target:
                    with st.expander(f"✏️ تعديل بيانات: {st.session_state.edit_target}", expanded=True):
                        with st.form("edit_supervisor_form"):
                            e_name = st.text_input("اسم المشرف", value=st.session_state.edit_target)
                            e_branches = st.text_area("الفروع", value=st.session_state.edit_branches)
                            e_share = st.number_input("نسبة المشاركة", min_value=0.0, max_value=100.0, value=st.session_state.edit_share, step=1.0)
                            
                            if st.form_submit_button("حفظ التعديلات"):
                                temp_df = df[df['اسم المشرف'] != st.session_state.edit_target]
                                branches_list = [b.strip() for b in e_branches.split('\n') if b.strip()]
                                share_val = e_share / 100.0
                                
                                new_rows = []
                                for br in branches_list:
                                    new_rows.append({
                                        "اسم المشرف": e_name,
                                        "الفرع": br,
                                        "نسبة المشاركة": share_val
                                    })
                                
                                final_df = pd.concat([temp_df, pd.DataFrame(new_rows)], ignore_index=True)
                                
                                if connected:
                                    if sheets_manager.update_supervisors(st.session_state.sheets_client, final_df):
                                        st.success("تم التعديل بنجاح!")
                                        st.session_state.supervisors_df = clean_supervisor_data(final_df)
                                        del st.session_state.edit_target
                                        st.rerun()
                                else:
                                    st.session_state.supervisors_df = clean_supervisor_data(final_df)
                                    del st.session_state.edit_target
                                    st.rerun()
                        
                        if st.button("إلغاء التعديل"):
                            del st.session_state.edit_target
                            st.rerun()
            
            else:
                # Missing columns - show error
                st.error(f"عفواً، لا يمكن تجميع البيانات. الأعمدة التالية مفقودة: {missing_cols}")
                st.warning("قد يكون ملف Google Sheets يحتوي على رؤوس أعمدة مختلفة أو فارغة.")
                if st.button("🛠️ إصلاح رؤوس الأعمدة (سيتم مسح البيانات القديمة في الورقة)"):
                    empty_df = pd.DataFrame(columns=required_cols)
                    if sheets_manager.update_supervisors(st.session_state.sheets_client, empty_df):
                        st.success("تم إصلاح الأعمدة! يرجى تحديث الصفحة.")
                        st.session_state.supervisors_df = None
                        st.rerun()
        else:
            st.info("لا توجد نتائج مطابقة للبحث.")

# --- REPORTS ---
elif page == "التقارير":
    st.title("📈 التقارير والنتائج")
    
    if st.session_state.data_processed is not None:
        df = st.session_state.data_processed
        
        # Metrics - using Arabic column names
        total_sales_25 = df['مبيعات 2025'].sum()
        total_comm = df['عمولة الفرع'].sum()
        total_sup_comm = df['عمولة المشرف'].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("إجمالي مبيعات 2025", f"{total_sales_25:,.2f}")
        m2.metric("إجمالي عمولة الفروع", f"{total_comm:,.2f}")
        m3.metric("إجمالي عمولة المشرفين", f"{total_sup_comm:,.2f}")
        
        # Charts (using Plotly if installed, or st.bar_chart)
        st.subheader("أعلى الفروع تحقيقاً للنمو")
        top_growth = df.nlargest(10, 'نسبة النمو %')
        st.bar_chart(top_growth.set_index('الفرع')['نسبة النمو %'])
        
    else:
        st.info("يرجى تحميل البيانات ومعالجتها في لوحة التحكم أولاً.")

# --- SETTINGS ---
elif page == "الإعدادات":
    st.title("⚙️ الإعدادات")
    
    st.subheader("المظهر")
    # Use session state to persist selection
    current_theme = st.session_state.theme
    index = 0 if current_theme == "light" else 1
    
    selected_theme = st.selectbox("اختر السمة", ["فاتح", "داكن"], index=index)
    
    # Update state if changed
    new_theme = "light" if selected_theme == "فاتح" else "dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    
    st.subheader("اللغة")
    lang = st.selectbox("اللغة", ["العربية", "English"])
