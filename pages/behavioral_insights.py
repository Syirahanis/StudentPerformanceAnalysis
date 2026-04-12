import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -------------------------
# Layout & Styling
# -------------------------
def load_css():
    base_path = os.path.dirname(os.path.dirname(__file__))
    css_path = os.path.join(base_path, "style", "custom.css")

    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found.")


def load_data():
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "data", "studentperformance.csv")
    df = pd.read_csv(file_path)

    df.columns = [col.strip().lower() for col in df.columns]

    rename_map = {
        "cgpa": "cgpa",
        "procrastination level": "procrastination_level",
        "sleep hours": "sleep_hours",
        "stress level (beginning of semester)": "stress_start",
        "stress level (end of semester)": "stress_end",
        "study hours before exam": "study_hours_before_exam",
    }
    df = df.rename(columns=rename_map)

    df["last_minute_studying"] = df["study_hours_before_exam"].apply(
        lambda x: "Regular Cramming" if x >= 3 else "No Cramming"
    )

    return df


def chart_header(title, subtitle, kicker=None):
    if kicker:
        st.markdown(
            f"""
            <div class="chart-card-header">
                <div class="chart-kicker">{kicker}</div>
                <h3>{title}</h3>
                <p>{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="chart-card-header">
                <h3>{title}</h3>
                <p>{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------------------------
# Stress Beginning of Semester vs End of Semester
# -----------------------------------------------
def stress_start_end_chart(df):
    avg_start = df["stress_start"].mean()
    avg_end = df["stress_end"].mean()

    chart_header(
        "Stress Levels: Start vs End of Semester",
        "A clear increase in stress levels is observed as exams approach.",
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Beginning<br>of Semester", "End<br>of Semester"],
            y=[avg_start, avg_end],
            text=[f"{avg_start:.2f}", f"{avg_end:.2f}"],
            textposition="outside",
            marker=dict(color=["#64c7c8", "#f27d72"]),
            width=[0.45, 0.45],
        )
    )

    fig.add_annotation(
        x=1,
        y=avg_end + 0.15,
        ax=0,
        ay=avg_start + 0.1,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1.1,
        arrowwidth=2,
        arrowcolor="#f27d72",
    )

    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=10, b=20),
        yaxis=dict(title="Average Stress Level (1–5)", range=[0, 5.5]),
        xaxis=dict(title=""),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="chart-note">↗ Stress nearly doubles as the semester progresses</div>', unsafe_allow_html=True)

# -----------------------------------------------
# Stress Surge by Procrastination Level
# -----------------------------------------------
def stress_vs_procrastination_chart(df):
    proc_levels = [1, 2, 3, 4, 5]

    avg_begin = [
        df[df["procrastination_level"] == p]["stress_start"].mean()
        for p in proc_levels
    ]
    avg_end = [
        df[df["procrastination_level"] == p]["stress_end"].mean()
        for p in proc_levels
    ]

    chart_header(
        "Stress Surge by Procrastination Level",
        "Higher procrastinators experience the steepest stress increase.",
        kicker="But what contributes to this rising stress?",
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[f"Level {p}" for p in proc_levels],
            y=avg_begin,
            name="Beginning of semester",
            marker=dict(color="#64c7c8"),
            text=[f"{v:.1f}" for v in avg_begin],
            textposition="outside",
        )
    )

    fig.add_trace(
        go.Bar(
            x=[f"Level {p}" for p in proc_levels],
            y=avg_end,
            name="End of semester",
            marker=dict(color="#f27d72"),
            text=[f"{v:.1f}" for v in avg_end],
            textposition="outside",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=10, b=20),
        barmode="group",
        yaxis=dict(title="Average Stress Level (1–5)", range=[0, 5.8]),
        xaxis=dict(title="Procrastination Level"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(orientation="h", y=1.12, x=0),
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="chart-note">High procrastinators experience the strongest stress surge by semester end</div>', unsafe_allow_html=True)

# -----------------------------------------------
# Procrastination Level vs CGPA Stacked Chart
# -----------------------------------------------
def procrastination_vs_cgpa_stacked_chart(df):

    proc_levels = [1, 2, 3, 4, 5]
    cgpa_groups = [1.0, 2.5, 3.5, 4.0]

    cgpa_labels = ['CGPA 1.0', 'CGPA 2.5', 'CGPA 3.5', 'CGPA 4.0']
    colors = ['#f27d72', '#f7c440', '#4f8df5', '#64c7c8']

    fig = go.Figure()

    for cgpa, label, color in zip(cgpa_groups, cgpa_labels, colors):

        counts = [
            len(df[(df["cgpa"] == cgpa) & (df["procrastination_level"] == p)])
            for p in proc_levels
        ]

        fig.add_trace(
            go.Bar(
                x=[f"Level {p}" for p in proc_levels],
                y=counts,
                name=label,
                marker_color=color,
            )
        )

    fig.update_layout(
        barmode='stack',   # 🔥 THIS IS THE KEY
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Procrastination Level (1 = Never → 5 = Always)",
        yaxis_title="Number of Students",
        legend=dict(orientation="h", y=1.15, x=0),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.markdown(
        """
        <div class="chart-card-header">
            <h3>Procrastination Level vs CGPA Distribution</h3>
            <p>Stacked view reveals how academic performance is distributed across procrastination levels.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------
# Last-Minute Studying vs CGPA
# -----------------------------------------------
def last_minute_chart(df):
    order = ["No Cramming", "Regular Cramming"]
    summary = df.groupby("last_minute_studying", as_index=False)["cgpa"].mean()
    summary["last_minute_studying"] = pd.Categorical(
        summary["last_minute_studying"], categories=order, ordered=True
    )
    summary = summary.sort_values("last_minute_studying")

    chart_header(
        "Last-Minute Studying vs CGPA",
        "Cramming increases effort but does not consistently improve performance.",
    )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=summary["last_minute_studying"],
            y=summary["cgpa"],
            text=summary["cgpa"].round(2),
            textposition="outside",
            marker=dict(color=["#cf5bbd", "#ea6e84"]),
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=300,
        margin=dict(l=20, r=20, t=10, b=20),
        yaxis=dict(title="Average CGPA", range=[0, 4]),
        xaxis=dict(title=""),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------
# Sleep Hours vs CGPA & Stress
# -----------------------------------------------
def sleep_chart(df):
    summary = (
        df.groupby("sleep_hours", as_index=False)
        .agg(avg_cgpa=("cgpa", "mean"), avg_stress=("stress_end", "mean"))
        .sort_values("sleep_hours")
    )

    chart_header(
        "Sleep Hours vs Stress & CGPA",
        "Adequate sleep supports better performance and lower stress levels.",
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=summary["sleep_hours"],
            y=summary["avg_cgpa"],
            mode="lines+markers",
            name="CGPA",
            yaxis="y1",
            line=dict(color="#22c7f0", width=3),
            marker=dict(size=8, color="#22c7f0"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=summary["sleep_hours"],
            y=summary["avg_stress"],
            mode="lines+markers",
            name="Stress",
            yaxis="y2",
            line=dict(color="#ef7a7a", width=3),
            marker=dict(size=8, color="#ef7a7a"),
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=300,
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis=dict(title="Sleep Hours"),
        yaxis=dict(title="CGPA", range=[0, 4]),
        yaxis2=dict(title="Stress", overlaying="y", side="right", range=[0, 5]),
        legend=dict(orientation="h", y=-0.22, x=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    st.plotly_chart(fig, use_container_width=True)


def show_behavioral_insights():
    load_css()
    df = load_data()

    st.markdown('<div class="section-tag stress-tag">Stress Analysis</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Academic Pressure Builds Over Time</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Stress levels were analyzed at the beginning and end of the study period — and what drives them.</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        stress_start_end_chart(df)
    with col2:
        stress_vs_procrastination_chart(df)

    st.markdown('<div class="section-divider"><span>Behavioral Patterns</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-tag habits-tag">Habits &amp; Lifestyle</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="subpage-title">How Daily Habits Shape Academic Outcomes</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Beyond stress, procrastination patterns, last-minute behavior, and sleep all play a critical role.</p>',
        unsafe_allow_html=True
    )

    col3, col4, col5 = st.columns(3, gap="large")
    with col3:
        procrastination_vs_cgpa_stacked_chart(df)
    with col4:
        last_minute_chart(df)
    with col5:
        sleep_chart(df)

    st.markdown(
        """
        <div class="highlight-banner">
            <h3>Academic success is shaped by a combination of behavioral habits — not study effort alone.</h3>
            <p>Procrastination, sleep quality, and stress management are critical factors in achieving better outcomes.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


show_behavioral_insights()