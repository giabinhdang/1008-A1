from pokemon import *
import random
from typing import List
from battle_mode import BattleMode
from data_structures.referential_array import *
from data_structures.stack_adt import *
from data_structures.queue_adt import *
from data_structures.sorted_list_adt import *
from data_structures.array_sorted_list import *
from data_structures.bset import *

class PokeTeam:
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]

    def __init__(self):
        self.team = ArrayR(self.TEAM_LIMIT) # change None value if necessary
        self.team_count = 0

    def choose_manually(self):
        self.team = ArrayR(self.TEAM_LIMIT)  # Initialize self.team as an ArrayR object
        print("Choose your Pokemon:")
        for i in range(self.TEAM_LIMIT):
            print(f"Select Pokemon {i+1}:")
            print("Available Pokemon:")
            for j, PokeType in enumerate(get_all_pokemon_types()):
                print(f"{j+1}. {PokeType.__name__}")
            choice = int(input("How many Pokemon you want to choose?"))
            while choice < 1 or choice > len(get_all_pokemon_types()):
                print ("Please choose again!")
                choice = int(input("How many Pokemon you want to choose?"))
            chosen_pokemon = get_all_pokemon_types()[choice - 1]()
            self.team.insert(i, chosen_pokemon)  # Use the insert method to add the chosen Pokemon to the team

    def choose_randomly(self) -> None:
        self.team = ArrayR(self.TEAM_LIMIT)
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            self.team[i] = all_pokemon[rand_int]()
            self.team_count += 1

    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        print("Before regeneration:", [p.get_health() if p is not None else None for p in self.team.array])
        if isinstance(self.team, ArrayR):
            for i in range(len(self.team)):
                if self.team[i] is not None:  # Ensure it's not None before calling regenerate
                    self.team[i].regenerate()
        elif isinstance(self.team, ArrayStack):
            # Use a temporary list to hold Pokémon while regenerating
            temp_list = []
            while not self.team.is_empty():
                pokemon = self.team.pop()
                pokemon.regenerate()  # Assuming all elements are Pokémon objects
                temp_list.append(pokemon)
            # Push them back to the stack
            while temp_list:
                self.team.push(temp_list.pop(-1))  # Push back in reverse order to maintain original order
        print("After regeneration:", [p.get_health() if p is not None else None for p in self.team.array])
        self.assemble_team(battle_mode)


    def assign_team(self, criterion: str = None) -> None:
        if self.team:
            non_pokemon = ArrayR(len(self.team))
            index = 0
            for pokemon in self.team:
                if pokemon is not None:
                    non_pokemon[index] = pokemon
                    index += 1
            if pokemon is not None:
                sorted_pokemon = sorted(non_pokemon, key=lambda pokemon: getattr(pokemon, criterion))
            else:
                None
            self.team = ArrayR(len(sorted_pokemon))
            for i, pokemon in enumerate(sorted_pokemon):
                self.team[i] = pokemon

    def assemble_team(self, battle_mode: BattleMode) -> None:
        original_team = self.team
        if battle_mode == BattleMode.SET:
            self.team = ArrayStack(self.TEAM_LIMIT)
            for pokemon in reversed(original_team.array):
                if pokemon is not None:
                    self.team.push(pokemon)
        elif battle_mode == BattleMode.ROTATE:
            self.team = CircularQueue(self.TEAM_LIMIT)
            for pokemon in original_team.array:
                if pokemon is not None:
                    self.team.append(pokemon)
        elif battle_mode == BattleMode.OPTIMISE:
            self.team = ArraySortedList(self.TEAM_LIMIT)
            self.assign_team("level")
        else:
            raise ValueError("Invalid battle mode.")
        
    def special(self, battle_mode: BattleMode) -> None:
        if battle_mode == BattleMode.SET:
            temp_stack = ArrayStack(self.TEAM_LIMIT)
            while not self.team.is_empty():
                temp_stack.push(self.team.pop())
            self.team = temp_stack

        elif battle_mode == BattleMode.ROTATE:
            half_size = len(self.team) // 2
            for i in range(half_size):
                bottom_index = len(self.team) - i - 1
                temp = self.team[bottom_index]
                self.team[bottom_index] = self.team[half_size + i]
                self.team[half_size + i] = temp

        elif battle_mode == BattleMode.OPTIMISE:
            temp_list = ArraySortedList(self.TEAM_LIMIT)
            for pokemon in self.team.array:
                if pokemon is not None:
                    temp_list.add(pokemon)
            if len(temp_list.array) % 2 == 1:
                reversed_list = ArraySortedList(self.TEAM_LIMIT)
                for i in range (len(temp_list) - 1, -1, -1):
                    reversed_list.add(temp_list[i])
                self.team = reversed_list
            else:
                self.team = temp_list

        else:
            raise ValueError("Invalid battle mode.")
        
        self.assemble_team(battle_mode)
       # self.update_pokedex_completion()

    def __getitem__(self, index: int):
        return self.team.array[index]

    def __len__(self):
        return len(self.team)

    def __str__(self):
        return "\n".join([str(pokemon) for pokemon in self.team])
    
    def is_empty(self) -> bool:
        return len(self.team) == 0

class Trainer:
    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedex = BSet()

    def pick_team(self, method: str) -> None:
        if method == "Random":
            self.team.choose_randomly()
        elif method == "Manual":
            self.team.choose_manually()
        else:
            raise ValueError("Choose either 'Random' or 'Manual'!")

    def get_team(self) -> PokeTeam:
        if self.team is None:
            self.team = PokeTeam()
        return self.team

    def get_name(self) -> str:
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        self.pokedex.add(pokemon.get_poketype().value)

    def get_pokedex_completion(self) -> float:
        total_types = len(PokeType)
        seen_types = len(self.pokedex)
        if total_types > 0: 
            completion = seen_types / total_types
        else: 
            completion = 0
        return round(completion, 2)

    def update_pokedex_completion(self) -> None:
        for pokemon in self.get_team():
            self.register_pokemon(pokemon)

    def __str__(self) -> str:
        return f"Trainer {self.name} Pokedex Completion: {int(self.get_pokedex_completion() * 100)}%"
    

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())


