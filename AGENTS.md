# AGENTS.md

## Cursor Cloud specific instructions

### Overview

**Slackers** is a Django 2.1 library management system (图书馆管理系统) with book search, borrowing/returning, reader profiles, statistics dashboards, and a Django admin panel. It uses SQLite (file-based, shipped as `library.sqlite3`), Bootstrap 3, jQuery, and ECharts for charts.

### Python version requirement

Django 2.1 is **incompatible with Python 3.12** (the system default). Python 3.8 must be installed via the deadsnakes PPA and used via a virtualenv at `/workspace/venv`. The update script handles this automatically.

### Running the dev server

```bash
source /workspace/venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

- Homepage: http://localhost:8000/
- Admin: http://localhost:8000/admin/ (username: `admin`, password: `admin`)
- Search: http://localhost:8000/search/
- Statistics: http://localhost:8000/statistics/

### Running tests

```bash
source /workspace/venv/bin/activate
python manage.py test
```

The test suite is empty (`library/tests.py`) but the test framework runs correctly.

### Key caveats

- **No linter configured** — the project has no flake8/pylint/mypy configuration. `python manage.py check` is the closest equivalent for Django system checks.
- **No build step** — static assets are vendored in `library/static/library/`. No npm/webpack needed.
- **Database is pre-populated** — `library.sqlite3` ships with 194 books and 50 readers. Do not delete it.
- **Admin account** — created via `python manage.py create_admin_account --username admin --password admin`. Already created in the current environment.
- **Reader login** — existing readers log in with their phone number as username and `password` as the password.
- **System dependencies for Pillow** — `libjpeg-dev zlib1g-dev` must be installed for `Pillow==5.2.0` to compile. The update script handles this.
