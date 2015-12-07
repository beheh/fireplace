from utils import *


def test_beneath_the_grounds():
	game = prepare_empty_game()
	game.player2.discard_hand()
	assert len(game.player2.deck) == 0
	grounds = game.player1.give("AT_035")
	grounds.play()
	assert len(game.player2.deck) == 3
	assert len(game.player2.hand) == 0
	game.end_turn()

	assert len(game.player2.hand) == 0
	assert len(game.player1.field) == 3
	for minion in game.player1.field:
		assert minion.id == "AT_036t"


def test_burgle():
	game = prepare_empty_game()
	burgle = game.player1.give("AT_033")
	burgle.play()
	assert len(game.player1.hand) == 2
	assert game.player1.hand[0].card_class == game.player2.hero.card_class
	assert game.player1.hand[0].type != CardType.HERO
	assert game.player1.hand[1].card_class == game.player2.hero.card_class
	assert game.player1.hand[1].type != CardType.HERO


def test_dark_bargain():
	game = prepare_game()
	for i in range(3):
		game.player2.summon(WISP)
	assert len(game.player2.field) == 3
	assert len(game.player1.hand) == 4
	bargain = game.player1.give("AT_025")
	bargain.play()
	assert len(game.player2.field) == 1
	assert len(game.player1.hand) == 2


def test_demonfuse():
	game = prepare_game()
	game.player2.max_mana = 9
	demonfuse = game.player1.give("AT_024")
	game.player2.summon(WISP)
	imp = game.player1.give(IMP)
	imp.play()
	game.player2.summon(IMP)
	assert len(demonfuse.targets) == 2
	assert imp.atk == imp.health == 1
	demonfuse.play(target=imp)
	assert imp.atk == imp.health == 4
	assert game.player2.max_mana == 10


def test_demonfuse_sense_demons():
	# https://github.com/HearthSim/hs-bugs/issues/111
	game = prepare_empty_game()
	demonfuse1 = game.player1.give("AT_024")
	demonfuse1.shuffle_into_deck()
	demonfuse2 = game.player1.give("AT_024")
	demonfuse2.shuffle_into_deck()
	sense = game.player1.give("EX1_317")
	sense.play()
	assert demonfuse1.zone == Zone.DECK
	assert demonfuse2.zone == Zone.DECK


def test_dragonhawk_rider():
	game = prepare_game(WARRIOR, WARRIOR)
	rider = game.player1.give("AT_083")
	game.player1.hero.power.use()
	rider.play()
	assert not rider.windfury
	game.end_turn()

	# do not trigger on enemy hero power
	game.player2.hero.power.use()
	assert not rider.windfury
	game.end_turn()

	# should gain windfury on inspire for single turn
	game.player1.hero.power.use()
	assert rider.windfury
	rider.attack(game.player2.hero)
	rider.attack(game.player2.hero)
	game.end_turn()

	assert not rider.windfury
	game.end_turn()

	# should lose windfury and effect when silenced
	game.player1.hero.power.use()
	assert rider.windfury
	rider.attack(game.player2.hero)
	assert rider.can_attack()
	game.player1.give(SILENCE).play(target=rider)
	assert not rider.windfury
	assert not rider.can_attack()
	game.end_turn(); game.end_turn()
	game.player1.hero.power.use()
	assert not rider.windfury


def test_dreadsteed():
	game = prepare_game()
	dreadsteed = game.player1.give("AT_019")
	dreadsteed.play()
	assert len(game.player1.field) == 1
	game.player1.give(MOONFIRE).play(target=dreadsteed)
	assert dreadsteed.dead
	assert len(game.player1.field) == 1


def test_fencing_coach():
	game = prepare_game(WARRIOR, WARRIOR)
	coach = game.player1.give("AT_115")
	assert game.player1.hero.power.cost == 2
	coach.play()
	assert game.player1.hero.power.cost == 0
	game.end_turn(); game.end_turn()

	assert game.player1.hero.power.cost == 0
	game.player1.hero.power.activate()
	assert game.player1.hero.power.cost == 2


