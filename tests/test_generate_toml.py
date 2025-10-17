import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def test_generate_toml_creates_actual_pyproject_toml_in_project_root():
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from pyreqs.utils import generate_toml  # type: ignore

    out_path = root / "pyproject.toml"

    if out_path.exists():
        out_path.unlink()

    generate_toml(
        name="pyreqs-demo",
        version="0.0.1",
        description="Temporary test pyproject",
        readme="README.md",
        package_includes=["pyreqs"],
        python="^3.10",
        dependencies={"requests": "^2.32.0"},
        dev_dependencies={"pytest": "^8.3.0"},
        output=str(out_path),
    )

    assert out_path.exists(), "pyproject.toml should be created at project root"
    content = out_path.read_text(encoding="utf-8")
    assert "[tool.poetry]" in content
    assert 'name = "pyreqs-demo"' in content
    assert "[build-system]" in content
