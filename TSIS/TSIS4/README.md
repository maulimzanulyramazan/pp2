# 🐍 Snake Game

Advanced Snake game with PostgreSQL database integration, power-ups, obstacles, and leaderboard system.

## 📋 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Game](#running-the-game)
- [Controls](#controls)
- [Game Features](#game-features)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

## ✨ Features

### Core Gameplay
- Classic snake movement with smooth controls
- Level progression (every 5 foods)
- Speed increases with each level
- Score tracking and personal best

### Food System
- **Normal Food** (Red) - 1 point, never expires
- **Gold Food** (Gold) - 3 points, high value
- **Timed Food** (Blue) - 2 points, disappears after 5 seconds
- **Poison Food** (Dark Red) - -2 points, shortens snake by 2 segments

### Power-Ups (5 seconds duration)
| Power-Up | Color | Effect |
|----------|-------|--------|
| Speed Boost | Purple | Increases snake speed |
| Slow Motion | Yellow | Decreases snake speed |
| Shield | Cyan | Ignores next collision |

### Obstacles
- Appear starting from Level 3
- Randomly placed at each new level
- Collision = Game Over (unless shielded)
- Number increases with level (max 20)

### Database Integration (PostgreSQL)
- Username entry on main menu
- Auto-save results to database after game over
- Top 10 leaderboard display
- Personal best shown during gameplay

### Settings (JSON)
- Snake color selection (6 colors)
- Grid overlay toggle
- Sound on/off

### Game Screens
- Main Menu (Play, Leaderboard, Settings, Quit)
- Username Input Screen
- Leaderboard Screen (Top 10 scores)
- Settings Screen
- Game Over Screen (Retry, Main Menu)

## 📦 Requirements

- Python 3.8+
- PostgreSQL 12+ (for leaderboard features)
- Required Python packages: