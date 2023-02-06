# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')

sys.path.insert(1, '../')
from utility import *


class AI():
    isExpectimax: bool = False
    reccursionDepth: int = 3
    reward_max: int = 50
    reward_min: int = -50
    nodes_explored_count: int = 0

    def get_next_move(self, wrld, alpha=-float("inf"), beta=float("inf")):
        # if there are no monsters, just go to the exit
        if len(wrld.monsters) == 0:
            path = a_star(wrld, (wrld.exitcell[0], wrld.exitcell[1]),
                          (character_location(wrld)[0], character_location(wrld)[1]))
            if path is None:  # Blocked in by explosion, wait until it goes away
                return character_location(wrld)
            return path[1]
            # Get the next move using minimax with alpha-beta pruning
        possible_moves = eight_neighbors(wrld, character_location(wrld)[0], character_location(wrld)[1])
        # possible_moves.append(character_location(wrld))
        prioritize_moves_for_self(wrld, possible_moves)
        values = []
        for move in possible_moves:
            value = self.get_value_of_state(wrld, move, monster_location(wrld), 0, alpha, beta)
            values.append(value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        print("Pruned", round(self.nodes_explored_count / 9 ** (self.reccursionDepth + 1) * 100), "% of the tree.",
              self.nodes_explored_count, "nodes explored.")
        self.nodes_explored_count = 0
        if len(values) == 0:
            return character_location(wrld)
        print(max(values), values)
        if min(values) < 0:
            print("No good moves")
        return possible_moves[values.index(max(values))]

    def get_value_of_state(self, wrld, self_pos, monster_pos, depth, alpha, beta):
        self.nodes_explored_count += 1
        if self_pos == wrld.exitcell:
            return 300 - depth

        if wrld.explosion_at(self_pos[0], self_pos[1]):
            return -100 - depth

        if self_pos in eight_neighbors(wrld, monster_pos[0], monster_pos[1]) or self_pos == monster_pos:
            return -100 - depth

        if depth == self.reccursionDepth:
            return evaluate_state(wrld, self_pos, monster_pos) - depth

        if depth % 2 == 1:  # Max Node (self)
            value = -float("inf")
            possible_moves = eight_neighbors(wrld, self_pos[0], self_pos[1])
            possible_moves.append(self_pos)
            for self_move in possible_moves:
                value = max(value, self.get_value_of_state(wrld, self_move, monster_pos, depth + 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:

            if not self.isExpectimax:  # If modeling monster as Minimax
                value = float("inf")
                possible_moves = eight_neighbors(wrld, monster_pos[0], monster_pos[1])
                possible_moves.append(monster_pos)
                for monster_move in possible_moves:
                    value = min(value, self.get_value_of_state(wrld, self_pos, monster_move, depth + 1, alpha, beta))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return value
            else:  # If Expectimax
                value = 0
                probability_total = 0
                possible_moves = eight_neighbors(wrld, monster_pos[0], monster_pos[1])
                possible_moves.append(monster_pos)
                for monster_move in possible_moves:
                    probability = 1 / len(possible_moves)
                    probability_total += probability
                    value += self.get_value_of_state(wrld, self_pos, monster_move, depth + 1, alpha,
                                                     beta) * probability
                    remaining_probability = 1 - probability_total
                    if value + (remaining_probability * self.reward_max) < alpha:
                        # print("Pruned expected node with remaining probability", remaining_probability)
                        break
                return value


def prioritize_moves_for_self(wrld, possible_moves):
    # Prioritize moves that are closer to the exit to prune the tree more
    possible_moves.sort(key=lambda move: euclidean_distance_to_exit(wrld, move))


def prioritize_moves_for_monster(wrld, possible_moves):
    # Prioritize moves that are closer to the exit to prune the tree more
    possible_moves.sort(key=lambda move: euclidean_dist(move, character_location(wrld)))


def evaluate_state(wrld, characterLocation=None, monsterLocation=None):
    """Returns a value for the current world state.
    wrld: World object
    returns: float"""
    # print("Evaluating state with character location: " + str(characterLocation) + " and monster location: " + str(monsterLocation))
    if characterLocation is None:
        characterLocation = character_location(wrld)
    if monsterLocation is None:
        monsterLocation = monster_location(wrld)

    number_of_move_options = len(eight_neighbors(wrld, characterLocation[0], characterLocation[1]))
    distance_to_exit = a_star_distance(wrld, characterLocation, wrld.exitcell)
    if len(wrld.monsters) == 0:
        return int(distance_to_exit * 5) + number_of_move_options * 10
    distance_to_monster = a_star_distance(wrld, characterLocation, monsterLocation)
    if distance_to_monster <= 2:  # The monster is within one tile away
        return -100
    return int((distance_to_monster * 5) - distance_to_exit * 6) + number_of_move_options * 5
