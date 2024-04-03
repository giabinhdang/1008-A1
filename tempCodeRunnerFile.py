
    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        for pokemon in self.team:
            if hasattr(pokemon, 'regenerate'):
                pokemon.regenerate()

        self.assemble_team(battle_mode)