import os
import streamlit as st


st.set_page_config(
    page_title="Study Smart, Not Study Hard",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    css_path = os.path.join("style", "custom.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Make sure style/custom.css exists.")


load_css()


st.markdown(
    """
    <div class="intro-page">
        <h1 class="intro-title">
            Does Studying Longer Actually Lead to Better Academic Performance?
        </h1>
        <p class="intro-subtitle">
            A data-driven exploration of student study habits, behavior, and CGPA
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")

# -------------------------
# News: Student Stress
# -------------------------
with col1:
    st.markdown(
        """
        <div class="intro-story-card pressure-card">
            <div class="story-tag pressure-tag">Academic Pressure</div>
            <div class="story-image-placeholder">Image placeholder</div>
            <h3 class="story-title">
                Student Hospitalized After 72-Hour Study Marathon Before Finals
            </h3>
            <p class="story-text">
                A senior engineering student was admitted to the emergency room after three
                consecutive all-nighters. Despite extreme efforts, her final exam scores remained
                below average, highlighting the dangers of excessive, unbalanced study habits.
            </p>
            <p class="story-source">Source: Placeholder case study, March 2026</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------
# News: Student Success
# -------------------------
with col2:
    st.markdown(
        """
        <div class="intro-story-card smart-card">
            <div class="story-tag smart-tag">Smart Habits</div>
            <div class="story-image-placeholder">Image placeholder</div>
            <h3 class="story-title">
                High-Performing Student Achieves Strong Results Through Efficient Daily Study
            </h3>
            <p class="story-text">
                By using active recall, summarizing key concepts, and maintaining consistent sleep,
                the student achieved strong academic results without relying on all-nighters.
                The approach focused on quality over quantity.
            </p>
            <p class="story-source">Source: Placeholder study habit profile, April 2026</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="intro-bottom-text">
        <p>
            Two students. Two completely different approaches. One common goal: academic success.
            These contrasting situations raise a fundamental question that affects millions of
            students worldwide: is academic success determined by the quantity of study time,
            or by the quality of study habits?
        </p>
        <p>
            This dashboard explores student data on study hours, procrastination, stress, sleep,
            and CGPA to challenge the belief that studying longer automatically leads to
            better results.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)