---
name: notion-content-plan
description: Generate a monthly Vietnamese content plan in Notion — wrapper page + inline database + N daily rows — for any product following the canonical 7-column schema (plus Chờ gì / Phương án B gating for rows that depend on events, approvals or unreleased features) (Omini Platform, Omini Care, or a new brand). Triggers on "content plan tháng X", "create monthly content plan", "lên kế hoạch nội dung", "30 bài cho tháng tới".
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

Every row uses these 7 core properties, plus the 2 gating columns described below:

| Property | Type | Notes |
|---|---|---|
| `Ngày` | title (text) | Format `DD/MM/YYYY` — IS the row title |
| `Trạng thái` | select | `Lên lịch` (default), `Đã đăng` |
| `Loại bài viết` | select | 12 options in this exact order/color: `Tổng kết:yellow`, `Pháp lý:orange`, `Giáo dục:purple`, `An toàn:pink`, `Kiến thức:brown`, `Hình ảnh nghề:gray`, `Vận hành:default`, `Cộng đồng:green`, `Chăm sóc KH:blue`, `Nghiệp vụ:red`, `Giá trị:orange`, `Quản lý:purple` |
| `Chủ đề` | text | Headline. Prefix with emoji + holiday tag when the day has one (e.g. `🎈 Quốc tế Thiếu nhi (1/6): …`) |
| `Nội dung chính` | text | 1–2 sentences of post substance |
| `CTA` | text | Short — `Dùng thử`, `Lưu bài`, `Tư vấn`, `Tham gia group`, `Xem video`, `Theo dõi` |
| `Mục tiêu` | text | Conversion goal — `Chuyển đổi trial`, `Brand awareness`, `Community building`, etc. |

**Gating columns (added 11/2026).** Some rows cannot be drafted when the plan is written: they depend on an event that hasn't happened, an approval, an unreleased feature, a customer's consent, or end-of-month numbers. Those rows get:

| Property | Type | Notes |
|---|---|---|
| `Trạng thái` = `Chờ điều kiện` | select option (red) | Instead of `Lên lịch`. Drafting skills skip these rows. |
| `Chờ gì` | text | The concrete condition, e.g. `Thể lệ quiz được duyệt`, `Buổi quay số 25/11 xong`, `Nhà thuốc đồng ý làm case`. |
| `Phương án B` | text | A backup post that can go out **on the same day** if the condition fails. It must not depend on anything itself. |

Every gated row needs both columns filled. A gated row without a Phương án B is how a calendar ends up with empty days the week a gate slips. See Step 6b.

## Brand voice (applies to the 4 Vietnamese text columns ONLY)

These rules govern `Chủ đề`, `Nội dung chính`, `CTA`, `Mục tiêu`. They do **not** apply to
this document or to any English-language report you write back to the user.

### Banned words

| Never write | Always write | Why |
|---|---|---|
| `tiệm`, `cửa tiệm`, `chủ tiệm` | `nhà thuốc và quầy thuốc`, `chủ nhà thuốc và quầy thuốc` | *Nhà thuốc* and *quầy thuốc* are two distinct license types in VN. Omini serves both; `tiệm` is colloquial and silently excludes half the audience. |

Exception: when a sentence describes **one specific business** (a case study), the singular
`một nhà thuốc` / `một chủ nhà thuốc` reads better than the full pair. Use the pair when
addressing the audience as a whole.

Watch for `quầy` used to mean *the sales counter* — now ambiguous against `quầy thuốc` the
business. Rewrite: `tại quầy` → `tại chỗ`, `ai đứng quầy` → `ai đứng bán`,
`sắp xếp quầy` → `sắp xếp khu bán`.

### No dash punctuation

Do not use `—` (em), `–` (en), or `-` (hyphen) as punctuation in the four text columns.
Dash-joined clauses are the single loudest AI tell in Vietnamese marketing copy. Replace with
a comma, a colon, `và`, or a full stop:

| Instead of | Write |
|---|---|
| `Lãi trên giấy nhưng quỹ vẫn cạn — vấn đề ở dòng tiền.` | `Lãi trên giấy nhưng quỹ vẫn cạn, vấn đề ở dòng tiền.` |
| `thu – chi – công nợ` | `thu, chi và công nợ` |
| `hộp – vỉ – viên` | `hộp, vỉ, viên` |
| `1–7/8` | `1 đến 7/8` |
| `D1 → D7 → D30` | `D1, D7, D30` |
| `🩺 Ngày Viêm gan (28/7) — Tầm soát B, C` | `🩺 Ngày Viêm gan (28/7): Tầm soát B, C` |

Markdown bullet markers (`- item`) in the wrapper page are fine; Notion renders them as
bullet dots, so no dash is visible to the reader.

### `Mục tiêu` vocabulary

Reuse the established set rather than inventing goals: `Chuyển đổi trial`,
`Brand awareness`, `Community building`, `Feature adoption`, `Educate market`,
`Activation rate`, `Hiệu quả vận hành`, `Tạo niềm tin pháp lý`, `Tạo niềm tin nghiệp vụ`.
Append ` + bám dịp lễ` on holiday-anchored rows.

## Workflow

### Step 1 — Resolve inputs

If `PRODUCT` is not specified, ask. Don't guess.
If `MONTH` is not specified, default to next month from `today` (CLAUDE_CODE_DATE env).
Compute the number of days in `MONTH` (28–31).

### Step 2 — Load prior context

Fetch the **two** most recent prior plans for the same product. Two months is not optional:
Rule 5 forbids duplicate topics within 60 days, and you cannot enforce that from one month.

```
mcp__notion-fetch with id=<parent page id>          // list children
// find the two most recent "Content Plan <Product> <prev MM/YYYY>"
// for EACH, fetch the wrapper page to get its collection:// data-source URL, then:
mcp__notion-query-data-sources
  SELECT "Ngày", "Loại bài viết", "Chủ đề" FROM "collection://<ds_id>"
```

Pull **every** row, not a sample — you are building a de-dup blocklist, and a 5-row sample
will let a near-duplicate through. Keep the full `Chủ đề` list in working memory while
drafting Step 6.

De-dup on *topic*, not wording. These are duplicates even though the words differ:
`Onboarding D1: 7 bước setup` vs `Onboarding D7: 3 tính năng nâng cao` are **fine** (a
deliberate series), but `Quản lý nhiều chi nhánh trên một tài khoản` vs
`Case study: chuỗi 3 nhà thuốc chuẩn hoá giá` are **too close** — both are "multi-location".
When two candidates collide, keep the one that fits the month's roadmap phase and re-draft
the other on a different axis (how-to vs case study vs legal vs community).

If `PRODUCT` is `Omini Platform`, also fetch the GTM roadmap to pick the right phase emphasis:
- Months 1–2 → foundation, content engine
- Months 2–3 → lead capture, social proof
- Months 3–4 → community, trust
- Months 4–6 → expansion, retention

**Query each prior month's data source separately** (`mode: "rows"`, one call per month). A single SQL query across two data sources needs a Notion Business plan, and this workspace doesn't have one; the call fails with `entitlement_required`.

Also read `references/competitor-patterns.md` before drafting. It records what Vietnamese pharmacy-software and pharma pages (Buymed, MISA, KiotViet, Sapo, TLGo) do, and the gaps none of them fill. Use it to pick formats and series, not to copy topics. For **Omini Care**, read `references/competitor-patterns-care.md` instead (Dạ Hương, Lactacyd, Pharmacity, Hasaki).

Prior months also set the **format arc** — read the wrapper-page callout of the previous
month and advance it rather than repeating it (e.g. 06 text long-form → 07 media comeback →
08 series + UGC). State the new month's format in the wrapper callout.

### Step 3 — Load holidays

Two sources, both required.

**Fixed-date:** load `references/vn-holidays.md` (or the user-supplied `HOLIDAYS` list) and
filter to the target month.

**Lunar:** Tết, Vu Lan, Trung Thu and friends drift every year. Never guess or recall them —
run the bundled helper:

```bash
python3 scripts/lunar_holidays.py <MM> <YYYY>       # holidays in that solar month
python3 scripts/lunar_holidays.py <MM> <YYYY> --all # every day + lunar date, for spot checks
```

