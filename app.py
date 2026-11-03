"""
EvidenceLens — Multimodal Claim-to-Decision Assistant
Modern Dark Obsidian & Sage Design System
Warm Obsidian Canvas (#14130F), Elevated Surface (#1A1914), Card (#1E1C16),
Sage Green (#5FB58F), Amber (#F0B158), Coral (#E27E62), Warm Cream (#EDE8DC)
"""

from __future__ import annotations

import json
import os
from datetime import date
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

APP_TITLE = "EvidenceLens"
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EvidenceLens · Multimodal Research & Claim Validation",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# UI DESIGN SYSTEM & THEME TOKENS
# Custom CSS tokens, card layouts, and responsive components
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --color-bg: #14130F;
    --color-bg-elevated: #1A1914;
    --color-bg-card: #1E1C16;
    --color-bg-hover: #29261E;
    --color-surface-sunken: #100F0C;
    --color-border: #2C2A22;
    --color-border-hover: #474437;
    --color-primary: #5FB58F;
    --color-accent: #5FB58F;
    --color-accent-hover: #75C5A1;
    --color-accent-dim: rgba(95, 181, 143, 0.14);
    --color-accent-glow: rgba(95, 181, 143, 0.25);
    --color-highlight: #F0B158;
    --color-highlight-dim: rgba(240, 177, 88, 0.14);
    --color-coral: #E27E62;
    --color-coral-dim: rgba(226, 126, 98, 0.14);
    --color-indigo: #A87492;
    --color-indigo-dim: rgba(168, 116, 146, 0.14);
    --color-text: #EDE8DC;
    --color-text-muted: #A9A294;
    --color-text-subtle: #7D776A;
    --radius-sm: 0.375rem;
    --radius-md: 0.625rem;
    --radius-lg: 1rem;
    --radius-full: 9999px;
}

/* Base Body Styling */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background-color: var(--color-bg) !important;
    color: var(--color-text) !important;
}

/* Remove default Streamlit top header & footer */
#MainMenu, header[data-testid="stHeader"], footer {
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1220px !important;
}

/* ── Top Navbar ────────────────────────────────────────────────────── */
.ev-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 0 1.25rem 0;
    border-bottom: 1px solid var(--color-border);
    margin-bottom: 2.2rem;
}
.ev-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.ev-logo-icon {
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #5FB58F 0%, #3e8162 100%);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 4px 14px 0 rgba(95, 181, 143, 0.28);
    border: 1px solid rgba(255, 255, 255, 0.12);
}
.ev-brand-name {
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: var(--color-text);
}
.ev-brand-sub {
    font-size: 0.75rem;
    color: var(--color-text-subtle);
    font-weight: 500;
    letter-spacing: 0.02em;
}
.ev-status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--color-accent-dim);
    border: 1px solid rgba(95, 181, 143, 0.32);
    color: var(--color-accent);
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.32rem 0.85rem;
    letter-spacing: 0.02em;
}
.ev-status-dot {
    width: 7px;
    height: 7px;
    background-color: var(--color-accent);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--color-accent);
}

/* ── Hero Section ──────────────────────────────────────────────────── */
.ev-hero {
    text-align: center;
    padding: 0.8rem 0 2rem 0;
    max-width: 840px;
    margin: 0 auto;
}
.ev-hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: var(--color-accent-dim);
    color: var(--color-accent);
    border: 1px solid rgba(95, 181, 143, 0.3);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    border-radius: var(--radius-full);
    padding: 0.35rem 1rem;
    margin-bottom: 1.25rem;
}
.ev-hero h1 {
    font-size: clamp(2.3rem, 4.8vw, 3.6rem);
    font-weight: 800;
    letter-spacing: -0.035em;
    line-height: 1.15;
    color: #F8F5EE;
    margin: 0 0 1rem 0;
}
.ev-hero p {
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--color-text-muted);
    margin: 0 auto 1.5rem auto;
}

/* ── Container Cards (Wrap Streamlit border containers) ─────────────── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--color-bg-card) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.6rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45) !important;
    transition: border-color 0.25s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.25s ease !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: var(--color-border-hover) !important;
}

/* Card Headers */
.ev-card-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: var(--color-text-subtle);
    margin-bottom: 1.2rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--color-border);
}

