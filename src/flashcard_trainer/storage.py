import json
from pathlib import Path

from flashcard_trainer.flashcards import Flashcard, card_to_dict, cards_from_dicts


def save_cards(path: Path, cards: list[Flashcard]) -> None:
    path.write_text(json.dumps([card_to_dict(card) for card in cards], indent=2))


def load_cards(path: Path) -> list[Flashcard]:
    if not path.exists():
        return []
    return cards_from_dicts(json.loads(path.read_text()))
