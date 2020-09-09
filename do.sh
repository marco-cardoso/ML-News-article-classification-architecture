# This FOR is necessary because for some reason the environment variables
# loaded from the docker-compose do not work in CRON
# for more details consider reading
# https://stackoverflow.com/questions/27771781/how-can-i-access-docker-set-environment-variables-from-a-cron-job
for variable_value in $(cat /proc/1/environ | sed 's/\x00/\n/g'); do
    export $variable_value
  done

# Update the database with the latest articles
/usr/local/bin/python3.7 /news_classifier/news_classifier/scraper/scraper.py

# Train the ML model and upload to S3
/usr/local/bin/python3.7 /news_classifier/news_classifier/models/train_model.py