# Edu-MarketPlace-Extended
Senior Project Course Repository for Edu MarketPlace Extended project
# Travis Build
[![Build Status](https://travis-ci.com/rhcu/Edu-MarketPlace-Extended.svg?token=pYybYTDfgmyYWjqaNrQy&branch=master)](https://travis-ci.com/rhcu/Edu-MarketPlace-Extended)
## Chat
Chat appliction in the `chat` folder is deployed automatically to Heroku in parallel with our web application. It's hosted on [edu-marketplace-chat.herokuapp.com](https://edu-marketplace-chat.herokuapp.com/)
## Running locally
You can use Docker and Compose to run application locally. Run `docker-compose up`. Keep in mind that there are several environment variables that should be defined in your system and will be passed to Docker container. They are:
- `SOCIAL_AUTH_AUTH0_DOMAIN`
- `SOCIAL_AUTH_AUTH0_KEY`
- `SOCIAL_AUTH_AUTH0_SECRET`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DJANGO_SECRET_KEY`