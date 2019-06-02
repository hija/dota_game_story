import jsonlines

class ReplayWindow:

    def __init__(self, window_data):
        self.window_data = window_data

    def calculate_window(self):
        ## Now we "summarize" the window
        self.kills = self.get_kills()
        self.smoked = self.get_smoked()

    def get_kills(self):
        kills = []
        for data_line in self.window_data:
            if data_line['type'] == 'DOTA_COMBATLOG_DEATH':
                attacker_beautified = ReplayWindow.beautify_name(data_line['attackername'])
                target_beautified = ReplayWindow.beautify_name(data_line['targetname'])
                kills.append((data_line['time'], data_line['attackername'], data_line['targetname'], attacker_beautified, target_beautified))
        return kills

    def get_smoked(self):
        smoked = []
        for data_line in self.window_data:
            if data_line['type'] == 'DOTA_COMBATLOG_MODIFIER_ADD' and data_line['inflictor'] == 'modifier_smoke_of_deceit':
                if len(smoked) == 0:
                    smoked.append(data_line['time']) # Put time at first element
                smoked.append(ReplayWindow.beautify_name(data_line['targetname']))
        return smoked

    def get_info_dict(self):
        return {'kills': self.kills, 'smoked': self.smoked}

    def beautify_name(name):
        if name.startswith('npc_dota_hero'):
            ugly_name_parts = name[len('npc_dota_hero_'):].split('_')
            return ' '.join(['{}{}'.format(x[0].upper(), x[1:]) for x in ugly_name_parts])
        elif name.startswith('npc_dota_roshan'):
            return 'Roshan'
        else:
            return name

class ReplayLinesParser:

    def __init__(self, replay_file_path):
        self.replay_file_path = replay_file_path

    def parse_replay_to_windows(self, timeframe = 5, overlap = 0):
        with jsonlines.open(self.replay_file_path) as jsonreader:
            replay_data = list(jsonreader)
            #timestamp = replay_data[0]['time']
            timestamp_replay_data = dict()
            for dataline in replay_data:
                timestamp = dataline['time']
                current_timestamp_data = timestamp_replay_data.get(timestamp, [])
                current_timestamp_data.append(dataline)
                timestamp_replay_data[timestamp] = current_timestamp_data

            timestamp_data_array = [timestamp_replay_data[key] for key in sorted(timestamp_replay_data.keys())]

            all_windows_data = []
            for i in range(0, len(timestamp_data_array), timeframe - overlap):
                window_data = []
                for j in range(i, (i+timeframe)):
                    if j < len(timestamp_data_array):
                        window_data.extend(timestamp_data_array[j])
                all_windows_data.append(window_data)

            ## Calculate values for each window
            all_windows = []
            for window_data in all_windows_data:
                window = ReplayWindow(window_data)
                window.calculate_window()
                all_windows.append(window)
            return all_windows


if __name__ == '__main__':
    rlp = ReplayLinesParser('replay/4725370654.json')
    rlp.parse_replay_to_windows()
