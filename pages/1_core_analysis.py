# core_analysis.py (enhanced – uses st.dialog for modals + 4 metric cards)

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
    css_path = os.path.join(base_path, "style", "core.css")
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
        "course": "course",
        "gender": "gender",
    }
    df = df.rename(columns=rename_map)
    df['weekly_study_hours'] = df['study_hours_per_day'] * df['study_days_per_week']

    if 'course' not in df.columns:
        courses = ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Economics']
        df['course'] = np.random.choice(courses, size=len(df))

    if 'gender' not in df.columns:
        df['gender'] = np.random.choice(['Male', 'Female'], size=len(df))

    return df


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _categorize_cgpa(cgpa):
    if cgpa >= 3.9:
        return '4.00 – Excellent'
    elif cgpa >= 3.4:
        return '3.50 – Good'
    elif cgpa >= 2.4:
        return '2.50 – Satisfactory'
    else:
        return '1.00 – Needs Improvement'


# ─────────────────────────────────────────────────────────────────────────────
# NATIVE STREAMLIT DIALOG (st.dialog – Streamlit ≥ 1.36)
# ─────────────────────────────────────────────────────────────────────────────

def _render_student_details(df: pd.DataFrame):
    """Render the full student-population breakdown inside a dialog or expander."""

    total = len(df)

    # ── Gender ──────────────────────────────────────────────────────────────
    st.markdown("#### 👥 Gender Distribution")
    gender_counts = df['gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    gender_counts['Percentage'] = (gender_counts['Count'] / total * 100).round(1).astype(str) + '%'

    # Changed: Bar chart to PIE CHART
    gender_color_map = {
        'Male': "#4A7FBF8C",    # Blue
        'Female': "#EC489A77",   # Pink
    }

    gender_colors = [gender_color_map.get(gender, '#9CA3AF') for gender in gender_counts['Gender']]
    
    g_fig = go.Figure(go.Pie(
        labels=gender_counts['Gender'],
        values=gender_counts['Count'],
        marker=dict(colors=gender_colors, line=dict(color='white', width=2)),
        textinfo='label+percent',
        textposition='auto',
        hoverinfo='label+value+percent',
        hole=0.4,  # Donut style (optional, set to 0 for full pie)
        showlegend=True,
        legendgroup='gender',
        pull=[0.02 if i == gender_counts['Count'].argmax() else 0 for i in range(len(gender_counts))],
    ))
    g_fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        ),
    )
    st.plotly_chart(g_fig, use_container_width=True, config={'displayModeBar': False})
    st.dataframe(
        gender_counts,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

        # ── Course ───────────────────────────────────────────────────────────────
    st.markdown("#### 📚 Course Distribution")
    
    # Function to extract course family
    def get_course_family(course):
        import re
        # Remove prefixes
        course = re.sub(r'^(Bachelor of |Diploma in )', '', str(course))
        
        # Map similar courses
        if re.search(r'Computer Science|Software Engineering|Game Development|Information Technology|Informatics Maritime', course, re.I):
            return 'Computer Science'
        elif re.search(r'Accounting', course, re.I):
            return 'Accounting'
        elif re.search(r'Medicine|MBBS|Biomedical|Dental Surgery|Medical Imaging|Physiotherapy', course, re.I):
            return 'Medicine/Medical'
        elif re.search(r'Business|Management|Investment|International Business', course, re.I):
            return 'Business/Management'
        elif re.search(r'Digital Media|Media Production', course, re.I):
            return 'Digital Media/Production'
        elif re.search(r'Islamic|Halal', course, re.I):
            return 'Islamic Studies/Finance'
        elif re.search(r'Education|Teaching|TESL', course, re.I):
            return 'Education/Teaching'
        elif re.search(r'Engineering', course, re.I):
            return 'Engineering'
        elif re.search(r'Pharmacy', course, re.I):
            return 'Pharmacy'
        elif re.search(r'Arts', course, re.I):
            return 'Arts'
        elif re.search(r'Psychology', course, re.I):
            return 'Psychology'
        elif re.search(r'Science(?! Computer)', course, re.I):
            return 'Science'
        elif re.search(r'Chemistry', course, re.I):
            return 'Chemistry'
        elif re.search(r'Arabic', course, re.I):
            return 'Arabic'
        elif re.search(r'Communication', course, re.I):
            return 'Communications'
        else:
            return course.strip()
    
    # Apply course family mapping
    df['course_family'] = df['course'].apply(get_course_family)
    
    # Count by course family
    course_counts = df['course_family'].value_counts().reset_index()
    course_counts.columns = ['Course Family', 'Students']
    course_counts['% of Total'] = (course_counts['Students'] / total * 100).round(1).astype(str) + '%'
    
    # Sort by student count descending for better visualization
    course_counts = course_counts.sort_values('Students', ascending=True)

    # Create color palette for courses (using a nice gradient)
    course_colors = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel
    
    c_fig = go.Figure(go.Bar(
        y=course_counts['Course Family'],
        x=course_counts['Students'],
        orientation='h',
        marker_color=course_colors[:len(course_counts)],
        marker_opacity=0.85,
        text=course_counts['Students'],
        textposition='outside',
        textfont=dict(size=10, color='#374151'),
        hovertemplate='<b>%{y}</b><br>Students: %{x}<br>% of Total: %{customdata}<extra></extra>',
        customdata=course_counts['% of Total'],
    ))
    c_fig.update_layout(
        height=max(350, len(course_counts) * 35),  # Dynamic height based on number of courses
        margin=dict(l=10, r=60, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='#E5E7EB',
            gridwidth=0.5,
            showticklabels=True,
            tickfont=dict(size=10),
            title="Number of Students",
            title_font=dict(size=11),
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=10.5),
            automargin=True,
            title=None,
        ),
        showlegend=False,
        bargap=0.2,
    )
    st.plotly_chart(c_fig, use_container_width=True, config={'displayModeBar': False})
    
    st.dataframe(
        course_counts.sort_values('Students', ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Course Family": "Course Family",
            "Students": st.column_config.NumberColumn("Students", format="%d"),
            "% of Total": st.column_config.TextColumn("% of Total"),
        }
    )

    st.divider()


