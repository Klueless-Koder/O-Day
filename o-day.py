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

# --- Page Setup ---
st.set_page_config(page_title="UWA Mining Club", page_icon="⛏️", layout="wide")

# --- THE "PRESTIGE" CSS SUITE ---
st.markdown("""
    <style>
    /* 1. BACKGROUND: Deep, expensive Navy Gradient */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1a2a4f 0%, #0b1426 60%, #000000 100%);
        background-attachment: fixed;
    }

    /* 2. TYPOGRAPHY: Clean, Modern, "Tech" Sans-Serif */
    * {
        font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif !important;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
        letter-spacing: 0.3px;
    }

    /* 3. GLASSMORPHISM FORM CONTAINER */
    /* This targets the form block to look like frosted glass */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* 4. PREMIUM INPUT FIELDS */
    .stTextInput input, .stTextInput input:focus {
        background-color: rgba(0, 0, 0, 0.3) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
        transition: all 0.3s ease;
    }
    
    /* Glow effect when user clicks an input */
    .stTextInput input:focus {
        border-color: #C5A059 !important;
        box-shadow: 0 0 10px rgba(197, 160, 89, 0.2);
    }

    /* 5. GOLD GRADIENT BUTTON */
    .stButton > button {
        background: linear-gradient(135deg, #C5A059 0%, #9A7B3E 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.6rem 2rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(197, 160, 89, 0.4);
        color: #000000 !important;
    }

    /* 6. RADIO BUTTONS */
    .stRadio label {
        background: transparent;
        padding: 5px;
        border-radius: 5px;
        transition: background 0.3s;
    }
    .stRadio label:hover {
        background: rgba(255,255,255,0.05);
    }

    /* 7. IMAGE STYLING */
    img {
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    /* --- NUCLEAR CLEANUP (Hiding Elements) --- */
    footer, header, [data-testid="stHeader"], .stAppDeployButton, 
    .viewerBadge_container__1QSob, [data-testid="stDecoration"], 
    [data-testid="stHeaderAction"], [data-testid="stImage"] button,
    button[title="View fullscreen"], #MainMenu {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    
    /* Fix spacing at top since header is gone */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem;
        max-width: 1200px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Logic ---
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
        st.error(f"System Error: {e}")
        return False

# --- LAYOUT ARCHITECTURE ---

# 1. Hero Section (Logo & Title Centered)
c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    try:
        # Centering the logo using columns padding
        st.image(LOGO_PATH, use_container_width=True)
    except:
        pass
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="font-size: 3.5rem; margin-bottom: 10px; background: linear-gradient(to right, #ffffff, #a0a0a0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Unearth Your <span style="background: linear-gradient(to right, #FFD700, #C5A059); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Future</span>
            </h1>
            <p style="font-size: 1.2rem; opacity: 0.8; font-weight: 300;">
                The Official Student Chapter of UWA Australian Institute of Mining and Metallurgy
            </p>
        </div>
    """, unsafe_allow_html=True)

# 2. The "Glass" Content Area
# We use a 1-2-1 ratio to keep the form readable in the middle, framed by the GIFs
col_left, col_center, col_right = st.columns([1, 2, 1], gap="large")

with col_left:
    st.image(SIDE_IMG_LEFT, use_container_width=True)

with col_right:
    st.image(SIDE_IMG_RIGHT, use_container_width=True)

with col_center:
    # THE FORM CARD
    with st.form("signup_form", clear_on_submit=True):
        st.markdown("<h3 style='text-align: center; margin-bottom: 25px;'>Member Application</h3>", unsafe_allow_html=True)
        
        # Details Section
        st.markdown("##### 👤 Personal Details")
        name = st.text_input("Full Name", placeholder="e.g. Jane Doe")
        student_number = st.text_input("Student Number", placeholder="8 digits")
        facebook = st.text_input("Facebook Handle", placeholder="For group chats & event invites")
        
        st.markdown("---")
        
        # Degree Section
        st.markdown("##### 🎓 Academic Profile")
        degree_selection = st.radio(
            "Select Degree", 
            DEGREE_OPTIONS, 
            label_visibility="collapsed"
        )
        other_degree_input = st.text_input("Other Degree (if applicable)", placeholder="Specify degree...")

        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)
        
        # The Premium Button
        submitted = st.form_submit_button("COMPLETE REGISTRATION")

        if submitted:
            # Validation Logic
            errors = []
            if not name.strip(): errors.append("Name is required.")
            if not student_number.strip() or not student_number.isdigit() or len(student_number.strip()) != 8:
                errors.append("Valid 8-digit Student Number required.")
            if not facebook.strip(): errors.append("Facebook handle is required.")
            
            final_degree = degree_selection
            if degree_selection == "Other":
                if not other_degree_input.strip():
                    errors.append("Please specify your degree.")
                else:
                    final_degree = other_degree_input

            if errors:
                for e in errors:
                    st.error(f"⚠️ {e}")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row_data = [name, student_number.strip(), facebook, final_degree, timestamp]
                
                with st.spinner("Processing Application..."):
                    success = add_to_google_sheets(row_data)
                    
                if success:
                    st.balloons()
                    st.success(f"Welcome aboard, {name}. Your application is confirmed.")

