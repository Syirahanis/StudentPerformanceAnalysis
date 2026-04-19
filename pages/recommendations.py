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


def html(content: str):
    """Render raw HTML safely."""
    st.markdown(content, unsafe_allow_html=True)


def spacer(px=8):
    st.markdown(f"<div style='height:{px}px'></div>", unsafe_allow_html=True)


def strategy_card(number, color, label, title, body, citations, takeaway):
    """Render a full strategy card with citation blocks and takeaway."""

    cite_html = ""
    for source, text in citations:
        cite_html += (
            '<div class="citation-block ' + color + '-cite" style="margin-bottom:0.7rem;">'
            '<div class="cite-icon">&#128196;</div>'
            '<div class="cite-content">'
            '<div class="cite-source">' + source + '</div>'
            '<p class="cite-text">' + text + '</p>'
            '</div>'
            '</div>'
        )

    card = (
        '<div class="strategy-card">'
        '<div class="strategy-top">'
        '<div class="strategy-number ' + color + '">' + number + '</div>'
        '<div class="strategy-meta">'
        '<div class="strategy-label ' + color + '">' + label + '</div>'
        '<h3 class="strategy-title">' + title + '</h3>'
        '</div>'
        '</div>'
        '<p class="strategy-body">' + body + '</p>'
        + cite_html +
        '<div class="takeaway-row ' + color + '-take">'
        '<span class="takeaway-icon">&#128161;</span>'
        '<span>' + takeaway + '</span>'
        '</div>'
        '</div>'
    )

    st.markdown(card, unsafe_allow_html=True)


