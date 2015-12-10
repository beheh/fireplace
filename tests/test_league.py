from utils import *


def test_eerie_statue():
	game = prepare_game()
	statue = game.player1.give("LOE_107")
	statue.play()
	game.end_turn(); game.end_turn()

	assert not statue.cant_attack
	wisp = game.player1.summon(WISP)
	assert statue.cant_attack
	wisp.destroy()
	assert not statue.cant_attack


def test_curse_of_rafaam():
	game = prepare_game()
	game.player2.discard_hand()
	assert len(game.player2.hand) == 0
	curse = game.player1.give("LOE_007")
	curse.play()
	assert len(game.player2.hand) == 1
	cursed = game.player2.hand[0]
	assert cursed.id == "LOE_007t"
	assert cursed.immune_to_spellpower
	assert game.player2.hero.health == 30
	game.end_turn()

	assert game.player2.hero.health == 30 - 2
	game.player2.give(KOBOLD_GEOMANCER).play()
	game.end_turn()
	assert game.player2.hero.health == 30 - 2
	game.end_turn()

	assert game.player2.hero.health == 30 - 2 - 2
	cursed.play()
	game.end_turn(); game.end_turn()

	assert game.player2.hero.health == 30 - 2 - 2