/* ── Secondary Pill Buttons (Quick Presets) ─────────────────────────── */
button[kind="secondary"] {
    background-color: var(--color-bg-card) !important;
    border: 1px solid var(--color-border) !important;
    color: var(--color-text) !important;
    border-radius: var(--radius-full) !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
}
button[kind="secondary"]:hover {
    border-color: var(--color-accent) !important;
    color: var(--color-accent) !important;
    background-color: var(--color-bg-hover) !important;
    box-shadow: 0 0 14px rgba(95, 181, 143, 0.22) !important;
    transform: translateY(-1px) !important;
}

/* ── Primary Action Button ─────────────────────────────────────────── */
button[kind="primary"] {
    background: var(--color-accent) !important;
    color: #0E1B14 !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: var(--radius-md) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1.6rem !important;
    box-shadow: 0 4px 16px 0 rgba(95, 181, 143, 0.3) !important;
    transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
    letter-spacing: -0.01em !important;
}
button[kind="primary"]:hover {
    background: var(--color-accent-hover) !important;
    transform: translateY(-1.5px) !important;
    box-shadow: 0 6px 22px 0 rgba(95, 181, 143, 0.45) !important;
    opacity: 0.98 !important;
}

/* ── Streamlit Form & Textarea Overrides ─────────────────────────────── */
div[data-testid="stTextArea"] label p,
div[data-testid="stFileUploader"] label p,
div[data-testid="stSelectbox"] label p {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--color-text-muted) !important;
    margin-bottom: 0.35rem !important;
}

div[data-testid="stTextArea"] textarea {
    background-color: var(--color-bg-elevated) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--color-text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    line-height: 1.55 !important;
    padding: 0.75rem !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--color-accent) !important;
    box-shadow: 0 0 0 3px rgba(95, 181, 143, 0.18) !important;
    background-color: var(--color-surface-sunken) !important;
}
textarea::placeholder {
    color: var(--color-text-subtle) !important;
    font-size: 0.88rem !important;
}

/* ── File Uploader ─────────────────────────────────────────────────── */
div[data-testid="stFileUploader"] section {
    background-color: var(--color-bg-elevated) !important;
    border: 1.5px dashed var(--color-border) !important;
    border-radius: var(--radius-md) !important;
    padding: 1rem !important;
    transition: all 0.25s ease !important;
}
div[data-testid="stFileUploader"] section:hover {
    border-color: var(--color-accent) !important;
    background-color: var(--color-bg-hover) !important;
}

/* Expander */
div[data-testid="stExpander"] {
    background-color: var(--color-bg-elevated) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-md) !important;
    margin-bottom: 1rem !important;
}
summary[data-testid="stExpanderToggle"] {
    color: var(--color-text-muted) !important;
    font-size: 0.86rem !important;
    font-weight: 600 !important;
}
summary[data-testid="stExpanderToggle"]:hover {
    color: var(--color-text) !important;
}

/* ── KPI Metric Cards Strip ─────────────────────────────────────────── */
.ev-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.9rem;
    margin-bottom: 1.3rem;
}
@media (max-width: 900px) {
    .ev-kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
.ev-kpi-card {
    background: var(--color-bg-elevated);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.2rem;
    transition: all 0.2s ease;
}
.ev-kpi-card:hover {
    border-color: var(--color-border-hover);
    transform: translateY(-1px);
}
.ev-kpi-title {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: var(--color-text-subtle);
    margin-bottom: 0.35rem;
}
.ev-kpi-value {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.ev-kpi-sub {
    font-size: 0.76rem;
    color: var(--color-text-muted);
}

/* Progress bar inside KPI */
.ev-bar-bg {
    background: var(--color-surface-sunken);
    border-radius: var(--radius-full);
    height: 6px;
    overflow: hidden;
    margin: 0.4rem 0;
}
.ev-bar-fill {
    height: 100%;
    border-radius: var(--radius-full);
    transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

/* ── Callout Quote ──────────────────────────────────────────────────── */
.ev-quote {
    background: var(--color-bg-elevated);
    border-left: 3.5px solid var(--color-accent);
    border-radius: var(--radius-sm);
    padding: 1.1rem 1.3rem;
    font-size: 1rem;
    line-height: 1.6;
    color: var(--color-text);
    margin-bottom: 1.2rem;
}

/* ── Evidence Matrix Items ─────────────────────────────────────────── */
.ev-evidence-card {
    background: var(--color-bg-elevated);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 0.95rem 1.1rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s ease;
}
.ev-evidence-card:hover {
    border-color: var(--color-border-hover);
    transform: translateY(-1px);
}
.ev-evidence-point {
    font-size: 0.92rem;
    line-height: 1.55;
    color: var(--color-text);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
}
.ev-evidence-source {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--color-text-subtle);
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid var(--color-border);
    padding: 0.2rem 0.55rem;
    border-radius: var(--radius-sm);
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}

/* ── Roadmap Item ──────────────────────────────────────────────────── */
.ev-step-row {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    background: var(--color-bg-elevated);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.7rem;
}
.ev-step-badge {
    width: 26px;
    height: 26px;
    background: var(--color-accent);
    color: #0E1B14;
    font-weight: 800;
    font-size: 0.78rem;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}
.ev-step-content {
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--color-text);
}

/* ── Opportunity Grid ───────────────────────────────────────────────── */
.ev-opp-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}
@media (max-width: 800px) {
    .ev-opp-grid { grid-template-columns: 1fr; }
}
.ev-opp-card {
    background: var(--color-bg-elevated);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 1.2rem;
}
.ev-opp-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--color-accent);
    margin-bottom: 0.5rem;
}
.ev-opp-body {
    font-size: 0.88rem;
    line-height: 1.55;
    color: var(--color-text-muted);
}

