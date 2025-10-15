
import React from 'react';
import { Parameter } from '../types';

interface SliderProps {
  parameter: Parameter;
  value: number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  isSumTo100?: boolean;
}

const Slider: React.FC<SliderProps> = ({ parameter, value, onChange, isSumTo100 = false }) => {
  const sliderStyle = {
    background: `linear-gradient(to right, #58a6ff ${value}%, #30363d ${value}%)`
  };

  return (
    <div>
      <div className="flex justify-between items-baseline mb-1">
        <label className="text-sm font-medium text-bright-sun" title={parameter.description}>
          {parameter.name}
        </label>
        <span className="text-sm font-mono text-dodger-blue bg-bunker px-2 py-0.5 rounded">
          {value}{isSumTo100 ? '%' : ''}
        </span>
      </div>
      <input
        type="range"
        min="0"
        max="100"
        value={value}
        onChange={onChange}
        className="w-full h-2 rounded-lg appearance-none cursor-pointer"
        style={sliderStyle}
      />
    </div>
  );
};

export default React.memo(Slider);
