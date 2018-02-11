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

### creates a function with arguments to pass through from run_game_plot.py
def plot_game_scatter_shots(season_ID, game_ID):

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
    away_df_1st3rd_scored = game_df[(game_df['Event_Team'] == away_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Goal') & (game_df['Period'] != 2)]
    away_df_1st3rd_saved = game_df[(game_df['Event_Team'] == away_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Saved') & (game_df['Period'] != 2)]
    away_df_1st3rd_missed = game_df[(game_df['Event_Team'] == away_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Missed') & (game_df['Period'] != 2)]
    
    away_df_2nd_scored = game_df_2nd[(game_df_2nd['Event_Team'] == away_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Goal') & (game_df['Period'] == 2)]
    away_df_2nd_saved = game_df_2nd[(game_df_2nd['Event_Team'] == away_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Saved') & (game_df['Period'] == 2)]
    away_df_2nd_missed = game_df_2nd[(game_df_2nd['Event_Team'] == away_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Missed') & (game_df['Period'] == 2)]
    
    home_df_1st3rd_scored = game_df[(game_df['Event_Team'] == home_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Goal') & (game_df['Period'] != 2)]
    home_df_1st3rd_saved = game_df[(game_df['Event_Team'] == home_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Saved') & (game_df['Period'] != 2)]
    home_df_1st3rd_missed = game_df[(game_df['Event_Team'] == home_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Missed') & (game_df['Period'] != 2)]
    
    home_df_2nd_scored = game_df_2nd[(game_df_2nd['Event_Team'] == home_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Goal') & (game_df['Period'] == 2)]
    home_df_2nd_saved = game_df_2nd[(game_df_2nd['Event_Team'] == home_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Saved') & (game_df['Period'] == 2)]
    home_df_2nd_missed = game_df_2nd[(game_df_2nd['Event_Team'] == home_team) & (game_df['Event'] == 'Shot') & (game_df['Event_Detail'] == 'Missed') & (game_df['Period'] == 2)]
    
    ### Sets the color options
    away_color = '#c45f00'
    home_color = '#2988bc'
    miss_color = 'white'
    legend_color = 'black'
    colors = [away_color, home_color, miss_color, legend_color]
    
    ### Creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
    game_plot = game_df.plot.scatter(x='Event_X0', y='Event_Y0', zorder=0, marker='<', s=80, c='none', edgecolors='none', alpha=0);
    
    game_scored_plot = game_df.plot.scatter(x='Event_X0', y='Event_Y0', zorder=0, marker='^', s=60, c=colors[3], edgecolors='none', alpha=1, label='Scored', ax=game_plot);
    game_saved_plot = game_df.plot.scatter(x='Event_X0', y='Event_Y0', zorder=0, marker='s', s=40, c=colors[3], edgecolors='none', alpha=1, label='Saved', ax=game_plot);
    game_missed_plot = game_df.plot.scatter(x='Event_X0', y='Event_Y0', zorder=0, marker='o', s=40, c=colors[2], edgecolors='black', alpha=1, label='Missed', ax=game_plot);
    
    try:
        away_1st3rd_scored_plot = away_df_1st3rd_scored.plot.scatter(x='Event_X0', y='Event_Y0', zorder=2, marker='<', s=100, c=colors[0], edgecolors='white', alpha=1, ax=game_plot);
    except:
        pass
    try:
        away_1st3rd_saved_plot = away_df_1st3rd_saved.plot.scatter(x='Event_X0', y='Event_Y0', zorder=1, marker='s', s=40, c=colors[0], edgecolors=colors[0], alpha=0.25, ax=game_plot);
    except:
        pass
    try:
        away_1st3rd_missed_plot = away_df_1st3rd_missed.plot.scatter(x='Event_X0', y='Event_Y0', zorder=1, marker='o', s=40, c=colors[2], edgecolors=colors[0], alpha=0.5, ax=game_plot);
    except:
        pass

    try:
        away_2nd_scored_plot = away_df_2nd_scored.plot.scatter(x='Event_X0', y='Event_Y0', zorder=2, marker='<', s=100, color=colors[0], edgecolors='white', alpha=1, ax=game_plot);
    except:
        pass
    try:
        away_2nd_saved_plot = away_df_2nd_saved.plot.scatter(x='Event_X0', y='Event_Y0', zorder=1, marker='s', s=40, color=colors[0], edgecolors=colors[0], alpha=0.25, ax=game_plot);
    except:
        pass    
    try:
        away_2nd_missed_plot = away_df_2nd_missed.plot.scatter(x='Event_X0', y='Event_Y0', zorder=1, marker='o', s=40, color=colors[2], edgecolors=colors[0], alpha=0.5, ax=game_plot);
    except:
        pass  
  
    try:
        home_1st3rd_scored_plot = home_df_1st3rd_scored.plot.scatter(x='Event_X0', y='Event_Y0', zorder=2, marker='>', s=100, c=colors[1], edgecolors='white', alpha=1, ax=game_plot);
    except:
        pass
    try:
        home_1st3rd_saved_plot = home_df_1st3rd_saved.plot.scatter(x='Event_X0', y='Event_Y0', zorder=1, marker='s', s=40, c=colors[1], edgecolors=colors[1], alpha=0.25, ax=game_plot);
    except:
        pass
    try:
        home_1st3rd_missed_plot = home_df_1st3rd_missed.plot.scatter(x='Event_X0', y='Event_Y0', zorder=1, marker='o', s=40, c=colors[2], edgecolors=colors[1], alpha=0.5, ax=game_plot);
    except:
        pass

    try:
        home_2nd_scored_plot = home_df_2nd_scored.plot.scatter(x='Event_X0', y='Event_Y0', zorder=2, marker='>', s=100, color=colors[1], edgecolors='white', alpha=1, ax=game_plot);
    except:
        pass
    try:
        home_2nd_saved_plot = home_df_2nd_saved.plot.scatter(x='Event_X0', y='Event_Y0', zorder=1, marker='s', s=40, color=colors[1], edgecolors=colors[1], alpha=0.25, ax=game_plot);
    except:
        pass    
    try:
        home_2nd_missed_plot = home_df_2nd_missed.plot.scatter(x='Event_X0', y='Event_Y0', zorder=1, marker='o', s=40, color=colors[2], edgecolors=colors[1], alpha=0.5, ax=game_plot);
    except:
        pass  

    ### Sets the background image of what will be the plot to the 'rink_image.jpeg' file
    rink_img = plt.imread("rink_image.jpg")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

    ### Eliminates the axis labels
    plt.axis('off')

    ### Adds text boxes to indicate home and away sides
    plt.text(50, 45, home_team, color=colors[1], fontsize=12)
    plt.text(-3, 45, '@', color='black', fontsize=12)
    plt.text(-60, 45, away_team, color=colors[0], fontsize=12)

    ### Sets the plot title
    plt.title(season_ID + ' Game ' + game_ID + ' ' + date + '\nUnblocked Shots (All)\n')

    ### Sets the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

    ### Helps eliminate whitespace
    game_plot.axes.get_xaxis().set_visible(False)
    game_plot.axes.get_yaxis().set_visible(False)

    ### Renders the image from the data and image components
    plt.savefig('Files/Plots/' + season_ID +  '/' + season_ID + '_' + game_ID + '_shots.jpg', bbox_inches='tight', pad_inches=0.2)

    ### Displays message
    print('Finished scatter plot for: ' + season_ID + ' ' + game_ID)
