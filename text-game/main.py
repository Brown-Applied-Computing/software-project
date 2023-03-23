from core import BasicPrompter, BasicPlayer, Context, play_game

if __name__ == "__main__":
    context = Context()
    player = BasicPlayer()
    prompter = BasicPrompter("scenarios/test.xml", context)
    play_game(player, prompter, context)