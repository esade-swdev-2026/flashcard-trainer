import typer

app = typer.Typer(help="A terminal flashcard trainer.")


@app.callback()
def main() -> None:
    pass


@app.command()
def add_card(question: str, answer: str, category: str = "general") -> None:
    """Add a new flashcard."""
    if not question.strip() or not answer.strip():
        typer.echo("question and answer must not be empty")
        raise typer.Exit(code=1)

    typer.echo(f"Added card [{category}]: {question} -> {answer}")


if __name__ == "__main__":
    app()
