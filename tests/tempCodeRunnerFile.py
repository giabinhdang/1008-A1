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