def _render_cgpa_details(df: pd.DataFrame):
    """Render the full student-population breakdown inside a dialog or expander."""

    total = len(df)

    # ── CGPA Groups ──────────────────────────────────────────────────────────
    st.markdown("#### 🎓 Students per CGPA Group")
    df_copy = df.copy()
    df_copy['CGPA Group'] = df_copy['cgpa'].apply(_categorize_cgpa)

    cgpa_group_order = [
        '4.00 – Excellent',
        '3.50 – Good',
        '2.50 – Satisfactory',
        '1.00 – Needs Improvement',
    ]
    
    # Shortened labels for better display
    short_labels = {
        '4.00 – Excellent': 'Excellent (4.00)',
        '3.50 – Good': 'Good (3.00-3.99)',
        '2.50 – Satisfactory': 'Satisfactory (2.00-2.99)',
        '1.00 – Needs Improvement': 'Needs Improvement (1.00-1.99)',
    }
    
    group_colors = {
        '4.00 – Excellent': '#C5E0B4',  # Soft pastel green
        '3.50 – Good': '#A7C7E8',       # Soft pastel blue
        '2.50 – Satisfactory': '#FFD966', # Soft pastel yellow
        '1.00 – Needs Improvement': '#F4B6C2', # Soft pastel pink
    }

    cgpa_counts = (
        df_copy['CGPA Group']
        .value_counts()
        .reindex(cgpa_group_order, fill_value=0)
        .reset_index()
    )
    cgpa_counts.columns = ['CGPA Group', 'Students']
    cgpa_counts['% of Total'] = (cgpa_counts['Students'] / total * 100).round(1).astype(str) + '%'
    
    # Add short labels for display
    cgpa_counts['Display Group'] = cgpa_counts['CGPA Group'].map(short_labels)

    # Gender breakdown per CGPA group
    cgpa_gender = (
        df_copy.groupby(['CGPA Group', 'gender'])
        .size()
        .unstack(fill_value=0)
        .reindex(cgpa_group_order, fill_value=0)
        .reset_index()
    )

    # FIXED: Bar chart with proper label positioning
    cg_fig = go.Figure()
    
    # Get max value for dynamic y-axis range (adds headroom for labels)
    max_students = cgpa_counts['Students'].max()
    
    for i, group in enumerate(cgpa_group_order):
        mask = cgpa_counts['CGPA Group'] == group
        student_count = cgpa_counts.loc[mask, 'Students'].values[0]
        
        cg_fig.add_trace(go.Bar(
            x=[short_labels[group]],  # Use short label
            y=[student_count],
            name=group,
            marker_color=group_colors[group],
            text=[f"{student_count}"],
            textposition='outside',
            textfont=dict(size=11, color='#374151'),
            hovertemplate=f'<b>{short_labels[group]}</b><br>Students: {student_count}<br>Percentage: {(student_count/total*100):.1f}%<extra></extra>',
        ))
    
    cg_fig.update_layout(
        height=360,  # Increased height to accommodate labels
        margin=dict(l=30, r=30, t=50, b=30),  # Increased top margin for label visibility
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=12),
            title="CGPA Range",
            title_font=dict(size=12),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E5E7EB',
            gridwidth=0.5,
            showticklabels=True,
            tickfont=dict(size=11),
            title="Number of Students",
            title_font=dict(size=12),
            range=[0, max_students * 1.25],  # Add 25% headroom for labels
        ),
        showlegend=False,
        bargap=0.35,
    )
    st.plotly_chart(cg_fig, use_container_width=True, config={'displayModeBar': False})

    # Merge totals with gender breakdown
    display_df = cgpa_counts[['Display Group', 'Students', '% of Total']].copy()
    display_df.columns = ['CGPA Group', 'Students', '% of Total']
    
    for col in cgpa_gender.columns[1:]:
        if col in cgpa_gender.columns:
            display_df[col] = cgpa_gender[col].values
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.caption(f"Total students: **{total:,}** · Genders: **{len(df['gender'].unique())}**")

