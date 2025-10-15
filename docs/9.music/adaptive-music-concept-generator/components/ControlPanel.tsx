
import React from 'react';
import { Settings } from '../types';
import { GROUPS } from '../constants';
import SliderGroup from './SliderGroup';

interface ControlPanelProps {
  settings: Settings;
  onSettingsChange: (groupId: string, newValues: number[]) => void;
}

const ControlPanel: React.FC<ControlPanelProps> = ({ settings, onSettingsChange }) => {
  return (
    <div className="space-y-6">
      {GROUPS.map(group => (
        <SliderGroup
          key={group.id}
          group={group}
          values={settings[group.id]}
          onChange={(newValues) => onSettingsChange(group.id, newValues)}
        />
      ))}
    </div>
  );
};

export default React.memo(ControlPanel);
