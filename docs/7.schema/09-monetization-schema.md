# Monetization Schema

**Schema Version**: 1.0.0  
**Last Updated**: 2025-10-13  
**Dependencies**: `01-core-types.md`, `02-card-system.md`, `08-archive-persistence.md`

---

## Overview

Defines monetization tiers, Essence token system, expansion packs, premium content, pricing structures, and entitlement tracking.

---

## 1. Tier System

### Player Tiers

```typescript
/**
 * Player monetization tier
 */
interface PlayerTier {
  player_id: PlayerID;
  tier: TierLevel;
  
  // Subscription
  subscription_active: boolean;
  subscription_type?: SubscriptionType;
  subscription_started?: ISO8601String;
  subscription_renews?: ISO8601String;
  
  // Essence balance
  essence_balance: number;
  essence_earned_free: number;
  essence_purchased: number;
  essence_spent: number;
  
  // Content ownership
  owned_expansion_packs: PackID[];
  owned_art_styles: ArtStyleID[];
  legacy_edition: boolean;
  
  // Usage
  premium_content_generations: number;
  premium_image_generations: number;
  premium_books_generated: number;
  
  // History
  total_spent_usd: number;
  lifetime_value: number;
  first_purchase?: ISO8601String;
  last_purchase?: ISO8601String;
}

enum TierLevel {
  Free = "free",
  Casual = "casual",              // Has purchased, no active subscription
  Premium = "premium"              // Active subscription
}

enum SubscriptionType {
  Monthly = "monthly",
  Quarterly = "quarterly",
  Yearly = "yearly"
}
```

### Tier Capabilities

```typescript
/**
 * What each tier can do
 */
interface TierCapabilities {
  tier: TierLevel;
  
  // Essence
  daily_free_essence: number;
  can_purchase_essence: boolean;
  
  // Archive
  archived_cards_per_season: number | "unlimited";
  archived_memories_per_season: number | "unlimited";
  
  // Book generation
  free_book_quality: "standard";
  can_generate_premium_books: boolean;
  premium_book_cost_essence: number;
  
  // Content
  base_cards_count: number;
  base_npcs_count: number;
  base_locations_count: number;
  can_purchase_expansion_packs: boolean;
  
  // AI quality
  local_ai_quality: number;         // 7/10 for all
  cloud_ai_available: boolean;
  cloud_ai_quality: number;         // 10/10 for premium
  
  // Image generation
  standard_art_included: boolean;
  can_generate_premium_art: boolean;
  premium_art_cost_essence: number;
}

const TIER_CAPABILITIES: Record<TierLevel, TierCapabilities> = {
  free: {
    tier: TierLevel.Free,
    daily_free_essence: 25,
    can_purchase_essence: true,
    archived_cards_per_season: 3,
    archived_memories_per_season: "unlimited",
    free_book_quality: "standard",
    can_generate_premium_books: true,
    premium_book_cost_essence: 250,
    base_cards_count: 470,
    base_npcs_count: 50,
    base_locations_count: 30,
    can_purchase_expansion_packs: true,
    local_ai_quality: 7,
    cloud_ai_available: false,
    cloud_ai_quality: 0,
    standard_art_included: true,
    can_generate_premium_art: true,
    premium_art_cost_essence: 50
  },
  
  premium: {
    tier: TierLevel.Premium,
    daily_free_essence: 25,         // Same as free
    can_purchase_essence: true,
    archived_cards_per_season: "unlimited",
    archived_memories_per_season: "unlimited",
    free_book_quality: "standard",
    can_generate_premium_books: true,
    premium_book_cost_essence: 0,   // Free for subscribers
    base_cards_count: 470,
    base_npcs_count: 50,
    base_locations_count: 30,
    can_purchase_expansion_packs: true,
    local_ai_quality: 7,
    cloud_ai_available: true,
    cloud_ai_quality: 10,
    standard_art_included: true,
    can_generate_premium_art: true,
    premium_art_cost_essence: 0     // Free for subscribers
  }
};
```

