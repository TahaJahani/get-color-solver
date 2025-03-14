from game import Game

json_name = input("Enter json file name: ")
game = Game.load_json(json_name)
game.print()
game.solve()
