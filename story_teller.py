import text_conditioner
import random

class StoryTeller:

    def __init__(self, all_windows):
        self.all_windows = all_windows

    def generate_story(self):
        db = text_conditioner.TextConditionDatabase()
        cons = db.get_all_conditions()
        for window in self.all_windows:
            info_dict = window.get_info_dict()
            for kill in info_dict['kills']:
                text_choices = []
                for con in cons:
                    if con.eval({'action': 'KILLED', 'killinfo': kill}):
                        text_choices.append(con.repText.format(*kill))
                if len(text_choices):
                    print(random.choice(text_choices))

            if len(info_dict['smoked']) > 0:
                text_choices = []
                for con in cons:
                    # Beautify smoked heroes
                    smoked_heroes = ', '.join(info_dict['smoked'][1:])
                    if con.eval({'action': 'SMOKED', 'smoked_heroes': smoked_heroes}):
                        text_choices.append(con.repText.format(info_dict['smoked'][0], smoked_heroes))
                if len(text_choices):
                    print(random.choice(text_choices))