Merge both lists. If a lunar and a fixed holiday land on adjacent days (e.g. Vu Lan 27/8 and
Ngày Y tế 28/8) keep both, on their own days. If they land on the *same* day, apply the
"don't stack holidays" note in `references/vn-holidays.md` and pick by audience.

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
  "Trạng thái" SELECT('Lên lịch':default, 'Đã đăng':green, 'Chờ điều kiện':red),
  "Loại bài viết" SELECT(
    'Tổng kết':yellow, 'Pháp lý':orange, 'Giáo dục':purple,
    'An toàn':pink, 'Kiến thức':brown, 'Hình ảnh nghề':gray,
    'Vận hành':default, 'Cộng đồng':green, 'Chăm sóc KH':blue,
    'Nghiệp vụ':red, 'Giá trị':orange, 'Quản lý':purple
  ),
  "Chủ đề" RICH_TEXT,
  "Nội dung chính" RICH_TEXT,
  "CTA" RICH_TEXT,
  "Mục tiêu" RICH_TEXT,
  "Chờ gì" RICH_TEXT,
  "Phương án B" RICH_TEXT
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

Both tables total 30. For a **31-day** month add one row to the type that carries the month's
theme (retention month → `Chăm sóc KH`; launch month → `Giá trị`). For a **28/29-day** month
drop from the largest bucket. Tally the mix before writing rows and again in the Step 9 report
— arithmetic drift here is easy and shows up as a lopsided calendar.

**Recurring series.** Give repeated formats a fixed name prefix in `Chủ đề` so followers learn to expect them, e.g. `🎬 Omini 45 giây: …` for real screen-recording demos and `🧩 Thử tài nhà thuốc #N: …` for quiz-style questions. Two series per month is enough. Pick names that can carry on into the next month.

**Patterns that worked in 11/2026** (from the competitor scan):
- **Free plan in numbers:** say exactly what's included (orders/day, liên thông/day, stores), never a vague "miễn phí". Competitors use "miễn phí trọn đời" (MISA) and price per day (KiotViet).
- **Customer stories with a fixed structure:** background, pain before switching, one real owner quote, two hard numbers (e.g. minutes per invoice, minutes to close the day). Consent first.
- **Guest experts on lives:** an HKD accountant or a pharmacist adds authority and keeps tax questions off Omini's own promises.
- **Owner-to-owner posts** (polls, "nói thật với nhau"): no competitor writes in this voice. Feed poll results into the month-end tổng kết.

Weekly recaps land on 7/14/21/28 (or nearest Sunday). When a recap day collides with a holiday, **combine**: title becomes `🎉 <Holiday> + Tóm tắt tuần N`, content lists both the holiday angle and the recap bullets.

### Step 6b — Gate check

Before creating rows, go through the payload and flag every row that cannot be written today. Typical triggers:

| Trigger | Example |
|---|---|
| Event not yet happened | Draw results, live recap, end-of-month numbers |
| Approval pending | Contest rules, prize structure, legal review |
| Feature not released or not QA'd | Check the sprint page's product-proof table. A feature allowed as a "teaser" there is **not** gated; write it as a teaser. |
| Consent or real data needed | Customer case study, testimonial video |
| Asset not built | A CTA like `Tải checklist` with no file behind it, a quiz link that doesn't exist yet |

For each flagged row: set `Trạng thái = Chờ điều kiện`, write `Chờ gì`, write `Phương án B`. Don't flag a row just because its topic is legal or sensitive; flag it only if something concrete is missing. And don't keep a row whose only purpose is to explain a process that isn't decided yet. Ask the user whether it's worth a slot (in 11/2026 the user removed such a row as useless).

### Step 7 — Batch-create rows

Call `mcp__notion-create-pages` with `parent={data_source_id: <ds_id>}`.

**Send at most ~10 rows per call.** The tool's stated limit is 100 pages, but that is not the
binding constraint: a full month of Vietnamese rows is ~12 KB of UTF-8 and the tool input gets
truncated mid-string, failing with `InputValidationError: could not be parsed as JSON`. Three
calls of 10–11 rows is the reliable shape for a 31-day plan. Do not try to "fix" the JSON on
retry — split the batch instead.

If a batch fails, check what actually landed (`SELECT "Ngày" ...`) before resending, so you
do not create duplicate rows for the same date.

### Step 8 — Verify before reporting

Run these two checks and fix anything they surface. Do not report success until both are clean.

**1. Coverage** — every date present exactly once:

