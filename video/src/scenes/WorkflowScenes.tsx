import type {ReactNode} from "react";
import {useCurrentFrame} from "remotion";
import {PixelStudent, type StudentPose} from "../components/PixelStudent";
import {Chip, KineticPhrase, UIFrame, Waveform} from "../components/Primitives";
import {SceneShell} from "../components/SceneShell";
import {COLORS, easeOut} from "../theme";
import type {SceneProps} from "./IntroScenes";

type WorkflowStageProps = SceneProps & {
  index: number;
  module: string;
  headline: ReactNode;
  screen: "minutes" | "inbox" | "documents" | "ask";
  pose: StudentPose;
  accent?: string;
  children?: ReactNode;
};

const WorkflowStage = ({duration, index, module, headline, screen, pose, accent = COLORS.cyan, children}: WorkflowStageProps) => {
  const frame = useCurrentFrame();
  const enter = easeOut(frame, 20, 25);
  return (
    <SceneShell duration={duration} index={index} accent={accent}>
      <div style={{position: "absolute", left: 80, top: 135, width: 430, opacity: enter, transform: `translateX(${(1 - enter) * -45}px)`}}>
        <div style={{fontSize: 18, color: accent, letterSpacing: 5, fontWeight: 750}}>{module}</div>
        <div style={{fontSize: 66, fontWeight: 800, lineHeight: 0.98, letterSpacing: -3.5, marginTop: 20}}>{headline}</div>
      </div>
      <UIFrame screen={screen} delay={16} style={{left: 530, top: 152, width: 1310, height: 820}} />
      <PixelStudent pose={pose} scale={0.98} style={{left: 70, bottom: -30}} />
      {children}
    </SceneShell>
  );
};

export const MinutesScene = ({duration}: SceneProps) => (
  <WorkflowStage duration={duration} index={4} module="WORKFLOW 01" headline={<>Audio to<br /><span style={{color: COLORS.amber}}>action.</span></>} screen="minutes" pose={1} accent={COLORS.amber}>
    <KineticPhrase text="FOUR WORKFLOWS" delay={5} style={{right: 76, top: 78, fontSize: 42, letterSpacing: 4, color: COLORS.muted}} />
    <Waveform style={{position: "absolute", left: 96, top: 430}} />
    <Chip delay={78} style={{left: 415, top: 350}}>AUDIO</Chip>
    <Chip delay={96} style={{left: 445, top: 445, background: COLORS.cyan}}>WHISPER</Chip>
    <Chip delay={114} style={{left: 425, top: 540, background: COLORS.amber}}>WORD</Chip>
  </WorkflowStage>
);

export const InboxScene = ({duration}: SceneProps) => (
  <WorkflowStage duration={duration} index={5} module="WORKFLOW 02" headline={<>Signal from<br /><span style={{color: COLORS.cyan}}>the noise.</span></>} screen="inbox" pose={4}>
    <Chip delay={54} style={{right: 106, top: 220, background: "#FFD9D5"}}>URGENT · 2</Chip>
    <Chip delay={74} style={{right: 106, top: 305, background: "#FFF0C8"}}>ACTION · 3</Chip>
    <Chip delay={94} style={{right: 106, top: 390, background: "#D7F8EE"}}>FYI · 3</Chip>
  </WorkflowStage>
);

export const DocumentsScene = ({duration}: SceneProps) => {
  const frame = useCurrentFrame();
  const enter = easeOut(frame, 60, 28);
  return (
    <WorkflowStage duration={duration} index={6} module="WORKFLOW 03" headline={<>One CSV.<br /><span style={{color: COLORS.amber}}>Twenty PDFs.</span></>} screen="documents" pose={7} accent={COLORS.amber}>
      <div style={{position: "absolute", left: 420, top: 400, display: "grid", gridTemplateColumns: "repeat(3, 42px)", gap: 8, opacity: enter, transform: `scale(${0.8 + enter * 0.2})`}}>
        {Array.from({length: 9}, (_, i) => <div key={i} style={{width: 42, height: 32, borderRadius: 5, background: i % 2 ? COLORS.amber : COLORS.cyan, opacity: 0.75}} />)}
      </div>
      <Chip delay={100} style={{left: 405, top: 565}}>CSV → PDF → ZIP</Chip>
    </WorkflowStage>
  );
};

export const AskScene = ({duration}: SceneProps) => (
  <WorkflowStage duration={duration} index={7} module="WORKFLOW 04" headline={<>Ask once.<br /><span style={{color: COLORS.cyan}}>Find exactly.</span></>} screen="ask" pose={2}>
    <div style={{position: "absolute", left: 345, top: 350, width: 270, padding: 22, borderRadius: "24px 24px 24px 4px", background: COLORS.white, color: COLORS.navy, fontSize: 20, fontWeight: 650, boxShadow: "0 24px 60px rgba(0,0,0,.35)"}}>
      “What is the deadline?”
    </div>
    <Chip delay={92} style={{left: 425, top: 500, background: COLORS.cyan}}>ANSWER · p. 4</Chip>
  </WorkflowStage>
);
