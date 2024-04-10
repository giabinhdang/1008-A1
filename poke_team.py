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

    # Time complexity: O(1), sets up simple attributes and intializes the team structure
    def __init__(self):
        self.team = ArrayStack(self.TEAM_LIMIT) # change None value if necessary
        self.team_count = 0

    # Time complexity: O(1), adds a pokemon to the team structure use a single operations; constant time for stacks and queues
    def add_pokemon(self, pokemon):
        # Add a Pokémon to the team structure
        if isinstance(self.team, ArrayStack):
            self.team.push(pokemon)
        elif isinstance(self.team, CircularQueue):
            self.team.append(pokemon)
        elif isinstance(self.team, ArraySortedList):
            self.team.add(pokemon)

    # Time complexity: O(1), removes a pokemon from the team structure using a single operation; constant time for stacks and queues
    def remove_pokemon(self):
        # Remove and return a Pokémon from the team structure
        if isinstance(self.team, ArrayStack):
            return self.team.pop()
        elif isinstance(self.team, CircularQueue):
            return self.team.serve()
        elif isinstance(self.team, ArraySortedList):
            return self.team.delete_at_index(0)  # Remove the first Pokémon in the sorted list

    # Time complexity: O(n), clears the team structure by removing all elements; linear time for stacks and queues
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
                self.team.delete_at_index(0)  # Remove the first Pokémon in the sorted list

    # Time complexity: O(1), operations within funciton
    # Worst case time complexity: O(n), where n is TEAM_LIMIT
    def choose_manually(self):
        self.team = ArrayStack(self.TEAM_LIMIT)  
        print("Choose your Pokemon:")
        # Get all available Pokemon types
        available_pokemon = get_all_pokemon_types()  
        for i in range(self.TEAM_LIMIT):
            print(f"\nSelect Pokemon {i + 1}:")
            # Display available Pokemon
            for index, PokeType in enumerate(available_pokemon, start=1):
                print(f"{index}. {PokeType.__name__}")
            while True:
                try:
                    choice = int(input(f"Enter your choice (1-{len(available_pokemon)}): "))
                    if 1 <= choice <= len(available_pokemon):
                        # Create an instance of the chosen Pokemon
                        chosen_pokemon = available_pokemon[choice - 1]()  
                        self.team.push(chosen_pokemon) 
                        break  
                    else:
                        print(f"Please enter a number between 1 and {len(available_pokemon)}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        print("Team selection complete.")


    # Time complexity: O(1), operations within funciton
    def choose_randomly(self) -> None:
        # Worst case time complexity: O(n), where n is TEAM_LIMIT
        self.team = ArrayStack(self.TEAM_LIMIT)  
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for _ in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            pokemon = all_pokemon[rand_int]()
            print(f"Selected Pokemon: {pokemon}")  
            if pokemon is not None:
                self.team.push(pokemon)  
                self.team_count += 1

    # Time complexity: O(n), iterating over all Pokemon to reset their health
    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None):
        # Use a temporary ArrayStack for regeneration regardless of the current battle mode
        temp_stack = ArrayStack(self.TEAM_LIMIT)
        
        # Move Pokémon to the temp_stack and reset their health
        while not self.is_empty():
            pokemon = self.remove_pokemon()  
            pokemon.health = type(pokemon)().health  
            temp_stack.push(pokemon)
        
        self.clear_team()
        
        # Move Pokémon back from temp_stack to the team
        while not temp_stack.is_empty():
            self.add_pokemon(temp_stack.pop())
        self.assemble_team(battle_mode)

    # Time complexity: O(n log n), sorting the team based on the criterion
    def assign_team(self, criterion: str = None) -> None:
        if criterion is None or self.is_empty():
            return
        # Use the ListItem for sorting the team
        new_team = ListItem()
        # Iterate through the current team
        while not self.is_empty():
            pokemon = self.remove_pokemon()  
            if pokemon:
                key = getattr(pokemon, criterion)
                item = ListItem(value=pokemon, key=key)
                new_team.add(item)
        # Clear the current team structure
        self.clear_team()
        # Re-add the pokemon to the team from the sorted list
        for i in range(len(new_team)):
            self.add_pokemon(new_team[i])


    def assemble_team(self, battle_mode: BattleMode) -> None:
        # Time complexity: O(n), transfering all Pokemon to a temp structure and back
        if battle_mode == BattleMode.SET:
            temp_stack = ArrayStack(self.TEAM_LIMIT)
            while not self.team.is_empty():  # If self.team is ArrayStack, it should have is_empty method
                pokemon = self.team.pop()  # This should be valid since self.team should be ArrayStack
                if pokemon is not None:
                    temp_stack.push(pokemon)
            self.team = ArrayStack(self.TEAM_LIMIT)
            while not temp_stack.is_empty():
                self.team.push(temp_stack.pop())
        # Time complexity: O(n), transfering all Pokemon to a temp structure and back
        elif battle_mode == BattleMode.ROTATE:
            temp_queue = CircularQueue(self.TEAM_LIMIT)
            # Pop all Pokemon into a temporary queue
            while not self.team.is_empty():
                pokemon = self.team.serve()
                if pokemon is not None:
                    temp_queue.append(pokemon)
            # Now queue back into self.team as a CircularQueue
            self.team = CircularQueue(self.TEAM_LIMIT)
            while not temp_queue.is_empty():
                self.team.append(temp_queue.serve())
        # Time complexity O(n log n)
        # Worst time complexity: O(n^2) 
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
        # Time complexity: O(n), iterating over all Pokemon to apply the special effect
        if battle_mode == BattleMode.SET:
            temp_stack = ArrayStack(self.TEAM_LIMIT)
            while not self.team.is_empty():
                temp_stack.push(self.team.pop())
            self.team = temp_stack

        # Time complexity: O(n), a number of operations to reverse the team based on half of the team size
        elif battle_mode == BattleMode.ROTATE:
            half_size = len(self.team) // 2
            for i in range(half_size):
                bottom_index = len(self.team) - i - 1
                temp = self.team[bottom_index]
                self.team[bottom_index] = self.team[half_size + i]
                self.team[half_size + i] = temp

        # Time complexity: O(n log n), due to sorting operation
        # Worst case time complexity: O(n^2), when the list is already sorted
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

    # Time complexity: O(1), simple operations
    def __getitem__(self, index: int):
        return self.team.array[index]

    # Time complexity: O(1), simple operations
    def __len__(self):
        return len(self.team)

    # Time complexity: O(1), simple operations
    # Worst case time complexity: O(n), if it has to iterate over all Pokemon
    def __str__(self):
        return f"PokeTeam with {self.team_count} Pokemon"
    
    # Time complexity: O(1), simple operations
    def is_empty(self) -> bool:
        return len(self.team) == 0
    
    # Time complexity: O(1), simple operations
    def push(self, pokemon):
        self.team.push(pokemon)

    # Time complexity: O(1), simple operations
    def pop(self):
        if len(self.team) > 0:
            return self.team.pop()
        else:
            return None

