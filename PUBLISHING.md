# GitHub publishing and release checklist

Target repository: `abhi8905/swiftui-ui-scalability`

The repository already exists at `https://github.com/abhi8905/swiftui-ui-scalability`. Use this checklist for the documentation update and later releases.

## Repository decisions

- Confirm whether the repository is public or private. Public is the practical choice for URL-based installation by other developers.
- Choose a license before making the repository public. Public visibility alone does not grant permission to reuse the work.
- Confirm the repository name and owner, then update the URL in `README.md` or `INSTALL.md` if either changes.
- Decide whether GitHub Issues should be enabled for compatibility reports and SwiftUI guidance corrections.
- Suggested repository description: `Agent Skill for adaptive SwiftUI layouts across iPhone, iPad, resizable windows, Dynamic Type, and localization.`
- Suggested topics: `swiftui`, `agent-skills`, `codex`, `gemini-cli`, `claude-code`, `xcode`, `accessibility`.

## Prepare a change

```bash
python3 scripts/validate_skill.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git add .
git commit -m "Document cross-agent skill installation"
```

Inspect the staged and committed content before publishing:

```bash
git status --short
git log -1 --stat
git ls-files
```

Run a credential and private-path check before every first publication:

```bash
rg -n 'BEGIN [A-Z ]*PRIVATE KEY|g''hp_[A-Za-z0-9]{20,}|github_''pat_[A-Za-z0-9_]{20,}|s''k-[A-Za-z0-9]{20,}|/Use''rs/[^/]+/' . --hidden --glob '!.git/**'
```

The expected result is empty. Review every match rather than adding a broad exclusion.

## Authenticate GitHub CLI

```bash
gh auth login -h github.com -w
gh auth status
```

Complete the browser flow as the intended owner, `abhi8905`. Do not paste a personal access token into repository files, terminal history, issues, or chat.

## Push the existing repository

Confirm the configured remote, then push the current branch:

```bash
git remote -v
git push -u origin main
```

For normal follow-up work, prefer a topic branch and pull request rather than pushing directly to a protected `main` branch.

## Post-push checks

1. Confirm the default branch is `main` and the validation workflow passes.
2. In repository settings, require the `validate` job on pull requests before merging to `main`.
3. Open every link in `README.md`, `INSTALL.md`, and `references/sources.md` that is important to installation or API compatibility.
4. Test a clean Gemini installation from the repository URL.
5. Test a clean Codex install or clone under `.agents/skills`.
6. Test a clean Claude clone under `.claude/skills` after Claude Code is installed.
7. Test Xcode discovery from a small sample app using the project-scoped layout in `INSTALL.md`.
8. Create a version tag only after the clean-install smoke tests pass:

   ```bash
   git tag -a v1.0.0 -m "SwiftUI UI Scalability skill v1.0.0"
   git push origin v1.0.0
   ```

9. Add a short GitHub release summary that states the Xcode/iOS baseline and links to the installation guide.

## Update workflow

For later changes, update sources and compatibility dates only when reverified, run both validators, review the diff, push to a branch, and merge through a pull request after CI passes. Keep installation paths stable so existing clones, submodules, and links continue working.
