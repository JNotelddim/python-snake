import os
import sys
import random
from bottle import debug, default_app, post, request, route, run
from configparser import ConfigParser
from typing import DefaultDict, Any
from pprint import pprint

from app import api
from src.board import Board
from src.brain import Brain

config = ConfigParser()
config.read('config.ini')
if 'APP_ENV' not in config['DEFAULT']:
    print('Missing required configurations, server shutting down.')
    sys.exit()

@post('/ping')
def ping():
    return api.ping_response()

@post('/start')
def start():
    data: Any = request.json
    print("Starting game %s" % data["game"]["id"])
    return api.start_response("#ffb6c1")


@post('/move')
def move():
    data = request.json
    print('Move data:')
    pprint(data)
    board = Board(data["board"])
    brain = Brain(data["you"]["id"], board)

    decision = brain.get_decision()
    print("Turn: ", data["turn"], "; snake_id: ", data["you"]["id"], "; made the decision to go ", decision)
    return api.move_response(decision)

@post('/end')
def end():
    data = request.json
    print ("Game %s ended" % data["game"]["id"])
    return api.end_response()


# Expose WSGI app (so gunicorn can find it)
app = default_app()

if __name__ == '__main__':
    run(app,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        reloader=(config['DEFAULT']['APP_ENV'] != 'production'),
        debug=(config['DEFAULT']['APP_ENV'] != 'production')
    )
