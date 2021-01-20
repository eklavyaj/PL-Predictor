import numpy as np
import pandas as pd
import pickle as p
import streamlit as st
import sklearn

def desc(HomeTeam, AwayTeam, winner):
    positions = pd.read_csv('csv_files/final_positions.csv')
    homeform = np.mean(positions['form'][positions['team']==HomeTeam])
    awayform = np.mean(positions['form'][positions['team']==AwayTeam])
    if((winner=='H') & ((homeform-awayform)>0)):
        team='Home'
        upset='No'
        homeadv='Yes'
    elif((winner=='H') & ((homeform-awayform)<0)):
        team='Home'
        upset='Yes'
        homeadv='Yes'
    elif((winner=='A') & ((homeform-awayform)>0)):
        team='Away'
        upset='Yes'
        homeadv='No'
    elif((winner=='A') & ((homeform-awayform)<0)):
        team='Away'
        upset='No'
        homeadv='No'
    elif((winner=='D') & (((homeform-awayform)>-0.15) & ((homeform-awayform)<0.15))):
        team = 'Draw'
        upset='No'
        homeadv='Neutral'
    elif((winner=='D') & ((homeform-awayform)>0.15)):
        team = 'Draw'
        upset='Yes'
        homeadv='No'
    elif((winner=='D') & ((homeform-awayform)<-0.15)):
        team = 'Draw'
        upset='Yes'
        homeadv='Yes'
    else:
        team = 'Draw'
        upset='Neutral'
        homeadv='Neutral'
    return [HomeTeam, AwayTeam, team, upset, homeadv]
    # print('{} vs. {} : {} \nUpset : {}\nHome Advantage : {}'.format())


def predict_winner(HomeTeam , AwayTeam , HTR):
    AllTeams = p.load(open('pickle_files/allteams.pickle', 'rb'))
    AllResults = p.load(open('pickle_files/allresults.pickle', 'rb'))

    rfc = p.load(open('pickle_files/final_predictions.pickle', 'rb'))
    hometeam = AllTeams[HomeTeam]
    awayteam = AllTeams[AwayTeam]
    htr = AllResults[HTR]
    case = np.array([hometeam,awayteam,htr])
    case = case.reshape(1,3)

    FTR = (rfc.predict(case))

    if(FTR == 1):
        return desc(HomeTeam , AwayTeam, 'D')
    elif (FTR == 0) :
        return desc(HomeTeam, AwayTeam , 'A')
    else :
        return desc(HomeTeam , AwayTeam , 'H')
        
def result(hteam, ateam, htime):

    [a, b, c, d, e] = predict_winner( hteam,ateam,htime)

    if htime == "H":
        output = a + " vs. " + b +" with the home team " + a + " winning at half time." 
    elif htime == "A":
        output = a + " vs. " + b +" with the away team " + b + " winning at half time." 
    elif htime == "D":
        output =  a + " vs. " + b + " with both teams tied at a half time."

    st.write(output)

    output = "Match ended "

    if c == "Home":
        output += "and the winner is the home team, " + hteam +"."
        st.write(output)

        if d == "Yes":
            output = "It is an upset."
        else:
            output = "It is not an upset."
        st.write(output)

        if e == "Yes":
            output = hteam + " exploited their home advantage."
        elif e == "No":
            output = hteam + " could not exploit their home advantage."
        else:
            output = "It was a tough match."
        st.write(output)

    elif c == "Away":
        output += "and the winner is the away team, " + ateam +"."
        st.write(output)

        if d == "Yes":
            output = "It is an upset."
        else:
            output = "It is not an upset."
        
        st.write(output)

        if e == "Yes":
            output = hteam + " exploited their home advantage."
        elif e == "No":
            output = hteam + " could not exploit their home advantage."
        else:
            output = "It was a tough match."
        st.write(output)
    
    elif c == "Draw":
        output += "in a draw."
        st.write(output)
        if d == "Yes":
            output = "It is an upset."
        else:
            output = "It is not an upset."
        st.write(output)

        if e == "Yes":
            output = hteam + " exploited their home advantage."
        elif e == "No":
            output = hteam + " could not exploit their home advantage."
        else:
            output = "It was a tough match."
        
        st.write(output)

    # return output

def main():
    st.title('Premier League Predictor')
    # choice = st.sidebar.radio('Select Action', ['Predictor'])

    with open('pickle_files/allteams.pickle', 'rb') as f:
        a = p.load(f)

    all_teams = list(a.keys())

    # if choice == 'Predictor':
    st.subheader('Enter Match Details')

    hteam = st.selectbox('Select Home Team', all_teams)

    all_teams2 = list(set(all_teams)- set(hteam))
    ateam = st.selectbox('Select Away Team', all_teams2)

    half_score = st.selectbox('Status at Half Time', ['Home Team', 'Away Team', 'Draw'])
    half_score = half_score[0]
    st.subheader('Result / Predictions')
    result(hteam, ateam, half_score)

if __name__ == '__main__':
    main()

