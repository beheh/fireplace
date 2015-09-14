#!/usr/bin/env python
import sys; sys.path.append("..")
import traceback
import logging
import random
import time
import os

from io import StringIO
from fireplace.cards.heroes import *
from fireplace.game import Game, GameOver
from fireplace.player import Player
from fireplace.utils import random_draft

logging.getLogger().setLevel(logging.DEBUG)

HEROES = [WARRIOR, SHAMAN, ROGUE, PALADIN, HUNTER, DRUID, WARLOCK, MAGE, PRIEST]

consoleLogger = logging.getLogger('fuzzy')
consoleLogger.addHandler(logging.StreamHandler())

def main():
	consoleLogger.info("Starting fuzzy test run")
	i = 0
	while True:
		buffer = StringIO()
		rootLogger = logging.getLogger('fireplace')
		rootLogger.setLevel(logging.DEBUG)
		rootLogger.handlers = []
		logHandler = logging.StreamHandler(buffer)
		rootLogger.addHandler(logHandler)
		try:
			hero1 = random.choice(HEROES)
			hero2 = random.choice(HEROES)
			deck1 = random_draft(hero=hero1)
			deck2 = random_draft(hero=hero2)
			player1 = Player(name="Player1")
			player1.prepare_deck(deck1, hero1)
			player2 = Player(name="Player2")
			player2.prepare_deck(deck2, hero2)

			game = Game(players=(player1, player2))
			game.start()

			for player in game.players:
				rootLogger.info("Can mulligan %r" % (player.choice.cards))
				mull_count = random.randint(0, len(player.choice.cards))
				cards_to_mulligan = random.sample(player.choice.cards, mull_count)
				player.choice.choose(*cards_to_mulligan)

			while True:
				player = game.current_player
				heropower = game.current_player.hero.power
				# sometimes play the hero power, just for kicks
				if heropower.is_usable() and random.randint(0, 3) == 0:
					if heropower.has_target():
						heropower.use(target=random.choice(heropower.targets))
					else:
						heropower.use()

				# iterate over our hand and play whatever is playable
				for card in game.current_player.hand:
					if card.is_playable() and random.randint(0, 2) == 0:
						target = None
						choice = None
						if card.has_target():
							target = random.choice(card.targets)
						if card.data.choose_cards:
							# choice = random.choice(card.data.choose_cards)
							continue
						card.play(target=target, choose=choice)
					else:
						rootLogger.info("Not playing %r" % (card))

				# Randomly attack with whatever can attack
				for character in game.current_player.characters:
					if character.can_attack() and random.randint(0, 3) != 0:
						character.attack(random.choice(character.targets))

				if player.choice:
					choice = random.choice(player.choice.cards)
					rootLogger.info("Choosing card %r" % (choice))
					player.choice.choose(choice)
					continue

				game.end_turn()
		except GameOver:
			i = i + 1
			if i % 50 == 0:
				consoleLogger.info("Completed %d game(s)" % (i))
			continue
		except Exception as e:
			buffer.flush()
			logHandler.flush()
			exc_type, exc_obj, tb = sys.exc_info()
			f = traceback.extract_tb(tb)[-1]
			location = "{}:{}".format(os.path.basename(f[0]), f[1])
			
			os.makedirs(name="err", exist_ok=True)
			filename = "err/{}.{}.txt".format(location, exc_type.__name__)
			if os.path.isfile(filename):
				consoleLogger.info("Ignoring %s in %s" % (exc_type.__name__, location))
				continue
			consoleLogger.warning("Error found: %s in %s" % (exc_type.__name__, location))
			out = open(filename, 'w')			
			out.write(traceback.format_exc())
			out.write(buffer.getvalue())
			out.flush()
			out.close()

		rootLogger.removeHandler(logHandler)        

if __name__ == "__main__":
	main()
