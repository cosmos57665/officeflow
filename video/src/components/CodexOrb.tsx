import type {CSSProperties} from "react";
import {spring, useCurrentFrame, useVideoConfig} from "remotion";
import {COLORS} from "../theme";

export type CodexOrbProps = {
  size?: number;
  style?: CSSProperties;
  label?: string;
  wink?: boolean;
};

export const CodexOrb = ({size = 170, style, label = "CODEX", wink = false}: CodexOrbProps) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame, fps, config: {damping: 18, stiffness: 110}});
  const pulse = 1 + Math.sin(frame / 13) * 0.035;

  return (
    <div style={{position: "absolute", width: size, height: size, transform: `scale(${pop * pulse})`, ...style}}>
      <div
        style={{
          position: "absolute",
          inset: -18,
          borderRadius: "50%",
          background: `conic-gradient(from ${frame * 2.2}deg, transparent, ${COLORS.cyan}, transparent 32%, ${COLORS.amber}, transparent 70%)`,
          opacity: 0.72,
          filter: "blur(2px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: "50%",
          border: `2px solid ${COLORS.cyan}`,
          background: `radial-gradient(circle at 35% 30%, #CFFFF7, ${COLORS.cyan} 10%, ${COLORS.teal} 40%, #071625 72%)`,
          boxShadow: `0 0 60px ${COLORS.cyan}66, inset 0 0 30px rgba(255,255,255,.18)`,
          display: "grid",
          placeItems: "center",
          color: COLORS.white,
          fontSize: size * 0.24,
          fontWeight: 800,
          letterSpacing: -2,
        }}
      >
        {wink ? ";)" : ">_"}
      </div>
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: size + 24,
          transform: "translateX(-50%)",
          color: COLORS.cyan,
          fontWeight: 700,
          letterSpacing: 4,
          fontSize: 16,
          whiteSpace: "nowrap",
        }}
      >
        {label}
      </div>
    </div>
  );
};
