import {existsSync} from "node:fs";
import {describe, expect, it} from "vitest";
import {SCENES} from "./story";

describe("animated scene registry", () => {
  it("maps every storyboard scene to a renderable component", async () => {
    const registryPath = new URL("./scenes/index.ts", import.meta.url);
    expect(existsSync(registryPath)).toBe(true);
    if (!existsSync(registryPath)) return;

    const {SCENE_COMPONENTS} = await import("./scenes");
    expect(Object.keys(SCENE_COMPONENTS)).toEqual(SCENES.map((scene) => scene.id));
    expect(Object.values(SCENE_COMPONENTS).every((component) => typeof component === "function")).toBe(true);
  });
});
