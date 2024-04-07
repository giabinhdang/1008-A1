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
        # Loop until one team is empty
        while not self.trainer_1.get_team().is_empty() and not self.trainer_2.get_team().is_empty():
            pokemon1 = self.trainer_1.get_team().pop()
            pokemon2 = self.trainer_2.get_team().pop()
            winner = self.battle_round(pokemon1, pokemon2)

            # Check if pokemon1 won and is not fainted
            if winner == pokemon1 and pokemon1.get_health() > 0:
                self.trainer_1.get_team().push(pokemon1)
            # Check if pokemon2 won and is not fainted
            elif winner == pokemon2 and pokemon2.get_health() > 0:
                self.trainer_2.get_team().push(pokemon2)
            # No need to reinsert fainted Pokémon

        # Determine the winner based on which team is not empty
        if not self.trainer_1.get_team().is_empty():
            return self.trainer_1
        elif not self.trainer_2.get_team().is_empty():
            return self.trainer_2
        else:
            return None  # Draw scenario


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
        # Pokedex multiplier for attack damage
        p1_multiplier = self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion()
        p2_multiplier = self.trainer_2.get_pokedex_completion() / self.trainer_1.get_pokedex_completion()

        # Determine the attacker and defender based on speed
        if pokemon1.speed > pokemon2.speed:
            self.perform_attack(pokemon1, pokemon2, p1_multiplier)
            if pokemon2.health > 0:
                self.perform_attack(pokemon2, pokemon1, p2_multiplier)
        elif pokemon2.speed > pokemon1.speed:
            self.perform_attack(pokemon2, pokemon1, p2_multiplier)
            if pokemon1.health > 0:
                self.perform_attack(pokemon1, pokemon2, p1_multiplier)
        else:
            # Both attack simultaneously
            self.perform_attack(pokemon1, pokemon2, p1_multiplier)
            self.perform_attack(pokemon2, pokemon1, p2_multiplier)

        # Handle the outcomes
        if pokemon1.health <= 0 and pokemon2.health <= 0:
            # Both faint
            self.team.remove(pokemon1)
            self.team.remove(pokemon2)
            return None  
        elif pokemon1.health > 0 and pokemon2.health <= 0:
            # Pokemon2 faints
            pokemon1.level_up()
            if self.style == 'Set':
                self.team.remove(pokemon1)
                self.team.push(pokemon1)
            self.team.remove(pokemon2)
            return pokemon1
        elif pokemon2.health > 0 and pokemon1.health <= 0:
            # Pokemon1 faints
            pokemon2.level_up()
            if self.style == 'Set':
                self.team.remove(pokemon2)
                self.team.push(pokemon2)
            self.team.remove(pokemon1)
            return pokemon2
        else:
            # Both survive; both lose 1 HP then check for fainting
            pokemon1.health -= 1
            pokemon2.health -= 1
            if pokemon1.health <= 0 and pokemon2.health > 0:
                # Pokemon1 faints
                pokemon2.level_up()
                if self.style == 'Set':
                    self.team.remove(pokemon2)
                    self.team.push(pokemon2)
                self.team.remove(pokemon1)
                return pokemon2
            elif pokemon2.health <= 0 and pokemon1.health > 0:
                # Pokemon2 faints
                pokemon1.level_up()
                if self.style == 'Set':
                    self.team.remove(pokemon1)
                    self.team.push(pokemon1)
                self.team.remove(pokemon2)
                return pokemon1
            return None


    def perform_attack(self, attacker: Pokemon, defender: Pokemon, multiplier: float):
        base_damage = ceil(attacker.attack - defender.defense)
        attack_damage = ceil(base_damage * multiplier)
        defender.health -= max(attack_damage, 0)

        
    # Note: These are here for your convenience
    # If you prefer you can ignore them
   # def set_battle(self) -> PokeTeam | None:
    #    self._create_teams()

   # def rotate_battle(self) -> PokeTeam | None:
     #   self._create_teams()

  #  def optimise_battle(self) -> PokeTeam | None:
    #    self._create_teams()

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