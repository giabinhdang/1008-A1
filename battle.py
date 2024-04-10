from __future__ import annotations
from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from pokemon_base import Pokemon
from data_structures.stack_adt import Stack
from data_structures.queue_adt import *
from data_structures.array_sorted_list import *
from data_structures.abstract_list import *
from math import ceil

class Battle:

    # Time complexity: O(1), sets up attributes and inializes data structures
    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    # Time complexity: O(1), do not depend on the size of the data
    def commence_battle(self) -> Trainer | None:
        if self.battle_mode == BattleMode.SET:
            return self.set_battle()
        elif self.battle_mode == BattleMode.ROTATE:
            return self.rotate_battle()
        elif self.battle_mode == BattleMode.OPTIMISE:
            return self.optimise_battle()
        else:
            raise ValueError("Invalid battle mode.")

    # Time complexity: O(n), where n is the number of Pokémon in the larger team
    def set_battle(self) -> Trainer | None:
        while not self.trainer_1.get_team().is_empty() and not self.trainer_2.get_team().is_empty():
            # Assuming `pop` method retrieves a Pokémon for battle and reduces team count
            pokemon1 = self.trainer_1.get_team().pop()
            pokemon2 = self.trainer_2.get_team().pop()
            # Simulate the battle round
            winner = self.battle_round(pokemon1, pokemon2)
            # Handle the battle outcome
            if winner is pokemon1:
                # If Pokémon 1 wins and is still healthy, push it back to its team; otherwise, it's removed
                if pokemon1.get_health() > 0:
                    self.trainer_1.get_team().push(pokemon1)
                # Pokémon 2 is not returned to its team since it lost
            elif winner is pokemon2:
                # If Pokémon 2 wins and is still healthy, push it back to its team; otherwise, it's removed
                if pokemon2.get_health() > 0:
                    self.trainer_2.get_team().push(pokemon2)
                # Pokémon 1 is not returned to its team since it lost
            #If there's no winner (both faint), neither Pokémon is returned to their teams

        # Determine the winner based on remaining Pokémon
        if self.trainer_1.get_team().is_empty() and not self.trainer_2.get_team().is_empty():
            return self.trainer_2
        elif not self.trainer_1.get_team().is_empty() and self.trainer_2.get_team().is_empty():
            return self.trainer_1
        else:
            return None  #It's a draw if both teams are empty


    # Time complexity: O(n), where n is the number of Pokémon in the larger team
    def rotate_battle(self) -> Trainer | None:
        team_1 = self.trainer_1.get_team().team
        team_2 = self.trainer_2.get_team().team

        while len(team_1) > 0 and len(team_2) > 0:
            pokemon1 = team_1.serve()
            pokemon2 = team_2.serve()
            if pokemon1 is None:
                return self.trainer_2
            elif pokemon2 is None:
                return self.trainer_1
            else:
                winner = self.battle_round(pokemon1, pokemon2)
                if winner == pokemon1 and pokemon1 is not None:
                    team_1.append(pokemon1)
                elif winner == pokemon2 and pokemon2 is not None:
                    team_2.append(pokemon2)
        if len(team_1) == 0:
            return self.trainer_2
        else:
            return self.trainer_1

    # Time complexity: O(n), ideal situation regarding the order of Pokemon and battle outcomes
    # Worst case scenario: O(n^2), if re-sorting as Pokemon are added back to the team
    def optimise_battle(self) -> Trainer | None:
        team_1 = ArraySortedList(len(self.trainer_1.get_team()))
        team_2 = ArraySortedList(len(self.trainer_2.get_team()))

        for pokemon in self.trainer_1.get_team():
            if pokemon is not None:
                team_1.add(pokemon)
        for pokemon in self.trainer_2.get_team():
            if pokemon is not None:
                team_2.add(pokemon)

        self.trainer_1.get_team().team = team_1
        self.trainer_2.get_team().team = team_2

        while len(team_1) > 0 and len(team_2) > 0:
            pokemon1 = team_1.delete_at_index(0)
            pokemon2 = team_2.delete_at_index(0)

            if pokemon1.level > pokemon2.level:
                team_1.add(pokemon1)
            elif pokemon1.level < pokemon2.level:
                team_2.add(pokemon2)
            else:
                team_1.add(pokemon1)
                team_2.add(pokemon2)

        if len(team_1) == 0:
            return self.trainer_2
        elif len(team_2) == 0:
            return self.trainer_1
        else:
            return None
        
    def _create_teams(self) -> None:
        # Time complexity: O(n), where n is the number of Pokémon in the team
        if self.battle_mode == BattleMode.SET:
            self.trainer_1.get_team().assemble_team(BattleMode.SET)
            self.trainer_2.get_team().assemble_team(BattleMode.SET)
        # Time complexity: O(n), where n is the number of Pokémon in the team
        elif self.battle_mode == BattleMode.ROTATE:
            self.trainer_1.get_team().assemble_team(BattleMode.ROTATE)
            self.trainer_2.get_team().assemble_team(BattleMode.ROTATE)
        # Time complexity: O(n log n), depends on the sorting algorithm used
        # Worst case scenario: O(n^2), depends on the sorting algorithm used
        elif self.battle_mode == BattleMode.OPTIMISE:
            self.trainer_1.get_team().assemble_team(BattleMode.OPTIMISE)
            self.trainer_2.get_team().assemble_team(BattleMode.OPTIMISE)
        else:
            raise ValueError("Invalid battle mode.")
        
    # Time complexity: O(1), do not depend on the size of the data
    def battle_round(self, pokemon1: Pokemon, pokemon2: Pokemon) -> Pokemon | None:
        p1_multiplier = self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion()
        p2_multiplier = self.trainer_2.get_pokedex_completion() / self.trainer_1.get_pokedex_completion()

        if pokemon1.speed > pokemon2.speed:
            first_attacker = pokemon1
            second_attacker = pokemon2
            first_multiplier = p1_multiplier
            second_multiplier = p2_multiplier
        else:
            first_attacker = pokemon2
            second_attacker = pokemon1
            first_multiplier = p2_multiplier
            second_multiplier = p1_multiplier

        damage = self.calculate_damage(first_attacker, second_attacker, first_multiplier)
        second_attacker.health -= damage
    
        if second_attacker.health <= 0:
            first_attacker.level_up()
            if first_attacker is pokemon1:
                self.trainer_1.update_pokedex_completion(first_attacker)
            else:
                self.trainer_2.update_pokedex_completion(first_attacker)

            return first_attacker

        # Counterattack if the second attacker is still standing
        if first_attacker.speed == second_attacker.speed or second_attacker.health > 0:
            counter_damage = self.calculate_damage(second_attacker, first_attacker, second_multiplier)
            first_attacker.health -= counter_damage
            if first_attacker.health <= 0:
                second_attacker.level_up()
                if second_attacker is pokemon2:
                    self.trainer_2.update_pokedex_completion(second_attacker)
                else:
                    self.trainer_1.update_pokedex_completion(second_attacker)

                return second_attacker

        # Aftermath check: if both Pokemon still stand, each loses 1 HP due to battle fatigue
        if first_attacker.health > 0 and second_attacker.health > 0:
            first_attacker.health -= 1
            second_attacker.health -= 1
            # Check for fainting after losing 1 HP
            if first_attacker.health <= 0:
                second_attacker.level_up()
                if second_attacker is pokemon2:
                    self.trainer_2.update_pokedex_completion(second_attacker)
                else:
                    self.trainer_1.update_pokedex_completion(second_attacker)

                return second_attacker
            elif second_attacker.health <= 0:
                first_attacker.level_up()
                if first_attacker is pokemon1:
                    self.trainer_1.update_pokedex_completion(first_attacker)
                else:
                    self.trainer_2.update_pokedex_completion(first_attacker)

                return first_attacker

        return None

    # Time complexity: O(1), do not depend on the size of the data
    def calculate_damage(self, attacker: Pokemon, defender: Pokemon, multiplier: float) -> int:
        base_damage = max(attacker.attack - defender.defence, 0)
        return ceil(base_damage * multiplier)

if __name__ == '__main__':
    t1 = Trainer('Ash')
    t2 = Trainer('Gary')
    b = Battle(t1, t2, BattleMode.SET)
    b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")