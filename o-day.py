import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- Configuration ---
SHEET_NAME = "Mining Club Signups" 
LOGO_PATH = "UWAStudentChapterLogo.png"
SIDE_IMG_LEFT = "guy-mining-diamonds-but-actually-just-dirt.gif"
SIDE_IMG_RIGHT = "zoolander-miner-walk-zoolander.gif"

DEGREE_OPTIONS = [
    "Chemical Engineering",
    "Civil Engineering",
    "Environmental Engineering",
    "Environmental Science",
    "Geology",
    "Mechanical Engineering",
    "Mining Engineering",
    "Other"
]

# --- Page Setup & Styling ---
st.set_page_config(page_title="UWA Mining Club", page_icon="⛏️", layout="wide")

st.markdown("""
    <style>
    /* --- SOPHISTICATED ROYAL BLUE BACKGROUND --- */
    .stApp {
        background: linear-gradient(180deg, #0f204b 0%, #000c24 100%);
        background-attachment: fixed;
    }
    
    /* Global Text Styles */
    h1, h2, h3, h4, h5, h6, .stRadio label, div.stMarkdown, p {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* --- 🚫 THE FOOTER KILLER (Hide "Made with Streamlit") 🚫 --- */
    
    /* 1. Target the main footer container */
    footer {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* 2. Target the footer by its test ID (Streamlit's internal name) */
    [data-testid="stFooter"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 3. Hide the 'Viewer Badge' (Bottom right user profile/menu) */
    .viewerBadge_container__1QSob {
        display: none !important;
    }
    
    /* 4. Hide the top decoration ribbon (The colored line at the top) */
    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* 5. Hide the Hamburger Menu & Top Header */
    [data-testid="stHeader"] {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden !important;
    }

    /* --- HIDE IMAGE ICONS (Arrows & Fullscreen) --- */
    [data-testid="stImage"] button {
        display: none !important;
    }
    button[title="View fullscreen"] {
        display: none !important;
    }
    [data-testid="StyledFullScreenButton"] {
        display: none !important;
    }

    /* --- FORM STYLING --- */
    .stTextInput input {
        color: #000000;
        background-color: #f0f2f6;
        border-radius: 5px;
        border: 1px solid #d1d5db;
    }
    .stRadio label { font-size: 1rem; }
    
    /* Submit Button - Gold Accent */
    .stButton > button {
        background-color: #C5A059;
        color: #000000;
        border-radius: 5px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 15px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background-color: #E6B86A;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.3);
        color: #000000;
    }
    
    /* --- LAYOUT ADJUSTMENTS --- */
    .block-container {
        padding-top: 50px !important; 
        padding-bottom: 2rem;
    }
    .stVerticalBlock { gap: 0rem !important; }
    
    </style>
    """, unsafe_allow_html=True)

# --- Google Sheets Connection Function ---
def add_to_google_sheets(data_row):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        sheet.append_row(data_row)
        return True
    except Exception as e:
        st.error(f"Google Sheets Error: {e}")
        return False

# --- Header Section ---
col_head1, col_head2 = st.columns([0.6, 1.4], vertical_alignment="center")

with col_head1:
    try:
        st.image(LOGO_PATH, width=600) 
    except Exception:
        st.write("⛏️")

with col_head2:
    st.markdown("""
        <div style="text-align: left;">
            <h1 style="font-size: 3.5rem; margin-bottom: 0px; line-height: 1.1; font-weight: 700;">
                Unearth Your <span style="color: #C5A059;">Future.</span>
            </h1>
            <h3 style="font-size: 1.8rem; font-weight: 300; color: #E0E0E0; margin-top: 5px; letter-spacing: 1px;">
                Join the UWA Mining Club
            </h3>
        </div>
    """, unsafe_allow_html=True)

# --- Main Form Layout ---
col_side_l, col_form_center, col_side_r = st.columns([1, 2.5, 1], gap="medium")

with col_side_l:
    st.image(SIDE_IMG_LEFT, width="stretch")

with col_side_r:
    st.image(SIDE_IMG_RIGHT, width="stretch")

with col_form_center:
    with st.form("signup_form", clear_on_submit=True):
        c1, c2 = st.columns(2, gap="small")
        
        with c1:
            st.subheader("Details")
            name = st.text_input("Full Name")
            student_number = st.text_input("Student Number (8 digits)")
            facebook = st.text_input("Facebook Handle")

        with c2:
            st.subheader("Degree")
            degree_selection = st.radio(
                "Select Degree:", 
                DEGREE_OPTIONS, 
                label_visibility="collapsed"
            )
            other_degree_input = st.text_input("If 'Other', specify here:")

        submitted = st.form_submit_button("Submit Application ➤")

        if submitted:
            # --- Validation ---
            has_error = False
            if not name.strip():
                st.error("⚠️ Missing Full Name.")
                has_error = True
            
            clean_s_num = student_number.strip()
            if len(clean_s_num) != 8 or not clean_s_num.isdigit():
                st.error("⚠️ Student Number must be 8 digits.")
                has_error = True

            if not facebook.strip():
                st.error("⚠️ Missing Facebook handle.")
                has_error = True
                
            final_degree = degree_selection
            if degree_selection == "Other":
                if not other_degree_input.strip():
                    st.error("⚠️ Please specify the 'Other' degree.")
                    has_error = True
                else:
                    final_degree = other_degree_input

            # --- Save to Google Sheets ---
            if not has_error:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row_data = [name, clean_s_num, facebook, final_degree, timestamp]
                
                with st.spinner("Saving to cloud..."):
                    success = add_to_google_sheets(row_data)
                    
                if success:
                    st.success(f"Success! {name} has been added to the database.")