# ─────────────────────────────────────────────────────────────────────────────
# DIALOG WRAPPER – uses @st.dialog when available, expander as fallback
# ─────────────────────────────────────────────────────────────────────────────

def _open_student_details_dialog(df: pd.DataFrame):
    """Try to open a native Streamlit dialog."""
    try:
        @st.dialog("📊 Student Population Details", width="large")
        def _dialog():
            _render_student_details(df)
        _dialog()
    except AttributeError:
        with st.expander("📊 Student Population Details", expanded=True):
            _render_student_details(df)

def _open_cgpa_details_dialog(df: pd.DataFrame):
    """Try to open a native Streamlit dialog."""
    try:
        @st.dialog("📊 CGPA Distribution Details", width="large")
        def _dialog():
            _render_cgpa_details(df)
        _dialog()
    except AttributeError:
        with st.expander("📊 CGPA Distribution Details", expanded=True):
            _render_cgpa_details(df)


# ─────────────────────────────────────────────────────────────────────────────
# METRIC CARD 1 – Total Students (Number only)
# ─────────────────────────────────────────────────────────────────────────────

def metric_card_total_students(df):
    """Metric card: Just the total number of students."""
    
    total_students = len(df)
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
            border-radius: 24px;
            border: 1px solid rgba(46,173,138,0.15);
            box-shadow: 0 8px 20px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.02);
            transition: all 0.3s ease;
            overflow: hidden;
            width: 100%;
        ">
            <div style="
                background: linear-gradient(135deg, rgba(46,173,138,0.08) 0%, rgba(46,173,138,0.02) 100%);
                padding: 0.9rem 1.2rem 1rem 1.2rem;
                text-align: center;
            ">
                <div style="
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 40px;
                    height: 40px;
                    background: rgba(46,173,138,0.12);
                    border-radius: 12px;
                    margin-bottom: 0.75rem;
                ">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2EAD8A" stroke-width="1.8">
                        <path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                    </svg>
                </div>
                <div style="
                    font-size: 0.75rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    color: #2EAD8A;
                    margin-bottom: 0.5rem;
                ">
                    Total Students
                </div>
                <div style="
                    font-size: 3rem;
                    font-weight: 800;
                    color: #111827;
                    line-height: 1;
                    margin-bottom: 0.25rem;
                ">
                    {total_students:,}
                </div>
                <div style="
                    font-size: 0.9rem;
                    color: #9CA3AF;
                    margin-top: 0.25rem;
                ">
                    participants<br>
                    surveyed 
                </div>     
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# METRIC CARD 2 – Average CGPA
# ─────────────────────────────────────────────────────────────────────────────

