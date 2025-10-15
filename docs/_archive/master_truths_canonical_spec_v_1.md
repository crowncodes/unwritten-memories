# Master Truths — Canonical Spec (v1.1)

> **Purpose**: Single source of truth for systems, vocabulary, and guardrails. Every new or updated doc **must** comply with this page or explicitly propose a change via the process below.

**Changelog:**
- **v1.1** (2025-10-13): Clarified season length selection (12/24/36 weeks, player choice) and relationship levels (0-5 with Level 0 = "Not Met")
- **v1.0** (Initial): Base canonical specifications

---

## 1) Core Principles
- **Player-first**: No predatory mechanics; decisions matter, not anxiety farming.
- **Stories with closure**: Each **Season** is a complete 3‑act arc; choices echo across seasons and lifetimes.
- **Additive content**: DLC adds possibilities, not power. No RNG/gacha. No pay-to-win.
- **Consistency over cleverness**: Terminology, scales, and UI states are canonical here.

---

## 2) Canonical Vocabulary & Scales
**Time units**
- **Turn**: Three per day (Morning / Afternoon / Evening). 7 days per week.
- **Season**: **12, 24, or 36 weeks** (player selects at season start based on aspiration complexity and desired depth).
  - **Standard (12w)**: Focused single-goal arc
  - **Extended (24w)**: Complex multi-path arc
  - **Epic (36w)**: Transformational saga arc
  - Players can end seasons early if goals complete ahead of schedule.

**Relationships**
- **Levels**: **0–5** (discrete stages; 0 = "Not Met", tracked internally but never displayed as "Level 0").
  - Level 0: Not Met (never interacted)
  - Level 1: Stranger (0-5 interactions)
  - Level 2: Acquaintance (6-15 interactions)
  - Level 3: Friend (16-30 interactions)
  - Level 4: Close Friend (31-75 interactions)
  - Level 5: Soulmate/Best Friend (76+ interactions)
- **Trust**: **0.0–1.0** continuous meter under the hood.
- **Level-Up Requirements**: Both interaction count AND minimum trust threshold required.
- **Statuses** (post-level): *Life Partnership*, *Estranged*, etc. (Statuses are **not** new levels.)
- **Display**: "Level 3 (Trust 0.62)" — never "10/10", "Level 6", or "Level 0" (show "Not Met" instead).

**Emotional State Lexicon**
- Canonical names include **EXHAUSTED** and **OVERWHELMED**.
- Deprecated alias: **DRAINED → EXHAUSTED** (map in logic and copy).
- New emotions must either map to an existing canonical name or propose an addition.

---

## 3) Economy & Resources
- **Time**: Weekly budget model (target: ~168h total; internal planning may assume ~48h flexible).
- **Energy**: Daily/phase-limited; gates higher-effort actions.
- **Money**: Liquidity for purchases, travel, activities.
- **Social Capital**: Earned/spendable relationship currency that unlocks favors, intros, and opportunities.
- **Modifiers**: Emotional state, skills, items provide multipliers/thresholds but are not currencies.

Authoring note: If introducing new currencies, they **must** be approved and added here first.

---

## 4) Turn Structure & Pacing
- **Cadence**: 3 turns/day; weekdays favor routines/obligations; weekends favor exploration/social.
- **Batching & Automation**: Repeating routines can be batched or auto-resolved to reduce friction.
- **Decision Tiers**: Top-tier/Decisive decisions **pause time** in UI; deadlines are in‑world, not real‑time.
- **Event Mix**: Each day blends routine, opportunity, social, and narrative beats (use category weights).

Copy standard: Replace any “FOMO/decide now” language with **“Time is paused while you decide.”**

---

## 5) Narrative Structure
- **Season (3‑act)**: Setup → Escalation/Complications → Resolution/Consequences.
- **Decisive-Decision Template**: Triggers, preconditions, foreshadowing beats, clear options with immediate and long‑range consequences; success/failure paths defined.
- **Continuity**: NPC memory, relationship levels/trust, key outcomes persist across seasons and lifetimes.

---

## 6) Card System (Unified)
- **Purpose**: Cards are the atomic memory/content units.
- **Taxonomy** (top-level): Life Direction • Aspirations • Relationships • Activities • Routines/Obligations • Places • Items/Utilities (7 buckets).
- **Base Deck**: 470+ curated base cards.
- **Evolution**: Cards evolve through usage/context; evolution is authored (not random) and preserves identity.

---

## 7) Fusion System
- **Types**: Simple • Complex • Chain • Legendary • Conditional.
- **Rules**: Fusion outputs declare prerequisites, inputs, and carried-forward traits; maintain traceability.
- **Levels/Trust**: Do **not** introduce new relationship levels; fusion may unlock statuses or traits.

---

