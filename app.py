import streamlit as st
import pickle
import pandas as pd
st.title("IPL WIN PREDICTOR")

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Delhi Capitals',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Lucknow Super Giants',
 'Gujarat Titans',
]

cities = ['Jaipur', 'Mumbai', 'Delhi', 'Kolkata', 'Hyderabad', 'Chennai',
       'Centurion', 'Indore', 'Chandigarh', 'Cape Town', 'Ahmedabad',
       'Port Elizabeth', 'Sharjah', 'Cuttack', 'Bangalore',
       'Johannesburg', 'Visakhapatnam', 'Pune', 'Kimberley', 'Dharamsala',
       'Bengaluru', 'East London', 'Abu Dhabi', 'Lucknow', 'Bloemfontein',
       'Dubai', 'Durban', 'Navi Mumbai', 'Raipur', 'Ranchi', 'Guwahati',
       'Nagpur'
]

pipe = pickle.load(open('pipe.pkl','rb'))

col1,col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Select Batting Team : ",sorted(teams))
 
with col2:
    bowling_team = st.selectbox("Select Bowling Team : ",sorted(teams))

selected_city = st.selectbox("Select Host city",sorted(cities))

target = st.number_input("Enter Target Runs ")

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input("Score")

with col4:
    overs=st.number_input("Overs Completed")
    
with col5:
    wickets = st.number_input("Wickets Out")


import os

def safe_logo(team_name):
    path = f"logos/{team_name}.png"
    return path if os.path.exists(path) else "logos/default.png"



if st.button("Predict Probability"):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_data = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets_left],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr],
    })

    result = pipe.predict_proba(input_data)
    loss = result[0][0]
    win = result[0][1]

    # Flex-style display for both teams
    st.markdown("### 🏏 Match Win Prediction")

    col9, col10 = st.columns(2)

    with col9:
        team_logo = safe_logo(batting_team)
        st.image(team_logo, width=80)
        st.markdown(f"**{batting_team}**<br>Win Probability: **{round(win*100)}%**", unsafe_allow_html=True)

    with col10:
        team_logo = safe_logo(bowling_team)
        st.image(team_logo, width=80)
        st.markdown(f"**{bowling_team}**<br>Win Probability: **{round(loss*100)}%**", unsafe_allow_html=True)
