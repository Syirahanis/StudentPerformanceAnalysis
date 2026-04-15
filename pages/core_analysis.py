# core_analysis.py (updated - side by side charts)

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

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
        "study days per week": "study_days_per_week",
        "study method": "study_method",
        "procrastination level": "procrastination_level",
        "sleep hours": "sleep_hours",
        "stress level (beginning of semester)": "stress_start",
        "stress level (end of semester)": "stress_end",
        "study hours before exam": "study_hours_before_exam",
    }
    df = df.rename(columns=rename_map)
    
    # Calculate weekly study hours
    df['weekly_study_hours'] = df['study_hours_per_day'] * df['study_days_per_week']

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


def cgpa_vs_study_hours_scatter(df):
    """Create a scatter plot showing CGPA vs Study Hours with jitter - swapped axes to show distribution of study hours across CGPA levels"""
    
    # Create a copy to avoid modifying original
    plot_df = df[['weekly_study_hours', 'cgpa']].dropna().copy()
    
    # Define CGPA categories in order
    cgpa_categories = [1.0, 2.5, 3.5, 4.0]
    cgpa_labels = ['1.0', '2.5', '3.5', '4.0']
    
    # Create a mapping for categorical x-axis positions (evenly spaced)
    cat_positions = {1.0: 0, 2.5: 1, 3.5: 2, 4.0: 3}
    
    # Add jitter to study hours to prevent overlapping
    np.random.seed(42)
    jitter_amount = 2.5
    plot_df['study_hours_jittered'] = plot_df['weekly_study_hours'] + np.random.uniform(-jitter_amount, jitter_amount, size=len(plot_df))
    
    # Color mapping for CGPA levels
    color_map = {
        4.0: TEAL,
        3.5: BLUE,
        2.5: AMBER,
        1.0: CORAL
    }
    
    # Calculate statistics for each CGPA level
    stats_by_cgpa = {}
    for cgpa_value in cgpa_categories:
        subset = plot_df[plot_df['cgpa'] == cgpa_value]['weekly_study_hours']
        if len(subset) > 0:
            stats_by_cgpa[cgpa_value] = {
                'mean': subset.mean(),
                'median': subset.median(),
                'std': subset.std(),
                'min': subset.min(),
                'max': subset.max(),
                'count': len(subset)
            }
    
    # Create figure
    fig = go.Figure()
    
    # Add scatter points for each CGPA level
    for cgpa_value in cgpa_categories:
        subset = plot_df[plot_df['cgpa'] == cgpa_value]
        
        # Add jitter to x-axis position (within the category band)
        x_jitter = np.random.uniform(-0.25, 0.25, size=len(subset))
        x_positions = [cat_positions[cgpa_value] + j for j in x_jitter]
        
        # Prepare hover text with detailed information
        hover_texts = [
            f"<b>CGPA: {row['cgpa']}</b><br>"
            f"Weekly Study Hours: {row['weekly_study_hours']:.0f} hrs/week<br>"
            f"Daily Average: {row['weekly_study_hours']/7:.1f} hrs/day<br>"
            f"Group average: {stats_by_cgpa[row['cgpa']]['mean']:.0f} hrs/week<br>"
            f"{'✨ Efficient learner (below group avg)' if row['weekly_study_hours'] < stats_by_cgpa[row['cgpa']]['mean'] else '📚 Above average study time'}"
            for _, row in subset.iterrows()
        ]
        
        fig.add_trace(go.Scatter(
            x=x_positions,
            y=subset['study_hours_jittered'],
            mode='markers',
            name=f'CGPA {cgpa_value}',
            marker=dict(
                size=10,
                color=color_map[cgpa_value],
                opacity=0.55,
                line=dict(width=1, color='white'),
                symbol='circle'
            ),
            text=hover_texts,
            hoverinfo='text',
            showlegend=True,
        ))
        
    
    # Calculate correlation using categorical positions for trendline
    # Create arrays with categorical positions
    x_for_trend = []
    y_for_trend = []
    for cgpa_value in cgpa_categories:
        subset = plot_df[plot_df['cgpa'] == cgpa_value]['weekly_study_hours']
        for hours in subset:
            x_for_trend.append(cat_positions[cgpa_value])
            y_for_trend.append(hours)
    
    # Add trendline (linear regression) using categorical positions
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        x_for_trend, 
        y_for_trend
    )
    
    correlation = r_value
    correlation_text = "Very Weak" if abs(correlation) < 0.2 else "Weak" if abs(correlation) < 0.4 else "Moderate"
    
    fig.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(l=40, r=30, t=50, b=40),
        paper_bgcolor="rgba(255,255,255,0.85)",
        plot_bgcolor="rgba(255,255,255,0.85)",
        xaxis=dict(
            title="<b>CGPA</b>",
            gridcolor='#E8E6E0',
            zeroline=False,
            range=[-0.5, 3.5],
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=['<b>1.0</b><br>(Failing)', '<b>2.5</b><br>(Pass)', '<b>3.5</b><br>(Good)', '<b>4.0</b><br>(Excellent)'],
            title_font=dict(size=11),
        ),
        yaxis=dict(
            title="<b>Weekly Study Hours</b>",
            gridcolor='#E8E6E0',
            zeroline=False,
            range=[0, 50],
            dtick=10,
            title_font=dict(size=11),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E8E6E0",
            borderwidth=1,
            font=dict(size=9)
        ),
    )
    

    return fig

