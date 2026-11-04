const evolveButton = /** @type {HTMLButtonElement} */ (document.getElementById("evolve"));
const selectedCount = document.getElementById("selected-count");
const legend = document.getElementById("legend");
const grid = document.getElementById("grid");
const solutionTemplate = /** @type {HTMLTemplateElement} */ (document.getElementById("solution-template"));

const NAMES = ["Hi-hat", "Snare", "Mid Tom", "Low Tom", "Kick"];
const COLORS = ["#00ff00", "#0000ff", "#ffff00", "#00ffff", "#ff0000"];
const MAX_PARENTS = 5;

// Sounds from: https://github.com/Tonejs/audio
const hiHat = new Tone.Player("/static/hihat.mp3").toDestination();
const snare = new Tone.Player("/static/snare.mp3").toDestination();
const midTom = new Tone.Player("/static/mid_tom.mp3").toDestination();
const lowTom = new Tone.Player("/static/low_tom.mp3").toDestination();
const kick = new Tone.Player("/static/kick.mp3").toDestination();
const drumSounds = [
    hiHat,
    snare,
    midTom,
    lowTom,
    kick,
];

/** @typedef {{ id: number, groove: Groove }} Solution */
/** @typedef {{ solution: Solution, element: HTMLElement, canvas: HTMLCanvasElement }} Tile */

// The tile being played
/** @type {Tile | null} */
let playing = null;

// The current tile's Tone.js part, meaning how it schedules its rhythm (Different for each individual)
/** @type {import("tone").Part | null} */
let part = null;

// Ids of selected parents
/** @type {Set<number>} */
const selected = new Set();

// Id of the current generation, assigned by the server
/** @type {string | null} */
let gid = null;

// Legend
NAMES.forEach((name, i) => {
    const legendColor = document.createElement("span");
    legendColor.className = "legend-color";
    legendColor.style.backgroundColor = COLORS[i];
    const span = document.createElement("span");
    span.append(legendColor, name);
    legend.append(span);
});

Tone.Transport.bpm.value = 120;
Tone.Transport.loop = true;
Tone.Transport.loopEnd = '1m'; // One measure. Removing this line will make your ears bleed!

/**
 * Recursively visits each note in Subdivision so you can apply a function (visit)
 * to each leaf using its start position, length and velocity.
 * @param {Subdivision} subdivision
 * @param {number} start
 * @param {number} length
 * @param {(start: number, length: number, velocity: number) => void} visit
 */
function walk(subdivision, start, length, visit) {
    if (subdivision.length == 0) {
        return;
    }
    const childLength = length / subdivision.length;
    subdivision.forEach((child, i) => {
        const childStart = start + i * childLength;
        if (Array.isArray(child)) {
            walk(child, childStart, childLength, visit);
        } else {
            const velocity = Math.min(Math.max(Number(child), 0), 1);
            visit(childStart, childLength, velocity);
        }
    });
}

/**
 * @param {string} algorithm
 * @param {number[]} pids
 * @returns {Promise<Solution[]>}
 */
async function generate(algorithm, pids) {
    const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algorithm, gid, pids }),
    });
    if (!response.ok) {
        throw new Error(`Generating failed: ${JSON.stringify(await response.json())}`);
    }
    const data = await response.json();
    gid = data.gid;
    return data.grooves.map(([id, groove]) => ({ id, groove }));
}

function stop() {
    Tone.Transport.stop(Tone.immediate());
    part?.dispose(); // Prevents multiple parts to play at once
    part = null;
    if (playing) {
        playing.element.classList.remove("playing");
        draw(playing, false);
    }
    playing = null;
}

/** @param {Tile} tile */
async function play(tile) {
    stop();
    await Tone.start();
    await Tone.loaded();
    const measure = Tone.Time("1m").toSeconds();
    const hits = [];
    tile.solution.groove.forEach((subdivision, track) => {
        walk(subdivision, 0, 1, (start, _length, velocity) => {
            if (velocity > 0) {
                hits.push([start * measure, { track, velocity }]);
            }
        });
    });
    part = new Tone.Part((time, { track, velocity }) => {
        const sound = drumSounds[track];
        sound.volume.setValueAtTime(Tone.gainToDb(velocity), time);
        sound.start(time);
    }, hits).start(0);
    playing = tile;
    tile.element.classList.add("playing");
    Tone.Transport.start();
}

// What happens when right-clicking solutions
/** @param {Tile} tile */
function toggleSelected({ solution, element }) {
    if (selected.has(solution.id)) {
        selected.delete(solution.id);
    } else if (selected.size < MAX_PARENTS) {
        selected.add(solution.id);
    }
    element.classList.toggle("selected", selected.has(solution.id));
    updateSelection();
}

function updateSelection() {
    evolveButton.disabled = selected.size == 0;
    selectedCount.textContent = `${selected.size}/${MAX_PARENTS} selected`;
}

/**
 * @param {Tile} tile
 * @param {boolean} playhead
 */
function draw({ solution, canvas }, playhead) {
    const ctx = canvas.getContext("2d");
    const h = canvas.height / NAMES.length;
    const p = 1; // Padding
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    solution.groove.forEach((subdivision, y) => {
        walk(subdivision, 0, 1, (start, length, velocity) => {
            const x = start * canvas.width;
            const w = length * canvas.width;
            const rect = ([x + p, y * h + p, w - p * 2, h - p * 2]);
            ctx.globalAlpha = 1;
            ctx.fillStyle = "#000000";
            ctx.fillRect(rect[0], rect[1], rect[2], rect[3]);
            if (velocity > 0) {
                ctx.globalAlpha = velocity;
                ctx.fillStyle = COLORS[y];
                ctx.fillRect(rect[0], rect[1], rect[2], rect[3]);
            }
        });
    });
    ctx.globalAlpha = 1;
    if (playhead) {
        const bar = Tone.Transport.PPQ * 4; // Number of ticks in a bar
        const x = Tone.Transport.getTicksAtTime(Tone.immediate()) / bar * canvas.width;
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(x - p, 0, p * 2, canvas.height);
    }
}

// Setup and drawing of initial as well as subsequent solutions
/** @param {Solution[]} solutions */
function render(solutions) {
    stop();
    selected.clear();
    updateSelection();
    grid.replaceChildren(...solutions.map(solution => {
        const element = /** @type {HTMLElement} */ (solutionTemplate.content.firstElementChild.cloneNode(true)); // Solution div
        const tile = { solution, element, canvas: element.querySelector("canvas") };
        element.dataset.id = solution.id.toString();
        element.onclick = () => {
            if (playing == tile) {
                stop();
            } else {
                play(tile);
            }
        };
        element.oncontextmenu = event => {
            event.preventDefault();
            toggleSelected(tile);
        };
        draw(tile, false);
        return element;
    }));
}

async function evolve() {
    render(await generate("random", [...selected]));
}

evolveButton.onclick = evolve;
generate("random", []).then(render);

(function animate() {
    if (playing) {
        draw(playing, true);
    }
    requestAnimationFrame(animate);
})();