---

## 2. Essence Token System

### Essence Balance

```typescript
/**
 * Player's Essence token balance
 */
interface EssenceBalance {
  player_id: PlayerID;
  
  // Current balance
  current_balance: number;
  
  // Sources
  earned_daily: number;
  earned_achievements: number;
  purchased: number;
  gifted: number;
  
  // Spending
  spent_on_books: number;
  spent_on_images: number;
  spent_on_content: number;
  
  // Daily grant
  last_daily_grant: ISO8601String;
  daily_grant_streak: number;
  next_daily_grant: ISO8601String;
  
  // History
  transaction_history: EssenceTransaction[];
  
  // Never expires
  expiration_date: null;            // Essence never expires
}

/**
 * Essence transaction
 */
interface EssenceTransaction {
  transaction_id: string;
  timestamp: ISO8601String;
  
  // Type
  transaction_type: EssenceTransactionType;
  
  // Amount
  amount: number;
  amount_type: "earned" | "spent";
  
  // Context
  source?: string;
  spent_on?: string;
  
  // Balance after
  balance_after: number;
}

enum EssenceTransactionType {
  DailyGrant = "daily_grant",
  Purchase = "purchase",
  Achievement = "achievement",
  Gift = "gift",
  BookGeneration = "book_generation",
  ImageGeneration = "image_generation",
  ContentPurchase = "content_purchase",
  Refund = "refund"
}
```

### Essence Products

```typescript
/**
 * Purchasable Essence packages
 */
interface EssencePackage {
  package_id: string;
  package_name: string;
  
  // Content
  essence_amount: number;
  bonus_essence?: number;
  total_essence: number;
  
  // Pricing
  price_usd: number;
  price_per_essence: number;
  
  // Display
  display_order: number;
  recommended: boolean;
  best_value: boolean;
  
  // Restrictions
  limited_time: boolean;
  available_until?: ISO8601String;
  max_purchases_per_user?: number;
}

/**
 * Standard Essence packages
 */
const ESSENCE_PACKAGES: EssencePackage[] = [
  {
    package_id: "essence_starter",
    package_name: "Starter",
    essence_amount: 100,
    bonus_essence: 0,
    total_essence: 100,
    price_usd: 1.99,
    price_per_essence: 0.0199,
    display_order: 1,
    recommended: false,
    best_value: false,
    limited_time: false
  },
  {
    package_id: "essence_casual",
    package_name: "Casual",
    essence_amount: 500,
    bonus_essence: 50,
    total_essence: 550,
    price_usd: 9.99,
    price_per_essence: 0.0182,
    display_order: 2,
    recommended: true,
    best_value: false,
    limited_time: false
  },
  {
    package_id: "essence_enthusiast",
    package_name: "Enthusiast",
    essence_amount: 1200,
    bonus_essence: 300,
    total_essence: 1500,
    price_usd: 24.99,
    price_per_essence: 0.0167,
    display_order: 3,
    recommended: false,
    best_value: true,
    limited_time: false
  },
  {
    package_id: "essence_storyteller",
    package_name: "Storyteller",
    essence_amount: 2500,
    bonus_essence: 1000,
    total_essence: 3500,
    price_usd: 49.99,
    price_per_essence: 0.0143,
    display_order: 4,
    recommended: false,
    best_value: false,
    limited_time: false
  }
];
```

---

## 3. Subscriptions

### Subscription Plans

