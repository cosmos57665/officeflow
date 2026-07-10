import type {ReactNode} from "react";
import {AbsoluteFill, interpolate, useCurrentFrame} from "remotion";
import {COLORS, sceneOpacity} from "../theme";

export type SceneShellProps = {
  children: ReactNode;
  duration: number;
  index: number;
  accent?: string;
};

export const SceneShell = ({children, duration, index, accent = COLORS.cyan}: SceneShellProps) => {
  const frame = useCurrentFrame();
  const wipe = interpolate(frame, [duration - 15, duration], [100, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: COLORS.navy,
        color: COLORS.white,
        fontFamily: "Geist, Arial, sans-serif",
        opacity: sceneOpacity(frame, duration),
        overflow: "hidden",
      }}
    >
      <AbsoluteFill
        style={{
          backgroundImage:
            "linear-gradient(rgba(98,230,209,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(98,230,209,.035) 1px, transparent 1px)",
          backgroundSize: "72px 72px",
          transform: `translate(${(frame * 0.18) % 72}px, ${(frame * 0.08) % 72}px)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 900,
          height: 900,
          right: -260,
          top: -420,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${accent}22, transparent 68%)`,
        }}
      />
      <div style={{position: "absolute", top: 44, left: 64, display: "flex", gap: 18, alignItems: "center"}}>
        <div style={{width: 42, height: 4, borderRadius: 8, background: accent}} />
        <span style={{fontSize: 18, color: COLORS.muted, letterSpacing: 3, fontWeight: 600}}>
          OFFICEFLOW / {String(index).padStart(2, "0")}
        </span>
      </div>
      <div style={{position: "absolute", right: 64, top: 48, color: COLORS.muted, fontSize: 16, letterSpacing: 2}}>
        BUILT WITH CODEX
      </div>
      {children}
      <div
        style={{
          position: "absolute",
          inset: 0,
          left: `${wipe}%`,
          background: `linear-gradient(90deg, transparent, ${accent}44, ${COLORS.navy})`,
        }}
      />
    </AbsoluteFill>
  );
};