```sql
SELECT COUNT(*) AS rows, COUNT(DISTINCT "Ngày") AS unique_dates
FROM "collection://<ds_id>"
```

Both numbers must equal the day count of the month.

**2. Brand voice** — no banned word, no dash punctuation, in any of the 4 text columns:

```sql
SELECT "Ngày", "Chủ đề" FROM "collection://<ds_id>"
WHERE "Chủ đề" LIKE '%tiệm%' OR "Nội dung chính" LIKE '%tiệm%'
   OR "Chủ đề" LIKE '%—%'   OR "Nội dung chính" LIKE '%—%'
   OR "Chủ đề" LIKE '%–%'   OR "Nội dung chính" LIKE '%–%'
   OR "Chủ đề" LIKE '%-%'   OR "Nội dung chính" LIKE '%-%'
   OR "CTA" LIKE '%-%'      OR "Mục tiêu" LIKE '%-%'
```

Must return zero rows. Patch offenders with `mcp__notion-update-page`
(`command: "update_properties"`, one call per row).

**Allowed exception:** official document numbers keep their hyphens (`CV 934/TTYQG-DA`,
`TT 18/2026/TT-BYT`, `COVID-19`). Rewriting them corrupts the reference. Read each flagged
row and list these exceptions in the report rather than "fixing" them.

**SQL sees trashed rows.** A row moved to Trash still comes back from SQL mode, so a deleted
date shows up as a duplicate in the coverage check. Before treating a duplicate as real,
`fetch` the extra page: a `deleted` attribute on `<page>` means it's in Trash and harmless.
View mode (`mode: "view"`) excludes trashed rows by default.

**3. Gating** — every gated row has its condition and its backup:

```sql
SELECT "Ngày" FROM "collection://<ds_id>"
WHERE "Trạng thái" = 'Chờ điều kiện'
  AND ("Chờ gì" IS NULL OR "Chờ gì" = '' OR "Phương án B" IS NULL OR "Phương án B" = '')
```

Must return zero rows. Run the brand-voice check on `Chờ gì` and `Phương án B` too; they are Vietnamese copy.

### Step 9 — Report & suggest next steps

Output to the user:
- URL of the wrapper page + row count
- List of holiday-anchored dates with their topics
- The post-type mix actually used (so they can eyeball the balance)

Then **always surface the downstream pipeline** so the plan doesn't stall as a static table. Present it as concrete, ordered next steps — a plan only has value once its rows become drafted, scheduled posts:

1. **Draft each post** → `chatgpt-create-pharmacy-post` (Platform) or `chatgpt-create-omini-care-post` (Care). Each draft saves a `post.txt` + `image.png` in a per-day folder. Build the manifest from `Lên lịch` rows only; leave `Chờ điều kiện` rows out until their condition is met, or draft their `Phương án B` instead.
2. **Schedule the drafts** → `facebook-schedule-business-suite` pushes each day's folder into the Business Suite content calendar at a chosen time (default 19:00).
3. *(Optional)* Cross-post finished media → `facebook-post-media`, `zalo-post-timeline`, `tiktok-share-post-video`, `youtube-share-post-video`.

End by **offering to kick off step 1 now** (or to print the plan as DRY_RUN markdown for review first). Name the exact skill for the user's product so they can act in one step.

## Rules

1. **Never deviate from the 7 core columns.** Old plans depend on them for downstream automation. The 2 gating columns (`Chờ gì`, `Phương án B`) are the only additions; no script reads them, so adding them to an older plan is safe.
2. **Always use `Lên lịch` as the initial status**, or `Chờ điều kiện` for gated rows (Step 6b). Never publish-by-default.
3. **Date format is `DD/MM/YYYY` everywhere** — title, holiday tags, prose. Vietnamese reading convention.
4. **Holiday tags use leading emoji + Vietnamese name + `(DD/MM)`** so they're visually scannable in the database view.
5. **Don't auto-generate marketing copy from thin air.** Base each row on:
   - Prior-month topics (no duplicates within 60 days)
   - The product's roadmap phase (for Platform)
   - The current season (for Care)
   - The holiday list (override any of the above)
