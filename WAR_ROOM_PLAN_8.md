# WAR_ROOM_PLAN_8 — Issue #8: Security hardening (safe-by-default)

## Subtasks

- [ ] 1. Create `security.py` — auth dependency, PDF validation, upload size cap, CORS config, host binding logic
- [ ] 2. Update `main.py` — integrate security module (CORS, auth dep, host binding, upload size cap)
- [ ] 3. Update `docker-compose.yml` — don't publish 8000 by default; use env vars for public exposure
- [ ] 4. Add comprehensive tests for all security features in `tests/test_security_issue8.py`
- [ ] 5. Run tests, fix failures, commit
- [ ] 6. Final cleanup + commit + push
