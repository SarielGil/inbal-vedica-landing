# Repository workflow

## Publishing

- In this repository, a bare user request to "push" after a completed website task means: commit only the files from that task and push the verified commit directly to `origin/main`.
- Do not create a pull request, require the GitHub CLI (`gh`), or introduce a feature branch unless the user explicitly asks for a branch or PR.
- Always inspect `git status -sb`, the relevant unstaged diff, and the staged diff before committing.
- In a mixed worktree, stage explicit task-scoped paths. Never use `git add -A` or include unrelated user files, audit logs, skills, scripts, or generated output.
- Run checks appropriate to the changed files and use a terse commit message describing the task.
- Publish committed work with `scripts/push_to_main.sh`. It permits only a fast-forward update and verifies the remote commit after pushing.
- Never force-push `main`. If `origin/main` is not an ancestor of `HEAD`, stop and report the divergence.

## Generated and audit files

- `.playwright-cli/` and `output/` are local browser-test artifacts and are not source files.
- `seo-logs/` contains intentional audit history. Include new reports only when the active task asks to save or publish an audit; do not bundle them into an unrelated website-content commit.
- Preserve unrelated local changes and untracked files unless the user explicitly places them in scope.
