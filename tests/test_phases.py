from utils import *
import pytest


def test_phase_knife_juggler_flamestrike():
	game = prepare_game()
	egg = game.player1.give("BRM_022")
	egg.play()
	juggler = game.player1.give("NEW1_019")
	juggler.play()
	game.end_turn()
	
	flamestrike = game.player2.give("CS2_032")
	assert game.player2.hero.health == 30
	flamestrike.play()
	assert game.player2.hero.health == 29


def test_phase_explosive_sheep_acolyte():
	game = prepare_game()
	game.player1.discard_hand()
	acolyte = game.player1.give("EX1_007")
	acolyte.play()
	for i in range(3):
		game.player2.summon("GVG_076")
	flamestrike = game.player1.give("CS2_032")
	
	assert len(game.player1.hand) == 1
	flamestrike.play()
	assert len(game.player1.hand) == 3


def test_phase_hero_powers():
	game = prepare_game(MAGE, MAGE)
	wisp = game.player2.summon(WISP)
	game.player1.hero.power.use(target=wisp)
	assert wisp.dead
	

def test_phase_endgame_hero_powers():
	with pytest.raises(fireplace.game.GameOver):
		game = prepare_game(MAGE, MAGE)
		game.player2.hero.set_current_health(1)
		game.player1.hero.power.use(target=game.player2.hero)