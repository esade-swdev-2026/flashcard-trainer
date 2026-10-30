from dataclasses import dataclass, replace
from datetime import date, timedelta
from typing import Any

FIRST_BOX = 1
# Leitner boxes: a card in box N is reviewed again REVIEW_INTERVAL_DAYS[N] days after
# its last review. A correct answer moves it up one box; a wrong one sends it back to box 1.
REVIEW_INTERVAL_DAYS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}
LAST_BOX = max(REVIEW_INTERVAL_DAYS)


@dataclass(frozen=True)
class Flashcard:
    question: str
    answer: str
    category: str = "general"
    box: int = FIRST_BOX
    last_reviewed: date | None = None


def normalize_answer(answer: str) -> str:
    return answer.strip().lower()


def check_answer(card: Flashcard, given_answer: str) -> bool:
    return normalize_answer(given_answer) == normalize_answer(card.answer)


def score_percentage(results: list[bool]) -> float:
    if not results:
        return 0.0
    correct = sum(1 for result in results if result)
    return (correct / len(results)) * 100


def next_box(current_box: int, was_correct: bool) -> int:
    if was_correct:
        return min(current_box + 1, LAST_BOX)
    return FIRST_BOX


def due_date(card: Flashcard) -> date | None:
    """The day the card should next be reviewed, or None if it has never been reviewed."""
    if card.last_reviewed is None:
        return None
    return card.last_reviewed + timedelta(days=REVIEW_INTERVAL_DAYS[card.box])


def is_due(card: Flashcard, today: date) -> bool:
    next_review = due_date(card)
    return next_review is None or next_review <= today


def due_cards(cards: list[Flashcard], today: date) -> list[Flashcard]:
    return [card for card in cards if is_due(card, today)]


def count_by_box(cards: list[Flashcard]) -> dict[int, int]:
    counts = {box: 0 for box in REVIEW_INTERVAL_DAYS}
    for card in cards:
        counts[card.box] += 1
    return counts


def review_card(card: Flashcard, was_correct: bool, today: date) -> Flashcard:
    return replace(card, box=next_box(card.box, was_correct), last_reviewed=today)


def card_to_dict(card: Flashcard) -> dict[str, Any]:
    return {
        "question": card.question,
        "answer": card.answer,
        "category": card.category,
        "box": card.box,
        "last_reviewed": card.last_reviewed.isoformat() if card.last_reviewed else None,
    }


def card_from_dict(fields: dict[str, Any]) -> Flashcard:
    """Build a card from saved fields. Raises ValueError if they are not a valid card."""
    try:
        question = str(fields["question"])
        answer = str(fields["answer"])
        category = str(fields.get("category", "general"))
        box = int(fields.get("box", FIRST_BOX))
        last_reviewed_text = fields.get("last_reviewed")
        last_reviewed = date.fromisoformat(last_reviewed_text) if last_reviewed_text else None
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"invalid card {fields!r}: {error}") from error
    if box not in REVIEW_INTERVAL_DAYS:
        raise ValueError(f"invalid card {fields!r}: box must be {FIRST_BOX}-{LAST_BOX}")
    return Flashcard(question, answer, category, box, last_reviewed)


def cards_from_dicts(saved: Any) -> list[Flashcard]:
    """Build cards from the saved JSON value. Raises ValueError if it is not a list of cards."""
    if not isinstance(saved, list):
        raise ValueError("expected a list of cards")
    for fields in saved:
        if not isinstance(fields, dict):
            raise ValueError(f"invalid card {fields!r}: expected an object")
    return [card_from_dict(fields) for fields in saved]
