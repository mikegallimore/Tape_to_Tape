# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:41:23 2018

@author: Michael Gallimore (@mikegallimore)
"""

import parse_game
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--season_ID", dest="season_ID", required=False)
parser.add_argument("--game_ID", dest="game_ID", required=False)

args = parser.parse_args()

parse_game.parse_game(args.season_ID, args.game_ID)