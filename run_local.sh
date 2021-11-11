#! /bin/bash
DATABASE_URL=$(heroku config:get DATABASE_URL -a mrpowerbot) python3 -m pipenv run bot.py