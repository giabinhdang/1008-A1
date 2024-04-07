def choose_randomly(self) -> None:
        self.team = ArrayR(self.TEAM_LIMIT)
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(self.TEAM_LIMIT):
            while True:
                rand_int = random.randint(0, len(all_pokemon)-1)
                pokemon = all_pokemon[rand_int]()
                if pokemon is not None:
                    self.team[i] = pokemon
                    self.team_count += 1
                    break  # break the loop if a valid Pokemon is found