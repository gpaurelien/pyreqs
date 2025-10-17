import argparse
import os
import sys
from pathlib import Path

from .parser import Parser
from .utils import generate_toml, setup_logging


def _default_project_name() -> str:
    return Path(os.getcwd()).name


def _filter_stdlib(imports: set[str]) -> set[str]:
    stdlib = getattr(sys, "stdlib_module_names", set())
    if not stdlib:
        # Fallback for very old Pythons (not expected here but safe)
        stdlib = set(sys.builtin_module_names)
    # Also ignore common dunder and local package markers
    ignored = {"__future__", "__main__"}
    return {imp for imp in imports if imp not in stdlib and imp not in ignored}


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyreqs",
        description=(
            "Scan the current project for imports and generate a Poetry-compatible pyproject.toml"
        ),
    )

    parser.add_argument(
        "--name",
        default=_default_project_name(),
        help="Project name for [tool.poetry]. Defaults to current directory name.",
    )
    parser.add_argument(
        "--version",
        default="0.1.0",
        help="Project version.",
    )
    parser.add_argument(
        "--description",
        default="",
        help="Project description.",
    )
    parser.add_argument(
        "--readme",
        default="README.md",
        help="README filename to include. Use empty string to omit.",
    )
    parser.add_argument(
        "--include",
        action="append",
        dest="package_includes",
        default=None,
        help=(
            "Add a package include (can be provided multiple times). If omitted, 'packages' is not written."
        ),
    )
    parser.add_argument(
        "--python",
        default="^3.10",
        help="Python version constraint (e.g. ^3.10).",
    )
    parser.add_argument(
        "--output",
        default="pyproject.toml",
        help="Output file path for the generated pyproject.toml.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_cli().parse_args(argv)
    logger = setup_logging(verbose=args.verbose)

    logger.info("Scanning project for Python imports...")
    p = Parser()
    discovered_imports = p.scan_project_for_imports()
    logger.debug("Discovered imports: %s", ", ".join(sorted(discovered_imports)) or "<none>")

    third_party = sorted(_filter_stdlib(discovered_imports))
    if third_party:
        logger.info("Found third-party packages: %s", ", ".join(third_party))
    else:
        logger.info("No third-party imports found. Generating minimal pyproject.toml")

    # Use wildcard version to let Poetry resolve actual versions
    dependencies = {name: "*" for name in third_party}

    logger.info("Writing %s", args.output)
    generate_toml(
        name=args.name,
        version=args.version,
        description=args.description,
        readme=(args.readme or None),
        package_includes=args.package_includes,
        python=str(args.python),
        dependencies=dependencies,
        dev_dependencies=None,
        output=str(args.output),
    )

    logger.info("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


