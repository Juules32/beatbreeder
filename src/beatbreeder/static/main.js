const evolveButton = /** @type {HTMLButtonElement} */ (document.getElementById("evolve"));
const selectedCount = document.getElementById("selected-count");
const legend = document.getElementById("legend");
const grid = document.getElementById("grid");
const solutionTemplate = /** @type {HTMLTemplateElement} */ (document.getElementById("solution-template"));

const NAMES = ["Hi-hat", "Snare", "Mid Tom", "Low Tom", "Kick"];
const COLORS = ["#00ff00", "#0000ff", "#ffff00", "#00ffff", "#ff0000"];
const STEPS = 16;
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

/** @typedef {{ id: string, phenotype: boolean[][] }} Solution */
/** @typedef {{ solution: Solution, element: HTMLElement, canvas: HTMLCanvasElement }} Tile */

// The tile being played
/** @type {Tile | null} */
let playing = null;

// Ids of selected parents
/** @type {Set<string>} */
const selected = new Set();

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
new Tone.Sequence(
    (time, step) => playing?.solution.phenotype.forEach((row, i) => {
        if (row[step]) {
            drumSounds[i].start(time);
        }
    }),
    [...Array(STEPS).keys()], // All the steps [0, 1, ..., 15]
    "16n", // Time between steps
).start(0);

/**
 * @param {string} algorithm
 * @param {string[]} parents
 * @returns {Promise<Solution[]>}
 */
async function generate(algorithm, parents) {
    const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algorithm, parents }),
    });
    if (!response.ok) {
        throw new Error(`Generating failed: ${JSON.stringify(await response.json())}`);
    }
    return (await response.json()).solutions;
}

function stop() {
    Tone.Transport.stop(Tone.immediate());
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
    const w = canvas.width / STEPS;
    const h = canvas.height / NAMES.length;
    const p = 1; // Padding
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    solution.phenotype.forEach((row, y) => {
        row.forEach((on, x) => {
            ctx.fillStyle = on ? COLORS[y] : "#000000";
            ctx.fillRect(x * w + p, y * h + p, w - p * 2, h - p * 2);
        });
    });
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
        element.dataset.id = solution.id;
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
