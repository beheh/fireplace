from utils import *


def test_anima_golem():
	game = prepare_game()
	anima = game.player1.give("GVG_077")
	anima.play()
	wisp1 = game.player1.summon(WISP)
	wisp2 = game.player2.summon(WISP)
	game.end_turn(); game.end_turn()

	assert not anima.dead
	wisp1.destroy()
	game.end_turn()

	assert anima.dead
	assert not wisp2.dead
	game.end_turn()


def test_ancestors_call():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	novice = game.player1.give("EX1_015")
	wisp = game.player2.give(WISP)
	call = game.player1.give("GVG_029")
	call.play()
	assert novice in game.player1.field
	assert wisp in game.player2.field
	assert not game.player1.hand
	assert not game.player2.hand


def test_blingtron_3000():
	game = prepare_game()
	blingtron = game.player1.give("GVG_119")
	blingtron.play()
	assert game.player1.weapon
	assert game.player2.weapon


def test_bolvar_fordragon():
	game = prepare_game()
	bolvar = game.player1.give("GVG_063")
	assert bolvar.atk == 1
	wisp = game.player1.give(WISP)
	wisp.play()
	game.player1.give(MOONFIRE).play(target=wisp)
	assert bolvar.atk == 2
	assert bolvar.buffs
	wisp = game.player1.give(WISP)
	wisp.play()
	game.player1.give(MOONFIRE).play(target=wisp)
	assert bolvar.atk == 3
	game.end_turn(); game.end_turn()

	assert bolvar.atk == 3
	assert bolvar.buffs
	bolvar.play()
	assert bolvar.atk == 3
	assert bolvar.buffs
	# game.player1.give(DREAM).play(target=bolvar)
	# assert bolvar.atk == 1
	# assert not bolvar.buffs


def test_bomb_lobber():
	game = prepare_game()
	lobber1 = game.player1.give("GVG_099")
	lobber2 = game.player1.give("GVG_099")
	game.end_turn()

	wisp = game.player2.give(WISP)
	warden = game.player2.give("EX1_396")
	game.end_turn()

	lobber1.play()
	assert game.player2.hero.health == 30
	game.end_turn()

	wisp.play()
	warden.play()
	game.end_turn()

	lobber2.play()
	assert wisp.dead ^ (warden.health == 7 - 4)


def test_bouncing_blade():
	game = prepare_game()
	acolyte = game.player1.give("EX1_007")
	acolyte.play()
	game.player1.discard_hand()
	blade = game.player1.give("GVG_050")
	blade.play()
	assert acolyte.dead
	assert len(game.player1.hand) == 3


def test_bouncing_blade_commanding_shout():
	game = prepare_game()
	acolyte = game.player1.give("EX1_007")
	acolyte.play()
	shout = game.player1.give("NEW1_036")
	shout.play()
	game.player1.discard_hand()
	assert acolyte.min_health == 1
	blade = game.player1.give("GVG_050")
	blade.play()
	assert acolyte.health == 1
	assert acolyte.zone == Zone.PLAY
	assert len(game.player1.hand) == 2


def test_crackle():
	game = prepare_game(SHAMAN, SHAMAN)
	crackle = game.player1.give("GVG_038")
	crackle.play(target=game.player2.hero)
	assert game.player2.hero.health in (24, 25, 26, 27)
	assert game.player1.overloaded == 1


def test_crackle_malygos():
	game = prepare_game(SHAMAN, SHAMAN)
	malygos = game.player1.give("EX1_563")
	malygos.play()
	game.end_turn(); game.end_turn()

	crackle = game.player1.give("GVG_038")
	crackle.play(target=game.player2.hero)
	assert game.player2.hero.health in (19, 20, 21, 22)
	assert game.player1.overloaded == 1


def test_crush():
	game = prepare_game()
	crush = game.player1.give("GVG_052")
	assert crush.cost == 7
	token = game.player1.give(SPELLBENDERT)
	token.play()
	assert crush.cost == 7
	game.player1.give(MOONFIRE).play(token)
	assert crush.cost == 3
	token.destroy()
	assert crush.cost == 7


