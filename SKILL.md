---
name: notion-content-plan
description: Generate a monthly Vietnamese content plan in Notion — wrapper page + inline database + N daily rows — for Omini Platform, Omini Care, or any product following the same 7-column schema.
---

# Notion — Monthly Content Plan Generator

Given a product, a month, and optionally a holiday list, this skill creates:

1. A wrapper page titled `Content Plan <Product> <MM/YYYY>` under a parent page.
2. An inline database titled `<Product> <MM/YYYY>` with the canonical 7-column schema.
3. N rows (default: one per calendar day) following the cadence and post-type mix of prior months.

Originally extracted from the workflow that built `Content Plan Omini Platform 06/2026` and `Content Plan Omini Care 06/2026`. The same schema and rhythm work for any pharmacy / health / family-care brand.

## When to use

- "Create June plan for Omini Platform" / "Lên content plan tháng 7 cho Omini Care"
- New month rolling over and you need 30 scheduled posts
- Onboarding a new product line that should follow the same content cadence

Do NOT use for:
- Single-post drafting → `chatgpt-create-pharmacy-post` / `chatgpt-create-omini-care-post`
- Publishing finished media → `facebook-post-media` / `zalo-post-timeline`
- Long-form roadmap / PRD planning → `roadmap-plan`

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `PARENT_PAGE_ID` | Yes | — | Notion page ID where the wrapper page should be created (e.g. the "Content Plans" hub) |
| `PRODUCT` | Yes | — | `Omini Platform` · `Omini Care` · or any custom product name |
| `MONTH` | Yes | — | Month + year, format `MM/YYYY` (e.g. `06/2026`) |
| `CADENCE` | No | `daily` | `daily` (30/31 rows) or `weekly` (4–5 rows) |
| `HOLIDAYS` | No | auto | List of `{date: "DD/MM/YYYY", name: "..."}` to weave in. If omitted, the skill loads `references/vn-holidays.md` |
| `THEME_HINT` | No | — | One-sentence direction (e.g. "summer health for families", "GTM phase 2: lead capture") |
| `DRY_RUN` | No | `false` | If `true`, print the row list as Markdown instead of creating in Notion |

## Canonical schema (do not deviate)

Every row uses exactly these 7 properties:

| Property | Type | Notes |
|---|---|---|
| `Ngày` | title (text) | Format `DD/MM/YYYY` — IS the row title |
| `Trạng thái` | select | `Lên lịch` (default), `Đã đăng` |
| `Loại bài viết` | select | 12 options in this exact order/color: `Tổng kết:yellow`, `Pháp lý:orange`, `Giáo dục:purple`, `An toàn:pink`, `Kiến thức:brown`, `Hình ảnh nghề:gray`, `Vận hành:default`, `Cộng đồng:green`, `Chăm sóc KH:blue`, `Nghiệp vụ:red`, `Giá trị:orange`, `Quản lý:purple` |
| `Chủ đề` | text | Headline. Prefix with emoji + holiday tag when the day has one (e.g. `🎈 Quốc tế Thiếu nhi (1/6) — …`) |
| `Nội dung chính` | text | 1–2 sentences of post substance |
| `CTA` | text | Short — `Dùng thử`, `Lưu bài`, `Tư vấn`, `Tham gia group`, `Xem video`, `Theo dõi` |
| `Mục tiêu` | text | Conversion goal — `Chuyển đổi trial`, `Brand awareness`, `Community building`, etc. |

## Workflow

### Step 1 — Resolve inputs

If `PRODUCT` is not specified, ask. Don't guess.
If `MONTH` is not specified, default to next month from `today` (CLAUDE_CODE_DATE env).
Compute the number of days in `MONTH` (28–31).

### Step 2 — Load prior context

Fetch the 1–2 most recent prior plans for the same product to mirror tone, post-type ratio, and CTA vocabulary:

