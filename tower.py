from poke_team import Trainer, PokeTeam
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple, List
from battle_mode import BattleMode
from battle import Battle
import random

class BattleResult(Enum):
    WIN = 1
    LOSS = 2
    DRAW = 3

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3

    # Time complexity: O(1), sets up attributes and initializes data structures
    def __init__(self) -> None:
        self.my_trainer = None
        self.enemy_trainers = CircularQueue(10)  
        self.enemy_lives = ArrayStack(10)
        self.my_lives = 0
        self.enemies_defeated_count = 0

    # Time complexity: O(1), sets the player's trainer and initializes the player's lives
    def set_my_trainer(self, trainer: Trainer) -> None:
        self.my_trainer = trainer
        self.my_lives = random.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES)

    # Time complexity: O(n), where n is the number of teams to generate
    def generate_enemy_trainers(self, num_teams: int) -> None:
        for _ in range(num_teams):
            enemy_trainer = Trainer(f"Enemy_{_ + 1}")
            enemy_trainer.pick_team("Random")
            self.enemy_trainers.append(enemy_trainer)
            self.enemy_lives.push(random.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES))

    # Time complexity: O(1), checks if there are battles remaining
    def battles_remaining(self) -> bool:
        return not self.my_lives == 0 and not self.enemy_lives.is_empty()

    # Time complexity: O(n)
    def simulate_battle(self, player: Trainer, enemy: Trainer) -> Tuple[BattleResult, int, int]:
        # Initialize the battle with ROTATE mode
        battle = Battle(player, enemy, BattleMode.ROTATE, criterion=None)

        # Commence the battle and capture the winner
        winner = battle.commence_battle()

        # Determine the outcome based on the winner
        if winner == player:
            battle_result = BattleResult.WIN
            player_lives_lost = 0
            enemy_lives_lost = 1
        elif winner == enemy:
            battle_result = BattleResult.LOSS
            player_lives_lost = 1
            enemy_lives_lost = 0
        else:
            # This handles the draw scenario
            battle_result = BattleResult.DRAW
            player_lives_lost = 1
            enemy_lives_lost = 1

        # Return the outcome, along with lives lost for both player and enemy
        return battle_result, player_lives_lost, enemy_lives_lost

    # Time complexity: O(1), returns the next battle result
    # Worst case time complexity: O(m + 2n), where m is the number of enemy trainers and n is the size of the team
    def next_battle(self) -> Tuple[BattleResult, Trainer, Trainer, int, int]:
        if self.enemy_trainers.is_empty():
            # Re-queue trainers that still have lives.
            for _ in range(self.enemy_lives.length()):
                lives = self.enemy_lives.pop()
                if lives > 0:
                    trainer = self.enemy_trainers.serve()  # Assuming serve() also dequeues.
                    self.enemy_trainers.append(trainer)
                    self.enemy_lives.push(lives)

        if self.enemy_trainers.is_empty():
            # No more enemies to fight.
            return BattleResult.DRAW, self.my_trainer, None, self.my_lives, 0

        enemy_trainer = self.enemy_trainers.serve()
        enemy_lives = self.enemy_lives.pop()

        # Regenerate both teams before the battle.
        self.my_trainer.get_team().regenerate_team()
        enemy_trainer.get_team().regenerate_team()

        # Simulate the battle.
        battle_result, player_lives_lost, enemy_lives_lost = self.simulate_battle(self.my_trainer, enemy_trainer)

        # Update lives based on the outcome.
        self.my_lives -= player_lives_lost
        enemy_lives -= enemy_lives_lost

        # Log the battle result.
        print(f"Battle result: {battle_result}. Player lives: {self.my_lives}. Enemy lives: {enemy_lives}.")

        # If the enemy still has lives, put them back in the queue.
        if enemy_lives > 0:
            self.enemy_trainers.append(enemy_trainer)
            self.enemy_lives.push(enemy_lives)
        else:
            self.enemies_defeated_count += 1

        return battle_result, self.my_trainer, enemy_trainer, self.my_lives, enemy_lives

    # Time complexity: O(1), returns the number of enemies defeated
    def enemies_defeated(self) -> int:
        return self.enemies_defeated_count