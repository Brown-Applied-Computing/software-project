import xml.etree.ElementTree as ET

class Prompter: # Abstract prompter that we can subclass
    def __init__(self):
        pass
    
    def make_prompt(self, context):
        # Returns a prompt given some context
        return ""
    def make_valid_play(self, play):
        # Takes in a play from the user. Should make the play and returns True if it is valid, returns False otherwise.
        return len(play) > 0
    def game_over(self, context):
        # Returns True when the game ends so that we can exit the game.
        return False

class Player: # Abstract player that we can subclass
    def __init__(self):
        pass

    def play(self, context):
        # Returns a play given a context
        return ""

class Context:
    def __init__(self):
        self.prev = [] # list of previous prompts and valid plays
        self.vars = {} # miscellaneous variables (including those specific to the scenario)
    def add_prompt(self, prompt):
        self.prev.append(("prompter", prompt))
    def add_play(self, play):
        self.prev.append(("player", play))
    def set_var(self, var, val):
        self.vars[var] = eval(val) # use eval because the val argument will be a string, such as "True"

def play_game(player, prompter, context):
    while True:
        prompt = prompter.make_prompt(context)
        print(prompt)
        if prompter.game_over(context):
            break

        play = player.play(prompt)
        while not prompter.make_valid_play(play, context):
            # keep asking the user for a play until we get a valid one
            play = player.play(prompt)

class BasicPrompter(Prompter):
    def __init__(self, file, context):
        super().__init__()
        self.room_id = "0"
        self.xml = ET.parse(file).getroot() # parse the XML file containing information about the scenario

        context.vars = {} # initialize context variables
        var_init = self.xml.findall('var')
        for var in var_init:
            context.vars[var.attrib['name']] = eval(var.text)
        context.vars["game_over"] = False
    
    def current_room(self):
        # returns the current room in the XML file based on the prompter's room_id variable
        for room in self.xml.findall('room'):
            if room.attrib["id"] == self.room_id:
                return room
        raise Exception("Moved to a room that does not exist in the XML file")

    def eval_flag(self, flag, context):
        # evaluates flags. For example, "$got_quesadilla and not $defeated_burgers"
        # would evaluate to context.vars["got_quesadilla"] and not context.vars["defeated_burgers"],
        # which may be true or false depending on the state of the context.
        flag = flag.split(" ")
        for i in range(len(flag)):
            if flag[i].startswith("$"):
                flag[i] = "context.vars['"+flag[i][1:]+"']"
        flag = ' '.join(flag)
        return eval(flag)
    
    def make_prompt(self, context):
        prompts = self.current_room().findall('prompt')
        for prompt in prompts:
            try:
                if self.eval_flag(prompt.attrib["flag"], context): # only uses prompts whose flags are True
                    try:
                        if prompt.attrib["gameover"] == '1':
                            context.vars["game_over"] = True # sets the game to be over if specified by the prompt
                    except KeyError: pass

                    try:
                        context.set_var(prompt.attrib["var"], prompt.attrib["val"]) # sets variables of the prompt, if specified
                    except KeyError: pass

                    context.add_prompt(prompt.text.strip()) # adds this prompt to the context
                    return prompt.text.strip()
            except KeyError:
                continue
        
        # if none of the flags were True, or no flags were given, use the first prompt
        context.add_prompt(prompts[0].text.strip()) # adds the first prompt to the context
        return prompts[0].text.strip()
    
    def make_valid_play(self, play, context):
        # Takes in a play from the user. Should make the play and returns True if it is valid, returns False otherwise.
        plays = self.current_room().findall('play')
        for p in plays:
            if p.text == play:
                try:
                    if not self.eval_flag(p.attrib["flag"], context): # does not allow a play if its flag is False
                        continue
                except KeyError: pass

                try:
                    self.room_id = p.attrib["to"] # moves to the room of the play, if specified
                except KeyError: pass
                try:
                    context.set_var(p.attrib["var"], p.attrib["val"]) # sets variables of the play, if specified
                except KeyError: pass

                context.add_play(play) # adds this play to the context
                return True
        return False

    def game_over(self, context):
        return context.vars["game_over"]

class BasicPlayer(Player):
    def __init__(self):
        super().__init__()

    def play(self, context):
        return input("> ") # takes input from a user