```typescript
/**
 * Subscription plan definition
 */
interface SubscriptionPlan {
  plan_id: string;
  plan_name: string;
  subscription_type: SubscriptionType;
  
  // Pricing
  price_usd: number;
  billing_period_days: number;
  price_per_month: number;
  
  // Benefits
  monthly_essence_grant: number;
  premium_book_generation_free: boolean;
  premium_image_generation_free: boolean;
  unlimited_archive: boolean;
  cloud_ai_access: boolean;
  
  // Savings
  discount_vs_monthly_pct: number;
  
  // Display
  display_order: number;
  recommended: boolean;
  best_value: boolean;
}

/**
 * Standard subscription plans
 */
const SUBSCRIPTION_PLANS: SubscriptionPlan[] = [
  {
    plan_id: "sub_monthly",
    plan_name: "Monthly Unlimited",
    subscription_type: SubscriptionType.Monthly,
    price_usd: 4.99,
    billing_period_days: 30,
    price_per_month: 4.99,
    monthly_essence_grant: 500,
    premium_book_generation_free: true,
    premium_image_generation_free: true,
    unlimited_archive: true,
    cloud_ai_access: true,
    discount_vs_monthly_pct: 0,
    display_order: 1,
    recommended: true,
    best_value: false
  },
  {
    plan_id: "sub_quarterly",
    plan_name: "Quarterly Unlimited",
    subscription_type: SubscriptionType.Quarterly,
    price_usd: 12.99,
    billing_period_days: 90,
    price_per_month: 4.33,
    monthly_essence_grant: 500,
    premium_book_generation_free: true,
    premium_image_generation_free: true,
    unlimited_archive: true,
    cloud_ai_access: true,
    discount_vs_monthly_pct: 13,
    display_order: 2,
    recommended: false,
    best_value: false
  },
  {
    plan_id: "sub_yearly",
    plan_name: "Yearly Unlimited",
    subscription_type: SubscriptionType.Yearly,
    price_usd: 39.99,
    billing_period_days: 365,
    price_per_month: 3.33,
    monthly_essence_grant: 500,
    premium_book_generation_free: true,
    premium_image_generation_free: true,
    unlimited_archive: true,
    cloud_ai_access: true,
    discount_vs_monthly_pct: 33,
    display_order: 3,
    recommended: false,
    best_value: true
  }
];
```

### Subscription State

```typescript
/**
 * Player's subscription state
 */
interface SubscriptionState {
  player_id: PlayerID;
  
  // Current subscription
  active: boolean;
  plan_id?: string;
  plan_name?: string;
  
  // Billing
  started_at?: ISO8601String;
  current_period_start?: ISO8601String;
  current_period_end?: ISO8601String;
  renews_at?: ISO8601String;
  cancels_at?: ISO8601String;
  
  // Status
  status: SubscriptionStatus;
  payment_method?: PaymentMethod;
  
  // Benefits
  benefits_active: boolean;
  monthly_essence_granted: boolean;
  last_essence_grant?: ISO8601String;
  
  // History
  subscription_history: SubscriptionPeriod[];
  total_subscription_months: number;
}

enum SubscriptionStatus {
  Active = "active",
  PastDue = "past_due",
  Canceled = "canceled",
  Paused = "paused",
  Expired = "expired"
}

interface SubscriptionPeriod {
  period_id: string;
  plan_id: string;
  started: ISO8601String;
  ended: ISO8601String;
  duration_days: number;
  amount_paid: number;
}

interface PaymentMethod {
  method_type: "credit_card" | "paypal" | "google_play" | "apple_pay";
  last_four?: string;
  expires?: string;
}
```

---

## 4. Expansion Packs

### Expansion Pack Definition

