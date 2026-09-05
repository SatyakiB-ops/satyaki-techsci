import streamlit as st
import base64
from pathlib import Path
from datetime import date, timedelta

from agents import travel_coordinator

APP_NAME = "MeraSafar"
APP_TAGLINE = "Skip the suffer and plan your safar.Your AI travel companion making every journey worth it"
BACKGROUND_IMAGE_URL = "https://images.stockcake.com/public/8/6/6/8666fbed-77b0-4637-8322-0f621becff21_large/sunset-road-trip-stockcake.jpg"
LOGO_PATH = Path(__file__).parent / "logo.svg"

st.set_page_config(page_title=APP_NAME, page_icon="🧭", layout="centered")

logo_base64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(10, 15, 30, 0.55), rgba(10, 15, 30, 0.75)),
            url("{BACKGROUND_IMAGE_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        background: rgba(255, 255, 255, 0.28);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.35);
        padding: 2.5rem 2.5rem 2rem 2.5rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    }}

    h1, .app-tagline, label, p, span {{
        color: #1a1a1a !important;
        text-shadow: none;
    }}

    h1 {{
        font-weight: 800;
        letter-spacing: -0.5px;
    }}

    .app-tagline {{
        font-size: 1.05rem;
        margin-top: -0.6rem;
        margin-bottom: 1.5rem;
    }}

    .stTextInput input, .stNumberInput input, .stDateInput input {{
        background: rgba(255, 255, 255, 0.9) !important;
        color: #111 !important;
        border-radius: 8px !important;
    }}

    button[kind="formSubmit"], .stButton > button, .stFormSubmitButton > button {{
        background-color: #1f6feb !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.4rem !important;
        border: none !important;
    }}

    button[kind="formSubmit"]:hover, .stButton > button:hover, .stFormSubmitButton > button:hover {{
        background-color: #1558c0 !important;
        color: #ffffff !important;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 0.2rem;">
        <img src="data:image/svg+xml;base64,{logo_base64}" width="52" height="52" />
        <h1 style="margin: 0;">{APP_NAME}</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f'<p class="app-tagline">{APP_TAGLINE}</p>',
    unsafe_allow_html=True,
)

with st.form("trip_form"):
    destination = st.text_input("Destination", placeholder="e.g. Switzerland")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=date.today() + timedelta(days=30))
    with col2:
        end_date = st.date_input("End date", value=date.today() + timedelta(days=37))

    budget = st.number_input("Budget per person (USD)", min_value=0, value=5000, step=100)
    origin = st.text_input("Flying from (origin city)", placeholder="e.g. Kolkata")
    travelers = st.number_input("Number of travelers", min_value=1, value=2)
    interests = st.text_input(
        "Interests",
        placeholder="e.g. technology, culture, food, temples, modern attractions",
    )

    submitted = st.form_submit_button("Plan my trip")

if submitted:
    if not destination:
        st.error("Please enter a destination.")
    elif end_date <= start_date:
        st.error("End date must be after start date.")
    else:
        num_days = (end_date - start_date).days

        query = f"""
        Plan a {num_days}-day trip to {destination} starting {start_date}, ending {end_date}.
        Budget: ${budget} per person (including flights from {origin})
        Interests: {interests}
        Travel group: {travelers} adults

        Please provide:
        1. Day-by-day detailed itinerary with attractions and timings
        2. Complete flight and hotel recommendations with costs
        3. Weather forecast and packing recommendations
        4. Restaurant recommendations for different cuisines
        5. Local tips, safety information, and cultural customs
        6. Transportation options and estimated costs
        7. Budget breakdown and money-saving tips
        8. Booking recommendations and travel warnings
        """

        with st.spinner("Planning your trip... this can take a minute or two."):
            try:
                response = travel_coordinator.run(query)
                st.markdown(response.content)
            except Exception as e:
                st.error(f"Something went wrong while planning your trip: {e}")