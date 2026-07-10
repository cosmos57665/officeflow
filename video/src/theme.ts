import {Easing, interpolate} from "remotion";

export const COLORS = {
  navy: "#08111F",
  navy2: "#0E1B2E",
  teal: "#0F766E",
  cyan: "#62E6D1",
  amber: "#FFB454",
  white: "#F7FAFC",
  muted: "#9FB2C9",
  line: "rgba(98,230,209,0.22)",
};

export const FONT = "Geist";

export const easeOut = (frame: number, from = 0, duration = 24) =>
  interpolate(frame, [from, from + duration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

export const sceneOpacity = (frame: number, duration: number) => {
  const enter = interpolate(frame, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const exit = interpolate(frame, [duration - 14, duration], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return Math.min(enter, exit);
};
