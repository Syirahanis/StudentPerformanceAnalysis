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


def apply_chart_style(fig, height=320):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_color="#1f2937",
            bordercolor="#d1d5db",
        ),
        xaxis=dict(
            tickfont=dict(size=11, color="#6b7280"),
            title_font=dict(size=15, color="#1f2937"),
            showgrid=False,
        ),
        yaxis=dict(
            tickfont=dict(size=11, color="#6b7280"),
            title_font=dict(size=15, color="#1f2937"),
            gridcolor="#e5e7eb",
        ),
    )
    return fig


def toggle_interpretation(key):
    """Toggle function for interpretation visibility"""
    if key not in st.session_state:
        st.session_state[key] = False
    st.session_state[key] = not st.session_state[key]


def render_interpretation_button(key, button_text="📊 Show Interpretation"):
    """Render a button that toggles interpretation visibility"""
    if st.button(button_text, key=f"btn_{key}", use_container_width=True):
        toggle_interpretation(key)


def render_interpretation_content(key, content_html):
    """Render the interpretation content if toggled on"""
    if st.session_state.get(key, False):
        st.markdown(content_html, unsafe_allow_html=True)
        if st.button("Hide Interpretation", key=f"hide_{key}", use_container_width=True):
            toggle_interpretation(key)