/* ── Navigation Tabs ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.4rem !important;
    background-color: var(--color-bg-elevated) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.35rem !important;
    border: 1px solid var(--color-border) !important;
    margin-bottom: 1.25rem !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm) !important;
    color: var(--color-text-muted) !important;
    padding: 0.5rem 1.1rem !important;
    font-size: 0.86rem !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background-color: var(--color-bg-card) !important;
    color: var(--color-accent) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4) !important;
    border: 1px solid var(--color-border) !important;
}

/* Footer */
.ev-footer {
    text-align: center;
    padding: 3rem 0 1rem 0;
    border-top: 1px solid var(--color-border);
    margin-top: 4rem;
    font-size: 0.82rem;
    color: var(--color-text-subtle);
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PRESET SAMPLES
# ─────────────────────────────────────────────────────────────────────────────
SAMPLES = {
    "solar_irrigation": {
        "title": "🌾 Solar Irrigation (Faisalabad)",
        "claim": "A low-cost solar water pump can help smallholder farmers in Faisalabad reduce irrigation costs by over 40% while stabilizing crop yields.",
        "context": "Small wheat and sugarcane farms in peri-urban Punjab face surging diesel and electricity costs. Most farmers have less than 5 acres and rely on intermittent canal water supplemented by tubewells.",
        "sources": "https://www.agripunjab.gov.pk\nhttps://energypedia.info/wiki/Solar_Powered_Irrigation_Systems",
    },
    "ai_cold_outreach": {
        "title": "🤖 AI Lead Generation Tool",
        "claim": "Personalized cold emails generated by multimodal LLMs achieve a 3x higher response rate compared to static email templates for B2B SaaS.",
        "context": "Early-stage B2B software companies are testing agentic email outreach that analyzes prospect LinkedIn profiles and company blogs before writing outbound sequences.",
        "sources": "https://blog.hubspot.com/sales\nhttps://arxiv.org/abs/2303.17580",
    },
    "water_fluoridation": {
        "title": "💧 Water Fluoridation Health",
        "claim": "Artificial water fluoridation at optimal levels (0.7 mg/L) causes systemic neurodevelopmental harm in children.",
        "context": "Municipal public health guidelines vs recent toxicology meta-analyses discussing fluoride exposure thresholds and developmental milestones.",
        "sources": "https://www.cdc.gov/fluoridation/basics/\nhttps://ntp.niehs.nih.gov/whatwestudy/assessments/noncancer/completed/fluoride",
    },
}

DEMO_RESULT: dict[str, Any] = {
    "verdict": "Mixed",
    "confidence": 72,
    "one_line": "The idea is highly promising for operational cost-savings, but initial capital expenditure and groundwater monitoring are critical hurdles.",
    "claim_breakdown": [
        "40% operational expense reduction is plausible once high capital cost is subsidized or amortized.",
        "Yield stabilization is contingent on water table depth and localized solar radiation hours.",
        "Target user profile (sub-5 acre farmers) requires community sharing or flexible micro-financing.",
    ],
    "supporting_evidence": [
        {"point": "Solar tubewells eliminate recurrent diesel expenditure, which constitutes up to 35-50% of seasonal farming operational costs.", "source": "Energypedia Solar Irrigation Survey"},
        {"point": "Daytime solar generation aligns with peak evapotranspiration irrigation windows in Punjab summer seasons.", "source": "Punjab Agriculture Research Brief"},
        {"point": "Multimodal sensor monitoring can optimize pumping schedules and prevent pump burnout.", "source": "User-provided context"},
    ],
    "counter_evidence": [
        {"point": "Upfront system acquisition cost remains steep for smallholders without government subsidy or lease models.", "source": "Local Agri-Finance Assessment"},
        {"point": "Unregulated pumping risks rapid localized groundwater depletion if flow restrictors are omitted.", "source": "Water Resources Development Review"},
    ],
    "assumptions_and_gaps": [
        "Water table depth across Faisalabad sub-districts is within the 40-70 ft suction limit for standard DC pumps.",
        "Availability of local technician networks for inverter maintenance and solar panel cleaning.",
    ],
    "next_steps": [
        "Conduct structured interviews with 10 smallholder farmers in Faisalabad to establish diesel spend baselines.",
        "Partner with a local rural bank or microfinance institution to test a 12-month solar lease structure.",
        "Deploy a 1-acre proof of concept with a flow-meter to quantify exact kilowatt-hour vs diesel cost differences.",
    ],
    "opportunity": {
        "problem": "Unpredictable diesel prices and erratic power grids erode the thin margins of smallholder farmers.",
        "who_benefits": "Smallholder farmers (1-5 acres), rural cooperative societies, and local equipment distributors.",
        "prototype": "Pay-per-hour solar irrigation kit bundled with a lightweight mobile WhatsApp bot for irrigation scheduling.",
    },
}

SYSTEM_INSTRUCTION = """You are EvidenceLens, a rigorous research validation assistant.
Turn a user's claim into a useful decision brief. Separate what is known, uncertain, and
missing. Never invent a source, statistic, quote, or URL. If sources are provided, use only
those URLs as source references. Do not present medical, legal, or financial content as
professional advice. Be concise, balanced, and practical for a student, founder, or NGO.

Return valid JSON only with exactly these keys:
{
  "verdict": "Supported|Mixed|Unclear|Weakly supported|Refuted",
  "confidence": 0,
  "one_line": "...",
  "claim_breakdown": ["..."],
  "supporting_evidence": [{"point": "...", "source": "..."}],
  "counter_evidence": [{"point": "...", "source": "..."}],
  "assumptions_and_gaps": ["..."],
  "next_steps": ["..."],
  "opportunity": {"problem": "...", "who_benefits": "...", "prototype": "..."}
}
The confidence must be an integer from 0 to 100. Use "User-provided context" as the
source for information supplied by the user. If there is not enough evidence, say so.
"""

# ─────────────────────────────────────────────────────────────────────────────
# API CALL
# ─────────────────────────────────────────────────────────────────────────────
def _clean_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    res = json.loads(cleaned)
    if not isinstance(res, dict):
        raise ValueError("Model returned valid JSON but not an object dictionary.")
    return res


def analyze_claim(
    claim_val: str,
    context_val: str,
    sources_val: str,
    image_bytes: bytes | None,
    image_type: str | None,
    model_name: str,
) -> dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key in ("your_actual_api_key_here", "your_google_ai_studio_key_here"):
        raise RuntimeError("GEMINI_API_KEY is not configured in .env. Switch to Demo Mode or supply a valid key.")

    client = genai.Client(api_key=api_key)
    prompt = f"""Investigate this claim as of {date.today().isoformat()}.

CLAIM:
{claim_val}

USER CONTEXT:
{context_val or "No additional context was provided."}

SOURCE URLS PROVIDED BY USER:
{sources_val or "No source URLs were provided. Do not invent any citations."}

If an image is attached, interpret its visual evidence critically.
Return strictly the JSON object requested in the system instruction."""

    contents: list[Any] = [prompt]
    if image_bytes and image_type:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=image_type))

    use_json_mime = model_name.lower().startswith("gemini")
    config_kwargs: dict[str, Any] = {
        "system_instruction": SYSTEM_INSTRUCTION,
        "temperature": 0.2,
    }
    if use_json_mime:
        config_kwargs["response_mime_type"] = "application/json"

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=types.GenerateContentConfig(**config_kwargs),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    return _clean_json(response.text)


