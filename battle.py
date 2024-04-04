from __future__ import annotations
from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from pokemon_base import Pokemon
from data_structures.stack_adt import Stack
from data_structures.queue_adt import *
from data_structures.array_sorted_list import *

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
            return self.optimize_battle()
        else:
            raise ValueError("Invalid battle mode.")

    def set_battle(self) -> Trainer | None:
        team_1 = self.trainer_1.get_team()
        team_2 = self.trainer_2.get_team()

        while team_1 and team_2:
            pokemon1 = team_1.team.pop()
            pokemon2 = team_2.team.pop()
            winner = self.battle_round(pokemon1, pokemon2)
            if winner == pokemon1:
                team_2.append(pokemon2)  
            else:
                team_1.append(pokemon1)  

        if not team_1:
            return self.trainer_2
        else:
            return self.trainer_1

    def rotate_battle(self) -> Trainer | None:
        team_1 = self.trainer_1.get_team()
        team_2 = self.trainer_2.get_team()

        while len(team_1) > 0 and len(team_2) > 0:
            pokemon1 = team_1.team.serve()
            pokemon2 = team_2.team.serve()
            if pokemon1 is None:
                return self.trainer_2
            elif pokemon2 is None:
                return self.trainer_1
            else:
                winner = self.battle_round(pokemon1, pokemon2)
                if winner == pokemon1:
                    team_1.append(pokemon1)
                else:
                    team_1.append(pokemon1)
        if len(team_1) == 0:
            return self.trainer_2
        else:
            return self.trainer_1

    def optimize_battle(self) -> Trainer | None:
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
        

    def battle_round(self, pokemon1: Pokemon, pokemon2: Pokemon) -> Pokemon:
        if pokemon1.health > pokemon2.health:
            return pokemon1
        elif pokemon1.health < pokemon2.health:
            return pokemon2
        else:
            return None
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
    b = Battle(t1, t2, BattleMode.ROTATE)
    b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
