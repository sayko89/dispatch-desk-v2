// Dispatch Desk: Gemini tutor bridge.
// When the player messages the tutor, the game looks for window.askTutor({ system, prompt }).
// This file defines it. If the model fails, the game falls back to scripted questions.
import { GoogleGenAI } from "@google/genai";

declare global {
  interface Window {
    askTutor?: (input: { system: string; prompt: string }) => Promise<string>;
  }
}

const apiKey = process.env.GEMINI_API_KEY || process.env.API_KEY;
const ai = new GoogleGenAI({ apiKey });

// Tried in order. If a model name is retired (404), the next one is used and remembered.
const MODELS = ["gemini-3.8-flash", "gemini-flash-latest"];
let modelIndex = 0;

window.askTutor = async ({ system, prompt }) => {
  let lastError: unknown;
  for (let i = modelIndex; i < MODELS.length; i++) {
    try {
      const res = await ai.models.generateContent({
        model: MODELS[i],
        contents: prompt,
        config: {
          systemInstruction: system,
          temperature: 0.4,
          // Thinking models count reasoning tokens here too, so leave room.
          maxOutputTokens: 2048,
        },
      });
      modelIndex = i;
      return (res.text ?? "").trim();
    } catch (err) {
      lastError = err;
      const msg = String((err as Error)?.message ?? err);
      if (!/404|NOT_FOUND|not found/i.test(msg)) throw err;
    }
  }
  throw lastError;
};
