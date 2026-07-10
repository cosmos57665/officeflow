import {Audio} from "@remotion/media";
import {AbsoluteFill, interpolate, Sequence, staticFile} from "remotion";
import "./fonts";
import {SCENE_COMPONENTS} from "./scenes";
import {SCENES} from "./story";
import {COLORS} from "./theme";

const effects = [
  {from: 210, file: "whoosh.wav", volume: 0.055},
  {from: 450, file: "whoosh.wav", volume: 0.045},
  {from: 810, file: "switch.wav", volume: 0.04},
  {from: 2315, file: "switch.wav", volume: 0.09},
  {from: 2610, file: "ding.wav", volume: 0.075},
];

export const OfficeFlowLaunch = () => (
  <AbsoluteFill style={{background: COLORS.navy}}>
    <Audio
      src={staticFile("audio/music-stylz.mp3")}
      volume={(frame) =>
        interpolate(frame, [0, 36, 2640, 2699], [0, 0.075, 0.075, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      }
    />
    {SCENES.map((scene) => {
      const Scene = SCENE_COMPONENTS[scene.id];
      return (
        <Sequence key={scene.id} from={scene.from} durationInFrames={scene.duration} premountFor={30}>
          <Audio src={staticFile(`audio/voice/${scene.id}.mp3`)} volume={() => 1} />
          <Scene duration={scene.duration} />
        </Sequence>
      );
    })}
    {effects.map((effect) => (
      <Sequence key={`${effect.file}-${effect.from}`} from={effect.from} premountFor={15}>
        <Audio src={staticFile(`audio/${effect.file}`)} volume={() => effect.volume} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
