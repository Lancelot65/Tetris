# Tetris in Python

This project is a simple implementation of the famous game TETRIS that runs in the terminal with some basic functionalities.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Font Change](#font-change)
- [Todo List](#todo-list)
- [Next Steps](#next-steps)
- [Contributions](#contributions)

<p align="center">
  <img src="https://github.com/Lancelot65/Tetris/tree/main/video/video_tetris.gif?raw=true" alt="Tetris Example"/>
</p>


## Installation

To install this project, you first need to clone the repository:

#### Note: I am not sure if this program works on Linux, as I developed it on Windows.

```bash
git clone https://github.com/username/tetris-python.git
cd tetris-python
```

Then, install the Uni-Curses dependency:

```bash
pip install windows-curses  # For Windows
# or
pip install curses          # For Linux/Mac
```

## Usage

To start the game, run the main script:

```bash
python main.py
```

## Font Change

For a better experience, it is recommended to temporarily change the font of your terminal. A font with equal height and width is ideal; you can find a square font in the `font` directory.

## Todo List

Here are some planned updates for the project:

- [ ] Add difficulty levels
- [ ] Adapt the scoring system for the difficulty level
- [ ] Improve the user interface

## Next Steps

Another repository will be created to implement a machine learning model that plays this Tetris. This will allow for the exploration of AI algorithms and enhance the gaming experience.

## Contributions

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b my-new-feature`).
3. Make your changes and commit (`git commit -m 'Add a new feature'`).
4. Push to the branch (`git push origin my-new-feature`).
5. Open a Pull Request.
