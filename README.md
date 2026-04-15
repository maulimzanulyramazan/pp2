# Mickey Clock (Pygame)

## Description

This project is a simple analog clock created using Pygame.
It displays the current system time using moving clock hands (minute and second), along with a clock face that includes numbers and tick marks.

## Features

* Analog clock with circular design
* Minute and second hands
* Numbers (1–12) around the clock
* Minute and hour tick marks
* Updates every second in real time

## Project Structure

```
mickeys_clock/
├── main.py          # Runs the application
├── clock.py         # Contains clock logic and drawing
├── images/          # (Optional) images for clock hands
│   └── mickey_hand.png
└── requirements.txt
```

## Requirements

* Python 3.10+
* Pygame

Install dependencies:

```
pip install -r requirements.txt
```

## How to Run

```
python main.py
```

## How It Works

* The program gets the current time using Python's datetime module
* Time is converted into angles (degrees)
* Trigonometry (sin, cos) is used to calculate hand positions
* Pygame draws the clock, numbers, and hands on the screen

## Notes

* The clock updates every second
* The center of the clock is fixed
* All drawing is done dynamically using Pygame

## Optional Improvements

* Add hour hand
* Use custom images (e.g., Mickey hands)
* Add background or clock design
* Smooth animation (real-time movement)
