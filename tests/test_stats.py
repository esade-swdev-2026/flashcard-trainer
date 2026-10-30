from datetime import date

from flashcard_trainer.flashcards import Flashcard, count_by_box


def test_count_by_box_counts_each_box() -> None:
    cards = [
        Flashcard(question="a?", answer="a"),
        Flashcard(question="b?", answer="b"),
        Flashcard(question="c?", answer="c", box=3, last_reviewed=date(2026, 10, 30)),
    ]
    assert count_by_box(cards) == {1: 2, 2: 0, 3: 1, 4: 0, 5: 0}


def test_count_by_box_with_no_cards_shows_every_box_empty() -> None:
    assert count_by_box([]) == {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
