# Contributing

Thanks for helping. A skill is just Markdown, so you do not need to write code.

## Ways to contribute

- **Fix or sharpen a skill.** You saw an agent get something wrong with a skill loaded? Add the rule that would have prevented it.
- **Add a skill.** Copy `templates/SKILL.template.md` to `skills/<lowercase-kebab-name>/SKILL.md`, then replace the examples with real skill content, follow the README catalog format, and open a PR.
- **Request a skill.** Open an issue with the **Skill request** template.
- **Report a bad rule.** If a skill gives outdated or wrong Flutter advice, open an issue with the version of Flutter and the package involved.

## Writing a good skill

1. **One skill, one job.** "Migrate to Riverpod" is a skill. "State management" is too wide.
2. **The description is a trigger.** Start with "Use when ..." and name the situations and keywords where the agent should load the skill. Under 300 characters. Do not use a colon followed by a space in it (it breaks the YAML); use a comma or wrap the whole value in quotes.
3. **Say what to do, then what to avoid.** Concrete steps and a short "common mistakes" list beat general advice.
4. **Show code.** Prefer a short wrong/right pair over a paragraph of explanation.
5. **Name versions.** If advice depends on a Flutter, Dart or package version, say which one.
6. **Keep it short.** Aim for under 300 lines. Long material goes into a `references/` folder next to `SKILL.md`, linked from the main file.
7. **Test it.** Run your agent on a real task with and without the skill. Include in the PR what changed in the result. Skills that make no difference will not be merged.

## Local check

```bash
pip install pyyaml
python scripts/validate_skills.py
```

The same check runs in CI on every pull request. It verifies the frontmatter, the folder name, and the description length.

## Pull requests

- One skill (or one fix) per PR.
- Folder name is lowercase with hyphens and matches `name:` in the frontmatter.
- Do not copy text from other repositories or from documentation. Write it in your own words.

## Code of conduct

Be kind and assume good intent. Critique the skill, not the person.