# -----------------------------------------------
# Chart 1 — Stress Start vs End
# -----------------------------------------------
def stress_start_end_chart(df):
    avg_start = df["stress_start"].mean()
    avg_end = df["stress_end"].mean()
    pct_change = ((avg_end - avg_start) / avg_start) * 100 if avg_start else 0

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Beginning of Semester", "End of Semester"],
            y=[avg_start, avg_end],
            text=[f"{avg_start:.2f}", f"{avg_end:.2f}"],
            textposition="outside",
            marker=dict(color=["#64c7c8", "#f27d72"]),
            width=[0.45, 0.45],
            hovertemplate="<b>%{x}</b><br>Average Stress: <b>%{y:.2f}</b><extra></extra>",
        )
    )

    fig.update_layout(
        yaxis=dict(title="Average Stress Level", range=[0, 5.5]),
        xaxis=dict(title="Semester Phase"),
        showlegend=False,
    )
    fig = apply_chart_style(fig, height=340)

    with st.container():
        st.markdown(
            '''
            <div class="chart-group card-teal">
                <div class="group-header">
                    <div class="group-kicker">SEMESTER COMPARISON</div>
                    <h3 class="group-title">Stress Levels: Beginning vs End of Semester</h3>
                    <p class="group-subtitle">Average stress increases as the semester progresses toward exams.</p>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        st.plotly_chart(fig, use_container_width=True, key="stress_start_end")

        # Collapsible interpretation
        interpretation_key = "insight_stress_start_end"
        render_interpretation_button(interpretation_key)
        
        interpretation_html = f'''
            <div class="group-insight insight-teal">
                <div class="insight-icon">📊</div>
                <div class="insight-content">
                    <div class="insight-title">KEY INSIGHT</div>
                    <div class="insight-text">
                        Students' stress levels increase noticeably over the course of the semester, rising from
                        <strong>{avg_start:.2f}</strong> at the beginning to <strong>{avg_end:.2f}</strong> by the end.
                        This represents an increase of approximately <strong>{pct_change:.0f}%</strong>, indicating
                        that academic pressure becomes much heavier as assignments, deadlines, and examinations approach.
                    </div>
                    <div class="insight-text">
                        Rather than remaining constant, stress builds gradually and reaches its highest point in the
                        final weeks of the semester, when multiple academic demands occur at the same time.
                    </div>
                    <div class="insight-title">OVERALL TAKEAWAY:</div>
                    <div class="insight-text">
                        <strong>Stress tends to peak toward the end of the semester due to increasing academic demands.</strong>
                        This highlights the importance of early preparation and effective time management to reduce last-minute pressure.
                    </div>
                </div>
            </div>
        '''
        render_interpretation_content(interpretation_key, interpretation_html)


# -----------------------------------------------
# Chart 2 — Stress vs Procrastination
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

    low_proc_stress = avg_end[0] if pd.notna(avg_end[0]) else 0
    high_proc_stress = avg_end[4] if pd.notna(avg_end[4]) else 0
    stress_ratio = high_proc_stress / low_proc_stress if low_proc_stress else 0

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[f"Level {p}" for p in proc_levels],
            y=avg_begin,
            name="Beginning",
            marker=dict(color="#64c7c8"),
            text=[f"{v:.1f}" if pd.notna(v) else "" for v in avg_begin],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Beginning Stress: <b>%{y:.1f}</b><extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=[f"Level {p}" for p in proc_levels],
            y=avg_end,
            name="End",
            marker=dict(color="#f27d72"),
            text=[f"{v:.1f}" if pd.notna(v) else "" for v in avg_end],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>End Stress: <b>%{y:.1f}</b><extra></extra>",
        )
    )

    fig.update_layout(
        barmode="group",
        yaxis=dict(title="Average Stress Level", range=[0, 5.8]),
        xaxis=dict(title="Procrastination Level"),
        legend=dict(orientation="h", y=1.10, x=0),
    )
    fig = apply_chart_style(fig, height=320)

    with st.container():
        st.markdown(
            '''
            <div class="chart-group card-orange">
                <div class="group-header">
                    <div class="group-kicker">BEHAVIORAL CORRELATION</div>
                    <h3 class="group-title">Stress Levels vs Procrastination Levels</h3>
                    <p class="group-subtitle">Higher procrastination is strongly associated with increased end-of-semester stress, suggesting that delaying tasks allows academic pressure to accumulate over time.</p>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        st.plotly_chart(fig, use_container_width=True, key="stress_procrastination")

        # Collapsible interpretation
        interpretation_key = "insight_stress_procrastination"
        render_interpretation_button(interpretation_key)
        
        interpretation_html = f'''
            <div class="group-insight insight-orange">
                <div class="insight-icon">⚠️</div>
                <div class="insight-content">
                    <div class="insight-title">KEY INSIGHT</div>
                    <div class="insight-text">
                        Students with higher levels of procrastination tend to experience much greater stress by the end
                        of the semester. While beginning-of-semester stress is relatively similar across most groups,
                        the gap becomes much clearer over time.
                    </div>
                    <div class="insight-text">
                        At the highest level of procrastination, end-of-semester stress rises to around
                        <strong>{high_proc_stress:.1f}</strong>, compared with only <strong>{low_proc_stress:.1f}</strong>
                        for those at the lowest level. This means that students who procrastinate the most experience
                        about <strong>{stress_ratio:.1f} times</strong> the stress by semester end.
                    </div>
                    <div class="insight-title">OVERALL TAKEAWAY:</div>
                    <div class="insight-text">
                        <strong>Higher procrastination is strongly associated with increased stress, especially toward the end
                        of the semester.</strong> Managing tasks earlier and avoiding excessive delay can help reduce the buildup
                        of pressure and lead to a more manageable workload.
                    </div>
                </div>
            </div>
        '''
        render_interpretation_content(interpretation_key, interpretation_html)


# -----------------------------------------------
# Chart 3 — Study Hours Per Day vs Stress
# -----------------------------------------------
def study_hours_vs_stress_chart(df):
    def categorize_hours(hours):
        if hours <= 2:
            return "Low (0-2 hours)"
        elif hours <= 4:
            return "Moderate (3-4 hours)"
        elif hours <= 6:
            return "High (5-6 hours)"
        else:
            return "Very High (7+ hours)"

    df_copy = df.copy()
    df_copy["study_category"] = df_copy["study_hours_before_exam"].apply(categorize_hours)

    summary = (
        df_copy.groupby("study_category", as_index=False)
        .agg(
            avg_stress_start=("stress_start", "mean"),
            avg_stress_end=("stress_end", "mean"),
            student_count=("study_category", "size")
        )
    )

    category_order = ["Low (0-2 hours)", "Moderate (3-4 hours)", "High (5-6 hours)", "Very High (7+ hours)"]
    summary["study_category"] = pd.Categorical(summary["study_category"], categories=category_order, ordered=True)
    summary = summary.sort_values("study_category")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=summary["study_category"],
            y=summary["avg_stress_start"],
            name="Beginning of Semester",
            marker=dict(color="#64c7c8"),
            text=[f"{v:.2f}" for v in summary["avg_stress_start"]],
            textposition="outside",
            hovertemplate="<b>Study Hours:</b> %{x}<br><b>Beginning Stress:</b> %{y:.2f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            x=summary["study_category"],
            y=summary["avg_stress_end"],
            name="End of Semester",
            marker=dict(color="#f27d72"),
            text=[f"{v:.2f}" for v in summary["avg_stress_end"]],
            textposition="outside",
            hovertemplate="<b>Study Hours:</b> %{x}<br><b>End Stress:</b> %{y:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        barmode="group",
        yaxis=dict(title="Average Stress Level", range=[0, 5.5]),
        xaxis=dict(title="Daily Study Hours"),
        legend=dict(orientation="h", y=1.10, x=0),
    )
    fig = apply_chart_style(fig, height=320)

    with st.container():
        st.markdown(
            '''
            <div class="chart-group card-purple">
                <div class="group-header">
                    <div class="group-kicker">STUDY HABITS ANALYSIS</div>
                    <h3 class="group-title">Stress Levels vs Daily Study Hours</h3>
                    <p class="group-subtitle">Comparing stress levels across different daily study durations.</p>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        st.plotly_chart(fig, use_container_width=True, key="study_hours_vs_stress")

        # Collapsible interpretation
        interpretation_key = "insight_study_hours"
        render_interpretation_button(interpretation_key)
        
        interpretation_html = '''
            <div class="group-insight insight-purple">
                <div class="insight-icon">📚</div>
                <div class="insight-content">
                    <div class="insight-title">KEY INSIGHT</div>
                    <div class="insight-text">
                        Longer daily study hours appear to reflect academic pressure rather
                        than guarantee stronger academic outcomes. This suggests that increasing study time alone is not enough;
                        how students manage their workload matters more.
                    </div>
                    <div class="insight-title">OVERALL TAKEAWAY:</div>
                    <div class="insight-text">
                        <strong>Study intensity appears to be linked with higher stress levels,</strong> but this relationship likely reflects academic pressure
                        rather than study hours alone. Managing workload early and maintaining consistent study habits may help reduce stress buildup.
                    </div>
                </div>
            </div>
        '''
        render_interpretation_content(interpretation_key, interpretation_html)


# -----------------------------------------------
# Chart 4 — Stress Comparison (Beginning vs End) by CGPA
# -----------------------------------------------
def stress_vs_cgpa_chart(df):
    def get_cgpa_group(cgpa):
        if cgpa < 2.00:
            return "Below 2.00"
        elif cgpa < 3.00:
            return "2.00 - 2.99"
        elif cgpa < 4.00:
            return "3.00 - 3.99"
        else:
            return "4.00"

    df_copy = df.copy()
    df_copy["cgpa_group"] = df_copy["cgpa"].apply(get_cgpa_group)

    summary = (
        df_copy.groupby("cgpa_group", as_index=False)
        .agg(
            avg_stress_start=("stress_start", "mean"),
            avg_stress_end=("stress_end", "mean"),
            student_count=("cgpa_group", "size")
        )
    )

    summary["stress_difference"] = summary["avg_stress_end"] - summary["avg_stress_start"]

    group_order = ["Below 2.00", "2.00 - 2.99", "3.00 - 3.99", "4.00"]
    summary["cgpa_group"] = pd.Categorical(summary["cgpa_group"], categories=group_order, ordered=True)
    summary = summary.sort_values("cgpa_group")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Beginning of Semester",
            x=summary["cgpa_group"],
            y=summary["avg_stress_start"],
            marker=dict(color="#64c7c8"),
            text=[f"{v:.2f}" for v in summary["avg_stress_start"]],
            textposition="outside",
            hovertemplate="<b>CGPA Group:</b> %{x}<br><b>Beginning Stress:</b> %{y:.2f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            name="End of Semester",
            x=summary["cgpa_group"],
            y=summary["avg_stress_end"],
            marker=dict(color="#f27d72"),
            text=[f"{v:.2f}" for v in summary["avg_stress_end"]],
            textposition="outside",
            hovertemplate="<b>CGPA Group:</b> %{x}<br><b>End Stress:</b> %{y:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        barmode="group",
        yaxis=dict(title="Average Stress Level", range=[0, 5.5]),
        xaxis=dict(title="CGPA Group"),
        legend=dict(orientation="h", y=1.10, x=0),
    )
    fig = apply_chart_style(fig, height=320)

    with st.container():
        st.markdown(
            '''
            <div class="chart-group card-blue">
                <div class="group-header">
                    <div class="group-kicker">STRESS COMPARISON</div>
                    <h3 class="group-title">Stress Levels by CGPA Group</h3>
                    <p class="group-subtitle">Comparing how stress changes across the semester for different performance levels.</p>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        st.plotly_chart(fig, use_container_width=True, key="stress_vs_cgpa")

        # Collapsible interpretation
        interpretation_key = "insight_stress_cgpa"
        render_interpretation_button(interpretation_key)
        
        interpretation_html = f'''
            <div class="group-insight insight-blue">
                <div class="insight-icon">📊</div>
                <div class="insight-content">
                    <div class="insight-title">KEY INSIGHT</div>
                    <div class="insight-text">
                        Stress increases across all CGPA groups,
                        but the pattern is not the same for every student.
                        <strong>Mid-performing students show the sharpest rise, while top-performing students appear to maintain more stable stress levels.</strong>
                    </div>
                    <div class="insight-title">OVERALL TAKEAWAY:</div>
                    <div class="insight-text">
                        This suggests that academic performance may depend not only on pressure itself, but also on how students manage it.
                    </div>
                </div>
            </div>
        '''
        render_interpretation_content(interpretation_key, interpretation_html)


# -----------------------------------------------
# Chart 5 — Study Method Treemap (Purple Theme)
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
        "Practice Questions":  "#C4B5FD",
        "Summarizing / Notes": "#BFDBFE",
        "Reading Notes":       "#A7F3D0",
        "Watching Videos":     "#FDE68A",
        "AI Quiz Game":        "#FBCFE8",
    }

    cgpa_label_map = {
        1.0: "Failing (CGPA < 2.00)",
        2.5: "Satisfactory (CGPA 2.00 - 2.99)",
        3.5: "Good (CGPA 3.00 - 3.99)",
        4.0: "Excellent (CGPA 4.00)"
    }

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

    cgpa_options = ["All CGPA", "Excellent (CGPA 4.00)", "Good (CGPA 3.00 - 3.99)", "Satisfactory (CGPA 2.00 - 2.99)", "Failing (CGPA < 2.00)"]
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

    if selected_cgpa == "All CGPA":
        methods_unique = list(method_colors.keys())
        labels, parents, values, colors_list, hover_texts = [], [], [], [], []

        labels.append("All Students")
        parents.append("")
        values.append(len(filtered_df))
        colors_list.append("#D1D5DB")
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
            textfont=dict(size=14, color="black"),
            root_color="#f8f0ff",
            branchvalues="total",
        ))
    else:
        selected_cgpa_display = cgpa_group_names.get(selected_cgpa, selected_cgpa)

        m_counts = (
            filtered_df.groupby("method_clean").size().reset_index(name="count")
        )

        labels = [selected_cgpa_display] + m_counts["method_clean"].tolist()
        parents = [""] + [selected_cgpa_display] * len(m_counts)
        values = [m_counts["count"].sum()] + m_counts["count"].tolist()
        colors_list = ["#9CA3AF"] + [method_colors.get(m, "#9A9890") for m in m_counts["method_clean"]]
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
            textfont=dict(size=14, color="black"),
            root_color="#f8f0ff",
            branchvalues="total",
        ))

    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    ct = pd.crosstab(plot_df["cgpa_label"], plot_df["method_clean"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    active_cols = [c for c in ["Practice Questions", "Summarizing / Notes"] if c in ct_pct.columns]
    active_pct = ct_pct[active_cols].sum(axis=1)
    high_cgpa_active = active_pct.get("Excellent (CGPA 4.00)", 0)
    low_cgpa_active = active_pct.get("Failing (CGPA < 2.00)", 0)

    with st.container():
        st.markdown('''
        <div class="chart-group card-purple">
            <div class="group-header">
                <div class="group-kicker">INTERACTIVE TREEMAP</div>
                <h3 class="group-title">Study Method by CGPA Group</h3>
                <p class="group-subtitle">Click a CGPA group above to explore study method distribution. Larger tiles = more students.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True, key="study_method_treemap")

        # Collapsible interpretation
        interpretation_key = "insight_treemap"
        render_interpretation_button(interpretation_key)
        
        interpretation_html = f'''
            <div class="group-insight insight-purple">
                <div class="insight-icon">🎯</div>
                <div class="insight-content">
                    <div class="insight-title">PERFORMANCE IMPACT</div>
                    <div class="insight-text">
                        High-performing students (CGPA 3.0–4.0) predominantly rely on <strong>active study strategies, with summarizing/making notes and practicing questions</strong> emerging as the most common approaches.<br><br>
                        However, practice questions alone may not be sufficient. While the only failing student relies entirely on practice (based on a very small sample), higher-performing groups show a stronger emphasis on summarizing, particularly among excellent students (CGPA 4.0).<br><br>
                        From another perspective, these active methods are also most frequently associated with higher CGPA groups, indicating a consistent relationship between study approach and academic performance.
                    </div>
                    <div class="insight-title">OVERALL TAKEAWAY:</div>
                    <div class="insight-text">
                        Students who engage in <strong>active learning methods</strong> tend to achieve better academic outcomes, suggesting that <strong>how you study may matter more than simply how much you study</strong>.
                    </div>
                </div>
            </div>
        '''
        render_interpretation_content(interpretation_key, interpretation_html)


# -----------------------------------------------
# Chart 6 — Procrastination Penalty (Red Theme)
# -----------------------------------------------
def procrastination_vs_cgpa_chart(df):
    import plotly.graph_objects as go
    import numpy as np

    cgpa_groups = [1.0, 2.5, 3.5, 4.0]
    cgpa_labels = ['Failing (CGPA < 2.00)', 'Satisfactory (CGPA 2.00–2.99)', 'Good (CGPA 3.00–3.99)', 'Excellent (CGPA 4.00)']
    cgpa_colors = ['#f27d72', '#f7c440', '#64c7c8', '#22c55e']

    proc_levels = [1, 2, 3, 4, 5]

    n_proc = len(proc_levels)
    n_groups = len(cgpa_groups)
    bar_width = 0.18
    x = np.arange(n_proc)

    fig = go.Figure()

    for i, (cgpa, label, color) in enumerate(zip(cgpa_groups, cgpa_labels, cgpa_colors)):
        counts = []
        for p in proc_levels:
            if cgpa == 4.0:
                mask = (df['cgpa'] >= 3.9) & (df['procrastination_level'] == p)
            elif cgpa == 3.5:
                mask = (df['cgpa'] >= 3.3) & (df['cgpa'] < 3.9) & (df['procrastination_level'] == p)
            elif cgpa == 2.5:
                mask = (df['cgpa'] >= 2.3) & (df['cgpa'] < 3.3) & (df['procrastination_level'] == p)
            else:
                mask = (df['cgpa'] < 2.3) & (df['procrastination_level'] == p)
            counts.append(len(df[mask]))

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

    total_by_proc = [len(df[df['procrastination_level'] == p]) for p in proc_levels]
    level_3_4_total = total_by_proc[2] + total_by_proc[3]
    total_students = len(df)
    pct_at_3_4 = (level_3_4_total / total_students) * 100 if total_students > 0 else 0

    level5_cgpa1 = len(df[(df['procrastination_level'] == 5) & (df['cgpa'] < 2.3)])
    cgpa1_total = len(df[df['cgpa'] < 2.3])
    pct_cgpa1_at_level5 = (level5_cgpa1 / cgpa1_total) * 100 if cgpa1_total > 0 else 0

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

        # Collapsible interpretation
        interpretation_key = "insight_procrastination"
        render_interpretation_button(interpretation_key)
        
        interpretation_html = f'''
            <div class="group-insight insight-red">
                <div class="insight-icon">🎯</div>
                <div class="insight-content">
                    <div class="insight-title">PROCRASTINATION PATTERNS</div>
                    <div class="insight-text">
                        Most students in the <strong>Good (CGPA 3.00–3.99)</strong> group are concentrated at procrastination levels 3 and 4, suggesting that moderate procrastination is common among higher-performing students.<br><br>
                        Although some students still achieve good results at high procrastination levels (level 5), these cases are less dominant compared to moderate levels, indicating that extreme procrastination is less typical among stronger academic performers. This pattern suggests that successful students do not necessarily eliminate procrastination; instead, they tend to manage it at moderate levels rather than allowing it to become extreme.
                    </div>
                    <div class="insight-title">OVERALL TAKEAWAY:</div>
                    <div class="insight-text">
                        There is a <strong>possible association between procrastination level and academic performance</strong>, where <strong>extreme procrastination is less common among higher-performing students</strong>.
                    </div>
                </div>
            </div>
        '''
        render_interpretation_content(interpretation_key, interpretation_html)


def show_behavioral_insights():
    load_css()
    df = load_data()

    # Initialize session state for all interpretations if not exists
    interpretation_keys = [
        "insight_stress_start_end",
        "insight_stress_procrastination",
        "insight_study_hours",
        "insight_stress_cgpa",
        "insight_treemap",
        "insight_procrastination"
    ]
    for key in interpretation_keys:
        if key not in st.session_state:
            st.session_state[key] = False

    # =========================
    # PAGE TITLE
    # =========================
    st.markdown(
        '<h1 class="page-title">How Stress and Habits Shape Academic Performance</h1>',
        unsafe_allow_html=True,
    )

    # =========================
    # STRESS ANALYSIS
    # =========================
    st.markdown('<div class="section-tag stress-tag">STRESS ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="subpage-title">Academic Pressure Builds Over Time</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Examining how stress evolves throughout the semester and how student habits relate to rising pressure.</p>',
        unsafe_allow_html=True,
    )

    # First row - Stress comparison charts
    col1, col2 = st.columns(2, gap="large")
    with col1:
        stress_start_end_chart(df)
    with col2:
        stress_vs_procrastination_chart(df)

    # Second row - Performance relationship charts
    col3, col4 = st.columns(2, gap="large")
    with col3:
        study_hours_vs_stress_chart(df)
    with col4:
        stress_vs_cgpa_chart(df)

    # =========================
    # METHODS & HABITS
    # =========================
    st.markdown('<div class="section-divider"><span>STUDY QUALITY &amp; LIFESTYLE</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag habits-tag">METHODS &amp; HABITS</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="subpage-title">How Study Behavior Relates to Performance</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Examining how stress evolves throughout the semester and how student behavior may contribute to rising academic pressure.</p>',
        unsafe_allow_html=True,
    )

    # Treemap - full width row
    study_method_vs_cgpa_chart(df)
    procrastination_vs_cgpa_chart(df)

    # ==================== FIXED HIGHLIGHT BANNER ====================
    banner_css = r"""
    <style>
    .highlight-banner {
        display: block;
        width: fit-content;
        margin: 2rem auto;
        padding: 1.2rem 1.6rem;
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.08);
        border: 1px solid rgba(168, 85, 247, 0.15);
    }
    .highlight-banner .banner-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    .highlight-card-inner {
        max-width: 800px;
        margin: 0 auto;
    }
    .highlight-banner .divider-line {
        height: 1px;
        width: 3rem;
        background: linear-gradient(90deg, transparent, #c084fc);
    }
    .highlight-banner .divider-line-right {
        background: linear-gradient(270deg, transparent, #c084fc);
    }
    .highlight-banner .divider-dot {
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 50%;
        background: #a855f7;
    }
    .highlight-banner h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #6b21a5;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1.5rem;
    }
    .highlight-banner .takeaway-list {
        max-width: 700px;
        margin: 0 auto;
        text-align: left;
    }
    .highlight-banner .takeaway-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        margin: 0.75rem 0;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(139, 92, 246, 0.1);
        transition: border-bottom-color 0.2s ease;
    }
    .highlight-banner .takeaway-item:hover {
        border-bottom-color: rgba(139, 92, 246, 0.3);
    }
    .highlight-banner .takeaway-icon {
        font-size: 1.1rem;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }
    .highlight-banner .takeaway-text {
        color: #334155;
        font-size: 0.9rem;
        line-height: 1.5;
        flex: 1;
    }
    .highlight-banner .takeaway-text strong {
        color: #7c3aed;
        font-weight: 600;
    }
    </style>
    """
    
    banner_html = """
    <div class="highlight-banner">
        <div class="highlight-card-inner">
            <div class="banner-divider">
                <div class="divider-line"></div>
                <div class="divider-dot"></div>
                <div class="divider-line divider-line-right"></div>
            </div>
            <h3>📊 Key Takeaways</h3>
            <div class="takeaway-list">
                <div class="takeaway-item">
                    <div class="takeaway-icon">📉</div>
                    <div class="takeaway-text">Study duration shows only a <strong>very weak relationship</strong> with CGPA</div>
                </div>
                <div class="takeaway-item">
                    <div class="takeaway-icon">⚠️</div>
                    <div class="takeaway-text">Stress levels <strong>increase significantly</strong> throughout the semester</div>
                </div>
                <div class="takeaway-item">
                    <div class="takeaway-icon">⏳</div>
                    <div class="takeaway-text">Procrastination is <strong>strongly linked</strong> to higher end-of-semester stress</div>
                </div>
                <div class="takeaway-item">
                    <div class="takeaway-icon">🧠</div>
                    <div class="takeaway-text">Active study methods are <strong>more closely associated</strong> with stronger academic performance</div>
                </div>
                <div class="takeaway-item">
                    <div class="takeaway-icon">🎯</div>
                    <div class="takeaway-text">Academic success depends more on <strong>study quality, behavior, and stress management</strong> than on study hours alone</div>
                </div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(banner_css, unsafe_allow_html=True)
    st.markdown(banner_html, unsafe_allow_html=True)

    left_empty, center_col, right_empty = st.columns([1, 2, 1])
    with center_col:
        if st.button(":material/analytics: Go to Recommendations", key="hidden_nav_btn", 
                    type="primary", use_container_width=True, help="Navigate to the recommendations page with actionable insights based on the analysis."):
            st.switch_page("pages/recommendations.py")

if __name__ == "__main__":
    show_behavioral_insights()