```typescript
/**
 * Expansion pack
 */
interface ExpansionPack {
  pack_id: PackID;
  pack_name: string;
  pack_category: PackCategory;
  
  // Pricing
  price_usd: number;
  price_essence?: number;           // Can also buy with Essence
  
  // Content
  new_cards: number;
  new_npcs: number;
  new_locations: number;
  new_aspirations: number;
  new_arcs: number;
  
  // Details
  description: string;
  theme: string;
  content_tags: string[];
  
  // Requirements
  requires_base_game: boolean;
  requires_packs?: PackID[];
  
  // Status
  released: boolean;
  release_date?: ISO8601String;
  early_access: boolean;
  
  // Assets
  thumbnail: URL;
  preview_images: URL[];
  trailer_url?: URL;
  
  schema_version: SemanticVersion;
}

enum PackCategory {
  Career = "career",
  Relationship = "relationship",
  Creative = "creative",
  Adventure = "adventure",
  Life_Stage = "life_stage",
  Culture = "culture",
  Special = "special"
}

/**
 * Example expansion packs
 */
const EXPANSION_PACKS: ExpansionPack[] = [
  {
    pack_id: "pack_creative_arts",
    pack_name: "Creative Arts Pack",
    pack_category: PackCategory.Creative,
    price_usd: 4.99,
    price_essence: 500,
    new_cards: 80,
    new_npcs: 8,
    new_locations: 5,
    new_aspirations: 12,
    new_arcs: 6,
    description: "Photography, painting, music, writing—pursue creative passions",
    theme: "creative_fulfillment",
    content_tags: ["photography", "painting", "music", "writing", "art"],
    requires_base_game: true,
    released: true,
    early_access: false,
    thumbnail: "pack_creative_arts_thumb.png",
    preview_images: [],
    schema_version: "1.0.0"
  },
  {
    pack_id: "pack_entrepreneurship",
    pack_name: "Entrepreneurship Pack",
    pack_category: PackCategory.Career,
    price_usd: 4.99,
    price_essence: 500,
    new_cards: 75,
    new_npcs: 6,
    new_locations: 4,
    new_aspirations: 10,
    new_arcs: 5,
    description: "Start a business, build an empire, navigate startup life",
    theme: "business_building",
    content_tags: ["business", "startup", "entrepreneur", "finance"],
    requires_base_game: true,
    released: true,
    early_access: false,
    thumbnail: "pack_entrepreneurship_thumb.png",
    preview_images: [],
    schema_version: "1.0.0"
  }
  // ... more packs
];
```

### Pack Ownership

```typescript
/**
 * Player's owned packs
 */
interface PackOwnership {
  player_id: PlayerID;
  
  // Owned packs
  owned_packs: OwnedPack[];
  
  // Stats
  total_packs_owned: number;
  total_spent_on_packs: number;
  
  // Unlocked content
  total_unlocked_cards: number;
  total_unlocked_npcs: number;
  total_unlocked_locations: number;
}

interface OwnedPack {
  pack_id: PackID;
  purchased_at: ISO8601String;
  purchased_with: "usd" | "essence";
  amount_paid: number;
  
  // Usage
  content_unlocked: boolean;
  cards_played_from_pack: number;
  npcs_met_from_pack: number;
  
  // Status
  installed: boolean;
  version: SemanticVersion;
}
```

---

## 5. Premium Content Generation

### Book Generation Costs

```typescript
/**
 * Book generation pricing
 */
interface BookGenerationPricing {
  book_type: "free" | "premium";
  
  // Cost
  essence_cost: number;
  free_for_subscribers: boolean;
  
  // Quality
  word_count_range: [number, number];
  ai_quality: number;               // 7/10 or 10/10
  
  // Features
  multi_pov: boolean;
  literary_techniques: boolean;
  rich_prose: boolean;
  sensory_details: boolean;
  
  // Generation time
  estimated_generation_minutes: number;
}

const BOOK_PRICING = {
  free: {
    book_type: "free",
    essence_cost: 0,
    free_for_subscribers: true,
    word_count_range: [3000, 5000],
    ai_quality: 7,
    multi_pov: false,
    literary_techniques: false,
    rich_prose: false,
    sensory_details: false,
    estimated_generation_minutes: 2
  },
  premium: {
    book_type: "premium",
    essence_cost: 250,
    free_for_subscribers: true,
    word_count_range: [12000, 15000],
    ai_quality: 10,
    multi_pov: true,
    literary_techniques: true,
    rich_prose: true,
    sensory_details: true,
    estimated_generation_minutes: 10
  }
};
```

