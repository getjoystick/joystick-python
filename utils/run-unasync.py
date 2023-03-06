import os
from pathlib import Path

import unasync


def main():
    additional_replacements = {
        # We want to rewrite to 'Client' instead of 'AsyncClient'
        # It affects two places:
        # - Import from `httpx`, which uses terms `AsyncClient` for async and `Client` for sync
        # - Our "export", where we use the same terms
        "AsyncClient": "Client",
    }
    rules = [
        unasync.Rule(
            fromdir="/src/joystick/_async",
            todir="/src/joystick/_sync",
            additional_replacements=additional_replacements,
        ),
    ]

    filepaths = []
    for root, _, filenames in os.walk(
        Path(__file__).absolute().parent.parent / "src/joystick/_async"
    ):
        for filename in filenames:
            if filename.rpartition(".")[-1] in (
                "py",
                "pyi",
            ):
                # and not filename.startswith("utils.py"):
                filepaths.append(os.path.join(root, filename))

    unasync.unasync_files(filepaths, rules)


if __name__ == "__main__":
    main()