```
mcp__notion-fetch with id=<parent page id>  // list children
// find most recent "Content Plan <Product> <prev MM/YYYY>"
// query its data source for ~5 sample rows
```

If `PRODUCT` is `Omini Platform`, also fetch the GTM roadmap to pick the right phase emphasis:
- Months 1–2 → foundation, content engine
- Months 2–3 → lead capture, social proof
- Months 3–4 → community, trust
- Months 4–6 → expansion, retention

### Step 3 — Load holidays

Either use the user-supplied `HOLIDAYS` list, or load `references/vn-holidays.md` (see below). Filter to entries whose `date` falls within the target month.

### Step 4 — Create wrapper page

Use `mcp__notion-create-pages` with `parent={page_id: PARENT_PAGE_ID}`:

```
title: "Content Plan <PRODUCT> <MONTH>"
icon: 📘 for Platform, 💚 for Care, else 📅
content: short intro paragraph describing the month's focus + holiday list
```

Save the returned page ID.

### Step 5 — Create the database

Use `mcp__notion-create-database` with `parent={page_id: <wrapper page id>}` and the exact CREATE TABLE statement:

```sql
CREATE TABLE (
  "Ngày" TITLE,
  "Trạng thái" SELECT('Lên lịch':default, 'Đã đăng':green),
  "Loại bài viết" SELECT(
    'Tổng kết':yellow, 'Pháp lý':orange, 'Giáo dục':purple,
    'An toàn':pink, 'Kiến thức':brown, 'Hình ảnh nghề':gray,
    'Vận hành':default, 'Cộng đồng':green, 'Chăm sóc KH':blue,
    'Nghiệp vụ':red, 'Giá trị':orange, 'Quản lý':purple
  ),
  "Chủ đề" RICH_TEXT,
  "Nội dung chính" RICH_TEXT,
  "CTA" RICH_TEXT,
  "Mục tiêu" RICH_TEXT
)
```

Title the database `<PRODUCT> <MONTH>`. Save the `data_source_id` from the `<data-source url="collection://...">` tag in the response.

### Step 6 — Generate the row payload

For each day `DD` from 1 to `<days in month>`:

1. If `DD/MM/YYYY` matches a holiday, anchor `Chủ đề` to that holiday with a leading emoji + `<Holiday Name> (DD/MM)` tag.
2. Otherwise pick a `Loại bài viết` according to the target mix (see below).
3. Write `Chủ đề` (≤ 80 chars), `Nội dung chính` (1–2 sentences), `CTA`, `Mục tiêu`.
4. Set `Trạng thái = "Lên lịch"`.

**Default post-type mix (Platform, 30 days):**
| Type | Count |
|---|---|
| Giá trị | 5 |
| Giáo dục | 4 |
| Pháp lý | 3 |
| Quản lý | 3 |
| Kiến thức | 3 |
| Nghiệp vụ | 3 |
| Cộng đồng | 3 |
| An toàn | 2 |
| Chăm sóc KH | 2 |
| Vận hành | 1 |
| Hình ảnh nghề | 1 |
| Tổng kết | 1 (month-end) |

**Default post-type mix (Care, 30 days):**
| Type | Count |
|---|---|
| Kiến thức | 8 |
| Giáo dục | 7 |
| An toàn | 6 |
| Tổng kết | 5 (one per week + month-end) |
| Chăm sóc KH | 4 |

Weekly recaps land on 7/14/21/28 (or nearest Sunday). When a recap day collides with a holiday, **combine**: title becomes `🎉 <Holiday> + Tóm tắt tuần N`, content lists both the holiday angle and the recap bullets.

### Step 7 — Batch-create rows

One call to `mcp__notion-create-pages` with `parent={data_source_id: <ds_id>}` and `pages: [...30 entries]`. The MCP tool accepts up to 100 pages per call.

### Step 8 — Report & suggest next steps

Output to the user:
- URL of the wrapper page + row count
- List of holiday-anchored dates with their topics
- The post-type mix actually used (so they can eyeball the balance)

