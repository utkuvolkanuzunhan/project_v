# project_v (short English summary of AGENTS.md, for Antigravity and agy)

This is a PUBLIC repository holding lesson image packs (`paketler/`, `katalog.json`) for the *** app,
plus the tools, plans and curriculum tree that produce them. `AGENTS.md` is the single source of rules.

1. Read `plan/DEVIR.md` first, then `YAPI.md`. Do not read big manifests end to end.
2. Never write keys, tokens, passwords or personal data: the repository is public.
3. Never `git push` without the owner's approval. No force push, no history rewrite.
4. Do not hand-edit published packs (`paketler/**`, `katalog.json`); they change only through `calisma_klasoru/araclar/yayin.py`.
5. Do not add or update dependencies, delete or move files without approval.
6. No Turkish characters in file or folder names. Notes are in Turkish, image prompts in English.
7. Test: `python -m unittest discover -s testler` (standard library only).
8. There are no git hooks or CI guards here: follow these rules by hand.
