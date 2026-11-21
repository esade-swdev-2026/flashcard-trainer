# Flashcard Trainer

A command-line tool for creating and reviewing flashcards, built for students who
want a quick, distraction-free way to memorize facts. It schedules reviews with the
Leitner system, so cards you know well come up less often.

## Get the code

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

```
git clone https://github.com/esade-swdev-2026/flashcard-trainer.git
cd flashcard-trainer
```

## Install

```
uv sync
```

This creates a virtual environment and installs everything, including the development
tools, from `uv.lock` — the committed file that pins exact versions so every teammate
and CI resolve the same ones. When you change a dependency in `pyproject.toml`, run
`uv lock` and commit the updated `uv.lock`; CI fails if the two disagree.

## Run

```
uv run flashcard-trainer --help
uv run flashcard-trainer add-card "Capital of France?" "Paris"
uv run flashcard-trainer add-card "What is 2+2?" "4" --category math
uv run flashcard-trainer list-cards
uv run flashcard-trainer quiz
```

Edit a card's answer (an empty new answer is rejected):

```bash
uv run flashcard-trainer edit-card "Capital of France?" "Paris"
```

Search cards whose question contains a keyword (case-insensitive):

```bash
uv run flashcard-trainer search-cards france
```

Show how many cards are in each Leitner box and how many are due today:

```bash
uv run flashcard-trainer stats
```

Quiz only one category:

```bash
uv run flashcard-trainer add-card "Capital of Spain?" "Madrid" --category geography
uv run flashcard-trainer quiz --category geography
```

Delete a card by its exact question:

```bash
uv run flashcard-trainer delete-card "Capital of France?"
```

`quiz` asks each card that is due today and tells you if you were right. Cards are
saved in `cards.json` in the current folder; pass `--file other.json` to any command
to use a different file.

Example session:

```
$ uv run flashcard-trainer quiz
Capital of France?: paris
Correct!
What is 2+2?: 5
Wrong. The answer is: 4
Score: 50%
$ uv run flashcard-trainer list-cards
[general] Capital of France? -> Paris  (box 2, due 2026-10-20)
[math] What is 2+2? -> 4  (box 1, due 2026-10-19)
```

### How the Leitner system works here

Every card sits in one of five boxes. New cards start in box 1 and are due straight
away. A correct answer moves a card up one box; a wrong answer sends it back to box 1.
The higher the box, the longer until the card is due again:

| Box | Due again after |
|-----|-----------------|
| 1   | 1 day           |
| 2   | 2 days          |
| 3   | 4 days          |
| 4   | 8 days          |
| 5   | 16 days         |

If no cards are due, `quiz` says so and exits.

## Run with Docker

Build the image once:

```bash
docker build -t flashcard-trainer .
```

Each `docker run --rm` starts a new container and deletes it when the command ends. The cards live in a named volume, `flashcards-data`, mounted at `/app/data`, so they survive between containers:

```bash
docker run --rm -v flashcards-data:/app/data flashcard-trainer add-card "Capital of France?" "Paris"
docker run --rm -v flashcards-data:/app/data flashcard-trainer list-cards
```

`list-cards` still shows the card, even though the container that added it is gone.

`quiz` asks for input, so it needs `-it`:

```bash
docker run --rm -it -v flashcards-data:/app/data flashcard-trainer quiz
```

To start over, delete the volume with `docker volume rm flashcards-data`.


## Use of AI

We developed the Flashcard Trainer as a team, from the initial idea and project structure to the CLI commands, Leitner system and testing. During the process, we used ChatGPT and Claude to help us with certain tasks, mainly when we needed suggestions, explanations or help solving problems.

- **Development and testing:** We used AI to help with some parts of the code, troubleshoot issues and suggest test cases. One example is the CLI tests for `stats`. We checked the suggestions, made changes where needed and ran the tests ourselves to make sure everything worked.
- **Docker and CI:** AI was useful for understanding things like layer caching, non-root users and Docker volumes. We also used it when working on the Dockerfile and the GitHub Actions release workflow. We tested the Docker setup locally and checked the results in CI.
- **Documentation:** We used AI to help write some README sections and command examples. We didn't just copy them though. When we tested the commands, we found two problems with their order and the category quiz, which we then corrected.
- **Git and code review:** AI helped us understand Git commands, deal with issues and prepare some review comments. The actual commits, reviews and merges were handled by us.

Overall, AI was mainly a tool to help us work through technical problems and speed up certain tasks. The project decisions, testing and responsibility for the final result remained with our team.


## Develop

```
uv run ruff check .          # lint
uv run ruff format .         # format (CI runs `--check` and fails on a diff)
uv run mypy src tests        # types
uv run pytest                # tests
```

These four commands are exactly what `.github/workflows/check.yml` runs on every push.
If they pass here, CI passes.

## Layout

```
src/flashcard_trainer/          the package
  flashcards.py   pure logic: the Flashcard type, answer checking, scoring, Leitner boxes
  storage.py      reads and writes the cards JSON file
  cli.py          the typer command-line interface
  __main__.py     lets `python -m flashcard_trainer` work
tests/            pytest tests, mirroring src/
pyproject.toml    dependencies and tool configuration — the single source of truth
```

## I/O

Everywhere the code touches the outside world (console or filesystem) rather than just computing:

- `src/flashcard_trainer/cli.py` — `typer.echo(...)` and `typer.prompt(...)` (console),
  `raise typer.Exit(code=1)` on bad input, and `date.today()` (the clock)
- `src/flashcard_trainer/storage.py` — `path.read_text()` / `path.write_text()` in
  `load_cards` / `save_cards`

Everything in `src/flashcard_trainer/flashcards.py` is pure: no I/O, just data in and
data out. Even "today" is passed in as an argument, which is what lets the Leitner
scheduling be tested without touching the filesystem, the terminal or the clock.