def study_method_vs_cgpa(df):
    """Create a stacked bar chart for study method composition by CGPA"""
    
    study_method_col = 'study_method'
    
    if study_method_col not in df.columns:
        st.error(f"Study Method column '{study_method_col}' not found.")
        return None
    
    # Consolidate minor categories
    method_map = {
        'Summarizing/making notes':          'Summarizing / notes',
        'Doing practice questions':          'Practice questions',
        'Reading lecture notes':             'Reading notes',
        'Watching recorded lectures/videos': 'Watching videos',
        'Ai generated quiz game':            'AI Quiz Game',
    }
    
    # Create cleaned method column
    df['Method_Clean'] = df[study_method_col].map(method_map).fillna('Other')
    
    cgpa_order = [1.0, 2.5, 3.5, 4.0]
    cgpa_labels = ['1.0', '2.5', '3.5', '4.0']
    methods = ['Practice questions', 'Summarizing / notes', 'Reading notes', 'Watching videos', 'AI Quiz Game']
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
            text=[f'{v:.0f}%' if v > 8 else '' for v in values],
            textposition='inside',
            textfont=dict(color='white', size=10, weight='bold'),
            hovertemplate=f'{method}: %{{y:.1f}}%<extra></extra>',
        ))
    
    fig.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(l=40, r=40, t=80, b=40),  # Increased top margin for legend
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
            title="CGPA",
            tickangle=0,
            tickfont=dict(size=11),
        ),
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=1.1,  # Position above the chart
            xanchor="center",
            x=0.45,  # Centered
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E8E6E0",
            borderwidth=1,
            font=dict(size=10),
            itemclick="toggle",
            itemdoubleclick="toggleothers"
        ),
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

    # Metrics Row
    col1, col2 = st.columns(2, gap="large")
    with col1:
        metric_card("Total Students Surveyed", f"{len(df):,}", "Across all courses and study years", color=BLUE)
    with col2:
        metric_card("Average CGPA", f"{df['cgpa'].mean():.2f}", "Overall student performance", color=TEAL)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Two charts side by side
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 0.5rem;">
                <h3>📊 CGPA vs Weekly Study Hours</h3>
                <p style="color: #6b7280; font-size: 0.85rem;">Study quantity doesn't guarantee success</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(cgpa_vs_study_hours_scatter(df), use_container_width=True)

    with col_right:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 0.5rem;">
                <h3>📚 Study Methods by CGPA</h3>
                <p style="color: #6b7280; font-size: 0.85rem;">Method diversity and balance lead to success</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        method_fig = study_method_vs_cgpa(df)
        if method_fig:
            st.plotly_chart(method_fig, use_container_width=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Combined Interpretation using Streamlit components
    with st.container():
        st.markdown("---")
        st.markdown("## 📖 What These Charts Tell Us")
        
        col_interpret_left, col_interpret_right = st.columns(2)
        
        with col_interpret_left:
            st.markdown("### 📉 Left Chart: CGPA vs Weekly Study Hours")
            st.markdown(
                """
                **CGPA vs Weekly Study Hours** shows that students across all CGPA levels 
                study similar hours (15-35 hrs/week). The **trendline is flat/negative**, 
                proving that studying longer doesn't lead to better grades.
                
                - ⚠️ Some struggling students (CGPA 1.0) study 35+ hours weekly but still fail
                - ✨ Many top performers (CGPA 4.0) study only 15-20 hours and excel
                - 📊 **Key takeaway:** It's not HOW LONG you study, but HOW you study
                """
            )
        
        with col_interpret_right:
            st.markdown("### 📚 Right Chart: Study Methods by CGPA")
            st.markdown(
                """
                **Study Methods by CGPA** reveals the REAL difference maker:
                
                - 🟢 **CGPA 4.0 (Excellent):** 100% Summarizing/notes — mastered the art of synthesis
                - 🔵 **CGPA 3.5 (Good):** Balanced approach — 45% Summarizing + 38% Practice Questions
                - 🟡 **CGPA 2.5 (Pass):** 75% Summarizing + 25% Videos — missing active recall
                - 🔴 **CGPA 1.0 (Failing):** 100% Practice Questions — all practice, no theory
                
                **The sweet spot:** CGPA 3.5 shows that **balance** between summarizing (45%) 
                and practice questions (38%) yields strong results before mastering summarization alone.
                """
            )
        
        st.info(
            "🎯 **The Verdict:** Study *quantity* doesn't determine success — "
            "the *right balance of study methods* does! Start with diverse methods (like CGPA 3.5), "
            "then streamline to what works best for you (like CGPA 4.0)."
        )
        
        # Add a second insight box with learning progression
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #E8F4FD 0%, #FFFFFF 100%); 
                        border-radius: 12px; 
                        padding: 1rem 1.5rem; 
                        margin-top: 1rem;
                        border-left: 4px solid #2EAD8A;">
                <p style="margin: 0; font-size: 0.95rem;">
                <strong>📈 The Learning Progression Revealed:</strong><br>
                <span style="color: #E05C3A;">CGPA 1.0</span> → Practice only (ineffective)<br>
                <span style="color: #E8A020;">CGPA 2.5</span> → Passive learning (summarizing + videos)<br>
                <span style="color: #4A7FBF;">CGPA 3.5</span> → <strong>BALANCED</strong> (summarizing + practice questions) ← The winning formula!<br>
                <span style="color: #2EAD8A;">CGPA 4.0</span> → Mastered summarization (efficient synthesis)
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    show_core_analysis()

