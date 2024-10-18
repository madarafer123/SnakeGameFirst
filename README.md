# Classic Snake Game 90s (Python)

This repository contains the source code for a classic Snake game inspired by the 90s version, developed with Python and the `pygame` library.  
The game includes several features such as different difficulty levels, extra lives, special apples, and nostalgic sound effects!

## Main Features

- **Snake Movement**: Controlled by the arrow keys.
- **Special Apples**: Periodically appear and grant extra points.
- **Adjustable Difficulty**: Three difficulty levels (Easy, Medium, Hard).
- **Extra Lives**: The player has up to three lives before the game ends.
- **Sound Effects and Music**: Nostalgic sounds for eating apples and a "Game Over" sound effect.
- **Game Over Screen**: With options to restart the game, return to the main menu, or exit.

## Game Instructions

- **Movement**: Use the arrow keys to move the snake.
- **Objective**: Eat apples to grow and increase your score.
- **Be Careful**: Avoid hitting walls or yourself, or you will lose lives.
- **Special Apples**: Blue apples give bonuses but disappear after 5 seconds.
- **Difficulty**: In the main menu, you can select between three difficulty levels.

## Assets

- **Images and Sounds**: The project uses customizable images and sounds, located in the `Icon` and `Sound Effects` folders.
- **Logo**: The game logo is displayed on the main menu and can be changed by replacing the `Snake Logo.png` file in the `Icon` folder.

## How to Customize

- **Images**: Replace the files in the `Icon` folder to change the appearance of the game.
- **Sounds**: To modify the sound effects, replace the files in the `Sound Effects` folder.

## Controls

- Arrow keys: Move the snake.
- Enter: Select menu options.
- `V`: Return to the main menu on the rules screen.

## Code Structure

- **menu_principal()**: Manages navigation in the main menu.
- **run_game()**: Executes the main game logic, including movement, collision, and scoring.
- **game_over_screen()**: Displays the "Game Over" screen with options to restart or exit.
- **rules_screen()**: Displays the game rules.
- **select_difficulty()**: Allows the player to choose the difficulty level.

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests with improvements or new features.
