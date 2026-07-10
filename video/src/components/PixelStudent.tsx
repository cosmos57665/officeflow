import type {CSSProperties} from "react";
import {Img, staticFile, useCurrentFrame} from "remotion";

export type StudentPose = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;

export type PixelStudentProps = {
  pose: StudentPose;
  scale?: number;
  style?: CSSProperties;
  bob?: boolean;
};

const SOURCE_WIDTH = 1672;
const SOURCE_HEIGHT = 941;
const CELL_WIDTH = SOURCE_WIDTH / 4;
const CELL_HEIGHT = SOURCE_HEIGHT / 2;

export const PixelStudent = ({pose, scale = 0.88, style, bob = true}: PixelStudentProps) => {
  const frame = useCurrentFrame();
  const column = pose % 4;
  const row = Math.floor(pose / 4);
  const width = CELL_WIDTH * scale;
  const height = CELL_HEIGHT * scale;
  const y = bob ? Math.sin(frame / 11) * 4 : 0;

  return (
    <div
      style={{
        position: "absolute",
        width,
        height,
        overflow: "hidden",
        transform: `translateY(${y}px)`,
        filter: "drop-shadow(0 26px 28px rgba(0,0,0,.45))",
        ...style,
      }}
    >
      <Img
        src={staticFile("characters/student-sheet-v2.png")}
        style={{
          position: "absolute",
          width: SOURCE_WIDTH * scale,
          height: SOURCE_HEIGHT * scale,
          left: -column * CELL_WIDTH * scale,
          top: -row * CELL_HEIGHT * scale,
          imageRendering: "pixelated",
        }}
      />
    </div>
  );
};
