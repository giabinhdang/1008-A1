<<<<<<< HEAD
def test_set_battle_team_structure(self):
        _, _ = self.__test_set_battle()

        # Check Ash's team size is 2 and that Ash has these 2 Pokemon left
        self.assertEqual(len(self.trainer2.get_team()), 2, f"{self.trainer2.get_name()} should have 2 pokemon left in their team")
        self.assertEqual(str(self.trainer2.get_team()[0]), "Pinsir (Level 5) with 22.0 health and 0 experience")
        self.assertEqual(str(self.trainer2.get_team()[1]), "Bellsprout (Level 1) with 50 health and 0 experience")

        # Check loser (Gary's team)
        self.assertEqual(len(self.trainer1.get_team()), 0, f"{self.trainer1.get_name()} should have no Pokemon left in their team")
=======
def test_str(self):
        trainer = Trainer('Ash')
        trainer.register_pokemon(Pikachu())
        trainer.register_pokemon(Pidgey())
        trainer.register_pokemon(Aerodactyl())
        trainer.register_pokemon(Squirtle())
        trainer.register_pokemon(Weedle())
        trainer.register_pokemon(Meowth())
        trainer.register_pokemon(Zapdos())

        expected_str ="Trainer Ash Pokedex Completion: 40%"

        self.assertEqual(str(trainer), expected_str, "Trainer Str method is not set up correctly")
>>>>>>> parent of 6421ac7 (update)
