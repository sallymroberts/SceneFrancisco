# Scene Francisco
Learn more about developer Sally Roberts at <https://www.linkedin.com/in/sallymroberts>.

Scene Francisco is a full stack web application that uses data published by the San Francisco Film Commission about movies filmed in San Francisco, supplemented with movie poster images and additional information for each movie obtained from other sources. The application:
  - Displays a list of movies filmed in San Francisco
  - Has a dropdown list to subset the list by genre
  - Provides a text search for movies by title 
  - Displays a Google map of San Francisco with markers indicating filming locations for each movie, with the ability to see the description of the location by clicking the marker
  - Displays a movie poster image and information about the movie at the top of the page that displays the Google map
  - Provides a link to the Internet Movie Database (IMDB) page for each movie

### Table of contents
- [Why I selected this project](#Why)
- [Technology](#Technology)
- [Movie list page](#Movie list page)
- [Movie detail page with Google map](#Movie detail page with Google map)
- [Movie data from San Francisco Film Commission](#Movie data from San Francisco Film Commission)
- [Structure](#Structure)
- [Future enhancements](#Future enhancements)
- [Acknowledgments](#Acknowledgments)

### <a name="Why"></a>Why I selected this project
I have 12 years of experience as a software engineer designing, developing and maintaining backend business software and I wanted to consolidate my learning at the Hackbright Software Engineering Fellowship for Women by selecting an application requiring a fairly even balance of front-end and back-end development. I enjoy working with data and I wanted to practice something new by using Google maps, so I thought it would be fun to use the San Francisco Film Commission data to display a map identifying filming locations for movies. I love living in the Bay Area and watching movies with scenes displaying well-known San Francisco landmarks, which is a fun contrast to my experience growing up in Columbia, MO, a small Midwestern college town.

### Technology
Python, Flask, JavaScript, jQuery, AJAX, JSON, Jinja, HTML, CSS, Twitter Bootstrap, SQLite3, SQLAlchemy 

##### API's
- I retrieved the latitude and longitude associated with the San Francisco Film Commission location descriptions by using the Python Geocoder library (https://pypi.python.org/pypi/geocoder) to access the Google Maps API   
- I retrieved the Internet Movie Database (IMDB) ID's for each movie title using a function created by Johannes Bader to access the IMDB API (http://www.johannesbader.ch/2013/11/tutorial-download-posters-with-the-movie-database-api-in-python/). Note: the function is documented at the bottom of Bader's page, which primarily provides code to obtain movie poster images. 
- I retrieved a short plot description, genre list, and movie poster image URL for each movie by using the Open Movie Database (OMDB) API (http://www.omdbapi.com/). I used the Internet Movie Database (IMDB) ID's (see above) to identify movies for the OMDB API.

##### Dependencies
Dependencies are listed in requirements.txt

### Movie list page
![image](https://raw.githubusercontent.com/sallymroberts/SceneFrancisco/master/static/images/movie_list_screen_shot.png)

### Movie detail page with Google map
![image](https://raw.githubusercontent.com/sallymroberts/SceneFrancisco/master/static/images/movie_detail_screen_shot.png)

### Movie data from San Francisco Film Commission
View public dataset published by the San Francisco Film Commission at: https://data.sfgov.org/Culture-and-Recreation/Film-Locations-in-San-Francisco/yitu-d5am
![image](https://raw.githubusercontent.com/sallymroberts/SceneFrancisco/master/static/images/SanFranciscoFilmCommissionData.png)

### Structure

##### Python files

###### Application server: server.py
Core of the flask app, processes all routes.

###### Data model: model.py
Defines the SQLite3 data model for the application and connects the SQLite3 database to the flask app using SQLAlchemy.

###### Convert seed data: seed.py
Converts the seed data provided by the San Francisco Film Commission in JSON format to the SQLite3 data model. The seed data contains information about movies filmed in San Francisco, including movie title, release year, filming locations, production company, distributor, director, writer(s), and actors. 

###### Retrieve and clean up data: update_tables.py
Contains many functions to retrieve additional data about the movies and to clean up the data, including:
  - Use the Internet Movie Database (IMDB) API to retrieve the IMDB ID associated with each movie title. Use that IMDB ID to build the URL for the IMDB page for each movie. Load the IMDB ID and IMDB URL to the Movies table.
  - A Google map requires the latitude and longitude identifying a location to display a marker on a map. I used the Python Geocoder function to access the Google API to retrieve the latitude and longitude associated with the location description provided by the San Francisco Film Commission, and loaded the latitude and longitude for each filming location to the Movie locations table.
  - The Internet Movie Database (IMDB) does not provide API’s to access most of the information about movies available on their site. The Open Movie Database (OMDB) provides an API to obtain movie data. I used the OMDB API to obtain the IMDB poster image URL, genre, and plot description and loaded this data to the Movies table.
  - Set the movie image URL to Null (None in Python) for movie poster URL’s retrieved using the Open Movie Database (OMDB) API that had the value “N/A”.
  - Download the Internet Movie Database (IMDB) movie poster images to respect IMDB’s desire to reduce impact on their servers by blocking hot-linking access to these images, which I encountered in my initial attempt to display these images on the movie detail page.
  - Update the Movies table with a reformatted title for movies beginning with “The “ and “A “ to facilitate listing the movies in alphabetical order. For example, I reformatted “The Bachelor” to “Bachelor, The”. In the app server.py file, I reformatted these titles to display the original title on the Movie detail page.
  - Update the Movies table with the correct Internet Movie Database (IMDB) ID for 33 IMDB ID’s incorrectly identified by the IMDB API for which I manually identified the correct IMDB ID. In most cases, the incorrect ID’s were for movies with similar or identical titles.
  - Update the Movies table with the correct title for 13 movies for which I manually identified the correct title while researching Internet Movie Database (IMDB) ID’s
  - Update the Movies table with the correct release year for 16 movies for which I manually identified the correct release year while researching Internet Movie Database (IMDB) ID’s.

##### Templates and Style Sheets

###### base.html
Contains base HTML and JavaScript used by other templates, including basic HTML tags, blocks, and JavaScript to provide access to Twitter Bootstrap, a CSS style sheet, Google Merriweather fonts, JavaScript for Google maps API’s, and jQuery.

###### movie_list.html
Contains HTML, JavaScript, Jinja, JQuery, and Twitter bootstrap used together with the CSS style sheet to display a list of movies filmed in San Francisco with input fields to subset the list by genre, search by title, and refresh the list. 

###### movie_detail.html
Contains HTML, JavaScript, Jinja, JQuery and Twitter bootstrap used together with the CSS style sheet to display information about each movie, an image of the movie poster, and a Google map with markers for filming locations for the movie. 

###### scenefranciso.css
Contains CSS referencing classes and ID’s defined in the HTML templates, to style the appearance of the text, input forms, links, and table containing the movie list.

### Future enhancements

##### Top filming locations page
I want to add a page to display a Google map with markers to identify the top filming locations in San Francisco, with info windows for each marker identifying the movies that were filmed at that location. To satisfy my curiosity, I performed an SQLite3 query of the Movie locations table to identify the top filming locations. The filming locations associated with 8 or more movies (sorted by number of movies) include:
- Golden Gate Bridge (27)
- City Hall (21)
- Fairmont Hotel (18)
- Chinatown (10)
- Coit Tower (10)
- St. Peter & Paul’s Church (10)
- Treasure Island (10)
- Alcatraz Island (8)
- Bay Bridge (8)
- Golden Gate Park (8)
- Grace Cathedral (8)

##### Automated testing
I have extensive experience defining and executing test plans as an essential part of the process of developing business software. I would like to add Python doctest's and unittests to my application to enjoy the benefits of automated testing:
- Reduced risk of introducing bugs while maintaining an application and refactoring code to make it clearer and more maintainable
- Clear definition of expected functionality, including edge cases 

##### Identify latitude and longitude for additional movie locations 
A Google map requires the latitude and longitude identifying a location to display a marker on a map. I used the Google maps API to identify the latitude and longitude associated with the location descriptions provided by the San Francisco Film Commission. For about 15% of the descriptions, the Google maps API was unable to identify the specific location, and returned the generic latitude and longitude for San Francisco. I listed these location descriptions on the movie detail page, without displaying markers on the map.

I would like to create an automated process to reformat the location descriptions in order to use the Google maps API to return a specific latitude and longitude. These location descriptions are written in a variety of ways, so this is a significant task to automate.  Several typical examples include:
- Cala Foods (California Street and Hyde)
- Columbus Avenue at Green & Stockton
- Geary St. from Polk to Larkin
- Grant between Bush and Market
- Epic Roasthouse

##### Search and subset movie list 
The current version accepts user input to subset the list by genre and to search by title (or partial title). I would like to add options to:
- Subset the list by director
- Subset the list by decades, based on release year
- Subset the list to only display movies for which there is a map with markers displaying filming locations. For about 20% of the movies, the San Francisco Film Commission data does not provide any specific filming locations.

##### Data cleanup 
I did a lot of data cleanup for this project (see description of update_tables.py under Python files in Structure section for details), and I would like to also:
- Correct the spelling of misspelled actor, writer and director names
- Correct the spelling of misspelled street names and location names
- Delete a few duplicate location descriptions for the same movie.

### Acknowledgments
In addition to the support of my husband and fellow Hackbright fellows, the following people were instrumental to the project, providing mentorship, inspiration, and guidance:

##### Hackbright Instructors
- Heather Bryant
- Joel Burton
- Cynthia Dueltgen 
- Lavinia Karl 
- Katie LeFevre 
- Meggie Mahnken
- Rachel Thomas 
- Denise Wiedl

##### Mentors
- Raina Carter 
- Mark Griffith
- Erik Vande Kieft