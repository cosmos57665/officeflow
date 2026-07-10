import {interpolate, useCurrentFrame} from "remotion";
import {CodexOrb} from "../components/CodexOrb";
import {PixelStudent} from "../components/PixelStudent";
import {FlowLine, KineticPhrase, NodeCard, UIFrame} from "../components/Primitives";
import {SceneShell} from "../components/SceneShell";
import {COLORS, easeOut} from "../theme";
import type {SceneProps} from "./IntroScenes";

export const BackendScene = ({duration}: SceneProps) => {
  const frame = useCurrentFrame();
  const shield = easeOut(frame, 118, 28);
  return (
    <SceneShell duration={duration} index={8}>
      <KineticPhrase text="POWERED BY GEMINI" delay={8} style={{left: 76, top: 128, fontSize: 96}} />
      <div style={{position: "absolute", left: 85, top: 250, color: COLORS.muted, fontSize: 25}}>
        Primary intelligence. Graceful fallbacks. Guarded operations.
      </div>

      <NodeCard title="FastAPI boundary" detail="Validation · safe errors · file limits" delay={36} style={{position: "absolute", left: 430, top: 390, width: 330}} />
      <FlowLine from={{left: 790, top: 467}} width={190} delay={58} />
      <NodeCard title="Gemini 2.5 Flash" detail="Primary runtime AI provider" delay={70} accent={COLORS.cyan} style={{position: "absolute", left: 1005, top: 365, width: 390, padding: "34px 32px"}} />
      <FlowLine from={{left: 1425, top: 467}} width={150} delay={90} color={COLORS.amber} />
      <CodexOrb size={160} style={{left: 1600, top: 375}} label="BUILT WITH CODEX" />

      <NodeCard title="Groq" detail="Provider fallback" delay={105} style={{position: "absolute", left: 920, top: 630, width: 255}} />
      <NodeCard title="OpenRouter" detail="Provider fallback" delay={117} style={{position: "absolute", left: 1200, top: 630, width: 255}} />
      <div style={{position: "absolute", left: 520, top: 675, width: 250, padding: 28, borderRadius: 26, border: `2px solid ${COLORS.amber}`, background: "rgba(255,180,84,.09)", opacity: shield, transform: `scale(${0.78 + shield * 0.22})`, textAlign: "center"}}>
        <div style={{fontSize: 52}}>◆</div>
        <div style={{fontSize: 21, fontWeight: 800, color: COLORS.amber, letterSpacing: 2}}>GUARDED</div>
        <div style={{fontSize: 16, color: COLORS.muted, marginTop: 8}}>Friendly failures, never stack traces</div>
      </div>
      <PixelStudent pose={4} scale={0.82} style={{left: 42, bottom: -32}} />
    </SceneShell>
  );
};

export const DemoScene = ({duration}: SceneProps) => {
  const frame = useCurrentFrame();
  const toggle = easeOut(frame, 65, 20);
  const outage = interpolate(frame, [10, 52], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <SceneShell duration={duration} index={9} accent={COLORS.amber}>
      <UIFrame screen="home" delay={0} style={{left: 485, top: 135, width: 1350, height: 845, filter: "brightness(.58)"}} />
      <KineticPhrase text="RELIABILITY FIRST" delay={10} style={{left: 72, top: 130, width: 700, fontSize: 86}} />
      <PixelStudent pose={6} scale={0.94} style={{left: 75, bottom: -25}} />

      <div style={{position: "absolute", left: 285, top: 390, width: 220, padding: 22, borderRadius: 22, background: "#311722", border: "1px solid #FF7282", opacity: outage, transform: `rotate(${(1 - outage) * -8}deg) scale(${0.8 + outage * 0.2})`}}>
        <div style={{fontSize: 46, color: "#FF7282", fontWeight: 850}}>WI-FI ×</div>
        <div style={{fontSize: 17, color: "#FFB7C0", marginTop: 8}}>Connection unavailable</div>
      </div>

      <div style={{position: "absolute", left: 830, top: 700, width: 470, padding: "28px 34px", borderRadius: 28, background: "rgba(8,17,31,.96)", border: `1px solid ${COLORS.cyan}`, boxShadow: `0 30px 80px rgba(0,0,0,.45), 0 0 42px ${COLORS.cyan}22`}}>
        <div style={{fontSize: 18, color: COLORS.muted, letterSpacing: 3, fontWeight: 700}}>DEMO MODE</div>
        <div style={{display: "flex", alignItems: "center", gap: 22, marginTop: 18}}>
          <div style={{width: 112, height: 54, borderRadius: 999, background: toggle > 0.5 ? COLORS.teal : "#334155", padding: 6}}>
            <div style={{width: 42, height: 42, borderRadius: "50%", background: COLORS.white, transform: `translateX(${toggle * 58}px)`, boxShadow: "0 5px 14px rgba(0,0,0,.3)"}} />
          </div>
          <div style={{fontSize: 24, fontWeight: 750, color: toggle > 0.5 ? COLORS.cyan : COLORS.muted}}>
            {toggle > 0.5 ? "CACHED OUTPUTS READY" : "CONNECTING…"}
          </div>
        </div>
      </div>
    </SceneShell>
  );
};
