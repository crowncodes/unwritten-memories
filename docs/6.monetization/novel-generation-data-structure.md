# Premium Novel Generation: Comprehensive Data Structure

## Overview

This data structure provides an LLM with everything needed to generate one chapter of literary-quality fiction while maintaining perfect continuity, avoiding contradictions, and implementing sophisticated literary techniques.

---

## 1. Master Story Context (Always Provided)

```typescript
interface MasterStoryContext {
  story_metadata: {
    title: string;
    themes: string[];                // ["courage", "becoming", "belief"]
    tone: string;                    // "hopeful_introspective_authentic"
    pov_style: "second_person" | "first_person" | "close_third";
    time_span: { start: string; end: string; total_duration: string };
  };
  
  // Immutable truths established in previous chapters
  established_facts: Array<{
    fact: string;
    week: number;
    importance: "critical" | "significant" | "detail";
  }>;
  
  // Character registry with voice patterns
  character_registry: CharacterProfile[];
  
  // Story arc status
  story_arcs: StoryArcSummary[];
  
  // What happened in previous chapters
  previous_chapters: ChapterSummary[];
}
```

---

## 2. Chapter Generation Packet (Per Chapter)

```typescript
interface ChapterGenerationPacket {
  // CHAPTER IDENTITY
  chapter_metadata: ChapterMetadata;
  
  // MASTER CONTEXT (prevents contradictions)
  master_context: MasterStoryContext;
  
  // THIS CHAPTER'S NARRATIVE
  chapter_narrative: ChapterNarrative;
  
  // ALL POV PERSPECTIVES (for this chapter)
  pov_perspectives: POVPerspective[];
  
  // LITERARY TECHNIQUE GUIDANCE
  technique_guidance: TechniqueGuidance;
  
  // CONTINUITY ANCHORS
  continuity_anchors: ContinuityAnchors;
  
  // FORESHADOWING SEEDS
  foreshadowing: ForeshadowingHints[];
}
```

### 2.1 Chapter Metadata

```typescript
interface ChapterMetadata {
  chapter_number: number;
  title: string;                     // "The Day Sarah Almost Quit"
  weeks_covered: number[];           // [32, 33]
  primary_pov: string;               // Character ID
  secondary_povs?: string[];         // Optional POV shifts within chapter
  
  act_placement: {
    act: 1 | 2 | 3;
    position_in_act: "early" | "middle" | "late";
    narrative_function: string;      // "Setup conflict" | "Escalate tension" | "Climax"
  };
  
  chapter_purpose: string;           // "Show Sarah's doubt before breakthrough"
  emotional_arc: string;             // "Discouraged → Crisis → Determination"
  
  target_word_count: number;         // 2500-3000
  pacing: "fast" | "moderate" | "slow";
}
```

### 2.2 Chapter Narrative

```typescript
interface ChapterNarrative {
  // SCENE BREAKDOWN
  scenes: Scene[];
  
  // KEY MOMENTS
  decisive_moments: DecisiveMoment[];
  
  // EMOTIONAL BEATS
  emotional_beats: EmotionalBeat[];
  
  // DIALOGUE MOMENTS
  key_dialogues: KeyDialogue[];
  
  // TENSION STRUCTURE
  tension_arc: {
    opening_tension: string;
    complications: string[];
    climax: string;
    resolution: string;
    ending_hook: string;
  };
}

interface Scene {
  scene_id: string;
  order: number;
  location: Location;
  time: TimeContext;
  present_characters: string[];      // Character IDs
  
  // WHAT HAPPENS
  summary: string;                   // "Sarah shows you her business plan"
  narrative_beats: string[];         // Step-by-step what occurs
  
  // WHO KNOWS WHAT
  information_state: {
    [character_id: string]: {
      what_they_know: string[];
      what_they_dont_know: string[];
      what_they_suspect: string[];
    };
  };
  
  // SCENE PURPOSE
  function: "setup" | "conflict" | "revelation" | "decision" | "aftermath";
  tension_level: number;             // 1-10
  emotional_weight: number;          // 1-10
  
  // LITERARY ELEMENTS
  dominant_sense: "sight" | "sound" | "touch" | "smell" | "taste";
  atmosphere: string;                // "tense anticipation in quiet cafe"
  
  // CALLBACKS & PAYOFFS
  callbacks?: string[];              // References to earlier moments
  plants?: string[];                 // Seeds for future payoff
}

interface Location {
  name: string;                      // "Café Luna"
  evolution_state: string;           // "Week 32 - Your regular spot, barista knows your order"
  
  sensory_palette: {
    visual: string[];                // ["morning light through windows", "steam from espresso"]
    auditory: string[];              // ["espresso machine hiss", "quiet murmur of voices"]
    olfactory: string[];             // ["fresh coffee", "baking bread"]
    tactile: string[];               // ["worn wooden table", "warm mug"]
    atmospheric: string;             // "morning calm before the city fully wakes"
  };
  
  emotional_association: string;     // "Comfort and safety for both of you"
  significance: string;              // "Where your friendship deepened"
}

interface TimeContext {
  week: number;
  day: string;                       // "Tuesday"
  time_of_day: "morning" | "afternoon" | "evening" | "night";
  season?: string;
  weather?: string;
  time_pressure?: string;            // "3 days until opening"
}

interface DecisiveMoment {
  moment_id: string;
  description: string;               // "Sarah decides whether to show you the business plan"
  
  context_before: {
    sarah_state: CharacterMomentState;
    player_state: CharacterMomentState;
    environmental_pressure: string;
  };
  
  the_choice: {
    options_considered: string[];
    internal_debate: string;         // Sarah's thought process
    deciding_factor: string;         // What tips the decision
    choice_made: string;
  };
  
  immediate_aftermath: {
    sarah_reaction: string;
    player_reaction: string;
    relationship_shift: number;      // +0.3
    emotional_shift: string;
  };
  
  symbolic_significance?: string;    // "Represents her willingness to be vulnerable"
}

interface EmotionalBeat {
  beat_id: string;
  character: string;                 // Character ID
  emotion: string;                   // "fear of judgment"
  intensity: number;                 // 1-10
  
  // THE LADDER (from premium-novel-spec.md)
  build_up: {
    baseline: string;
    pressure_points: string[];
    stakes: string;
    breaking_point: string;
  };
  
  // HOW IT MANIFESTS
  physical_manifestation: string[];  // ["hands trembling", "avoiding eye contact"]
  behavioral_tells: string[];        // ["talking too fast", "laughing nervously"]
  internal_experience: string;       // What they're feeling internally
  
  // HOW TO SHOW IT
  show_dont_tell: {
    avoid_stating: string;           // "Sarah was nervous" ❌
    show_through: string[];          // ["Her hands trembled", "She laughed—wrong pitch"] ✅
  };
  
  resolution?: {
    how_it_resolves: string;
    new_emotional_state: string;
  };
}

interface KeyDialogue {
  dialogue_id: string;
  participants: string[];
  context: string;                   // "Sarah is about to reveal her dream"
  
  // DIALOGUE STRUCTURE
  exchanges: DialogueExchange[];
  
  // SUBTEXT
  surface_conversation: string;      // "Talking about the bookshop plan"
  actual_conversation: string;       // "Talking about fear, trust, capability"
  
  // WHAT THIS DIALOGUE ACCOMPLISHES
  functions: Array<"reveal_character" | "advance_plot" | "build_tension" | "show_relationship" | "deliver_information">;
  
  // VOICE REMINDERS
  voice_notes: {
    [character_id: string]: {
      speech_patterns: string[];
      word_choice: string;
      emotional_state_affects_speech: string;
    };
  };
}

interface DialogueExchange {
  speaker: string;
  line: string;
  subtext: string;                   // What they're really saying
  delivery: string;                  // "quietly, like confessing"
  non_verbal: string[];              // ["avoids eye contact", "traces coffee rim"]
  listener_reaction: string;         // How others respond
}
```

