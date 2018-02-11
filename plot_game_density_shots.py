# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:41:23 2018

@author: Michael
"""
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### creates a function with arguments to pass through from run_game_plot.py
def plot_game_density_shots(season_ID, game_ID):

    ### extracts some game information from the league's json file which corresponds to the gameID
    json_url = "http://statsapi.web.nhl.com/api/v1/game/" + season_ID[0:4] + "0" + game_ID + "/feed/live"            
    process_json = requests.get(json_url)
    decoded_json = process_json.json()

    ### Creates home and away team variables from the dataframe created from the particular game log set to game_file
    home_team = decoded_json["gameData"]["teams"]["home"]["triCode"]
    away_team = decoded_json["gameData"]["teams"]["away"]["triCode"]

    ### Procures and stores the date 
    date = decoded_json["gameData"]["datetime"]["dateTime"].split('T')[0]
    date = datetime.strftime(datetime.strptime(date, '%Y-%m-%d'), '%m/%d/%Y') # format conversion
    date = str(date)

    ### Creates a variable that points to the .csv file that you need to have generated previously by running process_game.py for the particular game identified by the 'set_game' variable
    game_file = 'Files/Logs/Processed/' + season_ID + '/' + season_ID + '_' + game_ID + '_processed.csv'
    
    ### Creates a dataframe object that reads in info from the .csv file that should already be generated by previously running process_game.py for the particular game identified by the 'set_game' variable
    game_df = pd.read_csv(game_file)
    game_df_2nd = pd.read_csv(game_file)
    game_df_2nd['Event_X0'] *= -1
    game_df_2nd['Event_Y0'] *= -1

    ### Establishes distinct subsets of the overall dataframe for home and away events
    away_df_1st3rd = game_df[(game_df['Event_Team'] == away_team) & (game_df['Event'] == 'Shot')  & (game_df['Event_Detail'] != 'Blocked') & (game_df['Period'] != 2)]
    away_df_2nd = game_df_2nd[(game_df_2nd['Event_Team'] == away_team) & (game_df['Event'] == 'Shot')  & (game_df['Event_Detail'] != 'Blocked') & (game_df['Period'] == 2)]
    away_df_all = pd.concat([away_df_1st3rd, away_df_2nd])
    
    home_df_1st3rd = game_df[(game_df['Event_Team'] == home_team) & (game_df['Event'] == 'Shot')  & (game_df['Event_Detail'] != 'Blocked') & (game_df['Period'] != 2)]
    home_df_2nd = game_df_2nd[(game_df_2nd['Event_Team'] == home_team) & (game_df['Event'] == 'Shot')  & (game_df['Event_Detail'] != 'Blocked') & (game_df['Period'] == 2)]
    home_df_all = pd.concat([home_df_1st3rd, home_df_2nd])
    
    ### Sets the color options
    away_color = '#c45f00'
    home_color = '#2988bc'
    
    ### Styles the plot
    sns.set_style("white")
    
    ### Constructs 2D density plot
    away_plot = sns.kdeplot(away_df_all.Event_X0, away_df_all.Event_Y0, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.8, cmap='Reds')
    
    home_plot = sns.kdeplot(home_df_all.Event_X0, home_df_all.Event_Y0, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.8, cmap='Blues')
    
    ### Sets the background image of what will be the plot to the 'rink_image.jpeg' file
    rink_img = plt.imread("rink_image.jpg")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### Eliminates the axis labels
    plt.axis('off')
    
    ### Adds text boxes to indicate home and away sides
    plt.text(50, 45, home_team, color=home_color, fontsize=12)
    plt.text(-3, 45, '@', color='black', fontsize=12)
    plt.text(-60, 45, away_team, color=away_color, fontsize=12)
    
    ### Sets the plot title
    plt.title(season_ID + ' Game ' + game_ID + ' ' + date + '\nUnblocked Shots (All)\n')
    
    ### Sets the plots axis limits
    plt.xlim(-100,100)
    plt.ylim(-42.5,42.5)
    
    ### Helps eliminate whitespace
    away_plot.axes.get_xaxis().set_visible(False)
    away_plot.get_yaxis().set_visible(False)
    
    ### Shows plot
    plt.savefig('Files/Plots/' + season_ID + '/' + season_ID + '_' + game_ID + '_density.jpg', bbox_inches='tight', pad_inches=0.2)
    
    ### Displays message
    print('Finished density plot for: ' + season_ID + ' ' + game_ID)