def as_markdown(claim_title: str, res: dict[str, Any]) -> str:
    lines = [
        f"# EvidenceLens Research Brief: {claim_title}",
        "",
        f"**Verdict:** {res.get('verdict', 'Unclear')}  ",
        f"**Calibrated Confidence:** {res.get('confidence', 0)}%  ",
        f"**Generated Date:** {date.today().isoformat()}",
        "",
        f"> {res.get('one_line', '')}",
        "",
        "## 1. Claim Breakdown",
        *[f"- {item}" for item in res.get("claim_breakdown", [])],
        "",
        "## 2. Supporting Evidence",
        *[f"- **{i.get('point', '')}** — *{i.get('source', '')}*" for i in res.get("supporting_evidence", [])],
        "",
        "## 3. Counter-Evidence & Risks",
        *[f"- **{i.get('point', '')}** — *{i.get('source', '')}*" for i in res.get("counter_evidence", [])],
        "",
        "## 4. Gaps to Resolve",
        *[f"- {item}" for item in res.get("assumptions_and_gaps", [])],
        "",
        "## 5. Recommended Next Steps",
        *[f"{idx}. {item}" for idx, item in enumerate(res.get("next_steps", []), 1)],
        "",
        "## 6. Startup Opportunity Canvas",
        f"- **Problem:** {res.get('opportunity', {}).get('problem', '')}",
        f"- **Who Benefits:** {res.get('opportunity', {}).get('who_benefits', '')}",
        f"- **Recommended Prototype:** {res.get('opportunity', {}).get('prototype', '')}",
        "",
        "---",
        "_Generated by EvidenceLens. Verify high-stakes claims with qualified subject-matter experts._",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────────────────────────────────────
api_key_configured = bool(os.getenv("GEMINI_API_KEY")) and os.getenv("GEMINI_API_KEY") not in (
    "your_actual_api_key_here", "your_google_ai_studio_key_here"
)

status_badge = (
    '<span class="ev-status-badge"><span class="ev-status-dot"></span> Gemini API Online</span>'
    if api_key_configured
    else '<span class="ev-status-badge" style="color:var(--color-highlight);border-color:rgba(240,177,88,0.32);background:var(--color-highlight-dim);"><span class="ev-status-dot" style="background:var(--color-highlight);box-shadow:0 0 8px var(--color-highlight);"></span> Offline Demo Mode</span>'
)

st.markdown(f"""
<div class="ev-nav">
    <div class="ev-brand">
        <div class="ev-logo-icon">🔬</div>
        <div>
            <div class="ev-brand-name">EvidenceLens</div>
            <div class="ev-brand-sub">Research Triage & Claim Validation</div>
        </div>
    </div>
    <div>
        {status_badge}
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ev-hero">
    <div class="ev-hero-badge">✦ MULTIMODAL CLAIM & HYPOTHESIS ANALYZER</div>
    <h1>Turn any claim into a clear,<br>validated research brief</h1>
    <p>Paste a startup hypothesis, academic thesis, or public claim. Attach evidence screenshots or source links to get a balanced verdict with supporting proofs, counter-arguments, and validation next steps.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE & PRESET CHIPS
# ─────────────────────────────────────────────────────────────────────────────
if "claim_text" not in st.session_state:
    st.session_state["claim_text"] = ""
if "context_text" not in st.session_state:
    st.session_state["context_text"] = ""
if "sources_text" not in st.session_state:
    st.session_state["sources_text"] = ""

st.markdown("""
<div style="text-align:center; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.09em; color:var(--color-text-subtle); margin-bottom:0.75rem;">
    Quick Sample Hypotheses
</div>
""", unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns([1, 1, 1])

with col_s1:
    if st.button("🌾 Solar Irrigation (Faisalabad)", key="btn_solar", use_container_width=True):
        st.session_state["claim_text"] = SAMPLES["solar_irrigation"]["claim"]
        st.session_state["context_text"] = SAMPLES["solar_irrigation"]["context"]
        st.session_state["sources_text"] = SAMPLES["solar_irrigation"]["sources"]
        st.rerun()

with col_s2:
    if st.button("🤖 AI Lead Generation Tool", key="btn_ai", use_container_width=True):
        st.session_state["claim_text"] = SAMPLES["ai_cold_outreach"]["claim"]
        st.session_state["context_text"] = SAMPLES["ai_cold_outreach"]["context"]
        st.session_state["sources_text"] = SAMPLES["ai_cold_outreach"]["sources"]
        st.rerun()

with col_s3:
    if st.button("💧 Water Fluoridation Health", key="btn_water", use_container_width=True):
        st.session_state["claim_text"] = SAMPLES["water_fluoridation"]["claim"]
        st.session_state["context_text"] = SAMPLES["water_fluoridation"]["context"]
        st.session_state["sources_text"] = SAMPLES["water_fluoridation"]["sources"]
        st.rerun()

st.write("")

# ─────────────────────────────────────────────────────────────────────────────
# TWO-COLUMN WORKBENCH
# ─────────────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.15], gap="large")

# ═════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN: INPUT DOSSIER (Rendered INSIDE a real card container)
# ═════════════════════════════════════════════════════════════════════════════
with col_left:
    with st.container(border=True):
        st.markdown("""
<div class="ev-card-heading">
    <span>📥 Input & Evidence Dossier</span>
    <span style="font-size:0.72rem;color:var(--color-text-subtle);font-weight:500;">Step 1 of 2</span>
</div>
""", unsafe_allow_html=True)

        claim_input = st.text_area(
            "Claim or hypothesis",
            value=st.session_state["claim_text"],
            placeholder="State the specific claim to validate (e.g. Solar tubewells in Faisalabad cut costs by 40%)...",
            height=105,
            help="Specify geography, target audience, and numbers for calibrated results.",
        )

        context_input = st.text_area(
            "Context & audience (optional)",
            value=st.session_state["context_text"],
            placeholder="Add audience profile, constraints, local variables, or preliminary notes...",
            height=85,
        )

        sources_input = st.text_area(
            "Reference URLs (one per line, optional)",
            value=st.session_state["sources_text"],
            placeholder="https://example.org/study-1\nhttps://data.worldbank.org/...",
            height=70,
        )

        uploaded_image = st.file_uploader(
            "Visual evidence or chart (optional)",
            type=["png", "jpg", "jpeg", "webp"],
            help="Multimodal analysis: inspects diagrams, data sheets, and charts directly.",
        )

        if uploaded_image:
            st.image(uploaded_image, caption="Attached Visual Evidence", use_container_width=True)

        with st.expander("⚙️ Inference Engine & Mode", expanded=False):
            mode_choice = st.radio(
                "Execution Mode",
                ["Gemini API", "Offline Demo Mode"],
                index=0 if api_key_configured else 1,
            )
            selected_model = st.selectbox(
                "AI Model Engine",
                ["gemini-2.5-flash", "gemma-4-31b-it", "gemini-2.5-pro", "gemini-flash-latest"],
                index=0,
                help="Gemini 2.5 Flash is recommended for sub-second multimodal responses.",
            )

        submit_button = st.button("Generate Decision Brief →", type="primary", use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# HANDLE FORM SUBMIT
# ═════════════════════════════════════════════════════════════════════════════
if submit_button:
    if not claim_input.strip():
        with col_left:
            st.error("Please enter a claim or select one of the sample hypotheses above.")
    else:
        with st.spinner("Analyzing hypothesis, checking counter-evidence, and calibrating verdict..."):
            try:
                if mode_choice == "Offline Demo Mode":
                    brief_result = DEMO_RESULT
                else:
                    brief_result = analyze_claim(
                        claim_val=claim_input.strip(),
                        context_val=context_input.strip(),
                        sources_val=sources_input.strip(),
                        image_bytes=uploaded_image.getvalue() if uploaded_image else None,
                        image_type=uploaded_image.type if uploaded_image else None,
                        model_name=selected_model,
                    )
                st.session_state["active_result"] = brief_result
                st.session_state["active_claim"] = claim_input.strip()
            except Exception as e:
                with col_right:
                    st.error(f"Validation failed: {e}")

# ═════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN: RESULTS WORKBENCH (Inside real card container)
# ═════════════════════════════════════════════════════════════════════════════
with col_right:
    active_res = st.session_state.get("active_result")
    active_claim_title = st.session_state.get("active_claim", "")

    if not active_res:
        with st.container(border=True):
            st.markdown("""
<div style="text-align: center; padding: 3.5rem 1rem;">
    <div style="width: 64px; height: 64px; background: rgba(95,181,143,0.12); border: 1px solid rgba(95,181,143,0.28); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; margin: 0 auto 1.25rem auto;">
        ⚖️
    </div>
    <div style="font-size: 1.25rem; font-weight: 700; color: var(--color-text); margin-bottom: 0.5rem; letter-spacing: -0.01em;">
        Awaiting Claim Analysis
    </div>
    <div style="font-size: 0.9rem; color: var(--color-text-muted); max-width: 440px; margin: 0 auto 2rem auto; line-height: 1.6;">
        Choose a quick sample above or state your hypothesis on the left. EvidenceLens will extract supporting proofs, counter-arguments, and validation next steps.
    </div>
    <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; font-size: 0.78rem; color: var(--color-text-subtle);">
        <span>✓ 100% Transparent Sources</span>
        <span>✓ Multimodal Chart Analysis</span>
        <span>✓ Actionable Next Steps</span>
    </div>
</div>
""", unsafe_allow_html=True)

    else:
        verdict = active_res.get("verdict", "Unclear")
        confidence = max(0, min(100, int(active_res.get("confidence", 0))))

        # Verdict Color Mapping
        verdict_color = {
            "Supported": "#5FB58F",
            "Weakly supported": "#8FA75D",
            "Mixed": "#F0B158",
            "Unclear": "#A87492",
            "Refuted": "#E27E62",
        }.get(verdict, "#A9A294")

        verdict_badge_bg = {
            "Supported": "rgba(95, 181, 143, 0.16)",
            "Weakly supported": "rgba(143, 167, 93, 0.16)",
            "Mixed": "rgba(240, 177, 88, 0.16)",
            "Unclear": "rgba(168, 116, 146, 0.16)",
            "Refuted": "rgba(226, 126, 98, 0.16)",
        }.get(verdict, "rgba(255, 255, 255, 0.08)")

        sup_count = len(active_res.get("supporting_evidence", []))
        con_count = len(active_res.get("counter_evidence", []))
        steps_count = len(active_res.get("next_steps", []))

        with st.container(border=True):
            st.markdown("""
<div class="ev-card-heading">
    <span>📊 Analysis Dashboard</span>
    <span style="font-size:0.72rem;color:var(--color-accent);font-weight:700;">● Live Result</span>
</div>
""", unsafe_allow_html=True)

            # ── 4 KPI Summary Cards ──────────────────────────────────
            st.markdown(f"""
<div class="ev-kpi-grid">
    <div class="ev-kpi-card">
        <div class="ev-kpi-title">Verdict</div>
        <div style="margin: 0.25rem 0;">
            <span style="background:{verdict_badge_bg}; color:{verdict_color}; border:1px solid {verdict_color}44; border-radius:9999px; padding:0.25rem 0.75rem; font-size:0.85rem; font-weight:700;">
                ● {verdict}
            </span>
        </div>
        <div class="ev-kpi-sub">Calibrated verdict</div>
    </div>
    <div class="ev-kpi-card">
        <div class="ev-kpi-title">Confidence</div>
        <div class="ev-kpi-value" style="color: {verdict_color};">{confidence}<span style="font-size: 1.1rem; color: var(--color-text-subtle);">%</span></div>
        <div class="ev-bar-bg">
            <div class="ev-bar-fill" style="width: {confidence}%; background-color: {verdict_color};"></div>
        </div>
    </div>
    <div class="ev-kpi-card">
        <div class="ev-kpi-title">Evidence Ratio</div>
        <div class="ev-kpi-value" style="color: #F8F5EE;">{sup_count}<span style="font-size: 1.15rem; color: var(--color-text-subtle);"> / </span>{con_count}</div>
        <div class="ev-kpi-sub">{sup_count} pros · {con_count} risks</div>
    </div>
    <div class="ev-kpi-card">
        <div class="ev-kpi-title">Roadmap</div>
        <div class="ev-kpi-value" style="color: var(--color-accent);">{steps_count}</div>
        <div class="ev-kpi-sub">Next action items</div>
    </div>
</div>
""", unsafe_allow_html=True)

            # ── Tabs ─────────────────────────────────────────────────
            tab_brief, tab_matrix, tab_opportunity, tab_raw = st.tabs([
                "📊 Executive Brief",
                "⚖️ Evidence Matrix",
                "💡 Opportunity Canvas",
                "📥 Export Markdown",
            ])

            # TAB 1: EXECUTIVE BRIEF
            with tab_brief:
                st.markdown(f"""
<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-text-subtle); margin-bottom: 0.5rem;">
    Executive Takeaway
</div>
<div class="ev-quote">
    <strong>“</strong>{active_res.get('one_line', '')}<strong>”</strong>
</div>

<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-text-subtle); margin: 1.25rem 0 0.6rem 0;">
    Claim Breakdown
