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
            TextCondition('action == \'KILLED\'', '{1} manages to kill {2}.'),
            TextCondition('action == \'KILLED\'', '{1} kills {2}.'),
            TextCondition('action == \'KILLED\'', '{2} gets killed by {1}.'),
            TextCondition('action == \'KILLED\'', '{2} is dead!'),
            TextCondition('action == \'KILLED\'', '{1} cuts the throat of {2}.')
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