6. **Vietnamese only** for `Chủ đề`, `Nội dung chính`, `CTA`, `Mục tiêu`. The schema labels themselves are Vietnamese. Obey the **Brand voice** section above: no `tiệm`, no dash punctuation.
7. **CTA vocabulary is fixed** — pick from: `Dùng thử`, `Dùng thử ngay`, `Lưu bài`, `Tư vấn`, `Tư vấn miễn phí`, `Theo dõi`, `Xem video`, `Xem hướng dẫn`, `Đăng ký live`, `Tham gia group`, `Tải checklist`, `Tải giáo án`, `Xem báo cáo`, `Bình luận` (polls), `Đăng ký nhận thông báo` (teasers for unreleased features). Don't invent new ones.
8. **DRY_RUN mode prints to stdout, never to Notion.** Useful for review before bulk creation.
9. **Confirm with user before pushing 30+ rows** if you're unsure about the theme direction — those rows live under the user's brand.

## Editing a plan after it exists

Revisions ("drop that word", "reword the holiday rows") are common. Two traps:

**Never `replace_content` the wrapper page without re-declaring the database.** The inline
database is a *child block* of the wrapper page, so replacing the page content deletes it and
every row with it. Notion's MCP tool guards this with a `validation_error` listing what would
be deleted — that error is a safety net, not an obstacle. Resolve it by appending the database
tag to your new content:

```
<database url="https://app.notion.com/p/<database_id>">…title…</database>
```

Never pass `allow_deleting_content: true` on a wrapper page. For small intro tweaks prefer
`command: "update_content"` with search-and-replace pairs, which cannot orphan children.

**Rows are updated one at a time.** `mcp__notion-update-page` takes a single `page_id`. Fire
them in parallel batches of ~6. Send only the properties that changed; omitted properties are
left alone.

Before a bulk reword, list which rows actually need it — on a 31-row plan a rule change
typically hits 20–25, and touching the clean ones risks introducing new drift. Re-run the
Step 8 verification afterwards.

## What NOT to do

- Don't create the database without the wrapper page. The wrapper provides the narrative intro that gives the month a theme.
- Don't put English in the topic fields. Brand voice is Vietnamese.
- Don't reuse `Ngày` titles across months — they're unique per row.
- Don't skip the `is_pending` / publishing-mechanics for plans — those concerns belong to the downstream publishers (`facebook-post-media`, `zalo-post-timeline`).
- Don't generate >31 rows. If the user asks for "all of Q3," create three separate monthly plans, not one mega-plan.
- Don't add columns beyond the 7 core + 2 gating ones. If the user requests another field, suggest a new view first.

## References

- `references/competitor-patterns-care.md` — Omini Care peers (Dạ Hương, Lactacyd, Pharmacity, Hasaki): what performed, what transfers, what not to copy.
- `references/competitor-patterns.md` — What competitor pages do, which tactics transfer, and the gaps Omini can own. Refresh it every few months.
- `references/vn-holidays.md` — Curated Vietnamese + international observances relevant to pharmacy/health/family content. Loaded on demand. Fixed-date only.
- `scripts/lunar_holidays.py` — Resolves lunar holidays (Tết, Vu Lan, Trung Thu, Ông Công Ông Táo…) for any solar month. Ho Ngoc Duc conversion, UTC+7. Stdlib only, no deps. Verified against published dates for Tết 2024/2025/2026, Trung Thu 2024/2026, Vu Lan 2026.
- Example plans: `Content Plan Omini Platform 06/2026`, `Content Plan Omini Care 06/2026`, `Content Plan Omini Platform 08/2026` (Notion).
- Related skills (downstream pipeline): `chatgpt-create-pharmacy-post`, `chatgpt-create-omini-care-post` (draft) → `facebook-schedule-business-suite` (schedule) → `facebook-post-media`, `zalo-post-timeline`, `tiktok-share-post-video`, `youtube-share-post-video` (cross-post). Also: `campaign-plan`, `content-write`.

## Future hooks (not yet implemented)

- `--from-prior <month>` flag: clone a prior month's structure, shift dates, regenerate only the holiday-anchored rows.
- `--clone-to-google-calendar`: after creating the plan, push each row as an event on a publishing calendar.
- Product-specific recurring events (Omini anniversary, release milestones) alongside the calendar holidays.
- A `--lint` mode that runs the Step 8 verification against an existing plan without creating anything.
