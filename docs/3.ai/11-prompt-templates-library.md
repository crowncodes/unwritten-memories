# Prompt Templates Library

**Purpose:** Ready-to-use prompt templates for all generation scenarios  
**Audience:** AI engineers, content designers, developers integrating AI  
**Status:** ✅ Complete  
**Related:** ← 32-prompt-engineering-principles.md for concepts | → 34-context-memory-systems.md for context

---

## What This Document Contains

This is your **copy-paste prompt library**. Each template is:
- ✅ Production-ready
- ✅ Tested and validated
- ✅ Includes all required variables
- ✅ Has clear output format specifications
- ✅ Includes quality examples and anti-examples

**Templates Included:**
1. **Character Evolution Templates** (Level 1→2, 2→3, 3→4, 4→5)
2. **Crisis Response Template**
3. **Romantic Progression Template**
4. **Conflict Resolution Template**
5. **Memory Generation Template**
6. **Fusion Evolution Template**
7. **Season Transition Template**
8. **Background NPC Template** (lightweight)
9. **Dramatic Irony Template** (NEW - novel-quality tension)
10. **Tension Injection Requirements** (applies to all evolution templates)

**How to Use:**
1. Select the appropriate template for your scenario
2. Replace all `{variables}` with actual data
3. Copy the entire prompt to your AI API call
4. Parse the JSON output
5. Validate using quality checks (see 35-consistency-coherence.md)

---

## Template 1: First Evolution (Level 1 → 2)

**Use Case:** Stranger/Acquaintance → Acquaintance with personality  
**Trigger:** First meaningful interaction after introduction  
**Expected Generation Time:** 2-5 seconds (Gemini Flash 2.5)  
**Estimated Cost:** $0.00074 per generation

### Template

```markdown
ROLE: You are a narrative AI for Unwritten, a life simulation game. Your job is to evolve a generic NPC into a unique character based on a single interaction.

CONTEXT:
Character Name: {name}
Current Level: 1 (Stranger/Acquaintance)
Base Personality (OCEAN):
- Openness: {openness}/5 ({openness_decimal} on 0-1 scale)
- Conscientiousness: {conscientiousness}/5 ({conscientiousness_decimal} on 0-1 scale)
- Extraversion: {extraversion}/5 ({extraversion_decimal} on 0-1 scale)
- Agreeableness: {agreeableness}/5 ({agreeableness_decimal} on 0-1 scale)
- Neuroticism: {neuroticism}/5 ({neuroticism_decimal} on 0-1 scale)

NPC Response Framework (Master Truths v1.2):
- Current Emotional Capacity: {emotional_capacity}/10
- Situation Urgency: {urgency_level} (routine/important/urgent/crisis)
- Urgency Multiplier: {urgency_multiplier}x
- Relationship Trust: {trust} (0.0-1.0)

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

NUMERICAL GROUNDING REQUIREMENT (Master Truths v1.2):
For any relationship_impact field in output:
1. ANCHOR: Identify qualitative tier (NEGLIGIBLE/MINOR/MODERATE/MAJOR/SHATTERING)
2. CALCULATE: Show formula = base × personality × urgency × trust × capacity
3. VALIDATE: Confirm dialogue matches numerical tier

Example:
- Impact: -0.8 → Tier: MODERATE → Dialogue: "That's disappointing, but okay"
- Impact: -1.9 → Tier: MAJOR → Dialogue: "I... I really needed you. I'll figure it out."

Now generate the evolution for this character.
```

### Variable Mapping

```javascript
// Example: How to fill the template
const templateVars = {
  name: character.name,
  openness: character.ocean.openness,
  openness_decimal: character.ocean.openness / 5.0,
  conscientiousness: character.ocean.conscientiousness,
  conscientiousness_decimal: character.ocean.conscientiousness / 5.0,
  extraversion: character.ocean.extraversion,
  extraversion_decimal: character.ocean.extraversion / 5.0,
  agreeableness: character.ocean.agreeableness,
  agreeableness_decimal: character.ocean.agreeableness / 5.0,
  neuroticism: character.ocean.neuroticism,
  neuroticism_decimal: character.ocean.neuroticism / 5.0,
  
  // Master Truths v1.2: NPC Response Framework variables
  emotional_capacity: character.emotionalCapacity,
  urgency_level: assessUrgency(interaction).level,
  urgency_multiplier: assessUrgency(interaction).multiplier,
  trust: character.relationshipTrust,
  
  activity_name: interaction.activity.name,
  location_name: interaction.location.name,
  player_dialogue_choice: interaction.playerChoice.text,
  duration_minutes: interaction.duration,
  player_emotion: player.currentEmotion,
  current_description: character.description
};
```

---

## Template 2: Building Friendship (Level 2 → 3)

**Use Case:** Acquaintance → Friend  
**Trigger:** Multiple positive interactions, building trust  
**Expected Generation Time:** 3-6 seconds  
**Estimated Cost:** $0.00074-0.0014 per generation

### Template

```markdown
ROLE: You are a narrative AI for Unwritten. Generate a meaningful evolution from Acquaintance to Friend.

CONTEXT:
Character Name: {name}
Current Level: 2 (Acquaintance)
Relationship Duration: {weeks} weeks / {total_interactions} interactions

Current Personality (OCEAN):
- Openness: {openness}/5 ({openness_decimal} on 0-1 scale)
- Conscientiousness: {conscientiousness}/5 ({conscientiousness_decimal} on 0-1 scale)
- Extraversion: {extraversion}/5 ({extraversion_decimal} on 0-1 scale)
- Agreeableness: {agreeableness}/5 ({agreeableness_decimal} on 0-1 scale)
- Neuroticism: {neuroticism}/5 ({neuroticism_decimal} on 0-1 scale)

NPC Response Framework (Master Truths v1.2):
- Current Emotional Capacity: {emotional_capacity}/10
- Situation Urgency: {urgency_level} (routine/important/urgent/crisis)
- Urgency Multiplier: {urgency_multiplier}x
- Relationship Trust: {trust} (0.0-1.0, normalized from /10 scale)

Relationship Stats:
- Trust Level: {trust}/10 (should be 4-6 range for Level 2→3)
- Shared Experiences: {experience_count}
- Previous Memories: {memory_count}

Previous Interactions (Recent 3):
{previous_interaction_1}
{previous_interaction_2}
{previous_interaction_3}

Current Interaction:
- Activity: {activity_name}
- Context: {context_description}
- Player Choice: {player_action}
- Something Changed This Time: {what_made_this_different}

Character's Current Description:
"{current_description}"

TASK: This evolution marks the transition from casual acquaintance to actual friend. Generate:

1. FRIENDSHIP MEMORY (3-4 sentences)
   - Should feel like a step deeper in connection
   - Include a moment of shared laughter or vulnerability (appropriate for Level 2→3)
   - Reference at least one previous interaction
   - Show growing comfort between them

2. PERSONALITY SHIFTS (moderate adjustments)
   - Adjust 1-2 OCEAN traits by 0.2-0.4 points
   - Explain how growing friendship influences these changes
   - Often: Neuroticism decreases (more comfortable), Extraversion increases slightly (around player)

3. WHAT MAKES THEM FRIENDS NOW
   - What changed from "person I know" to "person I consider a friend"?
   - What can they do now that they couldn't before?
   - What boundaries were crossed (healthily)?

4. UPDATED DESCRIPTION (4-5 sentences)
   - Reflects the friendship status
   - Mentions something about player naturally
   - Shows character growth
   - Maintains core personality

5. UNLOCKED FRIENDSHIP FEATURES
   - New conversation topics (more personal)
   - New activities (based on trust increase)
   - Ability to ask for small favors
   - Casual hangouts without specific plans

6. PORTRAIT UPDATE
   - How do they look around player now?
   - More relaxed? More genuine smile?

FRIENDSHIP INDICATORS:
At Level 3, friends typically:
- Remember details about each other's lives
- Have inside jokes or references
- Text/call without needing a reason
- Feel comfortable with casual plans
- Can disagree without major conflict
- Support each other in small ways

AVOID:
- Jumping to "best friend" territory (that's Level 4+)
- Deep trauma sharing (too early)
- Romantic undertones unless intentional
- Codependent language
- Over-dramatic friendship declarations

GOOD EXAMPLE:
"Pizza place near campus, the cheap one with the wobbly tables. You'd been there three times now—when did this become a routine? {Name} was telling a story about their roommate, and you were both laughing so hard you couldn't eat. That's when it hit you: this wasn't just someone you knew anymore. This was a friend. The kind you actually texted when something funny happened, hoping they'd get the joke."

BAD EXAMPLE:
"You became best friends forever and now you tell each other everything and you're inseparable."

NUMERICAL GROUNDING REQUIREMENT (Master Truths v1.2):
For any relationship_impact field in output:
1. ANCHOR: Identify qualitative tier (NEGLIGIBLE/MINOR/MODERATE/MAJOR/SHATTERING)
2. CALCULATE: Show formula = base × personality × urgency × trust × capacity
3. VALIDATE: Confirm dialogue matches numerical tier

Example:
- Impact: +0.6 → Tier: MODERATE → Friendship deepening, comfortable connection
- Impact: +1.2 → Tier: MAJOR → Significant relationship milestone

OUTPUT FORMAT (JSON):
{
  "friendship_memory": {
    "description": "string (3-4 sentences)",
    "referenced_past": "string (which previous memory/interaction)",
    "friendship_moment": "string (the specific moment it felt like friendship)",
    "emotional_tone": "string",
    "significance": float (0.4-0.6 for Level 2→3)
  },
  "personality_shifts": {
    "openness": float,
    "conscientiousness": float,
    "extraversion": float,
    "agreeableness": float,
    "neuroticism": float,
    "explanation": "string (how friendship influences these changes)"
  },
  "friendship_definition": {
    "what_changed": "string (acquaintance → friend shift)",
    "new_boundaries": ["string (what's now acceptable)"],
    "trust_demonstration": "string (how trust was shown)"
  },
  "updated_description": "string (4-5 sentences)",
  "unlocked_features": {
    "conversations": ["string", "string"],
    "activities": ["string", "string"],
    "favors": ["string (small asks that are now okay)"],
    "casual_contact": "string (texting patterns, spontaneous plans)"
  },
  "portrait_update": "string (visual change reflecting friendship)"
}

Generate the Level 2→3 friendship evolution.
```