class Trainer:

    # Time complexity: O(1), sets up attributes and inializes data structures
    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedex = BSet()

    # Time complexity: O(n), directly calls "PokeTeam" which have O(n) time complexity
    def pick_team(self, method: str) -> None:
        if method == "Random":
            self.team.choose_randomly()
        elif method == "Manual":
            self.team.choose_manually()
        else:
            raise ValueError("Choose either 'Random' or 'Manual'!")

    # Time complexity: O(1), direct access or simple calculations
    def get_team(self) -> PokeTeam:
        if self.team is None:
            self.team = PokeTeam()
        return self.team

    # Time complexity: O(1), direct access or simple calculations
    def get_name(self) -> str:
        return self.name

    # Time complexity: O(1), direct access or simple calculations
    def register_pokemon(self, pokemon: Pokemon) -> None:
        self.pokedex.add(pokemon.get_poketype().value)

    # Time complexity: O(1), direct access or simple calculations
    def get_pokedex_completion(self) -> float:
        total_types = len(PokeType)
        seen_types = len(self.pokedex)
        if total_types > 0: 
            completion = seen_types / total_types
        else: 
            completion = 0
        return round(completion, 2)

    # Time complexity: O(1), direct access or simple calculations
    def update_pokedex_completion(self, new_pokemon: Pokemon) -> None:
        self.register_pokemon(new_pokemon)

    # Time complexity: O(1), direct access or simple calculations
    def __str__(self) -> str:
        return f"Trainer {self.name} Pokedex Completion: {int(self.get_pokedex_completion() * 100)}%"
    

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())


