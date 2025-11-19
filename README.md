# Space Shooter Game

A classic arcade-style Space Shooter game built with Python and Pygame.

## Features

- **Player Movement**: Control your spaceship with Arrow Keys.
- **Shooting**: Fire bullets using the Spacebar.
- **Enemies**: Randomly spawning enemies that move downwards.
- **Score System**: Earn points for destroying enemies.
- **Scrolling Background**: Dynamic background that scrolls vertically.
- **Sound Effects**: Shooting sounds and background music support.

### 🚀 Power-Up System
As you destroy enemies, your weapon upgrades automatically!
- **Level 1 (0-9 Kills)**: Single Yellow Bullet.
- **Level 2 (10-19 Kills)**: Double Blue Bullets.
- **Level 3 (20+ Kills)**: Triple Red Spread Shot.

### 🌌 Visual Progression
The game environment evolves as you progress:
- **Stage 1 (0-49 Kills)**: Deep Space Background + Basic Ship + Fire Bullets.
- **Stage 2 (50-99 Kills)**: Classic Space Background + Advanced Ship + Blue Fire.
- **Stage 3 (100+ Kills)**: Elite Ship + Powerful Red Fire.

## Controls

- **Left Arrow**: Move Left
- **Right Arrow**: Move Right
- **Spacebar**: Shoot
- **R**: Restart Game (on Game Over screen)

## Requirements

- Python 3.x
- Pygame (`pip install pygame`)

## How to Run

1. Install dependencies:
   ```bash
   pip install pygame
   ```
2. Run the game:
   ```bash
   python game.py
   ```

## Assets
- `space_background.png`, `newSpaceBackGround.jpg`: Backgrounds
- `sprite.png`, `newSprite.png`, `sprite3.png`: Player Ships
- `fire.png`, `blue_fire.png`: Projectiles
- `shoot.mp3`: Sound Effects
