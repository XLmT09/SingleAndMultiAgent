# Final Year Project

## **Important!!**

To use all functionality of this project, from running the application, to running checkstyle, to testing, you must be within the `product` directory **NOT** the root directory of this repository.

**_So remember to `cd product` before starting!_**

## 1 Setup

This project was developed using two different Windows machines. One using `Python 3.10.7` and the other using `Python 3.12.8`. I belive any python 3 version should work with this project.

### 1.1 Setup Enviorment

**_NOTE:_** Setting up an environment is optional but recommended because it helps isolate project dependencies.

To setup a enviorment follow these steps:

#### 1.1.1 Create the Python Virtual Enviorment.

1a. If your on Windows then do:

```bash
python -m venv .project-env
```

1b. If your on Mac or Linux then do:

```bash
python3 -m venv .project-env
```

#### 1.1.2 Activate the Enviorment

2a. If your on Windows then do:

```bash
.\.project-env\Scripts\activate
```

2b. If your on Mac or Linux then do:

```bash
source .project-env/bin/activate
```

**Now the enviorment is activated.**

#### 1.1.3 Deactivate the Enviorment

To deactivate the enviorment enter the following command:

```bash
deactivate
```

### 1.2 Download Dependencies

To download dependices for this project run the following command:

```
pip install -r requirments.txt
```

## 2 Running the Application

### 2.1 Building

First we need to build the mazes by doing:

```
python .\create_maze.py
```

### 2.2 Executing

To run the application you can use the following command format:
```
main.py [-h] --size {small,medium,large} --algo {random,dfs,bfs,ucs} [--highlight]
```

An example command below where I would like to the application on a small maze using the dfs algorithm:
```bash
# Exmaple Command
main.py --size small --algo dfs
```

## 3 Analysis Tools
Currently the only way to use analysis tools is to, chnage the source code.

Open the source code under `main.py`.

Then locate this block of code:
```python
# Initialize a specific computer class and pass arguments to constructor
computer = agent_types[config["algo"]](player,
                                        world.get_walkable_maze_matrix())
```

Then you just have to enable analysis mode by doing the following:
```python
# Initialize a specific computer class and pass arguments to constructor
computer = agent_types[config["algo"]](player,
                                        world.get_walkable_maze_matrix(),
                                        True)
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

This project uses python **_flake8_** checkstyling. It has been integrated to the gitlab pipeline.
If you would like to run the checkstyle yourself you can use one of the following commands:

**If your python enviorment is created within the product directory**
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
- `testing` : This contians all the python test files.
- `*.py` : All the python files used in the for the application are directly under product. Here are some points on the key files:
  - `main.py` : This is the file that starts the application, hence why we when running in steps **_2.2_** we use this file.
  - `computer.py` : All the different path finding algorithms are stored under here.
  - `world.py` : This file contains the data for the maze object and is primarily responsible for rendering the maze onto the Pygame screen.
  - `character.py` : This file manages player animations, movement, collisions, and related functionalities.
- `requirments.txt` : This file contains the dependencies needed fot this application.
- `maze\` : This directory gets generated after running `python .\create_maze.py`, and stores all the mazes to be used for the game.

## 7 Links to Assets used in this Project

[Character Sprites](https://craftpix.net/freebies/free-tiny-pixel-hero-sprites-with-melee-attacks/)\
[Background Cave Image](https://lil-cthulhu.itch.io/pixel-art-cave-background)\
[Platform Images](https://brackeysgames.itch.io/brackeys-platformer-bundle)\
[Diamond Images](https://drxwat.itch.io/pixel-art-diamond)\
[Ladder Image](https://nyknck.itch.io/wood-set)
