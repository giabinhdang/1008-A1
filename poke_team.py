from pokemon import *
import random
from typing import List
from battle_mode import BattleMode
from data_structures.referential_array import ArrayR

class PokeTeam:
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]

    def __init__(self):
        self.team = ArrayR(self.TEAM_LIMIT) # change None value if necessary
        self.team_count = 0

    def choose_manually(self):
        self.team = []
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
            self.team[i] = (chosen_pokemon)

    def choose_randomly(self) -> None:
        # Get all available Pokemon types
        all_pokemon = get_all_pokemon_types()
        for i in range(self.TEAM_LIMIT):
            # Generate a random index to choose a Pokemon type
            rand_int = random.randint(0, len(all_pokemon) - 1)
            # Create an instance of a randomly chosen Pokemon
            chosen_pokemon = all_pokemon[rand_int]()
            # Add the chosen Pokemon to the team list
            self.team[i] = chosen_pokemon

    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        for pokemon in self.team:
            if hasattr(pokemon, 'regenerate'):
                pokemon.regenerate()
                if pokemon.get_health() < 0:  
                    pokemon.set_health(0)  

        self.assemble_team(battle_mode)

    def assign_team(self, criterion: str = None) -> None:
        pass

    def assemble_team(self, battle_mode: BattleMode) -> None:
        pass

    def special(self, battle_mode: BattleMode) -> None:
        pass

    def __getitem__(self, index: int):
        return self.team[index]

    def __len__(self):
        return len(self.team)

    def __str__(self):
        return "\n".join([str(pokemon) for pokemon in self.team])

class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedex = set()

    def pick_team(self, method: str) -> None:
        if method == "Random":
            self.team.choose_randomly()
        elif method == "Manual":
            self.team.choose_manually()
        else:
            raise ValueError("Choose either 'Random' or 'Manual'!")

    def get_team(self) -> PokeTeam:
        return self.team

    def get_name(self) -> str:
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        self.pokedex.add(pokemon.get_poketype())

    def get_pokedex_completion(self) -> float:
        total_types = len(PokeType)
        seen_types = len(self.pokedex)
        completion = seen_types / total_types
        return round(completion, 2)

    def __str__(self) -> str:
        return f"Trainer {self.name} Pokedex Completion: {int(self.get_pokedex_completion() * 100)}%"

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())
