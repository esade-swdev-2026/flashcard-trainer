from typer.testing import CliRunner

from flashcard_trainer.cli import app

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
