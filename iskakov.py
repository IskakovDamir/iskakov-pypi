"""``pip install iskakov`` installs the own-baseline diagnostic.

This distribution carries no analysis code. It depends on ``own-baseline`` and
re-exports that package's command line under a second name, so ``iskakov`` and
``ownbaseline`` are the same program. In scripts, import the real package:

    from own_baseline import conditional_skill_report

This module exists for the console entry point.
"""
from __future__ import annotations

__version__ = "0.2.1"

_MISSING = (
    "iskakov is an alias for own-baseline, and own-baseline is not installed "
    "in this environment.\n"
    "    pip install own-baseline"
)


def main() -> int:
    """Run the own-baseline command line."""
    try:
        from own_baseline.cli import main as _main
    except ImportError:
        raise SystemExit(_MISSING)
    return _main()


if __name__ == "__main__":
    raise SystemExit(main())
