# Blackjack Game (Pygame)

#### Video demo: https://youtu.be/mmJG1hARnwg

Fully functional Blackjack game built using Python and Pygame. Play against a computer dealer in this classic card game with a style that's reminiscent of the early RPG games for PC.

## Contents
- [Features](#features)
- [Requirements](#requirements)
- [How to run](#how-to-run)
- [How to play](#how-to-play)
- [Project structure](#project-structure)
- [Contribution](#contribution)

## Features
- Player vs dealer Blackjack logic
- Game states: dealing, player turn, dealer turn, resolution, reset
- Game point tracking
- Classic-RPG-style textbox dialogue with skippable typewriter effect
- Fully playable game loop with input handling
- Original music
- Detailed logging

## Requirements
- Python 3.7+
- Pygame (tested with version 2.5.3)

## How to run
1. Clone the repo
2. Make sure you have Python installed
3. Install dependencies `pip install requirements.txt`
4. Run the game `python main.py`

## How to play
The game is keyboard-based. Progress through the dialogue with any key (`Esc` to skip the intro dialogue) and, during the gameplay, `H` to hit and `S` to stand. The aim is to win more games than the dealer.

## Project structure
```
blackjack/
|── main.py
|── game/
|   |── __init__.py
|   |── game_controller.py
|   |── constants.py
|   |── game_flags.py
|   |── game_manager.py
|   |── game_state.py
|   |── dialogue.py
|   |── textbox.py
|   |── person.py
|   |── hand.py
|   |── card.py
|   └── deck.py
|
|── assets/
|   |── cards/
|   |── music/
|   |── sounds/
|   └── table/
|
|── requirements.txt
└── README.md
```

## Contribution
Feel free to use, modify and contribute to this project for learning or your own purposes. Card assets are open source. Music composed and produced by me - please contact me if you want to reuse it.