def show_recommendations():
    load_css()

    # ── Page header ───────────────────────────────────────────────────────────
    html(
        '<div class="page-header">'
        '<div class="page-tag">Final Analysis</div>'
        '<h1 class="page-title">What This All Means And What You Can Do About It</h1>'
        '</div>'
    )

    # ── Conclusion panel ──────────────────────────────────────────────────────
    html(
        '<div class="conclusion-panel">'
        '<div class="conclusion-header">'
        '<div class="conclusion-icon">&#9678;</div>'
        '<div>'
        '<div class="conclusion-label">CONCLUSION</div>'
        '</div>'
        '</div>'
        '<p class="conclusion-body">'
        'Across 103 students, the data tells a clear and consistent story: '
        '<strong>it&#39;s not how long you study</strong> but it&#39;s <strong>how you study, '
        'when you start, and how well you manage pressure </strong> along the way that most strongly predicts academic success.'
        '</p>'
        '<p class="conclusion-body" style="margin-bottom:0;">'
        'The research beyond this dataset agrees.'
        '</p>'
        '</div>'
    )

    spacer(10)

    # ── Section heading row  ──────────
    html(
        '<div style="margin: 1rem 0 1.5rem 0;">'
        '<div style="display: flex; align-items: center; gap: 0.8rem;">'
        '<div style="width: 4px; height: 40px; background: linear-gradient(180deg, #7c3aed, #ec4899); border-radius: 4px;"></div>'
        '<h2 style="font-size: 2rem; font-weight: 900; margin: 0; letter-spacing: -0.02em;">3 Evidence-Backed Strategies</h2>'
        '</div>'
        '<p style="font-size: 0.95rem; color: #6b7280; margin: 0.5rem 0 0 0.9rem;">Supported by peer-reviewed research beyond this dataset</p>'
        '</div>'
    )
    # Strategy 1
    st.markdown("""
    <div class="strategy-card hover-card" style="border-bottom: 3px solid #a855f7;">
        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
            <div style="width: 50px; height: 50px; border-radius: 14px; background: linear-gradient(135deg, #7c3aed, #a855f7); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 900;">1</div>
            <div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #a855f7;">Study Smarter, Not Longer</div>
            </div>
        </div>
        <p style="font-size: 1rem; color: #374151; line-height: 1.7;">High-performing students leaned on active methods such as summarising, note-making, and practising questions rather than passive re-reading. Academic success is driven more by how students study rather than how long they study.</p>
        <div style="background: #f3e8ff40; border-left: 3px solid #a855f7; padding: 0.8rem; border-radius: 12px; margin: 0.8rem 0;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #a855f7;">Theobald (2025) · British Journal of Educational Psychology</div>
            <p style="font-size: 0.9rem; margin: 0.3rem 0 0 0;">Effective study strategies can <strong>compensate for lower study time</strong> in achieving academic goals.</p>
        </div>
        <div style="background: #f3e8ff; padding: 0.8rem 1rem; border-radius: 12px;">
            💡 <strong>Takeaway:</strong> Replace passive re-reading with active recall. Summarise in your own words. Test yourself. Teach it to someone else.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Strategy 2
    st.markdown("""
    <div class="strategy-card hover-card" style="border-bottom: 3px solid #f59e0b;">
        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
            <div style="width: 50px; height: 50px; border-radius: 14px; background: linear-gradient(135deg, #d97706, #f59e0b); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 900;">2</div>
            <div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #f59e0b;">Start Early. Stress Compounds If You Don't</div>
            </div>
        </div>
        <p style="font-size: 1rem; color: #374151; line-height: 1.7;">In this study, students at the highest procrastination level experienced <strong>more than twice</strong> the stress of their least-procrastinating peers by semester end.</p>
        <div style="background: #fffbeb40; border-left: 3px solid #f59e0b; padding: 0.8rem; border-radius: 12px; margin: 0.8rem 0;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #f59e0b;">Ahmady et al. (2021) · Systematic Review & Meta-Analysis</div>
            <p style="font-size: 0.9rem; margin: 0.3rem 0 0 0;">A significant <strong>negative correlation</strong> between stress and academic performance was found (<em>r</em> = −0.32).</p>
        </div>
        <div style="background: #fffbeb; padding: 0.8rem 1rem; border-radius: 12px;">
            ⏰ <strong>Takeaway:</strong> The earlier you start, the less you'll suffer in Week 14. Breaking tasks into smaller chunks early in the semester is one of the highest-leverage habits you can build.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Strategy 3
    st.markdown("""
    <div class="strategy-card hover-card" style="border-bottom: 3px solid #ec4899;">
        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
            <div style="width: 50px; height: 50px; border-radius: 14px; background: linear-gradient(135deg, #db2777, #ec4899); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 900;">3</div>
            <div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #ec4899;">Keep Procrastination Moderate. Don't Let It Become Extreme</div>
            </div>
        </div>
        <p style="font-size: 1rem; color: #374151; line-height: 1.7;">Most Good-band students (CGPA 3.00–3.99) clustered at <strong>moderate procrastination levels</strong>, not zero.</p>
        <div style="background: #fdf2f840; border-left: 3px solid #ec4899; padding: 0.8rem; border-radius: 12px; margin: 0.8rem 0;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #ec4899;">De Paola & Scoppa (2024) · Meta-Analysis (96 studies, 55k+ participants)</div>
            <p style="font-size: 0.9rem; margin: 0.3rem 0 0 0;"><strong>Active procrastination</strong> (strategic delay) has a weaker negative effect than <strong>passive procrastination</strong> (avoidance-driven), suggesting the type of delay matters as much as the amount.</p>
        </div>
        <div style="background: #fdf2f8; padding: 0.8rem 1rem; border-radius: 12px;">
            🎯 <strong>Takeaway:</strong> A little delay won't derail you. Chronic avoidance will. The goal isn't to be perfect but it's to not let things pile up until they collapse on you.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key message banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6d28d9 0%, #db2777 55%, #0891b2 100%); border-radius: 28px; padding: 2.5rem; text-align: center; margin: 1rem 0;">
        <div style="display: inline-block; padding: 0.3rem 1rem; background: rgba(255,255,255,0.2); border-radius: 40px; font-size: 0.75rem; font-weight: 700; color: white; margin-bottom: 1.5rem;">
            THE ONE THING TO TAKE WITH YOU
        </div>
        <div style="font-size: 2rem; font-weight: 800; font-style: italic; color: white; line-height: 1.3; max-width: 700px; margin: 0 auto 1.5rem auto;">
            "It's not the hours you put in.<br>It's what you put into the hours and when."
        </div>
        <p style="font-size: 1rem; color: rgba(255,255,255,0.9); max-width: 600px; margin: 0 auto;">
        The students in this dataset who performed best were not necessarily the ones who studied the most. They were the ones who used smarter methods, started earlier, and kept procrastination from spiralling.
        </p>
        <div style="display: flex; gap: 0.6rem; justify-content: center; flex-wrap: wrap; margin-top: 1.5rem;">
            <span style="padding: 0.3rem 1rem; background: rgba(255,255,255,0.15);color: white; border-radius: 40px;">🎯 Quality over Quantity</span>
            <span style="padding: 0.3rem 1rem; background: rgba(255,255,255,0.15); color: white; border-radius: 40px;">⏰ Start Early</span>
            <span style="padding: 0.3rem 1rem; background: rgba(255,255,255,0.15); color: white; border-radius: 40px;">📚 Active > Passive</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

        # ── References ────────────────────────────────────────────────────────────
    html(
        '<div class="references-box">'
        '<div class="references-title">References</div>'
        '<ul class="references-list">'
        '<li>Theobald, M. (2025). Study strategies and academic performance. <em>British Journal of Educational Psychology</em>.</li>'
        '<li>Ahmady, S. et al. (2021). Relation between stress, time management, and academic achievement: A systematic review and meta-analysis. <em>PMC / Medical Education</em>.</li>'
        '<li>De Paola, M. &amp; Scoppa, V. (2024). The influence of active and passive procrastination on academic performance: A meta-analysis. <em>Education Sciences</em>, 14(3), 323. MDPI.</li>'
        '</ul>'
        '</div>'
    )


show_recommendations()