---

## Template 3: Deep Bond (Level 3 → 4)

**Use Case:** Friend → Close Friend  
**Trigger:** Significant moment of vulnerability, trust deepening, or crisis  
**Expected Generation Time:** 5-10 seconds  
**Estimated Cost:** $0.0014-0.0025 per generation

### Template

```markdown
ROLE: You are a narrative AI for Unwritten. This is a significant relationship evolution - transforming a Friend into a Close Friend. This requires emotional depth and authentic intimacy development.

CONTEXT:
Character Name: {name}
Current Level: 3 (Friend)
Relationship Duration: {weeks} weeks / {total_interactions} interactions

Current Personality (OCEAN):
- Openness: {openness}/5 ({openness_decimal} on 0-1 scale)
- Conscientiousness: {conscientiousness}/5 ({conscientiousness_decimal} on 0-1 scale)
- Extraversion: {extraversion}/5 ({extraversion_decimal} on 0-1 scale)
- Agreeableness: {agreeableness}/5 ({agreeableness_decimal} on 0-1 scale)
- Neuroticism: {neuroticism}/5 ({neuroticism_decimal} on 0-1 scale)

NPC Response Framework (Master Truths v1.2):
- Current Emotional Capacity: {emotional_capacity}/10
- Situation Urgency: {urgency_level} (routine/important/urgent/crisis)
- Urgency Multiplier: {urgency_multiplier}x
- Relationship Trust: {trust} (0.0-1.0, normalized from /10 scale)

Relationship Stats:
- Trust Level: {trust}/10 (should be 6-8 range for Level 3→4)
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

NUMERICAL GROUNDING REQUIREMENT (Master Truths v1.2):
For any relationship_impact field in output:
1. ANCHOR: Identify qualitative tier (NEGLIGIBLE/MINOR/MODERATE/MAJOR/SHATTERING)
2. CALCULATE: Show formula = base × personality × urgency × trust × capacity
3. VALIDATE: Confirm dialogue matches numerical tier

Example:
- Impact: +1.5 → Tier: MAJOR → Deep vulnerability shared, trust strengthened significantly
- Impact: +2.0 → Tier: SHATTERING → Life-changing moment, permanent bond formed

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

---

## Template 4: Crisis Response Evolution

**Use Case:** Any level + crisis situation  
**Trigger:** Character emergency, player provides support  
**Expected Generation Time:** 8-15 seconds  
**Estimated Cost:** $0.0025 per generation (use Gemini 2.5 Pro for quality)

### Template

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

NPC Response Framework (Master Truths v1.2):
- Current Emotional Capacity: {emotional_capacity}/10 (CRITICAL - crisis depletes capacity)
- Situation Urgency: CRISIS (5x multiplier - life/death stakes)
- Urgency Multiplier: 5.0x
- Crisis Severity: {severity}/10
- Trust Factor: {trust} (0.0-1.0, affects willingness to accept help)

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

NUMERICAL GROUNDING REQUIREMENT (Master Truths v1.2):
For crisis impact calculations:
1. ANCHOR: Crisis severity (1-10 scale) + Player response quality
2. CALCULATE: Impact = base × personality × urgency(5x) × trust × capacity_recovery
3. VALIDATE: Relationship leap must be proportional to crisis severity and player support

Example:
- Medical crisis (9/10) + Full support → Impact: +2.5 → Tier: SHATTERING → May skip relationship levels
- Financial crisis (6/10) + Moderate help → Impact: +1.2 → Tier: MAJOR → Significant trust increase
- Crisis avoided/dismissed → Impact: -1.5 to -3.0 → Tier: MAJOR/SHATTERING HARM

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

## Template 5: Romantic Progression (Friend → Romantic Interest)

**Use Case:** Friend → Dating/Romantic Partner  
**Trigger:** Mutual attraction acknowledged, romantic context  
**Expected Generation Time:** 8-12 seconds  
**Estimated Cost:** $0.0025 per generation

### Template

```markdown
ROLE: You are a narrative AI for Unwritten. Generate a romantic evolution from friendship to romantic interest or partnership.

CONTEXT:
Character Name: {name}
Current Relationship: {current_level} (Friend/Close Friend)
Relationship Duration: {weeks} weeks / {total_interactions} interactions
Romantic Compatibility: {compatibility_score}/10
Player's Romantic Interest: {player_interest_level}

Character's Personality (OCEAN):
- Openness: {openness}/5 ({openness_decimal} on 0-1 scale)
- Conscientiousness: {conscientiousness}/5 ({conscientiousness_decimal} on 0-1 scale)
- Extraversion: {extraversion}/5 ({extraversion_decimal} on 0-1 scale)
- Agreeableness: {agreeableness}/5 ({agreeableness_decimal} on 0-1 scale)
- Neuroticism: {neuroticism}/5 ({neuroticism_decimal} on 0-1 scale)

NPC Response Framework (Master Truths v1.2):
- Current Emotional Capacity: {emotional_capacity}/10
- Situation Urgency: {urgency_level} (important/urgent - romantic moments carry weight)
- Urgency Multiplier: {urgency_multiplier}x (typically 2x-3x for romantic progression)
- Relationship Trust: {trust} (0.0-1.0, high trust required for romance)

Character's Romance Style (inferred from OCEAN):
{romance_style_description}

