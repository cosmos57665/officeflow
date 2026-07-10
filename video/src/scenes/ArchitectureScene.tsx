import {useCurrentFrame} from "remotion";
import {PixelStudent} from "../components/PixelStudent";
import {FlowLine, KineticPhrase, NodeCard} from "../components/Primitives";
import {SceneShell} from "../components/SceneShell";
import {COLORS, easeOut} from "../theme";
import type {SceneProps} from "./IntroScenes";

const services = ["MINUTES", "INBOX", "DOCS", "ASK PDF"];

export const ArchitectureScene = ({duration}: SceneProps) => {
  const frame = useCurrentFrame();
  const serviceEnter = easeOut(frame, 118, 28);
  return (
    <SceneShell duration={duration} index={3}>
      <KineticPhrase text="REACT + FASTAPI" delay={8} style={{left: 82, top: 125, fontSize: 104}} />
      <div style={{position: "absolute", left: 92, top: 255, color: COLORS.muted, fontSize: 25, letterSpacing: 1}}>
        A clean full-stack path from interface to useful output.
      </div>

      <NodeCard title="React / Vite" detail="Fast, focused interface" delay={30} style={{position: "absolute", left: 390, top: 390, width: 260}} />
      <FlowLine from={{left: 675, top: 465}} width={160} delay={52} />
      <NodeCard title="FastAPI" detail="Typed API boundary" delay={62} accent={COLORS.amber} style={{position: "absolute", left: 850, top: 390, width: 260}} />
      <FlowLine from={{left: 1135, top: 465}} width={160} delay={84} color={COLORS.amber} />
      <NodeCard title="Services" detail="One workflow, one job" delay={94} style={{position: "absolute", left: 1310, top: 390, width: 260}} />

      <div style={{position: "absolute", left: 545, top: 650, display: "flex", gap: 20, opacity: serviceEnter, transform: `translateY(${(1 - serviceEnter) * 30}px)`}}>
        {services.map((service, index) => (
          <div key={service} style={{width: 220, padding: "22px 18px", borderRadius: 18, textAlign: "center", background: index % 2 ? "rgba(255,180,84,.08)" : "rgba(98,230,209,.08)", border: `1px solid ${index % 2 ? COLORS.amber : COLORS.cyan}44`, fontSize: 19, fontWeight: 750, letterSpacing: 2}}>
            {service}
          </div>
        ))}
      </div>

      <div style={{position: "absolute", left: 660, top: 805, display: "flex", gap: 24}}>
        {["GEMINI PRIMARY", "WHISPER LOCAL", "PYMUPDF", "DOCX + PDF"].map((tool, index) => (
          <div key={tool} style={{padding: "11px 16px", borderRadius: 999, color: index === 0 ? COLORS.navy : COLORS.muted, background: index === 0 ? COLORS.cyan : "rgba(255,255,255,.04)", border: `1px solid ${COLORS.line}`, fontSize: 15, fontWeight: 700}}>
            {tool}
          </div>
        ))}
      </div>
      <PixelStudent pose={4} scale={0.92} style={{left: 20, bottom: -25}} />
    </SceneShell>
  );
};
