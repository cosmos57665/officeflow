import {loadFont} from "@remotion/fonts";
import {staticFile} from "remotion";

if (typeof FontFace !== "undefined") {
  for (const weight of ["400", "600", "800"]) {
    void loadFont({
      family: "Geist",
      url: staticFile("fonts/Geist-Variable.woff2"),
      weight,
    });
  }
}