### Image Generation Costs

```typescript
/**
 * Image generation pricing
 */
interface ImageGenerationPricing {
  image_type: "standard" | "premium";
  
  // Cost
  essence_cost: number;
  free_for_subscribers: boolean;
  
  // Quality
  resolution: string;
  style_options: number;
  customization_level: "low" | "medium" | "high";
  
  // Generation
  generation_time_seconds: number;
}

const IMAGE_PRICING = {
  standard: {
    image_type: "standard",
    essence_cost: 0,
    free_for_subscribers: true,
    resolution: "1024x1024",
    style_options: 3,
    customization_level: "low",
    generation_time_seconds: 5
  },
  premium: {
    image_type: "premium",
    essence_cost: 50,
    free_for_subscribers: true,
    resolution: "2048x2048",
    style_options: 10,
    customization_level: "high",
    generation_time_seconds: 15
  }
};
```

---

## 6. Special Editions

### Legacy Edition

```typescript
/**
 * Legacy Edition (one-time purchase)
 */
interface LegacyEdition {
  edition_id: "legacy_edition";
  price_usd: 49.99;
  
  // Lifetime benefits
  lifetime_benefits: {
    all_current_packs: true;
    all_future_packs: true;
    unlimited_archive: true;
    monthly_essence_grant: 1000;
    priority_support: true;
    exclusive_content: true;
    cloud_ai_access: true;
  };
  
  // Equivalent value
  equivalent_subscription_years: number; // ~5 years
  
  // Status
  available: boolean;
  limited_time: boolean;
  max_purchases: number | null;     // Unlimited
}
```

---

## 7. Entitlement Tracking

### Player Entitlements

```typescript
/**
 * What player has access to
 */
interface PlayerEntitlements {
  player_id: PlayerID;
  
  // Tier
  current_tier: TierLevel;
  
  // Subscription
  subscription_active: boolean;
  subscription_benefits: string[];
  
  // Owned content
  owned_packs: PackID[];
  owned_art_styles: string[];
  legacy_edition: boolean;
  
  // Access rights
  can_generate_premium_books: boolean;
  premium_book_cost: number;        // 0 if subscriber
  can_generate_premium_images: boolean;
  premium_image_cost: number;       // 0 if subscriber
  unlimited_archive: boolean;
  cloud_ai_access: boolean;
  
  // Limits
  archive_cards_per_season: number | "unlimited";
  daily_essence_grant: number;
  
  // Validation
  last_validated: ISO8601String;
  entitlement_valid: boolean;
}
```

---

## Notes for LLM Analysis

When validating monetization schemas:

1. **Ethical Constraints**: No pay-to-win, no timers, no expiration, no dark patterns
2. **Free Tier**: Full game (470 cards, 50 NPCs, all features), 25 Essence/day
3. **Essence Never Expires**: Critical - tokens never expire
4. **Pricing**: Essence packages $1.99-$49.99, subscriptions $4.99-$39.99/year
5. **Subscription Benefits**: Premium books free, premium images free, unlimited archive
6. **Pack Pricing**: Expansion packs $4.99-$7.99 or 500-800 Essence
7. **Book Costs**: Free = 0 Essence, Premium = 250 Essence (free for subscribers)
8. **Image Costs**: Standard = 0 Essence, Premium = 50 Essence (free for subscribers)

**Cross-schema dependencies**:
- PackID from card-system (packs add cards, NPCs, locations)
- PlayerID from character-system (all monetization tied to player)
- Book generation costs from novel-generation schema
- Archive limits from archive-persistence schema
- All purchased content must integrate with card-system
- Subscription benefits affect gameplay-mechanics capabilities
- Essence spending validated against balance
- Entitlements checked before premium content generation

