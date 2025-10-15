#!/usr/bin/env python3
"""
Lyria Stem Generator Script
Generates music stems for the Lifebond game using Google's Lyria API.

Requirements:
    pip install google-generativeai requests python-dotenv

Usage:
    python scripts/generate_lyria_stems.py --cue calm_positive --output app/assets/music/cues
"""

import os
import json
import argparse
import time
from pathlib import Path
from typing import List, Dict, Optional

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Using mock mode.")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables directly.")


# Cue definitions with MSV parameters
CUE_DEFINITIONS = {
    "calm_positive": {
        "tempo": 72,
        "key": "C",
        "mode": "Ionian",
        "bars": 8,
        "stems": ["pad", "piano", "light_rhythm"],
        "prompt": "Warm analog synthesizer pad and intimate felt piano with barely-there jazz brushes. 72 BPM, 8 bars, C major Ionian. Peaceful, calm, and comforting. Intimate journal music aesthetic. Soft attack, natural decay. Bar-aligned loop with seamless crossfade tail.",
        "msv": {
            "valence": 0.7,
            "arousal": 0.3,
            "tension": 0.2,
            "intimacy": 0.7,
            "sparsity": 3
        }
    },
    "melancholic_private": {
        "tempo": 60,
        "key": "C",
        "mode": "Dorian",
        "bars": 8,
        "stems": ["pad", "piano", "cello"],
        "prompt": "Dark brooding pad with detuned piano and melancholic cello melody. 60 BPM, 8 bars, C Dorian. Sad, intimate, and reflective. Small room ambience, close perspective. Natural fade at loop point.",
        "msv": {
            "valence": 0.3,
            "arousal": 0.2,
            "tension": 0.4,
            "intimacy": 0.8,
            "sparsity": 3
        }
    },
    "motivated": {
        "tempo": 80,
        "key": "G",
        "mode": "Mixolydian",
        "bars": 8,
        "stems": ["pad", "piano", "kick", "hihat"],
        "prompt": "Bright piano with warm pad, soft kick drum, and closed hi-hat pattern. 80 BPM, 8 bars, G Mixolydian. Energetic, motivated, and purposeful. Clear and forward-moving. Bar-aligned loop.",
        "msv": {
            "valence": 0.6,
            "arousal": 0.6,
            "tension": 0.3,
            "intimacy": 0.5,
            "sparsity": 2
        }
    }
}


