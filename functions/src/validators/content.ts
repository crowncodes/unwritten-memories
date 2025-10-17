export interface ContentQuality {
  ok: boolean;
  messages: string[];
  metrics: {
    length: number;
    uniqueWordRatio: number;
    showTellHeuristic: number;
    clicheCount: number;
  };
}

const CLICHES = [
  'at the end of the day',
  'needless to say',
  'last but not least',
  'outside the box',
  'hits different',
];

export function validateDialogueContent(text: string): ContentQuality {
  const tokens = text.split(/\s+/).filter(Boolean);
  const length = tokens.length;
  const unique = new Set(tokens.map((t) => t.toLowerCase())).size;
  const uniqueWordRatio = length ? unique / length : 0;
  // crude "show vs tell" heuristic: proportion of verbs/adverbs-like endings
  const showTellHeuristic = tokens.filter((t) => /ing$|ly$/.test(t.toLowerCase())).length / (length || 1);
  const clicheCount = CLICHES.reduce((acc, phrase) => acc + (text.toLowerCase().includes(phrase) ? 1 : 0), 0);

  const messages: string[] = [];
  if (length < 12) messages.push('dialogue too short');
  if (uniqueWordRatio < 0.4) messages.push('low lexical diversity');
  if (clicheCount > 0) messages.push('contains clichés');

  return {
    ok: messages.length === 0,
    messages,
    metrics: { length, uniqueWordRatio, showTellHeuristic, clicheCount },
  };
}




