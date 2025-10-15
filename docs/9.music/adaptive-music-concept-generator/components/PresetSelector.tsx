
import React, { useState } from 'react';
import { Preset } from '../types';

interface PresetSelectorProps {
  presets: Preset[];
  onSelect: (preset: Preset) => void;
}

const PresetSelector: React.FC<PresetSelectorProps> = ({ presets, onSelect }) => {
  const [selected, setSelected] = useState('Select a Preset...');

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const presetName = e.target.value;
    const preset = presets.find(p => p.name === presetName);
    if (preset) {
      onSelect(preset);
      setSelected(preset.name);
    }
  };

  return (
    <div className="w-full sm:w-auto">
      <label htmlFor="preset-selector" className="sr-only">
        Select a preset
      </label>
      <select
        id="preset-selector"
        value={selected}
        onChange={handleChange}
        className="w-full bg-bunker border border-outer-space text-ghost rounded-md px-4 py-3 focus:ring-2 focus:ring-dodger-blue focus:border-dodger-blue transition-colors duration-200"
      >
        <option disabled>Select a Preset...</option>
        {presets.map(preset => (
          <option key={preset.name} value={preset.name}>
            {preset.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default PresetSelector;
