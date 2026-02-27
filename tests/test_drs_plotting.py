import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from model.drs_model import DRSModel


@pytest.fixture
def drs_model():
    model = DRSModel()
    # Mock history data
    model.history_time = [0.0, 10.0, 10.0, 20.0]
    model.history_rate_config = [1, 1, 4, 4]  # Mode A then Mode B
    model.history_ore_levels = [
        (10000, 5000, 5000),
        (20000, 10000, 10000),
        (20000, 10000, 10000),
        (30000, 15000, 15000),
    ]
    return model


@patch("matplotlib.pyplot.subplots")
@patch("matplotlib.pyplot.show")
def test_plot_results_calls_matplotlib(mock_show, mock_subplots, drs_model):
    """
    Test that plot_results sets up subplots and calls show.
    """
    mock_fig = MagicMock()
    mock_ax1 = MagicMock()
    mock_ax2 = MagicMock()
    mock_subplots.return_value = (mock_fig, (mock_ax1, mock_ax2))

    drs_model.plot_results()

    # Verify subplots called
    mock_subplots.assert_called_once_with(2, 1, figsize=(10, 10), sharex=True)

    # Verify plot/step calls on axes
    assert mock_ax1.step.call_count == 3  # Mode A, Mode B, Shutdown
    assert mock_ax2.plot.call_count == 3  # Total, Ore 1, Ore 2

    # Verify Y-limits
    mock_ax1.set_ylim.assert_called_with(0, 4)
    mock_ax2.set_ylim.assert_called_with(0, 80)

    # Verify show was called
    mock_show.assert_called_once()


def test_plot_results_empty_history(capsys):
    """
    Test plot_results with no history data.
    """
    model = DRSModel()
    model.plot_results()
    captured = capsys.readouterr()
    assert "No history data to plot." in captured.out
