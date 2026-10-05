# Contributing

## Branches
- `main` is always working. Nobody commits to `main` directly.
- Branch name: `<module>/<short-description>` e.g. `vision/live-stream`, `forecasting/xgboost-baseline`.
- Merge through a Pull Request. At least one teammate reviews before merging.

## Commits
Prefix with the module: `vision: add ROI per camera`, `docs: update data contract`. One logical change per commit.

## Daily workflow
```
git checkout main
git pull
git checkout -b vision/my-change
# ... work ...
git add <files>
git commit -m "vision: what changed"
git push -u origin vision/my-change
```
Then open a Pull Request on GitHub.

## Never commit
- Videos, model weights (`*.pt`, `models/`), virtual environments, secrets or API keys (use a `.env` file, which is git-ignored).
- Large files go to Drive; put the link in the module README.

## Shared contracts
`docs/data_contract.md` (CSV columns, traffic levels, API shapes) is shared by everyone. Change it only through a PR that the affected owners approve, and announce it in the group.

## Code style
- Python: clear names, small functions, no hard-coded paths; settings at the top of the file or in arguments.
- Every module README states: how to run, input, output.
