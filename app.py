import os
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageFilter, ImageStat

st.set_page_config(page_title="BuildWise AI | Construction Intelligence", page_icon="🏗️", layout="wide")

st.markdown("""
<style>
.main {background: #f7f9fc;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#142b4a,#176b87); color: white; margin-bottom: 1rem;}
.hero h1 {color: white; margin-bottom: .3rem;}
.small-note {color: #5d6b7a; font-size: .88rem;}
div[data-testid="stMetric"] {background:white; border:1px solid #e4eaf1; padding:14px; border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🏗️ BuildWise AI</h1><p>Multimodal Construction Intelligence Platform</p><p>One workspace for visual site review, preliminary cost planning, weather-aware advisories and construction Q&A.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.title("Project Workspace")
    page = st.radio("Navigate", ["Overview", "Image Analysis", "Cost Estimator", "Weather Advisory", "AI Site Assistant"])
    st.divider()
    st.caption("Prototype • Human review required")
    st.caption("No image classifier is claimed unless a trained model is configured.")

def image_metrics(image):
    """Return explainable image heuristics; not a trained PPE/crack detector."""
    img = image.convert("RGB")
    arr = np.asarray(img, dtype=np.float32)
    gray = np.asarray(img.convert("L"), dtype=np.float32)
    edges = img.convert("L").filter(ImageFilter.FIND_EDGES)
    edge_mean = float(ImageStat.Stat(edges).mean[0])
    brightness = float(gray.mean())
    contrast = float(gray.std())
    return {"width": img.width, "height": img.height, "brightness": brightness, "contrast": contrast, "edge_activity": edge_mean}

def advisory_for_weather(rain, temp, wind):
    notes = []
    if rain >= 60:
        notes.append("High rain chance: review excavation stability, drainage, concrete pours and material protection.")
    elif rain >= 30:
        notes.append("Moderate rain chance: protect cement and aggregates; confirm the pour plan with the site engineer.")
    else:
        notes.append("Lower rain chance: still verify the latest local forecast before outdoor work.")
    if temp >= 38:
        notes.append("High temperature: plan hydration, shade, suitable work-rest cycles and concrete curing.")
    elif temp <= 5:
        notes.append("Low temperature: ask the engineer about cold-weather concrete procedures and worker protection.")
    if wind >= 40:
        notes.append("Strong wind: assess lifting operations, scaffolds and unsecured materials; follow site stop-work rules.")
    notes.append("This is a planning aid, not a live weather forecast or a substitute for the site's safety officer.")
    return notes

if page == "Overview":
    st.subheader("Project overview")
    a, b, c, d = st.columns(4)
    a.metric("Modules", "4")
    b.metric("Analysis mode", "Image heuristics")
    c.metric("Cost plan", "Editable inputs")
    d.metric("Assistant", "Guided Q&A")
    st.markdown("### What you can do")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Image-based review**\n\nUpload a construction-site image to inspect image quality and edge/texture indicators. These indicators do not identify PPE or diagnose structural cracks.")
        st.info("**Construction cost planning**\n\nEstimate a preliminary budget from quantities, unit rates, contingency and tax.")
    with col2:
        st.info("**Weather-aware advisory**\n\nEnter a forecast you already have to receive general work-planning reminders.")
        st.info("**Site assistant**\n\nAsk common planning questions or configure an optional Gemini API key in your hosting secrets.")
    st.warning("Safety-critical outputs must be verified by qualified site personnel. This educational prototype must not be used as a certified inspection system.")

elif page == "Image Analysis":
    st.subheader("Image-based construction review")
    st.write("Upload a photo of a site, worker PPE, or a wall/surface. The current version reports image characteristics only; it does not claim to detect helmets, vests, or structural defects.")
    upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])
    if upload:
        try:
            image = Image.open(upload)
            st.image(image, caption="Uploaded image", use_container_width=True)
            metrics = image_metrics(image)
            x, y, z = st.columns(3)
            x.metric("Image dimensions", f'{metrics["width"]} × {metrics["height"]}')
            y.metric("Brightness", f'{metrics["brightness"]:.1f}/255')
            z.metric("Contrast", f'{metrics["contrast"]:.1f}')
            st.metric("Edge activity (heuristic)", f'{metrics["edge_activity"]:.1f}/255')
            st.caption("Higher edge activity can come from texture, objects, or image noise; it is not a crack severity score.")
            st.download_button("Download image review report", pd.DataFrame([metrics]).to_csv(index=False), file_name="image_review_report.csv", mime="text/csv")
            st.markdown("**Human review checklist**")
            st.checkbox("A qualified reviewer checked whether required PPE is visible.")
            st.checkbox("A qualified reviewer assessed any suspected surface crack.")
            st.checkbox("The image is sufficiently clear and shows the relevant area.")
        except Exception as exc:
            st.error(f"Could not read this image: {exc}")
    else:
        st.info("Choose an image to begin.")

elif page == "Cost Estimator":
    st.subheader("Preliminary construction cost estimator")
    st.write("Enter project quantities and local rates. Defaults are examples only—not market quotations.")
    with st.form("cost_form"):
        col1, col2 = st.columns(2)
        with col1:
            area = st.number_input("Built-up area (sq ft)", min_value=0.0, value=1000.0, step=50.0)
            rate = st.number_input("Base construction rate (₹ / sq ft)", min_value=0.0, value=1800.0, step=100.0)
            extras = st.number_input("Additional works / materials (₹)", min_value=0.0, value=50000.0, step=5000.0)
        with col2:
            contingency_pct = st.slider("Contingency (%)", 0, 30, 10)
            tax_pct = st.slider("Tax / fees allowance (%)", 0, 30, 0)
            project_label = st.text_input("Project label", value="Sample project")
        submitted = st.form_submit_button("Calculate estimate", type="primary")
    if submitted:
        base = area * rate + extras
        contingency = base * contingency_pct / 100
        fees = (base + contingency) * tax_pct / 100
        total = base + contingency + fees
        st.markdown("### Estimate summary")
        m1, m2, m3 = st.columns(3)
        m1.metric("Base cost", f"₹{base:,.0f}")
        m2.metric("Contingency", f"₹{contingency:,.0f}")
        m3.metric("Indicative total", f"₹{total:,.0f}")
        breakdown = pd.DataFrame([
            {"Item": "Area × base rate", "Amount (₹)": area * rate},
            {"Item": "Additional works / materials", "Amount (₹)": extras},
            {"Item": "Contingency", "Amount (₹)": contingency},
            {"Item": "Tax / fees allowance", "Amount (₹)": fees},
            {"Item": "Indicative total", "Amount (₹)": total},
        ])
        st.dataframe(breakdown, use_container_width=True, hide_index=True)
        st.download_button("Download estimate (CSV)", breakdown.to_csv(index=False), file_name="construction_cost_estimate.csv", mime="text/csv")
        st.caption(f"Project: {project_label}. Validate quantities, specifications, local rates and applicable taxes with a qualified estimator.")

elif page == "Weather Advisory":
    st.subheader("Weather-aware site planning")
    st.write("This module does not fetch live weather. Enter values from a trusted local forecast.")
    col1, col2, col3 = st.columns(3)
    with col1:
        rain = st.slider("Chance of rain (%)", 0, 100, 20)
    with col2:
        temp = st.number_input("Temperature (°C)", min_value=-20.0, max_value=60.0, value=30.0, step=1.0)
    with col3:
        wind = st.number_input("Wind speed (km/h)", min_value=0.0, max_value=200.0, value=15.0, step=5.0)
    if st.button("Generate advisory", type="primary"):
        for note in advisory_for_weather(rain, temp, wind):
            st.write("• " + note)

elif page == "AI Site Assistant":
    st.subheader("Construction planning assistant")
    st.write("Ask a general construction planning question. For AI-generated answers, add a Gemini API key in your Streamlit app secrets.")
    question = st.text_area("Your question", placeholder="Example: What should a site team check before a concrete pour?")
    if st.button("Get guidance", type="primary", disabled=not question.strip()):
        api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        if api_key:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=("You are a cautious construction planning assistant. Give general, practical guidance, "
                              "state assumptions, and direct safety-critical decisions to qualified site engineers. "
                              "Do not claim to certify structural safety. User question: " + question)
                )
                st.markdown(response.text or "No response was returned.")
            except Exception as exc:
                st.error("The AI service could not respond. Check the API key, model availability and network settings.")
                st.caption(str(exc))
        else:
            q = question.lower()
            if any(word in q for word in ["concrete", "pour", "curing"]):
                answer = "Before a concrete pour, confirm approved drawings and mix, formwork stability, reinforcement placement and cover, embedded services, access, equipment, weather, testing arrangements and the engineer's sign-off. Follow the project method statement and local codes."
            elif any(word in q for word in ["ppe", "helmet", "safety", "worker"]):
                answer = "Use the site's approved risk assessment and PPE matrix. Check fit and condition of helmets, high-visibility clothing, footwear, eye/hand protection and task-specific equipment. A qualified safety officer should verify compliance; this app does not detect PPE automatically."
            elif any(word in q for word in ["crack", "wall", "structural"]):
                answer = "Photograph the area with a scale and location reference, record when it was noticed and whether it is changing, and restrict access if there may be immediate danger. Arrange prompt assessment by a qualified structural engineer. Do not rely on an image-only app to judge structural safety."
            elif any(word in q for word in ["cost", "budget", "estimate"]):
                answer = "Use measured quantities and current local supplier/labour rates, state inclusions and exclusions, include contingencies transparently, and have a qualified estimator review the result. Try the Cost Estimator module for an editable preliminary calculation."
            else:
                answer = "Start with the latest approved drawings, scope, method statement, site risk assessment and local requirements. Record assumptions, assign an accountable reviewer, and escalate safety-critical or structural questions to qualified professionals. Add a Gemini API key to enable generated responses."
            st.info(answer)
            st.caption("Rule-based guidance shown because no Gemini API key is configured.")

st.divider()
st.caption("BuildWise AI • Academic prototype • " + datetime.now().strftime("%Y"))
st.caption("Important: Not a certified safety, structural-diagnostic, engineering, or quantity-surveying tool.")
