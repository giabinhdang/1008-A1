def test_get_pokedex_completion(self):
        trainer = Trainer('Ash')
        trainer.register_pokemon(Pikachu())
        trainer.register_pokemon(Pidgey())
        trainer.register_pokemon(Aerodactyl())

        self.assertEqual(trainer.get_pokedex_completion(), 0.2)