# Eliot's Fall 2023 SJSU Robotics IntelSys Project
A simple simulator fulfilling SJSU Robotics Intelligent Systems' Trial Project requirements.
## Setup
Pip installs are perfectly fine. Just enter the project directory and run:

```bash
pip install -r requirements.txt
```
## Running
To run the simulator, just use python
```bash
python3 main.py
```
If you need help on the command line arguments, you can use
```bash
python3 main.py --help
```

## Design Structure
This project can be thought of in two parts:
- making a pathfinding algorithm for a grid
- making a GUI to display the results of that algorithm

Thus, the project directory structure reflects that:
- `grid` - the folder containing pathfinding algorithm and a `Grid` class
- `gui` - the folder containing GUI code to demonstrate the pathfinding algorithm.

### `grid`
Inside `grid`, there are two files: 
- `grid.py` provides an easy-to-use grid for export
- `a_star.py` provides the pathfinding algorithm. Since the goal is to move to the destination while avoiding the obstacles on the grid,
we use [A* shortest path algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
and set the cost of all obstacles to an infinite amount.
### `gui`
Inside `gui`, there are three files:
- `constants.py` contains color constants
- `gridDisplay.py` contains the `GridDisplay` class for easy displaying of a `Grid` object
- `gui.py` contains the `Scene` and `GUI` classes. The `GUI` class takes in user input, while the Scene class takes care of updating the internal `Grid`, robot position, and end goal.  