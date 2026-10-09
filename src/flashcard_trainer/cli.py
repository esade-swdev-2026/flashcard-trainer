from pathlib import Path

import typer

from flashcard_trainer.flashcards import Flashcard
from flashcard_trainer.storage import load_cards, save_cards

app = typer.Typer(help="A terminal flashcard trainer.")

DEFAULT_FILE = Path("cards.json")


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

    cards = load_cards(file)
    cards.append(Flashcard(question=question, answer=answer, category=category))
    save_cards(file, cards)

    typer.echo(f"Added card [{category}]: {question} -> {answer}")


@app.command()
def list_cards(file: Path = DEFAULT_FILE) -> None:
    """List all saved flashcards."""
    cards = load_cards(file)

    if not cards:
        typer.echo("No cards yet. Add one with add-card.")
        return

    for card in cards:
        typer.echo(f"[{card.category}] {card.question} -> {card.answer}")


if __name__ == "__main__":
    app()
