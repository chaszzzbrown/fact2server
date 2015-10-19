'''
in manage shell:

from gameplay.models import *
foo = GameInfo.objects.filter(game_category='tuning', is_completed=True).values('player_info__username', 'game_settings__name').annotate(cnt=Count('pk'))
with open('tuners.json', 'w') as f:
    json.dump(list(foo), f)

'''


import json

def aggy():
    res = {}
    for f in foo:
        tots = res.get(f['player_info__username'], {'easy1':0, 'easy2':0, 'medium1':0, 'medium2':0, 'hard1':0, 'hard2':0})
        tots[f['game_settings__name']] += f['cnt']
        res[f['player_info__username']] = tots
    return res

def outOne(k, row):
    fmt = '{}\t'*6 + '{}'
    print fmt.format(k, row['easy1'], row['easy2'], row['medium1'],
                     row['medium2'], row['hard1'], row['hard2'])

with open('tuners.json') as f:
    foo = json.load(f)

bar = aggy()
