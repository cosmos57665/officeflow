import "./index.css";
import { Composition } from "remotion";
import { OfficeFlowLaunch } from "./Composition";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="OfficeFlowLaunch"
      component={OfficeFlowLaunch}
      durationInFrames={2700}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
