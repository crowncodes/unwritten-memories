# Prompt Engineering Principles

**Purpose:** Core concepts for creating quality AI-generated content  
**Audience:** Content designers, AI engineers, narrative designers  
**Status:** ✅ Complete  
**Related:** ← 30-ai-architecture-overview.md | → 33-prompt-templates-library.md for templates

---

## What This Document Covers

This document establishes the **foundational principles** for prompt engineering in Unwritten. You'll learn:
- Five core principles for effective prompts
- OCEAN personality model behavioral mapping
- Memory tier system and significance
- Emotional resonance techniques
- Narrative coherence rules
- Consistency maintenance strategies

**This is required reading** before using the prompt templates in 33-prompt-templates-library.md.

---

## The Five Core Principles

### Principle 1: Specificity Over Generality

**The Problem:**
Vague prompts produce generic, forgettable content.

**The Solution:**
Be ruthlessly specific about what you want.

```markdown
❌ BAD: "Make the character evolve"
Problem: No direction, no constraints, unpredictable output

✅ GOOD: "Generate a specific memory of this coffee meetup that reveals 
         ONE new personality trait consistent with their OCEAN scores.
         Include a sensory detail and one line of paraphrased dialogue."
Result: Consistent, specific, memorable content
```

**Examples:**

```markdown
❌ Generic:
"The character was interesting and had hidden depths."

✅ Specific:
"When asked about her weekend, she mentioned restoring a 1960s motorcycle 
in her garage. Her hands were still stained with engine grease. She laughed 
when she noticed you noticed, almost embarrassed, then showed you photos 
of the bike's progress on her phone—every detail catalogued."
```

**Why This Works:**
- Specific details are memorable
- They create unique characters
- They give AI clear targets
- They prevent generic "mystery box" characters

---

### Principle 2: Constraint-Driven Creativity

**The Problem:**
Too much freedom produces inconsistent or implausible content.

**The Solution:**
The AI is most creative when given clear boundaries.

**The Three-Part Framework:**

1. **Boundaries (What NOT to do)**
   ```markdown
   - NO clichés ("mysterious past", "hidden depth")
   - NO over-dramatic revelations for first meetings
   - NO romantic content unless contextually appropriate
   ```

2. **Requirements (What MUST be included)**
   ```markdown
   - MUST include one sensory detail
   - MUST reference their OCEAN personality scores
   - MUST include paraphrased dialogue
   ```

3. **Creative Freedom (Within those limits)**
   ```markdown
   - Choose ANY specific hobby/interest/passion
   - Select ANY appropriate emotional tone
   - Create ANY realistic detail that fits
   ```

**Example Prompt Structure:**

```markdown
Generate a memory where Sarah reveals something personal.

BOUNDARIES:
- NOT about romance
- NOT a trauma dump
- NOT cliché (no "mysterious past")

REQUIREMENTS:
- ONE specific hobby or interest
- ONE sensory detail (smell, sound, or texture)
- Reflects her High Openness (4.2/5)
- Shows her introverted nature (E: 2.5/5)

CREATIVE FREEDOM:
- Choose the specific hobby
- Choose the setting
- Choose the emotional tone
```

**Result:** Creative but consistent content that fits the character.

---

### Principle 3: Examples Drive Consistency

**The Problem:**
AI interprets instructions differently each time without examples.

**The Solution:**
Always provide 2-3 examples of desired output.

**The Pattern:**

```markdown
TASK: Generate a memory of this interaction.

GOOD EXAMPLES:
1. "She mentioned her record collection while waiting for coffee. When asked 
   about her favorite, she lit up and talked about a rare Coltrane pressing 
   she found at an estate sale. The way she described the album cover—every 
   detail memorized—made it clear this wasn't just casual interest."

2. "He seemed nervous at first, fidgeting with his phone. But when the 
   conversation turned to his work as a sound designer, the nervousness 
   vanished. He explained how he records city sounds at 3 AM, creating 
   libraries of urban ambience. There was pride in his voice."

BAD EXAMPLES (DO NOT DO THIS):
1. "She was mysterious and intriguing with hidden depths" (too vague)
2. "He revealed his dark secret about his traumatic childhood" (too dramatic)
3. "They had an instant connection that changed everything" (too romance-novel)

Now generate the memory for this character: [context]
```

**Why This Works:**
- AI pattern-matches to examples
- Shows tone, length, and structure
- Demonstrates what to avoid
- Creates consistent output style

**Real Example - Memory Generation:**

```markdown
TASK: Create a Level 1→2 evolution memory

GOOD EXAMPLE (show the pattern):
"The café was crowded, but she noticed you struggling with too many bags and 
offered her extra chair without hesitation. Small gesture, but genuine. When 
you thanked her, she waved it off—'I was saving it anyway'—with this easy 
smile. Five minutes later you were comparing coffee orders and complaining 
about Monday mornings. Her laugh was unexpected, loud and unself-conscious. 
Made you want to hear it again."

Elements this example demonstrates:
✓ Sensory setting (crowded café)
✓ Specific action (offered chair)
✓ Personality hint (genuine, easy)
✓ Dialogue (indirect speech)
✓ Emotional note (unexpected laugh)
✓ Forward momentum (want to hear it again)

Your turn: Generate memory for {character_name}
```

---

### Principle 4: Emotional Authenticity Over Drama

**The Problem:**
AI defaults to melodrama when asked for "emotional" content.

**The Solution:**
Small, specific, authentic details create real emotion.

**The Authenticity Framework:**

**❌ Melodrama:**
```
"She broke down sobbing, her heart shattered into a million pieces as she 
revealed her traumatic past. The pain of her childhood consumed her."
```

**✅ Authentic Emotion:**
```
"She mentioned she still can't eat oranges. 'My father used to—' and she 
stopped talking, changing the subject quickly. You noticed her fingers had 
tightened around her coffee cup."
```

