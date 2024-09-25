import logging
import subprocess
import sys
from contextlib import contextmanager
from io import StringIO

from tqdm import tqdm

logger = logging.getLogger(__name__)


@contextmanager
def capture_output(verbose=False):
    """
    Context manager to capture stdout and stderr in real-time.
    If verbose is True, logs will be shown to the user.
    """
    if verbose:
        yield sys.stdout, sys.stderr
    else:
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err


def run_with_progress(
    func, *args, description="Processing", total_steps=100, verbose=False, **kwargs
):
    """
    Executes a function while capturing its logs and displays a progress bar.
    If verbose is True, the logs will be shown to the user. Otherwise, they will be hidden.

    Args:
        func (callable): The function to execute.
        description (str): Description for the progress bar.
        total_steps (int): Total number of steps for the progress bar.
        verbose (bool): Whether to show logs or not.
        *args, **kwargs: Arguments passed to the function.

    Returns:
        result: The result of the function execution.
    """
    logger.debug(f"Starting '{description}' with verbose={verbose}")

    with tqdm(total=total_steps, desc=description, unit="step") as pbar:
        with capture_output(verbose=verbose) as (out, err):
            result = func(*args, **kwargs)  # Call the passed function

            # If not verbose, process the captured output without showing it to the user
            if not verbose:
                for line in out.getvalue().splitlines():
                    pbar.update(1)  # Simulate progress based on log lines

            # Ensure the progress bar reaches the full total
            pbar.n = total_steps
            pbar.refresh()

    logger.debug(f"Finished '{description}'")
    return result
