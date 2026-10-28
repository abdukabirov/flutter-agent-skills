# flutter-agent-skills

Markdown skills for AI coding agents working on Flutter and Dart projects.

## Skills

- [flutter-ui-from-design](skills/flutter-ui-from-design/SKILL.md) — **Tested** in two small A/B rounds. The valid-run comparison passed, but the replacement run was selected after the initial result, so the evidence has replacement-selection bias. [Evidence](docs/evidence/flutter-ui-from-design.md)
- [flutter-state-to-riverpod](skills/flutter-state-to-riverpod/SKILL.md) — **Experimental**. No comparative evaluation is recorded in this repository.
- [flutter-go-router](skills/flutter-go-router/SKILL.md) — **Experimental**. No comparative evaluation is recorded in this repository.
- [flutter-testing](skills/flutter-testing/SKILL.md) — **Experimental**. No comparative evaluation is recorded in this repository.

Removed skills and their reports remain in [docs/evidence](docs/evidence/).

## Installation

Clone the repository:

```bash
git clone https://github.com/abdukabirov/flutter-agent-skills.git
cd flutter-agent-skills
```

### Claude Code

Claude Code supports personal skills in `~/.claude/skills/` and project skills in `.claude/skills/`. From the cloned repository root:

```bash
# Personal skills
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/

# Project-specific skills
mkdir -p /path/to/target-project/.claude/skills
cp -r skills/* /path/to/target-project/.claude/skills/
```

See the [official Claude Code skills documentation](https://code.claude.com/docs/en/skills).

### GitHub Copilot in VS Code

This repository stores skills in `skills/<skill-name>/SKILL.md`. For automatic discovery in a target project, copy a required skill directory into that project's `.github/skills/<skill-name>/` directory:

```bash
mkdir -p /path/to/target-project/.github/skills/flutter-ui-from-design
cp -r skills/flutter-ui-from-design/* /path/to/target-project/.github/skills/flutter-ui-from-design/
```

See the [official VS Code Agent Skills documentation](https://code.visualstudio.com/docs/agent-customization/agent-skills).

Automatic discovery was not demonstrated in this repository's test environment; this result may depend on the VS Code configuration.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
