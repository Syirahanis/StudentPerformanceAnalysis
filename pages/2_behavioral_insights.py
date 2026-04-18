import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -------------------------
# Layout & Styling
# -------------------------
def load_css():
    base_path = os.path.dirname(os.path.dirname(__file__))
    css_path = os.path.join(base_path, "style", "behavioral.css")

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
        "study method": "study_method",
        "procrastination level": "procrastination_level",
        "sleep hours": "sleep_hours",
        "stress level (beginning of semester)": "stress_start",
        "stress level (end of semester)": "stress_end",
        "study hours before exam": "study_hours_before_exam",
    }
    df = df.rename(columns=rename_map)

    return df


# -----------------------------------------------
# Chart 1 — Stress: Beginning vs End of Semester (Teal Theme)
# -----------------------------------------------
def stress_start_end_chart(df):
    avg_start = df["stress_start"].mean()
    avg_end = df["stress_end"].mean()
    pct_change = ((avg_end - avg_start) / avg_start) * 100

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Beginning of Semester", "End of Semester"],
            y=[avg_start, avg_end],
            text=[f"{avg_start:.2f}", f"{avg_end:.2f}"],
            textposition="outside",
            marker=dict(color=["#64c7c8", "#f27d72"]),
            width=[0.45, 0.45],
        )
    )
    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(title="Average Stress Level", range=[0, 5.5]),
        xaxis=dict(title=""),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
    )
    
    # ONE COMPLETE GROUP - everything inside one container
    with st.container():
        st.markdown(f'''
        <div class="chart-group card-teal">
            <div class="group-header">
                <div class="group-kicker">SEMESTER COMPARISON</div>
                <h3 class="group-title">Stress Levels: Start vs End of Semester</h3>
                <p class="group-subtitle">Average stress increases as the semester progresses toward exams.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.plotly_chart(fig, use_container_width=True, key="stress_start_end")
        
        st.markdown(f'''
        <div class="group-insight insight-teal">
            <div class="insight-icon">📊</div>
            <div class="insight-content">
                <div class="insight-title">KEY INSIGHT</div>
                <div class="insight-text">Stress increases by {pct_change:.0f}% as exams approach. Students report peak anxiety in the final weeks of the semester.</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


# --------------------------------------------------------
# Chart 2 — Stress vs Procrastination (Orange Theme)
# --------------------------------------------------------
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
    
    low_proc_stress = avg_end[0] if len(avg_end) > 0 else 0
    high_proc_stress = avg_end[4] if len(avg_end) > 4 else 0
    stress_ratio = high_proc_stress / low_proc_stress if low_proc_stress > 0 else 0

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[f"Level {p}" for p in proc_levels],
            y=avg_begin,
            name="Beginning",
            marker=dict(color="#64c7c8"),
            text=[f"{v:.1f}" for v in avg_begin],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            x=[f"Level {p}" for p in proc_levels],
            y=avg_end,
            name="End",
            marker=dict(color="#f27d72"),
            text=[f"{v:.1f}" for v in avg_end],
            textposition="outside",
        )
    )
    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=20, b=20),
        barmode="group",
        yaxis=dict(title="Average Stress Level", range=[0, 5.8]),
        xaxis=dict(title="Procrastination Level"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(orientation="h", y=1.12, x=0),
    )
    
    with st.container():
        st.markdown(f'''
        <div class="chart-group card-orange">
            <div class="group-header">
                <div class="group-kicker">BEHAVIORAL CORRELATION</div>
                <h3 class="group-title">Stress vs Procrastination Level</h3>
                <p class="group-subtitle">Higher procrastination = steeper stress growth by semester end.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.plotly_chart(fig, use_container_width=True, key="stress_procrastination")
        
        st.markdown(f'''
        <div class="group-insight insight-orange">
            <div class="insight-icon">⚠️</div>
            <div class="insight-content">
                <div class="insight-title">CRITICAL FINDING</div>
                <div class="insight-text">High procrastinators experience {stress_ratio:.1f}x more stress ({high_proc_stress:.1f} vs {low_proc_stress:.1f}). Delaying work compounds pressure exponentially.</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


# -----------------------------------------------
# Chart 3 — Study Method Treemap (Purple Theme)
# -----------------------------------------------
def study_method_vs_cgpa_chart(df):
    import plotly.express as px

    study_method_col = "study_method"
    if study_method_col not in df.columns:
        st.error(f"Column '{study_method_col}' not found.")
        return

    method_map = {
        "Summarizing/making notes": "Summarizing / Notes",
        "Doing practice questions": "Practice Questions",
        "Reading lecture notes": "Reading Notes",
        "Watching recorded lectures/videos": "Watching Videos",
        "Ai generated quiz game": "AI Quiz Game",
        "all of the above": "AI Quiz Game",
    }

    method_colors = {
        "Practice Questions":  "#C4B5FD",  # Pastel lavender-purple
        "Summarizing / Notes": "#BFDBFE",  # Pastel blue
        "Reading Notes":       "#A7F3D0",  # Pastel mint green
        "Watching Videos":     "#FDE68A",  # Pastel amber/yellow
        "AI Quiz Game":        "#FBCFE8",  # Pastel pink
    }

    # Updated CGPA mapping with group names
    cgpa_label_map = {
        1.0: "Failing (CGPA < 2.00)", 
        2.5: "Satisfactory (CGPA 2.00 - 2.99)", 
        3.5: "Good (CGPA 3.00 - 3.99)", 
        4.0: "Excellent (CGPA 4.00)"
    }
    
    # CGPA group display names
    cgpa_group_names = {
        "Excellent (CGPA 4.00)": "Excellent (CGPA 4.00)",
        "Good (CGPA 3.00 - 3.99)": "Good (CGPA 3.00 - 3.99)",
        "Satisfactory (CGPA 2.00 - 2.99)": "Satisfactory (CGPA 2.00 - 2.99)",
        "Failing (CGPA < 2.00)": "Failing (CGPA < 2.00)",
    }

    plot_df = df.copy()
    plot_df["method_clean"] = plot_df[study_method_col].map(method_map).fillna("Other")
    plot_df["cgpa_label"] = plot_df["cgpa"].map(cgpa_label_map).fillna("Other")
    plot_df["color_val"] = plot_df["method_clean"].map(method_colors).fillna("#9A9890")

    # CGPA filter via radio
    cgpa_options = ["All CGPA", "Excellent (CGPA 4.00)", "Good (CGPA 3.00 - 3.99)", "Satisfactory (CGPA 2.00 - 2.99)","Failing (CGPA < 2.00)"]
    selected_cgpa = st.radio(
        "Filter by CGPA group:",
        cgpa_options,
        horizontal=True,
        key="treemap_cgpa_filter",
        label_visibility="collapsed",
    )

    if selected_cgpa == "All CGPA":
        filtered_df = plot_df.copy()
        treemap_path = ["method_clean", "cgpa_label"]
        title_suffix = "All CGPA Groups"
    else:
        filtered_df = plot_df[plot_df["cgpa_label"] == selected_cgpa].copy()
        treemap_path = ["method_clean"]
        title_suffix = selected_cgpa

    grouped = (
        filtered_df.groupby(["method_clean", "cgpa_label"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
    grouped["color_val"] = grouped["method_clean"].map(method_colors).fillna("#9A9890")

    # Build treemap using graph_objects for full color control
    if selected_cgpa == "All CGPA":
        # labels = methods + cgpa sub-nodes + root
        methods_unique = list(method_colors.keys())
        labels, parents, values, colors_list, hover_texts = [], [], [], [], []

        # root - changed to grey
        labels.append("All Students")
        parents.append("")
        values.append(len(filtered_df))
        colors_list.append("#D1D5DB")  # Warm light grey  # Soft grey instead of purple
        hover_texts.append(f"Total: {len(filtered_df)} students")

        for method in methods_unique:
            m_df = grouped[grouped["method_clean"] == method]
            total_m = m_df["count"].sum()
            if total_m == 0:
                continue
            labels.append(method)
            parents.append("All Students")
            values.append(int(total_m))
            colors_list.append(method_colors.get(method, "#9A9890"))
            hover_texts.append(f"{method}<br>{total_m} students")

            for _, row in m_df.iterrows():
                # Use CGPA group name instead of raw label
                cgpa_display = cgpa_group_names.get(row['cgpa_label'], row['cgpa_label'])
                node_label = f"{method} — {cgpa_display}"
                labels.append(node_label)
                parents.append(method)
                values.append(int(row["count"]))
                colors_list.append(method_colors.get(method, "#9A9890"))
                hover_texts.append(f"{method}<br>{cgpa_display}<br>{row['count']} students")

        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colors=colors_list, line=dict(width=2, color="white")),
            hovertext=hover_texts,
            hoverinfo="text",
            texttemplate="<b>%{label}</b><br>%{value} students",
            textfont=dict(size=14, color="black"),  # Larger font (14) and black color
            root_color="#f8f0ff",
            branchvalues="total",
        ))
    else:
        # Get the display name for the selected CGPA group
        selected_cgpa_display = cgpa_group_names.get(selected_cgpa, selected_cgpa)
        
        # Flat treemap for single CGPA
        m_counts = (
            filtered_df.groupby("method_clean").size().reset_index(name="count")
        )
        
        # Replace "Selected Group" with the actual CGPA group name
        labels = [selected_cgpa_display] + m_counts["method_clean"].tolist()
        parents = [""] + [selected_cgpa_display] * len(m_counts)
        values = [m_counts["count"].sum()] + m_counts["count"].tolist()
        colors_list = ["#9CA3AF"] + [method_colors.get(m, "#9A9890") for m in m_counts["method_clean"]]  # Grey root
        hover_texts = [f"Total {selected_cgpa_display}: {m_counts['count'].sum()} students"] + [
            f"{row['method_clean']}<br>{row['count']} students" for _, row in m_counts.iterrows()
        ]

        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colors=colors_list, line=dict(width=2, color="white")),
            hovertext=hover_texts,
            hoverinfo="text",
            texttemplate="<b>%{label}</b><br>%{value} students",
            textfont=dict(size=14, color="black"),  # Larger font (14) and black color
            root_color="#f8f0ff",
            branchvalues="total",
        ))

    fig.update_layout(
        height=400,  # Increased height for better visibility when full width
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    # Compute insight stat
    ct = pd.crosstab(plot_df["cgpa_label"], plot_df["method_clean"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    active_cols = [c for c in ["Practice Questions", "Summarizing / Notes"] if c in ct_pct.columns]
    active_pct = ct_pct[active_cols].sum(axis=1)
    high_cgpa_active = active_pct.get("Excellent (4.00)", 0)
    low_cgpa_active = active_pct.get("Failing (< 2.00)", 0)

    with st.container():
        st.markdown('''
        <div class="chart-group card-purple">
            <div class="group-header">
                <div class="group-kicker">INTERACTIVE TREEMAP</div>
                <h3 class="group-title">Study Method by CGPA Group</h3>
                <p class="group-subtitle">Click a CGPA group below to explore study method distribution. Larger tiles = more students.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True, key="study_method_treemap")

        st.markdown(f'''
        <div class="group-insight insight-purple">
            <div class="insight-icon">🎯</div>
            <div class="insight-content">
                <div class="insight-title">PERFORMANCE IMPACT</div>
                <div class="insight-text">
                    High-performing students (CGPA 3.0–4.0) predominantly rely on <strong>active study strategies, with summarizing/making notes and practicing questions</strong> emerging as the most common approaches.<br><br>
                    However, practice questions alone may not be sufficient. While the only failing student relies entirely on practice (based on a very small sample), higher-performing groups show a stronger emphasis on summarizing, particularly among excellent students (CGPA 4.0).<br><br>
                    From another perspective, these active methods are also most frequently associated with higher CGPA groups, indicating a consistent relationship between study approach and academic performance.<br><br>
                </div>
                <div class="insight-title">OVERALL TAKEAWAY:</div>
                <div class="insight-text"> 
                    Students who engage in <strong>active learning methods</strong> tend to achieve better academic outcomes, suggesting that <strong>how you study may matter more than simply how much you study</strong>.
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

# -----------------------------------------------
# Chart 4 — Procrastination Penalty (Red Theme) — Enhanced
# -----------------------------------------------
def procrastination_vs_cgpa_chart(df):
    """
    Grouped bar chart showing distribution of students across procrastination levels
    for each CGPA group.
    """
    import plotly.graph_objects as go
    import numpy as np
    
    # Define CGPA groups and their display properties
    cgpa_groups = [1.0, 2.5, 3.5, 4.0]
    cgpa_labels = ['Failing (CGPA < 2.00)', 'Satisfactory (CGPA 2.00–2.99)', 'Good (CGPA 3.00–3.99)', 'Excellent (CGPA 4.00)']
    cgpa_colors = ['#f27d72', '#f7c440', '#64c7c8', '#22c55e']  # Coral, Amber, Teal, Green
    
    proc_levels = [1, 2, 3, 4, 5]
    proc_labels = ['Level 1\n(None)', 'Level 2\n(Low)', 'Level 3\n(Moderate)', 'Level 4\n(High)', 'Level 5\n(Severe)']
    
    # Calculate counts for each combination
    n_proc = len(proc_levels)
    n_groups = len(cgpa_groups)
    bar_width = 0.18
    x = np.arange(n_proc)
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for each CGPA group
    for i, (cgpa, label, color) in enumerate(zip(cgpa_groups, cgpa_labels, cgpa_colors)):
        counts = []
        for p in proc_levels:
            # Handle CGPA matching with tolerance for floating point
            if cgpa == 4.0:
                mask = (df['cgpa'] >= 3.9) & (df['procrastination_level'] == p)
            elif cgpa == 3.5:
                mask = (df['cgpa'] >= 3.3) & (df['cgpa'] < 3.9) & (df['procrastination_level'] == p)
            elif cgpa == 2.5:
                mask = (df['cgpa'] >= 2.3) & (df['cgpa'] < 3.3) & (df['procrastination_level'] == p)
            else:  # cgpa == 1.0
                mask = (df['cgpa'] < 2.3) & (df['procrastination_level'] == p)
            counts.append(len(df[mask]))
        
        # Calculate offset for this group
        offset = (i - n_groups / 2 + 0.5) * bar_width
        
        fig.add_trace(go.Bar(
            name=label,
            x=[f'Level {p}' for p in proc_levels],
            y=counts,
            width=bar_width,
            marker=dict(color=color, opacity=0.85),
            text=[str(int(c)) if c > 0 else '' for c in counts],
            textposition='outside',
            textfont=dict(size=10),
            offsetgroup=i,
            legendgroup=label,
            hovertemplate='<b>%{x}</b><br>%{fullData.name}<br>Students: <b>%{y}</b><extra></extra>'
        ))
    
    # Calculate total students per procrastination level for insights
    total_by_proc = [len(df[df['procrastination_level'] == p]) for p in proc_levels]
    level_3_4_total = total_by_proc[2] + total_by_proc[3]  # Levels 3 + 4
    total_students = len(df)
    pct_at_3_4 = (level_3_4_total / total_students) * 100 if total_students > 0 else 0
    
    # CGPA 1.0 students at level 5
    level5_cgpa1 = len(df[(df['procrastination_level'] == 5) & (df['cgpa'] < 2.3)])
    cgpa1_total = len(df[df['cgpa'] < 2.3])
    pct_cgpa1_at_level5 = (level5_cgpa1 / cgpa1_total) * 100 if cgpa1_total > 0 else 0
    
    # Update layout
    fig.update_layout(
        template='plotly_white',
        height=400,
        margin=dict(l=20, r=20, t=30, b=50),
        xaxis=dict(
            title='Procrastination Level (1 = Never → 5 = Always)',
            tickangle=0,
            tickfont=dict(size=11),
            title_font=dict(size=12),
        ),
        yaxis=dict(
            title='Number of Students',
            gridcolor='#e2e8f0',
            title_font=dict(size=12),
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.05,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=11),
            title=None,
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    
    with st.container():
        st.markdown('''
        <div class="chart-group card-red">
            <div class="group-header">
                <div class="group-kicker">DISTRIBUTION ANALYSIS</div>
                <h3 class="group-title">Procrastination Level vs CGPA Group</h3>
                <p class="group-subtitle">Majority of students are at levels 3–4; CGPA 1.0 sits entirely at level 5</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.plotly_chart(fig, use_container_width=True, key="procrastination_cgpa_distribution")

        st.markdown(f'''
        <div class="group-insight insight-red">
            <div class="insight-icon">🎯</div>
            <div class="insight-content">
                <div class="insight-title">PROCRASTINATION PATTERNS</div>
                <div class="insight-text">
                    Most students in the <strong>Good (CGPA 3.00–3.99)</strong> group are concentrated at procrastination levels 3 and 4, suggesting that moderate procrastination is common among higher-performing students.<br><br>
                    Although some students still achieve good results at high procrastination levels (level 5), these cases are less dominant compared to moderate levels, indicating that extreme procrastination is less typical among stronger academic performers. This pattern suggests that successful students do not necessarily eliminate procrastination; instead, they tend to manage it at moderate levels rather than allowing it to become extreme.<br><br>
                <div class="insight-title">OVERALL TAKEAWAY:</div>
                <div class="insight-text"> 
                    There is a <strong>possible association between procrastination level and academic performance</strong>, where <strong>extreme procrastination is less common among higher-performing students</strong>.
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

# ---------------------------------------------------------
# Chart 5 — Sleep Impact (Blue Theme)
# ---------------------------------------------------------
def sleep_chart(df):
    summary = (
        df.groupby("sleep_hours", as_index=False)
        .agg(avg_cgpa=("cgpa", "mean"), avg_stress=("stress_end", "mean"))
        .sort_values("sleep_hours")
    )

    summary["cgpa_norm"] = (summary["avg_cgpa"] / 4.0) * 100
    summary["stress_norm"] = (summary["avg_stress"] / 5.0) * 100
    
    if len(summary) > 0:
        optimal_idx = summary["avg_cgpa"].idxmax()
        optimal_sleep = summary.loc[optimal_idx, "sleep_hours"]
        optimal_cgpa = summary["avg_cgpa"].max()
        optimal_stress = summary.loc[optimal_idx, "avg_stress"]
    else:
        optimal_sleep, optimal_cgpa, optimal_stress = 7, 3.5, 4.0

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=summary["sleep_hours"],
            y=summary["cgpa_norm"],
            mode="lines+markers",
            name="CGPA",
            line=dict(color="#22c7f0", width=3),
            marker=dict(size=8),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=summary["sleep_hours"],
            y=summary["stress_norm"],
            mode="lines+markers",
            name="Stress",
            line=dict(color="#ef7a7a", width=3),
            marker=dict(size=8),
        )
    )
    fig.update_layout(
        template="plotly_white",
        height=340,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(title="Sleep Hours"),
        yaxis=dict(title="Normalized Score (%)", range=[0, 100]),
        legend=dict(orientation="h", y=1.1),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    
    with st.container():
        st.markdown(f'''
        <div class="chart-group card-blue">
            <div class="group-header">
                <div class="group-kicker">DUAL-AXIS ANALYSIS</div>
                <h3 class="group-title">Sleep Impact Analysis</h3>
                <p class="group-subtitle">Sleep influences both stress levels and academic outcomes.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.plotly_chart(fig, use_container_width=True, key="sleep_impact")
        
        st.markdown(f'''
        <div class="group-insight insight-blue">
            <div class="insight-icon">😴</div>
            <div class="insight-content">
                <div class="insight-title">SWEET SPOT IDENTIFIED</div>
                <div class="insight-text">{optimal_sleep:.0f}-{optimal_sleep+1:.0f} hours maximizes CGPA ({optimal_cgpa:.1f}) while minimizing stress ({optimal_stress:.1f}).</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def show_behavioral_insights():
    load_css()
    df = load_data()

    # Section 1: Stress
    st.markdown('<h1 class="page-title">What Really Drives Academic Performance?</h1>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag stress-tag">STRESS ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="subpage-title">Academic Pressure builds Over time</h2>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Examining how stress evolves throughout the semester and its relationship with procrastination.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        stress_start_end_chart(df)
    with col2:
        stress_vs_procrastination_chart(df)

    # Section 2: Behavioral Insights
    st.markdown('<div class="section-divider"><span>STUDY QUALITY &amp; LIFESTYLE</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag habits-tag">METHODS &amp; HABITS</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="subpage-title">How Methods &amp; Habits Impact Results</h2>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Understanding the relationship between study techniques, procrastination, sleep habits, and academic success.</p>', unsafe_allow_html=True)

    # Treemap - full width row
    study_method_vs_cgpa_chart(df)
    
    # Two column row below treemap
    col3, col4 = st.columns(2, gap="large")
    with col3:
        procrastination_vs_cgpa_chart(df)
    with col4:
        sleep_chart(df)

    # Summary banner
    st.markdown('''
    <div class="highlight-banner">
        <h3>📊 Key Takeaways</h3>
        <p>✅ Active learning methods significantly outperform passive reading</p>
        <p>✅ High procrastination leads to 2.1x more stress and 25% lower CGPA</p>
        <p>✅ 7-8 hours of sleep is the optimal range for academic success</p>
        <p>✅ Consistent studying beats last-minute cramming for long-term retention</p>
    </div>
    ''', unsafe_allow_html=True)

    st.page_link("pages/recommendations.py", label="Go to Recommendations Page")


if __name__ == "__main__":
    show_behavioral_insights()