This is for hydrating covid-related tweets using tweet ids from 2 data sources: COVID-19-TweetIDs and covid19_twitter. A total of 35 million tweets during January-July 2021 were hydrated and stored in MongoDB database. For each day 166668 tweets were collected.

set_up_db: Code for setting up MongoDB

jan_hydrate: Code for hydrating and storing 5 million tweets during January 2021. Multithreading with 13 Twitter api keys was used to speed up the data collection.(The code remains same for rest of the months except the main function needs to be called with the respective month number)