# Issue 9 Plan
- [ ] Add `USER` directive to Dockerfile, create user and make `/app/output` writable.
- [ ] Remove duplicate pip install in Dockerfile.
- [ ] Replace or remove dead `CMD` in Dockerfile.
- [x] Add `.dockerignore` ignoring uploads/, output/, .git, __pycache__, *.pdf, .venv, x.
- [ ] Pin dependencies in `requirements.txt`.
- [x] Remove `pdf-tools` sidecar and `version:` from `docker-compose.yml`.