def test_cobalt_guardian():
	game = prepare_game()
	cobalt = game.player1.give("GVG_062")
	cobalt.play()
	assert not cobalt.divine_shield
	game.player1.give(TARGET_DUMMY).play()
	assert cobalt.divine_shield
	game.player1.give(TARGET_DUMMY).play()
	assert cobalt.divine_shield


def test_cogmaster():
	game = prepare_game()
	cogmaster = game.player1.give("GVG_013")
	cogmaster.play()
	assert cogmaster.atk == 1
	dummy = game.player1.give(TARGET_DUMMY)
	dummy.play()
	assert cogmaster.atk == 3
	humility = game.player1.give("EX1_360")
	humility.play(target=cogmaster)
	assert cogmaster.atk == 3
	dummy.destroy()
	assert cogmaster.atk == 1
	game.player1.give(TARGET_DUMMY).play()
	assert cogmaster.atk == 3
	blessedchamp = game.player1.give("EX1_355")
	blessedchamp.play(target=cogmaster)
	assert cogmaster.atk == 4


def test_cogmasters_wrench():
	game = prepare_game()
	wrench = game.player1.summon("GVG_024")
	assert wrench.atk == game.player1.hero.atk == 1
	dummy = game.player1.give(TARGET_DUMMY)
	dummy.play()
	assert wrench.atk == game.player1.hero.atk == 3
	dummy.destroy()
	assert wrench.atk == game.player1.hero.atk == 1


def test_dr_boom():
	game = prepare_game()
	boom = game.player1.give("GVG_110")
	assert len(game.player1.field) == 0
	boom.play()
	assert len(game.player1.field) == 3
	assert len(game.player1.field.filter(id="GVG_110t")) == 2
	# Whirlwind the board
	game.player1.give("EX1_400").play()
	assert (30 - 2) >= game.player2.hero.health >= (30 - 8)


def test_druid_of_the_fang():
	game = prepare_game()
	fang = game.player1.give("GVG_080")
	assert not fang.powered_up
	fang.play()
	assert not fang.powered_up
	assert not fang.morphed
	assert fang in game.player1.field
	assert fang.id == "GVG_080"
	assert fang.atk == 4
	assert fang.health == 4
	game.end_turn(); game.end_turn()

	fang2 = game.player1.give("GVG_080")
	assert not fang2.powered_up
	game.player1.give(CHICKEN).play()
	assert fang2.powered_up
	fang2.play()
	druid2 = fang2.morphed
	assert druid2 in game.player1.field
	assert druid2.id == "GVG_080t"
	assert druid2.atk == 7
	assert druid2.health == 7
	assert druid2.race == Race.BEAST


def test_echo_of_medivh():
	game = prepare_game()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give(TARGET_DUMMY).play()
	game.player1.give(GOLDSHIRE_FOOTMAN).play()
	game.end_turn()
	game.player2.give(SPELLBENDERT).play()
	game.end_turn()
	game.player1.discard_hand()
	echo = game.player1.give("GVG_005")
	echo.play()
	assert game.player1.hand == [WISP, WISP, TARGET_DUMMY, GOLDSHIRE_FOOTMAN]
	assert len(game.player1.field) == 4


def test_fel_cannon():
	game = prepare_game()
	cannon = game.player1.give("GVG_020")
	cannon.play()
	game.end_turn(); game.end_turn()

	assert game.player1.hero.health == game.player2.hero.health == 30
	assert cannon.health == 5

	dummy1 = game.player1.give(TARGET_DUMMY)
	dummy1.play()
	game.end_turn()

	dummy2 = game.player2.give(TARGET_DUMMY)
	dummy2.play()
	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	assert not wisp.dead
	game.end_turn()

	assert dummy1.health == dummy2.health == 2
	assert not dummy1.dead
	assert not dummy2.dead
	assert wisp.dead


def test_fel_reaver():
	game = prepare_game()
	expected_size = len(game.player1.deck)
	felreaver = game.player1.give("GVG_016")
	felreaver.play()
	game.end_turn()

	for i in range(5):
		game.player2.give(WISP).play()
		expected_size -= 3
		assert len(game.player1.deck) == expected_size
		assert len(game.player2.deck) == 25


def test_floating_watcher():
	game = prepare_game(WARLOCK, WARLOCK)
	watcher = game.player1.give("GVG_100")
	watcher.play()
	assert watcher.atk == watcher.health == 4
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert watcher.atk == watcher.health == 4
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert watcher.atk == watcher.health == 4 + 2
	game.player1.hero.power.use()
	assert watcher.atk == watcher.health == 4 + 4


