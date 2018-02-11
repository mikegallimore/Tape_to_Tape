# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:41:23 2018

@author: Michael Gallimore (@mikegallimore)
"""

import parse_game
import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument("--season_ID", dest="season_ID", required=False)
parser.add_argument("--game_ID", dest="game_ID", required=False)

args = parser.parse_args()

### passes the arguments through to parse_game.py
parse_game.parse_game(args.season_ID, args.game_ID)

### to run this program, open your Python command prompt and make sure you're working out of the proper directory
### in the console, enter the run_game.py file with season and game arguments 
### example: python run_game.py --season_ID 20172018 --game_ID 20570