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

# Initialize session state for modal
if "show_modal" not in st.session_state:
    st.session_state.show_modal = False

# Main content container
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ==================== INTRODUCTION SECTION ====================
st.markdown('<div class="section" id="intro">', unsafe_allow_html=True)

# Hero Section - Update the hero-title part
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
                        <div class="footer-sub">By Arisha</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Button to trigger modal
    if st.button("📖 Read Full Story", key="read_story_btn", use_container_width=True):
        st.session_state.show_modal = True

with col2:
    st.markdown("""
    <div class="news-card news-card-teal">
        <div class="card-image featured-bg">
            <div class="news-tag tag-white">FEATURED</div>
            <div class="featured-center">
                <div class="icon-circle">💡</div>
                <h2 class="featured-title">Success Story</h2>
                <p class="featured-sub">Evidence-Based Learning</p>
            </div>
        </div>
        <div class="card-content">
            <div class="card-meta">
                <div class="meta-dot teal"></div>
                <span class="meta-label teal-text">SUCCESS STRATEGIES</span>
                <span class="meta-date">Apr 2026</span>
            </div>
            <div class="card-title">
                How This Valedictorian Maintained a 4.0 GPA With Just 4 Hours of Daily Study
            </div>
            <p class="card-text">
                Through <strong>active recall, spaced repetition, and consistent sleep schedules</strong>, 
                biochemistry graduate Sarah Chen achieved top honors while maintaining work-life balance. 
                Her secret: quality over quantity.
            </p>
            <div class="card-footer">
                <div>
                    <div class="footer-title">Academic Success Journal</div>
                    <div class="footer-sub">Research Feature</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Modal Popup using Streamlit's dialog
if st.session_state.show_modal:
    with st.expander("## 📰 2 UiTM Students Died Over The Weekend", expanded=True):
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
        
        The late Muhammad Adham Hazim was an outstanding student and had also received the **Dean’s Award last semester with a cumulative grade point average (CGPA) of 3.89.**
        > "Abang Ngah is a person who loves to study, and he would divide his time between his studies and running a part-time online business," he said.
        """)
        
        if st.button("Close", key="close_modal"):
            st.session_state.show_modal = False
            st.rerun()

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