def test_fist_of_jaraxxus():
	game = prepare_empty_game()
	fist1 = game.player1.give("AT_022")
	assert game.player2.hero.health == 30
	game.player1.give(SOULFIRE).play(target=game.player1.hero)
	assert game.player2.hero.health == 30 - 4
	assert fist1.zone == Zone.DISCARD
	fist2 = game.player1.give("AT_022")
	fist2.play()
	assert game.player2.hero.health == 30 - 4 - 4


def test_gormok_the_impaler():
	game = prepare_game()
	yeti = game.player1.give("CS2_182")
	dummy1 = game.player1.give(TARGET_DUMMY)
	yeti.play()
	dummy1.play()
	game.end_turn()

	gormok1 = game.player2.give("AT_122")
	assert not gormok1.has_target()
	gormok1.play()
	assert game.player1.hero.health == game.player1.hero.max_health
	assert yeti.health == 5
	assert dummy1.health == 2

	game.player2.discard_hand()
	gormok2 = game.player2.give("AT_122")
	wisp1 = game.player2.give(WISP)
	wisp2 = game.player2.give(WISP)
	dummy2 = game.player2.give(TARGET_DUMMY)
	wisp1.play()
	wisp2.play()
	dummy2.play()
	assert len(game.player2.field) == 4
	assert gormok2.has_target()
	assert game.player1.hero in gormok2.targets
	assert game.player2.hero in gormok2.targets
	assert yeti in gormok2.targets
	assert dummy1 in gormok2.targets
	assert gormok1 in gormok2.targets
	assert wisp1 in gormok2.targets
	assert wisp2 in gormok2.targets
	assert dummy2 in gormok2.targets

	gormok2.play(target=yeti)
	assert yeti.health == 1
	assert gormok2.atk == 4 == gormok2.health == 4


def test_grand_crusader():
	game = prepare_game()
	game.player1.discard_hand()
	crusader = game.player1.give("AT_118")
	assert len(game.player1.hand) == 1
	crusader.play()
	assert len(game.player1.hand) == 1
	card = game.player1.hand[0]
	assert card.card_class == CardClass.PALADIN
	assert card.data.collectible
	assert card.type != CardType.HERO


def test_icehowl():
	game = prepare_game()
	icehowl = game.player1.give("AT_125")
	icehowl.play()
	assert icehowl.charge
	assert not icehowl.can_attack()
	assert not icehowl.can_attack(game.player2.hero)
	assert not icehowl.can_attack(game.player1.hero)
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	assert icehowl.can_attack()
	assert icehowl.attack_targets == [wisp]


def test_lance_carrier():
	game = prepare_game()
	wisp = game.player2.summon(WISP)
	carrier1 = game.player1.give("AT_084")
	assert len(carrier1.targets) == 0
	carrier1.play()
	game.end_turn()

	carrier2 = game.player2.give("AT_084")
	assert wisp.atk == 1
	carrier2.play(target=wisp)
	assert wisp.atk == 3
	game.end_turn(); game.end_turn()

	assert wisp.atk == 3


def test_lock_and_load():
	game = prepare_empty_game()
	lockandload = game.player1.give("AT_061")
	game.player1.give(THE_COIN).play()
	assert len(game.player1.hand) == 1
	lockandload.play()
	assert game.player1.hero.buffs
	assert len(game.player1.hand) == 0
	game.player1.give(THE_COIN).play()
	assert len(game.player1.hand) == 1
	card = game.player1.hand[0]
	assert card.card_class == CardClass.HUNTER
	assert card.data.collectible
	assert card.type != CardType.HERO


def test_lowly_squire():
	game = prepare_game(HUNTER, HUNTER)
	squire = game.player1.give("AT_082")
	squire.play()
	assert squire.atk == 1
	game.player1.hero.power.use()
	assert squire.atk == 2
	game.end_turn(); game.end_turn()

	assert squire.atk == 2
	game.player1.hero.power.use()
	assert squire.atk == 3


