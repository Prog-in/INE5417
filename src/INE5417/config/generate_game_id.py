from time import time

milliseconds = int(time() * 1000)
game_id = str(milliseconds - 1639872000000)
file = open("game.id", "w")
file.write(game_id)
file.close()
