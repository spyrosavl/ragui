import os
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest
import typer
from typer.testing import CliRunner

from ragui._cli import app

runner = CliRunner()


def test_dev_file_not_found():
    result = runner.invoke(app, ["nonexistent.py"])
    assert result.exit_code == 1
    assert "does not exist" in result.stdout


@patch("builtins.open", mock_open(read_data="ragui = 'test'"))
@patch("uvicorn.run")
def test_dev_successful_run(mock_run):
    with patch.object(Path, "exists", return_value=True):
        result = runner.invoke(app, ["test.py"])
        assert result.exit_code == 0
        assert "Starting the RagUI server" in result.stdout
        mock_run.assert_called_once_with("ragui._server:app", reload=True, port=8000)


@patch("builtins.open", mock_open(read_data="x = 1"))
def test_dev_no_ragui_instance():
    with patch.object(Path, "exists", return_value=True):
        result = runner.invoke(app, ["test.py"])
        assert result.exit_code == 1
        assert "No RagUI instance found" in result.stdout


@patch("builtins.open", mock_open(read_data="ragui = 'test'"))
@patch("uvicorn.run")
def test_dev_custom_port(mock_run):
    with patch.object(Path, "exists", return_value=True):
        result = runner.invoke(app, ["test.py", "--port", "8080"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with("ragui._server:app", reload=True, port=8080)


@patch("builtins.open", mock_open(read_data="raise ValueError('test error')"))
def test_dev_script_error():
    with patch.object(Path, "exists", return_value=True):
        result = runner.invoke(app, ["test.py"])
        assert result.exit_code == 1
        assert "Error while running the script" in result.stdout


@patch("builtins.open", mock_open(read_data="ragui = 'test'"))
@patch("uvicorn.run")
def test_dev_no_reload(mock_run):
    with patch.object(Path, "exists", return_value=True):
        result = runner.invoke(app, ["test.py", "--no-reload"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with("ragui._server:app", reload=False, port=8000)