</div>
""", unsafe_allow_html=True)

                for b in active_res.get("claim_breakdown", []):
                    st.markdown(f"""
<div style="background: var(--color-bg-elevated); border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: 0.65rem 0.95rem; margin-bottom: 0.5rem; font-size: 0.88rem; line-height: 1.5; color: var(--color-text);">
    • {b}
</div>
""", unsafe_allow_html=True)

                st.markdown("""
<div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-text-subtle); margin: 1.4rem 0 0.7rem 0;">
    Validation Roadmap
</div>
""", unsafe_allow_html=True)

                for idx, step in enumerate(active_res.get("next_steps", []), 1):
                    st.markdown(f"""
<div class="ev-step-row">
    <div class="ev-step-badge">{idx}</div>
    <div class="ev-step-content">{step}</div>
</div>
""", unsafe_allow_html=True)

            # TAB 2: EVIDENCE MATRIX
            with tab_matrix:
                col_m1, col_m2 = st.columns(2)

                with col_m1:
                    st.markdown("""
<div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-accent); margin-bottom: 0.75rem;">
    ✅ Supporting Evidence
</div>
""", unsafe_allow_html=True)
                    supporting_list = active_res.get("supporting_evidence", [])
                    if supporting_list:
                        for item in supporting_list:
                            st.markdown(f"""
