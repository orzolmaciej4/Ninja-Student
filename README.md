# Ninja-Student
This project is part of the coursework for the COMP3567 Multimedia and Games Development module at Durham University for the academic year 2023-24. The game, titled "Ninja Student," is a 2D action platformer inspired by classics like Mario and Sonic. The premise is a student trying to save the city of Durham from trouble in the city centre.

## Core Development and Implementation:
Game Scene:
- Visual Representation: 2D pixel art graphics
- Internal Data Structure: Classes for player and enemies, each with their own sprites and animations.

Game Flow Design and Implementation:
- Players start at a menu screen to select difficulty, view controls, start, or quit the game.
- Players progress through levels by defeating enemies. Losing all lives takes players back to the first level. Completing all levels leads to an end screen.

Game Object Representation and Manipulation:
- Player and Enemies: Each has its own sprite and animations. The player sprite includes idle, jump, run, and wall slide animations, while enemies have idle and run animations.
- Movement and Actions: The player can move, jump, and dash using arrow keys.

## Game Mechanics:
Main Game Rules:
- Navigate the menu using arrow and enter keys.
- Move, jump, and dash to traverse levels and defeat enemies.
- Collect coins and lives. Three difficulties determine the initial number of lives and coins.

Control and Growth of Abilities:
- Collect lives and coins in bushes and boxes. Ten coins add a life and reset the coin balance.
- The dash ability, used for attacks, remains constant throughout the game.

## Utilization and Implementation of Game Engine Features:
Key Features Used:
- pyGame: Used extensively for developing the game, pyGame provided tools for:
    - Sprites: Handling animations and movements for both the player and enemies.
    - Multiple Screens: Implementing a menu, game levels, and end screens.
    - Keyboard Inputs: Allowing player interactions through arrow keys and other controls.
    - Sound Effects and Music: Integrating audio to enhance the gaming experience.
    - Collision Detection: Managing interactions between game objects such as player, enemies, and collectibles.
    - Game Clock: Ensuring a consistent frame rate of 60 fps.
    - Event Handling: Managing user inputs and game events.
    - Font and Graphics Rendering: Displaying text and graphics on the screen.
    - Reading JSON Files: Loading level designs which were created using the level editor defined in editor.py

Custom Features Implemented:
- Menu: Allows players to view game instructions and change difficulty.
- Image Loading: Functions for loading and rendering animations.
- Animation Class: Simplifies implementation of player and enemy actions.
- Clouds Class: Implements parallax scrolling for a more realistic game appearance.

Additional Features:
- External Assets: Graphics, sound effects, and music, some modified to fit the game theme.

## Multimedia Technologies:
Effective Use:
- Graphics: Retro pixel art.
- Audio: Sound effects and music.
- Particle Effects: Enhance visuals for events like dashes and collisions.
- Parallax Scrolling: Creates a sense of depth and immersion.

Advanced Object Interaction:
- Physics: Gravity affects player jumps and landings.
- Camera: Follows player movement.
- Collisions: Various interactions between player, enemies, projectiles, and level elements.

## Getting Started:
To start the game, run the executable 'game' in the build/game directory. Navigate the menu using arrow keys and press enter to begin.

## Source Code and Assets:
Source Code: Available in the game.py and the scripts folder contains the code for all additional components.
Assets: Available in the data folder.
Game assets, music and sound effects were used from the following sources:
- https://dafluffypotato.com/static/pg_tutorial/00_resources.zip
- https://pixabay.com/sound-effects/
- font from https://github.com/clear-code-projects/2D-Mario-style-platformer
