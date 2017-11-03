import axelrod as axl


players = (axl.Cooperator(), axl.Alternator())
match = axl.Match(players, 5)
match.play()

print(match.result)
print(match.final_score())
print(match.winner())

print("-----------------------------")

competitors = [axl.Cooperator(), axl.Defector(), axl.TitForTat(), axl.Grudger()]
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

# plot = axl.Plot(res)
# p = plot.boxplot()
# p.show()