def test_seal_of_champions():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	seal1 = game.player1.give("AT_074")
	seal1.play(target=wisp)
	assert wisp.divine_shield
	assert wisp.atk == 1 + 3
	game.end_turn(); game.end_turn()

	assert wisp.divine_shield
	assert wisp.atk == 1 + 3
	game.player1.give(MOONFIRE).play(target=wisp)
	assert not wisp.divine_shield
	assert wisp.atk == 1 + 3

	seal2 = game.player1.give("AT_074")
	seal2.play(target=wisp)
	assert wisp.atk == 1 + 3 + 3
	assert wisp.divine_shield
	game.player1.give(SILENCE).play(target=wisp)
	assert wisp.atk == 1
	assert not wisp.divine_shield


def test_seal_of_champions_shrinkmeister():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	seal = game.player1.give("AT_074")
	seal.play(target=wisp)
	assert wisp.atk == 1 + 3
	shrinkmeister = game.player1.give("GVG_011")
	shrinkmeister.play(target=wisp)
	assert wisp.atk == 1 + 3 - 2
	game.end_turn()
	assert wisp.atk == 1 + 3


def test_silver_hand_regent():
	game = prepare_game(HUNTER, HUNTER)
	regent = game.player1.give("AT_100")
	regent.play()
	assert len(game.player1.field) == 1
	game.player1.hero.power.use()
	assert len(game.player1.field) == 2
	assert game.player1.field[1].id == "CS2_101t"


def test_skycapn_kragg():
	game = prepare_game()
	kragg = game.player1.give("AT_070")
	wisp = game.player1.give(WISP)
	wisp.play()
	assert kragg.cost == 7
	game.end_turn()

	pirate = game.player2.give("CS2_146")
	pirate.play()
	assert kragg.cost == 7
	game.end_turn()

	game.player1.give("CS2_146").play()
	assert kragg.cost == 7 - 1
	game.player1.field[-1].destroy()
	assert kragg.cost == 7
	game.end_turn(); game.end_turn()

	game.player1.summon("CS2_146")
	assert kragg.cost == 7 - 1
	assert game.player1.mana == 10
	kragg.play()
	assert game.player1.mana == 10 - 6


def test_tiny_knight_of_evil():
	game = prepare_empty_game()
	knight = game.player1.give("AT_021")
	knight.play()
	assert len(game.player1.hand) == 0
	game.player1.give(SOULFIRE).play(target=game.player2.hero)
	assert not knight.buffs
	assert knight.atk == 3
	assert knight.health == 2
	game.player1.give(WISP)
	game.player1.give(SOULFIRE).play(target=game.player2.hero)
	assert knight.buffs
	assert knight.atk == 3 + 1
	assert knight.health == 2 + 1


def test_void_crusher():
	game = prepare_game(WARLOCK, WARLOCK)
	for i in range(3):
		game.player2.summon(WISP)
	crusher = game.player1.give("AT_023")
	crusher.play()
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 3
	game.player1.hero.power.use()
	assert crusher.dead
	assert len(game.player1.field) == 0
	assert len(game.player2.field) == 2


def test_wilfred_fizzlebang():
	game = prepare_empty_game(WARLOCK, WARLOCK)
	game.player1.discard_hand()
	fizzlebang = game.player1.give("AT_027")
	fizzlebang.play()
	game.player1.give("CS2_029").shuffle_into_deck()
	game.player1.give("CS2_029").shuffle_into_deck()
	assert len(game.player1.deck) == 2
	assert len(game.player1.hand) == 0
	game.player1.hero.power.use()
	assert len(game.player1.hand) == 1
	fireball1 = game.player1.hand[0]
	assert fireball1.cost == 0
	fireball1.discard()
	game.end_turn(); game.end_turn()

	fireball2 = game.player1.hand[0]
	assert fireball2.cost == 4


def test_wrathguard():
	game = prepare_game()
	wrathguard = game.player1.give("AT_026")
	wrathguard.play()
	assert game.player1.hero.health == 30
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert game.player1.hero.health == 30
	game.player1.give(MOONFIRE).play(target=wrathguard)
	assert game.player1.hero.health == 30 - 1
	game.player1.give(CIRCLE_OF_HEALING)
	assert game.player1.hero.health == 29
	game.end_turn()

	wargolem = game.player2.give("CS2_186")
	wargolem.play()
	game.end_turn()

	wrathguard.attack(target=wargolem)
	assert wrathguard.dead
	assert game.player1.hero.health == 29 - 7
