# Testing

1. Install a project in **editable mode** (i.e.  setuptools "develop mode") from a local project path using the following command:

```bash
pip install -e . 
```

or

```bash
pip install --editable .
```

2. Write your tests under the tests folder with the file prefix as `test_<test-name>.py`
3. Run tests using Pytest

```bash
pytest
```

or run a specific test using the command:

```bash
pytest tests/test_get_files.py
```
