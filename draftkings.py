import pulp
import optimizer
from docplex.cp.model import CpoModel

class DraftKings(optimizer.Optimizer):
    '''
    DK settings
    '''
    def __init__(self, num_lineups, overlap, solver, players_path, output_path):
        super().__init__(num_lineups, overlap, solver, players_path, output_path)
        self.salary_cap = 50000
        self.header = ['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F', 'UTIL']

    def type_1(self, lineups):
        '''
        Sets up the pulp problem. Adds all constraints
        '''
        #problem
        prob = pulp.LpProblem('NBA', pulp.LpMaximize)

        #players are the variables
        players_lineup = [pulp.LpVariable('player_{}'.format(i+1), cat='Binary') for i in range(self.num_players)]

        #max players
        prob += (pulp.lpSum(players_lineup[i] for i in range(self.num_players)) == 8)

        #positional constraints
        prob += (1 <= pulp.lpSum(self.positions['PG'][i]*players_lineup[i] for i in range(self.num_players)))
        prob += (1 <= pulp.lpSum(self.positions['SG'][i]*players_lineup[i] for i in range(self.num_players)))
        prob += (3 <= pulp.lpSum(self.positions['G'][i]*players_lineup[i] for i in range(self.num_players)))
        prob += (1 <= pulp.lpSum(self.positions['SF'][i]*players_lineup[i] for i in range(self.num_players)))
        prob += (1 <= pulp.lpSum(self.positions['PF'][i]*players_lineup[i] for i in range(self.num_players)))
        prob += (3 <= pulp.lpSum(self.positions['F'][i]*players_lineup[i] for i in range(self.num_players)))
        prob += (1 <= pulp.lpSum(self.positions['C'][i]*players_lineup[i] for i in range(self.num_players)))
        
        prob += ((3 + pulp.lpSum(self.positions['G/SF'][i]*players_lineup[i] for i in range(self.num_players))) <= (pulp.lpSum(self.positions['G'][i]*players_lineup[i] for i in range(self.num_players)) + pulp.lpSum(self.positions['SF'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['G/SF'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += ((3 + pulp.lpSum(self.positions['G/PF'][i]*players_lineup[i] for i in range(self.num_players))) <= (pulp.lpSum(self.positions['G'][i]*players_lineup[i] for i in range(self.num_players)) + pulp.lpSum(self.positions['PF'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['G/PF'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += ((3 + pulp.lpSum(self.positions['SG/PF'][i]*players_lineup[i] for i in range(self.num_players))) <= (pulp.lpSum(self.positions['F'][i]*players_lineup[i] for i in range(self.num_players)) + pulp.lpSum(self.positions['SG'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['SG/PF'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += ((3 + pulp.lpSum(self.positions['SG/SF'][i]*players_lineup[i] for i in range(self.num_players))) <= (pulp.lpSum(self.positions['F'][i]*players_lineup[i] for i in range(self.num_players)) + pulp.lpSum(self.positions['SG'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['SG/SF'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += ((3 + pulp.lpSum(self.positions['PG/SF'][i]*players_lineup[i] for i in range(self.num_players))) <= (pulp.lpSum(self.positions['F'][i]*players_lineup[i] for i in range(self.num_players)) + pulp.lpSum(self.positions['PG'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['PG/SF'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += ((3 + pulp.lpSum(self.positions['PG/PF'][i]*players_lineup[i] for i in range(self.num_players))) <= (pulp.lpSum(self.positions['F'][i]*players_lineup[i] for i in range(self.num_players)) + pulp.lpSum(self.positions['PG'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['PG/PF'][i]*players_lineup[i] for i in range(self.num_players))))
        
        prob += (3 >= (pulp.lpSum(self.positions['PG'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['PG/'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += (3 >= (pulp.lpSum(self.positions['SG'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['SG/'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['/SG'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += (3 >= (pulp.lpSum(self.positions['SF'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['SF/'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['/SF'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += (3 >= (pulp.lpSum(self.positions['PF'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['PF/'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['/PF'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += (2 >= (pulp.lpSum(self.positions['C'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['/C'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += (4 >= (pulp.lpSum(self.positions['G'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['G/SF'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['G/PF'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['G/C'][i]*players_lineup[i] for i in range(self.num_players))))
        prob += (4 >= (pulp.lpSum(self.positions['F'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['G/SF'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['G/PF'][i]*players_lineup[i] for i in range(self.num_players)) - pulp.lpSum(self.positions['F/C'][i]*players_lineup[i] for i in range(self.num_players))))

        #salary
        prob += ((pulp.lpSum(self.players_df.loc[i, 'Salary']*players_lineup[i] for i in range(self.num_players))) <= self.salary_cap)

        #at least 2 games
        used_game = [pulp.LpVariable('u{}'.format(i+1), cat='Binary') for i in range(self.num_games)]
        for i in range(self.num_games):
          prob += (used_game[i] <= pulp.lpSum(self.player_games[k][i]*players_lineup[k] for k in range(self.num_players)))
          prob += (pulp.lpSum(self.player_games[k][i]*players_lineup[k] for k in range(self.num_players)) <= 7*used_game[i])
        prob += (pulp.lpSum(used_game[i] for i in range(self.num_games)) >= 2)

        #variance - lineups can't overlap however many players the overlap is set to
        for i in range(len(lineups)):
            prob += ((pulp.lpSum(lineups[i][k]*players_lineup[k] for k in range(self.num_players))) <= self.overlap)

        #objective
        prob += pulp.lpSum((pulp.lpSum(self.players_df.loc[i, 'AvgPointsPerGame']*players_lineup[i] for i in range(self.num_players))))

        #solve
        status = prob.solve(self.solver)

        if status != pulp.LpStatusOptimal:
            print('Only {} feasible lineups produced'.format(len(lineups)), '\n')
            return None

        #formatting for later use
        lineup_copy = []
        for i in range(self.num_players):
            if players_lineup[i].varValue >= 0.9 and players_lineup[i].varValue <= 1.1:
                lineup_copy.append(1)
            else:
                lineup_copy.append(0)
        return lineup_copy
            

    def fill_lineups(self, lineups):
        '''
        Uses the binary data and matches names to create a dataframe
        '''
        filled_lineups = []
        for lineup in lineups:
          pgs = []
          sgs = []
          sfs = []
          pfs = []
          centers = []
          guards = []
          point_forwards = []
          power_points = []
          point_centers = []
          shooting_forwards = []
          shooting_powers = []
          shooting_centers = []
          forwards = []
          small_centers = []
          power_centers = []
          a_lineup = ['', '', '', '', '', '', '', '']
          players_lineup = lineup[:self.num_players]
          total_proj = 0
          if self.actuals:
            total_actual = 0
          players_in_lineup = []
          for num, player in enumerate(players_lineup):
            if player > 0.9 and player < 1.1:
              players_in_lineup.append(self.players_df.loc[num, 'Name'])
              if self.positions['PG'][num] == 1:
                if self.positions['SG'][num] == 1:
                  guards.append(self.players_df.loc[num, 'Name'])
                elif self.positions['SF'][num] == 1:
                    point_forwards.append(self.players_df.loc[num, 'Name'])
                elif self.positions['PF'][num] == 1:
                    power_points.append(self.players_df.loc[num, 'Name'])
                elif self.positions['C'][num] == 1:
                    point_centers.append(self.players_df.loc[num, 'Name'])
                else:
                    pgs.append(self.players_df.loc[num, 'Name'])
              elif self.positions['SG'][num] == 1:
                if self.positions['SF'][num] == 1:
                    shooting_forwards.append(self.players_df.loc[num, 'Name'])
                elif self.positions['PF'][num] == 1:
                    shooting_powers.append(self.players_df.loc[num, 'Name'])
                elif self.positions['C'][num] == 1:
                    shooting_centers.append(self.players_df.loc[num, 'Name'])
                else:
                    sgs.append(self.players_df.loc[num, 'Name'])
              elif self.positions['SF'][num] == 1:
                if self.positions['PF'][num] == 1:
                    forwards.append(self.players_df.loc[num, 'Name'])
                elif self.positions['C'][num] == 1:
                    small_centers.append(self.players_df.loc[num, 'Name'])
                else:
                    sfs.append(self.players_df.loc[num, 'Name'])
              elif self.positions['PF'][num] == 1:
                if self.positions['C'][num] == 1:
                    power_centers.append(self.players_df.loc[num, 'Name'])
                else:
                    pfs.append(self.players_df.loc[num, 'Name'])
              elif self.positions['C'][num] == 1:
                centers.append(self.players_df.loc[num, 'Name'])
              total_proj += self.players_df.loc[num, 'AvgPointsPerGame']
              if self.actuals:
                total_actual += self.players_df.loc[num, 'actual']
          add_players(pgs, a_lineup, 0, 5, 7, 7, [])
          add_players(sgs, a_lineup, 1, 5, 7, 7, [])
          add_players(sfs, a_lineup, 2, 6, 7, 7, [])
          add_players(pfs, a_lineup, 3, 6, 7, 7, [])
          add_players(centers, a_lineup, 4, 7, 7, 7, [])
          add_players2(guards, a_lineup, 0, 1, 5, 7, point_forwards, power_points, point_centers)
          add_players2(forwards, a_lineup, 2, 3, 6, 7, point_forwards, shooting_forwards, small_centers)
          add_players(point_forwards, a_lineup, 0, 2, 5, 6, small_centers)
          add_players(power_points, a_lineup, 0, 3, 5, 6, power_centers)
          add_players(point_centers, a_lineup, 0, 4, 5, 7, small_centers, power_centers)
          add_players(shooting_forwards, a_lineup, 1, 2, 5, 6, small_centers)
          add_players(shooting_powers, a_lineup, 1, 3, 5, 6, power_centers)
          add_players(shooting_centers, a_lineup, 1, 4, 5, 7, small_centers, power_centers)
          add_players(small_centers, a_lineup, 2, 4, 6, 7, power_centers)
          add_players(power_centers, a_lineup, 3, 4, 6, 7, [])
          a_lineup.append(round(total_proj, 2))
          if self.actuals:
            a_lineup.append(round(total_actual, 2))
          filled_lineups.append(a_lineup)       
        return filled_lineups

def add_players(il, ol, ind1, ind2, ind3, ind4, order2, order=[]):
  for i in range(len(il)):
    if ol[ind1] == '':
      ol[ind1] = il[i]
    elif ol[ind2] == '':
      if len(order) > 0 or len(order2) > 0:
        if ol[ind3] == '':
          ol[ind3] = il[i]
        elif ol[ind4] == '':
          ol[ind4] = il[i]
        elif ol[7] == '':
          ol[7] = il[i]
      else:
        ol[ind2] = il[i]
    elif ol[ind3] == '':
      ol[ind3] = il[i]
    elif ol[ind4] == '':
      ol[ind4] = il[i]
    elif ol[7] == '':
      ol[7] = il[i]

def add_players2(il, ol, ind1, ind2, ind3, ind4, order3, order2, order=[]):
  for i in range(len(il)):
    if ol[ind1] == '':
      if len(order) > 0 or len(order2) > 0 or len(order3) > 0:
        if ol[ind2] == '':
          ol[ind2] = il[i]
        elif ol[ind3] == '':
          ol[ind3] = il[i]
        elif ol[ind4] == '':
          ol[ind4] = il[i]
        elif ol[7] == '':
          ol[7] = il[i]
      else:
        ol[ind1] = il[i]
    elif ol[ind2] == '':
      ol[ind2] = il[i]
    elif ol[ind3] == '':
      ol[ind3] = il[i]
    elif ol[ind4] == '':
      ol[ind4] = il[i]
    elif ol[7] == '':
      ol[7] = il[i]