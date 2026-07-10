import {existsSync} from "node:fs";
import type {ReactElement} from "react";
import {describe, expect, it} from "vitest";
import {RemotionRoot} from "./Root";

describe("OfficeFlow launch composition", () => {
  it("registers the approved 90-second 1080p composition", () => {
    const root = RemotionRoot({}) as ReactElement<{children?: ReactElement}>;
    const composition = (root.props.children ?? root) as ReactElement<{
      id: string;
      durationInFrames: number;
      fps: number;
      width: number;
      height: number;
    }>;

    expect(composition.props.id).toBe("OfficeFlowLaunch");
    expect(composition.props.durationInFrames).toBe(2700);
    expect(composition.props.fps).toBe(30);
    expect(composition.props.width).toBe(1920);
    expect(composition.props.height).toBe(1080);
  });

  it("contains a decision-complete ten-scene storyboard", async () => {
    const storyPath = new URL("./story.ts", import.meta.url);
    expect(existsSync(storyPath)).toBe(true);
    if (!existsSync(storyPath)) return;

    const {SCENES} = await import("./story");
    expect(SCENES).toHaveLength(10);
    expect(SCENES[0]).toMatchObject({id: "hook", from: 0, duration: 210});
    expect(SCENES[SCENES.length - 1]).toMatchObject({id: "close", from: 2460, duration: 240});
    expect(SCENES.every((scene) => scene.duration > 0)).toBe(true);
    expect(Math.max(...SCENES.map((scene) => scene.from + scene.duration))).toBe(2700);
  });
});
