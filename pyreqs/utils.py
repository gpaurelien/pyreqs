from typing import Optional
import logging


def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    return logger


def generate_toml(
    name: str,
    version: str = "0.1.0",
    description: str = "",
    readme: Optional[str] = "README.md",
    package_includes: Optional[list[str]] = None,
    python: str = "^3.9",
    dependencies: Optional[dict[str, str]] = None,
    dev_dependencies: Optional[dict[str, str]] = None,
    output: str = "pyproject.toml",
) -> None:
    """Generate a Poetry-compatible pyproject.toml."""

    dependencies = dependencies or {}
    doc = {
        "tool": {
            "poetry": {
                "name": name,
                "version": version,
                "description": description,
                **({"readme": readme} if readme else {}),
                # 'packages' is optional, map simple list to [{ include = "<name>" }]
                **(
                    {
                        "packages": [
                            {"include": pkg}
                            for pkg in (package_includes or [])
                        ]
                    }
                    if package_includes
                    else {}
                ),
                "dependencies": {
                    "python": python,
                    **dependencies,
                },
                # 'group.dev.dependencies' is optional
                **(
                    {"group": {"dev": {"dependencies": dev_dependencies or {}}}}
                    if dev_dependencies
                    else {}
                ),
            }
        },
        "build-system": {
            "requires": ["poetry-core"],
            "build-backend": "poetry.core.masonry.api",
        },
    }

    # Fallback minimal TOML serialization (keeps your layout; handles common cases)
    def _fmt_table(header: str) -> str:
        return f"\n[{header}]"

    def _escape(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    lines: list[str] = []

    # [tool.poetry]
    lines.append(_fmt_table("tool.poetry"))
    lines.append(f'name = "{_escape(name)}"')
    lines.append(f'version = "{_escape(version)}"')
    lines.append(f'description = "{_escape(description)}"')
    if readme:
        lines.append(f'readme = "{_escape(readme)}"')
    if package_includes:
        lines.append("packages = [")
        for pkg in package_includes:
            lines.append(f'    {{ include = "{_escape(pkg)}" }}')
        lines.append("]")

    # [tool.poetry.dependencies]
    lines.append(_fmt_table("tool.poetry.dependencies"))
    lines.append(f'python = "{_escape(python)}"')
    for k, v in dependencies.items():
        lines.append(f'{k} = "{_escape(v)}"')

    # [tool.poetry.group.dev.dependencies]
    if dev_dependencies:
        lines.append(_fmt_table("tool.poetry.group.dev.dependencies"))
        for k, v in dev_dependencies.items():
            lines.append(f'{k} = "{_escape(v)}"')

    # [build-system]
    lines.append(_fmt_table("build-system"))
    lines.append('requires = ["poetry-core"]')
    lines.append('build-backend = "poetry.core.masonry.api"')

    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