## 8) Progression & Phases
- **Phase ladder** (high level): Foundations → Expansion → Mastery (names may localize per domain).
- Gating uses **skill checks**, **trust thresholds**, and **resource minima** — never paywalls.

---

## 9) Archives, Continuity & Persistence
- **Free**: Unlimited **Season Archives**; **3 Lifetime Archives**.
- **Plus/Ultimate**: Unlimited **Lifetime Archives**.
- Archives preserve: deck state, relationships (levels/trust), decisive outcomes, unlocked systems, and key world flags.

---

## 10) Monetization (Canonical)
- **Essence Tokens**: Daily free grant (baseline 25/day) for AI-heavy actions; subscription tiers raise limits.
- **Packs (DLC)**: Permanent unlocks, no RNG.
  - **Standard**: **20–30** cards
  - **Deluxe**: **35–50** cards
  - **Mega**: **60–80** cards (large locale/discipline collections)
- **Art Style Packs**: Visual-only style changes; typical price point **$2.99**.
- **Subscriptions**: **Plus $14.99/mo**, **Ultimate $29.99/mo** (exact entitlements maintained in Pricing table).

Policy: No timers, streaks, or scarcity designed to induce anxiety; in‑world deadlines are narrative devices only.

---

## 11) AI Personality & NPC Behavior
- **Stable voices**: NPCs maintain personality, goals, and memory across sessions.
- **Knowledge boundaries**: POV access is limited to what the character would plausibly know.
- **Authoring knobs**: Traits, goals, secrets, and trust thresholds are explicit dials; random drift is disallowed.

---

## 12) UX & Copy Standards
- **Decisions**: Show **paused time** affordance on decisive choices.
- **States**: Use canonical emotion names; show tooltips for mapped aliases.
- **Consistency**: Surface “Level X (Trust Y.Y)” for relationships; never show deprecated scales.
- **Accessibility**: Plain language; avoid purple prose in system text.

---

## 13) Authoring Rules for New Docs
When you create or edit any spec:
1. **Declare Intent**: Is it canonical, proposed, or exploratory?
2. **Align Scales**: Relationship 0–5; Trust 0.0–1.0; Season 12w (or mark as Extended 24/36).
3. **Economy Check**: Only Time/Energy/Money/Social Capital as currencies unless added here.
4. **Decision Tiering**: Paused-time for top-tier choices; no real-time urgency text.
5. **Pack Fit**: Classify as Standard/Deluxe/Mega; include card counts.
6. **Archive Policy**: Respect tier entitlements.
7. **Emotion Names**: Use canonical lexicon; map aliases.
8. **Fusion Rules**: Specify type, inputs, prerequisites, and traceability.

Every doc should end with a **Compliance Checklist** referencing these bullets.

---

## 14) Versioning & Change Process
- **Versioning**: Semantic (MAJOR.MINOR.PATCH) for this Truths doc; cite version in downstream docs.
- **Change Proposal (CP)**: Title • Rationale • Impacted Sections • Backward‑compat notes • Migration plan • Owner • Target release.
- **Approval**: 1 Product + 1 Narrative + 1 Systems sign‑off. Merge only after all are green.

---

## 15) Canonical Constants (v1.1)
- Season length options: **12 weeks (Standard)**, **24 weeks (Extended)**, **36 weeks (Epic)** (player choice at season start)
- Turns per day: **3** (Morning/Afternoon/Evening); Days per week: **7**
- Free daily Essence: **25** (subject to tiering)
- Relationship Levels: **0–5** (0=Not Met, 1-5 displayed); Trust: **0.0–1.0** (continuous)
- Level-up requirements: **Interaction count + Trust threshold** (both required)
- Pack sizes: **Standard 20–30**, **Deluxe 35–50**, **Mega 60–80**

> Update this block anytime numbers change. Downstream docs must reference constants by name, not hardcode values.
> 
> **v1.1 Updates:** Clarified season length as player choice (not variable duration), detailed relationship level progression (0-5 with explicit thresholds)

---

### Compliance Checklist (paste into new docs)
- [ ] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; EXHAUSTED/OVERWHELMED)
- [ ] Season = 12/24/36w (player choice at season start); 3 turns/day
- [ ] Relationship Level 0 = "Not Met" (never displayed as "Level 0")
- [ ] Level-up requires BOTH interaction count AND trust threshold
- [ ] Currencies limited to Time/Energy/Money/Social Capital
- [ ] Decisive decisions pause time; copy avoids FOMO framing
- [ ] Packs classified (Standard/Deluxe/Mega) with counts
- [ ] Archive policy respected by tier
- [ ] Fusion type, inputs, prerequisites, outputs defined
- [ ] NPC personality/memory constraints respected
- [ ] This doc cites **Truths v1.1** at the top

