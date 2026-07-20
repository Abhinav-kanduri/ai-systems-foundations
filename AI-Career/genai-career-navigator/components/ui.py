"""
Shared UI helpers: global styling and reusable visual components.

Everything here renders with native Streamlit + a little inline HTML/CSS so the
app looks polished, works offline, and adapts to light and dark themes. No
external fonts, scripts, or CDNs are used.
"""

import html

import streamlit as st

# Accent color used across the app (indigo/violet).
ACCENT = "109, 94, 252"  # rgb components, used inside rgba(...)


def inject_css():
    """Inject the global stylesheet once per page render."""
    st.markdown(
        f"""
        <style>
        :root {{ --gcn-accent: {ACCENT}; }}

        /* Headings a touch tighter and stronger */
        h1, h2, h3 {{ letter-spacing: -0.01em; }}

        /* Metric cards */
        div[data-testid="stMetric"] {{
            background: rgba(var(--gcn-accent), 0.06);
            border: 1px solid rgba(var(--gcn-accent), 0.18);
            border-radius: 14px;
            padding: 14px 16px;
        }}
        div[data-testid="stMetric"] label {{ opacity: 0.75; }}

        /* Expanders as soft cards */
        div[data-testid="stExpander"] {{
            border: 1px solid rgba(var(--gcn-accent), 0.18);
            border-radius: 14px;
            overflow: hidden;
        }}

        /* Tabs: pill-like active state */
        button[data-baseweb="tab"] {{ font-weight: 600; }}

        /* Flow of steps (chips connected by arrows) */
        .gcn-flow {{
            display: flex;
            flex-wrap: wrap;
            align-items: stretch;
            gap: 8px;
            margin: 6px 0 4px 0;
        }}
        .gcn-step {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(180deg,
                rgba(var(--gcn-accent), 0.14),
                rgba(var(--gcn-accent), 0.07));
            border: 1px solid rgba(var(--gcn-accent), 0.30);
            border-radius: 12px;
            padding: 9px 13px;
            font-weight: 600;
            font-size: 0.9rem;
            line-height: 1.25;
        }}
        .gcn-step .gcn-idx {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 22px;
            height: 22px;
            border-radius: 50%;
            background: rgba(var(--gcn-accent), 0.9);
            color: #fff;
            font-size: 0.78rem;
            font-weight: 700;
        }}
        .gcn-arrow {{
            align-self: center;
            font-size: 1.15rem;
            opacity: 0.45;
            padding: 0 1px;
        }}

        /* Phase cards */
        .gcn-phases {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: stretch;
            margin: 8px 0;
        }}
        .gcn-phase {{
            flex: 1 1 180px;
            background: linear-gradient(180deg,
                rgba(var(--gcn-accent), 0.12),
                rgba(var(--gcn-accent), 0.04));
            border: 1px solid rgba(var(--gcn-accent), 0.28);
            border-radius: 16px;
            padding: 16px 18px;
        }}
        .gcn-phase .gcn-kicker {{
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            opacity: 0.7;
            font-weight: 700;
        }}
        .gcn-phase .gcn-title {{ font-size: 1.05rem; font-weight: 800; margin: 2px 0 6px; }}
        .gcn-phase .gcn-body {{ font-size: 0.9rem; opacity: 0.9; }}

        /* Generic soft panel */
        .gcn-lane {{
            border: 1px solid rgba(var(--gcn-accent), 0.20);
            border-radius: 14px;
            padding: 12px 14px 14px;
            margin: 6px 0 12px;
        }}
        .gcn-lane .gcn-lane-title {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 800;
            opacity: 0.75;
            margin-bottom: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _esc(text) -> str:
    return html.escape(str(text).strip())


def flow(steps, numbered: bool = False):
    """Render a horizontal, wrapping flow of steps joined by arrows."""
    items = [s for s in (str(x).strip() for x in steps) if s]
    parts = []
    for i, label in enumerate(items):
        idx = f'<span class="gcn-idx">{i + 1}</span>' if numbered else ""
        parts.append(f'<div class="gcn-step">{idx}<span>{_esc(label)}</span></div>')
        if i < len(items) - 1:
            parts.append('<span class="gcn-arrow">&rarr;</span>')
    st.markdown(f'<div class="gcn-flow">{"".join(parts)}</div>', unsafe_allow_html=True)


def phase_cards(items):
    """Render a row of phase cards. `items` = list of (kicker, title, body)."""
    cards = []
    for kicker, title, body in items:
        cards.append(
            '<div class="gcn-phase">'
            f'<div class="gcn-kicker">{_esc(kicker)}</div>'
            f'<div class="gcn-title">{_esc(title)}</div>'
            f'<div class="gcn-body">{_esc(body)}</div>'
            "</div>"
        )
    st.markdown(f'<div class="gcn-phases">{"".join(cards)}</div>', unsafe_allow_html=True)


def lane(title: str, steps, numbered: bool = False):
    """A labeled panel containing a flow — used for pipeline 'lanes'."""
    items = [s for s in (str(x).strip() for x in steps) if s]
    parts = []
    for i, label in enumerate(items):
        idx = f'<span class="gcn-idx">{i + 1}</span>' if numbered else ""
        parts.append(f'<div class="gcn-step">{idx}<span>{_esc(label)}</span></div>')
        if i < len(items) - 1:
            parts.append('<span class="gcn-arrow">&rarr;</span>')
    st.markdown(
        f'<div class="gcn-lane"><div class="gcn-lane-title">{_esc(title)}</div>'
        f'<div class="gcn-flow">{"".join(parts)}</div></div>',
        unsafe_allow_html=True,
    )