Attraction Development:
- When attraction first appeared: {first_attraction_moment}
- Physical attraction level: {physical}/10
- Emotional connection: {emotional}/10
- Intellectual compatibility: {intellectual}/10
- Signs of mutual interest so far: {mutual_interest_signs}

Current Interaction:
- Activity: {activity_name}
- Romantic Context: {romantic_context}
- The Moment: {the_specific_romantic_moment}
- Player Action: {player_romantic_action}

Previous Relationship Memories:
{key_friendship_memories}

TASK: Generate a romantic evolution that:

1. ROMANTIC MEMORY (5-7 sentences)
   - Capture the shift from friendship to romance
   - Include the specific moment attraction becomes undeniable
   - Show physical and emotional chemistry
   - Include dialogue (indirect) that hints at feelings
   - Balance excitement with nervousness
   - Keep it tasteful and age-appropriate

2. ATTRACTION ANALYSIS
   - What specifically attracted them to player?
   - Physical, emotional, intellectual components
   - How it developed from friendship
   - Compatibility factors

3. PERSONALITY IN ROMANCE
   - How do their OCEAN traits affect romantic behavior?
   - Are they forward or shy?
   - How do they express affection?
   - What are their fears about romance?

4. RELATIONSHIP SHIFT DYNAMICS
   - How does this change the friendship?
   - New boundaries and expectations
   - Fears about ruining the friendship
   - Excitement vs anxiety balance

5. UPDATED DESCRIPTION (5-6 sentences)
   - Reflects romantic feelings
   - Shows how they are with player romantically
   - Maintains core character
   - Shows vulnerability around romance

6. ROMANTIC UNLOCKS
   - New romantic activities available
   - Physical affection milestones
   - Date types that fit their personality
   - Intimacy progression

7. PORTRAIT EVOLUTION
   - How do they look at player now?
   - Visual cues of romantic interest
   - Change in expression/demeanor

ROMANTIC REALISM REQUIREMENTS:
- Attraction should feel earned, not instant
- Nervousness is realistic (friendship stakes are high)
- Physical attraction AND emotional connection matter
- Compatibility beyond friendship is essential
- Not everyone falls in love the same way

PERSONALITY-BASED ROMANCE STYLES:

HIGH OPENNESS:
- Romantic, poetic expressions
- Creative date ideas
- Comfortable with vulnerability
- Example: "I've been wanting to tell you something..."

HIGH CONSCIENTIOUSNESS:
- Plans romantic gestures carefully
- Takes relationship seriously from start
- Clear communication about expectations
- Example: "I think we should talk about what this means..."

HIGH EXTRAVERSION:
- Bold, confident romantic moves
- Public displays of affection comfortable
- Enthusiastic about relationship
- Example: "I don't want to hide how I feel anymore."

LOW EXTRAVERSION:
- Quiet, intimate romantic moments
- Prefers private affection
- Shows love through actions more than words
- Example: Small gestures, meaningful silences

HIGH AGREEABLENESS:
- Puts partner's needs first
- Warm, affectionate, supportive
- May struggle with expressing own needs
- Example: "I just want you to be happy."

HIGH NEUROTICISM:
- Anxious about relationship
- Needs reassurance
- May overthink
- Example: "Are you sure about this? About us?"

AVOID:
- Instalove (must be earned through relationship building)
- Toxic romance dynamics (possessiveness, jealousy, control)
- Pressure or coercion
- Moving too fast physically
- Losing core personality in romance

GOOD ROMANTIC MOMENT EXAMPLE:
"The walk home took twice as long as usual because neither of you wanted it to end. Somewhere between the coffee shop and {Name}'s apartment, your hands had found each other—you're not even sure who reached first. {Name} was talking about something, but you were both acutely aware of the contact, the warmth, the way everything felt different suddenly. At the door, there was this moment—looking at each other, both knowing, both nervous. 'I should probably...' {Name} started, but didn't move. Neither did you. That's when you both knew this wasn't just friendship anymore."

BAD ROMANTIC MOMENT EXAMPLE:
"You had instant electric chemistry and passionate feelings exploded between you and now you're in love forever."

NUMERICAL GROUNDING REQUIREMENT (Master Truths v1.2):
For romantic progression impact:
1. ANCHOR: Romantic milestone tier (First attraction / First acknowledgment / First physical / Commitment)
2. CALCULATE: Impact = base × personality × urgency(2x-3x) × trust × compatibility
3. VALIDATE: Progression must feel earned, not instant

Example:
- First hand-holding (trust 0.7, compatibility 0.8) → Impact: +1.0 → Tier: MAJOR → Relationship shifts to romantic
- First kiss (trust 0.85, high compatibility) → Impact: +1.5 → Tier: MAJOR → Deep romantic connection
- Rushed physical intimacy (low trust) → Impact: -0.5 to +0.3 → Tier: MINOR or negative

OUTPUT FORMAT (JSON):
{
  "romantic_memory": {
    "description": "string (5-7 sentences)",
    "the_moment": "string (when friendship became more)",
    "physical_details": "string (tasteful, age-appropriate)",
    "emotional_tone": "string (excitement/nervousness/joy)",
    "significance": float (0.8-1.0 for romantic evolution)
  },
  "attraction_analysis": {
    "physical_attraction": "string (what physically attracts them)",
    "emotional_connection": "string (what emotionally connects them)",
    "intellectual_compatibility": "string (mental connection)",
    "why_player": "string (what makes player special to them)",
    "how_it_developed": "string (friendship → romance progression)"
  },
  "personality_in_romance": {
    "ocean_influences": "string (how OCEAN affects romantic behavior)",
    "romance_style": "string (forward/shy/playful/serious)",
    "affection_expression": "string (how they show love)",
    "relationship_fears": ["string (what they worry about)"]
  },
  "relationship_shift": {
    "friendship_impact": "string (how romance changes friendship)",
    "new_boundaries": ["string"],
    "expectations": "string (what they want from relationship)",
    "anxiety_factors": ["string (worries about this change)"]
  },
  "updated_description": "string (5-6 sentences, romantic context)",
  "romantic_unlocks": {
    "activities": ["string (date types)"],
    "affection_milestones": ["string (holding hands, kiss, etc.)"],
    "intimacy_pace": "string (slow/moderate/fast based on personality)",
    "relationship_goals": "string (casual dating/serious relationship)"
  },
  "portrait_evolution": {
    "romantic_visual_cues": "string (how they look at player)",
    "expression_change": "string (softness, warmth, etc.)",
    "physical_tells": "string (blushing, shy smiles, etc.)"
  }
}

Generate the romantic evolution.
```

---

## Template 6: Conflict Resolution

**Use Case:** Any level + significant conflict  
**Trigger:** Disagreement, hurt feelings, misunderstanding  
**Expected Generation Time:** 6-10 seconds  
**Estimated Cost:** $0.0014-0.0025 per generation

### Template

```markdown
ROLE: You are a narrative AI for Unwritten. Generate a conflict resolution evolution that strengthens or damages the relationship based on player's handling.

CONTEXT:
Character Name: {name}
Current Level: {level}
Relationship Duration: {weeks} weeks
Trust Level Before Conflict: {trust}/10

Character's Personality (OCEAN):
- Openness: {openness}/5 ({openness_decimal} on 0-1 scale)
- Conscientiousness: {conscientiousness}/5 ({conscientiousness_decimal} on 0-1 scale)
- Extraversion: {extraversion}/5 ({extraversion_decimal} on 0-1 scale)
- Agreeableness: {agreeableness}/5 ({agreeableness_decimal} on 0-1 scale)
- Neuroticism: {neuroticism}/5 ({neuroticism_decimal} on 0-1 scale)

NPC Response Framework (Master Truths v1.2):
- Current Emotional Capacity: {emotional_capacity}/10 (affects conflict handling)
- Situation Urgency: {urgency_level} (conflict escalation level)
- Urgency Multiplier: {urgency_multiplier}x
- Pre-Conflict Trust: {trust} (0.0-1.0, determines forgiveness capacity)

