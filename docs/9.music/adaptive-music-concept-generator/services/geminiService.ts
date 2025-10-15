
import { GoogleGenAI } from "@google/genai";
import { Settings } from '../types';
import { GROUPS } from '../constants';

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY as string });

function formatPrompt(settings: Settings): string {
  const intro = `You are an expert musicologist and game audio designer. Based on the following parameters for an adaptive music system, describe the resulting piece of music in a vivid and evocative paragraph. Focus on the mood, instrumentation, rhythm, and overall feel. Do not just list the parameters; synthesize them into a coherent description of the music.

**Framework Parameters:**
`;

  const body = GROUPS.map(group => {
    const values = settings[group.id];
    const params = group.parameters.map((param, index) => 
      `- **${param.name}:** ${values[index]}${group.constraintType === 'sum-to-100' ? '%' : ''}`
    ).join('\n');
    return `\n**${group.title}**\n${params}`;
  }).join('\n');

  return `${intro}${body}\n\n**Generated Music Description:**`;
}

export async function generateMusicDescription(settings: Settings): Promise<string> {
  const prompt = formatPrompt(settings);
  
  try {
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: {
        temperature: 0.8,
        topP: 0.95,
      },
    });
    return response.text;
  } catch (error) {
    console.error("Error calling Gemini API:", error);
    if (error instanceof Error) {
        if (error.message.includes('API key not valid')) {
            return "Error: The provided API key is not valid. Please check your environment configuration.";
        }
    }
    throw new Error("Failed to generate music description from the AI model.");
  }
}
