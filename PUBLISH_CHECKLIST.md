# Publishing checklist — Frank Yip

This repo is meant to be a **separate, public, synthetic-data portfolio project**.

1. Work from a **new, isolated directory**. Never copy files or Git history from any existing private repositories or employer projects.
2. Examine every file and ensure there are no tokens, private data, internal URLs, customer names, employer code, or proprietary business configuration.
3. Run `python -m pytest -q` and start the dashboard locally. Review its behaviour and be prepared to explain every component in an interview.
4. Check `git status`, `git diff --check`, and check the exact staged file list.
5. Create a new repository named `agent-ops-reference` under `cktsang599` with **public visibility only after explicit account-owner approval**.
6. Ensure `.env`, `*.sqlite3`, caches, test logs and system secrets stay untracked. Do not give GitHub CLI credentials to the repository or in this chat.
7. Confirm `https://github.com/cktsang599/agent-ops-reference` loads **without logging in**, and GitHub Actions tests pass.
8. Preferred code sample for the application: `agent_ops/planner.py` and `tests/test_engine.py`. Reference the repo README so reviewers see policy boundaries and limitations.

This is **not** the proprietary system mentioned on the CV. Explain that it is an independent demonstration of an approach used in production work.
