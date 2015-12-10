from ..utils import *


##
# Minions

# Obsidian Destroyer
class LOE_009:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOE_009t"))


# Eerie Statue
class LOE_107:
	update = Find(ALL_MINIONS - SELF) & Refresh(SELF, {GameTag.CANT_ATTACK: True})


##
# Spells

# Forgotten Torch
class LOE_002:
	play = Hit(TARGET, 3), Shuffle(CONTROLLER, "LOE_002t")

class LOE_002t:
	play = Hit(TARGET, 6)


# Curse of Rafaam
class LOE_007:
	play = Give(OPPONENT, "LOE_007t")

# Cursed!
class LOE_007t:
	in_hand = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 2))


# Raven Idol
class LOE_115:
	choose = ("LOE_115a", "LOE_115b")


##
# Secrets

# Sacred Trial
class LOE_027:
	events = Play(OPPONENT, MINION | HERO).after(
		(Count(ENEMY_MINIONS) >= 4) &
		(Reveal(SELF), Destroy(Play.CARD))
	)
