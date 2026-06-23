# notion-content-plan

A Claude Code skill that generates a monthly Vietnamese content plan in Notion — wrapper page + inline database + N daily rows — using the canonical 7-column schema shared by `Content Plan Omini Platform` and `Content Plan Omini Care`.

## Install

```bash
# Clone next to your other Claude skills
cd ~/.claude/skills
git clone git@github.com:streetcoderxyz/claude-notion-content-plan-skill.git notion-content-plan
```

Skills are auto-discovered by Claude Code from `~/.claude/skills/`. Invoke with `/notion-content-plan`.

## Usage

```
/notion-content-plan PRODUCT="Omini Platform" MONTH="07/2026"
```

Or just describe what you want — Claude will route to the skill if it matches:

> Tạo content plan tháng 7 cho Omini Care, nhớ bám các dịp lễ.

## What it does

1. Creates a wrapper page `Content Plan <PRODUCT> <MM/YYYY>` under the Notion parent you specify.
2. Creates an inline database `<PRODUCT> <MM/YYYY>` with the fixed 7-column schema:
   - `Ngày` (title), `Trạng thái`, `Loại bài viết` (12 categories), `Chủ đề`, `Nội dung chính`, `CTA`, `Mục tiêu`.
3. Populates one row per calendar day, mixing the 12 post types to match prior-month ratios.
4. Anchors holidays from `references/vn-holidays.md` — Children's Day, Family Day, Pharmacist Day, etc.

## Schema

Don't change it. Downstream skills (`facebook-post-media`, `zalo-post-timeline`, etc.) expect exactly these 7 columns. New requirements → propose a new view, not a new column.

## Holiday reference

`references/vn-holidays.md` lists Vietnamese + international observances relevant to pharmacy / health / family content. Includes fixed-date holidays and notes on lunar / variable dates (Tết, Father's Day, etc.).

## Related

- `chatgpt-create-pharmacy-post` — draft individual Platform posts.
- `chatgpt-create-omini-care-post` — draft individual Care posts.
- `facebook-post-media` — publish drafts to Facebook (timeline / group / album / video).
- `zalo-post-timeline` — publish to Zalo Timeline via ADB.

## License

MIT
