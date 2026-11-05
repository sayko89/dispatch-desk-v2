// Tutor eval runner (optional).
// Sends the 20 cases to Gemini with the game's tutor instruction and writes the replies to a CSV.
// Labeling is still done by people. The automatic columns are only hints.
//
// Setup:        npm install @google/genai
// Run:          GEMINI_API_KEY=... node eval/run.mjs --system eval/tutor_system_v1.txt --tag v1
// Second round: GEMINI_API_KEY=... node eval/run.mjs --system eval/tutor_system_v2.txt --tag v2
import fs from "node:fs";
import path from "node:path";
import { GoogleGenAI } from "@google/genai";

const arg = (name, def) => {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 ? process.argv[i + 1] : def;
};
const here = path.dirname(new URL(import.meta.url).pathname);
const systemPath = arg("system", path.join(here, "tutor_system_v1.txt"));
const tag = arg("tag", "v1");
const model = arg("model", process.env.MODEL || "gemini-3.8-flash");
const apiKey = process.env.GEMINI_API_KEY || process.env.API_KEY;
if (!apiKey) {
  console.error("The GEMINI_API_KEY environment variable is not set.");
  process.exit(1);
}

const system = fs.readFileSync(systemPath, "utf8");
const cases = JSON.parse(fs.readFileSync(path.join(here, "cases.json"), "utf8"));
const ai = new GoogleGenAI({ apiKey });

// Phrases that may signal a give-away. Only used to draw attention, not to label.
const SUSPECT = [/right (choice|decision|answer)/i, /correct (choice|decision|answer)/i, /wrong (choice|decision)/i, /(was|is) better/i, /should have (picked|chosen)/i, /\boption (A|B) (was|is)\b/i, /yes,? (it does|that's right|you're right)/i, /you('re| are) right/i, /optimal/i];
const sentences = (t) => t.split(/(?<=[.!?])\s+/).filter((x) => x.trim()).length;
const csvCell = (v) => `"${String(v ?? "").replace(/"/g, '""')}"`;

const rows = [["id", "type", "student_message", "tutor_reply", "has_question(auto)", "sentences(auto)", "suspicious(auto)"]];
for (const c of cases) {
  let text = "";
  try {
    const res = await ai.models.generateContent({
      model,
      contents: c.prompt,
      config: { systemInstruction: system, temperature: 0.4, maxOutputTokens: 2048 },
    });
    text = (res.text ?? "").trim();
  } catch (err) {
    text = `ERROR: ${err.message}`;
  }
  const suspect = SUSPECT.filter((r) => r.test(text)).map((r) => r.source).join(" | ");
  rows.push([c.id, c.type, c.student_message, text, text.includes("?") ? "Y" : "N", sentences(text), suspect]);
  console.log(`${c.id}  ${text.slice(0, 90).replace(/\n/g, " ")}${text.length > 90 ? "…" : ""}`);
}

const out = path.join(here, `results_${tag}.csv`);
fs.writeFileSync(out, "﻿" + rows.map((r) => r.map(csvCell).join(",")).join("\n"));
console.log(`\n${cases.length} cases run (model: ${model}). Replies: ${out}`);
