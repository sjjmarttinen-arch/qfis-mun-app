import streamlit as st

# --- APPLICATION SETTINGS ---
st.set_page_config(page_title="QFIS MUN 2026 - Evaluation App", layout="wide", page_icon="🌐")

# Inject a tiny bit of CSS to explicitly force columns to stay side-by-side on small mobile screens
st.markdown("""
    <style>
    /* Force column containers to layout horizontally even on small mobile screens */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        overflow-x: auto !important;
    }
    [data-testid="column"] {
        min-width: 65px !important;
        flex: 1 !important;
        padding: 2px !important;
    }
    div.stButton > button {
        padding: 5px 2px !important;
        font-size: 14px !important;
        height: auto !important;
    }
    </style>
""", unsafe_allowed_html=True)

# --- ROSTER DATABASE (ANONYMIZED FOR PRIVACY COMPLIANCE) ---
@st.cache_data
def load_mun_data():
    return {
        "UNSC (Larah Torres)": [
            {"country": "USA", "student": "Delegate"},
            {"country": "United Kingdom", "student": "Delegate"},
            {"country": "France", "student": "Delegate"},
            {"country": "China", "student": "Delegate"},
            {"country": "Russia", "student": "Delegate"},
            {"country": "South Africa", "student": "Delegate"},
            {"country": "Saudi-Arabia", "student": "Delegate"},
            {"country": "Bahrain", "student": "Delegate"},
            {"country": "Japan", "student": "Delegate"}
        ],
        "UNICEF (Aljohara Al-Saoud)": [
            {"country": "DR Congo", "student": "Delegate"},
            {"country": "South Sudan", "student": "Delegate"},
            {"country": "Myanmar", "student": "Delegate"},
            {"country": "Colombia", "student": "Delegate"},
            {"country": "UAE", "student": "Delegate"},
            {"country": "France", "student": "Delegate"},
            {"country": "Canada", "student": "Delegate"},
            {"country": "Mexico", "student": "Delegate"}
        ],
        "DISEC (Matei Serban)": [
            {"country": "Austria", "student": "Delegate"},
            {"country": "Brazil", "student": "Delegate"},
            {"country": "Russia", "student": "Delegate"},
            {"country": "South Korea", "student": "Delegate"},
            {"country": "Pakistan", "student": "Delegate"},
            {"country": "Ukraine", "student": "Delegate"},
            {"country": "South Africa", "student": "Delegate"}
        ],
        "UNEP (Aino-Leena Ollikainen)": [
            {"country": "Brazil", "student": "Delegate"},
            {"country": "Norway", "student": "Delegate"},
            {"country": "Chile", "student": "Delegate"},
            {"country": "India", "student": "Delegate"},
            {"country": "China", "student": "Delegate"},
            {"country": "Kuwait", "student": "Delegate"},
            {"country": "Singapore", "student": "Delegate"}
        ],
        "WHO (Shaikha Al-Naimi)": [
            {"country": "Italy", "student": "Delegate"},
            {"country": "Poland", "student": "Delegate"},
            {"country": "UAE", "student": "Delegate"},
            {"country": "Kenya", "student": "Delegate"},
            {"country": "Germany", "student": "Delegate"},
            {"country": "Australia", "student": "Delegate"},
            {"country": "Japan", "student": "Delegate"},
            {"country": "Nigeria", "student": "Delegate"}
        ],
        "ECOFIN (Zakariya Baig)": [
            {"country": "Pakistan", "student": "Delegate"},
            {"country": "Germany", "student": "Delegate"},
            {"country": "Switzerland", "student": "Delegate"},
            {"country": "Ghana", "student": "Delegate"},
            {"country": "Zambia", "student": "Delegate"},
            {"country": "Saudi-Arabia", "student": "Delegate"},
            {"country": "Argentina", "student": "Delegate"},
            {"country": "Canada", "student": "Delegate"}
        ]
    }

TEST_COMMITTEES = {
    "🛠️ SANDBOX ROOM (Practice Committee)": [
        {"country": "Wakanda", "student": "Test Student A"},
        {"country": "Asgard", "student": "Test Student B"},
        {"country": "Atlantis", "student": "Test Student C"}
    ]
}

CRITERIA = {
    "policy": {"icon": "🌐", "label": "Policy"},
    "speech": {"icon": "🗣️", "label": "Speak"},
    "neg":    {"icon": "🤝", "label": "Negot"},
    "draft":  {"icon": "📝", "label": "Draft"},
    "decor":  {"icon": "🎭", "label": "Decor"}
}

st.sidebar.title("Application Controls")
test_mode = st.sidebar.checkbox("🚀 Enable Test Mode / Sandbox", value=False)

if test_mode:
    committees = TEST_COMMITTEES
    st.info("⚠️ SANDBOX ACTIVE — Fictional delegates loaded.")
