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
from data_structures.abstract_list import *

class PokeTeam:
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]

    def __init__(self):
        self.team = ArrayStack(self.TEAM_LIMIT) # change None value if necessary
        self.team_count = 0

    def add_pokemon(self, pokemon):
        # Add a Pokémon to the team structure
        if isinstance(self.team, ArrayStack):
            self.team.push(pokemon)
        elif isinstance(self.team, CircularQueue):
            self.team.append(pokemon)
        elif isinstance(self.team, ArraySortedList):
            self.team.insert(pokemon)

    def remove_pokemon(self):
        # Remove and return a Pokémon from the team structure
        if isinstance(self.team, ArrayStack):
            return self.team.pop()
        elif isinstance(self.team, CircularQueue):
            return self.team.serve()
        elif isinstance(self.team, ArraySortedList):
            return self.team.pop(0)  # Remove the first Pokémon in the sorted list

    def clear_team(self):
        # Clear the current team structure, preparing for reassembly
        if isinstance(self.team, ArrayStack):
            while not self.team.is_empty():
                self.team.pop()
        elif isinstance(self.team, CircularQueue):
            while not self.team.is_empty():
                self.team.serve()
        elif isinstance(self.team, ArraySortedList):
            while not self.team.is_empty():
                self.team.pop(0)  # Remove the first Pokémon in the sorted list

    def choose_manually(self):
        self.team = ArrayStack(self.TEAM_LIMIT)  # Initialize self.team as an ArrayR object
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
        self.team = ArrayStack(self.TEAM_LIMIT)  # Initialize self.team as an ArrayStack object
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for _ in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            pokemon = all_pokemon[rand_int]()
            print(f"Selected Pokemon: {pokemon}")  # print the selected Pokemon
            if pokemon is not None:
                self.team.push(pokemon)  # Use push method to add the selected Pokemon to the stack
                self.team_count += 1


    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None):
        # Use a temporary ArrayStack for regeneration regardless of the current battle mode
        temp_stack = ArrayStack(self.TEAM_LIMIT)
        
        # Move Pokémon to the temp_stack and reset their health
        while not self.is_empty():
            pokemon = self.remove_pokemon()  # This abstract method adapts to the current structure
            pokemon.health = type(pokemon)().health  # Reset health
            temp_stack.push(pokemon)
        
        # Clear current team structure in preparation for reassembly
        self.clear_team()
        
        # Move Pokémon back from temp_stack to the team, now using the appropriate structure for the battle mode
        while not temp_stack.is_empty():
            self.add_pokemon(temp_stack.pop())
        
        # Optionally re-sort or re-organize the team based on the battle mode
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
        if battle_mode == BattleMode.SET:
            temp_stack = ArrayStack(self.TEAM_LIMIT)
            while not self.team.is_empty():  # If self.team is ArrayStack, it should have is_empty method
                pokemon = self.team.pop()  # This should be valid since self.team should be ArrayStack
                if pokemon is not None:
                    temp_stack.push(pokemon)

            self.team = ArrayStack(self.TEAM_LIMIT)
            while not temp_stack.is_empty():
                self.team.push(temp_stack.pop())

        elif battle_mode == BattleMode.ROTATE:
            temp_queue = CircularQueue(self.TEAM_LIMIT)
            # Pop all Pokemon into a temporary queue
            while not self.team.is_empty():
                pokemon = self.team.pop()
                if pokemon is not None:
                    temp_queue.append(pokemon)

            # Now queue back into self.team as a CircularQueue
            self.team = CircularQueue(self.TEAM_LIMIT)
            while not temp_queue.is_empty():
                self.team.append(temp_queue.serve())

        elif battle_mode == BattleMode.OPTIMISE:
            # You'll need to pop all elements from the stack to sort them
            # The ArraySortedList is expected to have a method to insert items in a sorted way
            temp_list = ArraySortedList(self.TEAM_LIMIT)
            while not self.team.is_empty():
                pokemon = self.team.pop()
                if pokemon is not None:
                    # The ListItem constructor may require the item and a key for sorting
                    temp_list.add(ListItem(pokemon, getattr(pokemon, self.criterion)))

            # Now move the sorted Pokemon back into self.team
            self.team = ArraySortedList(self.TEAM_LIMIT)
            for i in range(temp_list.length):
                self.team.add(temp_list[i])

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
        return f"PokeTeam with {self.team_count} Pokemon"
    
    def is_empty(self) -> bool:
        return len(self.team) == 0
    
    def push(self, pokemon):
        self.team.push(pokemon)

    def pop(self):
        if len(self.team) > 0:
            return self.team.pop()
        else:
            return None

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

    def update_pokedex_completion(self, new_pokemon: Pokemon) -> None:
        self.register_pokemon(new_pokemon)


    def __str__(self) -> str:
        return f"Trainer {self.name} Pokedex Completion: {int(self.get_pokedex_completion() * 100)}%"
    

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())


