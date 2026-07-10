export type SceneId =
  | "hook"
  | "plan"
  | "architecture"
  | "minutes"
  | "inbox"
  | "documents"
  | "ask"
  | "backend"
  | "demo"
  | "close";

export type StoryScene = {
  id: SceneId;
  from: number;
  duration: number;
  phrase?: string;
  narration: string;
};

export const SCENES: readonly StoryScene[] = [
  {
    id: "hook",
    from: 0,
    duration: 210,
    phrase: "ONE IDEA",
    narration:
      "I'm Codex. Sachin had an idea: what if repetitive office work could happen in seconds?",
  },
  {
    id: "plan",
    from: 210,
    duration: 240,
    narration:
      "He brought the problem. I helped turn it into a plan, and then into a working product.",
  },
  {
    id: "architecture",
    from: 450,
    duration: 360,
    phrase: "REACT + FASTAPI",
    narration:
      "Together, we built OfficeFlow: a modern React interface backed by FastAPI, with four practical workflows behind a clean API.",
  },
  {
    id: "minutes",
    from: 810,
    duration: 330,
    phrase: "FOUR WORKFLOWS",
    narration:
      "Meeting audio becomes a transcript, structured minutes, action items, and a downloadable Word document.",
  },
  {
    id: "inbox",
    from: 1140,
    duration: 270,
    narration:
      "Messy emails are sorted by priority, summarized, and paired with professional draft replies.",
  },
  {
    id: "documents",
    from: 1410,
    duration: 270,
    narration:
      "A single CSV becomes personalized documents, generated in one batch and packaged together.",
  },
  {
    id: "ask",
    from: 1680,
    duration: 270,
    narration:
      "A policy PDF becomes a conversation, returning precise answers with page citations.",
  },
  {
    id: "backend",
    from: 1950,
    duration: 300,
    phrase: "POWERED BY GEMINI",
    narration:
      "Built with Codex and powered at runtime by Gemini, OfficeFlow also has guarded operations and provider fallbacks to keep it dependable.",
  },
  {
    id: "demo",
    from: 2250,
    duration: 210,
    phrase: "RELIABILITY FIRST",
    narration:
      "When the internet disappears, Demo Mode keeps the presentation moving.",
  },
  {
    id: "close",
    from: 2460,
    duration: 240,
    narration:
      "One student. One AI collaborator. One working idea. Built by Sachin—with the help of ChatGPT's Codex.",
  },
] as const;
