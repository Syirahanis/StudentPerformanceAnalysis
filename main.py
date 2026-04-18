# main.py
import os
import streamlit as st
import base64

def get_base64(img_path):
    try:
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

news_img = get_base64("images/saysNews.png")
logo_img = get_base64("images/saysLogo.png")
kish_img = get_base64("images/kishendrans.png")
bernama_img = get_base64("images/bernamalogo.png")

st.set_page_config(
    page_title="Study Smart, Not Study Hard",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css():
    css_path = os.path.join("style", "main.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Make sure style/main.css exists.")

load_css()

st.markdown("""
<style>
/* Make the second column button teal */
div[data-testid="column"]:nth-child(2) button {
    background: linear-gradient(135deg, #0891b2, #0d9488) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

div[data-testid="column"]:nth-child(2) button:hover {
    background: linear-gradient(135deg, #0e7490, #0891b2) !important;
    box-shadow: 0 6px 14px rgba(8, 145, 178, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* Keep first column button red */
div[data-testid="column"]:first-child button {
    background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
}

div[data-testid="column"]:first-child button:hover {
    background: linear-gradient(135deg, #ef4444, #dc2626) !important;
    box-shadow: 0 6px 14px rgba(220, 38, 38, 0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== DIALOG RENDERERS ====================

def _render_uitm_story_dialog():
    """Render the UiTM students story content inside a dialog."""
    st.markdown("### Two students from different Universiti Teknologi MARA (UiTM) campuses died over the weekend")
    
    st.markdown("""
    According to Utusan Malaysia(2021), the first case involved **22-year-old Nurul Natasya Ezreen** who passed away on Friday, 9 July, at 2.50pm. She was a UiTM Merbok student, pursuing a diploma in Office Management and Technology, and was receiving treatment at the Sultan Abdul Halim Hospital in Kedah.
    
    Meanwhile, Bernama(2021) reported that on Saturday, 10 July, **21-year-old Muhammad Adham Hazim** who was pursuing a diploma in Civil Engineering at the Faculty of Civil Engineering, UiTM Pahang, was confirmed dead at 10.52pm while receiving treatment at the Sultanah Nur Zahirah Hospital in Terengganu.
    
    Both of the students died following **ruptured blood vessels in their heads**. Their families noted that prior to their death, they both complained about severe headaches.
    """)
    
    st.markdown("#### Nurul Natasya Ezreen's Story")
    st.markdown("""
    **Nurul Natasya Ezreen's** mother, Zuraimi Mohd Desa, told Utusan Malaysia that her daughter would confide in her and her husband over the past six months, letting them know about problems she faced.
    
    > "My late daughter did not have any underlying conditions before this, but lately she would complain about a headache due to all the **stress during her studies**," Zuraimi said.
    
    After passing out at her rental home, Nurul Natasya Ezreen was rushed to the hospital while **completing her coursework around 3am** on Thursday, 8 July. Her father received a phone call from her housemate regarding the incident and he asked them to call an ambulance.
    
    Her family did not get to see her until she passed away the next day.
    
    > "The last time we saw her was six months ago when she came back to visit us at home," the father noted.
    """)
    
    st.markdown("#### Muhammad Adham Hazim's Story")
    st.markdown("""
    **Muhammad Adham Hazim** was at his family home when he crawled into his parents' room, complaining about a splitting headache. His father, Mohd Rizaini Ghazali, told Bernama that the loss of his second of five children, also fondly known as Abang Ngah among family members, came as a complete shock, as the young man did not suffer from any illness.
    
    > "Only a few days ago, he complained of a headache… at about 5am yesterday, Abang Ngah crawled into our room."
    
    > "Abang Ngah complained about his splitting headache and asked my wife and me to take him to the hospital. We had to ask for help from neighbours to rush him to the hospital," Mohd Rizaini explained.
    
    He said that his son **often slept late to complete assignments and make preparations for the final exam** which was due in two weeks' time.
    
    The late Muhammad Adham Hazim was an outstanding student and had also received the **Dean's Award last semester with a cumulative grade point average (CGPA) of 3.89.**
    > "Abang Ngah is a person who loves to study, and he would divide his time between his studies and running a part-time online business," he said.
    """)


def _render_kishendran_story_dialog():
    """Render the Kishendran success story content inside a dialog."""
    st.markdown("### Kishendran achieved a perfect 4.00 GPA across six consecutive semesters")

    st.markdown("""
    Kishendran's story highlights how strong discipline, consistency, and persistence can lead to academic 
    excellence. Coming from a humble background, he maintained outstanding academic performance over multiple 
    semesters.

    His success was not described as last-minute cramming, but rather as sustained effort over time.
    The story also noted that he would wake up as early as **4AM** to complete assignments and stay on top of 
    his academic work.
    """)

    st.markdown("#### Key Success Habits")
    st.markdown("""
    - Maintained a **4.00 GPA for six consecutive semesters**
    - Practiced **strict discipline and time management**
    - Woke up **as early as 4AM** to stay consistent with academic responsibilities
    - Stayed committed despite coming from a modest family background
    """)

    st.markdown("""
    This story reflects an important idea for this dashboard:

    > Academic success is not just about studying longer, but about studying with discipline, consistency, and purpose.
    """)


# ==================== DIALOG WRAPPERS ====================

def _open_uitm_story_dialog():
    """Open native Streamlit dialog for UiTM story."""
    try:
        @st.dialog("📰 2 UiTM Students Died Over The Weekend", width="large")
        def _dialog():
            _render_uitm_story_dialog()
        _dialog()
    except AttributeError:
        # Fallback for older Streamlit versions
        with st.expander("📰 2 UiTM Students Died Over The Weekend", expanded=True):
            _render_uitm_story_dialog()


def _open_kishendran_story_dialog():
    """Open native Streamlit dialog for Kishendran story."""
    try:
        @st.dialog("🌟 From Lorry Driver's Son to Top Scholar", width="large")
        def _dialog():
            _render_kishendran_story_dialog()
        _dialog()
    except AttributeError:
        # Fallback for older Streamlit versions
        with st.expander("🌟 From Lorry Driver's Son to Top Scholar", expanded=True):
            _render_kishendran_story_dialog()


# ==================== MAIN CONTENT ====================

# Main content container
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ==================== INTRODUCTION SECTION ====================
st.markdown('<div class="section" id="intro">', unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="badge">
        <span class="badge-text">📊 DATA-DRIVEN INVESTIGATION</span>
    </div>
    <div class="hero-title">
        Does Studying Longer Actually Lead to<br>
        <span class="gradient-text">Better Academic Performance?</span>
    </div>
    <p class="hero-subtitle">
        A comprehensive analysis of <strong>103 students</strong> examining the relationship between study habits, 
        behavioral patterns, and academic outcomes.
    </p>
    <div class="legend-items">
        <div><span class="legend-dot" style="background: #a855f7;"></span>Study Patterns</div>
        <div><span class="legend-dot" style="background: #ec4899;"></span>Stress Analysis</div>
        <div><span class="legend-dot" style="background: #0891b2;"></span>Lifestyle Impact</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    news_img_style = f"background-image: url('data:image/png;base64,{news_img}');" if news_img else ""
    
    st.markdown(f"""
    <div class="news-card news-card-red">
        <div class="card-image" style="{news_img_style}">
            <div class="card-image-gradient"></div>
            <div class="news-tag tag-red">BREAKING NEWS</div>
        </div>
        <div class="card-content">
            <div class="card-meta">
                <div class="meta-dot red"></div>
                <span class="meta-label red-text">ACADEMIC PRESSURE CRISIS</span>
                <span class="meta-date">12 Jul 2021</span>
            </div>
            <div class="card-title">
                2 UiTM Students Died Over The Weekend Due To Ruptured Blood Vessels
            </div>
            <p class="card-text">
                Both families said that their children did not have any underlying conditions and they complained of 
                <strong>severe headaches due to stress from studying</strong>. The students passed away after working 
                <strong>late nights on assignments and exam preparation</strong>.
            </p>
            <div class="card-footer">
                <div class="footer-left">
                    {f"<img src='data:image/png;base64,{logo_img}' class='footer-logo'/>" if logo_img else ""}
                    <div>
                        <div class="footer-title">SAYS</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    kish_img_style = f"background-image: url('data:image/png;base64,{kish_img}');" if kish_img else ""
    bernama_img_tag = f"<img src='data:image/png;base64,{bernama_img}' class='footer-logo'/>" if bernama_img else ""
    
    st.markdown(f"""
    <div class="news-card news-card-teal">
        <div class="card-image" style="{kish_img_style}">
            <div class="card-image-gradient"></div>
            <div class="news-tag tag-white">FEATURED</div>
        </div>
        <div class="card-content">
            <div class="card-meta">
                <div class="meta-dot teal"></div>
                <span class="meta-label teal-text">ACADEMIC EXCELLENCE</span>
                <span class="meta-date">16 Aug 2025</span>
            </div>
            <div class="card-title">
                From Lorry Driver's Son to Top Scholar: 4.00 GPA Across 6 Semesters
            </div>
            <p class="card-text">
                Malaysian student Kishendran maintained an outstanding <strong>4.00 GPA for six consecutive semesters</strong>. 
                Despite his humble background, his success was driven by discipline and consistency, frequently 
                <strong>starting his day as early as 4AM</strong> to manage his academic workload.
            </p>
            <div class="card-footer">
                <div class="footer-left">
                    {bernama_img_tag}
                    <div>
                        <div class="footer-title">BERNAMA</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
        if st.button("📖 Read Full Story", key="read_story_btn", use_container_width=True):
            _open_uitm_story_dialog()
with col2:
        if st.button("📖 Read Full Story", key="read_kish_story_btn_teal", use_container_width=True):
            _open_kishendran_story_dialog()

# Narrative Bridge - Centered with decorative elements
st.markdown("""
<div class="narrative-bridge">
    <div style="display: flex; align-items: center; justify-content: center; gap: 0.75rem; margin-bottom: 1.5rem;">
        <div style="height: 1px; width: 3rem; background: linear-gradient(90deg, transparent, #c084fc);"></div>
        <div style="width: 0.5rem; height: 0.5rem; border-radius: 50%; background: #a855f7;"></div>
        <div style="height: 1px; width: 3rem; background: linear-gradient(270deg, transparent, #c084fc);"></div>
    </div>
    <div class="bridge-quote">
        Two stories. Two completely different approaches. One common goal: <span style="color: #9333ea; font-weight: 700;">academic success</span>.
    </div>
    <div class="bridge-question">
        These contrasting stories raise a fundamental question that affects millions of students worldwide:
    </div>
    <div class="bridge-highlight">
        Is academic success determined by the quantity of study time, or the quality of study habits?
    </div>
</div>
""", unsafe_allow_html=True)

# Scroll Indicator - Animated
st.markdown("""
<div class="scroll-indicator">
    <div class="scroll-text">EXPLORE THE DATA</div>
    <div class="scroll-arrow"></div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close intro section