def test_floating_watcher_armor():
	game = prepare_game()
	watcher = game.player1.give("GVG_100")
	watcher.play()
	shieldblock = game.player1.give("EX1_606")
	shieldblock.play()
	assert watcher.atk == watcher.health == 4
	assert game.player1.hero.armor == 5
	assert not game.player1.hero.damaged
	flameimp = game.player1.give("EX1_319")
	flameimp.play()
	assert watcher.atk == watcher.health == 6
	assert game.player1.hero.armor == 2
	assert not game.player1.hero.damaged


def test_gahzrilla():
	game = prepare_game()
	gahz = game.player1.give("GVG_049")
	gahz.play()
	assert gahz.atk == 6
	game.player1.give(MOONFIRE).play(target=gahz)
	assert gahz.atk == 6 * 2
	timberwolf = game.player1.give("DS1_175")
	timberwolf.play()
	assert gahz.atk == (6 * 2) + 1
	# TODO: Buffs are always taken into account at the end
	# game.player1.give(MOONFIRE).play(target=gahz)
	# assert gahz.atk == (6*2*2) + 1


def test_gallywix():
	game = prepare_game()
	gallywix = game.player1.give("GVG_028")
	gallywix.play()
	game.end_turn()

	game.player1.discard_hand()
	game.player2.discard_hand()
	game.player2.give("CS2_029").play(target=game.player1.hero)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == "CS2_029"
	assert len(game.player2.hand) == 1
	assert game.player2.hand[0].id == "GVG_028t"
	game.player2.hand[0].play()
	assert game.player2.temp_mana == 1
	assert len(game.player2.hand) == 0


def test_gazlowe():
	game = prepare_empty_game()
	game.player1.discard_hand()
	game.player1.give("GVG_117").play()
	assert len(game.player1.hand) == 0
	smite = game.player1.give("CS1_130")
	assert smite.cost == 1
	smite.play(target=game.player2.hero)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.MECHANICAL


def test_gazlowe_preparation():
	game = prepare_empty_game()
	game.player1.give("GVG_117").play()
	fireball = game.player1.give("CS2_029")
	assert fireball.cost == 4
	game.player1.give("EX1_145").play()
	assert fireball.cost == 1
	fireball.play(target=game.player2.hero)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.MECHANICAL


def test_goblin_blastmage():
	game = prepare_game()
	blastmage1 = game.player1.give("GVG_004")
	assert not blastmage1.powered_up
	assert game.player1.hero.health == 30
	blastmage1.play()
	assert game.player1.hero.health == 30
	game.end_turn(); game.end_turn()

	blastmage2 = game.player1.give("GVG_004")
	assert not blastmage2.powered_up
	clockwork = game.player1.give("GVG_082")
	clockwork.play()
	assert clockwork.race == Race.MECHANICAL
	assert blastmage2.powered_up
	blastmage2.play()
	assert game.player2.hero.health == 30 - 4
	game.end_turn(); game.end_turn()


def test_grove_tender():
	game = prepare_game(game_class=Game)
	for i in range(3):
		game.end_turn(); game.end_turn()

	assert game.player1.max_mana == 4
	assert game.player2.max_mana == 3
	grovetender1 = game.player1.give("GVG_032")
	grovetender1.play(choose="GVG_032a")
	assert game.player1.max_mana == 5
	assert game.player2.max_mana == 4
	assert game.player1.mana == 2
	assert game.player1.used_mana == 3
	game.end_turn(); game.end_turn()

	game.player1.discard_hand()
	game.player2.discard_hand()
	grovetender2 = game.player1.give("GVG_032")
	grovetender2.play(choose="GVG_032b")
	assert len(game.player1.hand) == 1
	assert len(game.player2.hand) == 1


