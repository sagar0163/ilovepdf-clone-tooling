# Issue 9 Plan
- [x] Add `USER` directive to Dockerfile, create user and make `/app/output` writable.
- [x] Remove duplicate pip install in Dockerfile.
- [x] Replace or remove dead `CMD` in Dockerfile.
- [x] Add `.dockerignore` ignoring uploads/, output/, .git, __pycache__, *.pdf, .venv, x.
- [x] Pin dependencies in `requirements.txt`.
- [x] Remove `pdf-tools` sidecar and `version:` from `docker-compose.yml`.
