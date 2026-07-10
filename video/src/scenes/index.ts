import type {FC} from "react";
import type {SceneId} from "../story";
import {ArchitectureScene} from "./ArchitectureScene";
import {CloseScene, HookScene, PlanScene, type SceneProps} from "./IntroScenes";
import {BackendScene, DemoScene} from "./ReliabilityScenes";
import {AskScene, DocumentsScene, InboxScene, MinutesScene} from "./WorkflowScenes";

export const SCENE_COMPONENTS: Record<SceneId, FC<SceneProps>> = {
  hook: HookScene,
  plan: PlanScene,
  architecture: ArchitectureScene,
  minutes: MinutesScene,
  inbox: InboxScene,
  documents: DocumentsScene,
  ask: AskScene,
  backend: BackendScene,
  demo: DemoScene,
  close: CloseScene,
};
