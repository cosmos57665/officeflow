import {existsSync, statSync} from "node:fs";
import {join} from "node:path";
import {execFileSync} from "node:child_process";
import {describe, expect, it} from "vitest";
import {SCENES} from "./story";

const audioDir = join(process.cwd(), "public", "audio");

describe("launch film audio assets", () => {
  it("contains one narration clip for every scene", () => {
    for (const scene of SCENES) {
      const file = join(audioDir, "voice", `${scene.id}.mp3`);
      expect(existsSync(file), scene.id).toBe(true);
      if (existsSync(file)) expect(statSync(file).size).toBeGreaterThan(2_000);
    }
  });

  it("keeps every narration clip inside its assigned scene", () => {
    for (const scene of SCENES) {
      const file = join(audioDir, "voice", `${scene.id}.mp3`);
      const seconds = Number(
        execFileSync(
          "ffprobe",
          ["-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", file],
          {encoding: "utf8"},
        ).trim(),
      );
      expect(seconds, scene.id).toBeLessThanOrEqual(scene.duration / 30);
    }
  });

  it("contains the licensed music bed and restrained sound effects", () => {
    for (const name of ["music-stylz.mp3", "whoosh.wav", "switch.wav", "ding.wav"]) {
      const file = join(audioDir, name);
      expect(existsSync(file), name).toBe(true);
      if (existsSync(file)) expect(statSync(file).size).toBeGreaterThan(2_000);
    }
  });
});