<div class="ev-evidence-card">
    <div class="ev-evidence-point">
        <span style="color: var(--color-accent); font-weight: 800;">•</span>
        <span>{item.get('point', '')}</span>
    </div>
    <div class="ev-evidence-source">📎 {item.get('source', 'Context / Reference')}</div>
</div>
""", unsafe_allow_html=True)
                    else:
                        st.caption("No supporting evidence found.")

                with col_m2:
                    st.markdown("""
<div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-coral); margin-bottom: 0.75rem;">
    ⚠️ Counter-Evidence & Risks
</div>
""", unsafe_allow_html=True)
                    counter_list = active_res.get("counter_evidence", [])
                    if counter_list:
                        for item in counter_list:
                            st.markdown(f"""
<div class="ev-evidence-card">
    <div class="ev-evidence-point">
        <span style="color: var(--color-coral); font-weight: 800;">•</span>
        <span>{item.get('point', '')}</span>
    </div>
    <div class="ev-evidence-source">📎 {item.get('source', 'Risk Assessment')}</div>
</div>
""", unsafe_allow_html=True)
                    else:
                        st.caption("No counter-evidence reported.")

                # Information Gaps
                st.markdown("""
<div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-highlight); margin: 1.4rem 0 0.6rem 0;">
    ❓ Information Gaps & Unverified Assumptions
