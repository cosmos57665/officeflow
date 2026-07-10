import {existsSync, statSync} from "node:fs";
import {join} from "node:path";
import {describe, expect, it} from "vitest";

const screenDir = join(process.cwd(), "public", "screens");
const expected = ["home", "minutes", "inbox", "documents", "ask"];

describe("current React interface captures", () => {
  it.each(expected)("contains a non-empty %s screen", (name) => {
    const file = join(screenDir, `${name}.png`);
    expect(existsSync(file)).toBe(true);
    if (!existsSync(file)) return;
    expect(statSync(file).size).toBeGreaterThan(20_000);
  });
});
