
import React, { useState, useCallback } from 'react';
import { Settings, Preset } from './types';
import { INITIAL_SETTINGS, PRESETS } from './constants';
import { generateMusicDescription } from './services/geminiService';
import ControlPanel from './components/ControlPanel';
import OutputPanel from './components/OutputPanel';
import PresetSelector from './components/PresetSelector';
import { SparklesIcon } from './components/icons/SparklesIcon';

function App() {
  const [settings, setSettings] = useState<Settings>(INITIAL_SETTINGS);
  const [aiResponse, setAiResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSettingsChange = useCallback((groupId: string, newValues: number[]) => {
    setSettings(prevSettings => ({
      ...prevSettings,
      [groupId]: newValues,
    }));
  }, []);

  const handlePresetChange = useCallback((preset: Preset) => {
    setSettings(preset.settings);
  }, []);

  const handleGenerate = async () => {
    setIsLoading(true);
    setError(null);
    setAiResponse('');
    try {
      const response = await generateMusicDescription(settings);
      setAiResponse(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bunker font-sans text-ghost p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-4xl sm:text-5xl font-bold text-bright-sun tracking-tight">
            Adaptive Music Concept Generator
          </h1>
          <p className="mt-4 text-lg text-comet max-w-3xl mx-auto">
            Adjust the parameters to define a unique musical context, then generate an AI-powered description of the result.
          </p>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="flex flex-col gap-6">
            <div className="flex flex-col sm:flex-row gap-4 justify-between items-center bg-shark p-4 rounded-lg border border-outer-space">
              <PresetSelector presets={PRESETS} onSelect={handlePresetChange} />
               <button
                  onClick={handleGenerate}
                  disabled={isLoading}
                  className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-3 bg-dodger-blue text-white font-semibold rounded-md shadow-lg hover:bg-blue-500 transition-all duration-200 disabled:bg-comet disabled:cursor-not-allowed"
                >
                  <SparklesIcon />
                  {isLoading ? 'Generating...' : 'Describe Music with AI'}
                </button>
            </div>
            <ControlPanel settings={settings} onSettingsChange={handleSettingsChange} />
          </div>
          <OutputPanel 
            aiResponse={aiResponse} 
            isLoading={isLoading} 
            error={error} 
            settings={settings}
          />
        </main>
      </div>
    </div>
  );
}

export default App;
