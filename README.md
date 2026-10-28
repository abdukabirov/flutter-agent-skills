# flutter-agent-skills

Open-source agent skills for **Flutter and Dart**. Each skill is a folder with a `SKILL.md` that teaches an AI coding agent (Claude Code, OpenCode, Cursor and others that read the `SKILL.md` format) how to do one Flutter task the way an experienced developer would.

> Status: early. Skills are added by the community, see [CONTRIBUTING.md](CONTRIBUTING.md).

Skills are checked by comparing the same task with and without the skill before a skill is marked as verified. Only `flutter-ui-from-design` has results in this repository; the other three remain experimental. Skills that do not help may be removed, and the evidence stays in docs/evidence.

## Why this exists

These skills focus on recurring Flutter tasks: implementing UI from a visual reference, migrating state to Riverpod, configuring go_router navigation, and writing reliable tests. They collect practical checks for problems such as layout mistakes, state-lifecycle errors, navigation regressions, and weak test coverage.

## Tested

| Skill | What it does | Verified |
|-------|--------------|----------|
| [flutter-ui-from-design](skills/flutter-ui-from-design/SKILL.md) | Builds responsive Flutter UI from screenshots and design references | [Tested in two small A/B rounds; valid-run comparison passed, with replacement-selection bias (2026-10-27)](docs/evidence/flutter-ui-from-design.md) |

## Experimental (not tested yet)

| Skill | What it does | Verified |
|-------|--------------|----------|
| [flutter-state-to-riverpod](skills/flutter-state-to-riverpod/SKILL.md) | Migrates `setState` and `Provider` code to Riverpod step by step | Not yet compared against an agent without the skill. Use at your own risk. |
| [flutter-go-router](skills/flutter-go-router/SKILL.md) | Sets up navigation with `go_router`: routes, redirects, deep links | Not yet compared against an agent without the skill. Use at your own risk. |
| [flutter-testing](skills/flutter-testing/SKILL.md) | Writes unit, widget and golden tests that actually test something | Not yet compared against an agent without the skill. Use at your own risk. |

## Removed after testing

| Skill | Evidence |
|-------|----------|
| flutter-widget-review | [No measurable benefit over the agent without the skill.](docs/evidence/flutter-widget-review.md) |
| flutter-release-checklist | [No measurable benefit over the agent without the skill.](docs/evidence/flutter-release-checklist.md) |
| flutter-scoped-changes | [No measurable benefit over the agent without the skill.](docs/evidence/flutter-scoped-changes.md) |

Missing a skill you need? Open an issue with the **Skill request** template.

## Install

Tested with GitHub Copilot agent mode in VS Code. In our tests the agent did
not discover the skill from .github/skills on its own: its skill tool listed
it as unavailable, and it used the skill only when the prompt told it to read
the file. Name the skill in your prompt and check the agent's output for
evidence that it read it. For Claude Code, install into ~/.claude/skills or
.claude/skills.

Copy the skills you want into your agent's skills directory.

```bash
git clone https://github.com/abdukabirov/flutter-agent-skills.git

# Claude Code, personal skills
mkdir -p ~/.claude/skills
cp -r flutter-agent-skills/skills/* ~/.claude/skills/

# Claude Code, one project only
mkdir -p your-project/.claude/skills
cp -r flutter-agent-skills/skills/* your-project/.claude/skills/
```

If you use the `skills` CLI from Vercel Labs, you can also try this optional command. Its syntax was not verified as part of this repository's tests:

```bash
npx skills add abdukabirov/flutter-agent-skills
```

## How a skill looks

```
skills/flutter-ui-from-design/
└── SKILL.md      # YAML frontmatter (name, description) + instructions
```

The `description` in the frontmatter helps compatible agent runtimes decide **when** to consider a skill, so each one starts with "Use when ...". Discovery behavior depends on the agent.

## Contributing

To contribute, propose a specific improvement in an issue or improve an existing skill with a real Flutter mistake you have seen an agent make. No code is needed, only Markdown. Read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

[MIT](LICENSE)
