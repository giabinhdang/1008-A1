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

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        if self.battle_mode == BattleMode.SET:
            return self.set_battle()
        elif self.battle_mode == BattleMode.ROTATE:
            return self.rotate_battle()
        elif self.battle_mode == BattleMode.OPTIMISE:
            return self.optimise_battle()
        else:
            raise ValueError("Invalid battle mode.")

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
            # If there's no winner (both faint), neither Pokémon is returned to their teams

        # Determine the winner based on remaining Pokémon
        if self.trainer_1.get_team().is_empty() and not self.trainer_2.get_team().is_empty():
            return self.trainer_2
        elif not self.trainer_1.get_team().is_empty() and self.trainer_2.get_team().is_empty():
            return self.trainer_1
        else:
            return None  # It's a draw if both teams are empty



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
                    team_1.push(pokemon1)
                elif winner == pokemon2 and pokemon2 is not None:
                    team_2.push(pokemon2)
        if len(team_1) == 0:
            return self.trainer_2
        else:
            return self.trainer_1

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
            pokemon1 = team_1.pop()
            pokemon2 = team_2.pop()

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
        if self.battle_mode == BattleMode.SET:
            self.trainer_1.get_team().assemble_team(BattleMode.SET)
            self.trainer_2.get_team().assemble_team(BattleMode.SET)
        elif self.battle_mode == BattleMode.ROTATE:
            self.trainer_1.get_team().assemble_team(BattleMode.ROTATE)
            self.trainer_2.get_team().assemble_team(BattleMode.ROTATE)
        elif self.battle_mode == BattleMode.OPTIMISE:
            self.trainer_1.get_team().assemble_team(BattleMode.OPTIMISE)
            self.trainer_2.get_team().assemble_team(BattleMode.OPTIMISE)
        else:
            raise ValueError("Invalid battle mode.")
        

    def battle_round(self, pokemon1: Pokemon, pokemon2: Pokemon) -> Pokemon | None:
        """
        Simulates a battle round between two Pokemon and returns the winner.
        If a Pokemon faints, the other one levels up.
        """
        # Get Pokedex completion rates for the multiplier effect
        p1_multiplier = self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion()
        p2_multiplier = self.trainer_2.get_pokedex_completion() / self.trainer_1.get_pokedex_completion()

        # Determine the attacking order based on speed
        first_attacker, second_attacker = (pokemon1, pokemon2) if pokemon1.speed > pokemon2.speed else (pokemon2, pokemon1)
        first_multiplier, second_multiplier = (p1_multiplier, p2_multiplier) if first_attacker is pokemon1 else (p2_multiplier, p1_multiplier)

        # First attack
        damage = self.calculate_damage(first_attacker, second_attacker, first_multiplier)
        second_attacker.health -= damage
        # Check if the second Pokemon faints after the first attack
        if second_attacker.health <= 0:
            first_attacker.level_up()
            # Assuming first_attacker belongs to trainer_1
            self.trainer_1.update_pokedex_completion(first_attacker)
            return first_attacker

        if first_attacker.health <= 0:
            second_attacker.level_up()
            # Assuming second_attacker belongs to trainer_2
            self.trainer_2.update_pokedex_completion(second_attacker)
            return second_attacker


        # If both Pokemon are still standing, return None indicating no winner in this round
        return None

    def calculate_damage(self, attacker: Pokemon, defender: Pokemon, multiplier: float) -> int:
        """
        Calculates the damage an attacker does to a defender, applying the Pokedex multiplier.
        """
        # Calculate base damage using attack and defense stats
        base_damage = max(attacker.attack - defender.defence, 0)
        # Apply the Pokedex completion multiplier
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