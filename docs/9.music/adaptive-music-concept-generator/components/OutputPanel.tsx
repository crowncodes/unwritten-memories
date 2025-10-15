
import React from 'react';
import { Settings } from '../types';
import { GROUPS } from '../constants';

interface OutputPanelProps {
  aiResponse: string;
  isLoading: boolean;
  error: string | null;
  settings: Settings;
}

const OutputPanel: React.FC<OutputPanelProps> = ({ aiResponse, isLoading, error, settings }) => {
  
  const renderSummary = () => (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-sm">
        {GROUPS.map(group => (
            <div key={group.id} className="bg-outer-space p-3 rounded-md">
                <h4 className="font-semibold text-bright-sun truncate mb-1">{group.title.split('. ')[1]}</h4>
                <ul className="space-y-1">
                    {group.parameters.map((param, index) => (
                        <li key={param.name} className="flex justify-between text-xs">
                            <span className="text-comet truncate mr-2">{param.name}</span>
                            <span className="font-mono text-dodger-blue">{settings[group.id][index]}</span>
                        </li>
                    ))}
                </ul>
            </div>
        ))}
    </div>
  );

  return (
    <div className="bg-shark p-6 rounded-lg border border-outer-space h-full flex flex-col gap-6">
      <div>
        <h3 className="text-xl font-bold text-bright-sun mb-3">Current Configuration</h3>
        {renderSummary()}
      </div>
      <div className="flex-grow flex flex-col">
        <h3 className="text-xl font-bold text-bright-sun mb-3">AI Music Description</h3>
        <div className="flex-grow bg-bunker p-4 rounded-md border border-outer-space text-ghost overflow-y-auto min-h-[200px] whitespace-pre-wrap font-serif">
          {isLoading && (
            <div className="flex items-center justify-center h-full">
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 border-2 border-dashed rounded-full animate-spin border-dodger-blue"></div>
                <span>Generating your musical masterpiece...</span>
              </div>
            </div>
          )}
          {error && <p className="text-red-400">{error}</p>}
          {!isLoading && !error && !aiResponse && (
            <p className="text-comet text-center my-auto">
              Click "Describe Music with AI" to generate a description based on your settings.
            </p>
          )}
          {aiResponse && <p>{aiResponse}</p>}
        </div>
      </div>
    </div>
  );
};

export default OutputPanel;