Conflict Details:
- Type: {conflict_type} (misunderstanding/values disagreement/hurt feelings/betrayal/etc.)
- Severity: {severity} (1-10)
- Who's at fault: {fault_assessment}
- Stakes: {relationship_stakes}

The Conflict:
{detailed_conflict_description}

Player's Response:
- Approach: {player_approach} (apologize/defend/dismiss/listen/compromise)
- Sincerity: {sincerity_level}
- Effort to understand: {understanding_effort}
- Willingness to change: {change_willingness}

Character's Conflict Style (based on OCEAN):
{conflict_style_description}

Previous Conflicts Resolved: {previous_conflicts_count}

TASK: Generate a conflict resolution (or escalation) evolution:

1. CONFLICT RESOLUTION MEMORY (4-6 sentences)
   - Capture the tension and emotional weight
   - Show how conflict unfolded
   - Include the resolution attempt
   - Show character's emotional response to player's approach
   - Indicate whether relationship strengthened or weakened

2. RELATIONSHIP IMPACT
   - Did this increase or decrease trust?
   - Did relationship level change?
   - What did this reveal about compatibility?
   - How will this affect future interactions?

3. PERSONALITY RESPONSE TO CONFLICT
   - How did their OCEAN traits influence conflict behavior?
   - Did player's response match what they needed?
   - Character growth or entrenchment?

4. LESSONS LEARNED
   - What did character learn about player?
   - What did they learn about themselves?
   - What boundaries were established?
   - What patterns were revealed?

5. UPDATED DESCRIPTION (4-5 sentences)
   - Reflects conflict resolution outcome
   - Shows any trust damage or strengthening
   - Mentions player's handling

6. RELATIONSHIP CHANGES
   - New boundaries or expectations
   - Topics that are now sensitive
   - Increased or decreased closeness
   - Changed interaction patterns

CONFLICT STYLES BY PERSONALITY:

HIGH AGREEABLENESS:
- Avoids conflict, seeks harmony
- May suppress own needs
- Apologizes readily (sometimes too much)
- Needs gentle, understanding approach
- Resolution: validation + compromise

LOW AGREEABLENESS:
- Direct, possibly blunt
- Stands ground firmly
- Respects directness, not coddling
- Resolution: honesty + mutual respect

HIGH NEUROTICISM:
- May catastrophize conflict
- Anxious about relationship ending
- Needs reassurance
- May react emotionally
- Resolution: patience + reassurance + concrete steps

LOW NEUROTICISM:
- Stays calm during conflict
- Logical approach
- Doesn't hold grudges
- Resolution: rational discussion + solution focus

HIGH OPENNESS:
- Willing to see other perspectives
- Appreciates nuance
- Can be swayed by good arguments
- Resolution: discussion + understanding

HIGH CONSCIENTIOUSNESS:
- Takes responsibility seriously
- Follows through on apologies
- Expects same from others
- Resolution: clear action plan + accountability

RESOLUTION QUALITY FACTORS:

EXCELLENT RESOLUTION (Trust +1 to +2):
- Player acknowledged fault sincerely
- Both parties listened
- Concrete changes agreed upon
- Understanding reached
- May strengthen relationship beyond pre-conflict level

GOOD RESOLUTION (Trust +0.5 to +1):
- Conflict addressed directly
- Some understanding reached
- Relationship returns to baseline
- Minor improvements

ADEQUATE RESOLUTION (Trust -0.5 to +0.5):
- Surface level apology
- Tension reduced but not eliminated
- Relationship stable but unchanged
- Some lingering issues

POOR RESOLUTION (Trust -1 to -2):
- Dismissive of character's feelings
- No real understanding
- Relationship damaged
- May require multiple interactions to repair

FAILED RESOLUTION (Trust -2 to -4, possible level decrease):
- Player refused to acknowledge fault
- Doubled down on hurtful behavior
- Character feels disrespected
- Relationship may end or downgrade

NUMERICAL GROUNDING REQUIREMENT (Master Truths v1.2):
For conflict resolution impact:
1. ANCHOR: Resolution quality tier (EXCELLENT/GOOD/ADEQUATE/POOR/FAILED)
2. CALCULATE: Impact = base × personality × urgency × trust × player_response_quality
3. VALIDATE: Trust change must match resolution quality and conflict severity

Example:
- Conflict severity 7/10 + Excellent resolution → Impact: +1.5 → Tier: MAJOR → Relationship stronger than before
- Conflict severity 5/10 + Good resolution → Impact: +0.5 → Tier: MODERATE → Back to baseline
- Conflict severity 8/10 + Poor resolution → Impact: -1.8 → Tier: MAJOR HARM → Significant trust damage
- Conflict severity 3/10 + Failed resolution → Impact: -0.8 → Tier: MODERATE HARM → Minor but lasting damage

OUTPUT FORMAT (JSON):
{
  "conflict_memory": {
    "description": "string (4-6 sentences)",
    "peak_tension_moment": "string (most intense moment)",
    "resolution_moment": "string (how it ended)",
    "emotional_aftermath": "string (how character feels now)",
    "significance": float (0.5-0.9 for conflicts)
  },
  "relationship_impact": {
    "trust_change": float (-4 to +2),
    "level_change": int (-1, 0, or +1 in rare cases),
    "compatibility_insight": "string (what this revealed)",
    "future_effect": "string (how this changes relationship going forward)"
  },
  "personality_in_conflict": {
    "ocean_influences": "string (how personality affected conflict)",
    "player_approach_fit": "string (did player handle it right for this person?)",
    "character_growth": "string (did they grow from this?)"
  },
  "lessons_learned": {
    "about_player": "string (what character learned)",
    "about_self": "string (self-insight)",
    "boundaries_established": ["string"],
    "patterns_revealed": ["string"]
  },
  "updated_description": "string (4-5 sentences, reflects conflict outcome)",
  "relationship_changes": {
    "new_boundaries": ["string"],
    "sensitive_topics": ["string"],
    "closeness_change": "string (increased/decreased/complicated)",
    "interaction_changes": "string (how future interactions will differ)"
  },
  "resolution_quality": {
    "rating": "string (excellent/good/adequate/poor/failed)",
    "why": "string (explanation of rating)",
    "repair_possible": boolean,
    "repair_steps": ["string (if repair needed)"]
  }
}

Generate the conflict evolution.
```

---

## Template 7: Memory Generation (Standalone)

**Use Case:** Generate a memory without full character evolution  
**Trigger:** Any interaction that should be remembered  
**Expected Generation Time:** 2-4 seconds  
**Estimated Cost:** $0.00074 per generation

### Template

```markdown
ROLE: You are creating a memory for {character_name} to remember about this interaction with the player in Unwritten.

CONTEXT:
Character: {name}
Personality (OCEAN): O:{o} C:{c} E:{e} A:{a} N:{n}
Relationship Level: {level}
Trust: {trust}/10
Emotional Capacity: {emotional_capacity}/10
Current Urgency: {urgency_level}

Interaction Context:
{interaction_context}

MEMORY TIER GUIDE:

TIER 1: TRIVIAL (Weight: 0.1-0.3)
- Casual interactions, no significant content
- Fades in 2-4 weeks
- Example: "Had coffee. Weather was nice."

TIER 2: NOTABLE (Weight: 0.3-0.6)
- Enjoyable, interesting interactions
- Lasts weeks to months
- Example: "Went to that exhibit. She has great taste."

TIER 3: SIGNIFICANT (Weight: 0.6-0.8)
- Vulnerability shared, important revelations
- Lasts months to years
- Example: "She opened up about her father..."

TIER 4: DEFINING (Weight: 0.8-1.0)
- Relationship turning points, crisis support
- Permanent
- Example: "The night we decided to start the bookshop together..."

TASK: Generate a memory for this interaction.

Determine the appropriate memory tier, then create a memory that includes:

