from dataclasses import dataclass


@dataclass(frozen=True)
class Flashcard:
    question: str
    answer: str
    category: str = "general"


def normalize_answer(answer: str) -> str:
    return answer.strip().lower()


def check_answer(card: Flashcard, given_answer: str) -> bool:
    return normalize_answer(given_answer) == normalize_answer(card.answer)


def score_percentage(results: list[bool]) -> float:
    if not results:
        return 0.0
    correct = sum(1 for result in results if result)
    return (correct / len(results)) * 100
