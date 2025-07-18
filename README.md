# Final Year Project

## **Important!!**

To use all functionality of this project, from running the application, to running checkstyle, to testing, you must be within the `product` directory **NOT** the root directory of this repository.

**_So remember to `cd product` before starting!_**

## 1 Setup

This project was developed using two different Windows machines. One using `Python 3.10.7` and the other using `Python 3.12.8`. I believe any python 3 version should work with this project.

### 1.1 Setup Environment

**_NOTE:_** Setting up an environment is optional but recommended because it helps isolate project dependencies.

To setup a environment follow these steps:

#### 1.1.1 Create the Python Virtual Environment.

1a. If your on Windows then do:

```bash
python -m venv .project-env
```

1b. If your on Mac or Linux then do:

```bash
python3 -m venv .project-env
```

#### 1.1.2 Activate the Environment

2a. If your on Windows then do:

```bash
.\.project-env\Scripts\activate
```

2b. If your on Mac or Linux then do:

```bash
source .project-env/bin/activate
```

**Now the environment is activated.**

#### 1.1.3 Deactivate the Environment

To deactivate the environment enter the following command:

```bash
deactivate
```

### 1.2 Download Dependencies

To download dependencies for this project run the following command:

```
pip install -r requirements.txt
```

## 2 Running the Application

### 2.1 Building

First we need to build the mazes by doing:

```
python .\create_maze.py
```

### 2.2 Executing Game Agent

To run the application you can use the following command format:
```bash
python main.py [-h] --size {small,medium,large,small-filled,medium-filled,large-filled} [--algo {random,dfs,bfs,ucs,astar,greedy,minimax,alphabeta,expectimax}] [--weighted] [--highlight][--enemy_count ENEMY_COUNT] [--explain] [--analysis]
```

An example command below where I would like the application on a small maze using the dfs algorithm:
```bash
# Example Command
python main.py --size small --algo dfs
```

Another example would be running the Alpha-Beta algorithm on a medium maze with one enemy:
```bash
# Example command
python main.py --size medium-filled --algo alphabeta --enemy_count 1 
```

### 2.3 Executing Game no Agent
If you want to control the player and not have an agent, then leave the algo flag out:
```bash
# Example command
python main.py --size small 
```

## 3 Analysis Tools
Use the `--analysis` flag to enable the analysis tool:

Then locate this block of code:
```python
# Example Command
python main.py --size medium --algo astar --analysis
```

This will print information of the algorithms onto the terminal.

## 4 Testing

To run every test you can do the following command:
```bash
python -m unittest discover ./testing/
```

To run specific test files, do the following:
```bash
python -m unittest .\testing\<test_file>
```

## 5 Checkstyle

This project uses python **_flake8_** checkstyle. It has been integrated to the gitlab pipeline.
If you would like to run the checkstyle yourself you can use one of the following commands:

**If your python environment is created within the product directory**
```bash
python -m flake8 --exclude <env_folder>
```

**Else you can simply run the following**
```bash
python -m flake8 
```

## 6 Repository Structure

[GitLab Rules](https://moodle.royalholloway.ac.uk/pluginfile.php/1740965/mod_resource/content/3/gitlab_rules.html) explains the root structure.

But an explanation will be given for the `product` directory:

- `assets\images` : This contains all the images and sprites used within the game.
- `testing` : This contains all the python test files.
- `agents\*`: This directory contains logic for every computer or agent type.
  - `computer.py`: The parent class for all computer types is stored in the file.
  - `uninformed_computer.py`: All uninformed computer classes are stored here. These are: `random`, `dfs` and `bfs`.
  - `informed_computer.py`: All informed computer classes are stored here. These are: `greedy`, `ucs` and `astar`.
  - `competitive_computer.py`: All competitive computer classes are stored here. These are `minimax`, `alphabeta` and `expectimax`.
- `characters\*`: This directory contains the different character types. There are only two types of characters: the main player or the enemy player. This manages player animations, movement, collisions, and related functionalities.
- `*.py` : All the python files used for the application are directly under `\product`. Here are some points on the key files:
  - `main.py` : This is the file contains the main game loops.
  - `world.py` : This file contains the data for the maze object and is primarily responsible for rendering the maze onto the Pygame screen.
  - `cli.py`: This file hold the cli logic.
  - `constants.py`: Most constants used in this programme originate from this file.
- `requirements.txt` : This file contains the dependencies needed fot this application.
- `maze\` : This directory gets generated after running `python .\create_maze.py`, and stores all the mazes to be used for the game.

## 7 Links to Assets used in this Project

[Character Sprites](https://craftpix.net/freebies/free-tiny-pixel-hero-sprites-with-melee-attacks/)\
[Background Cave Image](https://lil-cthulhu.itch.io/pixel-art-cave-background)\
[Platform Images](https://brackeysgames.itch.io/brackeys-platformer-bundle)\
[Diamond Images](https://drxwat.itch.io/pixel-art-diamond)\
[Ladder Image](https://nyknck.itch.io/wood-set)
