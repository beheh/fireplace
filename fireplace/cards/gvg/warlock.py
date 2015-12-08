from ..utils import *


##
# Minions

# Mistress of Pain
class GVG_018:
	events = Damage().on(
		lambda self, target, amount, source: source is self and Heal(FRIENDLY_HERO, amount)
	)


# Fel Cannon
class GVG_020:
	events = OWN_TURN_END.on(Hit(RANDOM(ALL_MINIONS - MECH), 2))


# Mal'Ganis
class GVG_021:
	update = (
		Refresh(FRIENDLY_MINIONS + DEMON - SELF, buff="GVG_021e"),
		Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True}),
	)

GVG_021e = buff(+2, +2)


# Anima Golem
class GVG_077:
	events = TURN_END.on(Find(FRIENDLY_MINIONS - SELF) | Destroy(SELF))


# Floating Watcher
class GVG_100:
	events = Damage(FRIENDLY_HERO).on(
		lambda self, target, amount, source: self.controller.current_player and Buff(SELF, "GVG_100e")
	)

GVG_100e = buff(+2, +2)


##
# Spells

# Darkbomb
class GVG_015:
	play = Hit(TARGET, 3)


# Demonheart
class GVG_019:
	play = Find(TARGET + FRIENDLY + DEMON) & Buff(TARGET, "GVG_019e") | Hit(TARGET, 5)

GVG_019e = buff(+5, +5)


# Imp-losion
class GVG_045:
	play = Hit(TARGET, RandomNumber(2, 3, 4)), Summon(CONTROLLER, "GVG_045t") * RandomNumber(2, 3, 4)