class LyriaClient:
    """Client for generating music stems using Google's Lyria/MusicLM API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Lyria client.
        
        Args:
            api_key: Google AI Studio API key. If None, reads from GOOGLE_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            print("⚠️  No API key found. Running in MOCK MODE.")
            print("   Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable for real generation.")
            self.mock_mode = True
        else:
            self.mock_mode = not GENAI_AVAILABLE
            if GENAI_AVAILABLE:
                genai.configure(api_key=self.api_key)
                print("✅ Google AI configured successfully")
            else:
                print("⚠️  google-generativeai not installed. Running in MOCK MODE.")
    
    def generate_stems(
        self, 
        prompt: str, 
        tempo: int, 
        bars: int, 
        stems: List[str],
        key: str = "C",
        mode: str = "Ionian"
    ) -> Dict:
        """
        Generate music stems using Lyria API.
        
        Args:
            prompt: Detailed music description
            tempo: BPM (58-100)
            bars: Number of bars (typically 8)
            stems: List of stem names to generate
            key: Musical key
            mode: Musical mode (Ionian, Dorian, etc.)
            
        Returns:
            Dict with generation results
        """
        if self.mock_mode:
            return self._mock_generate(prompt, tempo, bars, stems, key, mode)
        
        # Real implementation using Google AI
        return self._real_generate(prompt, tempo, bars, stems, key, mode)
    
    def _mock_generate(
        self, 
        prompt: str, 
        tempo: int, 
        bars: int, 
        stems: List[str],
        key: str,
        mode: str
    ) -> Dict:
        """Mock generation for testing."""
        print("\n🎵 MOCK GENERATION MODE")
        print("=" * 60)
        print(f"Prompt: {prompt}")
        print(f"Tempo: {tempo} BPM")
        print(f"Bars: {bars}")
        print(f"Key: {key} {mode}")
        print(f"Stems: {', '.join(stems)}")
        print("=" * 60)
        
        # Calculate loop duration
        seconds_per_bar = (60.0 / tempo) * 4  # Assuming 4/4 time
        total_duration_seconds = seconds_per_bar * bars
        loop_end_ms = int(total_duration_seconds * 1000)
        
        return {
            "status": "completed",
            "generation_id": f"mock_{int(time.time())}",
            "stems": {
                stem: f"https://mock-cdn.lyria.com/{stem}.opus" for stem in stems
            },
            "metadata": {
                "tempo": tempo,
                "bars": bars,
                "key": key,
                "mode": mode,
                "loop_end_ms": loop_end_ms
            }
        }
    
    def _real_generate(
        self, 
        prompt: str, 
        tempo: int, 
        bars: int, 
        stems: List[str],
        key: str,
        mode: str
    ) -> Dict:
        """
        Real generation using Google AI API.
        
        Note: As of now, Lyria/MusicLM may not have direct public API access.
        This is a template for when it becomes available.
        
        Alternative: Use Google AI Studio web interface to generate music,
        then download and organize files manually.
        """
        print("\n🎵 ATTEMPTING REAL GENERATION")
        print("=" * 60)
        
        try:
            # TODO: Replace with actual Lyria API endpoint when available
            # For now, this is pseudocode based on expected API structure
            
            # Option 1: Direct API call (when available)
            # model = genai.GenerativeModel('lyria-v1')
            # response = model.generate_music(
            #     prompt=prompt,
            #     tempo=tempo,
            #     duration_bars=bars,
            #     key=key,
            #     mode=mode,
            #     separate_stems=True
            # )
            
            # Option 2: Use Gemini to generate MusicXML or MIDI (current workaround)
            model = genai.GenerativeModel('gemini-pro')
            
            enhanced_prompt = f"""
            Create a detailed technical specification for generating music with these parameters:
            
            Description: {prompt}
            Tempo: {tempo} BPM
            Bars: {bars}
            Key: {key} {mode}
            Stems needed: {', '.join(stems)}
            
            For each stem, provide:
            1. Exact instrument/sound source
            2. Playing technique
            3. MIDI note ranges
            4. Velocity curves
            5. Articulation style
            6. Effects chain (reverb, EQ, compression)
            
            Output as JSON.
            """
            
            response = model.generate_content(enhanced_prompt)
            
            print(f"Generated specification:")
            print(response.text)
            
            # Calculate loop duration
            seconds_per_bar = (60.0 / tempo) * 4
            total_duration_seconds = seconds_per_bar * bars
            loop_end_ms = int(total_duration_seconds * 1000)
            
            return {
                "status": "specification_generated",
                "generation_id": f"real_{int(time.time())}",
                "specification": response.text,
                "metadata": {
                    "tempo": tempo,
                    "bars": bars,
                    "key": key,
                    "mode": mode,
                    "loop_end_ms": loop_end_ms
                },
                "note": "Use this specification with AI Studio or DAW to generate actual audio"
            }
            
        except Exception as e:
            print(f"❌ Error during generation: {e}")
            print("Falling back to mock mode...")
            return self._mock_generate(prompt, tempo, bars, stems, key, mode)
    
    def download_stem(self, stem_url: str, output_path: str) -> bool:
        """
        Download a generated stem file.
        
        Args:
            stem_url: URL of the stem to download
            output_path: Local path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)
            
            if self.mock_mode or "mock-cdn" in stem_url:
                # Create placeholder file
                with open(output_path, 'w') as f:
                    f.write(f"# Mock Opus file\n")
                    f.write(f"# Source URL: {stem_url}\n")
                    f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                print(f"✅ Created mock file: {output_path}")
                return True
            
            # Real download (when actual files are available)
            import requests
            response = requests.get(stem_url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Downloaded: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to download {stem_url}: {e}")
            return False


def generate_cue_bank_entry(cue_name: str, cue_def: Dict, output_dir: str) -> Dict:
    """
    Generate a cue bank JSON entry.
    
    Args:
        cue_name: Name of the cue (e.g., "calm_positive")
        cue_def: Cue definition dictionary
        output_dir: Output directory path
        
    Returns:
        JSON-compatible dictionary for cue bank
    """
    tempo = cue_def["tempo"]
    bars = cue_def["bars"]
    stems = cue_def["stems"]
    
    # Calculate loop end time
    seconds_per_bar = (60.0 / tempo) * 4  # 4/4 time
    total_duration = seconds_per_bar * bars
    loop_end_ms = int(total_duration * 1000)
    
    # Generate cue ID
    cue_id = f"{cue_name}_{cue_def['key'].lower()}{tempo}"
    
    # Build stems dictionary
    stems_dict = {}
    for stem in stems:
        stem_path = f"assets/music/cues/{cue_name}/{stem}.opus"
        stems_dict[stem] = stem_path
    
    return {
        "id": cue_id,
        "tempo": tempo,
        "meterBeats": 4,
        "bars": bars,
        "loopStartMs": 0,
        "loopEndMs": loop_end_ms,
        "key": cue_def["key"],
        "mode": cue_def["mode"],
        "tags": [cue_name, "adaptive", "game"],
        "stems": stems_dict
    }


def main():
    """Main script entry point."""
    parser = argparse.ArgumentParser(
        description="Generate music stems for Lifebond game using Lyria"
    )
    parser.add_argument(
        "--cue",
        choices=list(CUE_DEFINITIONS.keys()) + ["all"],
        default="calm_positive",
        help="Which cue to generate (default: calm_positive)"
    )
    parser.add_argument(
        "--output",
        default="app/assets/music/cues",
        help="Output directory for generated stems"
    )
    parser.add_argument(
        "--api-key",
        help="Google API key (or set GOOGLE_API_KEY env var)"
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Only generate JSON cue bank entries, skip stem generation"
    )
    
    args = parser.parse_args()
    
    # Initialize client
    client = LyriaClient(api_key=args.api_key)
    
    # Determine which cues to generate
    if args.cue == "all":
        cues_to_generate = CUE_DEFINITIONS.keys()
    else:
        cues_to_generate = [args.cue]
    
    all_cue_entries = []
    
    for cue_name in cues_to_generate:
        cue_def = CUE_DEFINITIONS[cue_name]
        
        print(f"\n{'='*60}")
        print(f"🎵 GENERATING CUE: {cue_name}")
        print(f"{'='*60}")
        
        # Generate JSON entry
        cue_entry = generate_cue_bank_entry(cue_name, cue_def, args.output)
        all_cue_entries.append(cue_entry)
        
        print(f"\n📝 Cue Bank Entry:")
        print(json.dumps(cue_entry, indent=2))
        
        if args.json_only:
            print(f"\n⏭️  Skipping stem generation (--json-only mode)")
            continue
        
        # Generate stems
        print(f"\n🎼 Generating stems...")
        response = client.generate_stems(
            prompt=cue_def["prompt"],
            tempo=cue_def["tempo"],
            bars=cue_def["bars"],
            stems=cue_def["stems"],
            key=cue_def["key"],
            mode=cue_def["mode"]
        )
        
        if response.get("status") in ["completed", "specification_generated"]:
            # Download stems
            stem_urls = response.get("stems", {})
            output_dir = os.path.join(args.output, cue_name)
            
            print(f"\n📥 Downloading stems to: {output_dir}")
            for stem_name, stem_url in stem_urls.items():
                output_path = os.path.join(output_dir, f"{stem_name}.opus")
                client.download_stem(stem_url, output_path)
        else:
            print(f"❌ Generation failed with status: {response.get('status')}")
    
    # Save cue bank JSON
    cue_bank_path = os.path.join(args.output, "cue_bank_generated.json")
    os.makedirs(os.path.dirname(cue_bank_path), exist_ok=True)
    
    with open(cue_bank_path, 'w') as f:
        json.dump({"cues": all_cue_entries}, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"\n📄 Cue bank JSON saved to: {cue_bank_path}")
    print(f"\n📋 Next steps:")
    print(f"   1. Review generated stems in: {args.output}")
    print(f"   2. Convert to Opus format if needed: ffmpeg -i input.wav -c:a libopus -b:a 96k output.opus")
    print(f"   3. Update app/assets/music/cue_banks/core_season_a.json with entries")
    print(f"   4. Test in game: flutter run")
    print()


if __name__ == "__main__":
    main()

