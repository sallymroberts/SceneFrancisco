# Scene Francisco
Learn more about developer Sally Roberts at <https://www.linkedin.com/in/sallymroberts>.

Check out Scene Francisco at <https://scenefrancisco.herokuapp.com/>.

Scene Francisco is a full stack web application that uses data published by the San Francisco Film Commission about movies filmed in San Francisco, supplemented with movie poster images and additional information for each movie obtained from other sources. The application:
  - Displays a list of movies filmed in San Francisco
  - Has a dropdown list to subset the list by genre
  - Provides a text search for movies by title 
  - Displays a Google map of San Francisco with markers indicating filming locations for each movie, with the ability to see the description of the location by clicking the marker
  - Displays a movie poster image and information about the movie at the top of the page that displays the Google map
  - Provides a link to the Internet Movie Database (IMDB) page for each movie

### Table of contents
- [Problem and Solution: Why I selected this project](#Why)
- [Movie list page](#List)
- [Movie detail page with Google map](#Map)
- [Movie data from San Francisco Film Commission](#FilmData)
- [Technology and Technical Choices](#Technology)
- [Structure](#Structure)
- [Future enhancements](#Future)
- [Acknowledgments](#Acknowledgments)

### <a name="Why"></a>Problem and Solution: Why I selected this project 
I developed this solo 4-week capstone project during the [Hackbright Academy](http://www.hackbrightacademy.com/) Summer 2015 fellowship. While I have a preference for backend development and 12 years of experience as a software engineer designing, developing and maintaining backend business software, I selected an application requiring a fairly even balance of front-end and back-end development in order to practice full stack development. I like working with data and I wanted to practice something new by using Google maps, so I thought it would be fun to use the San Francisco Film Commission data to display a map identifying filming locations for movies. I love living in the Bay Area and watching movies with scenes displaying well-known San Francisco landmarks, which is an enjoyable contrast to my experience growing up in a small Midwestern college town.  

I wanted to use my project to consolidate learning the full stack web development technology introduced during the first 5 weeks of the Hackbright fellowship, so that was a primary factor in my technical choices. I started by defining and populating a data model in SQLite3, using the San Francisco Film Commission data as my primary data source, supplemented by several API's to get additional data for each movie and the latitude and longitude for each movie filming location. I developed a 2-page web application (see screen shots below) using Flask for the web framework, Python for the backend, SQLAlchemy to access the data, and HTML, JavaScript, JQuery, Jinja, CSS and Twitter Bootstrap for the front-end. The summary at the top of the README describes the front-end functionality.   

### <a name="List"></a>Movie list page
![image](https://raw.githubusercontent.com/sallymroberts/SceneFrancisco/master/static/images/movie_list_screen_shot.png)

### <a name="Map"></a>Movie detail page with Google map
![image](https://raw.githubusercontent.com/sallymroberts/SceneFrancisco/master/static/images/movie_detail_screen_shot.png)

### <a name="FilmData"></a>Movie data from San Francisco Film Commission
This is the public dataset published by the San Francisco Film Commission that I used as the primary source of data for my application. Click https://data.sfgov.org/Culture-and-Recreation/Film-Locations-in-San-Francisco/yitu-d5am to view this data.
![image](https://raw.githubusercontent.com/sallymroberts/SceneFrancisco/master/static/images/SanFranciscoFilmCommissionData.png)

### <a name="Technology"></a>Technology and Technical Choices
#### Stack
Python, Flask, JavaScript, jQuery, AJAX, JSON, Jinja, HTML, CSS, Twitter Bootstrap, SQLite3, SQLAlchemy 

#### Dependencies
Dependencies are listed in requirements.txt

#### Defining and Populating the Data Model

###### Files associated with the data model
  - movie_seed.json is the San Francisco Film Commission data (seed data)
  - model.py defines the application data model (sf_movies.db) and connects the data model to the Flask app
  - seed.py loads the San Francisco Film Commission data into the application data model
  - update_tables.py contains functions to update the data model, which were created and run on an ad hoc basis throughout the project. Several functions access API's to retrieve additional data about each movie and the movie locations, and other functions clean up the data.

###### Downloading the San Francisco Film Commission dataset
The primary source of data was the SF Film Commission public dataset, which identifies movies filmed in San Francisco and the locations within San Francisco where the movies were filmed. It can be downloaded in a variety of formats, including Comma Separated Values (CSV) and JavaScript Object Notation (JSON).  I considered using the Python CSV module to process the data in CSV format, which provides functionality for distinguishing between commas used to separate data values and commas that are part of the data, for example. However, I chose to download the San Francisco Film Commission data in JSON format because it is a more standard data format for API’s and is easier to process because it clearly identifies and defines the data elements. 

###### Defining the Data Model
There are 5 tables in the Data Model:
 - The Movies table identifies basic information about each movie. Director id is a foreign key to the Directors table and the primary key is an auto-incremented integer for movie id.
 - The Directors table identifies director names and the primary key is an auto-incremented integer for director id.
 - The Actors table identifies actor names and the primary key is an auto-incremented integer for actor id. The San Francisco Film Commission data identified 0 to 3 actors per movie, in Actor 1, Actor 2, and Actor 3 columns.
 - The Movie Locations table has one row per filming location for each movie. It has columns for location description from the San Francisco Film Commission data, and latitude and longitude obtained using the Google maps API. The primary key is an auto-incremented integer for location id and movie id is a foreign key to the Movies table. A relationship is defined linking the Movies and Movie Locations tables to facilitate querying the data.
 - Movie Actors is used as an association table to link the Movies table with the Actors table in a many to many relationship, using columns for actor id and movie id as foreign keys and the primary key is an auto-incremented integer for movie actor id. Relationships are defined linking the Actors and Movie Actors tables and the Movies and Movie Actors tables to facilitate querying the data.

###### Normalizing the data

For a production application, I would usually choose to fully normalize the data for clarity, integrity, and ease of maintenance. However, I chose to make exceptions for the initial version of the data model. I did not normalize the locations due to time constraints and fairly messy data that would require time-consuming cleanup and research in order to clearly define unique locations. The Movies table contains columns for production company, writers, and distributors, which I loaded directly from the San Francisco Film Commission data for each movie instead of normalizing the data as I did for actors and directors. Creating normalized tables would have required data cleanup first to identify unique values and I planned to simply display the writers on the movie detail page and did not expect to use the production company and distributors in the initial version of the application, so I chose not to normalize this data.

###### Retrieving additional data using API's 
- Google maps require the latitude and longitude in order to display markers on the map for each location. I retrieved the latitude and longitude associated with the San Francisco Film Commission location descriptions by using the Python Geocoder library (https://pypi.python.org/pypi/geocoder) to access the Google Maps API.    
- I wanted to provide a link to the Internet Movie Database (IMDB) web page for each movie. The URL for the IMDB web page for a movie can be constructed from the IMDB ID, so I retrieved the Internet Movie Database (IMDB) ID's for each movie title using a function created by Johannes Bader to access the IMDB API (http://www.johannesbader.ch/2013/11/tutorial-download-posters-with-the-movie-database-api-in-python/). Note: the function is documented at the bottom of Bader's page, which primarily provides code to obtain movie poster images. 
- I wanted to display additional information and a movie poster image for each movie on the movie detail page. The Internet Movie Database (IMDB) does not provide API’s to access most of the information about movies available on their site. I used the Open Movie Database (OMDB) API to obtain the IMDB poster image URL, genre, and plot description, identifying the movies using the IMDB ID.
- I downloaded the Internet Movie Database (IMDB) movie poster images to respect IMDB’s desire to reduce impact on their servers by blocking hot-linking access to these images, which I encountered in my initial attempt to display these images on the movie detail page. 

#### Displaying the map and markers on the map

A Google map requires the latitude and longitude identifying a location to display a marker on a map. I used the Google maps API to identify the latitude and longitude associated with the location descriptions provided by the San Francisco Film Commission. For about 15% of the descriptions, the Google maps API was unable to identify the specific location, and returned the generic latitude and longitude for the center of San Francisco. I decided to list these location descriptions at the top of the movie detail page, instead of including these locations with markers using the generic latitude and longitude for San Francisco, because that is not a meaningful location for the marker.

As a future enhancement, I would like to create an automated process to reformat the location descriptions in order to use the Google maps API to return a specific latitude and longitude for more of these locations. These location descriptions are written in a variety of ways, so this is a significant task to automate.  Several typical examples include:
- Cala Foods (California Street and Hyde)
- Columbus Avenue at Green & Stockton
- Geary St. from Polk to Larkin
- Grant between Bush and Market
- Epic Roasthouse

#### Web Interface / Appearance

I wanted the screen interface and appearance to be understandable, easy to use, and attractive. Choices I made to implement this included: 
- I used Twitter Bootstrap, a popular front-end framework, to provide standard and attractive formatting for the web pages 
- To add visual interest, I selected a photo of the Golden Gate Bridge for use at the top of the movie list page and obtained movie poster images to display on the movie detail page
- I worked on making the page layouts clear, grouped components logically, and gave meaningful descriptive names to input fields used to search and subset the list on the movie list page
- My first attempt to use a text-shadow effect to make the page title on the movie list page readable and attractive against the Golden Gate Bridge photo background was not very successful. I asked another fellowship participant with substantial frontend experience for suggestions and she pointed me to a web page with sample code developed by Tom Elliot to create a "sharper glow" text shadow effect. I spent a while playing around with this effect, selecting various color combinations, fonts, and font sizes, until I achieved a result that worked well. 

### <a name="Structure"></a>Structure

##### Python files

###### Application server: server.py
Core of the flask app, processes all routes.

###### Data model: model.py
Defines the SQLite3 data model for the application and connects the SQLite3 database to the flask app using SQLAlchemy.

###### Convert seed data: seed.py
Converts the San Francisco Film Commission seed data in JSON format, identifying movies filmed in San Francisco and the locations where each movie was filmed, to the SQLite3 data model.  

###### Unit tests: tests.py
Contains unit tests for the info_from_imdb_id function within update_tables.py

###### Retrieve and clean up data: update_tables.py
Contains functions using API's to retrieve additional data about the movies and to clean up the data. Data cleanup functions include:
  - Set the movie image URL to Null (None in Python) for movie poster URL’s retrieved using the Open Movie Database (OMDB) API that had the value “N/A”.
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

### <a name="Future"></a>Future enhancements

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

##### Identify latitude and longitude for additional movie locations 
I would like to create an automated process to reformat the 15% of location descriptions for which the Google maps API was unable to identify a specific latitude and longitude within San Francisco, in order to use the Google maps API to obtain a precise latitude and longitude for these locations that could be used to place markers on the Google map.

##### Search and subset movie list 
The current version accepts user input to subset the list by genre and to search by title (or partial title). I would like to add options to:
- Subset the list by director
- Subset the list by decades, based on release year
- Subset the list to only display movies for which there is a map with markers displaying filming locations. For about 20% of the movies, the San Francisco Film Commission data does not provide any specific filming locations.

##### Data cleanup 
I would like to continue the process of cleaning up the data by creating functions to:
- Correct the spelling of misspelled actor, writer and director names
- Correct the spelling of misspelled street names and location names
- Delete a few duplicate location descriptions for the same movie.

##### Testing

Given time constraints, I chose to primarily use manual testing for my project. After completing the Hackbright fellowship, I created limited unit tests and doctests for the info_from_imdb_id function within the update_tables.py file in order to practice automated testing. I have extensive experience defining and executing manual test plans as part of the process of developing business software. I believe that automated testing is an essential agile software development practice and I would like to add tests to my application to achieve the benefits of automated testing, including:

- Reducing the risk of introducing unidentified bugs when maintaining an application
- Facilitating the practice of refactoring code to make it clearer and more maintainable, without incurring a high risk of breaking the code in the process
- Clearly defining expected functionality, including edge cases 

### <a name="Acknowledgments"></a>Acknowledgments
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