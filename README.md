# SwiftUI UI Scalability skill

An Agent Skill for reviewing, refactoring, and building SwiftUI layouts that remain usable across iPhone and iPad constraints, resizable windows, Dynamic Type, localization, keyboard presentation, and stateful layout transitions.

The skill is instruction-only. It does not add a Swift package, source file, framework, or runtime dependency to an app.

## Compatibility

| Tool | Support | Invocation |
| --- | --- | --- |
| Codex CLI, IDE extension, and app | Native Agent Skills | `$swiftui-ui-scalability` or automatic matching |
| Gemini CLI | Native Agent Skills | Ask for the skill by name or let Gemini match its description |
| Claude Code | Native Agent Skills | `/swiftui-ui-scalability` or automatic matching |
| Xcode 27 coding intelligence | Uses the selected agent's skill discovery | Type `/` in Xcode or ask the selected agent to use the skill |

See [INSTALL.md](INSTALL.md) for global, project-local, and Xcode setup.

For a local checkout that has not been published yet, run the development-link commands in [Install from an unpublished checkout](INSTALL.md#install-from-an-unpublished-checkout). This lets every available agent use the exact files being prepared for GitHub.

## Example prompts

```text
$swiftui-ui-scalability review ContentView.swift and its child views for iPhone and iPad resizing issues. Do not edit files.
```

```text
Use the swiftui-ui-scalability skill to refactor ProfileEditor so entered text, focus, and scroll position survive width changes. Keep the current deployment target.
```

```text
/swiftui-ui-scalability audit this SwiftUI screen at narrow widths, large accessibility text, long localized strings, RTL, and keyboard presentation.
```

## Repository contents

- `SKILL.md` — the routing instructions agents load first.
- `references/` — focused layout, geometry, accessibility, compatibility, and validation guidance.
- `agents/openai.yaml` — optional Codex presentation metadata.
- `scripts/validate_skill.py` — dependency-free structural and portability checks.
- `.github/workflows/validate.yml` — runs validation on pushes and pull requests.
- `PUBLISHING.md` — the repository creation and GitHub release checklist.

## Validate locally

```bash
python3 scripts/validate_skill.py
```

Codex maintainers can additionally run the validator bundled with the skill-creator skill:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## Source baseline

The SwiftUI guidance is independently authored and currently verified against Xcode 27 / iOS and iPadOS 27, with older availability called out where relevant. See [references/sources.md](references/sources.md) for primary sources, compatibility notes, and attribution.

## Scope and safety

The skill may inspect project settings, parent/child SwiftUI views, and relevant runtime evidence. A review request remains read-only; file changes require an explicit refactor, fix, or build request. The skill does not require network access, credentials, an MCP server, or scripts to perform a source review.
