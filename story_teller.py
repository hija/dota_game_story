import text_conditioner
import random

class StoryTeller:

    def __init__(self, all_windows):
        self.all_windows = all_windows

    def generate_story(self):
        db = text_conditioner.TextConditionDatabase()
        cons = db.get_all_conditions()
        for window in self.all_windows:
            for con in cons:
                info_dict = window.get_info_dict()
                text_choices = []
                for kill in info_dict['kills']:
                    if con.eval({'action': 'KILLED', 'killinfo': kill}):
                        text_choices.append(con.repText.format(*kill))
                if len(text_choices):
                    print(random.choice(text_choices))
