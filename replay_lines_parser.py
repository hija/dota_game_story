import jsonlines

class ReplayWindow:

    def __init__(self, window_data):
        self.window_data = window_data

    def calculate_window(self):
        pass

class ReplayLinesParser:

    def __init__(self, replay_file_path):
        self.replay_file_path = replay_file_path

    def parse_replay_to_windows(self, timeframe = 5, overlap = 3):
        with jsonlines.open(self.replay_file_path) as jsonreader:
            replay_data = list(jsonreader)
            #timestamp = replay_data[0]['time']
            timestamp_replay_data = dict()
            for dataline in replay_data:
                timestamp = dataline['time']
                timestamp_replay_data[timestamp] = dataline

            timestamp_data_array = [timestamp_replay_data[key] for key in sorted(timestamp_replay_data)]

            all_windows_data = []
            for i in range(0, len(timestamp_data_array),timeframe - overlap):
                window_data = []
                for j in range(i, (i+timeframe)):
                    window_data.append(replay_data[j])
                i += (timeframe - overlap)
                all_windows_data.append(window_data)

            ## Calculate values for each window


if __name__ == '__main__':
    rlp = ReplayLinesParser('replay/4725370654.json')
    rlp.parse_replay_to_windows()
