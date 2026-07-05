# Motivation
The goal is this project is to make a twin stick shooter

# Overall plan of action
- [x] test the original game and get requirements such as window size, type of assets, game play
- [x] add enemies animation (explosion)
- [x] add gameplay elements: scoring, pause/restart, enemy waves

# Notes
See NOTES.md for dev log

# What I learned so far with this project
- trying to fit the game objects in a predefined framework is not always the most efficient: I wanted to have a base class `Sprite` then having the player inheriting from it, etc ... but it slowed down some implementations
- the `ResourceManager` class is super helpful becuase I can just change the game parameters from the `JSON` and see the effects immediately, so super helpful for iterating / finetuning
- the lack of `game state machine` defined earlier in the project hindered the final steps ; the current game logic seems a bit spaghetti-code :-(
- experimenting / checking that my implementation of `OBB` gave the same results as what `PolygonCollision` returns what some (relatively) tough time to figure out the whole local to global rotation but definitely useful on the long temr