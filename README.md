# BSI_118
# Mini Ultimatum Game
This project implements a mini ultimatum game using the oTree framework. The game involves three players, where Player 1 endows a certain amount of currency and decides how much to send to Player 2. Player 3 acts as a "punisher" and can choose to punish Player 1 or not. The payouts for Player 1 and Player 2 depend on Player 3's decision.

# Game Flow
Intro: The introductory page is displayed only on the first round and provides an overview of the game.

Player 1: Player 1 enters the amount they want to send to Player 2.

Player 3: Player 3 decides whether to punish Player 1 or not.

Calculation: This page displays the amount sent, the punish decision, and the payouts for Player 1 and Player 2.

Questions: Player 3 answers a question to validate their understanding of the game. They select the capital city of Kenya from the given options.

Finish: The end page signifies the end of the game.

# Dependencies
Python 3.10
oTree 5.x
Installation
Clone the repository:

Copy
```
git clone https://github.com/your/repository.git
```

Install the dependencies:

basic
Copy
```
pip install -r requirements.txt
```

Run the oTree server:

Copy

```
otree devserver
```
