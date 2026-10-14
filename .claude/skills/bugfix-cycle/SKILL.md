---
name: bugfix-cycle
description: End-to-end bug-fix cycle for this requests fork — hunt for a real bug, fix it with a red-green test, commit and push to the working branch, open a PR to main, watch CI, merge only when the user confirms, and post the summary to Slack #555. Use this whenever the user (usually writing in Spanish) says things like "busca otro bug real", "abre el PR a main y vigílalo", "avísame cuando estén los tests", "fusiónalo en main", "publícalo en #555" or "qué sigue", even if they only name one step — each step has conventions here that the others depend on.
---

# Bug-fix cycle for the requests fork

This repo is `johanriveraprojects-prog/requests`, a fork of psf/requests. The user drives the work one step at a time in Spanish and expects replies in Spanish. Each step below usually ends with a short report and a question offering the next step; don't run ahead to the next step (especially opening a PR or merging) without the user asking.

## Environment

- Python env: `/home/user/requests/.venv` (created by the SessionStart hook). Use `.venv/bin/python`, `.venv/bin/pytest`, `.venv/bin/ruff`, `.venv/bin/pyright`.
- Working branch: the one named in the session instructions (so far `claude/determined-ramanujan-5njgnj`). Never push elsewhere.
- Full suite command — the cloud sandbox can't reach the tarpit host, so exclude those 5 tests (they pass in CI):
  ```bash
  .venv/bin/pytest -q -k "not (TestTimeout and connect)"
  ```
- Lint/format/types:
  ```bash
  .venv/bin/ruff check src tests
  .venv/bin/ruff format --check <changed files only>   # tests/test_lowlevel.py is pre-existing unformatted; don't touch it
  .venv/bin/pyright src/requests/
  ```

## 1. Hunt for a real bug

The goal is a bug a real caller can hit, not a style nit or a speculative edge case.

- Probe with small throwaway scripts (`.venv/bin/python - <<'EOF' ... EOF`) that call the public API with realistic inputs: header values servers actually send, URLs users actually type, formats the stdlib itself produces.
- Good hunting grounds are code paths with low test coverage (`pytest --cov=requests --cov-branch --cov-report=term-missing`) and places that implement an RFC partially — compare against the RFC or against what the stdlib does.
- Before calling something a bug, check that it isn't intended upstream behaviour and that the symptom is concrete (exception, wrong header, request silently going through the proxy, auth silently not sent...). If you're unsure whether a finding is a real bug, say so instead of fixing it.
- Past finds, for calibration: `iter_lines` spurious empty lines, `parse_header_links` splitting inside `<...>`, schemeless proxy URLs, Digest `qop` lists with spaces, `multiple_domains`, `no_proxy` IP:port, `morsel_to_cookie` RFC 1123 dates, Digest `-sess` algorithms.

## 2. Fix with a red-green test

1. Make the smallest change that fixes the root cause; match the surrounding code style and comment density.
2. Add a test next to related tests (`tests/test_utils.py`, `tests/test_requests.py`, `tests/test_lowlevel.py` for raw-socket cases). When httpbin can't produce the case, compute the expected value independently in the test (e.g. recompute a Digest response from the RFC formula).
3. Prove the test catches the bug — revert only the source file, run the new test, see it fail, restore:
   ```bash
   git stash -q -- src/requests/<file>.py && .venv/bin/pytest -q <test file> -k <name>; git stash pop -q
   ```
4. Run the full suite, ruff, ruff format and pyright (commands above). Report real numbers from this run, not earlier ones.
5. Add a bullet under `dev` → `**Bugfixes**` (or `**Improvements**`) in `HISTORY.md`: what works now, then "It used to …" describing the old symptom.

## 3. Commit and push

- Commit message: imperative subject (≤ ~60 chars), blank line, a short paragraph on the cause and the fix. End with the attribution trailers given in the session's system reminder. Never put a model name or ID in commits, PRs or code.
- `git push -u origin <branch>`; on network errors retry up to 4 times with 2s/4s/8s/16s backoff.
- Report to the user in Spanish: a before/after table of the symptom, the cause, the fix, the test evidence, the commit hash — then ask whether to open the PR to `main` and watch it.

## 4. Open the PR and watch it (only when asked)

PR body structure (English, like the rest of the repo):

```
## Summary
<one paragraph> + before/after table or short code example
## Change
- file: what changed; what still behaves as before
## Tests
- new tests and that they fail without the fix
- full suite count, ruff/pyright clean
<attribution footer from the session's system reminder>
```

Then:
- `subscribe_pr_activity` for the PR and `send_later` a check-in ~50 minutes out (re-arm ~4h apart while it only waits; stop after 3 unchanged check-ins and tell the user once).
- CI runs **twice** per commit: a `pull_request` run and a `push` run. Check both — `mergeable_state: "unstable"` often comes from a failure in the push run only.
- Known flake: `test_pyopenssl_redirect` on Windows with `ConnectionAbortedError 10053`. If it fails and the same job passed on the same commit in the other run, re-run the failed job once (`rerun_failed_jobs`) and tell the user. A second failure is real and must be investigated.
- If Tests runs sit in `queued` for a long time, check `.github/workflows/run-tests.yml` for `concurrency` before blaming GitHub, and tell the user to look at Settings → Actions.
- Report CI as a table (Tests / Lint / Type Check / zizmor). Only say "en verde" after reading the results of this commit.

## 5. Merge (only on explicit confirmation)

Merge only when the user says so ("Fusiónalo en main"). If Tests haven't finished, say so plainly in the reply — don't present the merge as CI-verified. After merging:

```bash
git fetch -q origin main && git merge --ff-only -q origin/main && git push -q -u origin <branch>
```

Also `unsubscribe_pr_activity` and delete any pending check-in trigger.

## 6. Post to Slack #555 (when asked)

Channel `#555`, ID `C0C7JMQAPQ8`. Message in Spanish:

```
**✅ Fusionado en `main`: <título corto>** ([PR #N](<url>))

**Bug:** <síntoma y causa en 1–2 frases>
<tabla antes/después o ejemplo de código>

**Arreglo:** <1 frase; qué sigue igual>

**Tests:** <casos nuevos, fallan sin el arreglo>. Suite local: <N> pasados.
**CI:** <resultado real; menciona flakes o tests que no llegaron a ejecutarse>
```

Return the message link to the user and offer the next step (usually: buscar otro bug).