def test_hobgoblin():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	assert wisp.health == 1
	hobgoblin = game.player1.give("GVG_104")
	hobgoblin.play()

	wolf1 = game.player1.give("DS1_175")
	wolf1.play()
	assert wolf1.atk == 3
	assert wolf1.health == 3

	wolf2 = game.player1.give("DS1_175")
	wolf2.play()
	assert wolf1.atk == 4
	assert wolf1.health == 3
	assert wolf2.atk == 4
	assert wolf2.health == 3

	loothoarder = game.player1.give("EX1_096")
	loothoarder.play()
	assert not loothoarder.buffs
	assert loothoarder.atk == 2
	assert loothoarder.health == 1

	# TODO: Test faceless-hobgoblin interaction
	# assert wisp.health == 1
	# assert wisp.atk == 1
	# faceless = game.player1.give("EX1_564")
	# faceless.play(target=wisp)
	# assert not faceless.buffs
	# assert faceless.atk == 1
	# assert faceless.health == 1


def test_implosion():
	game = prepare_game()
	mogushan = game.player1.give("EX1_396")
	mogushan.play()
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	implosion = game.player2.give("GVG_045")
	assert len(implosion.targets) == 2
	assert mogushan in implosion.targets
	assert wisp in implosion.targets
	wisp.destroy()
	assert len(game.player2.field) == 0
	implosion.play(target=mogushan)
	assert 2 <= len(game.player2.field) <= 4
	assert not mogushan.dead
	assert mogushan.health == 7 - len(game.player2.field)


def test_iron_juggernaut():
	game = prepare_empty_game()
	game.player2.discard_hand()
	juggernaut = game.player1.give("GVG_056")
	assert len(game.player2.deck) == 0
	juggernaut.play()

	assert game.player2.hero.health == 30
	assert len(game.player2.deck) == 1
	assert len(game.player2.hand) == 0
	game.end_turn()
	assert game.player2.hero.health == 20
	assert len(game.player2.deck) == 0
	assert len(game.player2.hand) == 0


def test_light_of_the_naaru():
	game = prepare_game()
	naaru1 = game.player1.give("GVG_012")
	naaru2 = game.player1.give("GVG_012")
	naaru3 = game.player1.give("GVG_012")
	assert game.player1.hero.health == 30
	naaru1.play(target=game.player1.hero)
	assert not game.player1.field
	assert game.player1.hero.health == 30

	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 29
	naaru2.play(target=game.player1.hero)
	assert not game.player1.field
	assert game.player1.hero.health == 30

	for i in range(5):
		game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 25
	naaru3.play(target=game.player1.hero)
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "EX1_001"
	assert game.player1.hero.health == 28


def test_lightbomb():
	game = prepare_game()

	wisp = game.player1.give(WISP)
	wisp.play()
	assert wisp.health == wisp.atk

	game.player1.give(LIGHTS_JUSTICE).play()
	assert game.player1.hero.atk > 0
	assert game.player1.hero.health == 30
	game.end_turn()

	dummy = game.player2.give(TARGET_DUMMY)
	dummy.play()
	assert dummy.health == 2
	assert dummy.atk == 0

	goldshire = game.player2.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	assert goldshire.atk == 1
	assert goldshire.health == 2
	game.end_turn()

	lightbomb = game.player1.give("GVG_008")
	lightbomb.play()
	assert wisp.dead
	assert not dummy.dead
	assert dummy.health == 2
	assert goldshire.health == 1
	assert game.player1.hero.health == 30


def test_malganis():
	game = prepare_game(HUNTER, HUNTER)
	voidwalker = game.player1.give("CS2_065")
	voidwalker.play()
	malganis = game.player1.give("GVG_021")
	assert voidwalker.atk == 1
	assert voidwalker.health == 3
	malganis.play()
	assert voidwalker.atk == 1 + 2
	assert voidwalker.health == 3 + 2
	assert game.player1.hero.immune
	game.end_turn()

	game.player2.hero.power.use()
	assert game.player1.hero.health == 30
	malganis.destroy()
	assert voidwalker.atk == 1
	assert voidwalker.health == 3


def test_malorne():
	game = prepare_empty_game()
	assert len(game.player1.deck) == 0
	malorne = game.player1.give("GVG_035")
	malorne.play()
	malorne.destroy()
	assert len(game.player1.deck) == 1
	game.player1.draw()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == "GVG_035"


