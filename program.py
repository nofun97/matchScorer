# score for newly-started game or set
ZERO_SCORE = "0-0"

# score for tied set (about to go to tiebreaker game)
TIED_SET = [6, 6]

def comp101_match(points, server, maxlen,
                  tiebreaker=comp101_tiebreaker,
                  game=comp101_game, 
                  set_score=comp101_set):
    """calculate the score of a full tennis match, made up of `points` and from
    the perspective of `server`; return score and winner (if there is one), or
    `False` if invalid match (made up of too many points)"""

    def won_set(score):
        """determine whether the set has been won"""
        return score in ('6', '7')

    # store `server` from original call
    starting_server = server
    
    # set representation of set score
    sets = []
    
    # point score representation of current (incomplete) game
    final_game = ""

    # iterate over the points until the set ends
    while points:
        
        # get set score, winner and remainder points for next set
        sscore, winner, remainder = set_score(points, server)
        
        # add game score for set only if at least one game won
        if sscore != ZERO_SCORE:
            sets.append(sscore)
            
        # CASE 1: there are no surplus points and there is a winner
        if winner in (0, 1) and not remainder:
            break
            
        else:
            # CASE 2.1: surplus points but there is a set winner
            if winner in (0, 1):
                
                # keep iterating over the surplus
                points = remainder
            
            # CASE 2.2: incomplete set
            else:
                    
                # iterate back through points game by game to work out
                # how far through the set we got, keeping track of the game
                # score as we go
                part_set_score = [0, 0]
                remainder = points
                while remainder:
                    if part_set_score == TIED_SET:
                        game_score, winner, remainder = \
                            tiebreaker(remainder, server)
                    else:
                        game_score, winner, remainder = game(remainder, server)
                        if winner in (0, 1):
                            part_set_score[winner] += 1
                        
                # if last game of current (incomplete) set is incomplete,
                # save point score, to append to set/game score
                if winner not in (0, 1) and game_score != ZERO_SCORE:
                    final_game = game_score
                break

    # invalid match if too many sets in total
    if len(sets) > maxlen:
        return False

    # iterate through sets, determining who won each, to calculate tally
    # of won sets for each player
    sets_won = [0, 0]
    for s in sets:
        server_score, receiver_score = s.split('-')
        if server_score > receiver_score and won_set(server_score):
            sets_won[0] += 1
        elif won_set(receiver_score):
            sets_won[1] += 1
            
    # calculate maximum number of sets a given player can win
    max_sets_won = (maxlen // 2) + 1
    
    # make sure neither player has won more than max number of sets given match
    # length
    for sets_won_each in sets_won:
        if sets_won_each > max_sets_won or (sets_won_each == max_sets_won and 
                                            final_game):
            return False

    # valid match, so join up bits of scores and return
    if final_game:
        return " ".join(sets + [final_game])
    else:
        return " ".join(sets)
