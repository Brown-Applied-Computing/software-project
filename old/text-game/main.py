from core import BasicPrompter, BasicPlayer, Context, play_game

if __name__ == "__main__":
    context = Context()
    player = BasicPlayer(context)
    prompter = BasicPrompter(context, "scenarios/test.xml")
    play_game(player, prompter)