
import React, { useCallback } from 'react';
import { Group, ConstraintType } from '../types';
import Slider from './Slider';

interface SliderGroupProps {
  group: Group;
  values: number[];
  onChange: (newValues: number[]) => void;
}

const SliderGroup: React.FC<SliderGroupProps> = ({ group, values, onChange }) => {
  const handleSliderChange = useCallback((sliderIndex: number, newValue: number) => {
    let newValues = [...values];
    newValues[sliderIndex] = newValue;

    if (group.constraintType === ConstraintType.SumTo100) {
      const remainder = 100 - newValue;
      const otherIndices = [0, 1, 2].filter(i => i !== sliderIndex);
      const otherTotal = values[otherIndices[0]] + values[otherIndices[1]];

      if (otherTotal === 0) {
        newValues[otherIndices[0]] = Math.floor(remainder / 2);
        newValues[otherIndices[1]] = Math.ceil(remainder / 2);
      } else {
        const ratio0 = values[otherIndices[0]] / otherTotal;
        newValues[otherIndices[0]] = Math.round(remainder * ratio0);
        newValues[otherIndices[1]] = remainder - newValues[otherIndices[0]];
      }
      
      const finalSum = newValues.reduce((a, b) => a + b, 0);
      if (finalSum !== 100) {
          const diff = 100 - finalSum;
          const nonZeroIndex = newValues.findIndex((val, index) => val > 0 && index !== sliderIndex);
          if(nonZeroIndex !== -1) {
            newValues[nonZeroIndex] += diff;
          } else {
            newValues[otherIndices[0]] += diff;
          }
      }
    }
    
    onChange(newValues);
  }, [group.constraintType, onChange, values]);

  return (
    <div className="bg-shark p-6 rounded-lg border border-outer-space">
      <h3 className="text-xl font-bold text-bright-sun mb-1">{group.title}</h3>
      <p className="text-sm text-comet mb-6">{group.description}</p>
      <div className="space-y-4">
        {group.parameters.map((param, index) => (
          <Slider
            key={param.name}
            parameter={param}
            value={values[index]}
            onChange={(e) => handleSliderChange(index, parseInt(e.target.value, 10))}
            isSumTo100={group.constraintType === ConstraintType.SumTo100}
          />
        ))}
        {group.constraintType === ConstraintType.SumTo100 && (
          <div className="text-right text-xs text-comet font-mono pt-2">
            Total: {values.reduce((a, b) => a + b, 0)}%
          </div>
        )}
      </div>
    </div>
  );
};

export default React.memo(SliderGroup);
