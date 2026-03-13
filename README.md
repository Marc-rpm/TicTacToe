# Tic-Tac-Toe Against a Sub-Intelligent Bot

This project is a simple implementation of the classic **Tic-Tac-Toe** game where a human player competes against a **sub-intelligent bot**. The purpose of the project is to demonstrate basic game logic, turn handling, and a very simple artificial opponent.

Unlike advanced AI implementations that use algorithms such as Minimax, the bot in this project intentionally uses a **limited and imperfect strategy**. Its behavior is designed to feel somewhat intelligent while still being beatable. The bot makes decisions based on a few basic rules instead of calculating all possible future moves.

## Features

* Playable Tic-Tac-Toe game (Player vs Bot)
* Simple command-line or graphical interface (depending on implementation)
* A bot with limited decision-making abilities
* Win, lose, and draw detection
* Turn-based gameplay

## Bot Behavior

The bot follows a small set of simple rules:

1. If it can win in the current move, it takes the winning spot.
2. If the player is about to win, it attempts to block the move.
3. Otherwise, it selects a random available position on the board.

Because the bot does not analyze the entire game tree, it can still make mistakes and miss optimal moves. This makes the gameplay more casual and fun rather than perfectly competitive.

## License

This project is open source and can be modified or distributed according to the chosen license in the repository.


---

## About me and the project

- [Installation](#installation)  
Clone the repo
- [License](#license)  
GNU Public License 3.0
- [Contact](#contact)  
https://github.com/Marc-rpm
---

## Installation

How to install and set up your project:

```bash
git clone https://github.com/C-Reaper/<repo>.git
cd <repo>
python3 ./src/main.py
```