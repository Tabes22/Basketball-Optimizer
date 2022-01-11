import pulp
import draftkings
#from docplex.cp.model import CpoModel

def main():
    my_solver = pulp.CPLEX_CMD(msg = 0)
    optimizer = draftkings.DraftKings(num_lineups = 200, overlap = 5, solver=my_solver, players_path='example_inputs.csv', output_path='example_outputs.csv')
    optimizer.create_indicators()
    lineups = optimizer.generate(formula=optimizer.type_1)
    filled_lineups = optimizer.fill_lineups(lineups)
    optimizer.save(optimizer.header, filled_lineups)
    optimizer.save(optimizer.header, filled_lineups, show_proj=True)

main()