def test_mechwarper():
	game = prepare_game()
	mechwarper = game.player1.give("GVG_006")
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	harvest = game.player1.give("EX1_556")
	clockwork = game.player1.give("GVG_082")
	clockwork2 = game.player1.give("GVG_082")
	assert harvest.cost == 3
	assert goldshire.cost == 1
	assert clockwork.cost == clockwork2.cost == 1

	mechwarper.play()
	assert harvest.cost == 3 - 1
	assert goldshire.cost == 1
	assert clockwork.cost == clockwork2.cost == 0

	clockwork.play()
	assert clockwork.cost == 1

	game.player1.give(SILENCE).play(target=mechwarper)
	assert harvest.cost == 3
	assert goldshire.cost == 1
	assert clockwork.cost == clockwork2.cost == 1

	mechwarper.destroy()
	assert harvest.cost == 3
	assert goldshire.cost == 1
	assert clockwork.cost == clockwork2.cost == 1


def test_mekgineer_thermaplugg():
	game = prepare_game()
	mekgineer = game.player1.give("GVG_116")
	mekgineer.play()

	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	game.player1.give(MOONFIRE).play(target=wisp1)
	assert wisp1.dead
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	game.end_turn()

	wisp2 = game.player2.give(WISP)
	wisp2.play()
	game.player2.give(MOONFIRE).play(target=wisp2)
	assert wisp2.dead
	assert len(game.player1.field) == 2
	assert len(game.player1.field.filter(id="EX1_029")) == 1
	assert len(game.player2.field) == 0


def test_metaltooth_leaper():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	dummy = game.player1.give(TARGET_DUMMY)
	dummy.play()
	metaltooth = game.player1.give("GVG_048")
	metaltooth.play()
	assert metaltooth.atk == 3
	assert metaltooth.health == 3
	assert wisp.atk == 1
	assert dummy.atk == 0 + 2


def test_micro_machine():
	game = prepare_game()
	micro = game.player1.give("GVG_103")
	micro.play()
	assert micro.atk == 1
	game.end_turn()

	assert micro.atk == 2
	game.end_turn()

	assert micro.atk == 3
	game.end_turn()

	assert micro.atk == 4


def test_neptulon():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	assert len(game.player1.hand) == 0
	assert len(game.player2.hand) == 0
	game.player1.give("GVG_042").play()
	assert len(game.player1.hand) == 4
	assert len(game.player2.hand) == 0
	for i in range(4):
		assert game.player1.hand[i].race == Race.MURLOC
	assert game.player1.overloaded == 3


def test_powermace():
	game = prepare_game()

	wisp = game.player1.give(WISP)
	wisp.play()
	powermace1 = game.player1.give("GVG_036")
	powermace1.play()
	assert wisp.atk == 1
	assert wisp.health == 1
	powermace1.destroy()
	assert wisp.atk == 1
	assert wisp.health == 1

	dummy = game.player1.give(TARGET_DUMMY)
	dummy.play()
	powermace2 = game.player1.give("GVG_036")
	powermace2.play()
	assert dummy.atk == 0
	assert dummy.health == 2
	powermace2.destroy()
	assert dummy.atk == 0 + 2
	assert dummy.health == 2 + 2


def test_recombobulator():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	recom = game.player1.give("GVG_108")
	recom.play(target=wisp)
	recom.destroy()

	assert wisp not in game.player1.field
	assert game.player1.field[0].cost == 0


def test_recombobulator_molten_giant():
	game = prepare_game()
	game.player1.hero.set_current_health(15)

	molten = game.player1.give("EX1_620")
	assert molten.cost == 5
	molten.play()
	game.end_turn(); game.end_turn()

	recom = game.player1.give("GVG_108")
	recom.play(target=molten)
	recom.destroy()

	assert molten not in game.player1.field
	assert game.player1.field[0].cost == 20


def test_reversing_switch():
	game = prepare_game()
	switch = game.player1.give("PART_006")
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	game.end_turn(); game.end_turn()

	switch.play(goldshire)
	assert goldshire.atk == 2


def test_sabotage():
	game = prepare_game()
	sabotage = game.player1.give("GVG_047")
	sabotage.play()

	sabotage2 = game.player1.give("GVG_047")
	sabotage2.play()
	game.end_turn()

	weapon = game.player2.give(LIGHTS_JUSTICE)
	weapon.play()
	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	sabotage3 = game.player1.give("GVG_047")
	sabotage3.play()
	assert not weapon.dead
	assert wisp.dead

	sabotage4 = game.player1.give("GVG_047")
	sabotage4.play()
	assert weapon.dead


