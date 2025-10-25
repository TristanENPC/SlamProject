SlamProject
===========

Summary
-------
SlamProject is a small Python project implementing a "Slam" (quiz / word-grid) game. It contains both a Flask-based web front-end (templates + static assets) and a set of Python modules that implement the game logic (grid generation, questions, players and turn handling). The project was developed as a student project for a course.

Highlights
----------
- A web interface served by `EssaiSite.py` using Flask and templates in `templates/`.
- A core game engine in `game.py` that manages turns, the final grid and interactions between players and the grid.
- Grid generation / crossword-like placement logic in `grid.py` (uses NumPy).
- Support files for words/questions: `mots.txt`, `questions.txt`, and `final.txt` (final grid data).

Quick start
-----------
Requirements:

- Python 3.8+ (tested with CPython)
- pip
- The project uses the following Python packages:
	- Flask
	- numpy

Install dependencies:

```bash
pip install Flask numpy
```

Run the web interface (development server):

```bash
python EssaiSite.py
# then open http://127.0.0.1:5000 in your browser
```

Run the game in CLI (basic):

```bash
python game.py
```

The CLI is a simple interactive runner used for testing the game logic and final-turn flow.

Repository structure
-------------------

- `EssaiSite.py`  : Flask web server that exposes routes and renders templates.
- `game.py`       : Core game logic — Game class, initialization of questions/words, and example `jeu` instance.
- `grid.py`       : Grid generation, placement and helper methods (uses NumPy).
- `player.py`     : Player classes (Player, HumanPlayer, BotPlayer).
- `question.py`   : Question data class.
- `mots.txt`      : Words used to populate the grids (format expected: word - definition).
- `questions.txt` : Questions list (format: question title - answer).
- `final.txt`     : Final grid data (format expected by `game.init_final_grid`).
- `templates/`    : Jinja2 HTML templates used by the web UI (`SiteSlam.html`, `SiteSlam2.html`, ...).
- `static/`       : Static assets (JS and CSS used by the web pages).
- `ReadMe`        : This file (project README).

Data formats and notes
----------------------
- `questions.txt` lines: each line should be "<title> - <answer>". `game.init_questions` splits on " - ".
- `mots.txt` lines: each line should be "<word> - <definition>" (used by `init_words`). Duplicate words are filtered.
- `final.txt` is parsed by `init_final_grid`. The code expects a specific structure — inspect `game.init_final_grid` for details.
- The grid generator is stochastic and may fail to generate a full grid on some runs; the code retries and returns False on failure.