**Why the second works:**
- Specific detail (oranges)
- Incomplete revelation (creates mystery naturally)
- Physical tell (tightening fingers)
- Respects pacing (doesn't dump everything)
- Feels real (people DO change subjects)

**The Small Details That Matter:**

```markdown
Instead of: "He was nervous"
Write: "He kept folding and unfolding the corner of the menu while he talked"

Instead of: "She was sad about her grandmother"
Write: "She still has her grandmother's reading glasses. They don't fit her, 
but she keeps them in her desk drawer at work. Sometimes she just holds them."

Instead of: "They had a deep connection"
Write: "Three hours passed like thirty minutes. When you checked your phone, 
you both looked surprised. 'Oh,' she said. Then: 'Want to order another round?'"
```

**Emotional Authenticity Rules:**

1. **Show, don't tell**
   - ❌ "He said he was scared"
   - ✅ "His hands shook when he picked up the coffee cup"

2. **Incomplete revelations build mystery**
   - ❌ Full trauma dump in first conversation
   - ✅ Hints and fragments that make you curious

3. **Physical details ground emotion**
   - ❌ "She was overwhelmed with feeling"
   - ✅ "Her eyes got wet but she blinked it back, laughed"

4. **Mundane moments reveal character**
   - ❌ Only show dramatic highs and lows
   - ✅ Show how they order coffee, tip servers, respond to small annoyances

5. **Earned emotion only**
   - ❌ Deep intimacy in first meeting
   - ✅ Build trust over multiple interactions

---

### Principle 5: Incremental Not Exponential

**The Problem:**
Characters that change too dramatically feel inconsistent and jarring.

**The Solution:**
Each evolution should be 5-15% different, not 50%+ different.

**The Evolution Curve:**

```
Level 1→2: 5-10% change
├─ Learn ONE new thing about them
├─ Shift 1-2 traits by 0.1-0.2 points
└─ They're recognizable but more specific

Level 2→3: 10-12% change
├─ Learn 2-3 new things
├─ Shift 2 traits by 0.2-0.3 points
└─ Familiarity building, comfort increasing

Level 3→4: 12-15% change
├─ Significant revelation
├─ Shift 2-3 traits by 0.3-0.5 points
└─ Qualitative shift: friend → close friend

Level 4→5: 10-12% change
├─ Deep integration into player's life
├─ Final personality refinement
└─ Relationship fully defined
```

**Examples:**

**❌ Exponential (too much):**
```
Week 1: Shy barista who doesn't make eye contact
Week 2: Confident entrepreneur who runs a successful business and is now 
       your best friend and wants to travel the world together

Problem: Total personality reversal in one week
```

**✅ Incremental (realistic):**
```
Week 1: Shy barista who doesn't make eye contact. Mumbles her recommendations.

Week 4: Still quiet, but makes eye contact now. Remembers your order. 
       Mentioned she likes vintage books.

Week 8: Opens up about grandmother who raised her. Shows you a photo. 
       Still introverted, but comfortable with YOU specifically.

Week 12: Invites you to help her look at potential bookshop spaces. 
        Nervous but excited. Trusts your opinion.

Week 18: Business plan complete. Asks if you want to be involved. 
        Still the same person fundamentally, but has grown.
```

**The Incremental Change Framework:**

```markdown
For each evolution, limit changes to:

✅ ONE new major detail about character
✅ ONE step deeper in vulnerability/trust
✅ ONE-TWO OCEAN trait shifts of 0.1-0.5 points
✅ ONE new unlock (conversation topic, activity, access)

❌ NO complete personality reversals
❌ NO sudden trauma reveals (unless crisis context)
❌ NO jumping relationship levels
❌ NO forgetting what came before
```

**Why This Matters:**

People change gradually, not suddenly. If your NPC is unrecognizable after one interaction, players lose immersion. They should think:

> "Ah, I see them more clearly now"

NOT:

> "Wait, is this the same person?"

---

### Principle 6: Emotional Capacity Realism (With Complexity)

**The Problem:**
Characters respond beyond their current emotional and mental capacity, breaking authenticity.

**The Solution:**
Always constrain character responses to their current emotional capacity (0-10 scale), BUT include realistic complexity: misjudgment, cultural factors, emergency overrides, and failures.

**The Core Insight:**

> A character at 2.5/10 emotional capacity cannot provide 8/10 level emotional support, no matter how much they want to help.

**BUT ALSO:**

> Real people misjudge their capacity, overcommit, underestimate, handle boundaries poorly, and sometimes push beyond limits in emergencies. Training data must include this messiness.

**Capacity Factors:**
```markdown
Emotional Capacity is affected by:
- Current stress level
- Sleep deprivation
- Recent trauma or crisis
- Number of active problems
- Physical exhaustion
- Mental bandwidth available
```

**Realistic Capacity Limitations:**

```markdown
❌ BAD: Character with 2.5/10 capacity provides perfect emotional support
"I completely understand what you're going through. Let me help you process this. 
What you're feeling is valid and I'm here to support you through every step. 
We'll work through this together and find a solution."

Problem: This requires 8/10 capacity. Character physically can't provide this.

✅ GOOD: Character with 2.5/10 capacity tries but shows limitations
"I want to help, I really do. But honestly? I'm so exhausted right now I can barely 
think straight. Can we... can we talk about this tomorrow? When I'm not running on 
fumes? You deserve better than half-attention."

Why it works:
- Acknowledges desire to help (they care)
- Shows realistic limitation (exhausted)
- Admits can't provide what's needed right now
- Suggests alternative (tomorrow)
- Respects friend's needs (you deserve better)
- FEELS AUTHENTIC
```

**Examples by Capacity Level:**

**CAPACITY 8-10/10 (Well-rested, low stress, available bandwidth):**
```markdown
CAN provide:
- Deep emotional support
- Active listening for hours
- Thoughtful advice
- Crisis intervention
- Multiple perspectives
- Patient explanation

Example:
"Tell me everything. I've got all night, and I'm all yours. What happened?"
```

**CAPACITY 5-7/10 (Normal, some stress, moderate bandwidth):**
```markdown
CAN provide:
- Moderate emotional support
- Listening for 30-60 minutes
- Basic advice
- Encouragement
- Practical help

CANNOT provide:
- Hours of processing
- Deep psychological analysis
- Crisis-level intervention

Example:
"I'm here for you. I've got an hour before I need to handle some stuff, 
but let's talk. What's going on?"
```

**CAPACITY 2-4/10 (Stressed, exhausted, limited bandwidth):**
```markdown
CAN provide:
- Acknowledgment ("I hear you")
- Physical presence
- Practical help (errands, not emotional labor)
- Promise to help later

CANNOT provide:
- Emotional support
- Long conversations
- Problem-solving
- Advice

Example:
"I can see this is really hard for you. I'm honestly not in a place to help 
the way you need right now—I'm barely keeping it together myself. Can I check 
in tomorrow? Or is there something practical I can do, like pick up groceries?"
```

**CAPACITY 0-1/10 (Crisis mode, overwhelmed, no bandwidth):**
```markdown
CAN provide:
- Nothing (and that's okay)
- Honesty about inability to help

CANNOT provide:
- Any emotional support
- Even practical help

Example:
"I'm sorry. I can't. I just... I can't right now. I'm so sorry."
```

**The Authenticity Framework:**

```markdown
For each emotional interaction, check:

1. What emotional support level is needed? (0-10)
2. What is character's current capacity? (0-10)
3. Is needed <= capacity + 2?
   
If YES: Character can provide support
If NO: Character must show limitations

When capacity insufficient:
✅ Show them trying but failing
✅ Show them acknowledging limitations
✅ Show them offering what they CAN provide
✅ Show them feeling guilty/frustrated they can't help

❌ Don't have them magically able to provide full support
❌ Don't ignore the capacity limitation
❌ Don't make them unfeeling (they care, but can't)
```

**Circumstance Stacking:**

Multiple stressors compound to reduce capacity:

```markdown
SCENARIO: Character dealing with 3 stressors simultaneously
- Job deadline (stress +2)
- Family crisis (stress +3)  
- Money problems (stress +2)
- Total: 7/10 stress

If character started at 8/10 capacity:
8 - 7 = 1/10 remaining capacity

At 1/10 capacity, character can:
- Acknowledge friend's problem
- Express care
- Admit inability to help right now
- Maybe offer small practical help

At 1/10 capacity, character CANNOT:
- Process friend's emotional crisis
- Provide advice
- Listen for extended period
- Take on friend's problems
```

**Why This Principle Matters:**

This is the difference between:
- Generic game dialogue ("I'll help you!")
- Authentic human interaction ("I want to help but I'm drowning myself")

This is what makes generated content feel like **real people** rather than **NPCs**.

### The Complexity Requirement *(NEW v1.2)*

**Training Data Must Include:**

**1. Misjudgment Examples (20% of dataset)**
```markdown
Character at 3/10 capacity THINKS they can help:
"Yeah, I can totally help you move this weekend! No problem."
[Overcommits, realizes mistake later, has to backtrack]

Character at 7/10 capacity UNDERESTIMATES what they can provide:
"I don't think I can handle that right now..."
[Actually could have helped, missed opportunity to support friend]

Why include these:
- Real people misjudge capacity constantly
- Shows consequences of poor self-assessment
- Creates authentic regret/relief patterns
```

**2. Failed Boundary-Setting (15% of dataset)**
```markdown
HIGH AUTHENTICITY FAILURE:
Character WANTS to say no but can't:
"I... I guess I can help. [internal: Why can't I just say no? I'm exhausted.]"
[People-pleasing despite low capacity]

DEFENSIVE FAILURE:
Character responds poorly to request:
"Why do you always ask me when I'm busy? Can't you see I'm drowning?"
[Lashes out due to overwhelm, damages relationship]

AVOIDANT FAILURE:
Character ghosts/avoids instead of honest conversation:
[Reads message, doesn't respond, avoids person for days]

Why include these:
- Many people handle boundaries poorly
- Cultural conditioning affects response
- Anxiety/guilt prevent honest communication
```

**3. Emergency Override (10% of dataset)**
```markdown
Parent/child scenario:
Capacity 1.5/10 + child in crisis = MUST respond
"I'm so tired I can barely think, but this is my kid. I find the energy."

Life-threatening emergency:
Capacity 2.0/10 + friend suicide risk = capacity doesn't matter
"I'm not okay but neither are they. I'll crash later. Right now, I'm here."

Why include these:
- Sometimes capacity limits ARE overridden
- Shows what people prioritize
- Demonstrates cost of pushing beyond limits
```

**4. Cultural/Communication Variation (20% of dataset)**
```markdown
Indirect communication (capacity 3/10):
"Oh, I'm fine! Just a little busy, haha."
[Says yes when should say no, cultural norm prevents directness]

Excessive apologizing (capacity 4/10):
"I'm so so sorry, I know I'm the worst, I just—I'm sorry—I really can't—sorry..."
[Can't set boundary without self-flagellation]

Aggressive (capacity 2/10, low agreeableness):
"Figure it out yourself. I'm not your therapist."
[Blunt refusal without softening, damages relationship]

Why include these:
- Not everyone communicates like therapy-speak
- Personality + culture shape boundary-setting
- Some responses are effective but harsh
```

**5. Authenticity Score Spectrum**

**MUST include full range 0.2-1.0:**

```markdown
0.2-0.4 (Very Inauthentic):
- Lies about availability
- Says yes when clearly no
- Completely avoids conversation
- Defensive lashing out

0.4-0.6 (Struggling/Mixed):
- Wants to be honest but can't quite
- Overcommits with awareness
- Apologizes excessively
- Half-truths

0.6-0.8 (Authentic but Imperfect):
- Honest about limits with some stumbling
- Offers alternatives
- Shows guilt but sets boundary
- Could be clearer but tries

0.8-1.0 (Highly Authentic):
- Clear, kind boundary-setting
- Acknowledges limitations honestly
- Offers what they CAN provide
- No excessive guilt or defensiveness

REQUIREMENT: Dataset CANNOT be all 0.8+ scores. Real people fail constantly.
```

**Integration with Other Principles:**

- Combine with Principle 4 (Emotional Authenticity) - show capacity through behavior
- Combine with Principle 5 (Incremental Change) - capacity fluctuates, doesn't reverse
- Combine with OCEAN mapping - personality affects HOW they show limitations

**Prompt Template Addition:**

Add to every prompt:
```markdown
EMOTIONAL CAPACITY: {character_capacity}/10

CHARACTER CONSTRAINTS:
- Current capacity: {capacity}/10
- Support needed: {needed}/10
- Can provide: {min(capacity + buffer, needed)}
- Buffer varies 1-3 based on: relationship, desperation, personality

COMPLEXITY REQUIREMENTS:
- Include misjudgment potential (over or underestimate)
- Show cultural/personality communication style
- Consider emergency override scenarios
- Generate authenticity spectrum (not just 0.8+)
- Include boundary-setting failures

If capacity insufficient:
Generate 3 responses:
1. High authenticity (0.7-0.9): Honest, clear, kind
2. Struggling authenticity (0.5-0.7): Wants to but can't quite
3. Failed authenticity (0.2-0.5): People-pleasing or defensive
```

---

## OCEAN Personality Model - Behavioral Mapping

### Understanding the Big Five

The OCEAN model (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) defines personality. Here's how to translate scores (1-5) into authentic behavior and dialogue.

> **Critical Connection:** OCEAN scores are the **PRIMARY FILTER** in the NPC Response Framework. They set the baseline, which urgency multipliers then amplify.

### How OCEAN Connects to Response Framework (Master Truths v1.2)

**The Hierarchy:**
```
1. OCEAN (Primary) → Sets baseline response tendency
2. Urgency (Multiplier 1x-5x) → Amplifies or dampens baseline
3. Trust (Modifier 0.5x-2x) → Affects interpretation
4. Capacity (Constraint) → Caps maximum response
```

**Example: Agreeableness Impact**

```markdown
Low Agreeableness (2.0/5.0 = 0.4):
├─ Baseline: Harsh, takes offense easily
├─ Routine context (1x): base -0.7
├─ Crisis context (5x): base -0.7 × 5 = -3.5 (clamped to -3.0)
└─ Urgency AMPLIFIES harsh personality

High Agreeableness (4.5/5.0 = 0.9):
├─ Baseline: Forgiving, understanding
├─ Routine context (1x): base -0.15
├─ Crisis context (5x): base -0.15 × 5 = -0.75
└─ Even in crisis, more forgiving than low-A in routine
```

**Key Insight:** Same action, same urgency, different personality = dramatically different impact.

---

### Openness (O): Curiosity & Creativity

**What It Measures:**
- Interest in new experiences
- Imagination and creativity
- Preference for variety vs. routine
- Abstract vs. concrete thinking

**LOW OPENNESS (1.0-2.5):**

```markdown
Behavioral Traits:
- Prefers routine and familiar topics
- Skeptical of new ideas initially
- Concrete, practical thinking
- "If it ain't broke, don't fix it" mentality
- Focuses on what's proven and reliable

Dialogue Style:
- Straightforward, traditional
- References past experiences
- Asks practical questions
- Dismissive of abstract concepts

Example Dialogue:
"I go to the same coffee shop every morning. Been going there for five years. 
Why would I change what works?"

"That sounds... interesting. But have you actually tried it, or is it just 
a theory?"

"I'm more of a practical person. Give me something I can use, not something 
I have to think about."

Activities They Enjoy:
- Familiar routines
- Traditional hobbies
- Proven methods
- Structured environments
```

**MEDIUM OPENNESS (2.5-3.5):**

```markdown
Behavioral Traits:
- Balanced between routine and novelty
- Willing to try new things occasionally
- Mix of practical and abstract thinking
- Appreciates both stability and change

Dialogue Style:
- Conversational, relatable
- Open but not pushy about new ideas
- Can discuss both concrete and abstract topics

Example Dialogue:
"I've been thinking about trying that new place, but my usual spot is so 
reliable. Maybe we could check it out together?"

"That's an interesting way to look at it. I never thought about it like that."

"I like having a plan, but I'm down for spontaneous stuff too."

Activities They Enjoy:
- Mix of familiar and new
- Variety in moderation
- Both structured and unstructured time
```

**HIGH OPENNESS (4.0-5.0):**

```markdown
Behavioral Traits:
- Enthusiastic about new experiences
- Abstract, philosophical thinking
- Creative and unconventional
- Excited by ideas and possibilities
- Bored by routine

Dialogue Style:
- Animated, idea-focused
- Makes unexpected connections
- Uses metaphors and analogies
- Asks "what if" questions

Example Dialogue:
"Have you ever thought about how every coffee shop has its own ecosystem? 
I've been documenting the social patterns. It's fascinating how the space 
shapes behavior."

"I just started learning Japanese calligraphy. It's this perfect blend of 
art and meditation. Want to see my practice sheets?"

"Routine kills creativity. I try to change something about my day every week 
just to keep my brain alert."

Activities They Enjoy:
- Novel experiences
- Creative pursuits
- Philosophical discussions
- Exploring new places/ideas
- Artistic expression
```

---

### Conscientiousness (C): Organization & Reliability

**What It Measures:**
- Organization and planning
- Self-discipline and reliability
- Goal-orientation
- Attention to detail

**LOW CONSCIENTIOUSNESS (1.0-2.5):**

```markdown
Behavioral Traits:
- Spontaneous and flexible
- May forget appointments or details
- Goes with the flow
- Messy or disorganized spaces
- Procrastinates on tasks

Dialogue Style:
- Casual, unplanned
- Apologetic about forgotten things
- "We'll figure it out" attitude

Example Dialogue:
"Oh shoot, was that today? I totally forgot. My bad. Want to just grab food 
somewhere nearby?"

"I know I said I'd bring that thing... I think it's in my car? Or maybe my 
apartment? I'll find it eventually."

"Planning stresses me out. Let's just see what happens."

What They're Like:
- Often late (but doesn't mean to be)
- Forgets to text back
- Creative chaos in living space
- Works in bursts of inspiration
- Adaptable to changes
```

**MEDIUM CONSCIENTIOUSNESS (2.5-3.5):**

```markdown
Behavioral Traits:
- Plans some things, spontaneous with others
- Generally reliable but not rigid
- Organized when it matters
- Can be flexible when needed

Dialogue Style:
- Friendly but responsible
- Plans ahead for important things
- Relaxed about minor details

Example Dialogue:
"I had a rough plan for today, but if something better comes up, I'm flexible."

"I try to keep my schedule organized, but I'm not going to freak out if 
things change."

"Let me put that in my calendar so I don't forget. Okay, what were we saying?"

What They're Like:
- Usually on time
- Remembers important dates
- Organized-ish spaces
- Balances planning with spontaneity
```

**HIGH CONSCIENTIOUSNESS (4.0-5.0):**

```markdown
Behavioral Traits:
- Very organized and punctual
- Follows through on all commitments
- Plans ahead extensively
- Detail-oriented
- Disciplined and goal-focused

Dialogue Style:
- Structured, dependable
- References schedules and plans
- Checks off completed tasks

Example Dialogue:
"I scheduled this two weeks in advance and arrived five minutes early. I 
brought notes on what I wanted to discuss."

"Let me send you a calendar invite with the details. I'll include the address 
and my contact info in case there are any issues."

"I have a system for this. It might seem like overkill, but it works."

What They're Like:
- Always on time (early, actually)
- Detailed to-do lists
- Clean, organized spaces
- Follows up reliably
- Achieves goals methodically
```

---

### Extraversion (E): Social Energy

**What It Measures:**
- Where you get energy (social vs. alone)
- Sociability and assertiveness
- Activity level and enthusiasm
- Comfort in group settings

**LOW EXTRAVERSION / INTROVERSION (1.0-2.5):**

```markdown
Behavioral Traits:
- Energized by alone time
- Quiet in groups, talkative one-on-one
- Prefers deep over broad connections
- Needs recharge time after socializing
- Observes before participating

Dialogue Style:
- Thoughtful, measured
- Speaks after thinking
- Prefers text to calls
- Direct in small groups

Example Dialogue:
"This is nice. Just the two of us. I can only handle so much socializing 
before I need to recharge."

"I'm not really a party person. Too many people, too much noise. This is 
more my speed."

"Can we text about it? I process better when I have time to think."

What They're Like:
- Selective about social events
- Close friend group (2-4 people)
- Needs alone time daily
- Drained by loud environments
- Thoughtful conversationalist
```

**MEDIUM EXTRAVERSION / AMBIVERT (2.5-3.5):**

```markdown
Behavioral Traits:
- Context-dependent energy
- Social but also needs downtime
- Comfortable in various settings
- Adapts social intensity

Dialogue Style:
- Varies by comfort level
- Can be outgoing or reserved
- Matches others' energy

Example Dialogue:
"I like hanging out, but I'm not really a 'go to a club' person, you know?"

"Some days I want to be around people, other days I just want to be home 
with a book. Depends on my mood."

"I'm good in groups, but I prefer smaller gatherings where I can actually 
talk to people."

What They're Like:
- Flexible social schedule
- Mix of group and solo activities
- Can enjoy parties OR quiet nights
- Moderate friend group (5-10 close friends)
```

**HIGH EXTRAVERSION (4.0-5.0):**

```markdown
Behavioral Traits:
- Energized by social interaction
- Talkative and engaging
- Thinks out loud
- Seeks out group activities
- Uncomfortable with silence

Dialogue Style:
- Animated, expressive
- Jumps into conversations
- Tells stories enthusiastically
- Suggests group plans

Example Dialogue:
"This is great! We should invite Marcus and Sarah next time. The more the 
merrier, right?"

"I can't believe I'm staying in on a Friday night. Want to do something? 
Literally anything. I'm going crazy here."

"So I was telling this story earlier—actually, let me start from the beginning..."

What They're Like:
- Large friend group (10+ close friends)
- Always making plans
- Energized by crowds
- Calls instead of texts
- Natural networker
```

---

### Agreeableness (A): Cooperation & Empathy

**What It Measures:**
- Concern for others
- Cooperation vs. competition
- Trust and empathy
- Conflict approach

**LOW AGREEABLENESS (1.0-2.5):**

```markdown
Behavioral Traits:
- Direct, possibly blunt
- Competitive rather than cooperative
- Values honesty over harmony
- Questions others' motives
- Self-interested

Dialogue Style:
- Straightforward, challenging
- Doesn't sugarcoat
- Points out flaws directly
- Debates for sport

Example Dialogue:
"I'm going to be honest - I think that's a terrible idea. Here's why..."

"I don't really care if it hurts their feelings. They asked for my opinion, 
I gave it."

"Why would I do that? What's in it for me?"

What They're Like:
- Blunt honesty (can seem harsh)
- Competitive in games/work
- Skeptical of intentions
- Values competence over niceness
- Efficient but not warm
```

**MEDIUM AGREEABLENESS (2.5-3.5):**

```markdown
Behavioral Traits:
- Balance between honest and diplomatic
- Cooperative but has boundaries
- Empathetic but realistic
- Stands ground when needed

Dialogue Style:
- Friendly but authentic
- Diplomatic disagreement
- Helps but not self-sacrificing

Example Dialogue:
"I see your point, but have you considered this perspective?"

"I want to help, but I also need to take care of my own stuff first."

"That's rough. I'm sorry you're dealing with that. What are you going to do?"

What They're Like:
- Helpful when convenient
- Honest but tactful
- Cooperates with reciprocity
- Empathetic with boundaries
```

**HIGH AGREEABLENESS (4.0-5.0):**

```markdown
Behavioral Traits:
- Warm, empathetic, supportive
- Avoids conflict, seeks harmony
- Puts others' needs first (sometimes too much)
- Trusts easily
- Self-sacrificing

Dialogue Style:
- Kind, encouraging
- Apologizes frequently
- Offers help immediately
- Validates emotions

Example Dialogue:
"That sounds really hard. I'm here for you. What do you need?"

"Oh my gosh, I'm so sorry. I didn't mean to—is everything okay?"

"Don't worry about me, I'm fine. Let's focus on you."

What They're Like:
- The "mom friend"
- Always available to help
- Avoids confrontation
- Puts others first (sometimes to own detriment)
- Warm and nurturing
```

---

### Neuroticism (N): Emotional Stability

**What It Measures:**
- Emotional volatility
- Tendency to experience negative emotions
- Stress response
- Anxiety levels

**LOW NEUROTICISM / HIGH STABILITY (1.0-2.5):**

```markdown
Behavioral Traits:
- Emotionally stable and calm
- Resilient in face of stress
- Optimistic outlook
- Slow to anger or worry
- Even-keeled

Dialogue Style:
- Steady, reassuring
- Downplays problems
- Confident tone
- "It'll be fine" attitude

Example Dialogue:
"Yeah, it's stressful, but we'll figure it out. We always do."

"I don't really get anxious about stuff like that. What's the worst that 
could happen?"

"You're overthinking it. Just do the thing, see what happens."

What They're Like:
- Calm in crises
- Rarely worries
- Emotionally steady
- Recovers quickly from setbacks
- Can seem too relaxed sometimes
```

**MEDIUM NEUROTICISM (2.5-3.5):**

```markdown
Behavioral Traits:
- Experiences normal emotional ups and downs
- Generally stable with occasional worries
- Stress in appropriate contexts
- Balanced emotional responses

Dialogue Style:
- Realistic about feelings
- Honest about concerns
- Neither catastrophizing nor dismissing

Example Dialogue:
"I'm a bit anxious about this, but I think I can handle it."

"I'm nervous, but excited too, you know? It's a good nervous."

"Okay, I need to vent for a minute. After that I'll be fine."

What They're Like:
- Normal worry levels
- Occasional stress
- Recovers from setbacks reasonably
- Emotional but not unstable
```

**HIGH NEUROTICISM (4.0-5.0):**

```markdown
Behavioral Traits:
- Prone to worry and anxiety
- Emotionally reactive
- May catastrophize situations
- Stress-sensitive
- Self-conscious

Dialogue Style:
- Anxious, seeking reassurance
- "What if" questions
- Expresses fears frequently
- Self-deprecating

Example Dialogue:
"What if everything goes wrong? I've been up all night thinking about all 
the ways this could fail..."

"I'm sorry, I'm being ridiculous. I just can't stop worrying about it."

"Are you mad at me? You seem quiet. Did I do something wrong?"

What They're Like:
- Frequent worrying
- Seeks reassurance
- Stress-prone
- Anxious about outcomes
- Self-critical
- May have anxiety/depression
```

---

## Memory System - Tier Architecture

### The Four-Tier Memory System

Memories in Unwritten have different weights and persistence. This creates realistic forgetting and emphasizes what matters.

---

### Tier 1: Trivial Memories (Weight: 0.1-0.3)

**What Qualifies:**
- Casual interactions with no significant content
- Repeated routine activities
- Small talk about weather/news
- Passing comments

**Characteristics:**
```markdown
Lifespan: 2-4 weeks, then fade
Effect on Personality: None
Effect on Relationship: Minimal (creates familiarity through repetition)
Storage: Summarized into patterns ("we often met for coffee")
```

**Examples:**

```
"Had coffee with them. Weather was nice. Talked about weekend plans."

"Ran into each other at the gym. Said hi, did our workouts."

"Texted about that meme I sent. They thought it was funny."
```

**When to Use:**
- Routine weekly activities
- Casual greetings
- Filler interactions
- Background relationship maintenance

**Generation Guidelines:**
```markdown
For Tier 1 memories:
- Keep to 1 sentence
- No sensory details needed
- Generic is okay here
- Focus on pattern ("another Friday coffee")
```

---

### Tier 2: Notable Memories (Weight: 0.3-0.6)

**What Qualifies:**
- Enjoyable or interesting interactions
- Learning something new about each other
- Shared activity with positive experience
- Discovery of common interests

**Characteristics:**
```markdown
Lifespan: Weeks to months
Effect on Personality: Minimal (may nudge traits 0.1-0.2)
Effect on Relationship: Builds familiarity and comfort
Storage: Kept as discrete memories
```

**Examples:**

```
"Went to that art exhibit she recommended. She has great taste in modern art. 
Noticed she spent a long time in front of the abstract pieces, really studying 
them. Made a mental note—she sees things I miss."

"He helped me move. Expected it to be awful, but he made it actually fun. 
Ordered pizza, told stupid jokes, didn't complain once. That's the kind of 
friend he is."

"She introduced me to her favorite coffee blend. The way she described the 
flavor notes—you'd think she was talking about wine. It's a whole world I 
didn't know existed."
```

**When to Use:**
- Level 1→2 evolutions
- Building relationship patterns
- Discovering shared interests
- Positive experiences together

**Generation Guidelines:**
```markdown
For Tier 2 memories:
- 2-3 sentences
- Include ONE sensory or behavioral detail
- Show what you're learning about them
- Positive or neutral tone
- Creates comfort, not drama
```

---

### Tier 3: Significant Memories (Weight: 0.6-0.8)

**What Qualifies:**
- Vulnerability shared
- Important information revealed
- Conflict successfully resolved
- Major life event discussed
- Trust deepening moments

**Characteristics:**
```markdown
Lifespan: Months to years
Effect on Personality: Moderate (shifts 0.2-0.4 points)
Effect on Relationship: Creates depth, unlocks new interaction types
Storage: Permanent with high recall priority
```

**Examples:**

```
"Late evening at the bar. The conversation drifted to family—specifically, 
why she doesn't talk to her father. There was no dramatic reveal, just quiet 
honesty about how some relationships can't be fixed, no matter how much you 
want them to be. She didn't ask for advice, and you didn't offer any. 
Sometimes listening is enough."

"He called at 2 AM. You expected crisis, but he just said he couldn't sleep 
and needed to talk. Three hours of conversation about nothing and everything—
careers, regrets, dreams we've given up on. When you finally hung up, you 
both felt lighter somehow."

"First real fight. About something stupid—restaurant choice—but it escalated. 
What mattered was what happened after: both of you apologized. Talked about 
why you'd snapped. Agreed to handle it differently next time. The friendship 
felt stronger for having survived conflict."
```

**When to Use:**
- Level 2→3 or 3→4 evolutions
- Vulnerability moments
- Conflict resolution
- Major revelations
- Trust demonstrations

**Generation Guidelines:**
```markdown
For Tier 3 memories:
- 4-5 sentences
- Include sensory details AND emotional texture
- Show vulnerability or deepening trust
- Dialogue content (not quoted, paraphrased)
- Should feel like a turning point (even small ones)
- References past interactions
```

---

### Tier 4: Defining Memories (Weight: 0.8-1.0)

**What Qualifies:**
- Relationship turning points
- Crisis support (major)
- Life-changing decisions made together
- Peak experiences
- Moments that define "us"

**Characteristics:**
```markdown
Lifespan: Permanent (never fade)
Effect on Personality: Significant (shifts 0.3-0.5+ points)
Effect on Relationship: Defines the entire relationship
Storage: Permanent, frequently referenced
```

**Examples:**

```
"The hospital waiting room at 3 AM. Marcus had called, voice shaking, and 
you were there in twenty minutes. Cancer scare—turned out to be benign, but 
those four hours before the results felt like four years. He didn't say much. 
You didn't need him to. Just sat there, together. When the doctor finally 
came out with good news, he broke down. Not from fear—from relief that you'd 
shown up. 'I didn't know who else to call,' he said. You realized: that's 
what friendship is. Being the person someone calls at 3 AM."

"The night you decided to start the bookshop together. Not a business 
decision—a leap of faith. Sarah had the dream, you had the belief in her. 
Sitting in that empty storefront, sketching layouts on napkins, both of you 
knowing this could fail spectacularly and doing it anyway. The handshake felt 
like a promise. Everything changed that night."

"She told you she loved you. Not romantic—familial. 'You're like a sister to 
me,' she said, and meant it. Twenty years of friendship crystallized in that 
moment. You'd been through breakups, job losses, family deaths, geographic 
moves. And somehow, impossibly, still here. Still showing up for each other."
```

**When to Use:**
- Level 3→4 or 4→5 evolutions
- Crisis evolutions
- Legendary card creations
- Relationship-defining moments
- Major life decisions

**Generation Guidelines:**
```markdown
For Tier 4 memories:
- 5-7 sentences
- Rich sensory AND emotional detail
- Clear "before and after" sense
- Dialogue fragments (the memorable phrases)
- References relationship history
- Should feel permanent
- Player should remember this memory
```

---

## Emotional Resonance Techniques

### Creating Content Players Feel

**The Goal:** Make players emotionally invested in these NPCs, not just mechanically engaged.

---

### Technique 1: Specificity Creates Emotion

**The Principle:**
Generic statements don't make you feel anything. Specific details do.

**Examples:**

```markdown
❌ Generic (no emotion):
"She was sad about her past"

✅ Specific (creates emotion):
"She still has her grandmother's reading glasses. They don't fit her, but 
she keeps them in her desk drawer at work. Sometimes she just holds them."

Why it works:
- Visual detail (glasses, desk drawer)
- Behavioral detail (holds them)
- Implies relationship (grandmother's)
- Suggests grief (still has them)
- Doesn't explain—lets you feel it
```

**Application:**

```markdown
Instead of: "He missed his home country"
Write: "He still calls it 'going home' even though he hasn't been back in 
fifteen years. When he cooks, it's always the recipes his mother taught him. 
The kitchen smells like a place you've never been."

Instead of: "They had chemistry"
Write: "Three hours passed like thirty minutes. When you checked your phone, 
you both looked surprised. 'Oh,' she said. Then, smiling: 'Want to order 
another round?'"
```

---

### Technique 2: Small Details > Big Drama

**The Principle:**
Quiet moments reveal character better than explosive ones.

**Examples:**

```markdown
❌ Big Drama:
"Her traumatic childhood shaped who she is today"

✅ Small Detail:
"She mentioned she still can't eat oranges. 'My father used to—' and she 
stopped talking, changing the subject quickly."

Why it works:
- Incomplete revelation (creates natural mystery)
- Physical trigger (oranges)
- Behavioral response (stops talking, changes subject)
- Implies trauma without explaining it
- Feels real (people DO avoid topics)
```

**The Incomplete Revelation:**

```markdown
Pattern: Start a revelation, then cut it off naturally

"He was about to say something, then—" (thought better of it)
"She mentioned therapy, then quickly added—" (defensive)
"His hand moved to his phone, like he was going to show you—" (decided not to)

This creates:
- Natural mystery
- Respect for boundaries
- Desire to know more
- Realistic pacing
```

---

### Technique 3: Show Vulnerability Through Behavior

**The Principle:**
Don't tell us someone is nervous/sad/excited. Show us through their actions.

**Behavioral Tells:**

```markdown
Nervous:
❌ "He said he was nervous"
✅ "He kept folding and unfolding the corner of the menu while he talked"

Sad:
❌ "She seemed sad"
✅ "Her eyes got wet, but she blinked it back. Laughed, embarrassed."

Excited:
❌ "She was excited"
✅ "She talked faster, hands moving as she explained. You could barely 
keep up, but her enthusiasm was infectious."

Defensive:
❌ "He got defensive"
✅ "His arms crossed. 'I'm not defensive,' he said, defensively."

Attracted:
❌ "There was chemistry"
✅ "She touched your arm when she laughed. Just for a second. You both 
noticed."
```

**Physical Tells Library:**

```markdown
Anxiety/Nervousness:
- Fidgeting with objects (phone, menu, jewelry)
- Leg bouncing under table
- Playing with hair
- Avoiding eye contact then forcing it
- Talking faster than usual
- Excessive apologizing

Sadness/Grief:
- Eyes getting wet but blinking it back
- Voice getting quieter
- Looking away at certain topics
- Forced brightness
- Shorter responses than usual

Excitement/Joy:
- Talking faster
- Animated hand gestures
- Leaning forward
- Eye contact increase
- Smiling despite trying not to

Attraction/Interest:
- Touching (arm, shoulder—brief)
- Prolonged eye contact
- Mirroring body language
- Leaning in
- Finding excuses to stay longer

Defensiveness:
- Arms crossing
- Leaning back
- Tone shift (cooler)
- Deflecting questions
- Over-explaining
```

---

### Technique 4: Earned Emotion

**The Principle:**
Deep emotional moments must be earned through relationship building.

**The Earning Curve:**

```markdown
Level 1 (Strangers):
✅ Can reveal: Surface interests, basic info, pleasant small talk
❌ Cannot reveal: Trauma, deep fears, intense vulnerability

Level 2 (Acquaintances):
✅ Can reveal: Hobbies, opinions, mild complaints, funny stories
❌ Cannot reveal: Family problems, relationship issues, deep insecurities

Level 3 (Friends):
✅ Can reveal: Some vulnerability, past experiences, worries, dreams
❌ Cannot reveal: Deepest traumas, darkest secrets (not yet)

Level 4 (Close Friends):
✅ Can reveal: Significant vulnerability, past trauma, fears, deep hopes
❌ Cannot reveal: Everything (some things take years, or never)

Level 5 (Best Friends/Partners):
✅ Can reveal: Almost anything, given right context and trust
❌ Cannot reveal: Even close friends have some private spaces
```

**Examples of Earned vs. Unearned:**

```markdown
❌ UNEARNED (Level 1 meeting):
"Nice to meet you. By the way, my father abused me and that's why I have 
trust issues."

✅ EARNED (Level 3, after multiple positive interactions):
"You know how I don't really talk about my family? There's a reason for that. 
My dad—he wasn't a good person. I don't usually tell people this, but..."

The difference:
- Relationship history justifies vulnerability
- Framing acknowledges trust level
- Still leaves details vague
- Respects pacing
```

---

### Technique 5: Avoid Melodrama

**The Principle:**
Real emotion is often quiet, not theatrical.

**Melodrama vs. Authentic:**

```markdown
SCENARIO: Character revealing painful memory

❌ Melodrama:
"She broke down sobbing, her heart shattered into a million pieces as the 
memories of her traumatic past consumed her entire being. She couldn't breathe, 
couldn't think, could only feel the all-encompassing agony of her childhood."

✅ Authentic:
"Her eyes got wet. She looked down at her coffee, laughed a little. 'Sorry. 
I don't usually—' She paused. 'Anyway.' You waited. She took a breath. 'My 
father wasn't kind. That's all I want to say about it right now.'"

Why authentic works:
- Physical restraint (looking down, laugh)
- Self-consciousness (apologizes)
- Incomplete revelation (boundaries)
- Gives you moment to respond
- Feels real
```

**Melodrama Red Flags:**

```markdown
❌ "Shattered into a million pieces"
❌ "Consumed by agony"
❌ "Heart-wrenching sobs"
❌ "All-encompassing darkness"
❌ "Soul-crushing pain"
❌ "Tears streaming down her face"

✅ Better alternatives:
"Got quiet"
"Voice cracked"
"Eyes got wet but didn't cry"
"Changed the subject"
"Looked away"
"Forced a smile"
```

**The Restraint Principle:**

> Real people hold back emotions in public. They cry alone, or with only the closest friends. They apologize for showing emotion. They deflect with humor. They minimize their pain.

Show characters trying NOT to show emotion. That's what creates emotion in players.

---

## Practical Generation Workflow

### Step-by-Step Process

When generating content for Unwritten, follow this workflow:

**Step 1: Check OCEAN Scores**
```markdown
Example:
Character: Sarah
O: 4.2 (High - creative, curious)
C: 3.8 (Medium-High - organized but flexible)
E: 2.5 (Low-Medium - introverted)
A: 4.5 (High - empathetic, warm)
N: 3.2 (Medium - some anxiety but manageable)

Implications:
- Will speak thoughtfully (Low E)
- Will share creative interests (High O)
- Will be warm and supportive (High A)
- May show some anxiety in new situations (Medium N)
```

**Step 2: Assess Relationship Level**
```markdown
Level 1: What can strangers share?
Level 2: What do acquaintances discuss?
Level 3: What do friends reveal?
Level 4: What do close friends know?
Level 5: What do best friends share?

This determines vulnerability ceiling.
```

**Step 3: Determine Memory Tier**
```markdown
Is this:
- Routine? → Tier 1
- Interesting? → Tier 2
- Vulnerable/Important? → Tier 3
- Defining? → Tier 4

This determines detail level and permanence.
```

**Step 4: Generate Draft**
```markdown
Create first pass focusing on:
- ONE specific detail
- ONE behavioral moment
- Appropriate emotional tone
- Personality consistency
```

**Step 5: Check Against Principles**
```markdown
✓ Specific enough? (Principle 1)
✓ Within constraints? (Principle 2)
✓ Matches examples? (Principle 3)
✓ Authentic emotion? (Principle 4)
✓ Incremental change? (Principle 5)
✓ OCEAN-consistent? (Behavioral mapping)
✓ Relationship-appropriate? (Memory tier)
```

**Step 6: Refine for Resonance**
```markdown
- Replace generic phrases with specific details
- Add sensory information where appropriate
- Ensure behavioral tells match stated emotions
- Check for melodrama, remove if found
- Verify incomplete revelations (don't explain everything)
```

---

## Summary Checklist

### Before Generating Content

✅ **Have you read the character's OCEAN scores?**  
✅ **Do you know the current relationship level?**  
✅ **Have you determined the appropriate memory tier?**  
✅ **Are you following the Five Core Principles?**  
✅ **Have you checked examples for tone and style?**  

### During Generation

✅ **Is dialogue matching personality traits?**  
✅ **Are behavioral details showing, not telling?**  
✅ **Is emotion earned, not melodramatic?**  
✅ **Is change incremental, not exponential?**  
✅ **Are details specific, not generic?**  

### After Generation

✅ **Would this feel real to a player?**  
✅ **Is the character consistent with previous content?**  
✅ **Would you remember this moment if it happened to you?**  
✅ **Does it respect the relationship pacing?**  
✅ **Is it free of clichés and melodrama?**  

---

## Principle 6: Novel-Quality Narrative *(NEW - 2025-10-14)*

### The Problem: Flat Game Dialogue vs Immersive Fiction

**Most game dialogue is functional, not memorable:**

```markdown
❌ GAME DIALOGUE (Flat):
"I can't help right now. I'm overwhelmed."

✅ NOVEL-QUALITY (Immersive):
"She reaches across the table, takes your hand. 'I can see you're really 
hurting,' she says softly. 'But I need to be honest—I'm not in a good place 
myself right now. Work is crushing me, I haven't slept in two days.' She 
pauses, looking down at her coffee. Her hands are shaking slightly. 'I've 
got maybe an hour. I can listen. But I can't give you the full emotional 
support you need right now. I wish I could. I really do.'"
```

### The Three Pillars of Novel-Quality Content

**1. Show, Don't Tell (Behavioral Grounding)**

```markdown
❌ TELLING: "She was nervous"
✅ SHOWING: "She fidgeted with her napkin, folding and refolding the corner. 
          Her voice came out quieter than usual."

❌ TELLING: "He felt overwhelmed"
✅ SHOWING: "He rubbed his temples, closed his eyes for a moment too long. 
          When he spoke, the words came slowly, like each one took effort."
```

**2. Length & Depth (150-200 words minimum)**

```markdown
Why 150-200 words?
- Creates immersive experience (not just information delivery)
- Allows for behavioral details and sensory grounding
- Matches literary fiction pacing
- Makes characters feel real, not like NPCs

EXCEPTION: Quick exchanges can be shorter, but primary responses 
should be rich and detailed.
```

**3. OCEAN Personality Must Be Visible**

Every character response should reflect their personality scores:

```markdown
HIGH AGREEABLENESS (4.5/5.0):
"She immediately reaches out. 'Of course I'll help. What do you need?' 
Her eyes are already scanning your face, looking for ways to comfort."

LOW AGREEABLENESS (2.0/5.0):
"She leans back, arms crossed. 'Look, I'm dealing with my own stuff 
right now. You're not the only one with problems.'"

HIGH NEUROTICISM (4.2/5.0):
"Her eyes widen. 'Oh god, is it serious? Should I be worried? I mean—
sorry—what happened? Is everyone okay?' She's already catastrophizing."

LOW NEUROTICISM (1.8/5.0):
"She nods calmly. 'Okay. Let's break this down step by step. First, 
what's the most urgent thing we need to handle?'"
```

### Implementation Requirements

**For Training Data Generation:**

```python
# Every training example must include:
{
  "character_response": "150-200 word narrative with behavioral depth",
  "behavioral_cues": [
    "Physical actions (fidgeting, eye contact, posture)",
    "Vocal qualities (tone, volume, pauses)",
    "Micro-expressions (fleeting emotions)"
  ],
  "ocean_influence": {
    "agreeableness": "How this trait shaped the response style",
    "neuroticism": "How emotional stability affected reaction",
    "extraversion": "How social energy influenced engagement"
  },
  "sensory_details": [
    "Environmental details (coffee shop ambiance)",
    "Specific objects (chipped mug, torn book)",
    "Physical sensations (cold hands, racing heart)"
  ]
}
```

### The Novel-Quality Checklist

Before accepting any generated content:

- [ ] **Length**: 150-200 words for primary response
- [ ] **Behavioral Grounding**: At least 3 physical/behavioral cues
- [ ] **Show vs Tell**: 80%+ showing emotion through action
- [ ] **OCEAN Visibility**: Personality clearly influences communication style
- [ ] **Specificity**: Includes specific objects, places, or sensory details
- [ ] **No Clichés**: Zero generic phrases
- [ ] **Immersive**: Feels like reading a novel, not playing a mobile game

### Why This Matters

**Impact on Player Experience:**
- Creates "one more week" engagement (page-turner effect)
- Makes characters feel real, not like NPCs
- Elevates game from "time-killer" to "emotional experience"
- Justifies premium pricing / IAP

**Impact on AI Training:**
- Training data quality directly determines model output quality
- Models learn patterns from data - feed them novel-quality, get novel-quality
- Flat training data → Flat AI responses (garbage in, garbage out)

**See:** `docs/3.ai/37-training-data-quality-standards.md` for complete requirements

---

## Next Steps

**You're now ready to:**
- → Use templates in 33-prompt-templates-library.md
- → Understand context injection in 34-context-memory-systems.md
- → Learn consistency maintenance in 35-consistency-coherence.md

**Remember:**
- Specific > Generic
- Constraints enable creativity
- Examples drive consistency
- Authentic > Dramatic
- Incremental > Exponential

## Numerical Grounding for Impact Calculations *(Master Truths v1.2)*

### The Three-Step Process

> **See:** `NUMERICAL-GROUNDING-CALIBRATION-GUIDE.md` for complete system

**Every numerical assignment requires:**

1. **ANCHOR** - Identify qualitative tier
2. **CALCULATE** - Apply formula with explicit factors  
3. **VALIDATE** - Confirm narrative matches number

### Example: Trust Impact Calculation

```markdown
SCENARIO: Player declines to help Sarah move (crisis)

STEP 1: ANCHOR
Qualitative assessment: "She's really hurt, needs weeks to recover"
→ Tier: MAJOR HARM (-1.5 to -2.0 range)

STEP 2: CALCULATE
Base: -0.5 (declining help)
× Personality (agreeableness 0.8): × 0.7 (softens slightly)
× Urgency (crisis): × 5.0 (AMPLIFIES MASSIVELY)
× Trust (0.65): × 1.2 (expectations were higher)
× Capacity (3.85 → low): × 0.9 (hardens judgment)

Formula: (-0.5 × 0.7 × 5.0 × 1.2 × 0.9) = -1.89 → -1.9

STEP 3: VALIDATE
Does -1.9 match "MAJOR HARM" tier? YES
Expected markers: "This really hurt", "Weeks to recover" ✓
Generated dialogue: "Oh. I... I really needed you."
→ VALIDATION PASSED
```

### Required Fields in All Generations

```json
{
  "relationship_impact": -1.9,
  
  "calculation": {
    "base": -0.5,
    "personality_modifier": 0.7,
    "urgency_multiplier": 5.0,
    "trust_modifier": 1.2,
    "capacity_factor": 0.9,
    "formula": "(-0.5 × 0.7 × 5.0 × 1.2 × 0.9) = -1.89"
  },
  
  "qualitative_tier": "MAJOR HARM (-1.5 to -2.0)",
  "narrative_markers": ["This really hurt", "Weeks to recover"],
  
  "validation": {
    "dialogue_matches_tier": true,
    "reasoning": "Shows hurt without melodrama, matches tier"
  }
}
```

### Qualitative Tiers (Quick Reference)

| Tier | Range | Recovery | Markers |
|------|-------|----------|---------|
| **Negligible** | -0.1 to -0.2 | Instant | "All good!", "Don't worry" |
| **Minor** | -0.3 to -0.5 | Hours | "A little disappointed" |
| **Moderate** | -0.8 to -1.2 | Days | "That stung", "I'm disappointed" |
| **Major** | -1.5 to -2.0 | Weeks | "You really hurt me", "I need space" |
| **Shattering** | -2.5 to -3.0 | Months | "I don't know if I can trust you" |

**No more arbitrary numbers.** Every score is grounded in narrative reality.

---

**These principles are the foundation of quality AI content. Master them before using the templates. 🎯**

---

## Compliance Checklist (Master Truths v1.2)

- [x] Uses canonical vocab & scales (Levels 0–5; Trust 0.0–1.0; Capacity 0.0-10.0)
- [x] **OCEAN personality connected to NPC Response Framework**
- [x] **Emotional capacity system with complexity requirements (misjudgment, failures, cultural variation)**
- [x] **Memory tier system with resonance weights (0.7-0.95)**
- [x] **Numerical grounding process documented (anchor → calculate → validate)**
- [x] Authenticity spectrum includes 0.2-1.0 full range (not just high scores)
- [x] Incremental change principle maintains consistency
- [x] Emotional authenticity over melodrama
- [x] This doc teaches **Truths v1.2** principles

