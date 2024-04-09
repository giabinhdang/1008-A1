from poke_team import Trainer, PokeTeam
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple, List
import random

class BattleResult(Enum):
    WIN = 1
    LOSS = 2
    DRAW = 3

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3

    def __init__(self) -> None:
        self.my_trainer = None
        self.enemy_trainers = CircularQueue(10)  # Assuming a max of 10 enemy trainers for this example
        self.enemy_lives = ArrayStack(10)
        self.my_lives = 0
        self.enemies_defeated_count = 0

    def set_my_trainer(self, trainer: Trainer) -> None:
        self.my_trainer = trainer
        self.my_lives = random.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES)

    def generate_enemy_trainers(self, num_teams: int) -> None:
        for _ in range(num_teams):
            enemy_trainer = Trainer(f"Enemy_{_ + 1}")
            enemy_trainer.pick_team("Random")
            self.enemy_trainers.append(enemy_trainer)
            self.enemy_lives.push(random.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES))

    def battles_remaining(self) -> bool:
        return not self.my_lives == 0 and not self.enemy_lives.is_empty()

    def next_battle(self) -> Tuple[BattleResult, Trainer, Trainer, int, int]:
        if self.enemy_trainers.is_empty():
            # Reload the queue if all enemies were defeated but still have lives
            for i in range(len(self.enemy_lives)):
                if self.enemy_lives.array[i] > 0:
                    self.enemy_trainers.append(self.enemy_trainers.array[i])
        
        enemy_trainer = self.enemy_trainers.serve()
        enemy_lives = self.enemy_lives.pop()
        # Simulate battle here...
        # For simplicity, let's say the player always wins.
        battle_result = BattleResult.WIN
        enemy_lives -= 1
        if battle_result == BattleResult.WIN:
            self.enemies_defeated_count += 1
        elif battle_result == BattleResult.LOSS:
            self.my_lives -= 1
        else:  # DRAW
            self.my_lives -= 1
            enemy_lives -= 1
        
        # Put the enemy trainer back with updated lives if they still have lives left
        if enemy_lives > 0:
            self.enemy_lives.push(enemy_lives)
            self.enemy_trainers.append(enemy_trainer)

        return battle_result, self.my_trainer, enemy_trainer, self.my_lives, enemy_lives

    def enemies_defeated(self) -> int:
        return self.enemies_defeated_count