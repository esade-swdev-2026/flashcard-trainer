from pathlib import Path

from typer.testing import CliRunner

from flashcard_trainer.cli import app
from flashcard_trainer.flashcards import Flashcard
from flashcard_trainer.storage import load_cards

runner = CliRunner()


def test_add_card_succeeds() -> None:
    result = runner.invoke(app, ["add-card", "What is 2+2?", "4"])
    assert result.exit_code == 0
    assert "Added card" in result.stdout


def test_add_card_rejects_empty_question() -> None:
    result = runner.invoke(app, ["add-card", "", "4"])
    assert result.exit_code == 1


def test_add_card_uses_default_category() -> None:
    result = runner.invoke(app, ["add-card", "Q", "A"])
    assert "[general]" in result.stdout


def test_add_card_accepts_custom_category() -> None:
    result = runner.invoke(app, ["add-card", "Q", "A", "--category", "math"])
    assert "[math]" in result.stdout


def test_add_card_persists_to_file(tmp_path: Path) -> None:
    file_path = tmp_path / "cards.json"
    runner = CliRunner()

    result = runner.invoke(
        app,
        ["add-card", "2+2?", "4", "--category", "math", "--file", str(file_path)],
    )

    assert result.exit_code == 0
    saved = load_cards(file_path)
    assert saved == [Flashcard(question="2+2?", answer="4", category="math")]


def test_add_card_appends_to_existing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "cards.json"
    runner = CliRunner()

    runner.invoke(app, ["add-card", "2+2?", "4", "--file", str(file_path)])
    runner.invoke(app, ["add-card", "Capital of France?", "Paris", "--file", str(file_path)])

    saved = load_cards(file_path)
    assert len(saved) == 2


def test_list_cards_shows_saved_cards(tmp_path: Path) -> None:
    file_path = tmp_path / "cards.json"
    runner = CliRunner()
    runner.invoke(app, ["add-card", "2+2?", "4", "--file", str(file_path)])

    result = runner.invoke(app, ["list-cards", "--file", str(file_path)])

    assert result.exit_code == 0
    assert "2+2?" in result.stdout
    assert "4" in result.stdout


def test_list_cards_empty_file_says_so(tmp_path: Path) -> None:
    file_path = tmp_path / "cards.json"
    runner = CliRunner()

    result = runner.invoke(app, ["list-cards", "--file", str(file_path)])

    assert result.exit_code == 0
    assert "no cards" in result.stdout.lower()


def test_quiz_reports_score(tmp_path: Path) -> None:
    file_path = tmp_path / "cards.json"
    runner = CliRunner()
    runner.invoke(app, ["add-card", "2+2?", "4", "--file", str(file_path)])
    runner.invoke(app, ["add-card", "Capital of France?", "Paris", "--file", str(file_path)])

    result = runner.invoke(app, ["quiz", "--file", str(file_path)], input="4\nParis\n")

    assert result.exit_code == 0
    assert "100.0" in result.stdout


def test_quiz_with_no_cards_says_so(tmp_path: Path) -> None:
    file_path = tmp_path / "cards.json"
    runner = CliRunner()

    result = runner.invoke(app, ["quiz", "--file", str(file_path)])

    assert result.exit_code == 0
    assert "no cards" in result.stdout.lower()


def test_delete_card_removes_matching_card(tmp_path: Path) -> None:
    file_path = tmp_path / "cards.json"
    runner = CliRunner()
    runner.invoke(app, ["add-card", "2+2?", "4", "--file", str(file_path)])
    runner.invoke(app, ["add-card", "Capital of France?", "Paris", "--file", str(file_path)])

    result = runner.invoke(app, ["delete-card", "2+2?", "--file", str(file_path)])

    assert result.exit_code == 0
    remaining = load_cards(file_path)
    assert remaining == [
        Flashcard(question="Capital of France?", answer="Paris", category="general")
    ]


def test_delete_card_not_found_fails(tmp_path: Path) -> None:
    file_path = tmp_path / "cards.json"
    runner = CliRunner()

    result = runner.invoke(app, ["delete-card", "nope?", "--file", str(file_path)])

    assert result.exit_code == 1
