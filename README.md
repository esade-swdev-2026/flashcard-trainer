# Flashcard Trainer

A command-line tool for creating and reviewing flashcards, built for students who
want a quick, distraction-free way to memorize facts.

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
uv run flashcard-trainer add-card "Capital of France?" "Paris" --count 3
```

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
src/flashcard_trainer/          your package — importable, installable, not just a script
  cli.py          the typer command-line interface
  __main__.py     lets `python -m flashcard_trainer` work
tests/            pytest tests, mirroring src/
pyproject.toml    dependencies and tool configuration — the single source of truth
```
