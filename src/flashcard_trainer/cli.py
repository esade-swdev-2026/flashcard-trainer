import json
from pathlib import Path

import typer

from flashcard_trainer.flashcards import Flashcard, check_answer, score_percentage
from flashcard_trainer.storage import load_cards, save_cards

app = typer.Typer(help="A terminal flashcard trainer.")

DEFAULT_FILE = Path("cards.json")


def load_cards_or_exit(file: Path) -> list[Flashcard]:
    try:
        return load_cards(file)
    except (OSError, json.JSONDecodeError, TypeError, KeyError) as error:
        typer.echo(f"Could not read cards from {file}: {error}")
        raise typer.Exit(code=1) from error


@app.callback()
def main() -> None:
    pass


@app.command()
def add_card(
    question: str,
    answer: str,
    category: str = "general",
    file: Path = DEFAULT_FILE,
) -> None:
    """Add a new flashcard."""
    if not question.strip() or not answer.strip():
        typer.echo("question and answer must not be empty")
        raise typer.Exit(code=1)

    cards = load_cards_or_exit(file)
    cards.append(Flashcard(question=question, answer=answer, category=category))
    save_cards(file, cards)

    typer.echo(f"Added card [{category}]: {question} -> {answer}")


@app.command()
def list_cards(file: Path = DEFAULT_FILE) -> None:
    """List all saved flashcards."""
    cards = load_cards_or_exit(file)

    if not cards:
        typer.echo("No cards yet. Add one with add-card.")
        return

    for card in cards:
        typer.echo(f"[{card.category}] {card.question} -> {card.answer}")


@app.command()
def quiz(file: Path = DEFAULT_FILE) -> None:
    """Quiz yourself on all saved flashcards."""
    cards = load_cards_or_exit(file)

    if not cards:
        typer.echo("No cards yet. Add one with add-card.")
        return

    results = []
    for card in cards:
        given_answer = typer.prompt(card.question)
        results.append(check_answer(card, given_answer))

    score = score_percentage(results)
    typer.echo(f"Score: {score}%")


if __name__ == "__main__":
    app()
