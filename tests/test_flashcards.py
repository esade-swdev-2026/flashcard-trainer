from flashcard_trainer.flashcards import Flashcard, check_answer, score_percentage


def test_correct_answer_matches_exactly() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math")
    assert check_answer(card, "4") is True


def test_wrong_answer_does_not_match() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math")
    assert check_answer(card, "5") is False


def test_answer_is_case_insensitive() -> None:
    card = Flashcard(question="Capital of France?", answer="Paris", category="geo")
    assert check_answer(card, "paris") is True


def test_answer_ignores_surrounding_whitespace() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math")
    assert check_answer(card, "  4  ") is True


def test_empty_given_answer_does_not_match() -> None:
    card = Flashcard(question="2+2?", answer="4", category="math")
    assert check_answer(card, "") is False


def test_score_with_mixed_results() -> None:
    assert score_percentage([True, True, False, True]) == 75.0


def test_score_all_correct() -> None:
    assert score_percentage([True, True]) == 100.0


def test_score_all_wrong() -> None:
    assert score_percentage([False, False]) == 0.0


def test_score_empty_session_is_zero() -> None:
    assert score_percentage([]) == 0.0
