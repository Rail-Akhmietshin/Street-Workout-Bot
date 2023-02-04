# Street-Workout-Bot

The bot was created to find like-minded people in street sports in the city of Kazan

* First you need to create a file with environment variables '.env' and register the following fields in it:

BOT_TOKEN=(YOUR BOT TOKEN)

POSTGRES_USER=(YOUR POSTGRESQL USER)

POSTGRES_PASSWORD=(YOUR POSTGRESQL PASSWORD)

POSTGRES_DB=(YOUR POSGTRESQL DATABASE)


* To launch the bot, you need to run the commands in the following sequence:

1) docker-compose up -d --build
2) docker exec $(docker ps -f name=new_bot_db_1 -q) pg_restore -U postgres -d (YOUR POSTGRESQL DATABASE) /re_store_db
