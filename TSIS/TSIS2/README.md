# TSIS2 - Paint Application with Extended Drawing Tools

A feature-rich paint application built with Pygame. Draw shapes, use freehand pencil, flood fill, add text, and save your artwork.

## Features

### Drawing Tools
- **Pencil** - Freehand drawing (1 key)
- **Line** - Straight line with live preview (2 key)
- **Rectangle** (3 key)
- **Circle** (4 key)
- **Square** (5 key)
- **Eraser** (6 key)
- **Flood Fill** - Fills closed areas (7 key)
- **Text Tool** - Click to place, type, Enter to confirm (8 key)

### Advanced Shapes (from Practice 11)
- **Right Triangle** (9 key)
- **Equilateral Triangle** (0 key)
- **Rhombus / Diamond** (- key)

### Brush Size
- Small (2px) - Q key
- Medium (5px) - W key
- Large (10px) - E key
- Increase/Decrease - +/- keys

### Colors
| Key | Color |
|-----|-------|
| R | Red |
| G | Green |
| B | Blue |
| Y | Yellow |
| P | Purple |
| O | Orange |
| K | Black |
| , (comma) | White |

### Other Features
- **Save Canvas** - Ctrl+S (saves as timestamped PNG)
- **Clear Canvas** - C key
- **On-screen buttons** for tools and brush sizes

## Installation

### Requirements
- Python 3.x
- Pygame library

### Setup
```bash
# Install pygame
pip install pygame

# Clone or download the project
# Run the application
python paint.py