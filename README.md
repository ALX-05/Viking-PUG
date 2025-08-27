Installation (Linux):
  1. Clone this repository
  ````
  git clone https://github.com/ALX-05/Viking-PUG
  ````
  2. Create python virtual environment
  ````
  python -m venv Viking-PUG
  ````
  3. cd to environment and activate environment
  ````
  cd Viking-PUG
  source ./bin/activate
  ````
  4. Install python dependencies
  ````
  pip install -r python-dependencies.txt
  ````
  5. Create .env file and add variables:

  `BOT_TOKEN=<your-discord-bot-token>`

  You should now be able to run the bot with `python3 bot.py`. use `deactivate` command to leave environment
