# Let's create a comprehensive framework for mutually exclusive music concept groups
# Based on research, I'll analyze the key dimensions that can be used for contextual music generation

import pandas as pd
import numpy as np

# Define mutually exclusive music concept groups based on research findings
music_framework = {
    "Emotional Arousal & Valence": {
        "description": "Based on Russell's Circumplex Model - energy level and positivity/negativity",
        "sliders": [
            {"name": "Energy Level", "range": "0-100", "description": "From calm/serene to highly energetic/frantic"},
            {"name": "Valence", "range": "0-100", "description": "From negative/dark to positive/bright"},
            {"name": "Tension", "range": "0-100", "description": "From relaxed to tense/anxious"}
        ],
        "constraints": "Any combination allowed - creates 3D emotion space",
        "examples": "Low Energy + High Valence = Content/Peaceful, High Energy + Low Valence = Angry/Aggressive"
    },
    
    "Temporal & Rhythmic Character": {
        "description": "Time-based musical elements that define movement and pace",
        "sliders": [
            {"name": "Tempo Intensity", "range": "0-100", "description": "From very slow (40 BPM) to very fast (200+ BPM)"},
            {"name": "Rhythmic Complexity", "range": "0-100", "description": "From simple steady beats to complex polyrhythms"},
            {"name": "Metric Stability", "range": "0-100", "description": "From fluid/rubato to strict metronomic time"}
        ],
        "constraints": "All can be active simultaneously - they modify different aspects of time",
        "examples": "High Tempo + Low Complexity = Dance music, Low Tempo + High Complexity = Progressive jazz"
    },
    
    "Harmonic & Tonal Architecture": {
        "description": "The structural foundation of musical harmony and tonality",
        "sliders": [
            {"name": "Consonance Level", "range": "0-100", "description": "From highly dissonant to perfectly consonant"},
            {"name": "Modal Character", "range": "0-100", "description": "From dark modes (minor, phrygian) to bright modes (major, lydian)"},
            {"name": "Harmonic Density", "range": "0-100", "description": "From simple triads to complex extended chords"}
        ],
        "constraints": "Must sum to 100 - these define the harmonic foundation",
        "examples": "High Consonance + Bright Modal = Happy pop, Low Consonance + Dark Modal = Horror scores"
    },
    
    "Textural Density & Space": {
        "description": "How musical elements are layered and positioned in sonic space",
        "sliders": [
            {"name": "Instrumental Density", "range": "0-100", "description": "From solo/sparse to full orchestral"},
            {"name": "Spatial Width", "range": "0-100", "description": "From mono/centered to wide stereo field"},
            {"name": "Dynamic Range", "range": "0-100", "description": "From compressed/flat to highly dynamic"}
        ],
        "constraints": "Any combination allowed - creates 3D spatial character",
        "examples": "High Density + Wide Space = Epic orchestral, Low Density + Narrow Space = Intimate solo"
    },
    
    "Cultural & Stylistic Identity": {
        "description": "Genre and cultural signifiers that provide contextual meaning",
        "sliders": [
            {"name": "Western Classical", "range": "0-100", "description": "Traditional orchestral and chamber music elements"},
            {"name": "Popular/Contemporary", "range": "0-100", "description": "Rock, pop, electronic, hip-hop elements"},
            {"name": "World/Ethnic", "range": "0-100", "description": "Non-western scales, instruments, and traditions"}
        ],
        "constraints": "Must sum to 100 - defines primary cultural context",
        "examples": "100% Classical = Symphony, 50% Pop + 50% World = World music fusion"
    },
    
    "Narrative & Contextual Function": {
        "description": "The role music plays in supporting story or environmental context",
        "sliders": [
            {"name": "Foreground Presence", "range": "0-100", "description": "From ambient background to attention-grabbing"},
            {"name": "Narrative Support", "range": "0-100", "description": "From abstract/atmospheric to story-driven"},
            {"name": "Emotional Directness", "range": "0-100", "description": "From subtle suggestion to obvious emotional manipulation"}
        ],
        "constraints": "Any combination allowed - defines functional role",
        "examples": "High Foreground + High Narrative = Film score climax, Low all = Ambient background"
    }
}

# Create a summary table
groups_data = []
for group_name, group_data in music_framework.items():
    groups_data.append({
        'Group Name': group_name,
        'Number of Sliders': len(group_data['sliders']),
        'Constraint Type': group_data['constraints'],
        'Primary Function': group_data['description']
    })

framework_df = pd.DataFrame(groups_data)
print("MUSIC GENERATION FRAMEWORK - 6 MUTUALLY EXCLUSIVE CONCEPT GROUPS")
print("=" * 80)
print(framework_df.to_string(index=False))
print("\n")

# Create detailed breakdown for each group
for group_name, group_data in music_framework.items():
    print(f"\n{group_name.upper()}")
    print("-" * len(group_name))
    print(f"Description: {group_data['description']}")
    print(f"Constraints: {group_data['constraints']}")
    print("\nSliders:")
    for i, slider in enumerate(group_data['sliders'], 1):
        print(f"  {i}. {slider['name']} ({slider['range']})")
        print(f"     {slider['description']}")
    print(f"\nExamples: {group_data['examples']}")
    print("=" * 60)