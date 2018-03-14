# Tape_to_Tape
Use Python to prep and analyze data already exported and saved locally from the Tape to Tape tracking app

<b>Available:</b>
- parse_game.py, which contains a function that pulls and reformats exported plays files from tapetotapetracker.com
- plot_game_density_shots.py, which contains a function that generates a 2D density plot of a game's shot events overlaying a rink image
- plot_game_scatter_shots.py, which contains a function that generates a scatter plot of a game's shot events overlaying a rink image
- run_game_parse.py, which creates a season and game argument it passes through to parse_game.py
- run_game_plot.py, which creates a season and game argument it passes through to the plotting scripts

<b>To-Do:</b>

Statistics scripts:
- Players
- Teams

Visualization scripts:
- Shot Assists
- Zone Entries and Entry Assists
- Zone Exits and Exit Assists

<b>Set-Up</b>

If you wish to use the scripts as is, make sure to:

- Store the scripts within the root directory of your choosing (for example, I house everything within a desktop folder named 'Tape2Tape')
- Create a 'Files' folder within your root directory and then create both a 'Logs' subfolder and a separate 'Plots' subfolder within the 'Files' folder
- Within the 'Logs' subfolder, create both an 'Exported' subfolder as well as a 'Processed' subfolder and then, within both, create subfolders for each season (e.g. '20172018') you intend to work with  
- Within the 'Plots' subfolder, create subfolders for each season (e.g. '20172018') you intend to work with

<b>Usage</b>

Open your command line interface and, when running Python and in the proper directory, enter variations of the following:
- <code>python run_game_parse.py --season_ID 20172018 --game_ID 20570</code>
- <code>python run_game_plot.py --season_ID 20172018 --game_ID 20570</code>

<b>Notes:</b>

I've written and tested these scripts using the Spyder3 IDE with Python 3.5.4 installed as part of the Anaconda 2.5 distribution

Special thanks: 
- Muneeb Alam (@muneebalamcu)
- Prashanth Iyer (@iyer_prashanth)
- Christoper Knieste (@chrisknieste)
- Rushil Ram (@_rushil_)