### 2.3 POV Perspectives

```typescript
interface POVPerspective {
  character_id: string;
  pov_type: "primary" | "secondary" | "brief_interlude";
  
  // WHEN THEY'RE POV CHARACTER
  word_count_allocation?: number;    // If primary POV
  scenes_from_their_pov: string[];   // Scene IDs
  
  // CHARACTER STATE AT CHAPTER START
  current_state: CharacterMomentState;
  
  // WHAT THEY KNOW/DON'T KNOW
  knowledge_state: KnowledgeState;
  
  // THEIR INTERNAL WORLD
  internal_narrative: InternalNarrative;
  
  // THEIR OBSERVATIONS OF OTHERS
  observations: CharacterObservation[];
  
  // VOICE CONSISTENCY
  voice_profile: VoiceProfile;
  
  // MEMORY ACCESS
  relevant_memories: MemoryFragment[];
  
  // WHAT THEY'RE HIDING/NOT SAYING
  unspoken: UnsaidThoughts[];
}

interface CharacterMomentState {
  // PERSONALITY AT THIS MOMENT
  personality: {
    openness: number;
    conscientiousness: number;
    extraversion: number;
    agreeableness: number;
    neuroticism: number;
  };
  
  // EMOTIONAL STATE
  emotional_state: {
    primary: string;                 // "ANXIOUS"
    secondary?: string;              // "HOPEFUL"
    intensity: number;               // 1-10
    duration: string;                // "3 days" - how long they've felt this way
  };
  
  // PHYSICAL STATE
  physical_state: {
    energy_level: number;            // 1-10
    health: string;                  // "Good" | "Tired" | "Stressed"
    physical_tells: string[];        // Current visible signs
  };
  
  // MENTAL STATE
  mental_state: {
    focus: string;                   // "Scattered" | "Focused" | "Obsessive"
    preoccupations: string[];        // What's on their mind
    stress_level: number;            // 1-10
  };
  
  // RELATIONSHIP STATE
  relationship_context: {
    [other_character_id: string]: {
      current_feeling: string;       // "Grateful but guilty"
      recent_interaction: string;
      unresolved_tension?: string;
    };
  };
  
  // LIFE CONTEXT
  life_context: {
    career_status: string;
    financial_status: string;
    living_situation: string;
    active_goals: string[];
    recent_events: string[];         // Last 7 days
    time_pressure: string[];         // Deadlines/urgency
  };
}

interface KnowledgeState {
  // WHAT THEY KNOW
  known_facts: string[];
  
  // WHAT THEY DON'T KNOW (but reader might)
  unknown_facts: string[];
  
  // WHAT THEY SUSPECT BUT AREN'T SURE
  suspicions: Array<{
    suspicion: string;
    confidence: number;              // 0.0-1.0
    based_on: string;
  }>;
  
  // WHAT THEY'RE WRONG ABOUT
  misconceptions?: Array<{
    belief: string;
    reality: string;
    when_corrected?: number;         // Chapter number if corrected later
  }>;
  
  // DRAMATIC IRONY OPPORTUNITIES
  dramatic_irony?: string[];         // Reader knows, character doesn't
}

interface InternalNarrative {
  // HOW THEY THINK
  thought_style: string;             // "Analytical, counts things, uses numbers"
  internal_voice: string;            // "Self-critical but trying to be braver"
  
  // ACTIVE THOUGHT THREADS
  preoccupations: InternalPreoccupation[];
  
  // THEIR STORY THEY TELL THEMSELVES
  self_narrative: string;            // "I'm the girl who plays it safe"
  narrative_evolution?: string;      // "Beginning to see herself as brave"
  
  // THEIR FEARS & DESIRES (In This Moment)
  active_fear: string;               // "Everyone will see I'm a fraud"
  active_desire: string;             // "To prove I can do this"
  
  // INTERNAL CONTRADICTIONS
  internal_conflict: string;         // "Wants to be seen vs. terrified of judgment"
}

interface CharacterObservation {
  observing: string;                 // Character being observed
  observation: string;               // What they notice
  interpretation: string;            // What they think it means
  emotional_response: string;        // How it makes them feel
  accuracy: "accurate" | "partially_accurate" | "misinterpretation";
}

interface VoiceProfile {
  // SPEAKING PATTERNS
  speech_patterns: string[];         // ["Short sentences when nervous", "Says 'I mean' a lot"]
  vocabulary_level: string;
  typical_sentence_length: string;
  
  // THOUGHT PATTERNS
  internal_monologue_style: string;  // "Questions herself constantly"
  metaphor_preference: string;       // "Uses book/reading metaphors"
  
  // EMOTIONAL EXPRESSION
  how_they_express_emotion: string;
  what_they_suppress: string;
  tells_when_lying: string[];
  
  // UNIQUE TICS
  verbal_tics: string[];
  behavioral_tics: string[];
  
  // VOICE DIFFERENTIATION
  distinct_from_other_povs: string;  // How this POV sounds different from others
}

interface MemoryFragment {
  memory_id: string;
  from_week: number;
  description: string;
  emotional_weight: number;          // 1-10
  sensory_details: string[];
  why_relevant: string;              // Why this memory surfaces now
  how_character_remembers: string;   // Their interpretation/feeling about it
}

interface UnsaidThoughts {
  what_they_think: string;
  why_they_dont_say_it: string;
  alternative_said: string;          // What they say instead
  subtext_signal: string;            // How reader can sense the unsaid
}
```

### 2.4 Technique Guidance

```typescript
interface TechniqueGuidance {
  // SCENE-LEVEL TECHNIQUES
  scene_techniques: {
    [scene_id: string]: {
      primary_technique: LiteraryTechnique;
      sensory_focus: string[];       // Which senses to emphasize
      pacing: "fast" | "moderate" | "slow";
      sentence_rhythm: "varied" | "short_punchy" | "flowing_long";
      
      show_dont_tell_reminders: Array<{
        avoid_telling: string;
        show_through: string[];
      }>;
    };
  };
  
  // DIALOGUE TECHNIQUES
  dialogue_guidance: {
    subtext_level: "minimal" | "moderate" | "heavy";
    functions_to_accomplish: string[];
    voice_differentiation_critical: boolean;
  };
  
  // EMOTIONAL BEATS
  emotional_technique: {
    build_method: "gradual" | "sudden" | "layered";
    release_method: "cathartic" | "subtle" | "unresolved";
    avoid_melodrama: string[];       // What NOT to do
  };
  
  // CHAPTER-LEVEL TECHNIQUES
  chapter_techniques: {
    opening_hook: HookGuidance;
    tension_architecture: TensionGuidance;
    ending_hook: HookGuidance;
    callbacks_to_plant: CallbackGuidance[];
  };
  
  // POV TRANSITION
  pov_transition_guidance?: {
    transition_point: string;        // When to switch POV
    transition_method: "scene_break" | "chapter_break" | "seamless";
    voice_shift_signal: string;      // How to signal the POV change
  };
}

interface LiteraryTechnique {
  technique: "showing" | "subtext" | "sensory_immersion" | "interiority" | "tension_building";
  application: string;               // Specific guidance for this scene
  examples: string[];                // Example approaches
  avoid: string[];                   // What not to do
}

interface HookGuidance {
  type: "question" | "action" | "emotion" | "mystery" | "stakes";
  approach: string;
  specific_elements: string[];
  tone: string;
}

interface TensionGuidance {
  micro_tension: Array<{
    in_scene: string;
    source: string;                  // What creates tension
    escalation: string;              // How it escalates
  }>;
  macro_tension: {
    chapter_stakes: string;
    unresolved_by_chapter_end: string[];
  };
}

interface CallbackGuidance {
  plant: string;                     // What to plant
  appears_casual_as: string;         // How it should seem natural
  payoff_in_chapter?: number;        // When it pays off
  emotional_resonance: string;       // What the payoff should feel like
}
```

