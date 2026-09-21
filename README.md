# notion-content-plan

A Claude Code skill that generates a monthly Vietnamese content plan in Notion — wrapper page + inline database + N daily rows — using the canonical 7-column schema shared by `Content Plan Omini Platform` and `Content Plan Omini Care`. Product-agnostic: pass any `PRODUCT`.

## Install

```bash
# Clone next to your other Claude skills
cd ~/.claude/skills
git clone git@github.com:streetcoderxyz/claude-notion-content-plan-skill.git notion-content-plan
```

Skills are auto-discovered by Claude Code from `~/.claude/skills/`. Invoke with `/notion-content-plan`.

## Usage

```
/notion-content-plan PRODUCT="Omini Platform" MONTH="10/2026"
/notion-content-plan PRODUCT="Omini Care"     MONTH="10/2026"
```

Or just describe what you want — Claude will route to the skill if it matches:

> Tạo content plan tháng 7 cho Omini Care, nhớ bám các dịp lễ.

## What it does

1. Creates a wrapper page `Content Plan <PRODUCT> <MM/YYYY>` under the Notion parent you specify.
2. Creates an inline database `<PRODUCT> <MM/YYYY>` with the fixed 7-column schema:
   - `Ngày` (title), `Trạng thái`, `Loại bài viết` (12 categories), `Chủ đề`, `Nội dung chính`, `CTA`, `Mục tiêu`.
3. Populates one row per calendar day, mixing the 12 post types to match prior-month ratios.
4. Anchors holidays from `references/vn-holidays.md` — Children's Day, Family Day, Pharmacist Day, etc.
5. De-dups against the **two** prior months, so a rolling plan never repeats itself within 60 days.
6. Verifies the result in Notion (date coverage + brand-voice lint) before reporting success.

## Schema

Don't change it. Downstream skills (`facebook-post-media`, `zalo-post-timeline`, etc.) expect exactly these 7 columns. New requirements → propose a new view, not a new column.

## Brand voice

The generated Vietnamese copy follows two hard rules, enforced by a post-create lint:

- **Never `tiệm`.** Write `nhà thuốc và quầy thuốc` — two distinct license types in Vietnam, and the colloquial `tiệm` silently excludes half the audience.
- **No dash punctuation** (`—`, `–`, `-`) in the copy columns. Dash-joined clauses are the loudest AI tell in Vietnamese marketing copy; use a comma, colon, `và`, or full stop.

See the *Brand voice* section of `SKILL.md` for the full rewrite table.

## Holiday reference

`references/vn-holidays.md` lists fixed-date Vietnamese + international observances relevant to pharmacy / health / family content.

Lunar holidays drift every year and must never be recalled from memory. `scripts/lunar_holidays.py` resolves them for any month:

```bash
$ python3 scripts/lunar_holidays.py 08 2026
08/2026 lunar holidays:
  27/08/2026  Vu Lan (Ram thang 7)         [AL 15/7]
              angle: Care: tri an cha me, suc khoe ong ba

$ python3 scripts/lunar_holidays.py 08 2026 --all   # every day + lunar date
```

Ho Ngoc Duc's conversion algorithm at UTC+7. Python stdlib only, no dependencies. Cross-checked against published dates for Tết 2024/2025/2026, Trung Thu 2024/2026, and Vu Lan 2026.

## Related

- `chatgpt-create-pharmacy-post` — draft individual Platform posts.
- `chatgpt-create-omini-care-post` — draft individual Care posts.
- `facebook-post-media` — publish drafts to Facebook (timeline / group / album / video).
- `zalo-post-timeline` — publish to Zalo Timeline via ADB.

## License

MIT
