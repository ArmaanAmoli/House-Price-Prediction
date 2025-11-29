import streamlit as st
import pandas as pd
import numpy as np
import joblib
from babel.numbers import format_currency

# ----------------- SIMPLE LIGHT THEME CSS ---------------------
st.markdown("""
<style>
    /* General body styling */
    .main {
        background-color: #f8f9fa;
        color: #212529;
    }
    
    /* Title styling */
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        border-bottom: 2px solid #3498db;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Container styling */
    .simple-box {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3498db;
    }
    
    /* Result box styling */
    .result-box {
        background-color: #e8f4fc;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3498db;
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
    }
    
    /* Subheader styling */
    .stSubheader {
        color: #2c3e50;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Slider styling */
    .stSlider {
        margin-bottom: 20px;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        margin-bottom: 10px;
    }
    
    /* Selectbox styling */
    .stSelectbox {
        margin-bottom: 20px;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Column styling */
    .column {
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- LOAD MODELS ---------------------
model = joblib.load('HousePricingModel.joblib')
Avg_Land_Price_per_sqft = joblib.load('Average_Land_Price_per_sqft.joblib')
mumbai = pd.read_csv("MumbaiMerged.csv")


def format_inr(amount):
    return format_currency(amount, 'INR', locale='en_IN')


# ----------------- TITLE ---------------------
st.markdown("<h1 class='main-title'>Mumbai House Price Estimator</h1>", unsafe_allow_html=True)


# ----------------- INPUT SECTION ---------------------
with st.container():
    st.markdown("<div class='simple-box'>", unsafe_allow_html=True)
    bhk = st.slider("Number of Bedrooms", 1, 4, 2)
    area = st.slider("Area in Square Feet", 300, 2000, 750, step=50)
    new = int(st.checkbox("New Property"))
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- FEATURES ---------------------
with st.container():
    st.markdown("<div class='simple-box'>", unsafe_allow_html=True)
    st.subheader("Additional Features")
    col1, col2 = st.columns(2)

    with col1:
        Gym = int(st.checkbox("Gym"))
        children_play_area = int(st.checkbox("Children Play Area"))
        club_house = int(st.checkbox("Club House"))
        indoor_games = int(st.checkbox("Indoor Games"))

    with col2:
        swimming_pool = int(st.checkbox("Swimming Pool"))
        jogging_trak = int(st.checkbox("Jogging Track"))
        garden = int(st.checkbox("Landscape Garden"))

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- AMENITIES ---------------------
with st.container():
    st.markdown("<div class='simple-box'>", unsafe_allow_html=True)
    st.subheader("Amenities")

    col3, col4 = st.columns(2)

    with col3:
        lift_aval = int(st.checkbox("Lift Available"))
        car_parking = int(st.checkbox("Car Parking"))
        Security = int(st.checkbox("24/7 Security"))

    with col4:
        Maintenance_staff = int(st.checkbox("Maintenance Staff"))
        Intercom = int(st.checkbox("Intercom"))

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------- LOCALITY ---------------------
localities = mumbai.columns[18::]
locality = st.selectbox("Choose your location", localities)
estimate = st.button("Estimate Price")

mumbai = mumbai.iloc[:, 2:]


# ----------------- PREDICTION ---------------------
if estimate:
    mumbai2 = pd.DataFrame(columns=mumbai.columns)
    input_list = [0] * len(mumbai.columns)

    input_list[0] = np.log(area)
    input_list[1] = bhk
    input_list[2] = new
    input_list[3] = Gym
    input_list[4] = lift_aval
    input_list[5] = car_parking
    input_list[6] = Maintenance_staff
    input_list[7] = Security
    input_list[8] = children_play_area
    input_list[9] = club_house
    input_list[10] = Intercom
    input_list[11] = garden
    input_list[12] = indoor_games
    input_list[13] = jogging_trak
    input_list[14] = swimming_pool
    input_list[15] = np.log(Avg_Land_Price_per_sqft[locality])

    for i, l in enumerate(mumbai.columns):
        if l == locality:
            input_list[i] = 1

    mumbai2.loc[len(mumbai2)] = input_list

    price = np.exp(model.predict(mumbai2)[0])

    import datetime
    current_year = datetime.date.today().year
    data_year = 2020

    while data_year < current_year:
        price += 0.15 * price
        data_year += 1

    st.markdown(f"<div class='result-box'>Estimated Price: ₹ {round(price):,}</div>", unsafe_allow_html=True)
