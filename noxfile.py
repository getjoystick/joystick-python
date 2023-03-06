import os
import re

import nox

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILES = ("setup.py", "noxfile.py", "utils/", "src/", "examples/")


@nox.session(
    python=[
        "3.7",
        "3.8",
        "3.9",
        "3.10",
        "3.11",
    ]
)
def test(session):
    session.install(".")
    session.install("pytest", "pytest-asyncio", "mock", "respx")

    pytest_argv = [
        "pytest",
        "--log-level=DEBUG",
        "--cache-clear",
        "--asyncio-mode=strict",
        "-vv",
        "tests/",
    ]
    # TODO: Consider supporting Python < 3.5
    # python_version = tuple(int(x) for x in session.python.split("."))
    # Python 3.6+ is required for async
    # if python_version < (3, 6):
    # pytest_argv.append("--ignore=test_elasticsearch/test_async/")

    session.run(*pytest_argv)


@nox.session()
def format(session):
    session.install("unasync", "isort", "black", "flake8")

    session.run("python", "utils/run-unasync.py")
    session.run("isort", "--profile=black", *SOURCE_FILES)
    for file in SOURCE_FILES:
        session.run("black", file)
    session.run("flake8", *SOURCE_FILES)
    lint(session)


@nox.session()
def lint(session):
    session.install("flake8", "black", "mypy", "isort", "types-requests")

    session.run("isort", "--check", "--profile=black", *SOURCE_FILES)
    session.run("black", "--check", *SOURCE_FILES)
    session.run("flake8", *SOURCE_FILES)

    session.install(".")

    session.run("mypy", "--strict", "--show-error-codes", "src/")


@nox.session()
def publish(session):
    version = os.getenv("GITHUB_REF_NAME")
    if version is None:
        raise ValueError(
            "Expect to run the publish session in a GitHub Actions workflow"
        )

    version_no_prefix = version[1:] if version[0] == "v" else version

    files_to_check = ["setup.py", "src/joystick/__init__.py", "CHANGELOG.md"]

    check_version_consistency(version_no_prefix, files_to_check)
    print(
        f"Version {version_no_prefix} is consistent across all files: {files_to_check}"
    )

    session.run("rm", "-rf", "dist", "build", external=True)
    session.install(".[dev]")
    session.install("setuptools", "twine", "wheel")
    session.run("python", "setup.py", "sdist", "bdist_wheel")
    session.run("twine", "check", "./dist/*")
    session.run("twine", "upload", "dist/*")


def check_version_consistency(version, files_to_check):
    version_for_regex = version.replace(".", "\\.")

    version_regex = rf"[\['\"]v?{version_for_regex}[\]'\"]"

    for file in files_to_check:
        with open(file, "r") as f:
            content = f.read()
            if re.search(version_regex, content) is None:
                raise ValueError(f"Version {version} not found in {file}")
