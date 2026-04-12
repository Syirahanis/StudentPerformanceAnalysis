import os
import streamlit as st


def load_css():
    base_path = os.path.dirname(os.path.dirname(__file__))
    css_path = os.path.join(base_path, "style", "custom.css")

    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found.")


def insight_box(title, description, extra_class=""):
    st.markdown(
        f"""
        <div class="insight-box {extra_class}">
            <div class="insight-icon">◔</div>
            <div class="insight-content">
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def recommendation_card(title, description):
    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-icon">✦</div>
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_recommendations():
    load_css()

    st.markdown(
        '<h1 class="page-title">The Answer: Study Smart, Not Study Hard</h1>',
        unsafe_allow_html=True
    )

    insight_box(
        "Study duration shows weak correlation with academic success",
        "Our data reveals only a weak relationship between total study hours and CGPA, suggesting that time invested is not the primary driver of results.",
        "purple-left"
    )

    insight_box(
        "Active learning methods yield stronger academic outcomes",
        "Students who employ active recall, practice testing, and mixed methods consistently outperform those relying on passive re-reading and summarizing.",
        "purple-left"
    )

    insight_box(
        "Sleep deprivation undermines both performance and wellbeing",
        "Students averaging 7–8 hours of sleep achieve better CGPA and report lower stress levels compared to those sleeping fewer hours.",
        "cyan-left"
    )

    insight_box(
        "Procrastination creates a vicious cycle of stress and poor outcomes",
        "High procrastinators experience higher stress and lower average CGPA, creating a feedback loop that compounds academic challenges.",
        "pink-left"
    )

    insight_box(
        "Last-minute cramming increases stress without improving grades",
        "Frequent all-nighters and exam cramming sessions raise stress sharply while providing little improvement in final CGPA scores.",
        "red-left"
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="large")

    with col1:
        recommendation_card(
            "Use Active Learning",
            "Practice tests and active recall over passive re-reading."
        )
    with col2:
        recommendation_card(
            "Prioritize Sleep",
            "Maintain 7–8 hours nightly for peak cognitive function."
        )
    with col3:
        recommendation_card(
            "Plan Ahead",
            "Reduce procrastination through structured schedules."
        )
    with col4:
        recommendation_card(
            "Quality Over Quantity",
            "Focus on effective study methods, not just hours."
        )

    st.markdown(
        """
        <div class="quote-box">
            "It's not the number of hours you study — it's how you use those hours that truly matters."
        </div>
        """,
        unsafe_allow_html=True
    )


show_recommendations()