def test_siege_engine():
	game = prepare_game(WARRIOR, WARRIOR)
	engine = game.player1.give("GVG_086")
	engine.play()
	assert engine.atk == 5
	game.player1.hero.power.use()
	assert game.player1.hero.armor == 2
	assert engine.atk == 6
	game.end_turn()
	game.player2.hero.power.use()
	assert engine.atk == 6
	game.end_turn()

	# Shield Block
	game.player1.give("EX1_606").play()
	assert game.player1.hero.armor == 7
	assert engine.atk == 7


def test_siltfin_spiritwalker():
	game = prepare_game()
	game.player1.discard_hand()
	siltfin = game.player1.give("GVG_040")
	siltfin.play()
	murloc = game.player1.give(MURLOC)
	murloc.play()
	game.player1.give(MOONFIRE).play(target=murloc)
	assert len(game.player1.hand) == 1


def test_shrinkmeister():
	game = prepare_game()
	dummy = game.player1.give(TARGET_DUMMY)
	dummy.play()
	wisp = game.player1.give(WISP)
	wisp.play()
	boulderfist = game.player1.give("CS2_200")
	boulderfist.play()
	game.end_turn()

	assert dummy.atk == 0
	game.player2.give("GVG_011").play(target=dummy)
	assert dummy.buffs
	assert dummy.atk == 0

	assert wisp.atk == 1
	game.player2.give("GVG_011").play(target=wisp)
	assert wisp.buffs
	assert wisp.atk == 0

	assert boulderfist.atk == 6
	game.player2.give("GVG_011").play(target=boulderfist)
	assert boulderfist.buffs
	assert boulderfist.atk == 6 - 2
	game.end_turn()

	# ensure buffs are gone after end of turn
	assert not dummy.buffs
	assert dummy.atk == 0
	assert not wisp.buffs
	assert wisp.atk == 1
	assert not boulderfist.buffs
	assert boulderfist.atk == 6


def test_tinkertown_technician():
	game = prepare_game()
	game.player1.discard_hand()
	game.player1.give(WISP).play()
	tech = game.player1.give("GVG_102")
	tech.play()
	assert tech.atk == tech.health == 3
	assert len(game.player1.hand) == 0

	dummy = game.player1.give(TARGET_DUMMY)
	dummy.play()
	tech2 = game.player1.give("GVG_102")
	tech2.play()
	assert tech2.atk == tech2.health == 4
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].type == CardType.SPELL


def test_tree_of_life():
	game = prepare_game()
	token1 = game.player1.give(SPELLBENDERT)
	token1.play()
	tree = game.player1.give("GVG_033")
	game.end_turn()

	token2 = game.player2.give(SPELLBENDERT)
	token2.play()
	game.end_turn()

	targets = (game.player1.hero, game.player2.hero, token1, token2)
	for target in targets:
		game.player1.give(MOONFIRE).play(target=target)

	assert token1.health == token2.health == 3 - 1
	assert game.player1.hero.health == game.player2.hero.health == 30 - 1
	tree.play()
	assert token1.health == token2.health == 3
	assert game.player1.hero.health == game.player2.hero.health == 30


def test_unstable_portal():
	game = prepare_game()
	game.player1.discard_hand()
	portal = game.player1.give("GVG_003")
	portal.play()
	assert len(game.player1.hand) == 1
	minion = game.player1.hand[0]
	assert minion.type == CardType.MINION
	assert minion.creator is portal
	assert minion.buffs


def test_voljin():
	game = prepare_game()
	voljin = game.player1.give("GVG_014")
	deathwing = game.player1.summon("NEW1_030")
	assert voljin.health == 2
	assert deathwing.health == 12
	voljin.play(target=deathwing)
	assert voljin.health == 12
	assert deathwing.health == 2


def test_voljin_stealth():
	game = prepare_game()
	tiger = game.player1.give("EX1_028")
	tiger.play()
	game.end_turn()

	voljin = game.player2.give("GVG_014")
	assert not voljin.targets
	voljin.play()
	assert not voljin.dead
	assert voljin.health == 2
	assert tiger.health == 5
