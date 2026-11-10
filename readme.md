# What is this?

This is a practice project for testing out django. I needed a place to store job application details, and this was more fun than a spreadsheet.

# Dependencies 

This uses [uv](https://docs.astral.sh/uv/) for dependencies. 

A previous version was dockerized. Maybe I'll patch that up some day!

## Important tooling
- Django
- Django rest framework
- Pytest
- Ruff

# Running it
- Create a `.env` file
  - Add a `SECRET_KEY` for django (it can be any string)
  - Add `DB_ENGINE` (`django.db.backends.sqlite3` only supported right now)
- run `uv run python manage.py runserver 0.0.0.0:8000` to start it locally
- Go to `http://localhost:8000/admin/` in your browser

# Tests and code quality
- Run them with `uv run pytest`
- All the tests should pass
  - Even playwright
- Ruff linter and formatter should be happy
    - `uv run ruff check` for the linter
    - `uv run ruff format` for the formatter


# Future plans
- Dockerize
- Set up waitress or gunicorn
- Add more features
- Deploy someplace