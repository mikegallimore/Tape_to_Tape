# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:41:23 2018

@author: Michael Gallimore (@mikegallimore)
"""

import csv
import pandas as pd
import requests
from datetime import datetime

### creates a function with arguments to pass through from run_game_parse.py
def parse_game(season_ID, game_ID):

    ### Creates variables that identify the exported plays and rosters as downloaded from tapetotapetracker.com
    ### If the filepath is left as is, make sure to create a 'Files' folder with an 'Exported' subfolder
    in_plays = 'files/logs/exported/' + season_ID + '/' + season_ID[:4] + '0' + game_ID + '_plays.csv'
    roster = 'files/logs/exported/' + season_ID + '/' + season_ID[:4] + '0' + game_ID + '_roster.csv'

    ### Trims the roster information in a dataframe before converting into a dict
    roster_df = pd.read_csv(roster, usecols = ['playerId', 'fullName'])
    roster_dict = dict(roster_df.values)

    ### Creates a variable that indicates the .csv file the information generated by this script will be stored in
    ### If the filepath is left as is, make sure to create a 'Processed' subfolder within the 'Files' folder
    out_plays = 'files/logs/processed/' + season_ID + '/' + season_ID + '_' + game_ID + '_processed.csv'

    with open(out_plays, 'w', newline='') as fileout:
        csvWriter = csv.writer(fileout)
        with open(in_plays, 'r') as filein:
            csvReader = list(csv.reader(filein))

            ### creates the header row of the cleaned-up file to be written out
            csvWriter.writerow(['Season_ID', 'Game_ID', 'Date', 'Home_Team', 'Away_Team', 'Period', 'Time_Elapsed', 'Time_Remaining', 'Home_ScoreDiff', 'Away_ScoreDiff', 'Home_Situation', 'Away_Situation', 'Event_Team', 'Event', 'Event_Detail', 'Event_Type', 'Event_Result', 'Event_Player0', 'Event_X0', 'Event_Y0', 'Event_Player1', 'Event_X1', 'Event_Y1', 'Assist0_Team', 'Assist0_Result', 'Assist0_Player0', 'Assist0_X0', 'Assist0_Y0', 'Assist0_Player1', 'Assist0_X1', 'Assist0_Y1', 'Assist1_Team', 'Assist1_Result', 'Assist1_Player0', 'Assist1_X0', 'Assist1_Y0', 'Assist1_Player1', 'Assist1_X1', 'Assist1_Y1', 'Assist2_Team', 'Assist2_Result', 'Assist2_Player0', 'Assist2_X0', 'Assist2_Y0', 'Assist2_Player1', 'Assist2_X1', 'Assist2_Y1', 'Assist3_Team', 'Assist3_Result', 'Assist3_Player0', 'Assist3_X0', 'Assist3_Y0', 'Assist3_Player1', 'Assist3_X1', 'Assist3_Y1', 'Assist4_Team', 'Assist4_Result', 'Assist4_Player0', 'Assist4_X0', 'Assist4_Y0', 'Assist4_Player1', 'Assist4_X1', 'Assist4_Y1', 'Event_ID', 'Linked_Events', 'Event_Tags', 'HomeOn_0', 'HomeOn_1', 'HomeOn_2', 'HomeOn_3', 'HomeOn_4', 'HomeOn_5', 'AwayOn_0', 'AwayOn_1', 'AwayOn_2', 'AwayOn_3', 'AwayOn_4', 'AwayOn_5'])
        
            ### creates the variables (which must be outside the for loop below) that will serve the event-by-event counter for each team
            HomeGoals = int(0)
            AwayGoals = int(0)

            ### begin looping through the exported plays file
            for row in csvReader[1:]:
            
                ### separates and adjusts the value of the season from the 'eventId' column in the exported plays file
                source_eventID = row[19] 
                seasongamenumber = source_eventID[:10]       
                season_first = seasongamenumber[:4]
                season_last = int(season_first) + 1
                season = str(season_first) + str(season_last)
                
                ### creates a gameID variable from the the previously split 'eventId' column in the exported plays file           
                gamenumber = str(seasongamenumber[5:])            
                
                ### extracts some game information from the league's json file which corresponds to the gameID
                json_url = "http://statsapi.web.nhl.com/api/v1/game/" + season_first + "0" + gamenumber + "/feed/live"            
                process_json = requests.get(json_url)
                decoded_json = process_json.json()
                
                date = decoded_json["gameData"]["datetime"]["dateTime"].split('T')[0]
                date = datetime.strftime(datetime.strptime(date, '%Y-%m-%d'), '%m/%d/%Y') # format conversion
                date = str(date)
                
                home_team = decoded_json["gameData"]["teams"]["home"]["triCode"]
                away_team = decoded_json["gameData"]["teams"]["away"]["triCode"]
                
                ### connects a variable to the 'Period' column in the exported plays file
                period = row[0]
                
                ### creates a new variable (event_detail) and connects others to the 'event', 'eventType', 'eventResult' and 'eventTeam' columns in the exported plays file
                event_team = row[18]
                
                event = row[15]
                event_detail = str()     

                if event == 'Goal':
                    event = 'Shot'
                    event_detail = 'Goal'
                elif event == 'Shot':
                    event = 'Shot'
                    event_detail = 'Saved'
                elif event == 'Missed Shot':
                    event = 'Shot'
                    event_detail = 'Missed'
                elif event == 'Blocked Shot':
                    event = 'Shot'
                    event_detail = 'Blocked'
                elif event == 'Zone Entry':
                    event = 'Entry'
                elif event == 'Zone Exit':
                    event = 'Exit'
                
                event_type = row[16]
            
                if event_type == 'Slap Shot':
                    event_type = 'Slap'
                elif event_type == 'Snap Shot':
                    event_type = 'Snap'
                elif event_type == 'Tip-In':
                    event_type = 'Tip'
                elif event_type == 'Wrist Shot':
                    event_type = 'Wrist'
                
                event_result = row[17]

                event_player0 = row[24]
                event_x0 = row[20]
                event_y0 = row[21]

                event_player1 = row[25]
                event_x1 = row[22]
                event_y1 = row[23]

                event_tags = row[66]

                # get the number of goals scored by the home and away team
                if event_detail == 'Goal' and event_team == home_team:
                    HomeGoals += 1
                elif event_detail == 'Goal' and event_team == away_team:
                    AwayGoals += 1

                # split the combined score state into distinct home and away goals scored differentials
                HomeScoreDiff = int(HomeGoals) - int(AwayGoals)
                AwayScoreDiff = int(AwayGoals) - int(HomeGoals)

                if event_detail == 'Goal' and event_team == home_team:
                    HomeScoreDiff = HomeScoreDiff - 1
                    AwayScoreDiff = AwayScoreDiff + 1
                elif event_detail == 'Goal' and event_team == away_team:
                    HomeScoreDiff = HomeScoreDiff + 1
                    AwayScoreDiff = AwayScoreDiff - 1

                # determine the home and away score situations
                if int(HomeScoreDiff) == int(AwayScoreDiff):
                    HomeSituation = 'Tied'
                    AwaySituation = 'Tied'
                elif int(HomeScoreDiff) > int(AwayScoreDiff):
                    HomeSituation = 'Leading'
                    AwaySituation = 'Trailing'
                elif int(HomeScoreDiff) < int(AwayScoreDiff):
                    HomeSituation = 'Trailing'
                    AwaySituation = 'Leading'

                ### connects variables to the various 'pass' columns in the exported plays file
                assist0_team = row[31]
                assist0_result = row[30]
                assist0_player0 = row[32]
                assist0_x0 = row[26]
                assist0_y0 = row[27]
                assist0_player1 = row[33]
                assist0_x1 = row[28]
                assist0_y1 = row[29]
            
                assist1_team = row[39]
                assist1_result = row[38]
                assist1_player0 = row[40]
                assist1_x0 = row[34]
                assist1_y0 = row[35]
                assist1_player1 = row[41]
                assist1_x1 = row[36]
                assist1_y1 = row[37]
            
                assist2_team = row[47]
                assist2_result = row[46]
                assist2_player0 = row[48]
                assist2_x0 = row[42]
                assist2_y0 = row[43]
                assist2_player1 = row[49]
                assist2_x1 = row[44]
                assist2_y1 = row[45]

                assist3_team = row[55]
                assist3_result = row[54]
                assist3_player0 = row[56]
                assist3_x0 = row[50]
                assist3_y0 = row[51]
                assist3_player1 = row[57]
                assist3_x1 = row[52]
                assist3_y1 = row[53]
            
                assist4_team = row[63]
                assist4_result = row[62]
                assist4_player0 = row[64]
                assist4_x0 = row[58]
                assist4_y0 = row[59]
                assist4_player1 = row[65]
                assist4_x1 = row[60]
                assist4_y1 = row[61]
           
                ### connects variables to the 'eventID' and 'linkedEvents' columns in the exported plays file
                event_ID = row[19].replace('20170'+str(gamenumber)+'_', '')
                linked_events = row[67].replace('20170'+str(gamenumber)+'_', '')

                ### gets counts of the number of home player columns from the exported plays file to arrive at a home strength value
                HomeOn_0 = row[9]
                HomeOn_1 = row[10]
                HomeOn_2 = row[11]
                HomeOn_3 = row[12]
                HomeOn_4 = row[13]
                HomeOn_5 = row[14]
                        
                AwayOn_0 = row[3]
                AwayOn_1 = row[4]
                AwayOn_2 = row[5]
                AwayOn_3 = row[6]
                AwayOn_4 = row[7]
                AwayOn_5 = row[8]
         
                ### connects variables to the 'PeriodTime' and 'PeriodTimeRemaining' columns in the exported plays file
                time_elapsed = row[1]
                time_remaining = row[2]            
 
                ### uses the exported roster file to convert the playerIDs within the exported plays file to player names
                try:
                    event_player0 = roster_dict[int(event_player0)].replace(' ', '.')
                except:
                    pass
                try:
                    event_player1 = roster_dict[int(event_player1)].replace(' ', '.')
                except:
                    pass

                try:
                    assist0_player0 = roster_dict[int(assist0_player0)].replace(' ', '.')
                except:
                    pass
                try:
                    assist0_player1 = roster_dict[int(assist0_player1)].replace(' ', '.')
                except:
                    pass
                try:
                    assist1_player0 = roster_dict[int(assist1_player0)].replace(' ', '.')
                except:
                    pass
                try:
                    assist1_player1 = roster_dict[int(assist1_player1)].replace(' ', '.')
                except:
                    pass
                try:
                    assist2_player0 = roster_dict[int(assist2_player0)].replace(' ', '.')
                except:
                    pass
                try:
                    assist2_player1 = roster_dict[int(assist2_player1)].replace(' ', '.')
                except:
                    pass
                try:
                    assist3_player0 = roster_dict[int(assist3_player0)].replace(' ', '.')
                except:
                    pass
                try:
                    assist3_player1 = roster_dict[int(assist3_player1)].replace(' ', '.')
                except:
                    pass
                try:
                    assist4_player0 = roster_dict[int(assist4_player0)].replace(' ', '.')
                except:
                    pass
                try:
                    assist4_player1 = roster_dict[int(assist4_player1)].replace(' ', '.')
                except:
                    pass
            
                try:
                    HomeOn_0 = roster_dict[int(HomeOn_0)].replace(' ', '.')
                except:
                    pass
                try:
                    HomeOn_1 = roster_dict[int(HomeOn_1)].replace(' ', '.')
                except:
                    pass
                try:
                    HomeOn_2 = roster_dict[int(HomeOn_2)].replace(' ', '.')
                except:
                    pass
                try:
                    HomeOn_3 = roster_dict[int(HomeOn_3)].replace(' ', '.')
                except:
                    pass
                try:
                    HomeOn_4 = roster_dict[int(HomeOn_4)].replace(' ', '.')
                except:
                    pass
                try:
                    HomeOn_5 = roster_dict[int(HomeOn_5)].replace(' ', '.')
                except:
                    pass

                try:
                    AwayOn_0 = roster_dict[int(AwayOn_0)].replace(' ', '.')
                except:
                    pass
                try:
                    AwayOn_1 = roster_dict[int(AwayOn_1)].replace(' ', '.')
                except:
                    pass
                try:
                    AwayOn_2 = roster_dict[int(AwayOn_2)].replace(' ', '.')
                except:
                    pass
                try:
                    AwayOn_3 = roster_dict[int(AwayOn_3)].replace(' ', '.')
                except:
                    pass
                try:
                    AwayOn_4 = roster_dict[int(AwayOn_4)].replace(' ', '.')
                except:
                    pass
                try:
                    AwayOn_5 = roster_dict[int(AwayOn_5)].replace(' ', '.')
                except:
                    pass

                ### creates sequences to insert and write out
                game_info = [season, gamenumber, date, home_team, away_team]
                event_info = [period, time_elapsed, time_remaining, HomeScoreDiff, AwayScoreDiff, HomeSituation, AwaySituation, event_team, event, event_detail, event_type, event_result, event_player0, event_x0, event_y0, event_player1, event_x1, event_y1]
                assist0_info = [assist0_team, assist0_result, assist0_player0, assist0_x0, assist0_y0, assist0_player1, assist0_x1, assist0_y1]
                assist1_info = [assist1_team, assist1_result, assist1_player0, assist1_x0, assist1_y0, assist1_player1, assist1_x1, assist1_y1]
                assist2_info = [assist2_team, assist2_result, assist2_player0, assist2_x0, assist2_y0, assist2_player1, assist2_x1, assist2_y1]
                assist3_info = [assist3_team, assist3_result, assist3_player0, assist3_x0, assist3_y0, assist3_player1, assist3_x1, assist3_y1]
                assist4_info = [assist4_team, assist4_result, assist4_player0, assist4_x0, assist4_y0, assist4_player1, assist4_x1, assist4_y1]
                identifiers = [event_ID, linked_events, event_tags]
                home_players = [HomeOn_0, HomeOn_1, HomeOn_2, HomeOn_3, HomeOn_4, HomeOn_5]
                away_players = [AwayOn_0, AwayOn_1, AwayOn_2, AwayOn_3, AwayOn_4, AwayOn_5]
            
                ### writes out the plays in the adjusted format
                csvWriter.writerow(game_info + event_info + assist0_info + assist1_info + assist2_info + assist3_info + assist4_info + identifiers + home_players + away_players)
    
    ### Displays message
    print('Finished parsing exported plays to create new "processed" file: ' + season_ID + ' ' + game_ID)