// Exposes Tone.js types to IDE
import * as ToneModule from "tone";

declare global {
    const Tone: typeof ToneModule;
}
