# Create practical implementation examples showing how different combinations create contextual music
import pandas as pd

# Define example scenarios with specific slider settings
contextual_scenarios = {
    "Tense Boss Battle": {
        "Emotional Arousal & Valence": {"Energy Level": 90, "Valence": 20, "Tension": 95},
        "Temporal & Rhythmic Character": {"Tempo Intensity": 85, "Rhythmic Complexity": 70, "Metric Stability": 80},
        "Harmonic & Tonal Architecture": {"Consonance Level": 20, "Modal Character": 15, "Harmonic Density": 65},
        "Textural Density & Space": {"Instrumental Density": 85, "Spatial Width": 90, "Dynamic Range": 95},
        "Cultural & Stylistic Identity": {"Western Classical": 60, "Popular/Contemporary": 30, "World/Ethnic": 10},
        "Narrative & Contextual Function": {"Foreground Presence": 95, "Narrative Support": 90, "Emotional Directness": 85}
    },
    
    "Peaceful Village": {
        "Emotional Arousal & Valence": {"Energy Level": 25, "Valence": 80, "Tension": 10},
        "Temporal & Rhythmic Character": {"Tempo Intensity": 30, "Rhythmic Complexity": 20, "Metric Stability": 40},
        "Harmonic & Tonal Architecture": {"Consonance Level": 85, "Modal Character": 75, "Harmonic Density": 40},
        "Textural Density & Space": {"Instrumental Density": 35, "Spatial Width": 60, "Dynamic Range": 30},
        "Cultural & Stylistic Identity": {"Western Classical": 20, "Popular/Contemporary": 20, "World/Ethnic": 60},
        "Narrative & Contextual Function": {"Foreground Presence": 20, "Narrative Support": 40, "Emotional Directness": 30}
    },
    
    "Mysterious Exploration": {
        "Emotional Arousal & Valence": {"Energy Level": 40, "Valence": 35, "Tension": 60},
        "Temporal & Rhythmic Character": {"Tempo Intensity": 45, "Rhythmic Complexity": 55, "Metric Stability": 30},
        "Harmonic & Tonal Architecture": {"Consonance Level": 45, "Modal Character": 30, "Harmonic Density": 75},
        "Textural Density & Space": {"Instrumental Density": 50, "Spatial Width": 85, "Dynamic Range": 70},
        "Cultural & Stylistic Identity": {"Western Classical": 40, "Popular/Contemporary": 35, "World/Ethnic": 25},
        "Narrative & Contextual Function": {"Foreground Presence": 60, "Narrative Support": 75, "Emotional Directness": 45}
    },
    
    "Romantic Dialogue": {
        "Emotional Arousal & Valence": {"Energy Level": 20, "Valence": 85, "Tension": 15},
        "Temporal & Rhythmic Character": {"Tempo Intensity": 25, "Rhythmic Complexity": 15, "Metric Stability": 20},
        "Harmonic & Tonal Architecture": {"Consonance Level": 90, "Modal Character": 85, "Harmonic Density": 25},
        "Textural Density & Space": {"Instrumental Density": 25, "Spatial Width": 40, "Dynamic Range": 45},
        "Cultural & Stylistic Identity": {"Western Classical": 70, "Popular/Contemporary": 25, "World/Ethnic": 5},
        "Narrative & Contextual Function": {"Foreground Presence": 35, "Narrative Support": 80, "Emotional Directness": 70}
    },
    
    "High-Speed Chase": {
        "Emotional Arousal & Valence": {"Energy Level": 95, "Valence": 40, "Tension": 85},
        "Temporal & Rhythmic Character": {"Tempo Intensity": 90, "Rhythmic Complexity": 60, "Metric Stability": 95},
        "Harmonic & Tonal Architecture": {"Consonance Level": 60, "Modal Character": 50, "Harmonic Density": 40},
        "Textural Density & Space": {"Instrumental Density": 80, "Spatial Width": 95, "Dynamic Range": 85},
        "Cultural & Stylistic Identity": {"Western Classical": 20, "Popular/Contemporary": 70, "World/Ethnic": 10},
        "Narrative & Contextual Function": {"Foreground Presence": 90, "Narrative Support": 95, "Emotional Directness": 80}
    }
}

# Create a comparison table
scenarios_df = []
for scenario_name, settings in contextual_scenarios.items():
    row = {"Scenario": scenario_name}
    for group_name, sliders in settings.items():
        for slider_name, value in sliders.items():
            row[f"{group_name} - {slider_name}"] = value
    scenarios_df.append(row)

scenarios_comparison = pd.DataFrame(scenarios_df)

# Save to CSV for easy reference
scenarios_comparison.to_csv("music_generation_scenarios.csv", index=False)

print("CONTEXTUAL MUSIC GENERATION EXAMPLES")
print("=" * 60)
print("Here are 5 example scenarios showing how different slider combinations")
print("create contextually appropriate music for different game moments:")
print()

for scenario_name, settings in contextual_scenarios.items():
    print(f"\n🎵 {scenario_name.upper()}")
    print("-" * (len(scenario_name) + 4))
    
    for group_name, sliders in settings.items():
        print(f"\n{group_name}:")
        for slider_name, value in sliders.items():
            # Create a simple visual bar
            bar = "█" * (value // 5) + "░" * ((100 - value) // 5)
            print(f"  {slider_name:20} [{bar}] {value}%")
    
    print("=" * 50)

print(f"\n✅ Complete scenarios data saved to: music_generation_scenarios.csv")
print(f"📊 Total combinations possible: {18**6:,} unique musical contexts")