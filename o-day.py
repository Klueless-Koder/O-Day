import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Configuration ---
# --- Configuration ---
FILE_NAME = "open_day_signups.csv"

# OLD WAY (Will Crash Online):
# LOGO_PATH = r"C:\Users\jdvan\OneDrive...\UWAStudentChapterLogo.png"

# NEW WAY (Works Online):
# Ensure the files are uploaded to the main folder of your GitHub repo
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
    /* Main Background - Dark Navy */
    .stApp {
        background-color: #001f3f;
    }
    
    /* Global Text Styles */
    h1, h2, h3, h4, h5, h6, .stRadio label, div.stMarkdown, p {
        color: #ffffff !important;
        font-family: 'Helvetica', sans-serif;
    }
    
    /* --- HIDE LINK ICONS (The Aggressive Fix) --- */
    /* Target the specific anchor tag class used by Streamlit */
    a.st-emotion-cache-1plm331, .st-emotion-cache-1plm331 {
        display: none !important;
        pointer-events: none;
    }
    /* Catch-all for any anchor inside a header */
    h1 a, h2 a, h3 a {
        display: none !important;
        opacity: 0 !important;
        pointer-events: none;
    }
    /* Hide the container wrapper if it exists */
    [data-testid="stHeaderAction"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Input Fields styling */
    .stTextInput input {
        color: #000000;
        background-color: #ffffff;
    }
    
    /* Submit Button Styling */
    .stButton > button {
        background-color: #0074D9;
        color: white;
        border-radius: 5px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 10px;
        border: 2px solid #0074D9;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #39CCCC;
        border-color: #39CCCC;
        color: #001f3f;
        transform: scale(1.02);
    }
    
    /* --- VERTICAL SPACING FIX (200px) --- */
    .block-container {
        padding-top: 200px !important;
        padding-bottom: 2rem;
    }
    
    .stVerticalBlock {
        gap: 0rem !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
col_head1, col_head2 = st.columns([0.6, 1.4], vertical_alignment="center")

with col_head1:
    try:
        st.image(LOGO_PATH, width=600)
    except Exception:
        st.write("⛏️")

with col_head2:
    # --- MARKETING TITLE ---
    st.markdown("""
        <div style="text-align: left;">
            <h1 style="font-size: 3.5rem; margin-bottom: 0px; line-height: 1.1;">
                Unearth Your <span style="color: #FFD700;">Future.</span>
            </h1>
            <h3 style="font-size: 1.8rem; font-weight: 300; color: #DDDDDD; margin-top: 5px;">
                Join the UWA Mining Club Today
            </h3>
        </div>
    """, unsafe_allow_html=True)

# --- Main Content Layout ---
col_side_l, col_form_center, col_side_r = st.columns([1, 2.5, 1], gap="medium")

# --- Left Sidebar Image ---
with col_side_l:
    st.image(SIDE_IMG_LEFT, use_container_width=True)

# --- Right Sidebar Image ---
with col_side_r:
    st.image(SIDE_IMG_RIGHT, use_container_width=True)

# --- Central Form Area ---
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
            # --- Validation Logic ---
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

            # --- Save Data ---
            if not has_error:
                new_data = {
                    "Name": [name],
                    "Student Number": [clean_s_num],
                    "Facebook": [facebook],
                    "Degree": [final_degree],
                    "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                }
                df_new = pd.DataFrame(new_data)

                if not os.path.isfile(FILE_NAME):
                    df_new.to_csv(FILE_NAME, index=False)
                else:
                    df_new.to_csv(FILE_NAME, mode='a', header=False, index=False)


                st.success(f"Success! {name} added.")
