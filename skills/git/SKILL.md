---
name: git
description: Safely synchronize a Git repository with its remote by inspecting status, fetching, committing relevant local changes, rebasing when behind, pushing, and verifying the result. Use whenever the user asks to sync Git, commit and push, pull latest changes, rebase and push, inspect branch status, or keep a repository up to date.
---

# Git synchronization

Use this skill for routine repository synchronization. The target state is a
working branch whose relevant local work is committed and whose local and
remote branch tips agree, with no work lost and no shared history rewritten.

## Repository-specific exclusions

In `/Users/hulaizh/.kimi-code`, these directories are local-only:

- `teaching/`
- `/docs/`
- `/ai-finance-skills-workspace/`

Keep them ignored and never stage or push files under them during routine
synchronization. Check the staged path list before committing so these paths
cannot enter the commit accidentally.

## Safety rules

- Do not force-push `main` or `master`, rewrite shared history, amend a commit
  you did not author, or bypass hooks with `--no-verify`.
- Stage files by explicit path. Do not use `git add -A` or `git add -u`.
- Never stage secrets such as `.env`, credentials, private keys, or tokens.
- Do not stage `data/` or `temp/` symlinks or their contents.
- Before staging a file, check its size and leave files at or above 50 MB
  untracked; add an appropriate ignore rule instead.
- Stop if a rebase, merge, cherry-pick, or other Git operation is already in
  progress, if `HEAD` is detached, or if there is no remote.
- If a conflict or unexpected remote change cannot be resolved with certainty,
  abort the in-progress rebase, report the conflicting paths, and stop.
- History removal is a separate, explicitly requested operation. Do not turn a
  routine sync into a history rewrite.

## Workflow

1. Inspect the repository in parallel:

   ```bash
   git status --short --untracked-files=all
   git branch -vv
   git remote -v
   ```

   Confirm the current branch, operation state, changed paths, and remote
   before making changes.

2. Fetch remote state without changing the worktree:

   ```bash
   git fetch --all --prune
   ```

3. If the worktree is clean and the branch is neither ahead nor behind, report
   that it is already in sync and stop.

4. If there are local changes, review them and stage only the named files that
   belong to the current request. Recheck the staged path list, excluded
   directories, sensitive files, and file sizes. Commit with a message in the
   form `<type>: <summary>`; use `feat`, `fix`, `docs`, `refactor`, `test`, or
   `chore` as the type. Add a body line when the summary does not explain why
   the change was made.

5. If the branch is behind its upstream, rebase the local commits:

   ```bash
   git pull --rebase origin <branch>
   ```

   Resolve only conflicts whose intended result is certain. Otherwise abort
   the rebase and report the conflicting files.

6. If the branch is ahead, push it and establish upstream tracking when needed:

   ```bash
   git push -u origin HEAD
   ```

   If the push is rejected because the remote moved, fetch and repeat the
   rebase-and-push steps once. Stop after a second rejection.

7. Verify the result:

   ```bash
   git status
   git branch -vv
   git log --oneline -3
   ```

   Report what was committed, pulled, and pushed, or the exact step and files
   that blocked synchronization.