Then **always surface the downstream pipeline** so the plan doesn't stall as a static table. Present it as concrete, ordered next steps — a plan only has value once its rows become drafted, scheduled posts:

1. **Draft each post** → `chatgpt-create-pharmacy-post` (Platform) or `chatgpt-create-omini-care-post` (Care). Each draft saves a `post.txt` + `image.png` in a per-day folder.
2. **Schedule the drafts** → `facebook-schedule-business-suite` pushes each day's folder into the Business Suite content calendar at a chosen time (default 19:00).
3. *(Optional)* Cross-post finished media → `facebook-post-media`, `zalo-post-timeline`, `tiktok-share-post-video`, `youtube-share-post-video`.

End by **offering to kick off step 1 now** (or to print the plan as DRY_RUN markdown for review first). Name the exact skill for the user's product so they can act in one step.

## Rules

1. **Never deviate from the 7-column schema.** Old plans depend on it for downstream automation.
2. **Always use `Lên lịch` as the initial status.** Never publish-by-default.
3. **Date format is `DD/MM/YYYY` everywhere** — title, holiday tags, prose. Vietnamese reading convention.
4. **Holiday tags use leading emoji + Vietnamese name + `(DD/MM)`** so they're visually scannable in the database view.
5. **Don't auto-generate marketing copy from thin air.** Base each row on:
   - Prior-month topics (no duplicates within 60 days)
   - The product's roadmap phase (for Platform)
   - The current season (for Care)
   - The holiday list (override any of the above)
6. **Vietnamese only** for `Chủ đề`, `Nội dung chính`, `CTA`, `Mục tiêu`. The schema labels themselves are Vietnamese.
7. **CTA vocabulary is fixed** — pick from: `Dùng thử`, `Dùng thử ngay`, `Lưu bài`, `Tư vấn`, `Tư vấn miễn phí`, `Theo dõi`, `Xem video`, `Xem hướng dẫn`, `Đăng ký live`, `Tham gia group`, `Tải checklist`, `Tải giáo án`, `Xem báo cáo`. Don't invent new ones.
8. **DRY_RUN mode prints to stdout, never to Notion.** Useful for review before bulk creation.
9. **Confirm with user before pushing 30+ rows** if you're unsure about the theme direction — those rows live under the user's brand.

## What NOT to do

- Don't create the database without the wrapper page. The wrapper provides the narrative intro that gives the month a theme.
- Don't put English in the topic fields. Brand voice is Vietnamese.
- Don't reuse `Ngày` titles across months — they're unique per row.
- Don't skip the `is_pending` / publishing-mechanics for plans — those concerns belong to the downstream publishers (`facebook-post-media`, `zalo-post-timeline`).
- Don't generate >31 rows. If the user asks for "all of Q3," create three separate monthly plans, not one mega-plan.
- Don't add columns. If user requests a new field, suggest a new view or a separate per-row property in a **future** version — current downstream scripts assume exactly these 7 columns.

## References

- `references/vn-holidays.md` — Curated Vietnamese + international observances relevant to pharmacy/health/family content. Loaded on demand.
- Example plans: `Content Plan Omini Platform 06/2026`, `Content Plan Omini Care 06/2026` (Notion).
- Related skills (downstream pipeline): `chatgpt-create-pharmacy-post`, `chatgpt-create-omini-care-post` (draft) → `facebook-schedule-business-suite` (schedule) → `facebook-post-media`, `zalo-post-timeline`, `tiktok-share-post-video`, `youtube-share-post-video` (cross-post). Also: `campaign-plan`, `content-write`.

## Future hooks (not yet implemented)

- `--from-prior <month>` flag: clone a prior month's structure, shift dates, regenerate only the holiday-anchored rows.
- `--clone-to-google-calendar`: after creating the plan, push each row as an event on a publishing calendar.
- Auto-detection of recurring holidays (Tết, Trung thu) and product-specific events (Omini anniversary).
