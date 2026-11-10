import copy
import random
from typing import override

from ..evolution_types import Groove, Subdivision
from ..util import get_random_velocity
from .genetic_algorithm import GA

### SETTINGS
POPULATION_SIZE = 15
TRACK_COUNT = 5

# INIT
INITIAL_MUTATIONS = 5
ACTIVE_CHANCE = 0.6

# EVOLUTION SETTINGS
CHANCE_TO_ONLY_MUTATE = 0.3
CHANCE_TO_ONLY_CROSSOVER = 0.3
# Otherwise mutate and crossover

# MUTATION SETTINGS (sum of first two should be < 1.0)
CHANCE_TO_MUTATE_CHILDREN = 0.1
CHANCE_TO_ADD_LEAF = 0.2

# CROSSOVER SETTINGS
CROSSOVER_METHOD_WEIGHT = 0.5
CHANCE_TO_REPLACE_WITH_GENE = 0.2
TRACK_BIAS = 0.8

# LEAF (sum of first three should be < 1.0)
CHANCE_TO_ADD_STEP = 0.2
CHANCE_TO_REMOVE_STEP = 0.2
CHANCE_TO_CHANGE_VELOCITIES = 0.2

### NO MORE SETTINGS



class TreeGA(GA):
    def __init__(self):
        self.population: list[Tree] = [Tree() for _ in range(POPULATION_SIZE)]

        for individual in self.population:
            for _ in range(INITIAL_MUTATIONS):
                individual.mutate()


    @override
    def evolve(self, parents: list[int]) -> None:
        new_population: list[Tree] = []
        parent_trees: list[Tree] = []
        for id in parents:
            parent_trees.append(self.population[id])

        for _ in range(POPULATION_SIZE):
            rand = random.random()
            if rand < CHANCE_TO_ONLY_MUTATE:
                new_individual: Tree = copy.deepcopy(random.choice(parent_trees))
                new_individual.mutate()
            else:
                new_individual: Tree = copy.deepcopy(random.choice(parent_trees))
                crossover_individual: Tree = copy.deepcopy(random.choice(parent_trees))  # crossover with itself is allowed

                new_individual.crossover(crossover_individual)

                if rand > CHANCE_TO_ONLY_MUTATE + CHANCE_TO_ONLY_CROSSOVER:
                    new_individual.mutate()

            new_population.append(new_individual)

        self.population = new_population


    @override
    def grooves(self) -> list[tuple[int, Groove]]:
        formatted_output: list[tuple[int, Groove]] = []
        for i in range(POPULATION_SIZE):
            individual: Groove = self.population[i].flatten()
            formatted_output.append((i, individual))

        return formatted_output


class Tree:
    def __init__(self) -> None:
        self.roots: list[TreeNode] = [TreeNode() for _ in range(TRACK_COUNT)]

    def mutate(self) -> None:
        for root in self.roots:
            root.mutate()

    def crossover(self, other: "Tree") -> None:
        if random.random() < CROSSOVER_METHOD_WEIGHT:
            self.gene_crossover(other)
        else:
            self.track_crossover(other)

    def gene_crossover(self, other: "Tree") -> None:
        gene: TreeNode = random.choice(other.roots).get_random_node_from_tree()
        for root in self.roots:
            root.replace_random_nodes(gene)

    def track_crossover(self, other: "Tree") -> None:
        new_roots: list[TreeNode] = []
        for i in range(TRACK_COUNT):
            if random.random() < TRACK_BIAS:
                new_roots.append(self.roots[i])
            else:
                new_roots.append(other.roots[i])

        self.roots = new_roots

    def flatten(self) -> Groove:
        return [root.flatten() for root in self.roots]


### MUTATIONS
# pass mutation to child(ren)
# remove child
# add new leaf
class TreeNode:
    def __init__(self):
        step = LeafNode()
        self.children: list[TreeNode] = [step]

    def flatten(self) -> Subdivision:
        flatlist: Subdivision = []
        for c in self.children:
            flatlist.append(c.flatten())

        return flatlist

    def get_random_node_from_tree(self) -> "TreeNode":
        return random.choice(self.children).get_random_node_from_tree()

    def replace_random_nodes(self, new_node: "TreeNode") -> None:
        for i in range(len(self.children)):
            if random.random() < CHANCE_TO_REPLACE_WITH_GENE:
                node_copy: TreeNode = copy.deepcopy(new_node)
                self.children[i] = node_copy
            else:
                self.children[i].replace_random_nodes(new_node)

    def mutate(self) -> None:
        rand: float = random.random()

        if rand < CHANCE_TO_MUTATE_CHILDREN:
            self.mutate_children()
        elif rand < CHANCE_TO_MUTATE_CHILDREN + CHANCE_TO_ADD_LEAF:
            self.add_leaf()

    def mutate_children(self) -> None:
        for c in self.children:
            c.mutate()

    def add_leaf(self) -> None:
        step = LeafNode()
        self.children.append(step)


### MUTATIONS
# add step to subdivision
# remove step from subdivision
# change step velocities
class LeafNode(TreeNode):
    def __init__(self):
        self.steps: list[float] = [get_random_velocity(active_chance=ACTIVE_CHANCE)]

    @override
    def flatten(self) -> Subdivision:
        return self.steps

    @override
    def get_random_node_from_tree(self) -> TreeNode:
        return self

    @override
    def replace_random_nodes(self, new_node: TreeNode) -> None:
        return

    @override
    def mutate(self) -> None:
        rand: float = random.random()

        if rand < CHANCE_TO_ADD_STEP:
            self.add_step()
        elif rand < CHANCE_TO_ADD_STEP + CHANCE_TO_REMOVE_STEP:
            self.remove_step()
        elif rand < CHANCE_TO_ADD_STEP + CHANCE_TO_REMOVE_STEP + CHANCE_TO_CHANGE_VELOCITIES:
            self.change_velocities()

    def add_step(self) -> None:
        self.steps.append(get_random_velocity(active_chance=ACTIVE_CHANCE))

    def remove_step(self) -> None:
        if len(self.steps) > 1:
            _ = self.steps.pop()

    def change_velocities(self) -> None:
        for i in range(len(self.steps)):
            self.steps[i] = get_random_velocity(active_chance=ACTIVE_CHANCE)
