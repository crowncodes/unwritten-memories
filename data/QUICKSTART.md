# Unwritten Quick Start Guide

## Initial Setup

### 1. Activate Virtual Environment

Your virtual environment is already created! Just activate it:

**Windows (PowerShell):**
```powershell
.\unwritten-env\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\unwritten-env\Scripts\activate.bat
```

### 2. Install/Update Dependencies

Install the missing dependency for settings management:

```bash
pip install pydantic-settings
```

Or reinstall all dependencies from scratch:

```bash
pip install -r requirements.txt
```

### 3. Install the Package in Development Mode

This allows you to import `unwritten` from anywhere:

```bash
pip install -e .
```

## Running the Application

### Method 1: Using the CLI command

After installing in development mode:

```bash
unwritten
```

With options:
```bash
unwritten --verbose
unwritten --config path/to/config.yaml
```

### Method 2: As a Python module

```bash
python -m unwritten.main
```

### Method 3: Using Make (if you have make installed)

```bash
make run
```

## Configuration

### Environment Variables

Create a `.env` file in the project root (copy from example):

```bash
# On Windows PowerShell
Copy-Item .env.example .env

# Then edit .env with your values
notepad .env
```

Example `.env` contents:
```
DEBUG=False
LOG_LEVEL=INFO
WANDB_API_KEY=your_wandb_key_here
HF_TOKEN=your_huggingface_token_here
```

## Development Workflow

### Running Tests

```bash
pytest tests/ -v
```

### Code Formatting

If you have black installed:
```bash
black src/ tests/
```

### Adding New Dependencies

1. Add to `requirements.txt`
2. Add to `pyproject.toml` dependencies section
3. Install: `pip install -r requirements.txt`

## Project Structure

```
unwritten/
├── src/unwritten/           # Main source code
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Entry point with CLI
│   ├── config/             # Configuration management
│   │   ├── settings.py     # Pydantic settings
│   │   └── __init__.py
│   ├── models/             # Data models
│   │   └── __init__.py
│   └── utils/              # Utility functions
│       ├── logging.py      # Logging setup
│       └── __init__.py
├── tests/                  # Test files
│   ├── test_main.py
│   └── __init__.py
├── data/                   # Data files (gitignored)
├── notebooks/              # Jupyter notebooks (gitignored)
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Modern Python project config
├── README.md               # Project documentation
└── .gitignore              # Git ignore rules
```

## Next Steps

1. **Update README.md** with your project description
2. **Configure .env** with your API keys
3. **Start coding** in `src/unwritten/`
4. **Write tests** in `tests/`
5. **Add your models** in `src/unwritten/models/`

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Install in editable mode
pip install -e .

# Run the app
python -m unwritten.main

# Run tests
pytest

# Format code
black src/ tests/

# Clean cache files
find . -type d -name "__pycache__" -exec rm -rf {} +  # Linux/Mac
# Or manually delete __pycache__ directories on Windows
```

## Troubleshooting

### Import errors

If you get import errors:
1. Make sure virtual environment is activated
2. Install in development mode: `pip install -e .`

### Missing dependencies

```bash
pip install -r requirements.txt
```

### Pydantic settings errors

```bash
pip install pydantic-settings
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/)

Happy coding! 🚀