def metric_card_avg_cgpa(df):
    """Metric card: Average CGPA with a simple gauge style."""
    
    avg_cgpa = df['cgpa'].mean()
    
    # Create a simple progress bar visualization
    progress_percent = (avg_cgpa / 4.0) * 100
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
            border-radius: 24px;
            border: 1px solid rgba(232,160,32,0.15);
            box-shadow: 0 8px 20px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.02);
            transition: all 0.3s ease;
            overflow: hidden;
            width: 100%;
        ">
            <div style="
                background: linear-gradient(135deg, rgba(232,160,32,0.06) 0%, rgba(232,160,32,0.01) 100%);
                padding: 1rem 1.2rem 1rem 1.2rem;
                text-align: center;
            ">
                <div style="
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 40px;
                    height: 40px;
                    background: rgba(232,160,32,0.12);
                    border-radius: 12px;
                    margin-bottom: 0.75rem;
                ">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#E8A020" stroke-width="1.8">
                        <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                    </svg>
                </div>
                <div style="
                    font-size: 0.75rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    color: #E8A020;
                    margin-bottom: 0.5rem;
                ">
                    Average CGPA
                </div>
                <div style="
                    font-size: 3rem;
                    font-weight: 800;
                    color: #111827;
                    line-height: 1;
                    margin-bottom: 0.5rem;
                ">
                    {avg_cgpa:.2f}
                </div>
                <div style="
                    background: rgba(232,160,32,0.1);
                    border-radius: 10px;
                    height: 6px;
                    width: 100%;
                    margin: 0.75rem 0;
                    overflow: hidden;
                ">
                    <div style="
                        background: linear-gradient(90deg, #E8A020 0%, #F59E0B 100%);
                        width: {progress_percent:.1f}%;
                        height: 100%;
                        border-radius: 10px;
                        transition: width 0.5s ease;
                    "></div>
                </div>
                <div style="
                    display: flex;
                    justify-content: space-between;
                    font-size: 0.65rem;
                    color: #9CA3AF;
                    margin-top: 0.25rem;
                ">
                    <span>0.00</span>
                    <span>4.00 Scale</span>
                    <span>4.00</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# CGPA Group config – single source of truth
# ─────────────────────────────────────────────────────────────────────────────

CGPA_GROUPS = {
    '🏆 Excellent (4.00)': {
        'filter': lambda d: d['cgpa'] == 4.00,
        'color': '#7B68C8',       # purple
        'bg':    'rgba(123,104,200,0.12)',
        'border':'#7B68C8',
        'emoji': '🏆',
        'label': 'Excellent',
        'range': '4.00',
    },
    '🎓 Good (3.00-3.99)': {
        'filter': lambda d: (d['cgpa'] >= 3.00) & (d['cgpa'] < 4.00),
        'color': '#4A7FBF',       # blue
        'bg':    'rgba(74,127,191,0.12)',
        'border':'#4A7FBF',
        'emoji': '🎓',
        'label': 'Good',
        'range': '3.00–3.99',
    },
    '📘 Satisfactory (2.00-2.99)': {
        'filter': lambda d: (d['cgpa'] >= 2.00) & (d['cgpa'] < 3.00),
        'color': '#E8A020',       # amber
        'bg':    'rgba(232,160,32,0.12)',
        'border':'#E8A020',
        'emoji': '📘',
        'label': 'Satisfactory',
        'range': '2.00–2.99',
    },
    '📉 Needs Improvement (<2.00)': {
        'filter': lambda d: d['cgpa'] < 2.00,
        'color': '#E05C3A',       # coral
        'bg':    'rgba(224,92,58,0.12)',
        'border':'#E05C3A',
        'emoji': '📉',
        'label': 'Needs Improvement',
        'range': '< 2.00',
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Chart – Interactive CGPA-Group Scatter (replaces both old charts)
# ─────────────────────────────────────────────────────────────────────────────

def cgpa_vs_study_hours_interactive(df):
    """
    All-in-one interactive scatter:
    • Toggle any of the 4 CGPA groups on/off via Streamlit buttons
    • Zoom / pan enabled natively
    • Returns (fig, correlation_all, per_group_stats, overall_corr)
    """
 
    plot_df = df[['weekly_study_hours', 'cgpa']].dropna().copy()
    np.random.seed(42)
    plot_df['cgpa_j'] = plot_df['cgpa'] + np.random.uniform(-0.07, 0.07, size=len(plot_df))
 
    overall_corr = plot_df['weekly_study_hours'].corr(plot_df['cgpa'])
 
    # ── Per-group stats ──────────────────────────────────────────────────────
    group_stats = {}
    for gname, gcfg in CGPA_GROUPS.items():
        mask = gcfg['filter'](plot_df)
        sub = plot_df[mask]
        if len(sub) == 0:
            continue
        group_stats[gname] = {
            'n':      len(sub),
            'mean':   sub['weekly_study_hours'].mean(),
            'median': sub['weekly_study_hours'].median(),
            'std':    sub['weekly_study_hours'].std(),
            'min':    sub['weekly_study_hours'].min(),
            'max':    sub['weekly_study_hours'].max(),
            'corr':   sub['weekly_study_hours'].corr(sub['cgpa']) if len(sub) > 2 else float('nan'),
            'color':  gcfg['color'],
            'emoji':  gcfg['emoji'],
            'label':  gcfg['label'],
            'range':  gcfg['range'],
        }
 
    # ── Session-state for active groups ─────────────────────────────────────
    if 'scatter_active_groups' not in st.session_state:
        st.session_state['scatter_active_groups'] = list(CGPA_GROUPS.keys())
 
    # ── Toggle buttons ───────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="margin-bottom:0.6rem;">
            <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase;
                         letter-spacing:0.08em; color:#9CA3AF;">
                Filter by CGPA Group — click to toggle
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
    btn_cols = st.columns(4)
    for i, (gname, gcfg) in enumerate(CGPA_GROUPS.items()):
        with btn_cols[i]:
            is_active = gname in st.session_state['scatter_active_groups']
            n_label   = group_stats.get(gname, {}).get('n', 0)
            btn_style = (
                f"background:{gcfg['color']}; color:white; border:none;"
                if is_active else
                f"background:white; color:{gcfg['color']}; "
                f"border:2px solid {gcfg['color']};"
            )
            # Render a styled button via HTML label + Streamlit button trick
            st.markdown(
                f"""
                <div style="
                    {btn_style}
                    border-radius:9999px; padding:0.45rem 0.5rem;
                    text-align:center; font-size:0.78rem; font-weight:700;
                    cursor:pointer; margin-bottom:0.3rem;
                    box-shadow: {'0 3px 10px rgba(0,0,0,0.15)' if is_active else 'none'};
                    transition: all 0.2s;
                ">
                    {gcfg['emoji']} {gcfg['label']}<br>
                    <span style="font-size:0.68rem; opacity:0.85;">{gcfg['range']} · {n_label} students</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                f"{'✓ ' if is_active else ''}{gcfg['label']}",
                key=f"toggle_{i}",
                use_container_width=True,
                help=f"{'Hide' if is_active else 'Show'} {gcfg['label']} group",
            ):
                if is_active:
                    if len(st.session_state['scatter_active_groups']) > 1:  # keep at least 1
                        st.session_state['scatter_active_groups'].remove(gname)
                else:
                    st.session_state['scatter_active_groups'].append(gname)
                st.rerun()
 
    active_groups = st.session_state['scatter_active_groups']
 
    # ── Build figure ─────────────────────────────────────────────────────────
    fig = go.Figure()
 
    # Scatter traces – one per active group
    for gname, gcfg in CGPA_GROUPS.items():
        if gname not in active_groups:
            continue
        mask = gcfg['filter'](plot_df)
        sub  = plot_df[mask]
        if len(sub) == 0:
            continue
        gstats = group_stats.get(gname, {})
 
        hover = [
            f"<b>{gcfg['emoji']} {gcfg['label']} Group</b><br>"
            f"CGPA: <b>{row['cgpa']:.2f}</b><br>"
            f"Weekly Study Hours: <b>{row['weekly_study_hours']:.0f} hrs</b><br>"
            f"Daily Average: {row['weekly_study_hours']/7:.1f} hrs/day<br>"
            f"─────────────────<br>"
            f"Group Mean: {gstats.get('mean',0):.0f} hrs | "
            f"Range: {gstats.get('min',0):.0f}–{gstats.get('max',0):.0f} hrs"
            for _, row in sub.iterrows()
        ]
 
        fig.add_trace(go.Scatter(
            x=sub['weekly_study_hours'],
            y=sub['cgpa_j'],
            mode='markers',
            name=f"{gcfg['emoji']} {gcfg['label']} (n={len(sub)})",
            marker=dict(
                size=11,
                color=gcfg['color'],
                opacity=0.68,
                line=dict(width=1.2, color='white'),
                symbol='circle',
            ),
            text=hover,
            hoverinfo='text',
        ))
 
    fig.update_layout(
        template="plotly_white",
        height=520,
        margin=dict(l=60, r=50, t=70, b=70),
        paper_bgcolor="rgba(255,255,255,0.97)",
        plot_bgcolor="rgba(255,255,255,0.97)",
        xaxis=dict(
            title="<b>Weekly Study Hours</b>",
            gridcolor='#EDE9E0',
            zeroline=False,
            range=[-1, 57],
            dtick=10,
            title_font=dict(size=13),
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            title="<b>CGPA</b>",
            gridcolor='#EDE9E0',
            zeroline=False,
            range=[0.8, 4.3],
            dtick=0.5,
            title_font=dict(size=13),
            tickfont=dict(size=11),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E8E6E0",
            borderwidth=1,
            font=dict(size=10.5),
            itemsizing='constant',
        ),
        hovermode='closest',
        dragmode='zoom',
        modebar=dict(
            orientation='v',
            bgcolor='rgba(255,255,255,0.8)',
        ),
    )
 
    return fig, overall_corr, group_stats, overall_corr
 


# ─────────────────────────────────────────────────────────────────────────────
# Per-group stat cards (shown below the chart)
# ─────────────────────────────────────────────────────────────────────────────

def _render_group_stat_cards(group_stats: dict, active_groups: list):
    """Four compact stat cards — one per active CGPA group."""

    cols = st.columns(len(active_groups)) if active_groups else []

    for i, gname in enumerate(g for g in CGPA_GROUPS if g in active_groups):
        gs = group_stats.get(gname)
        if gs is None:
            continue
        corr_str = f"{gs['corr']:.2f}" if not np.isnan(gs['corr']) else "n/a"
        corr_color = (
            '#DC2626' if abs(gs['corr']) < 0.15 else
            '#F59E0B' if abs(gs['corr']) < 0.30 else
            '#10B981'
        ) if not np.isnan(gs['corr']) else '#9CA3AF'



# ─────────────────────────────────────────────────────────────────────────────
# Legacy stubs – kept so any external call sites don't crash
# ─────────────────────────────────────────────────────────────────────────────

def cgpa_vs_study_hours_scatter(df):
    """Compatibility shim – delegates to cgpa_vs_study_hours_interactive."""
    fig, corr, _, _ = cgpa_vs_study_hours_interactive(df)
    return fig, corr


def cgpa_vs_study_hours_zoomed(df, target_cgpa=3.5):
    """Compatibility shim – returns None so caller skips the old zoomed section."""
    return None, 0, 0, 0, 0, 0, 0


# ─────────────────────────────────────────────────────────────────────────────
# Main page
# ─────────────────────────────────────────────────────────────────────────────

def show_core_analysis():
    load_css()
    df = load_data()

    if 'course' not in df.columns:
        courses = ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Economics']
        df['course'] = np.random.choice(courses, size=len(df))

    # Display both cards side by side and centered
    col1, col2 = st.columns([1, 1])  # Creates empty space on sides

    with col1:
        metric_card_total_students(df)
    with col2:
        metric_card_avg_cgpa(df)

    col1, col2 = st.columns([1, 1])

    with col1:
            st.markdown(
                """
                <style>
                div[data-testid="column"]:nth-of-type(1) button {
                    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
                    border: none;
                    border-radius: 9999px;
                    padding: 0.6rem 1rem;
                    font-weight: 600;
                    font-size: 0.85rem;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 8px rgba(46,173,138,0.25);
                }
                div[data-testid="column"]:nth-of-type(1) button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(46,173,138,0.35);
                    background: linear-gradient(135deg, #1E7B5F 0%, #166B52 100%);
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            if st.button("👥 View Student Details", key="btn_student_details", use_container_width=True):
                _open_student_details_dialog(df)
        
    with col2:
                st.markdown(
                    """
                    <style>
                    div[data-testid="column"]:nth-of-type(2) button {
                        background: linear-gradient(135deg, #E8A020 0%, #C97E0A 100%);
                        border: none;
                        border-radius: 9999px;
                        padding: 0.6rem 1rem;
                        font-weight: 600;
                        font-size: 0.85rem;
                        transition: all 0.3s ease;
                        box-shadow: 0 2px 8px rgba(232,160,32,0.25);
                    }
                    div[data-testid="column"]:nth-of-type(2) button:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 4px 12px rgba(232,160,32,0.35);
                        background: linear-gradient(135deg, #C97E0A 0%, #B06B07 100%);
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("📊 View CGPA Details", key="btn_cgpa_details", use_container_width=True):
                    _open_cgpa_details_dialog(df)

    # Page header
    st.markdown(
        """
        <div style="text-align: center; padding-top: 1rem; padding-bottom: 2rem;">
            <div style="
                display: inline-block;
                padding: 0.25rem 1rem;
                background: rgba(123, 104, 200, 0.15);
                color: #7B68C8;
                font-size: 0.8rem;
                font-weight: 600;
                border-radius: 9999px;
                margin-bottom: 1rem;
            ">
                Core Analysis
            </div>
            <h1 style="font-size: 2.5rem; font-weight: 800; color: #111827; margin-bottom: 0.75rem;">
                The Myth: Study Longer = Better Results
            </h1>
            <p style="font-size: 1.1rem; color: #6b7280; max-width: 60rem; margin: 0 auto;">
                We begin by examining the most common assumption that studying longer 
                leads to higher academic performance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Scatter header ────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(123,104,200,0.07) 0%, rgba(74,127,191,0.07) 100%);
            border: 1.5px solid rgba(123,104,200,0.2);
            border-radius: 18px;
            padding: 1.2rem 1.8rem;
            margin-bottom: 1.4rem;
            display: flex;
            align-items: center;
            gap: 1.1rem;
        ">
            <div style="
                flex-shrink: 0;
                width: 44px; height: 44px;
                background: linear-gradient(135deg, #7B68C8, #4A7FBF);
                border-radius: 12px;
                display: flex; align-items: center; justify-content: center;
                font-size: 1.3rem;
            ">📊</div>
            <div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #111827; line-height: 1.2; margin-bottom: 0.25rem;">
                    Study Hours vs CGPA
                </div>
                <div style="font-size: 0.86rem; color: #6b7280; line-height: 1.5;">
                    Each dot is a student.&nbsp;
                    <strong style="color: #4A7FBF;">Select CGPA groups</strong> to compare,
                    zoom &amp; pan the chart to dig deeper.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Interactive chart ─────────────────────────────────────────────────────
    fig, correlation, group_stats, visible_corr = cgpa_vs_study_hours_interactive(df)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            'displayModeBar': True,
            'responsive': True,
            'modeBarButtonsToAdd': ['select2d', 'lasso2d'],
            'modeBarButtonsToRemove': ['toImage'],
            'scrollZoom': True,
        },
    )

    # Stat row below chart
    col_left, col_right = st.columns(2)
    with col_left:
        r2 = visible_corr ** 2
        st.markdown(
            f"""
            <div style="font-size: 0.84rem; color: #6b7280; padding-left: 0.2rem;">
                <strong>Overall r&nbsp;=&nbsp;{correlation:.2f}</strong> &nbsp;|&nbsp;
                Visible r&nbsp;=&nbsp;{visible_corr:.2f} &nbsp;|&nbsp;
                R²&nbsp;=&nbsp;{r2:.3f}&nbsp;({r2*100:.1f}% variance explained)
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_right:
        badge_color = (
            "#DC2626" if abs(visible_corr) < 0.15 else
            "#F97316" if abs(visible_corr) < 0.30 else
            "#F59E0B" if abs(visible_corr) < 0.50 else "#10B981"
        )
        badge_text = (
            "🔴 Very Weak Correlation" if abs(visible_corr) < 0.15 else
            "🟠 Weak Correlation"      if abs(visible_corr) < 0.30 else
            "🟡 Moderate Correlation"  if abs(visible_corr) < 0.50 else
            "🟢 Strong Correlation"
        )
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end;">
                <span style="display: inline-block; padding: 0.35rem 1rem;
                             background: {badge_color}18; color: {badge_color};
                             font-size: 0.8rem; font-weight: 700;
                             border-radius: 9999px; border: 1px solid {badge_color}44;">
                    {badge_text}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Per-group stat cards ──────────────────────────────────────────────────
    active_groups = st.session_state.get('scatter_active_groups', list(CGPA_GROUPS.keys()))
    _render_group_stat_cards(group_stats, active_groups)

    # ── "So what?" callout banner ─────────────────────────────────────────────
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # Build a mini data-point: widest hours range among active groups
    ranges = [
        (gs['max'] - gs['min'], gs['label'], gs['min'], gs['max'])
        for gn, gs in group_stats.items() if gn in active_groups
    ]
    widest = max(ranges, key=lambda x: x[0]) if ranges else (0, '?', 0, 0)

    # Insight Callout
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(239,68,68,0.08) 0%, rgba(249,115,22,0.08) 100%);
            border-left: 4px solid #EF4444;
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            margin: 2rem auto;
            max-width: 48rem;
        ">
            <p style="font-size: 1.5rem; font-weight: 800; color: #111827; margin-bottom: 0.75rem;">
                The Data Speaks: Study Duration ≠ Better Grades
            </p>
            <p style="font-size: 1rem; color: #374151; margin-bottom: 0.75rem;">
                The scatter plot shows no clear pattern. Students with higher CGPA are not consistently studying more, and the points are widely spread.
                Even within the “Good” group(3.00-3.99), study time ranges from 1 to 38 hours, yet the CGPA remains the same.
                With a correlation of just 0.13, the message is clear: <br><span style="font-weight: 700; color: #DC2626;">more study hours do not guarantee better grades.</span> 
            </p>
            <p style="font-size: 0.9rem; color: #6b7280;">
                This raises an important question...
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            background: white;
            border-radius: 24px;
            border: 2px solid rgba(123,104,200,0.3);
            padding: 2rem;
            text-align: center;
            margin: 0 auto 2rem auto;
            max-width: 48rem;
        ">
            <div style="
                display: inline-block;
                padding: 0.75rem;
                background: linear-gradient(135deg, rgba(123,104,200,0.2) 0%, rgba(236,72,153,0.15) 100%);
                border-radius: 9999px;
                margin-bottom: 1rem;
            ">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#7B68C8" stroke-width="1.5">
                    <path d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
            <h2 style="font-size: 1.75rem; font-weight: 800; color: #111827; margin-bottom: 0.75rem;">
                What Other Factors Can Contribute to Academic Performance?
            </h2>
            <p style="font-size: 1rem; color: #6b7280; margin-bottom: 1.5rem;">
                Let's explore a comprehensive analysis of behavioral patterns, study methods, 
                and lifestyle choices across 6 key dimensions.
            </p>
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; color: #7B68C8;">
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                    Dive into the insights
                </span>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                     style="animation: bounce 1s infinite;">
                    <path d="M12 5v14M19 12l-7 7-7-7" />
                </svg>
            </div>
        </div>

        <style>
            @keyframes bounce {
                0%, 100% {{ transform: translateY(0); }}
                50%        {{ transform: translateY(5px); }}
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Center using empty columns (3-column layout with empty side columns)
    left_empty, center_col, right_empty = st.columns([1, 2, 1])

    with center_col:
        # Hidden button for navigation trigger
        if st.button(":material/analytics: Go to Behavioral Insights", key="hidden_nav_btn", 
                    type="primary", use_container_width=True, help="Navigate to detailed analysis"):
            st.switch_page("pages/2_behavioral_insights.py")
if __name__ == "__main__":
    show_core_analysis()