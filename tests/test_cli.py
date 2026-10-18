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
