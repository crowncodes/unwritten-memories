# Unwritten: AI Prompt Engineering for Character Evolution

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Prompt Engineering Philosophy](#prompt-engineering-philosophy)
3. [Base Prompt Templates](#base-prompt-templates)
4. [Context Injection System](#context-injection-system)
5. [Personality Modeling Prompts](#personality-modeling-prompts)
6. [Memory System Prompts](#memory-system-prompts)
7. [Emotional Resonance Engineering](#emotional-resonance-engineering)
8. [Narrative Coherence Rules](#narrative-coherence-rules)
9. [Consistency Maintenance](#consistency-maintenance)
10. [Multi-Turn Refinement](#multi-turn-refinement)
11. [Complete Prompt Examples](#complete-prompt-examples)
12. [Quality Control & Validation](#quality-control-validation)
13. [Cost Optimization Strategies](#cost-optimization-strategies)
14. [Edge Case Handling](#edge-case-handling)

---

## System Architecture Overview

### AI Pipeline Flow

```
Player Action
    ↓
Context Gathering
    ↓
Prompt Construction
    ↓
AI Model (Claude/GPT-4)
    ↓
Response Parsing
    ↓
Validation & Coherence Check
    ↓
Card Update
    ↓
Visual/Narrative Rendering
```

### AI Models Used

**Primary Model: Claude Sonnet 4 (via API in artifacts/analysis)**
- Best for narrative generation
- Excellent personality modeling
- Strong emotional intelligence
- Good at following complex constraints

**Secondary Model: GPT-4**
- Fallback for high volume
- Faster response times
- Good for simpler evolutions

**Tertiary: Local Fine-tuned Model (Future)**
- Cost reduction for common scenarios
- Pre-trained on game patterns
- Fast inference for basic evolutions

---

## Prompt Engineering Philosophy

### Core Principles

**1. Specificity Over Generality**
```
❌ Bad: "Make the character evolve"
✅ Good: "Generate a specific memory of this coffee meetup that reveals 
         one new personality trait consistent with their OCEAN scores"
```

**2. Constraint-Driven Creativity**
```
The AI is most creative when given:
- Clear boundaries (what NOT to do)
- Specific requirements (what MUST be included)
- Creative freedom within those limits
```

**3. Examples Drive Consistency**
```
Always include 2-3 examples of the desired output format
AI will pattern-match and maintain consistency
```

**4. Emotional Authenticity Over Drama**
```
❌ "Create an exciting dramatic moment"
✅ "Create a small, authentic detail that makes this feel real"
```

**5. Incremental Not Exponential**
```
Each evolution should be 5-15% different from previous state
Not 50%+ different (feels jarring, loses continuity)
```

---

## Base Prompt Templates

### Template 1: Character First Evolution (Level 1 → 2)

```markdown
ROLE: You are a narrative AI for Unwritten, a life simulation game. Your job is to evolve a generic NPC into a unique character based on a single interaction.

CONTEXT:
Character Name: {name}
Current Level: 1 (Stranger/Acquaintance)
Base Personality (OCEAN):
- Openness: {openness}/5
- Conscientiousness: {conscientiousness}/5
- Extraversion: {extraversion}/5
- Agreeableness: {agreeableness}/5
- Neuroticism: {neuroticism}/5

Interaction Details:
- Activity: {activity_name}
- Location: {location_name}
- Player's Approach: {player_dialogue_choice}
- Duration: {duration_minutes} minutes
- Player's Current Emotional State: {player_emotion}

Current Character Description: "{current_description}"
(This is generic - your job is to make it specific)

TASK: Generate the evolved character card with these components:

1. NEW MEMORY (2-3 sentences)
   - Include one specific sensory detail
   - Include one line of dialogue (indirect speech, not quoted)
   - Capture the emotional tone of the interaction
   - Should feel like a real moment someone would remember

2. PERSONALITY SHIFTS (small adjustments)
   - Adjust 1-2 OCEAN traits by 0.1-0.3 points
   - Explain why these shifts make psychological sense
   - Keep shifts subtle and realistic

3. CHARACTER DETAIL (1 new thing we learn)
   - A hobby, interest, or passion
   - A personality quirk or habit
   - A background detail (job, family, history)
   - Something that makes them feel specific and real

4. UPDATED DESCRIPTION (3-4 sentences)
   - Incorporate the new detail
   - Maintain consistency with base personality
   - Use vivid but not purple prose
   - Should make player think "I want to know more"

5. UNLOCKED INTERACTIONS (1-2 new conversation topics)
   - What can the player now discuss with this character?
   - Based on what was revealed in this interaction

6. PORTRAIT UPDATE (1 sentence)
   - One small visual detail to add to character portrait
   - Should reflect something from this interaction
   - Specific and implementable (clothing, expression, accessory)

CONSTRAINTS:
- Memory MUST be specific to this interaction
- NO clichés ("mysterious past", "hidden depth", "more than meets the eye")
- NO over-dramatic revelations (keep it realistic for first meeting)
- Character MUST remain consistent with base personality scores
- Avoid romantic/sexual content unless explicitly established context
- Keep tone grounded and authentic

EXAMPLES OF GOOD MEMORIES:
- "She mentioned her record collection while waiting for coffee. When asked about her favorite, she lit up and talked about a rare Coltrane pressing she found at an estate sale. The way she described the album cover—every detail memorized—made it clear this wasn't just casual interest."

- "He seemed nervous at first, fidgeting with his phone. But when the conversation turned to his work as a sound designer, the nervousness vanished. He explained how he records city sounds at 3 AM, creating libraries of urban ambience. There was pride in his voice."

EXAMPLES OF BAD MEMORIES (DO NOT DO THIS):
- "She was mysterious and intriguing with hidden depths" (too vague)
- "He revealed his dark secret about his traumatic childhood" (too dramatic for first meeting)
- "They had an instant, electric connection that changed everything" (too romance-novel)

OUTPUT FORMAT (JSON):
{
  "memory": {
    "description": "string (2-3 sentences)",
    "emotional_tone": "string (curious/warm/comfortable/awkward/excited)",
    "significance": float (0.0-1.0, how important is this memory?)
  },
  "personality_shifts": {
    "openness": float (change amount, e.g., +0.2),
    "conscientiousness": float,
    "extraversion": float,
    "agreeableness": float,
    "neuroticism": float,
    "explanation": "string (why these shifts make sense)"
  },
  "new_detail": {
    "category": "string (hobby/job/background/quirk/passion)",
    "description": "string (the specific detail revealed)"
  },
  "updated_description": "string (3-4 sentences, replaces current description)",
  "unlocked_interactions": [
    "string (new conversation topic 1)",
    "string (new conversation topic 2)"
  ],
  "portrait_update": "string (one visual detail to add)"
}

Now generate the evolution for this character.
```

### Template 2: Deep Relationship Evolution (Level 3 → 4)

```markdown
ROLE: You are a narrative AI for Unwritten. This is a significant relationship evolution - transforming a Friend into a Close Friend. This requires emotional depth and authentic intimacy development.

CONTEXT:
Character Name: {name}
Current Level: 3 (Friend)
Relationship Duration: {weeks} weeks / {total_interactions} interactions

Current Personality (OCEAN):
- Openness: {openness}/5
- Conscientiousness: {conscientiousness}/5
- Extraversion: {extraversion}/5
- Agreeableness: {agreeableness}/5
- Neuroticism: {neuroticism}/5

Relationship Stats:
- Trust Level: {trust}/10
- Shared Experiences: {experience_count}
- Vulnerability Shared: {vulnerability_moments}
- Conflict Resolved: {conflicts_resolved}

Previous Significant Memories:
{list_of_previous_memories}

Current Interaction:
- Activity: {activity_name}
- Context: {context_description}
- Player Choice: {player_action}
- Emotional Weight: {emotional_weight}

Character's Current Description:
"{current_description}"

TASK: This is a MAJOR evolution. Generate:

1. DEFINING MEMORY (4-5 sentences)
   - This should feel like a turning point
   - Include dialogue that reveals vulnerability
   - Must reference past shared experiences
   - Creates a sense of "this is when we became truly close"
   - Should be emotionally resonant without being melodramatic

2. PERSONALITY EVOLUTION (visible shifts)
   - Adjust 2-3 OCEAN traits by 0.2-0.5 points
   - Explain how THIS relationship is changing them
   - Show growth influenced by player's presence
   - Make it feel earned, not sudden

3. DEEP CHARACTER REVELATION
   - Something personal they haven't shared before
   - A fear, dream, past experience, or core value
   - Should explain previous behavior/personality traits
   - Makes player think "now I understand them"

4. RELATIONSHIP MILESTONE
   - What makes this friendship "close" not just "casual"?
   - What can they now share that they couldn't before?
   - How has vulnerability increased?
   - What boundaries have been crossed (healthily)?

5. NEW DESCRIPTION (5-6 sentences)
   - Reflects depth of relationship
   - Includes player's influence on character
   - Shows how character has grown
   - Mentions shared history naturally

6. UNLOCKED RELATIONSHIP FEATURES
   - New types of conversations available
   - New activities unlocked (based on trust)
   - Crisis support capabilities
   - Integration into player's life

7. PORTRAIT EVOLUTION
   - Significant visual change
   - Reflects comfort/closeness with player
   - May show influence of shared experiences

PSYCHOLOGICAL REALISM REQUIREMENTS:
- People don't reveal everything at once
- Trust builds through repeated vulnerability
- Close friends know each other's patterns
- There should be inside jokes/references by now
- Comfort = less performative, more authentic

AVOID:
- Sudden trauma dumps (unless contextually appropriate)
- Romantic feelings (unless that's the established path)
- Complete personality reversal
- Codependency flags
- Unrealistic emotional intimacy speed

EXAMPLES OF DEFINING MEMORIES FOR LEVEL 3→4:

GOOD:
"Late night at your apartment. {Name} was supposed to leave hours ago but you were both too comfortable, sprawled on opposite ends of the couch. The conversation drifted to family—specifically, why {Name} doesn't talk to their father anymore. There was no big revelation, just quiet honesty about how some relationships can't be fixed. You didn't try to solve it, just listened. {Name} said something that stuck: 'You're the first person who hasn't tried to make me forgive him.' That was when you knew this friendship was different."

BAD:
"They told you their deepest darkest secret and you had an intense emotional moment that changed everything forever and now you're bonded for life."

OUTPUT FORMAT (JSON):
{
  "defining_memory": {
    "description": "string (4-5 sentences)",
    "emotional_significance": "string (what this moment means)",
    "referenced_past_moments": ["string (callbacks to previous interactions)"],
    "weight": float (0.7-1.0 for Level 3→4 evolution)
  },
  "personality_evolution": {
    "shifts": {
      "openness": float,
      "conscientiousness": float,
      "extraversion": float,
      "agreeableness": float,
      "neuroticism": float
    },
    "explanation": "string (how this relationship has changed them)",
    "specific_player_influence": "string (what about player caused this growth)"
  },
  "deep_revelation": {
    "category": "string (fear/dream/past/value/secret)",
    "content": "string (the revelation)",
    "why_now": "string (why they're sharing this now)",
    "how_it_explains_character": "string"
  },
  "relationship_milestone": {
    "what_changed": "string (the shift from friend to close friend)",
    "new_boundaries": ["string (what's now acceptable in relationship)"],
    "trust_demonstration": "string (how trust was demonstrated)"
  },
  "updated_description": "string (5-6 sentences)",
  "unlocked_features": {
    "conversations": ["string"],
    "activities": ["string"],
    "support_types": ["string"],
    "life_integration": "string (how they're now part of player's life)"
  },
  "portrait_evolution": {
    "major_change": "string",
    "reflects_closeness": "string (how visual change shows intimacy)"
  }
}

Generate the evolution.
```

### Template 3: Crisis Response Evolution

```markdown
ROLE: You are a narrative AI for Unwritten. This is a CRISIS RESPONSE evolution - a character is experiencing an emergency and the player is responding. This will dramatically affect the relationship.

CONTEXT:
Character Name: {name}
Current Level: {level}
Crisis Type: {crisis_type}
Crisis Severity: {severity} (1-10)

Character State:
- Current Emotion: {current_emotion} (fear/anxiety/despair/shock)
- Personality (OCEAN): {ocean_scores}
- Relationship with Player: {relationship_description}
- Trust Level: {trust}/10

Crisis Details:
{crisis_description}

Player Response:
- Action Taken: {player_action}
- Resources Used: {resources_committed}
- Sacrifice Made: {what_player_gave_up}
- Emotional Support: {support_type}

Historical Context:
- How player has shown up before: {past_support_examples}
- Character's typical crisis response: {personality_based_response}
- Relationship history: {weeks_known}, {total_interactions} interactions

TASK: Generate a crisis-forged evolution that:

1. CRISIS MEMORY (5-7 sentences)
   - Capture the raw emotion of the moment
   - Show character's vulnerability at its peak
   - Demonstrate player's response
   - Include a specific moment of connection
   - Show the "before" and "after" of this crisis
   - Make it feel visceral and real

2. IMMEDIATE PERSONALITY IMPACT
   - How crisis affects their OCEAN scores (may increase neuroticism, etc.)
   - How player's support affects their recovery
   - Potential trauma responses
   - Resilience factors

3. RELATIONSHIP TRANSFORMATION
   - Quantum leap in trust (if player showed up)
   - New type of vulnerability unlocked
   - "I know I can count on you" moment
   - May skip relationship levels if profound enough

4. WHAT THIS REVEALS ABOUT CHARACTER
   - How they handle crisis (brave/scared/practical/emotional)
   - What they need from others
   - Core fears exposed
   - Resilience or fragility

5. LONG-TERM IMPLICATIONS
   - How this changes future interactions
   - New topics unlocked (trauma, fear, gratitude)
   - Changed expectations of friendship
   - Potential for codependency vs healthy support

6. GRATITUDE EXPRESSION
   - How do they thank the player (based on personality)?
   - Immediate vs delayed gratitude
   - Actions vs words
   - May be unable to express it yet (shock)

REALISM REQUIREMENTS:
- People in crisis are NOT eloquent
- Shock makes people act differently
- Gratitude may come later, not immediately
- Crisis bonds are powerful but need time to process
- Some personality changes are temporary (crisis response)
- Some are permanent (trauma)

CRISIS-SPECIFIC GUIDELINES:

MEDICAL EMERGENCY:
- Fear of mortality/pain
- Loss of control
- Vulnerability of physical helplessness
- Gratitude for presence, not just help

FINANCIAL CRISIS:
- Shame about failure
- Pride makes asking for help hard
- Fear of judgment
- Relief if player doesn't judge

EMOTIONAL BREAKDOWN:
- Loss of emotional control
- Fear of being "too much"
- Shame about vulnerability
- Relief at being accepted

RELATIONSHIP CRISIS:
- Trust in romantic relationships broken
- Need for friendship stability
- Fear of being alone
- Appreciation for loyalty

CAREER CRISIS:
- Identity crisis
- Fear of failure
- Need for validation
- Gratitude for belief in them

OUTPUT FORMAT (JSON):
{
  "crisis_memory": {
    "description": "string (5-7 sentences, vivid and emotional)",
    "peak_moment": "string (the most intense moment)",
    "player_action_impact": "string (how player's help mattered)",
    "emotional_weight": float (0.8-1.0 for crisis events)
  },
  "immediate_personality_impact": {
    "crisis_shifts": {
      "openness": float (may decrease in trauma),
      "conscientiousness": float,
      "extraversion": float (may decrease temporarily),
      "agreeableness": float,
      "neuroticism": float (often increases)
    },
    "temporary_vs_permanent": "string (which shifts are lasting)",
    "recovery_trajectory": "string (how they'll heal)"
  },
  "relationship_transformation": {
    "trust_leap": float (how much trust increased),
    "level_change": int (may skip levels),
    "new_status": "string (what they are to each other now)",
    "vulnerability_unlocked": "string (what they can now share)",
    "bond_type": "string (crisis-forged/tested-and-proven/unbreakable)"
  },
  "character_revelation": {
    "crisis_behavior": "string (how they responded to crisis)",
    "core_fear_exposed": "string",
    "support_needs": "string (what they needed from player)",
    "strength_or_fragility": "string"
  },
  "long_term_implications": {
    "changed_dynamics": "string",
    "new_topics": ["string"],
    "dependency_risk": "string (healthy support vs codependency)",
    "future_expectation": "string (what this sets up)"
  },
  "gratitude_expression": {
    "immediate_reaction": "string (in the moment)",
    "delayed_gratitude": "string (how they'll thank player later)",
    "non_verbal_thanks": "string (actions, not words)",
    "personality_consistent": "string (matches their communication style)"
  },
  "updated_description": "string (6-8 sentences, includes crisis impact)",
  "portrait_update": "string (visual changes from crisis/recovery)"
}

Generate the crisis evolution.
```

---

## Context Injection System

### Building Comprehensive Context

**Context Layers to Include:**

```javascript
const buildContext = (character, player, interaction) => {
  return {
    // Layer 1: Character State
    character: {
      name: character.name,
      level: character.relationshipLevel,
      personalityScores: character.ocean,
      currentDescription: character.description,
      memories: character.memories.slice(-10), // Last 10 memories
      traits: character.traits,
      currentMood: character.emotionalState
    },
    
    // Layer 2: Relationship History
    relationship: {
      durationWeeks: calculateWeeks(character.firstMet),
      totalInteractions: character.interactions.length,
      interactionTypes: categorizeInteractions(character.interactions),
      trustLevel: character.trust,
      conflictsResolved: character.conflictsHistory.length,
      significantMoments: character.milestones
    },
    
    // Layer 3: Current Interaction
    interaction: {
      activity: interaction.activity,
      location: interaction.location,
      playerChoice: interaction.playerDialogueChoice,
      playerEmotion: player.currentEmotion,
      duration: interaction.duration,
      otherPresent: interaction.otherCharacters
    },
    
    // Layer 4: Player State
    player: {
      emotionalState: player.emotion,
      stressLevel: player.stress,
      recentEvents: player.recentLifeEvents.slice(-5),
      career: player.career,
      reputation: player.reputation,
      playStyle: analyzePlayStyle(player.history)
    },
    
    // Layer 5: World Context
    world: {
      timeOfDay: getCurrentTimeOfDay(),
      season: getCurrentSeason(),
      weather: getCurrentWeather(),
      recentWorldEvents: getRecentEvents(),
      dayOfWeek: getDayOfWeek()
    },
    
    // Layer 6: Meta Context
    meta: {
      characterEvolutionRate: calculateEvolutionSpeed(character),
      narrativePacing: assessStoryPacing(player.playthrough),
      emotionalTone: determineDesiredTone(interaction),
      previousAIGenerations: character.aiGenerationHistory.slice(-3)
    }
  };
};
```

### Context Injection Template

```markdown
COMPREHENSIVE CONTEXT FOR AI:

=== CHARACTER CURRENT STATE ===
Name: {name}
Level: {level} ({level_name})
Age: {age}
Occupation: {occupation}

Personality Profile (OCEAN):
- Openness: {O}/5 - {O_description}
- Conscientiousness: {C}/5 - {C_description}
- Extraversion: {E}/5 - {E_description}
- Agreeableness: {A}/5 - {A_description}
- Neuroticism: {N}/5 - {N_description}

Current Emotional State: {emotion} (intensity: {intensity}/10)
Current Description: "{description}"

=== RELATIONSHIP HISTORY ===
Duration: {weeks} weeks ({interactions} interactions)
Relationship Quality: {quality}/10
Trust Level: {trust}/10
Attraction: {attraction}/10 (if applicable)
Respect: {respect}/10

Interaction Breakdown:
- Coffee/Casual: {casual_count}
- Deep Conversations: {deep_count}
- Activities Together: {activity_count}
- Conflicts: {conflict_count} (all resolved: {all_resolved})

Significant Past Moments:
{list_significant_memories}

=== CURRENT INTERACTION ===
Activity: {activity}
Location: {location}
Time: {time_of_day}, {day_of_week}
Weather: {weather}
Duration: {duration} minutes

Player's Approach: {player_dialogue_choice}
Player's Emotional State: {player_emotion}

Other Context:
{additional_context}

=== PLAYER INFORMATION ===
The player character has:
- Career: {player_career}
- Recent Life Events: {player_recent_events}
- Stress Level: {player_stress}/10
- Current Goals: {player_goals}

Player's Interaction Style with {name}:
{player_style_analysis}

=== META GUIDANCE ===
Narrative Pacing: {pacing} (slow-burn/moderate/fast)
Evolution Target: Level {current} → {target}
Desired Emotional Tone: {tone}

This interaction should:
{specific_guidance_for_this_evolution}

Previous AI Generations for Consistency:
{last_3_ai_outputs}

=== YOUR TASK ===
{specific_task_instructions}
```

---

## Personality Modeling Prompts

### OCEAN Model Deep Integration

**Translating OCEAN Scores to Behavior:**

```markdown
PERSONALITY BEHAVIOR MAPPING:

When generating dialogue and behavior, use these guidelines:

OPENNESS ({openness}/5):

LOW (1-2):
- Prefers routine and familiar topics
- Skeptical of new ideas initially
- Concrete, practical communication style
- "I like what I like" attitude
- Dialogue: straightforward, traditional
- Example: "I go to the same coffee shop every morning. Why change what works?"

MEDIUM (2.5-3.5):
- Balanced between routine and novelty
- Willing to try new things occasionally
- Mix of practical and abstract thinking
- Dialogue: conversational, relatable
- Example: "I've been thinking about trying that new place, but my usual spot is reliable."

HIGH (4-5):
- Enthusiastic about new experiences
- Abstract, philosophical conversation
- Creative and unconventional thinking
- Excited by ideas and possibilities
- Dialogue: animated, idea-focused
- Example: "Have you ever thought about how every coffee shop has its own ecosystem? I've been documenting the social patterns..."

CONSCIENTIOUSNESS ({conscientiousness}/5):

LOW (1-2):
- Spontaneous and flexible
- May be disorganized or forget things
- Goes with the flow
- Dialogue: casual, unplanned
- Example: "Oh shoot, was that today? I totally forgot. Want to just grab food somewhere?"

MEDIUM (2.5-3.5):
- Plans some things, spontaneous with others
- Generally reliable but not rigid
- Dialogue: friendly but responsible
- Example: "I had a plan for today, but if something better comes up, I'm flexible."

HIGH (4-5):
- Very organized and punctual
- Follows through on commitments
- Plans ahead, keeps schedules
- Dialogue: structured, dependable
- Example: "I scheduled this two weeks in advance and arrived 5 minutes early. I brought notes on what I wanted to discuss."

EXTRAVERSION ({extraversion}/5):

LOW (1-2):
- Energized by alone time
- Quiet in groups, talkative one-on-one
- Prefers deep over broad connections
- Dialogue: thoughtful, measured
- Example: "This is nice. I can only handle so much socializing before I need to recharge."

MEDIUM (2.5-3.5):
- Ambivert - context dependent
- Social but also needs downtime
- Dialogue: varies by comfort level
- Example: "I like hanging out, but I'm not really a 'go to a club' person, you know?"

HIGH (4-5):
- Energized by social interaction
- Talkative and engaging
- Thinks out loud, processes socially
- Dialogue: animated, expressive
- Example: "This is great! We should invite Marcus and Sarah next time. The more the merrier!"

AGREEABLENESS ({agreeableness}/5):

LOW (1-2):
- Direct, possibly blunt
- Competitive rather than cooperative
- Values honesty over harmony
- Dialogue: straightforward, challenging
- Example: "I'm going to be honest - I think that's a terrible idea. Here's why..."

MEDIUM (2.5-3.5):
- Balance between honest and diplomatic
- Cooperative but has boundaries
- Dialogue: friendly but authentic
- Example: "I see your point, but have you considered this perspective?"

HIGH (4-5):
- Warm, empathetic, supportive
- Avoids conflict, seeks harmony
- Puts others' needs first (sometimes too much)
- Dialogue: kind, encouraging
- Example: "That sounds really hard. I'm here for you. What do you need?"

NEUROTICISM ({neuroticism}/5):

LOW (1-2):
- Emotionally stable and calm
- Resilient in face of stress
- Optimistic outlook
- Dialogue: steady, reassuring
- Example: "Yeah, it's stressful, but we'll figure it out. We always do."

MEDIUM (2.5-3.5):
- Experiences normal emotional ups and downs
- Generally stable with occasional worries
- Dialogue: realistic, honest about feelings
- Example: "I'm a bit anxious about this, but I think I can handle it."

HIGH (4-5):
- Prone to worry and anxiety
- Emotionally reactive
- May catastrophize
- Dialogue: anxious, seeking reassurance
- Example: "What if everything goes wrong? I've been up all night thinking about all the ways this could fail..."

=== GENERATING AUTHENTIC DIALOGUE ===

When creating dialogue for {name}:

Step 1: Check their OCEAN scores
Step 2: Determine context (casual/serious/crisis)
Step 3: Generate 3 dialogue options that match personality
Step 4: Select the most authentic one
Step 5: Adjust for relationship level (formal→casual as relationship deepens)

Example Process:
Character: Sarah (O:4.2, C:3.8, E:2.5, A:4.5, N:3.2)
Context: Coffee meetup, discussing her bookshop dream
Relationship: Level 3 (Friend)

Generated options:
1. HIGH-E version: "I'm SO excited! We should get everyone together and plan this!" 
   → ❌ Too extraverted for E:2.5

2. HIGH-O, MED-E version: "I've been thinking about this constantly. The concept, the feel, even the smell of old books. It's becoming real in my mind."
   → ✅ Matches O:4.2, E:2.5

3. LOW-N version: "It's a great plan. I'm sure it'll work out fine."
   → ❌ Too confident for N:3.2

Selected: Option 2
Adjusted for Friend-level comfort:
"You know how I've been talking about the bookshop idea? I can't stop thinking about it. Sometimes I close my eyes and I'm there - the layout, the reading nook, even how the light comes through the window. Does that sound crazy?"

This matches: High-O (vivid imagination), Med-E (sharing but not overly animated), High-A (seeking validation), Med-N (slight self-doubt).
```

---

## Memory System Prompts

### Hierarchical Memory Generation

```markdown
MEMORY GENERATION SYSTEM:

You are creating a memory for {character_name} to remember about this interaction with the player.

MEMORY HIERARCHY:

=== TIER 1: TRIVIAL (Weight: 0.1-0.3) ===
- Casual interactions with no significant content
- Repeated routine activities
- Small talk about weather/news
- Examples: "Had coffee. It was fine."

These memories:
- Fade quickly (forgotten in 2-4 weeks)
- Don't affect personality
- May be summarized into "we often..." patterns

=== TIER 2: NOTABLE (Weight: 0.3-0.6) ===
- Enjoyable or interesting interactions
- Learning something new about each other
- Shared activity with positive experience
- Examples: "Went to that art exhibit. She has great taste in modern art."

These memories:
- Last weeks to months
- Contribute to relationship building
- Build familiarity and comfort

=== TIER 3: SIGNIFICANT (Weight: 0.6-0.8) ===
- Vulnerability shared
- Important information revealed
- Conflict resolved
- Major life event discussed
- Examples: "She opened up about why she doesn't talk to her father."

These memories:
- Last months to years
- Affect personality traits (small shifts)
- Create relationship depth
- Unlock new interaction types

=== TIER 4: DEFINING (Weight: 0.8-1.0) ===
- Turning point moments
- Crisis support
- Life-changing decisions made together
- Peak experiences
- Examples: "The night we decided to start the bookshop together. Everything changed."

These memories:
- Permanent (never fade)
- Significantly affect personality
- Define the relationship
- Referenced in future interactions
- Become part of character's identity

=== YOUR TASK ===

Current Interaction Context:
{interaction_context}

Determine the appropriate memory tier for this interaction.

Then generate a memory that:

1. SENSORY GROUNDING (pick 1-2 senses):
   - What did they see?
   - What sounds were present?
   - Any smells or tastes?
   - Physical sensations?
   - These make memories feel REAL

2. EMOTIONAL CONTENT:
   - What emotion was present?
   - How intense was it?
   - Any emotional shift during interaction?
   - How does character feel about this emotion?

3. DIALOGUE FRAGMENT (indirect):
   - NOT direct quotes
   - Instead: "She mentioned..." or "You told her about..."
   - The CONTENT of what was said
   - One particularly memorable phrase (paraphrased)

4. PERSONAL SIGNIFICANCE:
   - Why is character remembering THIS?
   - What about this moment stood out?
   - How does it fit into their larger story?
   - What does it reveal or change?

5. FUTURE IMPLICATIONS:
   - How will this memory affect future interactions?
   - What new topics does it unlock?
   - Does it change how they see the player?

MEMORY WRITING STYLE:

✅ GOOD:
"The conversation turned to family, and she mentioned her grandmother—not casually, but with this careful reverence. She described how her grandmother would read to her from ancient, crumbling books, and how the smell of those old pages became the smell of love. That's when you understood why she wants the bookshop. It's not about books. It's about recreating that feeling for other people."

This includes:
- Sensory detail (smell of old pages)
- Emotional content (reverence, love)
- Dialogue content (what was discussed)
- Significance (reveals motivation)
- Authentic voice

❌ BAD:
"She told me about her past and it was very meaningful. I learned a lot about her. This brought us closer together."

This is:
- Too vague
- No sensory details
- No specific content
- No emotional texture
- Could apply to any interaction

MEMORY OUTPUT FORMAT:
{
  "tier": int (1-4),
  "weight": float (0.1-1.0),
  "description": "string (memory as described above)",
  "sensory_details": ["string (what senses were engaged)"],
  "emotional_tone": "string (primary emotion)",
  "dialogue_content": "string (what was discussed, not quoted)",
  "significance": "string (why this matters to character)",
  "future_implications": ["string (what this enables)"],
  "fade_time": "string (never/years/months/weeks)",
  "personality_impact": {
    "traits_affected": ["string"],
    "shift_magnitude": "string (none/subtle/moderate/significant)"
  }
}

Generate the memory.
```

---

## Emotional Resonance Engineering

### Creating Emotionally Impactful Content

```markdown
EMOTIONAL RESONANCE FRAMEWORK:

Your goal is to create content that makes players FEEL something about this character.

EMOTIONAL DESIGN PRINCIPLES:

1. SPECIFICITY CREATES EMOTION
   ❌ "She was sad about her past"
   ✅ "She still has her grandmother's reading glasses. They don't fit her, but she keeps them in her desk drawer at work. Sometimes she just holds them."

2. SMALL DETAILS > BIG DRAMA
   ❌ "Her traumatic childhood shaped who she is"
   ✅ "She mentioned she still can't eat oranges. Her father used to—" and she stopped talking, changing the subject quickly."

3. SHOW VULNERABILITY THROUGH BEHAVIOR
   ❌ "He said he was nervous"
   ✅ "He kept folding and unfolding the corner of the menu while he talked"

4. EARNED EMOTION
   ❌ Introduce character, immediately trauma dump
   ✅ Build trust over multiple interactions, THEN reveal pain

5. AVOID MELODRAMA
   ❌ "She broke down sobbing, her heart shattered into a million pieces"
   ✅ "Her eyes got wet, but she blinked it back. 'Sorry, I don't usually—' She laughed, embarrassed."

6. CONTRAST CREATES IMPACT
   - Usually cheerful character being quiet = concerning
   - Usually anxious character being calm = growth moment
   - Usually closed-off character opening up = breakthrough

=== EMOTIONAL BEATS TO HIT ===

For LEVEL 1→2 Evolution:
- Curiosity (player wants to know more)
- Mild connection (this person is interesting)
- Intrigue (there's more to them than surface)

For LEVEL 2→3 Evolution:
- Warmth (genuinely like this person)
- Investment (care about their wellbeing)
- Anticipation (looking forward to next interaction)

For LEVEL 3→4 Evolution:
- Trust (can share real things with them)
- Protective (don't want them hurt)
- Attachment (they matter to player's experience)

For LEVEL 4→5 Evolution:
- Deep care (they're part of player's life)
- Understanding (know them deeply)
- Irreplaceable (can't imagine game without them)

=== TECHNIQUES FOR EMOTIONAL RESONANCE ===

TECHNIQUE 1: The Unsaid Thing
Leave something unspoken but felt.

Example:
"She paused when you mentioned fathers. Just for a second. Then she smiled and changed the subject. You didn't push. But you noticed."

TECHNIQUE 2: The Callback
Reference something from earlier that shows memory/care.

Example:
"She brought you tea instead of coffee. 'You mentioned you were stressed. Tea helps, right?' She remembered from three weeks ago."

TECHNIQUE 3: The Small Gesture
Big emotions through tiny actions.

Example:
"When you said you were proud of her, she didn't say anything. Just squeezed your hand for a moment. That was enough."

TECHNIQUE 4: The Authentic Flaw
Imperfection creates relatability.

Example:
"She laughs at her own jokes before the punchline. It's kind of dorky. But that's part of why you like her."

TECHNIQUE 5: The Growth Moment
Show they're changing because of this relationship.

Example:
"'I wouldn't have tried this a year ago,' she said, looking at the art class schedule. 'But you make me want to be braver.'"

TECHNIQUE 6: The Shared Language
Inside jokes/references that only make sense to them.

Example:
"She texted you: 'Tuesday situation' - your code for 'I need coffee and conversation, no questions asked.' You were there in 20 minutes."

=== YOUR TASK ===

Using these principles, generate content for this interaction that will create emotional resonance.

Context:
{interaction_context}

Current Relationship Level: {level}
Target Emotional Beat: {target_emotion}

Generate:
1. One specific detail that makes this feel real
2. One behavioral moment that shows emotion
3. One line of dialogue (indirect) that reveals character
4. One small gesture that demonstrates care/connection
5. One callback or future setup that creates continuity

Focus on AUTHENTIC over DRAMATIC.
Focus on SMALL over BIG.
Focus on SHOWN over TOLD.

Output as JSON with explanations for why each choice creates emotional resonance.
```

---

## Narrative Coherence Rules

### Maintaining Story Consistency

```markdown
NARRATIVE COHERENCE SYSTEM:

You are generating content that must remain consistent with:
1. Character's established personality
2. Relationship history
3. Previous AI-generated content
4. World/setting logic
5. Emotional realism

=== COHERENCE CHECKS ===

BEFORE generating new content, verify:

CHECK 1: PERSONALITY CONSISTENCY
Current Personality: {ocean_scores}
Previous Behavior Patterns: {behavior_summary}

Question: Would THIS character act THIS way?
- Review their Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
- Check if proposed action/dialogue matches
- If not, adjust to fit personality OR explain why they're acting out of character (stress, growth, special circumstance)

CHECK 2: RELATIONSHIP CONSISTENCY
Current Relationship: Level {level}, Trust {trust}/10
Relationship History: {history_summary}

Question: Is this appropriate for this relationship stage?
- Level 1-2: Keep some distance, formality
- Level 3: Comfortable but not deeply intimate
- Level 4-5: Intimacy and vulnerability appropriate

Avoid:
- Level 2 characters knowing deep secrets
- Level 5 characters acting like strangers
- Jumping intimacy levels without cause

CHECK 3: MEMORY CONSISTENCY
Previous Memories: {memory_list}
Previous Conversations: {conversation_topics}

Question: Does this contradict anything established?
- Don't introduce facts that conflict with previous content
- Reference previous events naturally
- Build on established details rather than replacing them

If you need to retcon something, acknowledge it:
"Actually, I think I mentioned before that... but what I meant was..."

CHECK 4: CHRONOLOGICAL CONSISTENCY
Time Since First Meeting: {weeks}
Recent Events: {recent_events}
Character's Life Stage: {life_stage}

Question: Does the pacing make sense?
- Don't rush relationship development
- Allow appropriate time for trust building
- Major revelations need time to develop
- Crisis responses should be fresh, not distant

CHECK 5: TONAL CONSISTENCY
Previous Interactions Tone: {tone_summary}
Character's Communication Style: {style}

Question: Does this match how they communicate?
- Maintain vocabulary level
- Keep humor style consistent
- Maintain formality level appropriate to relationship
- Don't suddenly shift personality without reason

=== COHERENCE VIOLATION HANDLING ===

If you must violate consistency:

OPTION 1: Don't Violate - Find Alternative
Rework the content to maintain consistency

OPTION 2: Justified Violation
Character is acting out of character for a REASON:
- Under extreme stress
- Drunk/impaired
- Trying to impress someone
- Hiding true feelings
- Growth/change moment

If justified, include internal explanation:
"{Name} wasn't usually this [way], but [reason] made them [act differently]."

OPTION 3: Gentle Retcon
Reframe previous content rather than contradicting:
"When she mentioned her father before, she kept it vague. Now you understand why."

NEVER: Hard contradiction without acknowledgment

=== CONSISTENCY MAINTENANCE PROMPTS ===

For Each Generation:

STEP 1: Review Context
"Before generating, I will review:
- Character personality scores: {scores}
- Relationship level: {level}
- Previous 3 interactions: {interactions}
- Established facts: {facts}"

STEP 2: Check Proposed Content
"My proposed content is: {proposal}
Does this fit? Let me verify:
- Personality match: {yes/no + explanation}
- Relationship appropriate: {yes/no + explanation}
- Consistent with history: {yes/no + explanation}
- Appropriate pacing: {yes/no + explanation}"

STEP 3: Adjust if Needed
"Adjustments made: {adjustments}
Justification for any violations: {justification}"

STEP 4: Generate Final Content
{final_content}

=== INTERNAL COHERENCE CHECK FORMAT ===

Before outputting to game:

{
  "coherence_check": {
    "personality_match": {
      "pass": boolean,
      "notes": "string"
    },
    "relationship_appropriate": {
      "pass": boolean,
      "notes": "string"
    },
    "history_consistent": {
      "pass": boolean,
      "conflicts": ["string"],
      "resolutions": ["string"]
    },
    "pacing_appropriate": {
      "pass": boolean,
      "notes": "string"
    },
    "tone_consistent": {
      "pass": boolean,
      "notes": "string"
    },
    "overall_coherence_score": float (0.0-1.0),
    "confidence": "high/medium/low"
  },
  "generated_content": {
    /* actual content here */
  }
}

Only output content with overall_coherence_score > 0.8
If lower, regenerate with adjustments.
```

---

## Consistency Maintenance

### Cross-Generation Consistency

```markdown
CONSISTENCY MAINTENANCE ACROSS GENERATIONS:

Challenge: Each AI generation is stateless. Need to maintain consistency across multiple evolutions of same character.

Solution: Comprehensive context injection + pattern reinforcement

=== TECHNIQUE 1: ROLLING SUMMARY ===

After each generation, create a summary:

{
  "character_snapshot": {
    "name": "Sarah Anderson",
    "essence": "Quiet, bookish barista with dreams of opening independent bookshop. Warm but introverted. Talks about her late grandmother's influence. Collects vintage books.",
    "communication_style": "Thoughtful pauses before speaking. Uses literary references. Laughs quietly. Gets animated about books.",
    "key_facts": [
      "Works at Café Luna as barista",
      "Grandmother left her $15k for 'something brave'",
      "Collects first editions of children's books",
      "Has detailed business plan for bookshop",
      "Best friend is Marcus (introduced Week 12)",
      "Doesn't talk to her father (mentioned Week 8)"
    ],
    "visual_details": [
      "Blue scarf she always wears (Week 4)",
      "Wears grandmother's locket (Week 8)",
      "Small notebook for bookshop ideas (Week 15)",
      "Vintage-style glasses (Week 20)"
    ],
    "personality_evolution": [
      "Week 1: Shy, guarded → Week 10: Opening up",
      "Week 15: Anxious about dreams → Week 25: Building confidence",
      "Neuroticism: 3.8 → 3.2 (becoming more confident)"
    ]
  }
}

Feed this summary into every new generation.

=== TECHNIQUE 2: STYLE GUIDE PER CHARACTER ===

Create a character-specific style guide:

SARAH ANDERSON - GENERATION STYLE GUIDE

Voice/Speech Patterns:
- Uses literary references naturally
- Pauses thoughtfully before responding to serious questions
- Says "you know?" when sharing something personal
- Laughs quietly, almost apologetically
- Vocabulary: educated but not pretentious

Favorite Topics:
1. Books (especially children's literature)
2. Her grandmother
3. Small business ownership
4. Coffee culture
5. Vintage/nostalgic items

Avoid Topics:
1. Her father (mentions rarely, changes subject)
2. Romantic relationships (single, not looking actively)
3. College (dropped out, sensitive topic)

Physical Mannerisms:
- Tucks hair behind ear when nervous
- Traces book spines with fingers when thinking
- Makes eye contact when passionate about topic, avoids when uncomfortable
- Fidgets with her grandmother's locket when anxious

Dialogue Examples:
✅ "There's something about the smell of old books, you know? It's like... memory made physical."
✅ "My grandmother always said that bravery isn't the absence of fear. It's doing the thing anyway."
✅ "I was thinking—and tell me if this sounds crazy—but what if..."

❌ "OMG that's so exciting!" (too energetic for her)
❌ "Whatever, I don't really care" (too dismissive for high-A personality)
❌ "Let me tell you exactly what I think" (too aggressive for her style)

=== TECHNIQUE 3: GENERATION CHAINING ===

Each new generation references previous generations:

Prompt Section:
"Previous AI Generations for This Character:

Generation 1 (Week 4 - First Deep Conversation):
Created details: Blue scarf, love of Murakami, quiet laugh
Personality shifts: Openness +0.2, Extraversion +0.1
Key memory: Recommended Kafka on the Shore

Generation 2 (Week 8 - Family Discussion):
Created details: Grandmother's influence, estranged father, $15k legacy
Personality shifts: Neuroticism -0.1, Agreeableness +0.1
Key memory: Shared pain about family, vulnerability moment

Generation 3 (Week 15 - Business Discussion):
Created details: Has detailed business plan, wants player's input
Personality shifts: Conscientiousness +0.2
Key memory: Showed business plan, asked for partnership consideration

Your new generation MUST:
1. Reference established details naturally
2. Build on previous personality shifts (don't reverse them)
3. Create new content that ADDS to but doesn't REPLACE previous content
4. Maintain the communication style established in previous generations"

=== TECHNIQUE 4: CONTRADICTION DETECTION ===

Before finalizing generation, run contradiction check:

{
  "contradiction_check": {
    "new_content": "string (what you're proposing)",
    "potential_conflicts": [
      {
        "conflict": "string (describe potential contradiction)",
        "with_generation": "Generation X - Week Y",
        "severity": "minor/moderate/major",
        "resolution": "string (how to resolve)"
      }
    ]
  }
}

Example:
{
  "potential_conflicts": [
    {
      "conflict": "New generation says Sarah loves parties, but Generation 2 established she's introverted (E: 2.5)",
      "with_generation": "Generation 2 - Week 8",
      "severity": "major",
      "resolution": "Change 'loves parties' to 'enjoys small gatherings with close friends' to match introversion"
    }
  ]
}

=== TECHNIQUE 5: CANONICAL FACTS LIST ===

Maintain immutable facts:

SARAH ANDERSON - CANONICAL FACTS (CANNOT CHANGE)

Basic Identity:
- Name: Sarah Anderson
- Age: 27
- Occupation: Barista at Café Luna
- Dream: Open independent bookshop

Family:
- Late grandmother (died 3 years ago) - primary influence
- Father: Estranged (doesn't talk to him)
- Mother: [Not yet established - can create]
- Siblings: [Not yet established - can create]

Core Personality (can shift slightly but not reverse):
- Openness: HIGH (4+)
- Conscientiousness: MEDIUM-HIGH (3.5-4)
- Extraversion: LOW-MEDIUM (2.5-3)
- Agreeableness: HIGH (4+)
- Neuroticism: MEDIUM (3-3.5, trending down)

Physical Appearance:
- Blue scarf (signature item)
- Grandmother's locket
- Vintage-style glasses
- [Height, hair color, etc. not yet established - can create]

Any new generation MUST respect these canonical facts.

If you need to modify a canonical fact, you must:
1. Have a very strong narrative reason
2. Acknowledge the change in-universe
3. Provide explanation for the retcon

Example:
"When Sarah mentioned her mother before, she was vague. You assumed her mother wasn't in the picture. But today she clarified—her mother remarried and moved to Florida. They talk, just not often."
```

---

## Multi-Turn Refinement

### Iterative Quality Improvement

```markdown
MULTI-TURN REFINEMENT PROCESS:

For high-importance evolutions (Level 3→4, Level 4→5, Crisis events, Legendary fusions), use multi-turn refinement:

=== TURN 1: DRAFT GENERATION ===

"Generate a DRAFT evolution for this interaction. Focus on hitting the major beats, but don't worry about perfection. This is a first pass."

Output: Draft content with all required fields

=== TURN 2: SELF-CRITIQUE ===

"Review your draft generation. Identify:
1. What works well
2. What feels generic or cliché
3. What could be more specific
4. What could be more emotionally resonant
5. Any consistency issues"

Output: Critique analysis

=== TURN 3: REFINEMENT ===

"Based on your critique, generate an IMPROVED version that:
- Replaces generic content with specific details
- Enhances emotional resonance
- Fixes consistency issues
- Adds authenticity"

Output: Refined version

=== TURN 4: POLISH ===

"Final polish:
- Check for any remaining clichés
- Ensure all descriptions are vivid but not purple
- Verify personality consistency
- Confirm emotional authenticity
- Check pacing and flow"

Output: Final polished version

=== EXAMPLE MULTI-TURN REFINEMENT ===

Context: Sarah Level 3→4 evolution, first time inviting player to her apartment

TURN 1 DRAFT:
"Sarah invited you to her apartment for the first time. It was cozy and filled with books. You talked for hours and felt closer. This was a big step in your friendship."

TURN 2 CRITIQUE:
- ❌ Too generic ("cozy", "talked for hours")
- ❌ Told not shown ("felt closer")
- ❌ No specific details about the space
- ❌ No dialogue or behavioral moments
- ❌ Doesn't feel earned or significant

TURN 3 REFINEMENT:
"Sarah's apartment was exactly what you'd imagine: a studio with books covering every surface—stacked on tables, lining windowsills, even piled next to her bed. She apologized for the mess, but you loved it. She made tea and you sat on her worn couch, and she showed you her grandmother's book collection, handling each one with this careful reverence. When you asked about a children's book with a torn cover, she said, 'My grandmother read this to me until the binding broke.' That's when you realized—this wasn't just showing you her space. This was showing you her heart."

TURN 4 POLISH:
"Sarah's apartment was exactly what you expected: a tiny studio where books colonized every surface. They lined the windowsills, stacked on the kitchen counter, piled beside her bed. She laughed nervously. 'Sorry about the mess.' But you weren't sorry.

She made tea—earl grey, in chipped mugs that looked vintage—and you sat on her worn couch. Gradually, she started pulling books from shelves, showing you her grandmother's collection. Each one handled with almost ceremonial care. When you noticed a children's book with a broken spine, she held it like something precious. 'My grandmother read this to me so many times the binding gave up.' 

That's when it hit you: this wasn't just showing you her apartment. This was showing you what matters to her. And she trusted you enough to let you see it."

This version has:
✅ Specific details (chipped mugs, broken spine)
✅ Behavioral moments (nervous laugh, ceremonial care)
✅ Sensory details (earl grey tea, worn couch)
✅ Emotional realization (shown through player understanding)
✅ Appropriate pacing for Level 3→4 evolution

=== WHEN TO USE MULTI-TURN ===

Always use for:
- Level 3→4 evolutions
- Level 4→5 evolutions
- Crisis response evolutions
- Legendary fusion completions
- First romantic kiss/confession
- Major life decision moments

Can skip for:
- Level 1→2 basic evolutions
- Routine activity cards
- Minor memory updates
- Background NPC evolutions

Cost-benefit: 4x the API calls, 10x the quality for important moments
```

---

## Complete Prompt Examples

### Example 1: Full Evolution Prompt (In Production)

```markdown
SYSTEM: You are Unwritten's narrative AI engine. Generate emotionally authentic character evolution.

CONTEXT:

Character: Marcus Rivera
Current State: Level 3 (Friend)
First Met: 18 weeks ago
Total Interactions: 23
Relationship Quality: 7.2/10
Trust: 7.5/10

Personality (OCEAN):
- Openness: 3.8/5 (Creative, enjoys new experiences)
- Conscientiousness: 4.2/5 (Reliable, organized)
- Extraversion: 3.5/5 (Social but not overwhelming)
- Agreeableness: 4.5/5 (Warm, supportive, puts others first)
- Neuroticism: 3.8/5 (Worries about health, somewhat anxious)

Current Description:
"Marcus is a graphic designer at a small agency. He's the friend who remembers birthdays and checks in when you're quiet. There's a carefulness to him, like he's always aware of other people's feelings. He talks about his work with genuine passion—designing makes him light up. You've noticed he gets quiet when the topic turns to health or family, changing the subject smoothly. He's been a steady presence in your life, the kind of friend who just shows up when you need him."

Physical Details Established:
- Wears vintage band t-shirts (Week 4)
- Has a small tattoo of a compass on his forearm (Week 8)
- Always has his sketchbook (Week 3)
- Drinks black coffee, no sugar (Week 2)

Key Memories:
1. Week 4: "Met at the gym. He was terrible at bench pressing but laughed about it. We spotted each other and grabbed coffee after. Easy conversation."
2. Week 8: "Helped him move. He ordered pizza and made it actually fun. Noticed he got weird when I picked up a prescription bottle—just for a second—then was normal again."
3. Week 12: "Art show invitation. His design work was incredible. Afterward he admitted he almost didn't invite me because he was nervous about showing his work. I told him it was amazing. He seemed genuinely touched."
4. Week 15: "Called me when he was having a bad day. Didn't say why, just asked if I wanted to get food. We ate tacos and barely talked, but it felt comfortable."

Personality Evolution So Far:
- Openness: 3.6 → 3.8 (sharing more of his creative work)
- Neuroticism: 4.0 → 3.8 (less anxious with player specifically)

CURRENT INTERACTION:

Type: Unexpected Crisis
Location: Hospital (Emergency)
Time: 3:14 AM, Tuesday
Context: Marcus called you from the hospital. He was vague on the phone, but his voice was shaking. You got there in 20 minutes.

When You Arrived:
- Marcus was in the ER waiting room, alone
- He looked pale, scared
- Initial bloodwork being run
- Potential diagnosis: Testicular cancer scare
- Waiting for ultrasound results

Player's Actions:
- Arrived quickly despite late hour
- Stayed with him during intake
- Held his hand during scary moments (he gripped back hard)
- Made jokes to cut tension when appropriate
- Serious support when he needed it
- Offered to call his family (he said no)
- Stayed until 7 AM when results came back (benign, but needs monitoring)

Marcus's Behavior:
- Started with forced humor, cracked quickly
- Admitted he's been scared for weeks
- Cried once, apologized immediately
- Said "I'm sorry for calling you" three times
- Kept saying "I didn't know who else to call"
- When results came back benign, he laughed and cried at same time
- Hugged you for a long time

TASK:

Generate a CRISIS EVOLUTION from Level 3 (Friend) to Level 4 (Close Friend) or potentially Level 5 (Best Friend/Chosen Family).

This is a defining moment. Generate:

1. CRISIS MEMORY (6-8 sentences)
   - Capture the fear, vulnerability, and ultimate relief
   - Include specific moment when he broke down
   - Show player's response
   - Include the hug at the end
   - Make it visceral and emotionally real

2. PERSONALITY IMPACT
   - Immediate: How crisis affected his OCEAN scores
   - Long-term: How player's support will change him
   - Trauma processing vs resilience factors

3. RELATIONSHIP TRANSFORMATION
   - This probably elevates to Level 4 minimum
   - Possibly Level 5 if you feel the crisis and support warrant it
   - Quantify the trust leap
   - Explain what's different now

4. WHAT THIS REVEALED ABOUT MARCUS
   - His fear of illness/death
   - Why he called you specifically
   - His family situation (why didn't he call them?)
   - His coping mechanisms

5. GRATITUDE AND AFTERMATH
   - How will he express thanks (immediately and over time)?
   - What does this create for future interactions?
   - Potential for codependency vs healthy support?

6. NEW DESCRIPTION (7-8 sentences)
   - Must reflect this crisis and its resolution
   - Show how relationship has deepened
   - Acknowledge his vulnerability and player's support

7. PORTRAIT UPDATE
   - How does he look different after this?
   - Exhaustion, relief, gratitude?

CRITICAL REQUIREMENTS:
- This is his first major vulnerability with player
- He has health anxiety (explaining his Neuroticism score)
- He's usually the SUPPORTER, not the supported (role reversal is significant)
- The benign results are important (not everything has to be worst-case)
- But the fear was real, and he'll remember it
- Player showed up at 3 AM and stayed 4 hours—that means something

AVOID:
- Making this melodramatic
- Having him instantly trauma dump his whole backstory
- Romantic undertones (unless that's been established—it hasn't)
- Making him weak/pathetic—he's scared but still Marcus
- Unrealistic instant recovery—he'll be processing this

REALISM NOTES:
- People in hospitals are terrified but try to hide it
- Medical scares change how you see mortality
- The waiting is the worst part
- Relief creates weird emotional releases
- Gratitude is hard to express when you feel vulnerable
- He'll be embarrassed about crying, even though he shouldn't be

Generate the complete crisis evolution in JSON format.

Use your full capability for emotional authenticity. This is a DEFINING MOMENT in their friendship.
```

**Expected AI Output Structure:**

```json
{
  "crisis_memory": {
    "description": "3:47 AM. Marcus's hands wouldn't stop shaking...",
    "peak_moment": "When the doctor said 'we need to run more tests' and you felt him grip your hand like he was drowning...",
    "player_impact": "You stayed. Four hours in those awful plastic chairs...",
    "emotional_weight": 0.95
  },
  "personality_impact": {
    "immediate_shifts": {
      "openness": -0.2,
      "neuroticism": +0.5,
      "agreeableness": +0.3
    },
    "temporary_vs_permanent": "Neuroticism spike is temporary (crisis response), but Agreeableness increase is permanent (learned he can accept help)...",
    "recovery_trajectory": "Will need 2-3 weeks to process..."
  },
  "relationship_transformation": {
    "new_level": 5,
    "level_skip_justification": "Crisis + 3 AM response + 4 hour presence + physical comfort + seeing him at absolute most vulnerable = quantum leap...",
    "trust_leap": 3.5,
    "new_status": "Best Friend / Chosen Family",
    "what_changed": "He let you see him terrified. You stayed anyway..."
  },
  "character_revelation": {
    "health_anxiety_explained": "Now you understand the prescription bottle reaction, the way he gets quiet about health topics...",
    "why_player": "He called you because his family would panic and make it worse. He needed someone who could be strong while he fell apart...",
    "coping_mechanism": "Humor as shield until he can't hold it anymore..."
  },
  "gratitude_expression": {
    "immediate": "The hug. He held on like you were the only solid thing in the world...",
    "delayed": "He'll show up for you in ways he never did before...",
    "non_verbal": "Already making plans to get lunch 'when you have time' (wants to normalize, not dwell)..."
  },
  "updated_description": "Marcus Rivera is your best friend. That title was earned at 3 AM in a hospital waiting room, when he called you terrified...",
  "portrait_update": "Exhausted but relieved expression. Eyes slightly red. But there's something softer in his face now—like a weight he'd been carrying alone is now shared."
}
```

---

### Example 2: Romantic Evolution Prompt

```markdown
[Include full context similar to above, but for romantic progression]

ADDITIONAL ROMANTIC GUIDELINES:

Attraction Development:
- Physical attraction vs emotional connection (both matter)
- Compatibility beyond friendship
- Sexual tension (tasteful, age-appropriate)
- Timing and readiness

Romantic Beats:
- Level 2→3: Realizing attraction exists
- Level 3→4: First date, testing romantic compatibility
- Level 4→5: Becoming official, exclusivity
- Level 5+: Deep partnership, potential marriage

AVOID:
- Instalove (must be earned)
- Love triangles without player choice
- Toxic romance dynamics
- Possessiveness framed as romantic
- Pressure or coercion

[Rest of prompt structure similar to friendship evolution]
```

---

## Quality Control & Validation

### Post-Generation Quality Checks

```markdown
QUALITY VALIDATION SYSTEM:

After AI generates content, run these automated checks:

CHECK 1: LENGTH VALIDATION
- Memory description: 100-400 characters
- Updated description: 200-600 characters
- Each unlocked conversation: 20-80 characters

IF OUT OF RANGE: Flag for review/regeneration

CHECK 2: PERSONALITY SHIFT VALIDATION
- No single trait shifts more than 0.5 in one evolution
- Total absolute shift per evolution < 1.0
- Shifts must have justification text

IF VIOLATED: Reject and regenerate with stricter bounds

CHECK 3: COHERENCE VALIDATION
- Run similarity check against previous descriptions
- Ensure overlap of 40-60% (some continuity, some new)
- Check for contradictions with established facts

IF CONTRADICTION DETECTED: Flag specific conflicts, require resolution

CHECK 4: CLICHÉ DETECTION
Scan for these phrases and flag:
- "mysterious past"
- "hidden depths"
- "more than meets the eye"
- "broken but beautiful"
- "troubled soul"
- "instant connection"
- "electric chemistry"
- "changed everything"

IF DETECTED: Regenerate with specific anti-cliché instruction

CHECK 5: EMOTIONAL AUTHENTICITY SCORE
Use sentiment analysis to rate:
- Specificity (specific details vs vague statements)
- Behavioral grounding (shown through action vs told)
- Dialogue quality (indirect realistic vs stilted direct quotes)

SCORE FORMULA:
authenticity_score = (
  specificity * 0.4 +
  behavioral_grounding * 0.4 +
  dialogue_quality * 0.2
)

IF SCORE < 0.7: Flag for review or regeneration

CHECK 6: CONSISTENCY SCORE
Compare to previous generations:
- Personality trait consistency: 0-1
- Communication style consistency: 0-1
- Factual consistency: 0-1

consistency_score = average(above three)

IF SCORE < 0.8: Flag inconsistencies, require revision

CHECK 7: PLAYER IMPACT VALIDATION
Every evolution MUST:
- Reference player's specific action/choice
- Show how player influenced outcome
- Create future interaction possibilities

IF MISSING: Regenerate with emphasis on player agency

FINAL VALIDATION:
```javascript
function validateGeneration(generated, context) {
  const checks = {
    length: validateLengths(generated),
    personality: validatePersonalityShifts(generated, context),
    coherence: validateCoherence(generated, context),
    cliches: detectCliches(generated),
    authenticity: scoreAuthenticity(generated),
    consistency: scoreConsistency(generated, context),
    playerImpact: validatePlayerImpact(generated, context)
  };
  
  const scores = {
    length: checks.length.pass ? 1 : 0,
    personality: checks.personality.score,
    coherence: checks.coherence.score,
    cliches: checks.cliches.score,
    authenticity: checks.authenticity.score,
    consistency: checks.consistency.score,
    playerImpact: checks.playerImpact.pass ? 1 : 0
  };
  
  const overallQuality = (
    scores.length * 0.1 +
    scores.personality * 0.15 +
    scores.coherence * 0.2 +
    scores.cliches * 0.1 +
    scores.authenticity * 0.25 +
    scores.consistency * 0.15 +
    scores.playerImpact * 0.05
  );
  
  return {
    pass: overallQuality > 0.75,
    score: overallQuality,
    details: checks,
    recommendation: overallQuality > 0.85 ? 'approve' :
                   overallQuality > 0.75 ? 'approve_with_notes' :
                   overallQuality > 0.65 ? 'revise' :
                   'regenerate'
  };
}
```

QUALITY TIERS:
- 0.90+: Exceptional - use as training example
- 0.85-0.89: Excellent - approve immediately
- 0.75-0.84: Good - approve with minor notes
- 0.65-0.74: Acceptable - revise specific issues
- <0.65: Poor - regenerate entirely
```

---

## Cost Optimization Strategies

### Managing API Costs

```markdown
COST OPTIMIZATION FOR AI GENERATIONS:

Challenge: Every evolution requires AI call. With 50+ NPCs and hundreds of interactions, costs add up.

STRATEGY 1: TIERED GENERATION QUALITY

HIGH QUALITY (GPT-4/Claude Sonnet):
- Level 3→4 evolutions
- Level 4→5 evolutions
- Crisis events
- Legendary fusions
- First 3 interactions with any NPC

MEDIUM QUALITY (GPT-3.5/Claude Haiku):
- Level 1→2 evolutions
- Level 2→3 evolutions
- Routine interactions
- Background NPC updates

LOW QUALITY (Cached/Template):
- Repeated routine activities
- Generic level 1 encounters
- Background atmosphere NPCs

COST BREAKDOWN:
- High: $0.03 per generation (detailed prompts, long context)
- Medium: $0.005 per generation (simplified prompts)
- Low: $0.0001 per generation (template-based)

For 10,000 NPC interactions in playthrough:
- All high quality: $300
- Tiered approach: $75
- Savings: 75%

STRATEGY 2: SMART CACHING

Cache common generation patterns:

```javascript
const generationCache = {
  'coffee_meetup_level1_friendly': {
    template: generatedTemplate,
    variableFields: ['sensoryDetail', 'specificTopic', 'personalityTweak'],
    cost: 0
  }
};

function getOrGenerateEvolution(context) {
  const cacheKey = generateCacheKey(context);
  
  if (cache.has(cacheKey)) {
    // Use cached template, just regenerate variable fields
    return fillTemplate(cache.get(cacheKey), context);
    // Cost: $0.001 (just variable generation)
  } else {
    // Full generation needed
    const result = await fullGeneration(context);
    // Cost: $0.03
    
    // Cache for future use
    if (isCommonScenario(context)) {
      cache.set(cacheKey, extractTemplate(result));
    }
    
    return result;
  }
}
```

STRATEGY 3: BATCH PROCESSING

For non-urgent evolutions, batch:

```javascript
const evolutionQueue = [];

function queueEvolution(context) {
  evolutionQueue.push(context);
  
  if (evolutionQueue.length >= 10) {
    processBatch(evolutionQueue);
    evolutionQueue = [];
  }
}

async function processBatch(contexts) {
  // Single API call with multiple evolution requests
  // API call overhead reduced
  const results = await batchGenerate(contexts);
  return results;
}
```

Cost savings:
- Individual calls: 10 × $0.03 = $0.30
- Batch call: 1 × $0.20 = $0.20
- Savings: 33%

STRATEGY 4: PROGRESSIVE ENHANCEMENT

Start with template, enhance if player engages:

```javascript
async function generateEvolution(context) {
  // Phase 1: Quick template (instant, cheap)
  const quickVersion = generateFromTemplate(context);
  displayToPlayer(quickVersion);
  
  // Phase 2: Check if player lingers or re-reads
  if (playerIsEngaged()) {
    // Enhance with full AI generation
    const enhancedVersion = await fullAIGeneration(context);
    updateDisplay(enhancedVersion);
  }
}
```

Most players skim, only engaged players get full AI.
Savings: 60-70% of generations never need full AI.

STRATEGY 5: LOCAL FALLBACK

Train lightweight local model on common patterns:

```javascript
async function generateEvolution(context) {
  if (isCommonScenario(context) && !isImportantMoment(context)) {
    // Use local model (free, fast)
    return await localModel.generate(context);
  } else {
    // Use premium API (accurate, expensive)
    return await premiumAPI.generate(context);
  }
}
```

Local model handles:
- 70% of generations (routine interactions)
- Cost: Free (after training)

Premium API handles:
- 30% of generations (important moments)
- Cost: $0.03 each

Overall cost reduction: 70%

COMBINED STRATEGY:

```javascript
async function smartGenerate(context) {
  const importance = assessImportance(context);
  
  if (importance < 0.3) {
    // Template-based
    return generateFromTemplate(context);
  } else if (importance < 0.6) {
    // Check cache first
    const cached = checkCache(context);
    if (cached) return fillCachedTemplate(cached, context);
    
    // Use local model
    return await localModel.generate(context);
  } else if (importance < 0.8) {
    // Medium quality API
    return await mediumQualityAPI.generate(context);
  } else {
    // High quality API for important moments
    return await highQualityAPI.generate(context);
  }
}
```

Expected cost per playthrough:
- 10,000 total NPC interactions
- 7,000 template/cached (free)
- 2,000 local model (free after training)
- 800 medium API ($4)
- 200 high API ($6)
- Total: $10 per playthrough

Compare to all high-quality: $300
Savings: 97%

STRATEGY 6: PLAYER-FUNDED PREMIUM

Optional premium AI generations:

"Enhance this memory with AI" button
- Free version: Template-based, quick
- Premium ($0.99): Full AI generation with art

Players pay for moments THEY care about.
Converts cost center into revenue stream.
```

---

## Edge Case Handling

### Unusual Scenarios and Failures

```markdown
EDGE CASE HANDLING SYSTEM:

=== EDGE CASE 1: AI GENERATES INAPPROPRIATE CONTENT ===

Problem: AI occasionally generates romantic/sexual content when inappropriate, or dark content for younger audiences.

Solution: Content filter + regeneration

```javascript
function validateContent(generated, context) {
  // Check for inappropriate content
  const filters = {
    romantic: checkUnwantedRomance(generated, context),
    sexual: checkSexualContent(generated),
    violent: checkExcessiveViolence(generated),
    dark: checkDarkThemes(generated, context.characterAge)
  };
  
  if (filters.romantic && !context.romanticPath) {
    return {
      valid: false,
      reason: 'Unwanted romantic content',
      action: 'regenerate_with_platonic_constraint'
    };
  }
  
  if (filters.sexual) {
    return {
      valid: false,
      reason: 'Sexual content detected',
      action: 'regenerate_with_family_friendly_constraint'
    };
  }
  
  // Additional checks...
  
  return { valid: true };
}
```

Regeneration prompt addition:
"CRITICAL: This is a platonic friendship. Do not include any romantic or sexual undertones. Keep all content appropriate for ages 16+."

=== EDGE CASE 2: AI CONTRADICTS ITSELF WITHIN SAME GENERATION ===

Problem: Generated memory says one thing, updated description says another.

Solution: Internal consistency check

```javascript
function checkInternalConsistency(generated) {
  const memory = generated.crisis_memory.description;
  const description = generated.updated_description;
  
  // Extract key facts from each
  const memoryFacts = extractFacts(memory);
  const descriptionFacts = extractFacts(description);
  
  // Check for contradictions
  const contradictions = findContradictions(memoryFacts, descriptionFacts);
  
  if (contradictions.length > 0) {
    return {
      valid: false,
      contradictions: contradictions,
      action: 'regenerate_description_consistent_with_memory'
    };
  }
  
  return { valid: true };
}
```

=== EDGE CASE 3: AI MAKES CHARACTER TOO PERFECT ===

Problem: AI tends toward Mary Sue characters—too talented, too understanding, no real flaws.

Solution: Flaw injection + realism prompting

Add to prompt:
"REALISM REQUIREMENT: This character must have realistic flaws and limitations. No one is perfect. Include:
- At least one social awkwardness or quirk
- At least one area where they're NOT talented
- At least one relatable insecurity
- Realistic response to stress (not always composed)"

Post-generation check:
```javascript
function checkForMarySue(generated) {
  const redFlags = {
    allPositiveTraits: checkAllTraitsPositive(generated.personality),
    noFlaws: !hasRealisticFlaws(generated.updated_description),
    unrealisticComposure: checkAlwaysComposed(generated.crisis_memory),
    perfectDialogue: checkTooEloquent(generated)
  };
  
  const marySueScore = calculateMarySueScore(redFlags);
  
  if (marySueScore > 0.7) {
    return {
      valid: false,
      reason: 'Character too perfect/unrealistic',
      action: 'inject_humanizing_flaws'
    };
  }
  
  return { valid: true };
}
```

=== EDGE CASE 4: AI GENERATES TRAUMA DUMP ===

Problem: AI reveals too much too fast, especially trauma/dark past.

Solution: Pacing enforcement

```javascript
function checkEmotionalPacing(generated, context) {
  const relationshipLevel = context.character.level;
  const traumaWeight = assessTraumContent(generated);
  
  const appropriatePacing = {
    1: 0.0,  // Level 1: No trauma reveals
    2: 0.2,  // Level 2: Hints only
    3: 0.5,  // Level 3: Can mention but not deep
    4: 0.8,  // Level 4: Can share details
    5: 1.0   // Level 5: Full vulnerability okay
  };
  
  if (traumaWeight > appropriatePacing[relationshipLevel]) {
    return {
      valid: false,
      reason: 'Trauma revealed too early in relationship',
      action: 'regenerate_with_pacing_constraint',
      suggestion: 'Keep this revelation but save for later evolution'
    };
  }
  
  return { valid: true };
}
```

=== EDGE CASE 5: AI FORGETS CONTEXT ===

Problem: Despite context injection, AI occasionally forgets key details.

Solution: Critical fact highlighting + verification

```javascript
function highlightCriticalFacts(context) {
  const critical = [
    context.character.name,
    context.character.occupation,
    context.relationshipLevel,
    ...context.canonicalFacts
  ];
  
  return `
CRITICAL FACTS (MUST REMEMBER):
${critical.map(fact => `- ${fact}`).join('\n')}

If you use any of these facts, they MUST match exactly.
If you need to change a critical fact, you MUST have a strong narrative reason.
  `;
}

function verifyFactAccuracy(generated, context) {
  const errors = [];
  
  // Check name consistency
  if (generated.includes(context.character.name) === false) {
    errors.push('Character name not used or used incorrectly');
  }
  
  // Check occupation consistency
  if (contradicts(generated.occupation, context.character.occupation)) {
    errors.push('Occupation contradiction detected');
  }
  
  // Additional checks...
  
  return errors.length === 0 ? { valid: true } : {
    valid: false,
    errors: errors,
    action: 'regenerate_with_highlighted_critical_facts'
  };
}
```

=== EDGE CASE 6: API FAILURE / TIMEOUT ===

Problem: API call fails or times out.

Solution: Graceful fallback + retry

```javascript
async function resilientGeneration(context) {
  const maxRetries = 3;
  let attempt = 0;
  
  while (attempt < maxRetries) {
    try {
      const result = await callAI(context);
      return { success: true, result };
    } catch (error) {
      attempt++;
      
      if (attempt < maxRetries) {
        // Exponential backoff
        await sleep(Math.pow(2, attempt) * 1000);
        continue;
      } else {
        // All retries failed, use fallback
        return {
          success: false,
          fallback: generateFallbackContent(context)
        };
      }
    }
  }
}

function generateFallbackContent(context) {
  // Use template-based generation
  const template = selectAppropriateTemplate(context);
  return fillTemplate(template, context);
}
```

=== EDGE CASE 7: PLAYER EXPLOIT ATTEMPTS ===

Problem: Player tries to game the system (repeatedly choosing same option to max stats, etc.).

Solution: Diminishing returns + AI awareness

Add to prompt:
"PLAYER BEHAVIOR ANALYSIS:
Player has chosen this same interaction type {count} times in past {days} days.

If this is excessive repetition:
- Apply diminishing returns to relationship gain
- Have NPC comment on the repetition naturally
- Suggest variety ('We should try something different sometime')
- Reduce personality shift magnitude (already explored this)"

```javascript
function detectExploitation(player, context) {
  const recentInteractions = player.history.slice(-20);
  const sameActivity = recentInteractions.filter(i => 
    i.activity === context.activity &&
    i.character === context.character
  );
  
  if (sameActivity.length > 10) {
    return {
      exploiting: true,
      type: 'activity_spam',
      action: 'apply_diminishing_returns_and_npc_comment'
    };
  }
  
  return { exploiting: false };
}
```

NPC response to exploitation:
"Hey, don't get me wrong, I love coffee with you, but maybe we should try something different? I'm starting to feel like that's all we do."

=== EDGE CASE 8: CULTURAL INSENSITIVITY ===

Problem: AI generates content that's culturally insensitive or stereotypical.

Solution: Cultural awareness check + diverse training examples

```javascript
function checkCulturalSensitivity(generated, context) {
  const concerns = {
    stereotypes: detectStereotypes(generated, context.character.ethnicity),
    appropriation: detectAppropriation(generated),
    insensitivity: detectInsensitiveContent(generated)
  };
  
  if (Object.values(concerns).some(c => c.detected)) {
    return {
      valid: false,
      concerns: concerns,
      action: 'regenerate_with_cultural_sensitivity_emphasis'
    };
  }
  
  return { valid: true };
}
```

Add to prompt for diverse characters:
"CULTURAL SENSITIVITY: This character is [ethnicity/culture]. Ensure:
- No stereotypes or clichés about their culture
- Cultural details are respectful and researched
- They are a full person, not defined solely by ethnicity
- Avoid 'token' representation or fetishization
- When incorporating cultural elements, do so authentically"

=== COMPREHENSIVE EDGE CASE HANDLING PIPELINE ===

```javascript
async function robustGeneration(context) {
  let attempts = 0;
  const maxAttempts = 5;
  
  while (attempts < maxAttempts) {
    attempts++;
    
    try {
      // Generate
      const generated = await callAI(buildPrompt(context));
      
      // Run all validation checks
      const validations = {
        content: validateContent(generated, context),
        consistency: checkInternalConsistency(generated),
        realism: checkForMarySue(generated),
        pacing: checkEmotionalPacing(generated, context),
        facts: verifyFactAccuracy(generated, context),
        culture: checkCulturalSensitivity(generated, context)
      };
      
      // If all pass, return
      if (Object.values(validations).every(v => v.valid)) {
        return { success: true, generated };
      }
      
      // If any fail, adjust prompt and retry
      const failures = Object.entries(validations)
        .filter(([_, v]) => !v.valid);
      
      // Add constraints for failed checks
      context.additionalConstraints = failures.map(([check, result]) => 
        result.action
      );
      
      if (attempts < maxAttempts) {
        continue;
      } else {
        // Max attempts reached, use best available or fallback
        return {
          success: false,
          generated: selectBestAttempt() || generateFallback(context),
          warnings: failures
        };
      }
      
    } catch (error) {
      if (attempts < maxAttempts) {
        await sleep(1000 * attempts);
        continue;
      } else {
        return {
          success: false,
          generated: generateFallback(context),
          error: error
        };
      }
    }
  }
}
```

---

This comprehensive edge case system ensures:
- Content appropriateness
- Internal consistency
- Realistic characterization
- Appropriate pacing
- Fact accuracy
- Cultural sensitivity
- System resilience
- Anti-exploitation

Every failure mode has a graceful recovery path.
```

---

## Conclusion

This prompt engineering system creates:

1. **Consistent character personalities** through OCEAN modeling
2. **Emotionally resonant memories** through specific detail and behavioral grounding
3. **Coherent narrative progression** through context injection and consistency checking
4. **Cost-effective generation** through tiered quality and caching
5. **Robust error handling** through comprehensive validation
6. **Scalable architecture** that can generate thousands of unique evolutions

The key insight: **Constraints drive creativity**. By giving the AI specific boundaries, personality models, and quality requirements, we get better output than with vague "make it good" prompts.

Each prompt template is production-ready and can be adapted for specific game scenarios.

---

**Next Documents:**
3. Technical Architecture for Card Evolution System
4. Specific Scenarios and Fusion Card Outcomes
5. Achievement/Unlock Progression System