# Install and use the skill

This repository uses the open Agent Skills layout: the repository root is the skill directory and contains `SKILL.md`. Inspect the files before installing; a skill can influence how an agent reads files and runs tools.

The repository URL is:

```text
https://github.com/abhi8905/swiftui-ui-scalability
```

For unpublished edits, use the local checkout path so an agent can exercise the exact working tree before it is committed and pushed.

## Install from an unpublished checkout

From the root of this skill repository, capture its absolute location:

```bash
pwd
```

Then use one of these development links. Run only the commands for tools you use.

### Codex and Gemini shared user location

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "/absolute/path/to/swiftui-ui-scalability" "$HOME/.agents/skills/swiftui-ui-scalability"
```

Gemini can create and manage its own development link instead:

```bash
gemini skills link "/absolute/path/to/swiftui-ui-scalability" --scope user
```

### Claude Code user location

```bash
mkdir -p "$HOME/.claude/skills"
ln -s "/absolute/path/to/swiftui-ui-scalability" "$HOME/.claude/skills/swiftui-ui-scalability"
```

Before linking, inspect the destination with `ls -ld`. If it already exists, determine whether it is the current source install, a stale copy, or another link. Do not overwrite it blindly.

## Recommended shared installation on macOS

Codex and Gemini CLI both discover user skills in `~/.agents/skills`. Claude Code discovers user skills in `~/.claude/skills`. Keep one canonical checkout and link Claude to it:

```bash
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
git clone https://github.com/abhi8905/swiftui-ui-scalability.git "$HOME/.agents/skills/swiftui-ui-scalability"
ln -s "$HOME/.agents/skills/swiftui-ui-scalability" "$HOME/.claude/skills/swiftui-ui-scalability"
```

If you already cloned the repository elsewhere, link that absolute directory into the same locations. Do not use `ln -f`; inspect and remove or rename an older installation deliberately.

## Codex

### Install

For a user-wide installation, clone or link the complete directory at:

```text
~/.agents/skills/swiftui-ui-scalability/
```

For one repository only, place it under the consuming repository:

```text
<project>/.agents/skills/swiftui-ui-scalability/
```

Codex can also install a skill from GitHub through the built-in `$skill-installer` workflow. Ask Codex:

```text
$skill-installer install https://github.com/abhi8905/swiftui-ui-scalability
```

### Verify and invoke

1. Start Codex in the target project.
2. Open the skills picker with `/skills` or type `$` and confirm `swiftui-ui-scalability` appears.
3. Invoke it explicitly with `$swiftui-ui-scalability`, followed by a concrete review, refactor, or build request.
4. If a newly installed skill is not visible, restart Codex. Skill edits are normally detected automatically.

The optional `agents/openai.yaml` file supplies Codex display metadata and a default prompt. Other agents can safely ignore it.

Codex installations in legacy or application-managed directories may still work, but new shared installations should use `.agents/skills`, which is the current documented cross-client location.

## Gemini CLI

### Install from GitHub

```bash
gemini skills install https://github.com/abhi8905/swiftui-ui-scalability --scope user
```

Use `--scope workspace` instead when only the current project should see it.

### Link the local checkout while developing

```bash
gemini skills link "/absolute/path/to/swiftui-ui-scalability" --scope user
```

### Verify and invoke

1. Start `gemini`.
2. Run `/skills list` and confirm the skill is enabled.
3. After editing the checkout, run `/skills reload`.
4. Ask: `Use the swiftui-ui-scalability skill to review this view and its descendants.`

Gemini asks for consent when installing and when activating a skill. Review the source and approve only the access needed for the task.

## Claude Code

### Install Claude Code if needed

On macOS, the official Homebrew option is:

```bash
brew install --cask claude-code
```

Launch `claude` and complete its sign-in flow.

### Install the skill

For every project, clone or link the complete skill directory at:

```text
~/.claude/skills/swiftui-ui-scalability/
```

For one repository only, use:

```text
<project>/.claude/skills/swiftui-ui-scalability/
```

### Verify and invoke

1. Start Claude Code from the target project.
2. Type `/` and confirm `/swiftui-ui-scalability` is listed.
3. Run `/swiftui-ui-scalability`, followed by the task.
4. Claude can also load the skill automatically when the request matches the frontmatter description.

## Discovery precedence and duplicate copies

Project-scoped skills override user-scoped skills with the same name in Gemini CLI, and coding agents generally prefer the most local applicable configuration. If a change does not appear, check for duplicate `swiftui-ui-scalability` directories before editing the skill again.

Useful checks:

```bash
find "$HOME/.agents/skills" "$HOME/.gemini/skills" "$HOME/.claude/skills" -maxdepth 2 -name SKILL.md -print 2>/dev/null
gemini skills list
```

In Codex, use `/skills`; in Claude Code, type `/`. Confirm which scope or path supplied the listed skill.

## Xcode 27

Xcode is the host; the selected coding agent consumes the skill. Do not drag this repository into the project navigator, add it to a target, or include it in Copy Bundle Resources.

### Project-scoped setup for a team

The cleanest cross-agent setup is a Git submodule at the shared Codex/Gemini location plus a relative Claude link:

```bash
cd "/absolute/path/to/YourApp"
git submodule add https://github.com/abhi8905/swiftui-ui-scalability.git .agents/skills/swiftui-ui-scalability
mkdir -p .claude/skills
ln -s ../../.agents/skills/swiftui-ui-scalability .claude/skills/swiftui-ui-scalability
git add .gitmodules .agents/skills/swiftui-ui-scalability .claude/skills/swiftui-ui-scalability
```

After cloning the app repository elsewhere, initialize the skill with:

```bash
git submodule update --init --recursive
```

If the team does not want a submodule, copy the skill into both agent locations or document a local linking step. Avoid committing absolute symlinks because they only work on the original machine.

### Enable and verify in Xcode

1. Open **Xcode > Settings > Intelligence**.
2. Install or enable Codex, Gemini, or Claude Agent, then sign in to that provider.
3. Open the app project and the coding assistant, then select that agent.
4. Type `/` to inspect available skills. If the selected agent uses its own invocation syntax, explicitly ask: `Use the swiftui-ui-scalability skill ...`.
5. Run a read-only review first and confirm that the response cites this skill's layout, geometry, accessibility, and validation guidance.

Xcode keeps provider-specific global configuration under:

```text
~/Library/Developer/Xcode/CodingAssistant/codex
~/Library/Developer/Xcode/CodingAssistant/gemini
~/Library/Developer/Xcode/CodingAssistant/ClaudeAgentConfig
```

Those settings apply only when the agent is launched inside Xcode. Prefer project-scoped installation when a repository should behave consistently for the whole team.

If a user-wide terminal installation does not appear inside Xcode, use the project-scoped setup above or place the skill in the selected provider's Xcode-only configuration using that provider's normal skill layout. Keep Xcode-only copies linked to the canonical checkout to prevent version drift.

### Let terminal agents build and test through Xcode

This is optional and separate from installing the skill.

1. In **Xcode > Settings > Intelligence**, enable **Allow external agents to use Xcode tools**.
2. Connect Codex:

   ```bash
   codex mcp add xcode -- xcrun mcpbridge
   codex mcp list
   ```

3. Connect Claude Code:

   ```bash
   claude mcp add --transport stdio xcode -- xcrun mcpbridge
   claude mcp list
   ```

4. Keep the relevant Xcode workspace open, then ask the terminal agent to build, run tests, or inspect previews using Xcode tools.

## Smoke-test prompt

Use this read-only prompt in every installed agent:

```text
Use the swiftui-ui-scalability skill. Review the selected SwiftUI root view and its descendants without editing. Identify the actual parent constraint, Dynamic Type and localization risks, state or focus continuity risks, minimum supported OS, and a concrete validation matrix. Distinguish static evidence from runtime checks that were not executed.
```

A successful smoke test should be specific to the project, preserve scope, avoid device-name-only breakpoints, treat `GeometryReader` as a last resort rather than banning it, and clearly state which runtime checks remain.

## Update or uninstall

For a Git checkout, update without creating a merge commit:

```bash
git -C "$HOME/.agents/skills/swiftui-ui-scalability" pull --ff-only
```

For Gemini-managed installations, inspect the available version, then reinstall when the repository changes:

```bash
gemini skills list
gemini skills uninstall swiftui-ui-scalability --scope user
gemini skills install https://github.com/abhi8905/swiftui-ui-scalability --scope user
```

For development links, changes are visible immediately after the agent reloads its skill inventory. To uninstall a link, first verify it with `ls -ld`, then use `unlink` on that exact link. Do not recursively delete a path until you know whether it is a link or the canonical checkout.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Skill is not listed | The directory must contain an uppercase `SKILL.md`; install the whole directory, then restart Codex/Claude or run Gemini `/skills reload`. |
| Old instructions still load | Search user, workspace, Xcode-only, and legacy locations for another skill with the same `name`. |
| Gemini refuses activation | Review the source and respond to its installation/activation consent prompt. |
| Xcode does not show the skill | Confirm the selected provider is enabled and signed in, the app repository is the open project root, and the provider can discover its project-scoped skill path. |
| Agent recommends unavailable APIs | Include the app target, deployment version, active Xcode version, and exact SDK in the prompt; the skill requires overload-level availability checks. |
| Review edits files unexpectedly | Stop the run and restate that the action is review-only. The skill's action contract treats review as read-only. |

## Clean-install acceptance check

A release candidate is ready only when a fresh directory—not the author's existing personal install—passes all of these checks:

1. The agent lists `swiftui-ui-scalability` from the intended scope.
2. Explicit invocation opens the skill without broken-reference errors.
3. A read-only smoke test inspects callers and descendants but changes no files.
4. The result separates static findings from unexecuted runtime checks.
5. The result respects the target's current minimum OS.
6. Removing or disabling the test installation makes the skill disappear, proving that a stale duplicate was not used.

## Official setup references

- [OpenAI: Build skills](https://developers.openai.com/codex/skills)
- [Gemini CLI: Managing Agent Skills](https://geminicli.com/docs/cli/using-agent-skills/)
- [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [Apple: Extending and customizing agents](https://developer.apple.com/documentation/Xcode/extending-and-customizing-agents)
- [Apple: Giving external agents access to Xcode](https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode)