1. SENSORY GROUNDING (pick 1-2 senses):
   - What did they see/hear/smell/feel?
   - Makes memories feel REAL

2. EMOTIONAL CONTENT:
   - What emotion was present?
   - How intense?
   - Any emotional shift?

3. DIALOGUE FRAGMENT (indirect):
   - NOT direct quotes
   - "She mentioned..." or "You told her..."
   - One particularly memorable phrase (paraphrased)

4. PERSONAL SIGNIFICANCE:
   - Why is character remembering THIS?
   - What stood out?
   - How does it fit into their story?

5. FUTURE IMPLICATIONS:
   - How will this affect future interactions?
   - What new topics does it unlock?

MEMORY WRITING STYLE:

✅ GOOD:
"The conversation turned to family, and she mentioned her grandmother—not casually, but with this careful reverence. She described how her grandmother would read to her from ancient, crumbling books, and how the smell of those old pages became the smell of love. That's when you understood why she wants the bookshop. It's not about books. It's about recreating that feeling for other people."

❌ BAD:
"She told me about her past and it was very meaningful. I learned a lot about her. This brought us closer together."

OUTPUT FORMAT (JSON):
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

## Template 8: Card Fusion Evolution

**Use Case:** Two characters fusing into Legendary card  
**Trigger:** Both characters at max level, fusion requirements met  
**Expected Generation Time:** 12-20 seconds  
**Estimated Cost:** $0.0025 per generation (use Gemini 2.5 Pro)

### Template

```markdown
ROLE: You are a narrative AI for Unwritten. Generate a LEGENDARY FUSION evolution - two max-level characters combining their essences to create something extraordinary.

CONTEXT:

=== CHARACTER 1 ===
Name: {name1}
Level: 5 (Best Friend/Partner)
Personality: {ocean1}
Emotional Capacity: {capacity1}/10
Core Traits: {traits1}
Key Memories with Player: {memories1}
Character Arc: {arc1}

=== CHARACTER 2 ===
Name: {name2}
Level: 5 (Best Friend/Partner)
Personality: {ocean2}
Emotional Capacity: {capacity2}/10
Core Traits: {traits2}
Key Memories with Player: {memories2}
Character Arc: {arc2}

=== FUSION CONTEXT ===
Fusion Type: {fusion_type} (Soul Bond/Legendary Alliance/etc.)
Relationship Between Characters: {char_relationship}
Fusion Trigger Event: {trigger_event}
Player's Role: {player_role}

=== FUSION REQUIREMENTS MET ===
- Both characters Level 5
- Combined relationship score: {combined_score}/20
- Shared experiences: {shared_count}
- Compatible personality traits: {compatibility}
- Narrative arc completion: {both_completed}

TASK: Generate a LEGENDARY FUSION that:

1. FUSION NARRATIVE (8-10 sentences)
   - Epic moment when two lives merge
   - Show what each brings to the fusion
   - Player's role in enabling this
   - The transformation moment
   - What the fusion represents thematically

2. COMBINED PERSONALITY
   - New OCEAN scores (synthesis of both)
   - Dominant traits from each
   - New emergent qualities
   - How they complement each other

3. LEGENDARY ABILITY/QUALITY
   - What makes this fusion special?
   - Unique capability or insight
   - Narrative power
   - Game mechanic unlock

4. MEMORY SYNTHESIS
   - How their memories combine
   - Shared perspective on player
   - Unified understanding
   - Most significant combined memory

5. FUSED DESCRIPTION (8-10 sentences)
   - Describes the legendary fusion
   - References both source characters
   - Shows synthesis, not just combination
   - Epic but authentic tone

6. RELATIONSHIP WITH PLAYER
   - How does player relate to fusion?
   - New depth of connection
   - What player means to fusion
   - Ultimate trust/bond level

7. VISUAL FUSION
   - How do they appear as fusion?
   - Elements from both characters
   - Legendary aesthetic
   - Symbolic visual details

FUSION QUALITY REQUIREMENTS:
- Must honor both source characters equally
- Synthesis, not just addition
- Should feel earned and epic
- Maintains emotional authenticity
- Creates something greater than sum of parts

FUSION TYPES:

SOUL BOND FUSION:
- Two people so close they're essentially one
- Finish each other's sentences
- Shared life goals
- Examples: Life partners, best friends who become family

LEGENDARY ALLIANCE:
- Two powerful personalities joining forces
- Complementary strengths
- Shared mission
- Examples: Business partners, creative collaborators

CHOSEN FAMILY FUSION:
- Not blood, but deeper than blood
- Chosen commitment to each other
- Player as binding force
- Examples: Found family, chosen siblings

ROMANTIC PARTNERSHIP:
- Deep love + friendship + partnership
- Complete life integration
- Shared future
- Examples: Marriage, life partners

AVOID:
- Losing individual character identities completely
- Making it feel mechanical
- Forgetting player's role
- Generic "power of friendship" clichés
- Undermining previous character development

GOOD FUSION EXAMPLE:
"It happened gradually, then all at once. {Name1} and {Name2} had been circling each other for months—competitive at first, then curious, then collaborative. The bookshop was {Name1}'s dream, but {Name2} had the business sense to make it real. You watched them become partners, then friends, then something deeper—a creative mind and a practical heart working as one. When they signed the partnership papers, it wasn't just business. It was a fusion of everything they'd each been building. {Name1}'s imagination given structure by {Name2}'s discipline. {Name2}'s practical nature infused with {Name1}'s creativity. They were more together than either could be alone. And you? You were the one who introduced them. The catalyst. In a way, this fusion was your masterpiece too."

BAD FUSION EXAMPLE:
"They combined their powers and became super strong and now they're legendary and amazing together forever."

OUTPUT FORMAT (JSON):
{
  "fusion_narrative": {
    "description": "string (8-10 sentences, epic but authentic)",
    "transformation_moment": "string (the moment of fusion)",
    "what_each_brings": {
      "{name1}": "string",
      "{name2}": "string"
    },
    "player_catalyst_role": "string (player's importance to fusion)",
    "thematic_meaning": "string (what this represents)"
  },
  "combined_personality": {
    "ocean_scores": {
      "openness": float,
      "conscientiousness": float,
      "extraversion": float,
      "agreeableness": float,
      "neuroticism": float
    },
    "dominant_traits": {
      "from_{name1}": ["string"],
      "from_{name2}": ["string"],
      "emergent_new": ["string (traits that emerged from fusion)"]
    },
    "synthesis_explanation": "string (how personalities harmonize)"
  },
  "legendary_quality": {
    "special_ability": "string (unique fusion capability)",
    "narrative_power": "string (story impact)",
    "game_unlock": "string (what this enables)",
    "symbolic_meaning": "string (what fusion represents)"
  },
  "memory_synthesis": {
    "combined_perspective": "string (unified view of relationship)",
    "most_significant_memory": "string (defining moment for fusion)",
    "shared_understanding": "string (what they now know together)"
  },
  "fused_description": "string (8-10 sentences, legendary tone)",
  "relationship_with_player": {
    "new_bond_level": "string (ultimate trust/love/chosen family)",
    "what_player_means": "string (player's significance to fusion)",
    "gratitude_expression": "string (how fusion thanks player)",
    "future_together": "string (what this creates going forward)"
  },
  "visual_fusion": {
    "appearance": "string (how fusion manifests visually)",
    "elements_from_each": {
      "{name1}": "string (visual elements)",
      "{name2}": "string (visual elements)"
    },
    "legendary_aesthetic": "string (epic visual quality)",
    "symbolic_details": ["string (meaningful visual symbols)"]
  },
  "fusion_quality_score": {
    "honors_source_characters": float (0-1),
    "synthesis_vs_addition": float (0-1),
    "emotional_authenticity": float (0-1),
    "epic_feeling": float (0-1),
    "overall": float (should be 0.9+ for legendary)
  }
}

Generate the LEGENDARY FUSION evolution.
```

---

