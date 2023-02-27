# Web scraping

## Description
A program for scraping information from Wikipedia, with a particular focus on the statistics of the players in the 2022 NBA playoffs and the FIS Alpine Ski World Cup.

### Get HTML
Gets the HTML from the provided url, with optional paramteres, and the option to save to file.

### Filter URLS
Uses the HTML to find all urls and changes them to a standard format. We can then find the urls of the articles and the images.

### Time planner
Creates markdown for a time table showing the date, venue, and type of winter sport.

### Fetch player statistics
Finds the statistics for the top 3 player in the 2022 NBA Playoffs, and creates a plot showing the three best players on each team.


## Instructions for installing
To run this program the python requests module and Beautiful Soup is required. Write the following in terminal to install:

`python3 -m pip install requests`

`python3 -m pip install beautifulsoup4`


## Instructions on running
Run tests in terminal by writing `pytest tests/test_FILENAME.py`, where filename is the file to be tested.



