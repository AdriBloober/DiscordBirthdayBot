# DiscordBirthdayBot

## What is it?!
**InviteLink: https://discordapp.com/api/oauth2/authorize?client_id=705817352411021322&permissions=2048&scope=bot**  
You can say to the birthday bot, when you have birthday and the bot will congratulate you on any server.

## Self-Hosted Installation

You can see all Environment variables in the resources/config.py  
### Pipenv
Requirements: python3.8 python3.8-pip
```shell script
python3.8 -m pip install pipenv
pipenv install
```
For running use:
``pipenv run python run.py``
Do not forget the Environment variables
### Docker
Use the docker-compose.yml to run all
```shell script
docker-compose pull
docker-compose build
docker-compose up -d
```

## Developer

Developed by AdriBloober#1260 (https://twitter.com/AdriBloober)  
Open for contribution (fork and open Pull reqtest)