### 2.5 Continuity Anchors

```typescript
interface ContinuityAnchors {
  // RECURRING ELEMENTS TO INCLUDE
  recurring_elements: RecurringElementUsage[];
  
  // ESTABLISHED FACTS TO HONOR
  must_honor_facts: string[];
  
  // RELATIONSHIP STATES TO MAINTAIN
  relationship_continuity: Array<{
    characters: [string, string];
    current_state: string;
    recent_developments: string;
    trajectory: "improving" | "stable" | "declining" | "complicated";
  }>;
  
  // WORLD CONTINUITY
  world_state: {
    date: string;
    season: string;
    weather_pattern: string;
    location_states: Array<{
      location: string;
      current_state: string;         // "Construction still ongoing"
    }>;
  };
  
  // PERSONALITY CONTINUITY
  personality_check: Array<{
    character: string;
    current_traits: number[];        // OCEAN
    recent_growth: string;
    cannot_contradict: string[];     // Established character facts
  }>;
  
  // TIMELINE CONTINUITY
  timeline_markers: Array<{
    event: string;
    timing: string;
    relation_to_chapter: "before" | "during" | "after";
  }>;
  
  // LANGUAGE CONTINUITY
  established_vocabulary: Array<{
    term: string;
    how_its_used: string;
    by_whom: string;
  }>;
}

interface RecurringElementUsage {
  element: string;                   // "Sarah's cerulean scarf"
  previous_appearances: number[];    // Chapters where it appeared
  this_chapter_usage: {
    should_appear: boolean;
    context: string;
    emotional_weight?: number;
    evolution?: string;              // How it's different/same
  };
  symbolic_weight: string;
}
```

### 2.6 Foreshadowing Seeds

```typescript
interface ForeshadowingHints {
  // FUTURE EVENTS TO HINT AT
  future_event: string;              // "Sarah's partner will leave"
  occurs_in_chapter: number;
  
  // HOW TO PLANT IT
  planting_method: {
    subtlety_level: "barely_noticeable" | "subtle" | "moderate";
    where_to_plant: string;          // "In Sarah's internal thoughts about future"
    plant_as: string;                // "Small moment of doubt she dismisses"
    reader_should_feel: string;      // "Vague unease, not certainty"
  };
  
  // SIGNALS TO INCLUDE
  signals: Array<{
    type: "dialogue_hint" | "behavioral_tell" | "environmental_sign" | "internal_thought" | "symbolic_object";
    content: string;
    delivery: string;                // How to present it naturally
  }>;
  
  // MISDIRECTION (optional)
  misdirection?: {
    false_signal: string;
    makes_reader_think: string;
    actual_truth: string;
  };
  
  // PAYOFF GUIDANCE
  payoff_context: {
    when_revealed: string;
    callback_method: string;         // How to reference this plant
    emotional_impact: string;        // "Oh, THAT'S what that meant"
  };
}
```

---

## 3. Example: Complete Chapter Packet

