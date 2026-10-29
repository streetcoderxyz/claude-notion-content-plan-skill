# Peer content patterns (Vietnamese B2C intimate care and family health)

Collected 29/10/2026 for the Omini Care 11/2026 revision. Read with a logged-in Facebook
session over CDP (Brave profile `chatgpt-skill-brave`), about 40 recent posts from Dạ Hương
and 20 to 30 each from Lactacyd, Pharmacity and Hasaki. Long Châu (`/nhathuoclongchau`)
returned nothing. Reaction counts are what the feed showed. Many of these posts are
probably boosted, so compare them with each other and don't treat them as organic benchmarks.

This file is for **Omini Care only**. The Platform (B2B pharmacy software) notes live in
`competitor-patterns.md`.

## Who does what

| Page | Size | What they lean on |
|---|---|---|
| **Dạ Hương** (Hoa Linh), facebook.com/dahuonghoalinh | 306K | Life-moment posts for one persona at a time (students, office deadlines, sport), a 4-line "Phiên Bản Mới" range with a pick-by-need selector, life-stage posts (puberty, pregnancy, sensitive skin), price lists with Shopee links, KOC reels with one-line captions, CSR and sponsorships (women workers, students, scholarships, pickleball), trust badges (Thương hiệu Quốc gia), prize minigames on 20/10 |
| **Lactacyd** (Sanofi), facebook.com/LactacydVietnam | n/a | Sensory "one-minute reset" framing, pH education ("không dùng chung sữa tắm"), a hosted series ("Hãy Chọn Tắm Đúng"), ingredient-tech naming (LACTOBIOME+) |
| **Pharmacity**, facebook.com/pharmacity.vn | n/a | In-store event weeks ("Đến là có quà"), long livestreams with deep discounts, "A hay B" product comparisons |
| **Hasaki**, facebook.com/hasaki.vn | n/a | Deal posts: price, original price, link, branch count. Mostly single-digit engagement |

## What performed (relative)

| Post | Reactions / comments / shares |
|---|---|
| Dạ Hương minigame 20/10 | 4.2K / 1.4K / 714 |
| Dạ Hương "Tháng này hãy dịu dàng với bản thân hơn" (letter format) | 2.9K / 43 / 20 |
| Dạ Hương "Cả tuần căng task" (students, deadline) | 1.8K / 31 / 41 |
| Dạ Hương "Điểm 10 tự tin tới trường" | 1.7K / 78 / 61 |
| Dạ Hương "Chọn phiên bản theo nhu cầu" (range selector) | 1.6K / 8 / 20 |
| Dạ Hương price list with Shopee links | 1.2K |
| Dạ Hương Thương hiệu Quốc gia (trust badge) | 1.1K / 23 / 17 |
| Dạ Hương mẹ bầu selection criteria | 872 |
| Dạ Hương "Deadline căng thẳng" (product-first) | 16 |
| Hasaki / Pharmacity deal-only posts | mostly under 20 |

## Tactics that transfer to Omini Care

1. **Life moment first, product second.** One persona, one real day, then the habit, then
   the product at most once. For Bắc Ninh the persona nobody writes for is the woman doing
   long shifts at an industrial park. Series name in use: `🌿 Một ngày thoáng sạch:`.
2. **Life-stage education for the family.** A mother talking to her daughter at puberty
   fits "chăm sóc sức khỏe gia đình bạn" better than any product post.
3. **Pick-by-need cards** ("Hôm nay bạn cần gì?"). Omini's version picks by the person
   being cared for (con nhỏ, ông bà, chính mình) and links to earlier posts.
4. **Authenticity help in public.** Ask for a photo of the product plus where it was bought,
   then answer case by case. Good for after-sale and receiving-goods posts.
5. **Clear price per bottle with a marketplace link.** Price lists get attention, while
   bare deal posts don't.

## Do not copy

- Dạ Hương claims (`kháng khuẩn`, `ngừa viêm ngứa`, "an toàn cho mẹ bầu") are outside
  Dạ Yến Thảo's cosmetic dossier. `chatgpt-create-omini-care-post/references/brand.md` §5 rules.
- Prize minigames need approved rules first. Gate them (`Chờ điều kiện`) and never draft one
  as a plain row.
- Euphemisms like "cô bé" and "bé mèo" are common in this category, but Omini copy is plain
  and neighbourly. Write `vùng nhạy cảm` or `vùng bên ngoài`.
- KOL ambassadors, event sponsorships and NielsenIQ-style research are beyond a one-store
  budget.

## Refresh

Re-scan before relying on this for a flagship month (03/2027 8/3). The scan helper is a
short CDP script that scrolls the page and collects `div[aria-posinset]` text plus
engagement spans; rebuild it on top of `chatgpt-create-pharmacy-post/scripts/brave_cdp.py`.