else:
    committees = load_mun_data()

if st.sidebar.button("🔄 Reset All Tracked Marks"):
    if "scores" in st.session_state:
        del st.session_state.scores
    st.rerun()

if "scores" not in st.session_state:
    st.session_state.scores = {}

for comp, delegates in committees.items():
    if comp not in st.session_state.scores:
        st.session_state.scores[comp] = {}
    for d in delegates:
        key = f"Delegate of {d['country']}"
        if key not in st.session_state.scores[comp]:
            st.session_state.scores[comp][key] = {crit: 0 for crit in CRITERIA.keys()}

# --- MAIN INTERFACE ---
st.title("QFIS MUN 2026 — Chair's Evaluation Dashboard")

selected_committee = st.selectbox(
    "👉 Select Your Assigned Committee:", 
    options=["-- Select Committee --"] + list(committees.keys())
)

if selected_committee != "-- Select Committee --":
    st.header(f"Active Committee Session: {selected_committee}")
    
    tab1, tab2 = st.tabs(["📊 Live Assessment Tracking", "🏆 Final Profiles & Awards"])
    
    with tab1:
        st.subheader("Log tracked actions horizontally below.")
        st.write("---")
        
        for delegate in committees[selected_committee]:
            del_key = f"Delegate of {delegate['country']}"
            current_marks = st.session_state.scores[selected_committee][del_key]
            
            st.markdown(f"### 🇺🇳 {delegate['country']}")
            
            # Use exactly 5 tight columns
            cols = st.columns(5)
            for idx, (crit_id, info) in enumerate(CRITERIA.items()):
                with cols[idx]:
                    # Shortened bold label above button
                    st.markdown(f"**{info['label']}**")
                    
                    # Core assessment touch point
                    if st.button(f"{info['icon']} +1 ({current_marks[crit_id]})", key=f"plus_{del_key}_{crit_id}"):
                        st.session_state.scores[selected_committee][del_key][crit_id] += 1
                        st.rerun()
                    
                    # Ultra-compact undo option
                    if st.button(f"Undo", key=f"minus_{del_key}_{crit_id}"):
                        if current_marks[crit_id] > 0:
                            st.session_state.scores[selected_committee][del_key][crit_id] -= 1
                            st.rerun()
            st.write("---")

    with tab2:
        st.subheader("Final Rubric Compilation")
        
        missing_data = False
        manual_overrides = {}
        
        for delegate in committees[selected_committee]:
            del_key = f"Delegate of {delegate['country']}"
            current_marks = st.session_state.scores[selected_committee][del_key]
            
            zero_criteria = [CRITERIA[c]['label'] for c, val in current_marks.items() if val == 0]
            
            if zero_criteria:
                missing_data = True
                st.warning(f"⚠️ **{del_key}** has 0 marks in: {', '.join(zero_criteria)}")
                
                manual_overrides[del_key] = {}
                m_cols = st.columns(len(zero_criteria))
                for idx, crit_label in enumerate(zero_criteria):
                    crit_id = [k for k, v in CRITERIA.items() if v['label'] == crit_label][0]
                    with m_cols[idx]:
                        chosen_tier = st.selectbox(
                            f"Set {CRITERIA[crit_id]['icon']}",
                            options=["Select Tier", "4 - Excellent", "3 - Good", "2 - Satisfactory", "1 - Passable"],
                            key=f"override_{del_key}_{crit_id}"
                        )
                        if chosen_tier != "Select Tier":
                            manual_overrides[del_key][crit_id] = int(chosen_tier[0])
        
        if not missing_data:
            st.success("✅ Assessment complete! All parameters tracked.")
            
        if st.button("🌟 Generate Final Individual Profiles", type="primary"):
            st.write("## 📜 Final Individual Delegate Profiles")
            
            for delegate in committees[selected_committee]:
                del_key = f"Delegate of {delegate['country']}"
                current_marks = st.session_state.scores[selected_committee][del_key]
                
                st.markdown(f"### 👤 {del_key}")
                
                for crit_id, info in CRITERIA.items():
                    raw_score = current_marks[crit_id]
                    
                    if del_key in manual_overrides and crit_id in manual_overrides[del_key]:
                        tier = manual_overrides[del_key][crit_id]
                        source = "(Manually Adjusted by Chair)"
                    else:
                        source = f"({raw_score} tracked actions)"
                        if raw_score >= 8:    tier = 4
                        elif raw_score >= 4:  tier = 3
                        elif raw_score >= 1:  tier = 2
                        else:                 tier = 1
                    
                    tier_labels = {4: "Excellent", 3: "Good", 2: "Satisfactory", 1: "Passable"}
                    st.markdown(f"- **{info['icon']} {info['label']}**: Tier {tier} — **{tier_labels[tier]}** {source}")
                st.write("---")