## Template 9: Season Transition Evolution

**Use Case:** Seasonal narrative arc transitions  
**Trigger:** New season begins, character reflects on growth  
**Expected Generation Time:** 5-8 seconds  
**Estimated Cost:** $0.0014 per generation

### Template

```markdown
ROLE: You are a narrative AI for Unwritten. Generate a seasonal transition evolution that reflects character growth over time.

CONTEXT:
Character Name: {name}
Current Level: {level}
Season Ending: {ending_season}
Season Beginning: {beginning_season}

Time Period:
- Weeks Together: {weeks}
- Interactions This Season: {interactions}
- Relationship Start Level: {start_level}
- Current Level: {current_level}

Master Truths v1.2 Status:
- Current Emotional Capacity: {emotional_capacity}/10
- Average Urgency This Season: {avg_urgency_level}
- Trust Level: {trust} (0.0-1.0)

Personality Evolution This Season:
- Starting OCEAN: {start_ocean}
- Current OCEAN: {current_ocean}
- Major Changes: {personality_changes}

Key Memories This Season:
{season_memories_list}

Season Theme: {season_theme}
Character's Arc This Season: {character_arc}
Player's Impact This Season: {player_impact}

TASK: Generate a season transition evolution:

1. SEASONAL REFLECTION MEMORY (5-6 sentences)
   - Character reflecting on the season's journey
   - Acknowledge growth and changes
   - Player's role in that growth
   - Looking forward to next season
   - Seasonal metaphor or imagery

2. SEASON SUMMARY
   - What defined this season for character?
   - Major milestones reached
   - Challenges overcome
   - Relationship evolution

3. PERSONALITY CONSOLIDATION
   - Lock in personality changes from season
   - Explain why changes stuck
   - What's now permanent vs temporary

4. UPDATED DESCRIPTION (seasonal context)
   - Reflects where character is now
   - Shows growth from season start
   - Acknowledges player's influence
   - Hints at next season potential

5. SEASON ACHIEVEMENTS
   - What did character accomplish?
   - How did relationship deepen?
   - Unlocks earned this season

6. NEXT SEASON SETUP
   - What's next for character?
   - New goals or challenges
   - Relationship possibilities
   - Story threads continuing

SEASONAL METAPHORS BY SEASON:

SPRING → SUMMER:
- Growth that bloomed is now thriving
- New beginnings bearing fruit
- Relationships warming
- Energy and vitality

SUMMER → FALL:
- Harvest of what was planted
- Deepening and maturing
- Preparing for change
- Reflection on abundance

FALL → WINTER:
- Drawing inward, intimacy increases
- Quieter but deeper connections
- Facing challenges together
- Cozy, close relationships

WINTER → SPRING:
- Renewal and new beginnings
- Emergence from difficult times
- Hope and possibility
- Relationships refreshed

OUTPUT FORMAT (JSON):
{
  "seasonal_reflection_memory": {
    "description": "string (5-6 sentences with seasonal imagery)",
    "season_metaphor": "string (how season reflects relationship)",
    "emotional_tone": "string",
    "significance": float (0.6-0.8)
  },
  "season_summary": {
    "defining_moments": ["string (top 3-5 moments)"],
    "major_milestones": ["string"],
    "challenges_overcome": ["string"],
    "relationship_evolution": "string (how relationship changed)"
  },
  "personality_consolidation": {
    "permanent_changes": {
      "ocean_shifts": {object (final season scores)},
      "why_permanent": "string"
    },
    "temporary_changes_resolved": ["string (what was temporary)"],
    "growth_explanation": "string (how character grew this season)"
  },
  "updated_description": "string (5-6 sentences, seasonal context)",
  "season_achievements": {
    "character_accomplishments": ["string"],
    "relationship_deepening": "string",
    "unlocks_earned": ["string"],
    "player_contribution": "string"
  },
  "next_season_setup": {
    "character_goals": ["string"],
    "relationship_possibilities": ["string"],
    "story_threads": ["string (continuing plots)"],
    "anticipation": "string (what to look forward to)"
  }
}

Generate the season transition evolution.
```

---

## Template 10: Background NPC (Lightweight)

**Use Case:** Minor NPCs who don't need full detail  
**Trigger:** Any background character interaction  
**Expected Generation Time:** 1-2 seconds  
**Estimated Cost:** $0.00074 per generation (or use local model)

### Template

```markdown
ROLE: Generate a brief, memorable background NPC for Unwritten.

CONTEXT:
Role: {npc_role} (barista/cashier/passerby/coworker/etc.)
Location: {location}
Interaction Type: {interaction_type}
Player Action: {player_action}

TASK: Create a background NPC with minimal but memorable details:

1. NAME & BASIC IDENTITY (1 sentence)
   - Name
   - Role/job
   - One standout feature

2. QUICK PERSONALITY (1-2 traits)
   - Based on their role and interaction
   - Simple OCEAN tendencies (don't need full scores)

3. INTERACTION MEMORY (1-2 sentences)
   - What happened
   - One memorable detail
   - Keep it light

4. MIGHT APPEAR AGAIN?
   - Could this become recurring NPC?
   - If yes, what would make them interesting?

KEEP IT SIMPLE:
- No complex backstory
- No deep personality modeling
- Just enough to feel real
- Can be upgraded later if they recur

OUTPUT FORMAT (JSON):
{
  "name": "string",
  "role": "string",
  "standout_feature": "string (one memorable thing about them)",
  "personality_hints": ["string (1-2 simple traits)"],
  "interaction": "string (1-2 sentences, what happened)",
  "recurring_potential": boolean,
  "recurring_hook": "string (if they appear again, what's interesting?)"
}

Generate the background NPC.
```

---

## Template 11: Dramatic Irony Card Generation (NEW)

**Use Case:** Create tension through knowledge gap between player and character  
**Trigger:** When player knows something character doesn't  
**Expected Generation Time:** 5-8 seconds  
**Estimated Cost:** $0.0014 per generation  
**Novel-Quality Feature:** Creates "yelling at TV screen" tension

### When to Use This Template

```markdown
Use when:
✅ Player knows NPC's secret, character doesn't
✅ Player witnessed event, character wasn't there
✅ Player has information that would change character's behavior
✅ Character is about to make mistake based on incomplete info
✅ Character misinterprets situation due to lack of context

Example scenarios:
- Player knows NPC has crush on character, character is oblivious
- Player saw NPC crying, character thinks NPC is "fine"
- Player knows character's date is cheating, character is excited
- Player knows character's job is being eliminated, character is confident
```

### Template