</div>
""", unsafe_allow_html=True)
                for gap in active_res.get("assumptions_and_gaps", []):
                    st.markdown(f"""
<div style="background: var(--color-bg-elevated); border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: 0.65rem 0.95rem; margin-bottom: 0.5rem; font-size: 0.88rem; color: var(--color-text-muted);">
    <span style="color: var(--color-highlight); margin-right: 0.4rem;">⚠️</span> {gap}
</div>
""", unsafe_allow_html=True)

            # TAB 3: OPPORTUNITY CANVAS
            with tab_opportunity:
                opp_data = active_res.get("opportunity", {})
                st.markdown(f"""
<div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-accent); margin-bottom: 0.8rem;">
    💡 Venture & Impact Framework
</div>
<div class="ev-opp-grid">
    <div class="ev-opp-card">
        <div class="ev-opp-label">Target Problem</div>
        <div class="ev-opp-body">{opp_data.get('problem', '—')}</div>
    </div>
    <div class="ev-opp-card">
        <div class="ev-opp-label">Primary Beneficiary</div>
        <div class="ev-opp-body">{opp_data.get('who_benefits', '—')}</div>
    </div>
    <div class="ev-opp-card">
        <div class="ev-opp-label">Recommended MVP</div>
        <div class="ev-opp-body">{opp_data.get('prototype', '—')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

            # TAB 4: EXPORT MARKDOWN
            with tab_raw:
                md_brief = as_markdown(active_claim_title, active_res)
                st.markdown("""
<div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-text-subtle); margin-bottom: 0.8rem;">
    📥 Download & Export
</div>
""", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Markdown Dossier (.md)",
                    data=md_brief,
                    file_name=f"evidencelens-{date.today().isoformat()}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
                st.text_area("Markdown Dossier Preview", value=md_brief, height=220)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ev-footer">
    EvidenceLens · Built for rigorous hypothesis validation and evidence synthesis.<br>
    Powered by Google Gemini 2.5 & Gemma · 100% transparent citations and verification.
</div>
""", unsafe_allow_html=True)
