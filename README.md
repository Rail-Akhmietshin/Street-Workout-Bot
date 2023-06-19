# Street-Workout-Bot

The bot was created to find like-minded people in street sports in the city of Kazan

## Description

The bot allows you to choose and sign up for a workout at your favorite outdoor playground, where everyone else can join by contacting you after your agreement.

Opportunities:
* Choose and sign up for a workout
* Find out the location of the site
* Find out who and for what time is registered for training at a certain site (only your name and date are visible to outsiders),
* View an illustration of the site
* Select a workout category
* Contact people with their consent to conduct joint training


## Usage

* First you need to create a file with environment variables '.env' and register the following fields in it:

BOT_TOKEN=(YOUR BOT TOKEN)\
POSTGRES_USER=(YOUR POSTGRESQL USER)\
POSTGRES_PASSWORD=(YOUR POSTGRESQL PASSWORD)\
POSTGRES_DB=(YOUR POSGTRESQL DATABASE)\
POSTGRES_PORT=( YOUR POSGTRESQL PORT OR DEFAULT (5432) )\

* To launch the bot, you need to run the commands in the following sequence:

1) docker-compose up -d --build
2) docker exec $(docker ps -f name=(YOUR DIRECTORY NAME)_db_1 -q) pg_restore -U postgres -d (YOUR POSTGRESQL DATABASE) /re_store_db
