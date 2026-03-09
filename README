# FicHub.net

> A frontend for generating ebooks from web fiction (fanfic & web serials).

[![License](https://img.shields.io/badge/license-AGPL%203.0-blue.svg)](#license)

FicHub.net assembles EPUB, MOBI, and PDF documents using metadata and content
provided by external services.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Support](#support)
- [License](#license)
- [Contact](#contact)

## Features

- Export ebooks in multiple formats (EPUB/MOBI/PDF).
- Integrates with the Alexandria API for metadata and content lookup.
- Uses Elasticsearch for search fallback.
- Configurable caching and asset directories.

## Prerequisites

- Python 3.14 or later (see `pyproject.toml`).
- PostgreSQL database.
- Elasticsearch instance.
- Calibre (for MOBI/PDF exports).
- Node.js/TypeScript and Sass (optional, for frontend builds).

## Development Setup

The easiest way to get started is with the Docker‑based development
environment described in [dev-docker-compose/README](dev-docker-compose/README).

### Python environment

```sh
# create and activate a uv-managed virtual environment
uv venv

# install the package and development requirements
uv pip install . --group dev
```

### Frontend assets

Compile TypeScript and Sass using the `make frontend` helper:

```sh
make frontend
```

Alternatively, install the Node toolchain directly and run your preferred
build commands.

### Configuration

Copy example configuration files and adjust credentials as needed:

```sh
cd src/fichub_net
cp authentications.ex.py authentications.py
cp rl_conf.ex.py rl_conf.py
```

Set environment variables such as `OIL_DB_DBNAME`. For non-env settings,
update `authentications.py` (API/Elasticsearch endpoints) and `ebook.py`
(cache directories).

## Deployment

See the [FicHub/infra-dev](https://github.com/FicHub/infra-dev) repository for
production deployment instructions using Docker.

## Support

Join the community for help and discussion:

- **IRC:** `##fichub` on Libera.Chat
- **Discord:** <https://discord.gg/sByBAhX>

Consider supporting the project maintainer on Patreon:
<https://www.patreon.com/irides>

## License

This project is released under the **GNU Affero General Public License v3.0 or
later**. See the [LICENSE](LICENSE) file for full text.

## Contact

For questions, bug reports, or contributions, use the channels listed under
[Support](#support).
