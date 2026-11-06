from datetime import date

from flashcard_trainer.flashcards import Flashcard, in_category, should_review

TODAY = date(2026, 11, 6)


def test_card_is_in_its_own_category() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math")
    assert in_category(card, "math") is True


def test_category_match_ignores_case() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math")
    assert in_category(card, "MATH") is True


def test_card_is_not_in_another_category() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math")
    assert in_category(card, "geo") is False


def test_no_category_matches_every_card() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math")
    assert in_category(card, None) is True


def test_due_card_in_category_should_be_reviewed() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math")
    assert should_review(card, TODAY, "math") is True


def test_card_not_yet_due_should_not_be_reviewed_even_in_category() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math", box=5, last_reviewed=TODAY)
    assert should_review(card, TODAY, "math") is False


def test_category_match_ignores_surrounding_spaces() -> None:
    card = Flashcard(question="2+2?", answer="4", category=" math ")
    assert in_category(card, "math ") is True