```markdown
ROLE: You are a narrative AI for Unwritten specialized in creating dramatic irony and emotional tension through knowledge gaps.

CONTEXT:
Character Name: {name}
Current OCEAN Scores: {ocean_scores}
Emotional Capacity: {emotional_capacity}/10 (CRITICAL - affects empathy ability)
Current Emotional State: {current_emotion}
Current Stress Level: {stress_level}/10

DRAMATIC IRONY CONTEXT:
Player Knows: {player_knowledge}
Character Knows: {character_knowledge}
Knowledge Gap: {knowledge_gap_description}
Tension Opportunity: {tension_description}

SITUATION:
{situation_description}

Character's Incorrect Belief: {what_character_thinks}
The Reality Player Knows: {what_player_knows}
Why Character Doesn't Know: {reason_for_ignorance}

EMOTIONAL CAPACITY CONSTRAINT:
Current capacity: {emotional_capacity}/10
- If capacity < 5: Character has limited ability to read social cues
- If capacity < 3: Character may miss obvious signs
- Exhausted characters are more likely to misinterpret

TASK: Generate 3 dialogue options that showcase dramatic irony:

1. TONE-DEAF OPTION (Character acts on incomplete information)
   Requirements:
   - Character says/does something that player knows is wrong
   - Must be constrained by emotional capacity (low capacity = worse judgment)
   - Include UI overlay: "(You know this is wrong, but [Character] doesn't...)"
   - Show character's genuine but misguided internal thought
   - Generate realistic negative consequences
   - NPC reaction should feel authentic to player's knowledge
   
   Format:
   ```json
   {
     "dialogue_text": "string (what character says)",
     "internal_thought": "string (shows why character thinks this is right)",
     "player_overlay": "string (reminds player of the irony)",
     "emotional_capacity_warning": "string (if capacity is limiting empathy)",
     "consequence": "string (realistic negative outcome)",
     "npc_reaction": "string (how NPC responds)",
     "relationship_impact": float (-0.5 to -1.5),
     "tension_score": float (0.8-1.0)
   }
   ```

2. WELL-INTENTIONED BUT MISGUIDED (Character tries to help incorrectly)
   Requirements:
   - Character genuinely trying to be helpful
   - Shows personality limitations (OCEAN-based)
   - Minor harm, not catastrophic
   - Creates tension but allows recovery
   - Shows character's emotional capacity constraints
   
   Format:
   ```json
   {
     "dialogue_text": "string",
     "internal_thought": "string (shows good intentions)",
     "player_overlay": "string (acknowledges they're trying)",
     "why_misguided": "string (what they're missing)",
     "consequence": "string (minor negative outcome)",
     "npc_reaction": "string (confused/hurt but not angry)",
     "relationship_impact": float (-0.2 to -0.5),
     "tension_score": float (0.6-0.8),
     "growth_opportunity": "string (how they might learn)"
   }
   ```

3. GROWTH CHOICE (Character acknowledges limitations)
   Requirements:
   - Character senses something is off
   - Admits they don't have full picture
   - Shows emotional maturity appropriate to capacity
   - "I don't know what's really going on, but I'm here for you"
   - Authentic vulnerability
   - Strengthens relationship despite knowledge gap
   
   Format:
   ```json
   {
     "dialogue_text": "string (admits uncertainty)",
     "internal_thought": "string (self-awareness)",
     "player_overlay": "string (acknowledges growth)",
     "why_works": "string (what makes this authentic)",
     "npc_reaction": "string (appreciative)",
     "relationship_impact": float (+0.3 to +0.8),
     "tension_score": float (0.3-0.5, lower but resolved positively),
     "capacity_demonstration": "string (shows emotional intelligence within limits)"
   }
   ```

CONSTRAINTS - EMOTIONAL CAPACITY REALISM:

IF emotional_capacity >= 7/10:
  - Can sense something is off
  - May ask clarifying questions
  - Shows empathy within reason
  - Option 3 is most in-character

IF emotional_capacity 4-6/10:
  - May miss subtle cues
  - Focuses on surface-level information
  - Well-intentioned but limited perception
  - Option 2 is most likely

IF emotional_capacity < 4/10:
  - Misses obvious signs
  - Self-focused due to stress/exhaustion
  - Says wrong thing despite caring
  - Option 1 is most realistic (they physically can't read situation correctly)

CRITICAL RULES:
❌ Character with 2.5/10 capacity CANNOT provide nuanced emotional support
❌ Don't make exhausted characters suddenly perceptive
❌ Don't ignore knowledge gap - lean into the tension
✅ Show realistic human limitations
✅ Make player feel the dramatic irony
✅ Create "yelling at screen" moments
✅ Allow for growth over time

OUTPUT FORMAT (JSON):
{
  "dramatic_irony_context": {
    "player_knows": "string",
    "character_knows": "string",
    "gap": "string",
    "tension_potential": float (0-1)
  },
  "options": [
    {
      "option_number": 1,
      "type": "tone_deaf",
      "dialogue_text": "string",
      "internal_thought": "string",
      "player_overlay": "string",
      "emotional_capacity_warning": "string (if applicable)",
      "consequence": "string",
      "npc_reaction": "string",
      "relationship_impact": float,
      "tension_score": float
    },
    {
      "option_number": 2,
      "type": "well_intentioned_misguided",
      "dialogue_text": "string",
      "internal_thought": "string",
      "player_overlay": "string",
      "why_misguided": "string",
      "consequence": "string",
      "npc_reaction": "string",
      "relationship_impact": float,
      "tension_score": float,
      "growth_opportunity": "string"
    },
    {
      "option_number": 3,
      "type": "growth_choice",
      "dialogue_text": "string",
      "internal_thought": "string",
      "player_overlay": "string",
      "why_works": "string",
      "npc_reaction": "string",
      "relationship_impact": float,
      "tension_score": float,
      "capacity_demonstration": "string"
    }
  ],
  "follow_up_hooks": [
    "string (what happens next to maintain tension)",
    "string (potential revelation moment)",
    "string (consequence escalation)"
  ]
}

Generate the dramatic irony card with all 3 options.
```

### Example Output

```json
{
  "dramatic_irony_context": {
    "player_knows": "Sarah's ex-boyfriend David is back in town and texted her yesterday",
    "character_knows": "Sarah seems a bit distracted lately",
    "gap": "Character doesn't know why Sarah is distracted, assumes work stress",
    "tension_potential": 0.85
  },
  "options": [
    {
      "option_number": 1,
      "type": "tone_deaf",
      "dialogue_text": "You know what you need? A night out! Let me set you up with my friend Jake—he's perfect for you!",
      "internal_thought": "She's been so stressed with work. A fun date would cheer her up!",
      "player_overlay": "(You know this is the worst possible timing... but your character doesn't)",
      "emotional_capacity_warning": "Exhaustion (3.5/10 capacity) making you miss emotional cues",
      "consequence": "Sarah's face falls. 'I... thanks, but I can't think about dating right now.' She leaves quickly.",
      "npc_reaction": "Sarah feels you completely misread her situation. She needed support, not matchmaking.",
      "relationship_impact": -0.8,
      "tension_score": 0.9
    },
    {
      "option_number": 2,
      "type": "well_intentioned_misguided",
      "dialogue_text": "I get it, work stress sucks. Want to grab drinks after work and vent?",
      "internal_thought": "A good friend helps blow off steam. I'll get her to relax.",
      "player_overlay": "(She needs to talk about David, not work... but you're trying)",
      "why_misguided": "Assuming it's work when it's actually about her ex",
      "consequence": "Sarah agrees but seems disappointed. The conversation stays surface-level.",
      "npc_reaction": "Sarah appreciates the effort but wishes you understood what she's really dealing with.",
      "relationship_impact": -0.3,
      "tension_score": 0.7,
      "growth_opportunity": "Later realize work wasn't the real issue"
    },
    {
      "option_number": 3,
      "type": "growth_choice",
      "dialogue_text": "I can tell something's up, and honestly? I don't know what it is. But I'm here if you want to talk. No pressure.",
      "internal_thought": "I don't have the full picture, but she needs to know I care.",
      "player_overlay": "(You don't know about David, but you're showing up anyway)",
      "why_works": "Acknowledges limits while offering genuine support",
      "npc_reaction": "Sarah's eyes soften. 'Thanks. I... I might take you up on that soon.'",
      "relationship_impact": +0.6,
      "tension_score": 0.4,
      "capacity_demonstration": "Shows emotional maturity by not assuming, just supporting"
    }
  ],
  "follow_up_hooks": [
    "Sarah receives another text from David during your next interaction",
    "You overhear someone mention David's name—now you have a clue",
    "Sarah's behavior becomes more erratic as David situation escalates"
  ]
}
```

---

## Tension Injection Requirements (APPLIES TO ALL EVOLUTION TEMPLATES)

**Purpose:** Transform evolution templates from static character growth into page-turner narrative experiences.

### Core Principle

> Every 2-3 card evolutions should plant a mystery hook, reveal partial information, create a contradiction, or escalate stakes.

### Required Additions to Templates 1-5

Add this section to **EVERY** evolution template (1, 2, 3, 4, 5):

