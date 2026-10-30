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