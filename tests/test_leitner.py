from datetime import date

import pytest

from flashcard_trainer.flashcards import (
    LAST_BOX,
    Flashcard,
    card_from_dict,
    card_to_dict,
    cards_from_dicts,
    due_cards,
    due_date,
    is_due,
    next_box,
    review_card,
)

TODAY = date(2026, 10, 18)


def test_correct_answer_moves_card_up_one_box() -> None:
    assert next_box(2, was_correct=True) == 3


def test_correct_answer_in_last_box_stays_in_last_box() -> None:
    assert next_box(LAST_BOX, was_correct=True) == LAST_BOX


def test_wrong_answer_sends_card_back_to_box_one() -> None:
    assert next_box(4, was_correct=False) == 1


def test_new_card_is_due_immediately() -> None:
    card = Flashcard(question="2+2?", answer="4")
    assert due_date(card) is None
    assert is_due(card, TODAY) is True


def test_box_one_card_is_due_the_next_day() -> None:
    card = Flashcard(question="2+2?", answer="4", box=1, last_reviewed=date(2026, 10, 17))
    assert is_due(card, TODAY) is True


def test_box_three_card_is_not_due_before_its_interval() -> None:
    card = Flashcard(question="2+2?", answer="4", box=3, last_reviewed=date(2026, 10, 16))
    assert due_date(card) == date(2026, 10, 20)
    assert is_due(card, TODAY) is False


def test_due_cards_keeps_only_cards_due_today() -> None:
    new_card = Flashcard(question="new?", answer="yes")
    waiting_card = Flashcard(question="old?", answer="no", box=5, last_reviewed=TODAY)
    assert due_cards([new_card, waiting_card], TODAY) == [new_card]


def test_review_card_records_new_box_and_review_date() -> None:
    card = Flashcard(question="2+2?", answer="4", box=2)
    reviewed = review_card(card, was_correct=True, today=TODAY)
    assert reviewed.box == 3
    assert reviewed.last_reviewed == TODAY
    assert card.box == 2  # original card is unchanged


def test_card_survives_dict_round_trip() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math", box=3, last_reviewed=TODAY)
    assert card_from_dict(card_to_dict(card)) == card


def test_old_card_without_box_loads_into_box_one() -> None:
    card = card_from_dict({"question": "2+2?", "answer": "4", "category": "math"})
    assert card.box == 1
    assert card.last_reviewed is None


@pytest.mark.parametrize(
    "fields",
    [
        {"answer": "4"},
        {"question": "2+2?", "answer": "4", "box": 9},
        {"question": "2+2?", "answer": "4", "box": "high"},
        {"question": "2+2?", "answer": "4", "last_reviewed": "yesterday"},
    ],
)
def test_invalid_card_raises_value_error(fields: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        card_from_dict(fields)


def test_saved_value_that_is_not_a_list_raises_value_error() -> None:
    with pytest.raises(ValueError):
        cards_from_dicts({"question": "2+2?"})
