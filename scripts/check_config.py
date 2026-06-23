"""Exercise C — read configuration from the environment (standalone script).

The lab's Exercise C asks you to read a secret (`DATABASE_URL`) from the
environment instead of hardcoding it, and to report ONLY whether it is set —
never the value itself, because it is a secret.

This lives in its own script (not in app/taskutils.py) because it is an
application-startup concern, not a task-data utility.

Run it with:
    python scripts/check_config.py

Try it both ways to see the two branches:
    DATABASE_URL="postgresql://localhost/taskflow" python scripts/check_config.py
    python scripts/check_config.py
"""

import os  # `os` gives us access to environment variables via os.environ.


def report_database_url() -> str:
    """Return a SAFE message about whether DATABASE_URL is configured.

    The function deliberately returns a *message*, not the URL, so there is no
    way for a caller to accidentally log or print the secret.
    """
    # `python-dotenv` is optional. If it is installed, load_dotenv() reads a
    # local `.env` file and pushes its keys into the environment. We import it
    # inside a try/except so this script still runs even when the package is
    # not installed (it just relies on real environment variables instead).
    try:
        from dotenv import load_dotenv

        load_dotenv()  # no-op if there is no .env file present
    except ImportError:
        # python-dotenv is not installed — that's fine, we fall back to reading
        # whatever is already in the real environment.
        pass

    # `os.environ.get("DATABASE_URL")` returns the value if the variable exists,
    # or `None` if it does not. Using `.get` (rather than `os.environ[...]`)
    # avoids a KeyError when the variable is unset, so we can handle the missing
    # case gracefully below.
    url = os.environ.get("DATABASE_URL")

    # A ternary expression chooses the message based on presence ONLY. We never
    # interpolate `url` into the output, so the secret value can never leak.
    return "DATABASE_URL is configured" if url else "DATABASE_URL is not set"


# `if __name__ == "__main__":` runs the block below only when this file is
# executed directly (python scripts/check_config.py), not when it is imported.
if __name__ == "__main__":
    print(report_database_url())
