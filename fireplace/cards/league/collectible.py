from ..utils import *


##
# Minions

# Obsidian Destroyer
class LOE_009:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOE_009t"))


# Tunnel Trogg
class LOE_018:
	events = Overload(CONTROLLER).on(Buff(SELF, "LOE_018e") * Overload.AMOUNT)

LOE_018e = buff(atk=1)


# Sacred Trial
class LOE_027:
	events = Play(OPPONENT, MINION | HERO).after(
		(Count(ENEMY_MINIONS) >= 4) &
		(Reveal(SELF), Destroy(Play.CARD))
	)


##
# Spells

# Forgotten Torch
class LOE_002:
	play = Hit(TARGET, 3), Shuffle(CONTROLLER, "LOE_002t")

class LOE_002t:
	play = Hit(TARGET, 6)


# Raven Idol
class LOE_115:
	choose = ("LOE_115a", "LOE_115b")
