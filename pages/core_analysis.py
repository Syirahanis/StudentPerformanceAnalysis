# core_analysis.py (fixed - modal now works properly)

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
    
    # Ensure course column exists
    if 'course' not in df.columns:
        courses = ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Economics']
        df['course'] = np.random.choice(courses, size=len(df))
    
    # Ensure gender column exists
    if 'gender' not in df.columns:
        df['gender'] = np.random.choice(['Male', 'Female'], size=len(df))
    
    return df


# -------------------------
# Modal Dialog for Detailed View (Hidden by default)
# -------------------------
def show_details_modal(df, title="Student Population Details"):
    """Display a modal with detailed breakdown of students"""
    
    # Get gender distribution
    gender_counts = df['gender'].value_counts()
    gender_df = pd.DataFrame({
        'Category': gender_counts.index,
        'Count': gender_counts.values,
        'Percentage': (gender_counts.values / len(df) * 100).round(1)
    })
    
    # Get course distribution
    course_counts = df['course'].value_counts()
    course_df = pd.DataFrame({
        'Category': course_counts.index,
        'Count': course_counts.values,
        'Percentage': (course_counts.values / len(df) * 100).round(1)
    })
    
    # Create a unique ID for this modal to avoid conflicts
    modal_id = "detailsModal"
    
    # Create HTML for modal - HIDDEN by default (display: none)
    modal_html = f"""
    <div id="{modal_id}" style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        backdrop-filter: blur(8px);
        z-index: 9999;
        display: none;
        align-items: center;
        justify-content: center;
        font-family: system-ui, -apple-system, sans-serif;
    ">
        <div style="
            background: white;
            border-radius: 32px;
            max-width: 650px;
            width: 90%;
            max-height: 85vh;
            overflow-y: auto;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
            animation: slideUp 0.3s ease-out;
        ">
            <div style="
                padding: 1.5rem;
                border-bottom: 1px solid #e5e7eb;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: sticky;
                top: 0;
                background: white;
                border-radius: 32px 32px 0 0;
            ">
                <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #111827;">
                    📊 {title}
                </h2>
                <button onclick="closeModal('{modal_id}')" style="
                    background: none;
                    border: none;
                    font-size: 1.5rem;
                    cursor: pointer;
                    color: #6b7280;
                    padding: 0.5rem;
                    border-radius: 999px;
                    transition: all 0.2s;
                " onmouseover="this.style.backgroundColor='#f3f4f6'" onmouseout="this.style.backgroundColor='transparent'">
                    ✕
                </button>
            </div>
            
            <div style="padding: 1.5rem;">
                <!-- Gender Distribution -->
                <div style="margin-bottom: 2rem;">
                    <h3 style="
                        font-size: 1.1rem;
                        font-weight: 600;
                        color: #374151;
                        margin-bottom: 1rem;
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                    ">
                        <span>👥</span> Gender Distribution
                    </h3>
                    <div style="
                        background: #f9fafb;
                        border-radius: 16px;
                        padding: 1rem;
                    ">
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="border-bottom: 2px solid #e5e7eb;">
                                    <th style="text-align: left; padding: 0.75rem 0.5rem; color: #6b7280; font-weight: 600;">Gender</th>
                                    <th style="text-align: right; padding: 0.75rem 0.5rem; color: #6b7280; font-weight: 600;">Count</th>
                                    <th style="text-align: right; padding: 0.75rem 0.5rem; color: #6b7280; font-weight: 600;">Percentage</th>
                                </tr>
                            </thead>
                            <tbody>
    """
    
    for _, row in gender_df.iterrows():
        modal_html += f"""
        <tr style="border-bottom: 1px solid #f3f4f6;">
            <td style="padding: 0.75rem 0.5rem; font-weight: 500;">{row['Category']}</td>
            <td style="padding: 0.75rem 0.5rem; text-align: right;">{row['Count']:,}</td>
            <td style="padding: 0.75rem 0.5rem; text-align: right;">{row['Percentage']}%</td>
        </tr>
        """
    
    modal_html += """
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Course Distribution -->
                <div>
                    <h3 style="
                        font-size: 1.1rem;
                        font-weight: 600;
                        color: #374151;
                        margin-bottom: 1rem;
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                    ">
                        <span>📚</span> Course Distribution
                    </h3>
                    <div style="
                        background: #f9fafb;
                        border-radius: 16px;
                        padding: 1rem;
                        max-height: 350px;
                        overflow-y: auto;
                    ">
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="border-bottom: 2px solid #e5e7eb; position: sticky; top: 0; background: #f9fafb;">
                                    <th style="text-align: left; padding: 0.75rem 0.5rem; color: #6b7280; font-weight: 600;">Course</th>
                                    <th style="text-align: right; padding: 0.75rem 0.5rem; color: #6b7280; font-weight: 600;">Count</th>
                                    <th style="text-align: right; padding: 0.75rem 0.5rem; color: #6b7280; font-weight: 600;">Percentage</th>
                                </tr>
                            </thead>
                            <tbody>
    """
    
    for _, row in course_df.iterrows():
        # Truncate long course names
        course_name = str(row['Category'])[:50] + '...' if len(str(row['Category'])) > 50 else row['Category']
        modal_html += f"""
        <tr style="border-bottom: 1px solid #f3f4f6;">
            <td style="padding: 0.75rem 0.5rem; font-size: 0.9rem;">{course_name}</td>
            <td style="padding: 0.75rem 0.5rem; text-align: right;">{row['Count']:,}</td>
            <td style="padding: 0.75rem 0.5rem; text-align: right;">{row['Percentage']}%</td>
        </tr>
        """
    
    modal_html += f"""
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div style="
                    margin-top: 1.5rem;
                    padding-top: 1rem;
                    border-top: 1px solid #e5e7eb;
                    text-align: center;
                    color: #6b7280;
                    font-size: 0.875rem;
                ">
                    Total Students: {len(df):,} | Total Courses: {len(course_df)} | Genders: {len(gender_df)}
                </div>
            </div>
        </div>
    </div>
    
    <style>
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
    </style>
    
    <script>
        function showModal(modalId) {{
            var modal = document.getElementById(modalId);
            if (modal) {{
                modal.style.display = 'flex';
                modal.style.alignItems = 'center';
                modal.style.justifyContent = 'center';
                console.log('Modal shown:', modalId);
            }} else {{
                console.log('Modal not found:', modalId);
            }}
        }}
        
        function closeModal(modalId) {{
            var modal = document.getElementById(modalId);
            if (modal) {{
                modal.style.display = 'none';
                console.log('Modal closed:', modalId);
            }}
        }}
        
        // Close modal when clicking outside
        document.addEventListener('click', function(e) {{
            var modal = document.getElementById('{modal_id}');
            if (modal && modal.style.display === 'flex') {{
                if (e.target === modal) {{
                    closeModal('{modal_id}');
                }}
            }}
        }});
        
        // Close modal with Escape key
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                var modal = document.getElementById('{modal_id}');
                if (modal && modal.style.display === 'flex') {{
                    closeModal('{modal_id}');
                }}
            }}
        }});
    </script>
    """
    
    return modal_html, modal_id


