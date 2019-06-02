import sys, traceback
import sqlite3

class TextCondition:

    def __init__(self, condition, repText):
        self.condition = condition
        self.repText = repText

        self.fired = False

    def eval(self, information):
        try:
            return eval(self.condition, information)
        except NameError:
            return False # Means the condition cannot be checked with current information
        except:
            traceback.print_exc()

    def save_to_db(self, textconditiondb):
        textconditiondb.save_condition(self)

class TextConditionDatabase:

    batchCommit = False
    def __init__(self, filename = 'conditions.db'):
        self.conn = sqlite3.connect(filename)

    def initdb(self):
        ### Hardcoded Textconditions
        c = self.conn.cursor()

        # Create table
        c.execute('''CREATE TABLE textconditions (condition text, reptext text)''')

        # Commit table
        self.conn.commit()

        # Insert Data
        self.batchCommit = True

        conditions = [
            TextCondition('action == \'KILLED\' and killinfo[2].startswith(\'npc_dota_hero\')', '[{0}] {3} manages to kill {4}.'),
            TextCondition('action == \'KILLED\' and killinfo[2].startswith(\'npc_dota_hero\')', '[{0}] {3} kills {4}.'),
            TextCondition('action == \'KILLED\' and killinfo[2].startswith(\'npc_dota_hero\')', '[{0}] {4} gets killed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2].startswith(\'npc_dota_hero\')', '[{0}] {4} is dead!'),
            TextCondition('action == \'KILLED\' and killinfo[2].startswith(\'npc_dota_hero\')', '[{0}] {3} cuts the throat of {4}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_roshan\'', '[{0}] {3} is able to kill rosh!'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_roshan\'', '[{0}] {3} kills roshan!'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_roshan\'', '[{0}] Roshan gets killed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_roshan\'', '[{0}] Rosh is down - killed by {3}!'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_tower3_bot\'', '[{0}] Radiant\'s bottom (T3) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_tower2_bot\'', '[{0}] Radiant\'s bottom (T2) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_tower1_bot\'', '[{0}] Radiant\'s bottom (T1) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_tower3_top\'', '[{0}] Radiant\'s top (T3) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_tower2_top\'', '[{0}] Radiant\'s top (T2) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_tower1_top\'', '[{0}] Radiant\'s top (T1) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_tower1_mid\'', '[{0}] Radiant\'s mid (T1) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_tower2_mid\'', '[{0}] Radiant\'s mid (T2) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_tower3_mid\'', '[{0}] Radiant\'s mid (T3) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_tower3_bot\'', '[{0}] Dire\'s bottom (T3) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_tower2_bot\'', '[{0}] Dire\'s bottom (T2) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_tower1_bot\'', '[{0}] Dire\'s bottom (T1) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_tower3_top\'', '[{0}] Dire\'s top (T3) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_tower2_top\'', '[{0}] Dire\'s top (T2) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_tower1_top\'', '[{0}] Dire\'s top (T1) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_tower1_mid\'', '[{0}] Dire\'s mid (T1) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_tower2_mid\'', '[{0}] Dire\'s mid (T2) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_tower3_mid\'', '[{0}] Dire\'s mid (T3) tower is destroyed by {3}.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_fort\'', '[{0}] Dire\'s ancient was detroyed - Radiants win the game.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_fort\'', '[{0}] The Dire\'s ancient is down - Radiants win the game.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_badguys_fort\'', '[{0}] Radiants bringing down the ancient and winning the game.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_fort\'', '[{0}] Radiant\'s ancient was detroyed - Dire win the game.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_fort\'', '[{0}] The Radiant\'s ancient is down - Dire win the game.'),
            TextCondition('action == \'KILLED\' and killinfo[2] == \'npc_dota_goodguys_fort\'', '[{0}] Dire bringing down the ancient and winning the game.'),
            TextCondition('action == \'SMOKED\'', '[{0}] {1} are smoking to find some good kills')
                    ]
        for condition in conditions:
            condition.save_to_db(self)

        self.batchCommit = False
        self.conn.commit()

    def save_condition(self, textcondition):
        c = self.conn.cursor()
        c.execute("INSERT INTO textconditions VALUES (?, ?)", (textcondition.condition, textcondition.repText))
        if self.batchCommit == False:
            self.conn.commit()

    def get_all_conditions(self):
        c = self.conn.cursor()
        conditions = []
        for row in c.execute('SELECT condition, reptext FROM textconditions'):
            conditions.append(TextCondition(row[0], row[1]))
        return conditions

if __name__ == '__main__':
    ## Super short testing -- should print yikes
    conditions = [TextCondition('1==1', 'yikes'), TextCondition('1==0', 'nope')]
    for condition in conditions:
        if condition.eval({}):
            print(condition.repText)
