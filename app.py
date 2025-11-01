# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib

# from babel.numbers import format_currency

# def format_inr(amount):
#     # Format the amount as INR currency using the 'en_IN' locale
#     formatted_amount = format_currency(amount, 'INR', locale='en_IN')
#     return formatted_amount

# model = joblib.load('HousePricingModel.joblib')
# Avg_Land_Price_per_sqft = joblib.load('Average_Land_Price_per_sqft.joblib')

# mumbai = pd.read_csv("MumbaiMerged.csv")
# st.title("Mumbai House Price Estimator")
# #st.write("Mumbai House Price Estimator")
# bhk = st.slider("Number of Bedreeoms" , step=1 , min_value=1 , max_value=4)
# min = 300
# max = 2000
# area = st.slider("Area in SquareFt." , step=50 , min_value=min , max_value=max)
# #bhk = st.session_state.BHK
# new = int(st.checkbox('New Property'))
# st.header("Additional Features")
# st.write("Activities")
# Gym = int(st.checkbox("Gym"))
# children_play_area = int(st.checkbox("Children Play area"))
# club_house = int(st.checkbox("ClubHouse"))
# indoor_games = int(st.checkbox("Indoor Games"))
# swiming_pool = int(st.checkbox("Swimming Pool"))
# jogging_trak = int(st.checkbox("Jogging Track"))
# garden = int(st.checkbox("Landscape Garden"))

# st.write("Aminities")
# lift_aval = int(st.checkbox("Lift Availability"))
# car_parking = int(st.checkbox("Car Parking"))
# Security = int(st.checkbox("24/7 Security"))
# Maintenance_staff = int(st.checkbox("Maintenance Staff"))
# Intercom = int(st.checkbox("Intercom"))


# localities = mumbai.columns[18::]
# locality = st.selectbox("Choose your location" ,localities)
# estimate = st.button("Estimate")

# mumbai = mumbai.iloc[:: , 2::]

# #st.write(mumbai.columns)

# # '''
# # 'Area', 'No. of Bedrooms', 'New/Resale', 'Gymnasium',
# # 'Lift Available', 'Car Parking', 'Maintenance Staff', '24x7 Security',
# # 'Children's Play Area', 'Clubhouse', 'Intercom', 'Landscaped Gardens',
# # 'Indoor Games', 'Jogging Track', 'Swimming Pool',
# # 'Average_price_per_sq_ft'
# # '''
# if estimate:
#     mumbai2 = pd.DataFrame(columns=mumbai.columns)

#     input_list = [0]*len(mumbai.columns)
#     input_list[0] = np.log(area)
#     input_list[1] = bhk
#     input_list[2] = new
#     input_list[3] = Gym
#     input_list[4] =lift_aval
#     input_list[5] = car_parking
#     input_list[6] = Maintenance_staff
#     input_list[7] = Security
#     input_list[8] = children_play_area
#     input_list[9] = club_house
#     input_list[10] = Intercom
#     input_list[11] = garden
#     input_list[12] = indoor_games
#     input_list[13] = jogging_trak
#     input_list[14] = swiming_pool
#     input_list[15] = np.log(Avg_Land_Price_per_sqft[locality])
#     i = 0
#     for l in mumbai.columns:
#         if(l == locality):
#             input_list[i] =1 
#         i = i+1

#     #st.dataframe(mumbai2)
#     #st.write(input_list)
#     mumbai2.loc[len(mumbai2)] = input_list
#     st.success("₹ " + str(round(np.exp(model.predict(mumbai2)[0]))))
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from babel.numbers import format_currency

# ======= Custom Glassmorphism CSS =======
st.markdown("""
    <style>
    /* ====== Background Image Fullscreen ====== */
    [data-testid="stAppViewContainer"] {
        background: 
            linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.55)),
            url("https://images.unsplash.com/photo-1603262110263-fb3d0e0b9c53?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }

    /* ====== Remove default white areas ====== */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="stDecoration"], [data-testid="stMainBlockContainer"] > div {
        background: transparent !important;
    }

    /* ====== Centered Main Title ====== */
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1.2rem;
        text-shadow: 0 3px 8px rgba(0, 0, 0, 0.6);
    }

    /* ====== Transparent input fields ====== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.12);
        color: #ffffff;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.3);
        padding: 0.5rem;
    }

    /* ====== Sliders ====== */
    .stSlider > div > div > div > div {
        background: #3a86ff !important;
        height: 6px;
    }

    /* ====== Buttons ====== */
    .stButton button {
        width: 100%;
        background: #3a86ff;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        height: 2.8rem;
        transition: all 0.25s ease-in-out;
    }

    .stButton button:hover {
        background: #2563eb;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4);
    }

    /* ====== Result Box ====== */
    .result-box {
        font-size: 1.8rem;
        text-align: center;
        font-weight: 700;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
        padding: 20px;
        margin-top: 25px;
        color: #ffffff;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    }

    /* ====== Section Headings ====== */
    h2, .stSubheader {
        color: #ffffff !important;
        font-weight: 700;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
    }

    /* ====== Dropdowns ====== */
    div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.12) !important;
        color: #fff !important;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* ====== Remove extra padding ====== */
    section.main > div {
        padding-top: 1rem;
    }

    /* ====== Responsive tweaks ====== */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)





# ======= Load Models =======
model = joblib.load('HousePricingModel.joblib')
Avg_Land_Price_per_sqft = joblib.load('Average_Land_Price_per_sqft.joblib')
mumbai = pd.read_csv("MumbaiMerged.csv")

# ======= Helper =======
def format_inr(amount):
    return format_currency(amount, 'INR', locale='en_IN')

# ======= App Title =======
st.markdown("<h1 class='main-title'>🏙️ Mumbai House Price Estimator</h1>", unsafe_allow_html=True)

# ======= Input Section =======
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    bhk = st.slider("Number of Bedrooms", 1, 4, 2, step=1)
    area = st.slider("Area in Square Feet", 300, 2000, 750, step=50)
    new = int(st.checkbox("New Property"))
    st.markdown("</div>", unsafe_allow_html=True)

# ======= Additional Features =======
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🏋️ Additional Features")
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

# ======= Amenities =======
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🚪 Amenities")
    col3, col4 = st.columns(2)
    with col3:
        lift_aval = int(st.checkbox("Lift Available"))
        car_parking = int(st.checkbox("Car Parking"))
        Security = int(st.checkbox("24/7 Security"))
    with col4:
        Maintenance_staff = int(st.checkbox("Maintenance Staff"))
        Intercom = int(st.checkbox("Intercom"))
    st.markdown("</div>", unsafe_allow_html=True)

# ======= Locality =======
localities = mumbai.columns[18::]
locality = st.selectbox("📍 Choose your location", localities)
estimate = st.button("💰 Estimate Price")

mumbai = mumbai.iloc[:, 2:]

# ======= Prediction Logic =======
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

    # One-hot encode locality
    for i, l in enumerate(mumbai.columns):
        if l == locality:
            input_list[i] = 1

    mumbai2.loc[len(mumbai2)] = input_list

    price = np.exp(model.predict(mumbai2)[0])
    st.markdown(f"<div class='result-box'>🏠 Estimated Price: <br> ₹ {round(price):,}</div>", unsafe_allow_html=True)