```typescript
const CHAPTER_8_PACKET: ChapterGenerationPacket = {
  chapter_metadata: {
    chapter_number: 8,
    title: "The Business Plan",
    weeks_covered: [28],
    primary_pov: "player",
    secondary_povs: ["sarah"],
    
    act_placement: {
      act: 2,
      position_in_act: "early",
      narrative_function: "Escalate tension - Sarah reveals dream but also doubts"
    },
    
    chapter_purpose: "Show Sarah's vulnerability and player's role as believer",
    emotional_arc: "Nervous anticipation → Vulnerability → Tentative hope",
    target_word_count: 2800,
    pacing: "moderate"
  },
  
  chapter_narrative: {
    scenes: [
      {
        scene_id: "cafe_invitation",
        order: 1,
        location: {
          name: "Café Luna",
          evolution_state: "Week 28 - Regular spot, comfortable routine established",
          sensory_palette: {
            visual: ["Afternoon light golden through windows", "Steam rising from cups", "Sarah's nervous fingers on notebook"],
            auditory: ["Espresso machine background hum", "Quiet afternoon crowd murmur"],
            olfactory: ["Fresh coffee", "Vanilla from pastries"],
            tactile: ["Warm ceramic mug", "Worn wooden table smooth under palms"],
            atmospheric: "Familiar safety mixed with electric anticipation"
          },
          emotional_association: "Safe space where important conversations happen",
          significance: "Where their friendship deepened over weeks"
        },
        
        time: {
          week: 28,
          day: "Tuesday",
          time_of_day: "afternoon",
          season: "Early autumn",
          weather: "Clear, crisp",
          time_pressure: null
        },
        
        present_characters: ["player", "sarah"],
        
        summary: "Sarah texts asking to meet, seems nervous. At cafe, she has a notebook but keeps almost leaving before finally deciding to show it.",
        
        narrative_beats: [
          "Player arrives, Sarah already there with closed notebook",
          "Small talk feels forced, Sarah avoids eye contact",
          "Sarah starts to speak three times, stops each time",
          "She almost leaves, gathering her things",
          "Player says something that makes her stay",
          "She takes a breath and opens the notebook",
          "She says: 'I want to show you something. But you have to promise to be honest.'"
        ],
        
        information_state: {
          "player": {
            what_they_know: ["Sarah works at café", "She loves books", "They've grown close"],
            what_they_dont_know: ["Extent of her planning", "How long she's dreamed this", "Her grandmother's influence"],
            what_they_suspect: ["This is important to her", "She's scared of judgment"]
          },
          "sarah": {
            what_they_know: ["Player is supportive friend", "They listen well", "They've encouraged her before"],
            what_they_dont_know: ["Player's financial situation", "If player believes in her"],
            what_they_suspect: ["Player might think it's unrealistic", "This might change the relationship"]
          }
        },
        
        function: "setup",
        tension_level: 7,
        emotional_weight: 8,
        dominant_sense: "sight",
        atmosphere: "Charged anticipation in familiar space",
        
        plants: [
          "Sarah's three false starts - callback to her pattern of self-sabotage",
          "The notebook is worn - she's been planning this for years",
          "Her grandmother's words mentioned briefly"
        ]
      },
      
      // ... more scenes ...
    ],
    
    decisive_moments: [
      {
        moment_id: "sarah_decides_to_share",
        description: "Sarah decides to show the business plan despite her fear",
        
        context_before: {
          sarah_state: {
            personality: { openness: 3.5, conscientiousness: 4.0, extraversion: 2.8, agreeableness: 3.9, neuroticism: 3.8 },
            emotional_state: { primary: "ANXIOUS", secondary: "HOPEFUL", intensity: 8, duration: "3 days since asking to meet" },
            physical_state: { energy_level: 4, health: "Nervous exhaustion", physical_tells: ["Trembling hands", "Dry mouth", "Can't sit still"] },
            mental_state: { focus: "Scattered", preoccupations: ["Will they laugh?", "This is stupid", "But what if..."], stress_level: 8 },
            relationship_context: {
              "player": { current_feeling: "Trusts but terrified", recent_interaction: "Last week you encouraged her creativity", unresolved_tension: "Hasn't been fully honest about dreams" }
            },
            life_context: {
              career_status: "Barista, feels stuck",
              financial_status: "$47,892.46 saved (knows to penny)",
              living_situation: "Small apartment, alone",
              active_goals: ["Save $50k", "Find courage to share dream"],
              recent_events: ["Grandmother's birthday passed", "Saw perfect storefront location"],
              time_pressure: ["Storefront might be rented soon", "Getting older, dreams fading"]
            }
          },
          
          player_state: {
            // ... similar structure ...
          },
          
          environmental_pressure: "Café is their place - if it goes badly, loses safe space"
        },
        
        the_choice: {
          options_considered: [
            "Make excuse and leave (safe but cowardly)",
            "Show plan but minimize it (safe but dishonest)",
            "Show plan fully and ask for real opinion (terrifying but real)"
          ],
          internal_debate: "Every voice in her head saying 'don't do it'. Grandmother's voice saying 'take up space'. Can't tell which is louder.",
          deciding_factor: "You said something simple: 'Sarah, whatever it is, I'm listening.' And meant it.",
          choice_made: "Opens notebook, voice shaking: 'I want to open a bookshop. And I'm terrified you'll think I'm ridiculous.'"
        },
        
        immediate_aftermath: {
          sarah_reaction: "Relief floods through her, followed immediately by panic. Can't take it back now.",
          player_reaction: "Surprise at the scope of planning, then genuine excitement. 'How long have you been working on this?'",
          relationship_shift: 0.15,
          emotional_shift: "Sarah: ANXIOUS → VULNERABLE but also slightly HOPEFUL"
        },
        
        symbolic_significance: "First time Sarah has spoken her dream aloud to anyone. Changes everything."
      }
    ],
    
    emotional_beats: [
      {
        beat_id: "sarah_vulnerability_peak",
        character: "sarah",
        emotion: "vulnerable_fear",
        intensity: 9,
        
        build_up: {
          baseline: "Sarah has been 'fine' for weeks, planning in secret",
          pressure_points: [
            "Saw storefront might be rented",
            "Grandmother's birthday reminded her of time passing",
            "Player asked how she's doing - couldn't keep lying"
          ],
          stakes: "This friendship is precious. If you think she's foolish, she loses both the dream and the friend.",
          breaking_point: "Moment when she opens the notebook and speaks"
        },
        
        physical_manifestation: [
          "Hands trembling so much she has to set down coffee",
          "Voice cracks on 'bookshop'",
          "Can't maintain eye contact",
          "Posture hunched like bracing for impact"
        ],
        
        behavioral_tells: [
          "Talks too fast",
          "Apologizes before you respond",
          "Touches grandmother's bracelet",
          "Halfway to standing up (flight response)"
        ],
        
        internal_experience: "Like standing naked while someone decides if you're worthy. Every second before you respond feels like dying.",
        
        show_dont_tell: {
          avoid_stating: "Sarah felt vulnerable and scared",
          show_through: [
            "Her hand trembled so badly she had to set the mug down",
            "The words came out in a rush, like ripping off a bandage",
            "'I'm sorry,' she said before you could even respond",
            "She touched her grandmother's bracelet—the nervous habit you'd noticed before"
          ]
        },
        
        resolution: {
          how_it_resolves: "Your genuine excitement and practical questions make her realize you're taking her seriously",
          new_emotional_state: "Cautiously hopeful, slightly less alone"
        }
      }
    ],
    
    key_dialogues: [
      {
        dialogue_id: "the_reveal",
        participants: ["sarah", "player"],
        context: "Sarah is about to reveal her carefully hidden dream",
        
        exchanges: [
          {
            speaker: "sarah",
            line: "I want to show you something. But you have to promise to be honest.",
            subtext: "Please don't just be nice. I need the truth but I'm terrified of it.",
            delivery: "Quietly, looking at the notebook not at you",
            non_verbal: ["Fingers tracing the notebook spine repeatedly", "Slight tremor in voice"],
            listener_reaction: "You lean forward slightly, giving her full attention"
          },
          {
            speaker: "player",
            line: "Okay. I promise.",
            subtext: "I'm here. Whatever this is, I'm listening for real.",
            delivery: "Simple, direct, grounding",
            non_verbal: ["Still hands", "Open posture", "Patient"],
            listener_reaction: "Sarah takes a shaky breath"
          },
          {
            speaker: "sarah",
            line: "I want to open a bookshop.",
            subtext: "This is my dream. The thing I've hidden. Please don't laugh.",
            delivery: "Like confessing something shameful, voice barely above whisper",
            non_verbal: ["Opens notebook but doesn't look up", "Shoulder hunched defensively"],
            listener_reaction: "Your expression shifts - surprise, then something warmer"
          },
          {
            speaker: "sarah",
            line: "I know it's probably not realistic. I mean, bookshops aren't exactly—",
            subtext: "I'm already trying to take it back because I'm terrified of your judgment.",
            delivery: "Rushed, apologetic",
            non_verbal: ["Starts to close notebook", "Half-laughs nervously"],
            listener_reaction: "You interrupt gently"
          },
          {
            speaker: "player",
            line: "Sarah. Can I look at this first?",
            subtext: "Stop apologizing for your dream. Let me actually see what you've created.",
            delivery: "Firm but kind, cutting through her spiral",
            non_verbal: ["Reach toward notebook", "Make eye contact"],
            listener_reaction: "Sarah stops mid-apology, nods"
          },
          {
            speaker: "player",
            line: "How long have you been working on this?",
            subtext: "This is serious. This is real. You're not foolish - you're prepared.",
            delivery: "Genuine curiosity, turning pages, impressed",
            non_verbal: ["Examining the detailed plans", "Surprise showing on face"],
            listener_reaction: "Sarah's shoulders start to relax slightly"
          },
          {
            speaker: "sarah",
            line: "Four years. I've been saving. Planning. I just... I never told anyone.",
            subtext: "I've been carrying this alone. You're the first person I trusted enough to show.",
            delivery: "Admission, quieter, more honest",
            non_verbal: ["Finally makes eye contact", "Still tense but slightly less defensive"],
            listener_reaction: "Your expression shifts - understanding the weight of what she's sharing"
          }
        ],
        
        surface_conversation: "Discussing the bookshop business plan",
        actual_conversation: "Discussing trust, belief, capability, and whether Sarah is allowed to want big things",
        
        functions: ["reveal_character", "advance_plot", "build_tension", "show_relationship", "deliver_information"],
        
        voice_notes: {
          "sarah": {
            speech_patterns: ["Apologizes reflexively", "Uses 'I mean' when backtracking", "Talks faster when nervous"],
            word_choice: "Simple, unpretentious, but precise about what matters to her",
            emotional_state_affects_speech: "Anxiety makes her apologize and minimize. Vulnerability makes her quieter but more honest."
          },
          "player": {
            speech_patterns: ["Short, grounding statements", "Asks questions rather than making pronouncements"],
            word_choice: "Direct but warm, practical but encouraging",
            emotional_state_affects_speech: "Curiosity genuine, excitement starting to show through measured response"
          }
        }
      }
    ],
    
    tension_arc: {
      opening_tension: "Sarah's text was vague but something's clearly important. Nervous energy when you arrive.",
      complications: [
        "She keeps almost leaving",
        "Multiple false starts create mounting tension",
        "You don't know what this is about - uncertainty for reader"
      ],
      climax: "Sarah opens the notebook and speaks her dream aloud for the first time",
      resolution: "Your genuine response begins to shift her from terror to tentative hope",
      ending_hook: "She asks: 'Do you think I can actually do this?' And you realize your answer matters more than you knew."
    }
  },
  
  pov_perspectives: [
    {
      character_id: "player",
      pov_type: "primary",
      word_count_allocation: 2200,
      scenes_from_their_pov: ["cafe_invitation", "business_plan_review"],
      
      current_state: {
        // ... full state object ...
      },
      
      knowledge_state: {
        known_facts: [
          "Sarah works at the café",
          "She's quiet but thoughtful",
          "She loves books obsessively",
          "You've grown close over 8 months"
        ],
        unknown_facts: [
          "She's been planning this for 4 years",
          "She has nearly $48k saved",
          "Her grandmother died encouraging her to dream bigger"
        ],
        suspicions: [
          {
            suspicion: "This meeting is important to her",
            confidence: 0.95,
            based_on: "Her unusual nervousness in text"
          },
          {
            suspicion: "She's been holding something back",
            confidence: 0.7,
            based_on: "Sometimes catches her looking distant"
          }
        ],
        dramatic_irony: null
      },
      
      internal_narrative: {
        thought_style: "Observant, reads people well, pragmatic but optimistic",
        internal_voice: "Steady, supportive, notices details others miss",
        preoccupations: [
          {
            thought: "Sarah seems more nervous than usual",
            recurring: true,
            emotional_tone: "Concerned, curious"
          }
        ],
        self_narrative: "I'm the person who shows up for people. I believe in possibilities.",
        active_fear: "Saying the wrong thing and losing this friendship",
        active_desire: "To support whatever this is",
        internal_conflict: "Want to protect her from disappointment vs. want to encourage her dreams"
      },
      
      observations: [
        {
          observing: "sarah",
          observation: "She's touching her grandmother's bracelet - only does that when anxious",
          interpretation: "Whatever this is, it's important and scary for her",
          emotional_response: "Protective, want to make her feel safe",
          accuracy: "accurate"
        },
        {
          observing: "sarah",
          observation: "The notebook is worn at the edges, pages dog-eared",
          interpretation: "She's been working on this for a long time",
          emotional_response: "Respect, curiosity about what's inside",
          accuracy: "accurate"
        }
      ],
      
      voice_profile: {
        speech_patterns: ["Direct but gentle", "Uses questions to show interest", "Calm, grounding presence"],
        vocabulary_level: "Moderate, accessible, authentic",
        typical_sentence_length: "Varied - short when grounding, longer when thinking",
        internal_monologue_style: "Observant, noting details, interpreting behavior",
        metaphor_preference: "Practical metaphors, occasional emotional insight",
        how_they_express_emotion: "Through actions and tone more than words",
        what_they_suppress: "Own doubts about life direction",
        tells_when_lying: "Breaks eye contact, which is rare",
        verbal_tics: ["Says 'okay' when thinking", "Pauses before important statements"],
        behavioral_tics: ["Leans forward when listening", "Still hands when serious"],
        distinct_from_other_povs: "More external focus, observes others. Sarah's POV is internal, self-critical. Marcus's POV (if included) would be analytical."
      },
      
      relevant_memories: [
        {
          memory_id: "sarah_first_conversation",
          from_week: 8,
          description: "First real conversation at the café. She mentioned Murakami. Something clicked.",
          emotional_weight: 7,
          sensory_details: ["Her surprised smile", "Coffee too hot", "Rain outside"],
          why_relevant: "This is where the friendship started - adds weight to this moment",
          how_character_remembers: "As a turning point. Didn't know it then, but that was when Sarah became important."
        },
        {
          memory_id: "sarah_grandmother_mention",
          from_week: 18,
          description: "Sarah briefly mentioned her grandmother, voice changed. Didn't press but noted it mattered.",
          emotional_weight: 6,
          sensory_details: ["She went very quiet", "Traced coffee cup rim", "Looked out window"],
          why_relevant: "Grandmother clearly important to her - watch for that connection",
          how_character_remembers: "One of the few times she's mentioned family. File away for later understanding."
        }
      ],
      
      unspoken: [
        {
          what_they_think: "I've been waiting for her to let me in. This feels like a threshold.",
          why_they_dont_say_it: "Too much pressure. Let her reveal at her pace.",
          alternative_said: "'I'm listening.'",
          subtext_signal: "The way you lean forward, give full attention, create space"
        }
      ]
    },
    
    {
      character_id: "sarah",
      pov_type: "secondary",
      word_count_allocation: 600,
      scenes_from_their_pov: ["sarah_pov_interlude"],
      
      current_state: {
        personality: {
          openness: 3.5,
          conscientiousness: 4.0,
          extraversion: 2.8,
          agreeableness: 3.9,
          neuroticism: 3.8
        },
        
        emotional_state: {
          primary: "ANXIOUS",
          secondary: "HOPEFUL",
          intensity: 8,
          duration: "3 days building to this"
        },
        
        physical_state: {
          energy_level: 4,
          health: "Nervous exhaustion, didn't sleep well",
          physical_tells: ["Trembling hands", "Dry mouth", "Rapid heartbeat"]
        },
        
        mental_state: {
          focus: "Scattered, can't focus on anything but this",
          preoccupations: [
            "What if they laugh?",
            "This is stupid",
            "Grandmother said to take up space",
            "The numbers add up. The numbers definitely add up.",
            "$47,892.46. Need $50k. So close."
          ],
          stress_level: 9
        },
        
        relationship_context: {
          "player": {
            current_feeling: "Trust mixed with terror of losing respect",
            recent_interaction: "Last week they encouraged my photography idea. They listen. But this is bigger.",
            unresolved_tension: "Haven't been fully honest. Feel like I'm lying by omission."
          }
        },
        
        life_context: {
          career_status: "Barista at Café Luna - 6 years. Feels stuck but haven't told anyone.",
          financial_status: "$47,892.46 saved. Knows it to the penny. Tracks every dollar.",
          living_situation: "Studio apartment, small, alone, quiet",
          active_goals: ["Save $50k total", "Find courage to share dream", "Find business partner or go alone"],
          recent_events: [
            "Grandmother's birthday was Tuesday - would've been 80",
            "Saw perfect storefront location Tuesday morning",
            "Can't stop thinking about both"
          ],
          time_pressure: ["Storefront location might be rented soon", "Getting older - 27 now, time moving", "Savings complete soon, then what?"]
        }
      },
      
      knowledge_state: {
        known_facts: [
          "Have $47,892.46 saved",
          "Business plan is solid - checked numbers 100 times",
          "Grandmother wanted her to do this",
          "Player is kind but doesn't know if they'll believe in this"
        ],
        unknown_facts: [
          "Player's actual financial situation",
          "If player has own dreams they're hiding",
          "How deep player's friendship really goes"
        ],
        suspicions: [
          {
            suspicion: "Player might think I'm unrealistic",
            confidence: 0.6,
            based_on: "Everyone thinks bookshops fail"
          },
          {
            suspicion: "This might change our friendship",
            confidence: 0.8,
            based_on: "Showing your real dreams to someone changes things"
          }
        ],
        misconceptions: [
          {
            belief: "Player might judge her for dreaming",
            reality: "Player will be supportive",
            when_corrected: 8
          }
        ]
      },
      
      internal_narrative: {
        thought_style: "Analytical, counts things, returns to numbers for comfort, catastrophizes",
        internal_voice: "Self-critical but trying to be braver. Grandmother's voice echoes underneath.",
        
        preoccupations: [
          {
            thought: "The numbers work. $2,400 rent, ~$300 utilities, $15,000 initial inventory, I've run this 1,000 times.",
            recurring: true,
            emotional_tone: "Desperate need for certainty"
          },
          {
            thought: "Grandmother said 'You apologize for existing. Make up your mind to take up space.'",
            recurring: true,
            emotional_tone: "Miss her, trying to honor her"
          },
          {
            thought: "What if they laugh? What if they don't laugh but I see pity in their eyes? Which is worse?",
            recurring: true,
            emotional_tone: "Terror"
          }
        ],
        
        self_narrative: "I'm the careful one. The one who plans everything and never takes risks. The one who plays it safe and hates herself for it.",
        narrative_evolution: "But grandmother didn't raise someone who hid. I'm trying to remember that.",
        
        active_fear: "Everyone will see I'm a fraud who has big dreams but no courage",
        active_desire: "To prove to myself I can do one brave thing",
        internal_conflict: "Desperate to be seen vs. terrified of being seen"
      },
      
      observations: [
        {
          observing: "player",
          observation: "They leaned forward when I said I wanted to show them something",
          interpretation: "They're actually listening, not just being polite",
          emotional_response: "Small hope, mixed with more fear because now I have to follow through",
          accuracy: "accurate"
        },
        {
          observing: "player",
          observation: "Their hands are still, patient. Not checking phone. Not fidgeting.",
          interpretation: "This matters to them. Or I matter to them.",
          emotional_response: "Want to believe it but scared to",
          accuracy: "accurate"
        }
      ],
      
      voice_profile: {
        speech_patterns: [
          "Apologizes reflexively before finishing thoughts",
          "Says 'I mean' when backtracking",
          "Uses 'I know' to pre-empt criticism",
          "Qualifies everything ('probably', 'maybe', 'I think')"
        ],
        vocabulary_level: "Simple but precise about what matters to her",
        typical_sentence_length: "Short when nervous, longer when passionate about books",
        internal_monologue_style: "Self-questioning, numbers for comfort, grandmother's voice echoing, catastrophic imagination",
        metaphor_preference: "Book and reading metaphors, sometimes literary references",
        how_they_express_emotion: "Indirectly, through behavior, has to build up to direct expression",
        what_they_suppress: "Desire, ambition, anger at herself",
        tells_when_lying: "Over-explains, avoids eye contact, touches grandmother's bracelet",
        verbal_tics: [
          "'I'm sorry' before saying anything vulnerable",
          "'I know this sounds...' when expecting judgment",
          "Self-deprecating laugh that sounds wrong"
        ],
        behavioral_tics: [
          "Touches grandmother's bracelet when anxious",
          "Traces rim of coffee cup in circles",
          "Can't maintain eye contact when scared",
          "Hunches shoulders defensively"
        ],
        distinct_from_other_povs: "Ultra self-critical, numbers-focused, internal spiral. Player's POV is observant outward. Sarah's is critical inward."
      },
      
      relevant_memories: [
        {
          memory_id: "grandmother_deathbed",
          from_week: -104,
          description: "Grandmother holding her hand: 'You apologize for existing. Make up your mind to take up space.' Died two days later.",
          emotional_weight: 10,
          sensory_details: ["Hospital smell", "Her papery hand", "Morphine-distant voice", "The certainty in her eyes"],
          why_relevant: "This moment is WHY she's doing this. Grandmother is why she saved. Why she planned. Why she's trying.",
          how_character_remembers: "The words loop constantly. Like a promise she hasn't kept yet. Like permission she hasn't accepted."
        },
        {
          memory_id: "first_saving_moment",
          from_week: -208,
          description: "First $100 saved. Felt like nothing and everything. Started the plan document that night.",
          emotional_weight: 7,
          sensory_details: ["Bank receipt", "Starting a new notebook", "Feeling of secret hope"],
          why_relevant: "Four years of saving led to this moment. Every dollar was a tiny act of belief.",
          how_character_remembers: "The night she started taking herself seriously. The night the dream became a plan."
        },
        {
          memory_id: "first_conversation_with_player",
          from_week: 8,
          description: "They came in reading Murakami. She spoke to a customer. She never spoke to customers.",
          emotional_weight: 8,
          sensory_details: ["Their surprised but warm smile", "Feeling like she'd done something brave"],
          why_relevant: "This is the person who made her feel like maybe she could be braver. That's why telling them matters so much.",
          how_character_remembers: "The first time in years someone looked at her like she was interesting instead of invisible."
        }
      ],
      
      unspoken: [
        {
          what_they_think: "If you believe in me, maybe I can believe in myself.",
          why_they_dont_say_it: "Too much pressure. Too vulnerable. What if they say no?",
          alternative_said: "'Do you think I can actually do this?'",
          subtext_signal: "The desperation in asking, the way she holds breath waiting for answer"
        },
        {
          what_they_think: "I've been alone with this dream for four years and I'm so tired of carrying it alone.",
          why_they_dont_say_it: "Admitting loneliness feels like admitting weakness",
          alternative_said: "'I never told anyone before.'",
          subtext_signal: "The weight in those words, the slight crack in voice"
        }
      ]
    }
  ],
  
  technique_guidance: {
    scene_techniques: {
      "cafe_invitation": {
        primary_technique: {
          technique: "tension_building",
          application: "Use Sarah's repeated false starts to build tension. Each time she almost speaks and doesn't, reader tension increases.",
          examples: [
            "She opened her mouth. Closed it. Traced the coffee cup rim.",
            "Three times she started to speak. Three times the words died before sound."
          ],
          avoid: [
            "Don't tell us she's nervous - show the behavior",
            "Don't rush the tension - let it build through repeated beats",
            "Don't explain her thoughts directly - let reader infer from behavior"
          ]
        },
        sensory_focus: ["sight", "sound", "touch"],
        pacing: "slow",
        sentence_rhythm: "varied",
        
        show_dont_tell_reminders: [
          {
            avoid_telling: "Sarah was very nervous about showing you the business plan.",
            show_through: [
              "Her hands trembled when she set down the mug",
              "She gathered her things twice, almost leaving",
              "The notebook stayed closed for fifteen minutes",
              "She apologized before speaking: 'I'm sorry, I—' and stopped"
            ]
          }
        ]
      },
      
      "business_plan_reveal": {
        primary_technique: {
          technique: "showing",
          application: "Show the vulnerability through physical details and specific behaviors",
          examples: [
            "The notebook's spine was cracked from use, pages dog-eared",
            "Her voice cracked on 'bookshop'",
            "She touched her grandmother's bracelet—once, twice, three times"
          ],
          avoid: [
            "Stating emotions directly",
            "Generic descriptions",
            "Telling us what this means to her - show through detail"
          ]
        },
        sensory_focus: ["sight", "touch", "sound"],
        pacing: "moderate",
        sentence_rhythm: "varied",
        
        show_dont_tell_reminders: [
          {
            avoid_telling: "The business plan was very detailed and showed how much work she'd put in.",
            show_through: [
              "Pages of calculations in her precise handwriting",
              "Vendor contacts, sketches, timelines spanning years",
              "Numbers checked and double-checked, margins filled with notes",
              "A photo of a storefront, edges worn from handling"
            ]
          }
        ]
      }
    },
    
    dialogue_guidance: {
      subtext_level: "heavy",
      functions_to_accomplish: [
        "Reveal Sarah's fear of judgment",
        "Show player's supportive nature",
        "Advance plot (business plan revealed)",
        "Deepen relationship (vulnerability shared)",
        "Establish trust dynamic"
      ],
      voice_differentiation_critical: true
    },
    
    emotional_technique: {
      build_method: "layered",
      release_method: "subtle",
      avoid_melodrama: [
        "No dramatic crying (too much)",
        "No soaring declarations (not Sarah's style)",
        "No immediate transformation (she's still scared after)"
      ]
    },
    
    chapter_techniques: {
      opening_hook: {
        type: "mystery",
        approach: "Sarah's vague text creates curiosity",
        specific_elements: [
          "Unusual for Sarah to ask to meet specifically",
          "Her nervousness palpable even in text",
          "Player's curiosity matched by slight concern"
        ],
        tone: "Intrigued, slightly worried"
      },
      
      tension_architecture: {
        micro_tension: [
          {
            in_scene: "cafe_invitation",
            source: "Sarah keeps almost leaving",
            escalation: "Each false start increases stakes - will she actually share or will moment pass?"
          },
          {
            in_scene: "business_plan_reveal",
            source: "Player's response unknown",
            escalation: "Every second of silence before response feels eternal to Sarah"
          }
        ],
        macro_tension: {
          chapter_stakes: "Sarah's dream revealed - player's response shapes her next choice",
          unresolved_by_chapter_end: [
            "Can she actually do this?",
            "Will player help or is this still alone?",
            "What happens next with this plan?"
          ]
        }
      },
      
      ending_hook: {
        type: "question",
        approach: "Sarah asks directly if player thinks she can do it",
        specific_elements: [
          "Question hangs in air",
          "Reader knows answer matters deeply",
          "Player realizes their belief might be what tips the scale"
        ],
        tone: "Vulnerable hope, weighty anticipation"
      },
      
      callbacks_to_plant: [
        {
          plant: "Sarah's grandmother's words: 'Take up space'",
          appears_casual_as: "Brief mention when she's struggling to speak up",
          payoff_in_chapter: 15,
          emotional_resonance: "When Sarah finally does take up space, grandmother's words return"
        },
        {
          plant: "The photo of the storefront in her notebook",
          appears_casual_as: "Just one element in the detailed plans",
          payoff_in_chapter: 12,
          emotional_resonance: "When they visit that actual storefront and she realizes it's real"
        },
        {
          plant: "The exact amount saved: $47,892.46",
          appears_casual_as: "Mentioned briefly in dialogue",
          payoff_in_chapter: 18,
          emotional_resonance: "When she spends it all and has to trust the investment"
        }
      ]
    },
    
    pov_transition_guidance: {
      transition_point: "After business plan revealed from player POV, brief Sarah POV interlude",
      transition_method: "scene_break",
      voice_shift_signal: "Clear section break, Sarah's POV indicated by immediate internal voice shift to her analytical, self-critical style"
    }
  },
  
  continuity_anchors: {
    recurring_elements: [
      {
        element: "Sarah's cerulean scarf",
        previous_appearances: [2, 4, 6],
        this_chapter_usage: {
          should_appear: true,
          context: "She's wearing it - visual consistency, comfort item",
          emotional_weight: 3,
          evolution: "Same scarf, but now reader knows it was grandmother's"
        },
        symbolic_weight: "Represents grandmother's influence and Sarah's connection to her past"
      },
      {
        element: "Café Luna",
        previous_appearances: [1, 2, 3, 4, 5, 6, 7],
        this_chapter_usage: {
          should_appear: true,
          context: "Primary setting - their safe space",
          emotional_weight: 7,
          evolution: "Still comfortable but now charged with new significance"
        },
        symbolic_weight: "Safe space where important moments happen"
      },
      {
        element: "Coffee cup rim tracing",
        previous_appearances: [4, 6],
        this_chapter_usage: {
          should_appear: true,
          context: "Sarah does this when nervous - behavioral consistency",
          emotional_weight: 5
        },
        symbolic_weight: "Sarah's nervous tell"
      }
    ],
    
    must_honor_facts: [
      "Sarah has worked at Café Luna for 6 years",
      "Grandmother died 2 years ago (Week -104)",
      "Player and Sarah met 20 weeks ago (Week 8)",
      "Sarah has been saving for 4 years",
      "This is the first time Sarah has told anyone about the dream",
      "Grandmother's last words were about taking up space"
    ],
    
    relationship_continuity: [
      {
        characters: ["player", "sarah"],
        current_state: "Close friends, growing deeper but undefined",
        recent_developments: "Player has been supportive about Sarah's photography interest (Week 27)",
        trajectory: "improving"
      }
    ],
    
    world_state: {
      date: "Week 28, Tuesday",
      season: "Early autumn",
      weather_pattern: "Clear, crisp - good weather",
      location_states: [
        {
          location: "Café Luna",
          current_state: "Normal afternoon operations, not too crowded"
        }
      ]
    },
    
    personality_continuity: [
      {
        character: "sarah",
        current_traits: [3.5, 4.0, 2.8, 3.9, 3.8],
        recent_growth: "Slightly more open after weeks of friendship (Openness +0.2 from Week 1)",
        cannot_contradict: [
          "Sarah is naturally reserved and anxious",
          "She's incredibly conscientious about planning",
          "She's agreeable and tends to apologize",
          "She has higher neuroticism - anxiety is real struggle"
        ]
      },
      {
        character: "player",
        current_traits: [4.2, 3.8, 3.6, 4.5, 3.1],
        recent_growth: "Stable personality, growing more confident in friendship role",
        cannot_contradict: [
          "Player is observant and notices details",
          "They're supportive but pragmatic",
          "They listen more than they talk",
          "They value authenticity"
        ]
      }
    ],
    
    timeline_markers: [
      {
        event: "First meeting at Café Luna",
        timing: "20 weeks ago (Week 8)",
        relation_to_chapter: "before"
      },
      {
        event: "Sarah's grandmother's birthday",
        timing: "2 days ago",
        relation_to_chapter: "just before"
      },
      {
        event: "Perfect storefront spotted",
        timing: "2 days ago (same day as grandmother's birthday)",
        relation_to_chapter: "just before"
      },
      {
        event: "Investment decision",
        timing: "10 weeks from now (Week 38)",
        relation_to_chapter: "after"
      }
    ],
    
    established_vocabulary: [
      {
        term: "Take up space",
        how_its_used: "Grandmother's phrase, Sarah remembers it when trying to be brave",
        by_whom: "Grandmother (deceased), echoes in Sarah's mind"
      },
      {
        term: "The usual",
        how_its_used: "What Sarah and player order at Café Luna",
        by_whom: "Both, casual shorthand"
      }
    ]
  },
  
  foreshadowing: [
    {
      future_event: "Sarah will need financial investment beyond her savings",
      occurs_in_chapter: 12,
      
      planting_method: {
        subtlety_level: "subtle",
        where_to_plant: "In player's observation of the business plan numbers",
        plant_as: "Brief thought: 'This is ambitious. Will $50k be enough?' Then dismissed.",
        reader_should_feel: "Vague concern, quickly forgotten in excitement"
      },
      
      signals: [
        {
          type: "internal_thought",
          content: "Player notices the budget is tight with no cushion",
          delivery: "Brief thought while reviewing plan, not dwelled on"
        },
        {
          type: "dialogue_hint",
          content: "Sarah mentions 'I've calculated for worst case, but real estate in this area...'",
          delivery: "Trails off, player reassures her it's fine"
        }
      ],
      
      payoff_context: {
        when_revealed: "Chapter 12 when lease requires more money than expected",
        callback_method: "Player remembers that moment: 'You asked if $50k would be enough. I said yes. I was wrong.'",
        emotional_impact: "Guilt mixed with determination to help"
      }
    },
    
    {
      future_event: "Sarah will have a crisis of confidence before opening",
      occurs_in_chapter: 16,
      
      planting_method: {
        subtlety_level: "barely_noticeable",
        where_to_plant: "In Sarah's internal monologue after sharing plan",
        plant_as: "Small voice: 'What if I fail?' She pushes it away.",
        reader_should_feel: "Normal self-doubt, every dreamer has this"
      },
      
      signals: [
        {
          type: "internal_thought",
          content: "Sarah briefly imagines failure, quickly suppresses it",
          delivery: "Quick flash in her POV section, immediately countered with numbers/logic"
        },
        {
          type: "behavioral_tell",
          content: "She touches her grandmother's bracelet while asking 'Do you think I can do this?'",
          delivery: "Subtle physical gesture, easily missed"
        }
      ],
      
      payoff_context: {
        when_revealed: "Chapter 16 when everything goes wrong before opening",
        callback_method: "That small voice becomes a roar. The doubt she pushed away returns amplified.",
        emotional_impact: "'I knew this would happen. I always knew.' Full crisis."
      }
    },
    
    {
      future_event: "The friendship will deepen into something more complex",
      occurs_in_chapter: 20,
      
      planting_method: {
        subtlety_level: "subtle",
        where_to_plant: "In the moment after Sarah asks 'Can I do this?' and player realizes how much their answer matters",
        plant_as: "A beat of silence. Something shifts. Not named, just felt.",
        reader_should_feel: "Something changed here, not sure what"
      },
      
      signals: [
        {
          type: "environmental_sign",
          content: "The café light changes, afternoon to golden hour",
          delivery: "Casual observation, marks the moment"
        },
        {
          type: "internal_thought",
          content: "Player notices: 'The way she's looking at me feels different. Like I'm not just a friend answering a question. Like my answer matters in a bigger way.'",
          delivery: "Fleeting thought, quickly moved past"
        }
      ],
      
      misdirection: {
        false_signal: "Could be interpreted as just deepening friendship",
        makes_reader_think: "They're becoming best friends",
        actual_truth: "Feelings beginning to complicate the dynamic"
      },
      
      payoff_context: {
        when_revealed: "Chapter 20 when one of them finally acknowledges the shift",
        callback_method: "'It changed that day, didn't it? At the café. When you said you believed in me. Something shifted then.'",
        emotional_impact: "Oh. It's been building since THAT moment."
      }
    }
  ]
};
```

