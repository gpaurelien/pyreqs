# pyreqs
A lib to auto-generate a pyproject.toml based on your dependencies.

## How to use this tool

### A quick example:
    - pyreqs \
    --name "data-processor" \
    --version "2.1.0" \
    --description "Processes CSV files" \
    --python "^3.10" \
    --include "data_processor" \
    --verbose