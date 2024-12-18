import os
from pathlib import Path

import typer
import uvicorn

app = typer.Typer()


@app.command()
def dev(script: str, port: int = 8000, reload: bool = True):
    """
    Run RagUI server for local development.

    Example:
        ragui main.py
    """
    script_path = Path(script)

    if not script_path.exists():
        typer.echo(f"Error: The script '{script}' does not exist.")
        raise typer.Exit(code=1)

    namespace: dict = {}
    try:
        with open(script_path) as f:
            code = f.read()
            exec(code, namespace)

        if "ragui" in namespace:
            typer.echo("Starting the RagUI server...")
            os.environ["RAGUI_SCRIPT"] = str(script_path)
            uvicorn.run("ragui._server:app", reload=reload, port=port)
        else:
            typer.echo("Error: No RagUI instance found in the script.")
            raise typer.Exit(code=1)

    except Exception as e:
        typer.echo(f"Error while running the script: {e}")
        raise typer.Exit(code=1)


def main():
    app()