---

## 4. Generation Prompt Structure

The LLM receives:

1. **Master Story Context** (always provided)
2. **This Chapter's Complete Packet** (as shown above)
3. **Master Generation Prompt** (instructions on how to use the data)

### Master Generation Prompt

```markdown
You are generating Chapter {N} of a literary-quality novel based on gameplay data.

**YOUR TASK:**
Write Chapter {N}: "{TITLE}" using the comprehensive data provided.

**CRITICAL REQUIREMENTS:**

1. **CONTINUITY:**
   - Honor ALL established facts
   - Maintain character personality traits and voice
   - Respect the timeline and previous events
   - Reference relevant past moments naturally

2. **POV EXECUTION:**
   - Write from {PRIMARY_POV}'s perspective
   - Use their internal narrative style and voice
   - Include their observations and interpretations
   - Access their knowledge state ONLY (don't reveal what they don't know)
   - If switching to secondary POV, signal clearly and shift voice completely

3. **LITERARY TECHNIQUES:**
   - SHOW, don't tell (see technique_guidance)
   - Use sensory details from scene descriptions
   - Build tension through scene structure
   - Layer subtext into dialogue
   - Vary sentence rhythm for pacing
   - Plant callbacks subtly
   - Include foreshadowing hints as specified

4. **EMOTIONAL AUTHENTICITY:**
   - Build emotional beats properly (don't rush catharsis)
   - Use physical manifestations of emotion
   - Ground feelings in sensory experience
   - Honor character's emotional state and how it affects perception

5. **DIALOGUE:**
   - Each character must sound distinct (use voice_profile)
   - Dialogue must serve multiple functions
   - Include subtext from dialogue_subtext fields
   - Show non-verbal elements (delivery, reactions)
   - Honor speech patterns and tics

6. **STRUCTURE:**
   - Follow scene order provided
   - Hit all narrative beats
   - Build tension through complications
   - End with the specified hook
   - Target word count: {WORD_COUNT}

7. **FORESHADOWING:**
   - Plant hints as specified in foreshadowing array
   - Make them natural, not obvious
   - Reader should barely notice on first read

8. **VOICE CONSISTENCY:**
   - If {PRIMARY_POV} is "player": Second-person, observant, external focus
   - If {PRIMARY_POV} is "sarah": Third-person close, internal, self-critical, analytical
   - If {PRIMARY_POV} is other: Use their specific voice_profile

9. **NO CONTRADICTIONS:**
   - Check all information against established_facts
   - Verify personality traits match current state
   - Confirm timeline markers are honored
   - Ensure recurring elements appear correctly

**DATA STRUCTURE USAGE:**
- Use character_moment_state for how POV character perceives moment
- Use knowledge_state to control what's revealed
- Use sensory_palette for scene descriptions
- Use emotional_beats for building feeling
- Use key_dialogues for exchanges (include subtext)
- Use technique_guidance for literary approach
- Use callbacks_to_plant for future payoffs
- Use foreshadowing for subtle hints

**OUTPUT:**
Write ONLY the chapter prose. No meta-commentary. No breaking character. No explanations.

Literary-quality fiction that feels like it was written by a human novelist, not generated.

Ready? Write Chapter {N}.
```

