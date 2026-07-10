import type {CSSProperties, ReactNode} from "react";
import {Img, staticFile, useCurrentFrame} from "remotion";
import {COLORS, easeOut} from "../theme";

export const KineticPhrase = ({text, delay = 0, style}: {text: string; delay?: number; style?: CSSProperties}) => {
  const frame = useCurrentFrame();
  const enter = easeOut(frame, delay, 28);
  return (
    <div
      style={{
        position: "absolute",
        opacity: enter,
        transform: `translateY(${(1 - enter) * 60}px) scale(${0.94 + enter * 0.06})`,
        fontSize: 126,
        lineHeight: 0.9,
        letterSpacing: -6,
        fontWeight: 800,
        color: COLORS.white,
        textShadow: `0 0 50px ${COLORS.cyan}22`,
        ...style,
      }}
    >
      {text}
    </div>
  );
};

export const NodeCard = ({title, detail, delay = 0, accent = COLORS.cyan, style}: {
  title: string;
  detail: string;
  delay?: number;
  accent?: string;
  style?: CSSProperties;
}) => {
  const frame = useCurrentFrame();
  const enter = easeOut(frame, delay, 22);
  return (
    <div
      style={{
        padding: "22px 26px",
        border: `1px solid ${accent}55`,
        borderRadius: 22,
        background: "rgba(14,27,46,.88)",
        boxShadow: `0 22px 60px rgba(0,0,0,.28), inset 0 1px ${accent}22`,
        opacity: enter,
        transform: `translateY(${(1 - enter) * 34}px) scale(${0.94 + enter * 0.06})`,
        ...style,
      }}
    >
      <div style={{fontSize: 26, fontWeight: 750, color: COLORS.white}}>{title}</div>
      <div style={{fontSize: 17, color: COLORS.muted, marginTop: 7, lineHeight: 1.3}}>{detail}</div>
    </div>
  );
};

export const FlowLine = ({from, width, delay = 0, color = COLORS.cyan}: {
  from: {left: number; top: number};
  width: number;
  delay?: number;
  color?: string;
}) => {
  const frame = useCurrentFrame();
  const progress = easeOut(frame, delay, 30);
  return (
    <div style={{position: "absolute", left: from.left, top: from.top, width: width * progress, height: 3, background: color, boxShadow: `0 0 18px ${color}`}}>
      <div style={{position: "absolute", right: -7, top: -5, width: 13, height: 13, borderRadius: "50%", background: color}} />
    </div>
  );
};

export const UIFrame = ({screen, delay = 0, style, children}: {
  screen: "home" | "minutes" | "inbox" | "documents" | "ask";
  delay?: number;
  style?: CSSProperties;
  children?: ReactNode;
}) => {
  const frame = useCurrentFrame();
  const enter = easeOut(frame, delay, 32);
  const float = Math.sin(frame / 23) * 5;
  return (
    <div
      style={{
        position: "absolute",
        width: 1240,
        height: 775,
        borderRadius: 28,
        overflow: "hidden",
        border: `1px solid ${COLORS.cyan}55`,
        background: COLORS.navy2,
        boxShadow: "0 42px 100px rgba(0,0,0,.5)",
        opacity: enter,
        transform: `translateY(${(1 - enter) * 65 + float}px) scale(${0.91 + enter * 0.09})`,
        ...style,
      }}
    >
      <div style={{height: 38, background: "#102036", display: "flex", alignItems: "center", paddingLeft: 18, gap: 9}}>
        {[COLORS.amber, COLORS.cyan, COLORS.teal].map((color) => (
          <span key={color} style={{width: 10, height: 10, borderRadius: "50%", background: color}} />
        ))}
        <span style={{marginLeft: 18, fontSize: 13, color: COLORS.muted, letterSpacing: 2}}>OFFICEFLOW / REACT</span>
      </div>
      <Img src={staticFile(`screens/${screen}.png`)} style={{width: "100%", height: "calc(100% - 38px)", objectFit: "cover", objectPosition: "top"}} />
      {children}
    </div>
  );
};

export const Chip = ({children, delay = 0, style}: {children: ReactNode; delay?: number; style?: CSSProperties}) => {
  const frame = useCurrentFrame();
  const enter = easeOut(frame, delay, 18);
  return (
    <div style={{position: "absolute", padding: "13px 18px", borderRadius: 999, background: COLORS.white, color: COLORS.navy, fontSize: 17, fontWeight: 700, boxShadow: "0 18px 38px rgba(0,0,0,.35)", opacity: enter, transform: `translateX(${(1 - enter) * -70}px)`, ...style}}>
      {children}
    </div>
  );
};

export const Waveform = ({style}: {style?: CSSProperties}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{display: "flex", gap: 7, alignItems: "center", height: 70, ...style}}>
      {Array.from({length: 18}, (_, i) => {
        const height = 10 + Math.abs(Math.sin(frame / 6 + i * 0.7)) * 52;
        return <div key={i} style={{width: 6, height, borderRadius: 9, background: i % 3 === 0 ? COLORS.amber : COLORS.cyan, boxShadow: `0 0 12px ${COLORS.cyan}55`}} />;
      })}
    </div>
  );
};
