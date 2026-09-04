"""The alias has one job: hand the own-baseline command line a second name.

Two things can break it. The dependency can go missing, in which case the user
should see one sentence and not a traceback. And the forwarded entry point can
drift from what own-baseline actually exposes, which is what happens when the
real package renames its main.
"""
import subprocess
import sys
from importlib.metadata import entry_points

import iskakov


def test_module_is_not_a_package():
    """A module-level __getattr__ that forwards to own_baseline answers __path__
    as well, and Python then treats this module as a package rooted in someone
    else's directory. It cost a broken console script once; keep it flat."""
    assert not hasattr(iskakov, "__path__")


def test_console_script_is_declared():
    scripts = {e.name: e.value for e in entry_points(group="console_scripts")}
    assert scripts.get("iskakov") == "iskakov:main"


def test_forwards_to_own_baseline():
    from own_baseline.cli import main as real
    assert iskakov.main.__module__ == "iskakov"
    r = subprocess.run([sys.executable, "-c",
                        "import iskakov, sys; sys.argv=['iskakov','floors',"
                        "'--n','39505','--rho','0.4844','--no-color']; "
                        "raise SystemExit(iskakov.main())"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "+0.0247" in r.stdout, r.stdout
    assert callable(real)


def test_missing_dependency_gives_a_sentence(tmp_path):
    """Blocking own_baseline should produce the install line, not a traceback."""
    blocker = tmp_path / "own_baseline.py"
    blocker.write_text("raise ImportError('blocked for the test')\n")
    r = subprocess.run([sys.executable, "-c",
                        "import iskakov; raise SystemExit(iskakov.main())"],
                       capture_output=True, text=True,
                       env={**dict(__import__("os").environ),
                            "PYTHONPATH": str(tmp_path)})
    assert r.returncode == 1
    assert "pip install own-baseline" in r.stderr
    assert "Traceback" not in r.stderr
