# Tape_to_Tape
Prep and analyze data exported from the Tape to Tape tracking app

<b>Available:</b>
- parse_game.py, which contains a function that pulls and reformats exported plays files from tapetotapetracker.com
- run_game.py, which creates a season and game argument it passes through to parse_game.py

<b>To-Do:</b>
- Script(s) for generating player and team statistics
- Script(s) for generating visualizations

<b>Before You Use:</b>
- If you wish to use the scripts as is, make sure to create a 'Files' folder within the directory the scripts are located in as well as both an 'Exported' and 'Processed' folder within the 'Files' folder

<b>Usage</b>
- Open your command line interface and, when running Python and in the proper directory, enter a variant of the following example:
- <code>python run_game.py --season_ID 20172018 --game_ID 20570</code>

<b>Note:</b>
- I've written and tested these scripts using the Spyder3 IDE with Python 3.5.4 installed as part of the Anaconda 2.5 distribution

Special Thanks:
- Muneeb Alam @muneebalamcu
- Christoper Knieste @chrisknieste
- Rushil Ram @_rushil_
