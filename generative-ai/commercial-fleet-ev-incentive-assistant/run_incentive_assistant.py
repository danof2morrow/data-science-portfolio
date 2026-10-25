"""Run the unchanged notebook export with readable terminal displays."""

from pathlib import Path
import runpy

import IPython.display as ipython_display


def terminal_display(*objects, **kwargs):
    for value in objects:
        if isinstance(value, ipython_display.Markdown):
            print(value.data)
        else:
            print(value)


if __name__ == "__main__":
    original_display = ipython_display.display
    try:
        ipython_display.display = terminal_display
        runpy.run_path(
            str(Path(__file__).with_name("commercial_fleet_ev_incentive_assistant.py")),
            run_name="__main__",
        )
    finally:
        ipython_display.display = original_display
