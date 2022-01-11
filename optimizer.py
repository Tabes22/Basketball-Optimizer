import sys
import csv
import copy
import pandas as pd

class Optimizer:
    '''
    Optimizer class
    '''
    def __init__(self, num_lineups, overlap, solver, players_path, output_path):
        self.num_lineups = num_lineups
        self.overlap = overlap
        self.solver = solver
        self.players_df = self.load_inputs(players_path)
        self.num_players = len(self.players_df.index)
        self.output_path = output_path
        self.positions = {'PG': [],'SG': [], 'SF': [], 'PF': [], 'C': [], 'G': [], 'F': [], 'PG/': [], 'PG/SF': [], 'PG/PF': [], 'PG/C': [], '/SG': [], 'SG/': [], 'SG/SF': [], 'SG/PF': [], 'G/SF': [], 'G/PF': [], 'G/C': [], 'SF/': [], '/SF': [], 'PF/': [], '/PF': [], 'F/C': [], '/C': []}
        self.player_games = []
        self.num_games = None
        self.actuals = True if 'actual' in self.players_df else False

    def load_inputs(self, path):
        '''
        Returns loaded data into a dataframe
        '''
        try:
            data = pd.read_csv(path)
        except IOError:
            sys.exit('Invalid Filepath: {}'.format(path))
        return data

    def save(self, header, filled_lineups, show_proj = False):
        '''
        Saves filled lineups to CSV
        '''
        #Remove projections/actuals in order to upload to DK
        header_copy = copy.deepcopy(header)
        ouput_proj_path = self.output_path.split('.')[0] + '_proj.csv'
        if self.actuals:
            lineups_for_upload = [lineup[:-2] for lineup in filled_lineups]
            header_copy.extend(('PROJ', 'Actual'))
        else:
            lineups_for_upload = [lineup[:-1] for lineup in filled_lineups]
            header_copy.extend(('PROJ'))
        if not show_proj:
            with open(self.output_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(lineups_for_upload)
            print('Saved to: {}'.format(self.output_path))
        elif show_proj:
            with open(ouput_proj_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header_copy)
                writer.writerows(filled_lineups)
            print('Saved projection lineups to: {}'.format(ouput_proj_path))

    def create_indicators(self):
        '''
        Preprocesses data and classifies players into different indicators to be used by constraints.
        '''
        games = list(set(self.players_df['TeamAbbrev'].values))
        self.num_games = len(games)

        for pos in self.players_df.loc[:, 'Position']:
            for key in self.positions:
                self.positions[key].append(1 if key in pos else 0)

        for player_game in self.players_df.loc[:, 'TeamAbbrev']:
            self.player_games.append([1 if player_game == game else 0 for game in games])

    def generate(self, formula):
        '''
        Generates x lineups
        '''
        lineups = []
        for i in range (self.num_lineups):
            lineup = formula(lineups)
            if lineup:
                lineups.append(lineup)
            else:
                break
        return lineups