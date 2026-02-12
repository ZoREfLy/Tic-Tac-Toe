# Phase 5: Documentation & Polish

## Context
Final cleanup — update all docs, add requirements.txt, update CLAUDE.md, update .gitignore.

## 5.1 `requirements.txt` — DONE
Already created with correct content:
```
numpy>=1.24
flask>=3.1
pytest>=8.0
```

## 5.2 Update `CLAUDE.md` — DONE
Already updated with:
- New file structure
- New run commands: `python3 cli.py` (terminal), `python3 -m web.app` (web)
- Architecture description matching new modules
- Test command: `pytest tests/ -v`

## 5.3 Update `.gitignore` — TODO (partial)
Current `.gitignore`:
```
.DS_Store
__pycache__/
*.dat
.venv/
plans/
```

Remaining changes:
- Add `models/` (ignore model files but keep dir via `.gitkeep`)
- Add `*.pyc`

## 5.4 Add `models/.gitkeep` — TODO
`models/` directory exists (contains `p1.dat`, `p2.dat`) but has no `.gitkeep`.
Add `.gitkeep` so the directory is tracked even when `models/` contents are ignored.

## Tests for Phase 5
```bash
# Run full test suite — everything from all phases should pass
pytest tests/ -v
```

## Verification
```bash
pytest tests/ -v              # all tests pass
python3 cli.py                 # CLI works
python3 -m web.app             # web works at localhost:5000
```

## Git
```bash
git add -A && git commit -m "docs: update documentation, requirements, and gitignore"
```
