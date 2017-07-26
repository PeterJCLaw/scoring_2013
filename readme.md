# Student Robotics 2013 Scorer

This is a script to do scores for the [Student Robotics](http://srobo.org) 2013
game entitled 'A Strange Game'.
To use it, copy and edit `valid_scorecards/tokens.yml` file,
 and pass the name as the only command line argument.
The entries in the tokens files are the token counts
 (or the letter 'p' if the robot put a token on a pedestal)
 for the given robot.

Example:
~~~~ bash
python scores.py valid_scorecards/tokens.yml
~~~~

The scoring script that is expected to be used is `compd-score-match.py`,
which is executable, and outputs compd suitable commands.
Expected usage is to be passed either `league` or `knockout`, and a match
number. This then reads the yaml file for that match, which is stored at
`matches/MATCH_NUMBER.yaml`. The format for these is shown by the example
file `matches/example.yaml`.

Example:
~~~~ bash
./compd-score-match.py league 2
~~~~
