#!/usr/bin/env python

import os
import sys
import yaml

import score

MATCH_ID = 'match-{0}'

def usage():
    print "Usage: score-match.py (league|knockout) MATCH_NUMBER"
    print "  Scores the match file at matches/MATCH_NUMBER.yaml"
    print "  Outputs scoring format suitable for piping at compd"


if len(sys.argv) is not 3:
    usage()
    exit(1)

style = sys.argv[1]
if style not in ['league', 'knockout']:
    usage()
    exit(2)

match_num = sys.argv[2]
match_file = "matches/{0}.yaml".format(match_num)

if not os.path.exists(match_file):
    print "Match file '{0}' doesn't exist. Have you created it?".format(match_file)
    usage()
    exit(3)

scores = yaml.load(open(match_file).read())

# Perform some horrible munging becuase 'scores' assumes teams named for letters
ids = ['a', 'b', 'c', 'd']

id_tla_mapping = dict(zip(ids, scores.keys()))
tla_id_mapping = dict(zip(scores.keys(), ids))
mapped_scores = {}
for tla, squares in scores.iteritems():
    id_ = tla_id_mapping[tla]
    mapped_scores[id_] = squares

scorer = None
try:
    scorer = score.StrangeGameScorer(mapped_scores)
except score.TooManyTokens as e:
    e.who = id_tla_mapping[e.who]
    raise

scorer.compute_cell_winners()

match_id = MATCH_ID.format(match_num)

for tla in scores.keys():
    id_ = tla_id_mapping[tla]
    this_score = scorer.compute_game_score(id_)
    print 'set-score {0} {1} {2}'.format(match_id, tla, this_score)

for tla, dsqs in scores.iteritems():
    if dsqs.get('dsq', False):
        print 'disqualify {0} {1}'.format(match_id, tla)

if style == 'league':
    print 'calc-league-points {0}'.format(match_id)
#else:
#    # Knockout
#    print 'update-knockout-after {0}'.format(match_id)
