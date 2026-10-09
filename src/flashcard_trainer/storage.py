import json
from pathlib import Path

from flashcard_trainer.flashcards import Flashcard


def save_cards(path: Path, cards: list[Flashcard]) -> None:
    data = [{"question": c.question, "answer": c.answer, "category": c.category} for c in cards]
    path.write_text(json.dumps(data))


def load_cards(path: Path) -> list[Flashcard]:
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    return [Flashcard(**item) for item in data]
