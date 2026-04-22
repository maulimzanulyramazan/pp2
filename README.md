# Python Game Development Practice

## About This Project
This project contains three simple games built with Pygame library. Each game demonstrates different game mechanics and programming concepts.

---

## Game 1: Drawing App (Paint)

### Description
A simple drawing application where you can draw shapes, change colors, and use different tools.

### Features
- Free drawing with mouse
- Draw rectangles and circles
- Eraser tool
- Color selection (Red, Green, Blue)
- Clear screen function
- Adjustable brush size

### How to Play
| Key | Action |
|-----|--------|
| 1 | Free drawing mode |
| 2 | Rectangle mode |
| 3 | Circle mode |
| 4 | Eraser mode |
| R | Red color |
| G | Green color |
| B | Blue color |
| C | Clear screen |
| ESC | Exit |

### How to Draw
- **Free draw**: Press 1 → Click and drag mouse
- **Rectangle**: Press 2 → Click → Drag → Release
- **Circle**: Press 3 → Click → Drag → Release
- **Eraser**: Press 4 → Click and drag to erase

---

## Game 2: Snake Game

### Description
Classic Snake game where you control a snake, eat food, grow longer, and avoid hitting walls or yourself.

### Features
- Snake grows when eating food
- Wall collision detection (game over)
- Self collision detection (game over)
- Level system (every 3 foods = new level)
- Speed increases with each level
- Score and level counter
- Random food position (never on snake)

### How to Play
| Key | Action |
|-----|--------|
| ↑ ↓ ← → | Move snake |
| SPACE | Restart game |
| ESC | Exit |

### Game Rules
1. Eat red food to grow and get points
2. Don't hit the walls
3. Don't hit your own body
4. Every 3 foods = new level + faster speed

### Level System
- Level 1: Speed 5
- Level 2: Speed 7
- Level 3: Speed 9
- Level 4: Speed 11
- (Speed increases every level)

---

## Game 3: Racer Game

### Description
A car racing game where you drive your red car, avoid enemy cars, and collect coins on the road.

### Features
- Player car (red) moves left and right
- Enemy cars appear in different colors
- Random coin generation on the road
- Coin counter in top right corner
- Road with white lane lines
- Gray road with sidewalks
- Game over on collision with enemy cars

### How to Play
| Key | Action |
|-----|--------|
| ← → | Move car left/right |
| SPACE | Restart game |
| ESC | Exit |

### Game Rules
1. Avoid hitting enemy cars (blue, green, orange, purple)
2. Collect yellow coins with "$" symbol
3. Coins always appear (never run out)
4. 4 enemy cars on screen at the same time
5. Game ends when you hit an enemy car

### Road Design