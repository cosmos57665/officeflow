import {interpolate, useCurrentFrame} from "remotion";
import {CodexOrb} from "../components/CodexOrb";
import {PixelStudent} from "../components/PixelStudent";
import {KineticPhrase, NodeCard, UIFrame} from "../components/Primitives";
import {SceneShell} from "../components/SceneShell";
import {COLORS, easeOut} from "../theme";

export type SceneProps = {duration: number};

export const HookScene = ({duration}: SceneProps) => {
  const frame = useCurrentFrame();
  const subtitle = easeOut(frame, 42, 26);
  return (
    <SceneShell duration={duration} index={1} accent={COLORS.amber}>
      <KineticPhrase text="ONE IDEA" delay={12} style={{left: 105, top: 160}} />
      <div style={{position: "absolute", left: 115, top: 325, width: 690, color: COLORS.muted, fontSize: 36, lineHeight: 1.25, opacity: subtitle, transform: `translateY(${(1 - subtitle) * 25}px)`}}>
        Repetitive office work,
        <br />reimagined in seconds.
      </div>
      <PixelStudent pose={0} scale={1.12} style={{left: 205, bottom: -40}} />
      <CodexOrb size={210} style={{right: 310, top: 300}} label="AN IDEA BECOMES A SYSTEM" />
      <div style={{position: "absolute", right: 242, top: 600, width: 410, height: 1, background: `linear-gradient(90deg, transparent, ${COLORS.amber}, transparent)`, opacity: Math.sin(frame / 12) * 0.2 + 0.7}} />
    </SceneShell>
  );
};

export const PlanScene = ({duration}: SceneProps) => {
  const frame = useCurrentFrame();
  const line = interpolate(frame, [18, 120], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <SceneShell duration={duration} index={2}>
      <div style={{position: "absolute", left: 90, top: 142, fontSize: 26, color: COLORS.cyan, letterSpacing: 5, fontWeight: 700}}>SACHIN + CODEX</div>
      <div style={{position: "absolute", left: 90, top: 194, width: 780, fontSize: 78, lineHeight: 0.96, fontWeight: 780, letterSpacing: -4}}>
        From a prompt
        <br />to a product.
      </div>
      <PixelStudent pose={1} scale={1.2} style={{left: 65, bottom: -80}} />
      <CodexOrb size={145} style={{right: 110, top: 120}} />
      <div style={{position: "absolute", left: 840, top: 255, width: 780, height: 3, background: `linear-gradient(90deg, ${COLORS.cyan} ${line * 100}%, transparent ${line * 100}%)`}} />
      <NodeCard title="01 / Understand" detail="Four real office bottlenecks" delay={38} style={{position: "absolute", left: 890, top: 330, width: 520}} />
      <NodeCard title="02 / Architect" detail="Frontend, API, services, fallbacks" delay={64} accent={COLORS.amber} style={{position: "absolute", left: 1050, top: 500, width: 520}} />
      <NodeCard title="03 / Build" detail="A reliable full-stack demo" delay={90} style={{position: "absolute", left: 890, top: 670, width: 520}} />
    </SceneShell>
  );
};

export const CloseScene = ({duration}: SceneProps) => {
  const frame = useCurrentFrame();
  const reveal = easeOut(frame, 15, 35);
  const wink = frame > 150;
  return (
    <SceneShell duration={duration} index={10} accent={COLORS.amber}>
      <UIFrame screen="home" delay={0} style={{left: 360, top: 108, width: 1460, height: 910, filter: "brightness(.24) saturate(.7)", opacity: 0.45}} />
      <div style={{position: "absolute", inset: 0, background: "linear-gradient(90deg, #08111F 22%, transparent 66%), linear-gradient(0deg, #08111F 0%, transparent 42%)"}} />
      <div style={{position: "absolute", left: 105, top: 150, opacity: reveal, transform: `translateY(${(1 - reveal) * 40}px)`}}>
        <div style={{fontSize: 27, color: COLORS.cyan, letterSpacing: 6, fontWeight: 700}}>OFFICEFLOW</div>
        <div style={{fontSize: 100, fontWeight: 800, letterSpacing: -6, lineHeight: 0.95, marginTop: 28}}>
          One student.
          <br />One AI collaborator.
          <br /><span style={{color: COLORS.amber}}>One working idea.</span>
        </div>
      </div>
      <PixelStudent pose={wink ? 6 : 5} scale={1.05} style={{right: 290, bottom: -30}} />
      <CodexOrb size={150} wink={wink} label={wink ? "NICE WORK, SACHIN" : "CODEX"} style={{right: 120, top: 165}} />
      <div style={{position: "absolute", left: 112, bottom: 92, fontSize: 31, fontWeight: 600, letterSpacing: -0.5}}>
        Built by Sachin <span style={{color: COLORS.muted}}>with the help of</span> ChatGPT&apos;s Codex <span style={{color: COLORS.amber}}>;)</span>
      </div>
    </SceneShell>
  );
};