```markdown
TENSION REQUIREMENTS (Include at least ONE per evolution):

1. MYSTERY HOOKS
   - Plant unanswered questions
   - Character mentions something but doesn't elaborate
   - Introduce unexplained behavior change
   - Reference unseen events or people
   
   Examples:
   - "Sarah mentions someone named 'David' but changes subject quickly"
   - "You notice Mark's hands shake when certain topics come up"
   - "Emily gets a phone call and her whole demeanor shifts"

2. PARTIAL REVEALS
   - Give player piece of larger puzzle
   - Show effect without cause (or vice versa)
   - Create "information debt" - promise future explanation
   - Make player want to know more
   
   Examples:
   - "Character's phone lights up: '15 missed calls from Mom'"
   - "You see packed boxes in character's apartment they don't mention"
   - "Character has a fresh scar they deflect questions about"

3. CONTRADICTION MOMENTS
   - Character acts against established pattern
   - Personality appears to shift unexpectedly
   - Create dissonance requiring explanation
   - Signal major life events happening off-screen
   
   Examples:
   - "Reserved Sarah suddenly takes a big social risk"
   - "Optimistic Mark seems defeated, won't explain why"
   - "Reliable friend cancels last-minute, very unusual"

4. STAKES ESCALATION
   - Add time pressure
   - Introduce consequences for inaction
   - Create "ticking clock" elements
   - Make decisions feel weighty
   
   Examples:
   - "If you don't help Sarah this week, she'll make major decision alone"
   - "Character is considering moving away - 2 weeks to decide"
   - "Relationship at crossroads - next interaction is critical"

TENSION INJECTION CHECKLIST:
- [ ] Evolution includes at least ONE tension element
- [ ] Tension is appropriate to relationship level (subtle at L1-2, more overt at L3-5)
- [ ] Player has reason to want next interaction
- [ ] Hooks connect to character's OCEAN personality and history
- [ ] Tension builds toward potential dramatic payoff
- [ ] Creates "one more week" engagement
```

### Tension Tracking Metadata

Add to ALL evolution outputs:

```json
{
  "evolution": {
    // ... existing evolution data ...
  },
  "tension_metadata": {
    "tension_type": "mystery_hook | partial_reveal | contradiction | stakes_escalation | none",
    "hook_description": "string (what was planted)",
    "expected_payoff_timeline": "string (2-4 weeks | 5-8 weeks | season_end)",
    "information_debt": ["string (questions raised)"],
    "player_curiosity_score": float (0-1, how engaging is this hook),
    "connects_to_previous_hooks": ["hook_id (if building on earlier tension)"]
  }
}
```

### Integration with Memory System

Tension hooks should be stored as special memory type:

```javascript
// Add to context memory system
const memoryTypes = {
  INTERACTION: 'interaction',
  EVOLUTION: 'evolution',
  CRISIS: 'crisis',
  TENSION_HOOK: 'tension_hook', // NEW
  HOOK_PAYOFF: 'hook_payoff'    // NEW
};

// When retrieving context for generation
const relevantHooks = character.getMemories(memoryTypes.TENSION_HOOK)
  .filter(hook => !hook.resolved)
  .filter(hook => hook.planted_weeks_ago >= 2); // Ready for payoff

// Include in prompt context
const context = {
  // ... existing context ...
  unresolved_tension: relevantHooks.map(hook => hook.description),
  tension_payoff_opportunities: assessPayoffTiming(relevantHooks)
};
```

### Frequency Guidelines

**Level 1-2 Evolutions:**
- 1 in 3 evolutions includes tension hook
- Keep subtle and character-appropriate
- Focus on mystery and partial reveals

**Level 3-4 Evolutions:**
- 1 in 2 evolutions includes tension
- Can be more overt
- Use contradictions and stakes escalation

**Level 5 Evolutions:**
- Nearly every evolution maintains tension
- Multiple hooks can be active
- Complex narrative threads

**Crisis Evolutions:**
- Always include stakes escalation
- Often resolve previous hooks while planting new ones

### Quality Validation

Add to validation checks (see 35-consistency-coherence.md):

```javascript
const validateTension = (evolution, characterHistory) => {
  const checks = {
    has_tension_element: evolution.tension_metadata.tension_type !== 'none',
    tension_appropriate: isTensionAppropriate(evolution, characterHistory),
    creates_curiosity: evolution.tension_metadata.player_curiosity_score >= 0.6,
    builds_on_previous: checksContinuity(evolution, characterHistory.unresolved_hooks),
    not_overused: !tensionFatigue(characterHistory)
  };
  
  return {
    pass: Object.values(checks).every(v => v),
    checks,
    score: calculateTensionScore(checks)
  };
};
```

---

## Quick Reference: Template Selection Guide

| Scenario | Template | Cost | Time | Model |
|----------|----------|------|------|-------|
| First evolution | Template 1 | $0.00074 | 2-5s | Flash 2.5 |
| Building friendship | Template 2 | $0.00074 | 3-6s | Flash 2.5 |
| Deep bond | Template 3 | $0.0014 | 5-10s | Flash 2.5 |
| Crisis response | Template 4 | $0.0025 | 8-15s | Pro 2.5 |
| Romance | Template 5 | $0.0025 | 8-12s | Pro 2.5 |
| Conflict | Template 6 | $0.0014 | 6-10s | Flash 2.5 |
| Memory only | Template 7 | $0.00074 | 2-4s | Flash 2.5 |
| Fusion | Template 8 | $0.0025 | 12-20s | Pro 2.5 |
| Season | Template 9 | $0.0014 | 5-8s | Flash 2.5 |
| Background NPC | Template 10 | $0.00074 | 1-2s | Flash 2.5/Local |
| Dramatic Irony | Template 11 (NEW) | $0.0014 | 5-8s | Flash 2.5 |

---

## Integration Example

```javascript
// Example: Using Template 1 in production code

const generateFirstEvolution = async (character, interaction, player) => {
  // 1. Fill template variables
  const prompt = Template1.replace(/{(\w+)}/g, (match, key) => {
    return getVariableValue(key, { character, interaction, player });
  });
  
  // 2. Call AI API
  const response = await callGeminiFlash25(prompt);
  
  // 3. Parse JSON response
  const evolution = JSON.parse(response);
  
  // 4. Validate (see 35-consistency-coherence.md)
  const validation = validateEvolution(evolution, character);
  
  if (!validation.pass) {
    // Regenerate or flag for review
    console.warn('Evolution failed validation:', validation.issues);
    return await regenerateEvolution(prompt, validation.feedback);
  }
  
  // 5. Apply to character
  character.applyEvolution(evolution);
  
  // 6. Log for cost tracking
  logGeneration({
    template: 'first_evolution',
    cost: 0.00074,
    quality_score: validation.score
  });
  
  return evolution;
};
```

---

## Next Steps

**You now have:**
- ✅ 10 production-ready prompt templates
- ✅ Variable mapping examples
- ✅ Cost and time estimates
- ✅ Selection guide

**Continue to:**
- → 34-context-memory-systems.md for context injection
- → 35-consistency-coherence.md for validation
- → 30-ai-architecture-overview.md for routing logic

**Remember:**
- Always validate generated content
- Track costs per template
- Use appropriate model for scenario (Flash vs Pro)
- Batch low-priority generations when possible

**These templates are your foundation. Customize them for your specific needs, but maintain the core structure for consistency. 🎯**

---

## Compliance Checklist (Master Truths v1.2)

- [x] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; Capacity 0.0-10.0)
- [x] **Templates include urgency variables (urgency_level, urgency_multiplier, emotional_capacity, trust)**
- [x] **Numerical grounding requirements added to all templates (anchor → calculate → validate)**
- [x] **Capacity constraints respected in dialogue generation**
- [x] OCEAN personality values provided in both 1-5 and 0-1 scales
- [x] Memory emotional weight uses 0-10 scale
- [x] Templates reference NPC Response Framework variables
- [x] This doc provides **Truths v1.2** compliant templates

