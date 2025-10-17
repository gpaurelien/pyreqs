import ast
import logging
import os
from typing import Optional, Union


class Parser:
    """Parses files through a given directory."""

    def __init__(self):
        self.directory: str = os.getcwd()
        self.filespath: dict[str, list[str]] = {}

    def get_imports_from_file(self, filepath: str) -> set:
        imports = set()
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=filepath)
            except SyntaxError as err:
                raise err

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for p in node.names:
                    imports.add(p.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
        return imports

    def scan_project_for_imports(self) -> set:
        imports = set()
        for path, _, files in os.walk(self.directory):
            # TODO: exclude some folder names, e.g, .venv, __pycache__, etc...
            directory: str = path.split("/")[-1]
            self.filespath[directory] = []
            for f in files:
                if f.endswith(".py"):
                    imports |= self.get_imports_from_file(os.path.join(path, f))
                    self.filespath[directory].append(f)
        return imports