---

## 5. Quality Assurance Data

```typescript
interface QualityChecks {
  // RUN BEFORE GENERATION
  pre_generation_validation: {
    continuity_check: boolean;        // All facts cross-referenced?
    character_state_valid: boolean;   // Personality/knowledge states consistent?
    timeline_coherent: boolean;       // Events in logical order?
    voice_profiles_distinct: boolean; // Each POV sounds different?
  };
  
  // RUN AFTER GENERATION
  post_generation_validation: {
    contradictions_check: string[];   // Any contradictions found?
    established_facts_honored: boolean;
    voice_consistency: boolean;       // Did voice match profile?
    technique_application: {
      show_dont_tell: boolean;
      sensory_grounding: boolean;
      subtext_present: boolean;
      tension_maintained: boolean;
      callbacks_planted: boolean;
    };
    word_count: number;               // Within target?
    ending_hook_present: boolean;
  };
  
  // HUMAN REVIEW FLAGS
  review_flags: {
    needs_human_review: boolean;
    reasons: string[];
  };
}
```

---

## 6. Summary: Why This Structure Works

### Prevents Contradictions
- **Established facts database** prevents new information from conflicting with old
- **Character state tracking** ensures personality remains consistent or evolves logically
- **Timeline markers** prevent temporal impossibilities
- **Relationship continuity** tracks how connections should feel at this moment