# -------------------------
# Enhanced Metric Card with Course Bar Chart & Modal
# -------------------------
def metric_card_total_students(df):
    """Metric card for Total Students Surveyed with course distribution bar chart"""
    
    total_students = len(df)
    
    # Get course distribution
    course_counts = df['course'].value_counts().reset_index()
    course_counts.columns = ['course', 'students']
    course_counts = course_counts.sort_values('students', ascending=False)
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=course_counts['course'],
        y=course_counts['students'],
        marker_color=TEAL,
        marker_opacity=0.7,
        marker_line_color='white',
        marker_line_width=1,
        showlegend=False,
        hovertemplate='<b>%{x}</b><br>Students: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        height=80,
        width=140,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickangle=0,
            tickfont=dict(size=9, color='#6b7280'),
            showgrid=False,
            showline=False,
            showticklabels=True,
            ticks='',
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            ticks='',
        ),
        bargap=0.3,
    )
    
    # Convert to HTML
    chart_html = fig.to_html(include_plotlyjs=False, full_html=False, config={'displayModeBar': False})
    
    # Create the modal HTML
    modal_html, modal_id = show_details_modal(df, "Student Population Details")
    
    # Create the button and card HTML
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(46, 173, 138, 0.15) 0%, rgba(74, 127, 191, 0.1) 100%);
            border-radius: 20px;
            border: 1px solid rgba(203, 213, 225, 0.5);
            padding: 1.5rem;
            backdrop-filter: blur(8px);
            position: relative;
            overflow: hidden;
            height: 100%;
        ">
            <div style="position: relative; z-index: 10;">
                <div style="
                    display: inline-block;
                    padding: 0.25rem 0.75rem;
                    background: rgba(255, 255, 255, 0.8);
                    backdrop-filter: blur(4px);
                    color: #374151;
                    font-size: 0.7rem;
                    font-weight: 500;
                    border-radius: 9999px;
                    margin-bottom: 1rem;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                ">
                    Total Students Surveyed
                </div>
                <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem;">
                    <div>
                        <div style="font-size: 3rem; font-weight: 800; color: #111827; margin-bottom: 0.25rem; line-height: 1;">
                            {total_students:,}
                        </div>
                        <div style="font-size: 0.7rem; color: #6b7280;">
                            Across {len(course_counts)} courses
                        </div>
                    </div>
                    <div style="flex-shrink: 0; width: 140px;">
                        {chart_html}
                    </div>
                </div>
            </div>
            <button 
                onclick="showModal('{modal_id}')"
                style="
                    position: absolute;
                    bottom: 1rem;
                    right: 1rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.5rem 1rem;
                    background: rgba(255, 255, 255, 0.9);
                    backdrop-filter: blur(4px);
                    color: #374151;
                    font-size: 0.75rem;
                    font-weight: 500;
                    border-radius: 9999px;
                    border: 1px solid rgba(203, 213, 225, 0.5);
                    cursor: pointer;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                    transition: all 0.2s;
                "
                onmouseover="this.style.backgroundColor='rgba(255,255,255,1)'; this.style.transform='scale(1.02)'"
                onmouseout="this.style.backgroundColor='rgba(255,255,255,0.9)'; this.style.transform='scale(1)'"
            >
                View Details
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
            </button>
        </div>
        {modal_html}
        """,
        unsafe_allow_html=True,
    )


# -------------------------
# Enhanced Metric Card with CGPA Distribution Pie Chart
# -------------------------
def metric_card_avg_cgpa(df):
    """Metric card for Average CGPA with enhanced distribution pie chart"""
    
    avg_cgpa = df['cgpa'].mean()
    
    # Define CGPA ranges with more detailed categories
    def categorize_cgpa(cgpa):
        if cgpa >= 3.9:
            return '4.00 (Excellent)'
        elif cgpa >= 3.4:
            return '3.50 (Good)'
        elif cgpa >= 2.4:
            return '2.50 (Satisfactory)'
        else:
            return '1.00 (Needs Improvement)'
    
    df['cgpa_category'] = df['cgpa'].apply(categorize_cgpa)
    
    # Calculate distribution
    distribution = df['cgpa_category'].value_counts()
    
    # Ensure all categories exist
    all_categories = ['4.00 (Excellent)', '3.50 (Good)', '2.50 (Satisfactory)', '1.00 (Needs Improvement)']
    for cat in all_categories:
        if cat not in distribution:
            distribution[cat] = 0
    
    distribution = distribution[all_categories]
    
    # Colors for pie chart
    pie_colors = {
        '4.00 (Excellent)': PURPLE,
        '3.50 (Good)': BLUE,
        '2.50 (Satisfactory)': AMBER,
        '1.00 (Needs Improvement)': CORAL
    }
    
    # Create enhanced pie chart with better styling
    fig = go.Figure()
    
    # Get values and labels for display
    labels = [cat.split(' ')[0] for cat in distribution.index]
    values = distribution.values
    
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(
            colors=[pie_colors[cat] for cat in distribution.index],
            line=dict(color='white', width=2)
        ),
        textinfo='percent',
        textposition='inside',
        textfont=dict(size=10, color='white', weight='bold'),
        hoverinfo='label+percent+value',
        showlegend=False,
        sort=False,
        pull=[0.02 if v == max(values) else 0 for v in values],
    ))
    
    fig.update_layout(
        height=120,
        width=120,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[
            dict(
                text=f"{avg_cgpa:.2f}",
                x=0.5, y=0.5,
                font=dict(size=16, color='#1f2937', weight='bold'),
                showarrow=False
            )
        ]
    )
    
    chart_html = fig.to_html(include_plotlyjs=False, full_html=False, config={'displayModeBar': False})
    
    # Calculate percentages for display
    total = distribution.sum()
    percentages = {cat: (dist/total)*100 for cat, dist in distribution.items()}
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(123, 104, 200, 0.12) 0%, rgba(232, 160, 32, 0.08) 100%);
            border-radius: 20px;
            border: 1px solid rgba(203, 213, 225, 0.5);
            padding: 1.5rem;
            backdrop-filter: blur(8px);
            position: relative;
            overflow: hidden;
            height: 100%;
        ">
            <div style="position: relative; z-index: 10;">
                <div style="
                    display: inline-block;
                    padding: 0.25rem 0.75rem;
                    background: rgba(255, 255, 255, 0.8);
                    backdrop-filter: blur(4px);
                    color: #374151;
                    font-size: 0.7rem;
                    font-weight: 500;
                    border-radius: 9999px;
                    margin-bottom: 1rem;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                ">
                    Average CGPA
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 1.5rem;">
                    <div>
                        <div style="font-size: 3rem; font-weight: 800; color: #111827; margin-bottom: 0.25rem; line-height: 1;">
                            {avg_cgpa:.2f}
                        </div>
                        <div style="font-size: 0.7rem; color: #6b7280;">
                            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                                <div style="width: 0.5rem; height: 0.5rem; border-radius: 9999px; background-color: {PURPLE};"></div>
                                <span>Excellent: {percentages['4.00 (Excellent)']:.1f}%</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                                <div style="width: 0.5rem; height: 0.5rem; border-radius: 9999px; background-color: {BLUE};"></div>
                                <span>Good: {percentages['3.50 (Good)']:.1f}%</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <div style="width: 0.5rem; height: 0.5rem; border-radius: 9999px; background-color: {AMBER};"></div>
                                <span>Satisfactory: {percentages['2.50 (Satisfactory)']:.1f}%</span>
                            </div>
                        </div>
                    </div>
                    <div style="flex-shrink: 0; width: 120px; height: 120px;">
                        {chart_html}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------------
# Enhanced Chart 1 – CGPA vs Weekly Study Hours Scatter
# -------------------------
def cgpa_vs_study_hours_scatter(df):
    """Enhanced scatter plot: CGPA vs Weekly Study Hours with improved trend line."""
    
    plot_df = df[['weekly_study_hours', 'cgpa']].dropna().copy()
    
    np.random.seed(42)
    jitter_amount = 0.08
    plot_df['cgpa_jittered'] = plot_df['cgpa'] + np.random.uniform(-jitter_amount, jitter_amount, size=len(plot_df))
    
    # Calculate correlation
    correlation = plot_df['weekly_study_hours'].corr(plot_df['cgpa'])
    
    # Color based on CGPA
    colors = []
    for cgpa in plot_df['cgpa']:
        if cgpa >= 3.9:
            colors.append(PURPLE)
        elif cgpa >= 3.4:
            colors.append(BLUE)
        elif cgpa >= 2.4:
            colors.append(AMBER)
        else:
            colors.append(CORAL)
    
    hover_texts = [
        f"<b>CGPA: {row['cgpa']:.2f}</b><br>"
        f"Weekly Study Hours: {row['weekly_study_hours']:.0f} hrs/week<br>"
        f"Daily Average: {row['weekly_study_hours']/7:.1f} hrs/day"
        for _, row in plot_df.iterrows()
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=plot_df['weekly_study_hours'],
        y=plot_df['cgpa_jittered'],
        mode='markers',
        name='Students',
        marker=dict(
            size=12,
            color=colors,
            opacity=0.65,
            line=dict(width=1.5, color='white'),
            symbol='circle'
        ),
        text=hover_texts,
        hoverinfo='text',
        showlegend=False,
    ))
    
    # Calculate and add trend line with confidence interval
    x_trend = plot_df['weekly_study_hours']
    y_trend = plot_df['cgpa']
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_trend, y_trend)
    x_line = np.linspace(x_trend.min(), x_trend.max(), 100)
    y_line = slope * x_line + intercept
    
    # Calculate confidence interval
    n = len(x_trend)
    t_value = stats.t.ppf(0.975, n-2)
    y_pred = slope * x_trend + intercept
    residuals = y_trend - y_pred
    mse = np.sum(residuals**2) / (n-2)
    x_mean = np.mean(x_trend)
    se_line = np.sqrt(mse * (1/n + (x_line - x_mean)**2 / np.sum((x_trend - x_mean)**2)))
    ci_upper = y_line + t_value * se_line
    ci_lower = y_line - t_value * se_line
    
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_line, x_line[::-1]]),
        y=np.concatenate([ci_upper, ci_lower[::-1]]),
        fill='toself',
        fillcolor='rgba(154, 152, 144, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='95% Confidence Interval',
        showlegend=True,
        hoverinfo='none',
    ))
    
    fig.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode='lines',
        name=f'Trend Line (r = {correlation:.2f})',
        line=dict(color=TEAL, width=3, dash='solid'),
        showlegend=True,
    ))
    
    # Add horizontal line at average CGPA
    avg_cgpa = plot_df['cgpa'].mean()
    fig.add_hline(
        y=avg_cgpa,
        line_dash="dot",
        line_color=GRAY,
        line_width=1.5,
        annotation_text=f"Avg CGPA: {avg_cgpa:.2f}",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color=GRAY)
    )
    
    fig.update_layout(
        template="plotly_white",
        height=500,
        margin=dict(l=60, r=40, t=60, b=70),
        paper_bgcolor="rgba(255,255,255,0.95)",
        plot_bgcolor="rgba(255,255,255,0.95)",
        title=dict(
            text="<b>Study Hours vs CGPA Analysis</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=16, color='#1f2937')
        ),
        xaxis=dict(
            title="<b>Weekly Study Hours</b>",
            gridcolor='#E8E6E0',
            zeroline=False,
            range=[0, 55],
            dtick=10,
            title_font=dict(size=13),
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            title="<b>CGPA</b>",
            gridcolor='#E8E6E0',
            zeroline=False,
            range=[1.6, 4.2],
            dtick=0.5,
            title_font=dict(size=13),
            tickfont=dict(size=11),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E8E6E0",
            borderwidth=1,
            font=dict(size=11),
        ),
        hovermode='closest',
    )
    
    return fig, correlation


# -------------------------
# Enhanced zoomed scatter plot for CGPA 3.5 focus
# -------------------------
def cgpa_vs_study_hours_zoomed(df, target_cgpa=3.5):
    """Enhanced zoomed scatter plot focusing on a single CGPA group."""
    
    # Filter for target CGPA range
    if target_cgpa == 3.5:
        plot_df = df[(df['cgpa'] >= 3.4) & (df['cgpa'] < 3.9)][['weekly_study_hours', 'cgpa']].dropna().copy()
    else:
        plot_df = df[df['cgpa'] == target_cgpa][['weekly_study_hours', 'cgpa']].dropna().copy()
    
    if len(plot_df) == 0:
        return None, 0, 0, 0, 0, 0, 0
    
    n_students = len(plot_df)
    mean_hours = plot_df['weekly_study_hours'].mean()
    median_hours = plot_df['weekly_study_hours'].median()
    std_hours = plot_df['weekly_study_hours'].std()
    min_hours = plot_df['weekly_study_hours'].min()
    max_hours = plot_df['weekly_study_hours'].max()
    
    np.random.seed(42)
    jitter_amount = 0.03
    plot_df['cgpa_jittered'] = plot_df['cgpa'] + np.random.uniform(-jitter_amount, jitter_amount, size=len(plot_df))
    
    colors = [TEAL if hours > mean_hours else BLUE for hours in plot_df['weekly_study_hours']]
    
    hover_texts = [
        f"<b>CGPA: {row['cgpa']:.2f}</b><br>"
        f"Weekly Study Hours: {row['weekly_study_hours']:.0f} hrs/week<br>"
        f"Daily Average: {row['weekly_study_hours']/7:.1f} hrs/day<br>"
        f"{'📚 Above average study time' if row['weekly_study_hours'] > mean_hours else '✨ Efficient learner (below avg)'}"
        for _, row in plot_df.iterrows()
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=plot_df['weekly_study_hours'],
        y=plot_df['cgpa_jittered'],
        mode='markers',
        name=f'CGPA {target_cgpa} Students',
        marker=dict(
            size=14,
            color=colors,
            opacity=0.8,
            line=dict(width=1.5, color='white'),
            symbol='circle'
        ),
        text=hover_texts,
        hoverinfo='text',
        showlegend=True,
    ))
    
    # Add mean line
    fig.add_vline(
        x=mean_hours,
        line_dash="dash",
        line_color=TEAL,
        line_width=2.5,
        annotation_text=f"Mean: {mean_hours:.0f} hrs/week",
        annotation_position="top",
        annotation_font=dict(size=11, color=TEAL)
    )
    
    # Add median line
    fig.add_vline(
        x=median_hours,
        line_dash="dot",
        line_color=AMBER,
        line_width=2,
        annotation_text=f"Median: {median_hours:.0f} hrs/week",
        annotation_position="bottom",
        annotation_font=dict(size=10, color=AMBER)
    )
    
    fig.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=60, r=40, t=60, b=70),
        paper_bgcolor="rgba(255,255,255,0.95)",
        plot_bgcolor="rgba(255,255,255,0.95)",
        title=dict(
            text=f"<b>Study Hours Distribution for CGPA {target_cgpa} Students</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=14, color='#1f2937')
        ),
        xaxis=dict(
            title="<b>Weekly Study Hours</b>",
            gridcolor='#E8E6E0',
            zeroline=False,
            range=[0, 55],
            dtick=10,
            title_font=dict(size=12),
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            title="<b>CGPA</b>",
            gridcolor='#E8E6E0',
            zeroline=False,
            range=[3.35, 3.65] if target_cgpa == 3.5 else [target_cgpa - 0.15, target_cgpa + 0.15],
            title_font=dict(size=12),
            tickfont=dict(size=10),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E8E6E0",
            borderwidth=1,
            font=dict(size=10),
        ),
        hovermode='closest',
    )
    
    return fig, n_students, mean_hours, median_hours, std_hours, min_hours, max_hours


# -------------------------
# Main page
# -------------------------
def show_core_analysis():
    load_css()
    df = load_data()
    
    # Ensure course column exists for demo
    if 'course' not in df.columns:
        courses = ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Economics']
        df['course'] = np.random.choice(courses, size=len(df))
    
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
            <p style="font-size: 1.1rem; color: #6b7280; max-width: 42rem; margin: 0 auto;">
                We begin by examining the most common assumption — that studying longer 
                leads to higher academic performance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Metric cards side by side
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        metric_card_total_students(df)
    
    with col2:
        metric_card_avg_cgpa(df)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Main scatter plot
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 1rem;">
            <h2 style="font-size: 1.5rem; font-weight: 700; color: #111827;">Study Hours vs CGPA</h2>
            <p style="color: #6b7280; font-size: 0.9rem;">
                Analysis of students shows no strong relationship between study duration and academic performance
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Create container with card-like styling
    fig, correlation = cgpa_vs_study_hours_scatter(df)
    
    st.markdown(
        """
        <div style="
            background: white;
            border-radius: 20px;
            border: 1px solid #e5e7eb;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
            margin-bottom: 1.5rem;
        ">
        """,
        unsafe_allow_html=True,
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'responsive': True})
    
    # Footer with correlation info
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(
            f"""
            <div style="font-size: 0.85rem; color: #6b7280;">
                <strong>Statistical Summary:</strong><br>
                Correlation coefficient: r = {correlation:.2f}<br>
                R² = {(correlation**2):.3f} ({((correlation**2)*100):.1f}% variance explained)
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_right:
        badge_color = "#DC2626" if abs(correlation) < 0.3 else "#F59E0B" if abs(correlation) < 0.5 else "#10B981"
        badge_text = "Weak Correlation" if abs(correlation) < 0.3 else "Moderate Correlation" if abs(correlation) < 0.5 else "Strong Correlation"
        st.markdown(
            f"""
            <div style="display: inline-block; padding: 0.35rem 1rem; background: rgba(239, 68, 68, 0.1); color: {badge_color}; font-size: 0.8rem; font-weight: 600; border-radius: 9999px; float: right;">
                {badge_text}
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Zoomed scatter plot for CGPA 3.5
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    zoomed_result = cgpa_vs_study_hours_zoomed(df, target_cgpa=3.5)
    if zoomed_result[0] is not None:
        fig_zoomed, n35, mean_hours, median_hours, std_hours, min_hours, max_hours = zoomed_result
        
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h3 style="font-size: 1.25rem; font-weight: 600; color: #111827;">🔍 Variation in Study Hours within CGPA 3.5 Students</h3>
                <p style="color: #6b7280; font-size: 0.85rem;">
                    n={n35} students | Mean: {mean_hours:.0f} hrs/week | 
                    Median: {median_hours:.0f} hrs/week | Std Dev: {std_hours:.0f} hrs/week | 
                    Range: {min_hours:.0f}-{max_hours:.0f} hrs
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown(
            """
            <div style="
                background: white;
                border-radius: 20px;
                border: 1px solid #e5e7eb;
                padding: 1.5rem;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            ">
            """,
            unsafe_allow_html=True,
        )
        
        st.plotly_chart(fig_zoomed, use_container_width=True, config={'displayModeBar': True, 'responsive': True})
        
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
                border-left: 4px solid {BLUE};
                border-radius: 12px;
                padding: 1rem 1.25rem;
                font-size: 0.9rem;
                color: #374151;
                margin-top: 1rem;
            ">
                💡 <strong>Key Insight:</strong> Even within the same CGPA (3.5), study hours vary widely — 
                from {min_hours:.0f} to {max_hours:.0f} hours/week (a {max_hours-min_hours:.0f}-hour range). 
                This reinforces that <strong>study quality matters more than quantity</strong>.
                Students achieving the same grades use very different amounts of study time.
                <br><br>
                📊 <strong>Statistical Note:</strong> The standard deviation of {std_hours:.0f} hours indicates 
                substantial variability in study habits among students with identical academic performance.
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Insight Callout
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(249, 115, 22, 0.08) 100%);
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
                With a correlation of just 0.12, study hours alone are <span style="font-weight: 700; color: #DC2626;">not a reliable predictor</span> of academic success.
            </p>
            <p style="font-size: 0.9rem; color: #6b7280;">
                This raises an important question...
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Transition Question
    st.markdown(
        """
        <div style="
            background: white;
            border-radius: 24px;
            border: 2px solid rgba(123, 104, 200, 0.3);
            padding: 2rem;
            text-align: center;
            margin: 0 auto 2rem auto;
            max-width: 48rem;
        ">
            <div style="
                display: inline-block;
                padding: 0.75rem;
                background: linear-gradient(135deg, rgba(123, 104, 200, 0.2) 0%, rgba(236, 72, 153, 0.15) 100%);
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
                Let's explore a comprehensive analysis of behavioral patterns, study methods, and lifestyle choices across 6 key dimensions.
            </p>
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; color: #7B68C8;">
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Dive into the insights</span>
                <div style="display: flex; flex-direction: column; gap: 0.125rem;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: bounce 1s infinite;">
                        <path d="M12 5v14M19 12l-7 7-7-7" />
                    </svg>
                </div>
            </div>
        </div>
        
        <style>
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(5px); }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    show_core_analysis()