from dataclasses import replace
from datetime import date
from pathlib import Path

import typer

from flashcard_trainer.flashcards import (
    Flashcard,
    check_answer,
    due_cards,
    due_date,
    is_due,
    review_card,
    score_percentage,
)
from flashcard_trainer.storage import load_cards, save_cards

app = typer.Typer(help="A terminal flashcard trainer using the Leitner system.")

DEFAULT_FILE = Path("cards.json")


def load_cards_or_exit(file: Path) -> list[Flashcard]:
    try:
        return load_cards(file)
    except (OSError, ValueError) as error:
        typer.echo(f"Could not read cards from {file}: {error}", err=True)
        raise typer.Exit(code=1) from error


def save_cards_or_exit(file: Path, cards: list[Flashcard]) -> None:
    try:
        save_cards(file, cards)
    except OSError as error:
        typer.echo(f"Could not save cards to {file}: {error}", err=True)
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
    """Add a new flashcard. New cards start in box 1."""
    if not question.strip() or not answer.strip():
        typer.echo("question and answer must not be empty", err=True)
        raise typer.Exit(code=1)

    cards = load_cards_or_exit(file)
    cards.append(Flashcard(question=question, answer=answer, category=category))
    save_cards_or_exit(file, cards)

    typer.echo(f"Added card [{category}]: {question} -> {answer}")


@app.command()
def list_cards(file: Path = DEFAULT_FILE) -> None:
    """List all saved flashcards with their Leitner box and next review date."""
    cards = load_cards_or_exit(file)

    if not cards:
        typer.echo("No cards yet. Add one with add-card.")
        return

    for card in cards:
        next_review = due_date(card)
        due_text = next_review.isoformat() if next_review else "now"
        typer.echo(
            f"[{card.category}] {card.question} -> {card.answer}  (box {card.box}, due {due_text})"
        )


@app.command()
def delete_card(question: str, file: Path = DEFAULT_FILE) -> None:
    """Delete a flashcard by its question."""
    cards = load_cards(file)
    remaining = [card for card in cards if card.question != question]

    if len(remaining) == len(cards):
        typer.echo(f"No card found with question: {question}")
        raise typer.Exit(code=1)

    save_cards(file, remaining)
    typer.echo(f"Deleted card: {question}")


@app.command()
def quiz(file: Path = DEFAULT_FILE) -> None:
    """Review the cards that are due today, moving each one between Leitner boxes."""
    cards = load_cards_or_exit(file)
    today = date.today()

    if not cards:
        typer.echo("No cards yet. Add one with add-card.")
        return
    if not due_cards(cards, today):
        typer.echo("No cards due today. Come back tomorrow.")
        return

    updated_cards = list(cards)
    results = []
    for index, card in enumerate(cards):
        if not is_due(card, today):
            continue
        was_correct = check_answer(card, typer.prompt(card.question))
        typer.echo("Correct!" if was_correct else f"Wrong. The answer is: {card.answer}")
        results.append(was_correct)
        updated_cards[index] = review_card(card, was_correct, today)

    save_cards_or_exit(file, updated_cards)
    typer.echo(f"Score: {score_percentage(results):.0f}%")


@app.command()
def edit_card(question: str, new_answer: str, file: Path = DEFAULT_FILE) -> None:
    """Edit a flashcard's answer by its question."""
    cards = load_cards(file)

    for index, card in enumerate(cards):
        if card.question == question:
            cards[index] = replace(card, answer=new_answer)
            save_cards(file, cards)
            typer.echo(f"Updated card: {question} -> {new_answer}")
            return

    typer.echo(f"No card found with question: {question}")
    raise typer.Exit(code=1)


@app.command()
def search_cards(keyword: str, file: Path = DEFAULT_FILE) -> None:
    """Search flashcards whose question contains the given keyword."""
    cards = load_cards(file)
    matches = [card for card in cards if keyword.lower() in card.question.lower()]

    if not matches:
        typer.echo("No matching cards found.")
        return

    for card in matches:
        typer.echo(f"[{card.category}] {card.question} -> {card.answer}")


if __name__ == "__main__":
    app()