### Enables Layered Writing
- **Multiple perspectives** with complete internal worlds
- **Subtext guidance** for dialogue
- **Emotional beat structures** for proper build-up
- **Sensory palettes** for immersive scenes

### Maintains Character Voices
- **Voice profiles** specify speech patterns, thought styles, tics
- **Internal narrative style** differs per character
- **Knowledge state** controls what each POV can reveal
- **Observation arrays** show how each character interprets others differently

### Ensures Natural POV Transitions
- **Voice shift signals** guide the transition
- **Complete state for each POV** so writer can fully embody them
- **Distinct_from_other_povs field** reminds how this voice differs

### Implements Literary Techniques
- **Technique guidance** specifies which techniques per scene
- **Show don't tell reminders** with concrete examples
- **Tension architecture** structures dramatic build
- **Callback and foreshadowing** systematically planted

### Creates Natural Flow
- **Scene breakdown** provides structure
- **Narrative beats** guide moment-to-moment progression
- **Tension arc** ensures proper dramatic rhythm
- **Pacing guidance** controls sentence rhythm and speed

### Maintains Continuity Across Chapters
- **Previous chapters summary** reminds what came before
- **Recurring elements tracking** ensures consistency
- **Master story context** provides big picture
- **Timeline markers** place chapter in larger story

This data structure provides **everything an LLM needs** to generate one chapter of high-quality literary fiction that:
- Never contradicts itself
- Maintains consistent character voices
- Uses sophisticated literary techniques
- Feels natural and emotionally authentic
- Sets up future developments
- Honors past developments
- Creates immersive, compelling prose

The key is **exhaustive detail** while maintaining **clear organization** so the LLM can navigate the data structure effectively.

