from pathlib import Path

from typer.testing import CliRunner

from flashcard_trainer.cli import app

runner = CliRunner()


def test_add_card_rejects_empty_question() -> None:
    """CLI test: invalid input exits non-zero without writing files."""
    result = runner.invoke(app, ["add-card", "", "4"])
    assert result.exit_code != 0


def test_add_card_persists_to_file(tmp_path: Path) -> None:
    """I/O test: verifies disk persistence using tmp_path."""
    file_path = tmp_path / "cards.json"
    result = runner.invoke(
        app,
        ["add-card", "What is 2+2?", "4", "--file", str(file_path)],
    )
    assert result.exit_code == 0
    assert file_path.exists()


def test_list_cards_rejects_corrupt_file(tmp_path: Path) -> None:
    """CLI test: corrupt cards file exits code 1 with clean message, no traceback."""
    bad_file = tmp_path / "corrupt.json"
    bad_file.write_text("not json")
    result = runner.invoke(app, ["list-cards", "--file", str(bad_file)])
    assert result.exit_code == 1
    assert "Could not read cards" in result.output
