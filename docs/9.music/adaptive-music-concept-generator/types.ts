
export interface Parameter {
  name: string;
  description: string;
}

export enum ConstraintType {
  Independent = 'independent',
  SumTo100 = 'sum-to-100',
}

export interface Group {
  id: string;
  title: string;
  description: string;
  constraintType: ConstraintType;
  parameters: [Parameter, Parameter, Parameter];
}

export type Settings = {
  [key: string]: number[];
};

export type Preset = {
  name: string;
  settings: Settings;
};
