// Exposes Tone.js types to IDE
import * as ToneModule from "tone";

declare global {
    const Tone: typeof ToneModule;

    // JS threw errors for recursive types (Subdivision)
    // You have to use an interface in TS as a workaround #cleancode
    interface Subdivisions extends Array<Subdivision> {}
    type Subdivision = number[] | Subdivisions;
    type Groove = Subdivision[];
}
