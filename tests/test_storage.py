from pathlib import Path

from flashcard_trainer.core import Flashcard
from flashcard_trainer.storage import load_cards, save_cards


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    file_path = tmp_path / "cards.json"
    cards = [
        Flashcard(question="2+2?", answer="4", category="math"),
        Flashcard(question="Capital of France?", answer="Paris", category="geo"),
    ]

    save_cards(file_path, cards)
    loaded = load_cards(file_path)

    assert loaded == cards


def test_load_missing_file_returns_empty_list(tmp_path: Path) -> None:
    file_path = tmp_path / "does_not_exist.json"

    assert load_cards(file_path) == []
