#!/usr/bin/env python3
"""
VERY BASIC Lyria API Example
Simplest possible script to call Lyria for music generation.

Usage:
    python simple_lyria_example.py
"""

import os
import json

# Try to import Google AI, fall back to mock if not available
try:
    import google.generativeai as genai
    MOCK_MODE = False
except ImportError:
    MOCK_MODE = True
    print("Running in MOCK mode (google-generativeai not installed)")


def generate_music_stem(prompt: str, output_file: str):
    """
    Generate a single music stem.
    
    Args:
        prompt: Description of the music to generate
        output_file: Where to save the result
    """
    print(f"\n🎵 Generating: {output_file}")
    print(f"Prompt: {prompt}\n")
    
    if MOCK_MODE:
        # Create mock file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(f"Mock audio file\nPrompt: {prompt}\n")
        print(f"✅ Created mock file: {output_file}")
        return
    
    # Real API call
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Set GOOGLE_API_KEY environment variable")
        return
    
    genai.configure(api_key=api_key)
    
    # NOTE: Lyria may not be directly accessible yet.
    # This is the expected structure when it becomes available:
    
    try:
        # Future Lyria API call (pseudocode):
        # model = genai.GenerativeModel('lyria-v1')
        # audio = model.generate_music(
        #     prompt=prompt,
        #     duration_seconds=26.67,  # 8 bars at 72 BPM
        #     output_format='opus'
        # )
        # audio.save(output_file)
        
        # Current workaround: Generate specification
        model = genai.GenerativeModel('gemini-pro')
        spec = model.generate_content(f"Create detailed music spec for: {prompt}")
        
        print(f"Generated specification:")
        print(spec.text)
        print(f"\n💡 Use this spec with AI Studio or DAW to create: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Generate a simple calm_positive pad stem."""
    
    # Simple prompt for one stem
    prompt = (
        "Warm analog synthesizer pad. "
        "72 BPM, 8 bars, C major. "
        "Peaceful and calming. "
        "Seamless loop."
    )
    
    output_file = "app/assets/music/cues/calm_positive/pad.opus"
    
    # Generate it
    generate_music_stem(prompt, output_file)
    
    print("\n" + "="*60)
    print("✅ Done!")
    print("="*60)
    print("\nNext steps:")
    print("1. If mock mode: Replace mock file with real audio")
    print("2. If specification mode: Use spec with AI Studio/DAW")
    print("3. Convert to Opus: ffmpeg -i input.wav -c:a libopus output.opus")
    print("4. Test in game: flutter run")


if __name__ == "__main__":
    main()

