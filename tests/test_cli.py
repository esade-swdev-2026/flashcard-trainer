from pathlib import Path

from typer.testing import CliRunner

from flashcard_trainer.cli import app

runner = CliRunner()


def test_list_cards_rejects_corrupt_file(tmp_path: Path) -> None:
    """CLI test: corrupt cards file exits code 1 with clean message, no traceback."""
    bad_file = tmp_path / "corrupt.json"
    bad_file.write_text("not json")
    result = runner.invoke(app, ["list-cards", "--file", str(bad_file)])
    assert result.exit_code == 1
    assert "Could not read cards" in result.output


def test_add_card_to_unwritable_path_exits_cleanly(tmp_path: Path) -> None:
    """CLI test: a file that cannot be written exits code 1 with a message, no traceback."""
    bad_file = tmp_path / "missing-folder" / "cards.json"
    result = runner.invoke(app, ["add-card", "2+2?", "4", "--file", str(bad_file)])
    assert result.exit_code == 1
    assert "Could not save cards" in result.output
