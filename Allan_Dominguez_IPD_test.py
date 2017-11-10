import axelrod as axl
import re
from Allan_Dominguez_IPD import Allan_Dominguez
import Allan_Dominguez_GA

me = Allan_Dominguez()

# To change memory depth and generate a new strategy (uncomment below)
num = input("What depth? ")
pwr = int(re.search(r'\d+', num).group())
me.classifier['memory_depth'] = pwr
me.classifier['bit_string'] = Allan_Dominguez_GA.strategy_gen(pwr)

players = (me, axl.APavlov2011())
match = axl.Match(players, 70)
match.play()

print(match.result)
print(match.final_score())
print(match.winner())

print("-----------------------------")

competitors = [me, axl.Defector(), axl.TitForTat(), axl.Random(), axl.APavlov2011(), axl.Cooperator()]
tournament = axl.Tournament(competitors, turns=3, repetitions=1)
res = tournament.play(keep_interactions=True)

print("\nInteractions between players")
matches = []
for player_index, interaction in sorted(res.interactions.items()):
    player1 = tournament.players[player_index[0]]
    player2 = tournament.players[player_index[1]]
    match = axl.Match((player1, player2), turns=3)
    match.result = interaction[0]
    matches.append(match)


print("\nPlayers ranked")
c = 1
for p in res.ranked_names:
    print("%d: %s" % (c, p))
    c += 1