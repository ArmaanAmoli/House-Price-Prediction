import streamlit as st
import pandas as pd
import numpy as np
import joblib
from babel.numbers import format_currency

# ----------------- SIMPLE LIGHT THEME CSS ---------------------
st.markdown("""
<style>
body {
    background-color: #ffffff;
}

[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
    font-family: 'Inter', sans-serif;
    color: #1f2937;
}

/* Clean title */
.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 1rem;
}

/* Simple input sections */
.simple-box {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 8px;
    margin-bottom: 20px;
}

/* Clean button */
.stButton button {
    width: 100%;
    background: #2563eb;
    color: white;
    border-radius: 6px;
    border: none;
    height: 2.6rem;
}

.stButton button:hover {
    background: #1d4ed8;
}

/* Simple result box */
.result-box {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 8px;
    text-align: center;
    font-size: 1.4rem;
    font-weight: 600;
    margin-top: 20px;
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
