# core_analysis.py (updated)

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# -------------------------
# Color Palette
# -------------------------
BLUE   = '#4A7FBF'
TEAL   = '#2EAD8A'
AMBER  = '#E8A020'
CORAL  = '#E05C3A'
PURPLE = '#7B68C8'
GRAY   = '#9A9890'

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
        "study hours per day": "study_hours_per_day",
        "study method": "study_method",
        "procrastination level": "procrastination_level",
        "sleep hours": "sleep_hours",
        "stress level (beginning of semester)": "stress_start",
        "stress level (end of semester)": "stress_end",
        "study hours before exam": "study_hours_before_exam",
    }
    df = df.rename(columns=rename_map)

    return df


def metric_card(title, value, subtitle, color=BLUE):
    st.markdown(
        f"""
        <div style="
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 1.2rem 1rem;
            text-align: center;
            box-shadow: 0 8px 24px rgba(36, 37, 38, 0.08);
            border-left: 4px solid {color};
            height: 100%;
        ">
            <p style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">
                {title}
            </p>
            <p style="font-size: 2.8rem; font-weight: 800; color: #111827; margin-bottom: 0.25rem; line-height: 1;">
                {value}
            </p>
            <p style="font-size: 0.8rem; color: #9ca3af; margin: 0;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def study_hours_boxplot(df):
    """Create a box plot for study hours by CGPA group - matching matplotlib style"""
    cgpa_order = [1.0, 2.5, 3.5, 4.0]
    cgpa_labels = ['1.0<br>(Failing)', '2.5<br>(Pass)', '3.5<br>(Good)', '4.0<br>(Excellent)']
    colors = [CORAL, AMBER, BLUE, TEAL]

    fig = go.Figure()

    # Set random seed for consistent jitter
    np.random.seed(42)

    for i, (cgpa, label, color) in enumerate(zip(cgpa_order, cgpa_labels, colors), start=1):
        subset = df[df["cgpa"] == cgpa]["study_hours_per_day"].dropna()
        
        # Add jittered scatter points
        jitter = np.random.uniform(-0.25, 0.25, size=len(subset))
        x_jittered = [i + j for j in jitter]
        
        fig.add_trace(go.Scatter(
            x=x_jittered,
            y=subset,
            mode='markers',
            marker=dict(
                size=6,
                color=color,
                opacity=0.35,
                symbol='circle'
            ),
            showlegend=False,
            hoverinfo='y',
            name=f'Data points - {label.replace("<br>", " ")}'
        ))
        
        # Add box plot
        fig.add_trace(go.Box(
            y=subset,
            x=[i] * len(subset),
            name=label,
            boxmean=False,
            marker_color=color,
            line=dict(color=color, width=1.5),
            fillcolor=color,
            opacity=0.75,
            boxpoints=False,
            whiskerwidth=0.6,
            showlegend=False,
            hoverinfo='y',
            quartilemethod="linear",
        ))

    fig.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(l=40, r=20, t=60, b=50),
        paper_bgcolor="rgba(255,255,255,0.85)",
        plot_bgcolor="rgba(255,255,255,0.85)",
        yaxis=dict(
            title="Study Hours per Day",
            gridcolor='#E8E6E0',
            zeroline=False,
            range=[0, 8],
            dtick=1,
        ),
        xaxis=dict(
            title="CGPA Group",
            tickangle=0,
            tickfont=dict(size=11),
        ),
        title=dict(
            text="<b>Study Hours per Day by CGPA Group</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=14)
        ),
    )
    
    # Add subtitle annotation
    fig.add_annotation(
        text="Wide spread within each group — duration alone does not predict performance",
        xref="paper",
        yref="paper",
        x=0,
        y=1.08,
        showarrow=False,
        font=dict(size=10, color="#6B6960"),
        align="left"
    )

    return fig


def study_method_vs_cgpa(df):
    """Create a stacked bar chart for study method composition by CGPA"""
    
    # The column is now 'study_method' after cleaning
    study_method_col = 'study_method'
    
    if study_method_col not in df.columns:
        st.error(f"Study Method column '{study_method_col}' not found. Available columns: {', '.join(df.columns.tolist())}")
        return None
    
    # Consolidate minor categories
    method_map = {
        'Summarizing/making notes':          'Summarizing / notes',
        'Doing practice questions':          'Practice questions',
        'Reading lecture notes':             'Reading notes',
        'Watching recorded lectures/videos': 'Watching videos',
        'Ai generated quiz game':            'Other',
        'all of the above':                  'Other',
    }
    
    # Create cleaned method column
    df['Method_Clean'] = df[study_method_col].map(method_map).fillna('Other')
    
    cgpa_order = [1.0, 2.5, 3.5, 4.0]
    cgpa_labels = ['1.0', '2.5', '3.5', '4.0']
    methods = ['Practice questions', 'Summarizing / notes', 'Reading notes', 'Watching videos', 'Other']
    method_colors = [TEAL, BLUE, PURPLE, AMBER, GRAY]
    
    # Create cross tabulation
    ct = pd.crosstab(df['cgpa'], df['Method_Clean'])
    ct = ct.reindex(columns=methods, fill_value=0)
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    ct_pct = ct_pct.reindex(cgpa_order, fill_value=0)
    
    # Create figure
    fig = go.Figure()
    
    for method, color in zip(methods, method_colors):
        values = ct_pct[method].values
        
        fig.add_trace(go.Bar(
            x=cgpa_labels,
            y=values,
            name=method,
            marker_color=color,
            marker=dict(opacity=0.88),
            text=[f'{v:.0f}%' if v > 6 else '' for v in values],
            textposition='inside',
            textfont=dict(color='white', size=11, weight='bold'),
            hovertemplate=f'{method}: %{{y:.1f}}%<extra></extra>',
        ))
    
    fig.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(l=40, r=120, t=60, b=50),
        paper_bgcolor="rgba(255,255,255,0.85)",
        plot_bgcolor="rgba(255,255,255,0.85)",
        barmode='stack',
        yaxis=dict(
            title="% of Students",
            gridcolor='#E8E6E0',
            zeroline=False,
            range=[0, 100],
            tickformat='.0f',
            ticksuffix='%',
        ),
        xaxis=dict(
            title="CGPA Group",
            tickangle=0,
            tickfont=dict(size=11),
        ),
        title=dict(
            text="<b>Study Method Composition by CGPA Group</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=14)
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E8E6E0",
            borderwidth=1,
            font=dict(size=10)
        ),
    )
    
    # Add subtitle annotation
    fig.add_annotation(
        text="Practice questions are more prevalent among higher-performing students",
        xref="paper",
        yref="paper",
        x=0,
        y=1.08,
        showarrow=False,
        font=dict(size=10, color="#6B6960"),
        align="left"
    )
    
    return fig

def show_core_analysis():
    load_css()
    df = load_data()

    # Page Header
    st.markdown(
        """
        <div style="text-align: center; padding-top: 1rem; padding-bottom: 1rem;">
            <h1 class="page-title">Core Analysis: Does Study Time Really Matter?</h1>
            <p class="page-subtitle">
                Examining the relationship between study hours, study methods, and academic performance
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metrics Row - Two cards
    col1, col2 = st.columns(2, gap="large")

    with col1:
        total_students = len(df)
        metric_card(
            "Total Students Surveyed",
            f"{total_students:,}",
            "Across all courses and study years",
            color=BLUE
        )

    with col2:
        avg_cgpa = df["cgpa"].mean()
        metric_card(
            "Average CGPA",
            f"{avg_cgpa:.2f}",
            "Overall student performance",
            color=TEAL
        )

    # Charts below metrics
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Study Hours Box Plot
    st.markdown(
        """
        <div class="chart-card-header">
            <h3>📊 Study Hours Distribution by CGPA Group</h3>
            <p>Box plot showing the spread of daily study hours across different performance levels</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    boxplot_fig = study_hours_boxplot(df)
    st.plotly_chart(boxplot_fig, use_container_width=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Study Method Stacked Bar Chart
    st.markdown(
        """
        <div class="chart-card-header">
            <h3>📚 Study Method Composition by CGPA Group</h3>
            <p>How study strategies differ across academic performance levels</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    method_fig = study_method_vs_cgpa(df)
    if method_fig:
        st.plotly_chart(method_fig, use_container_width=True)

    # Add insight note
    st.markdown(
        """
        <div class="highlight-banner" style="margin-top: 1.5rem;">
            <h3>💡 Key Insights</h3>
            <p>
                <strong>1. Study Hours Alone Don't Determine Success:</strong> Students across all CGPA levels show similar ranges of study hours.<br>
                <strong>2. Study Methods Matter More:</strong> Higher-performing students are more likely to use <strong>practice questions</strong> 
                and active recall techniques, while lower performers rely more on passive methods like <strong>reading notes</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    show_core_analysis()