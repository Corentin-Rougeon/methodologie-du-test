def bowling_score(rolls):
    """Compute the total score for a player's game of bowling."""

    total = 0
    frame = 0
    count = len(rolls)
    newframe = True
    for index, roll in enumerate(rolls):
        if frame == 10:
            break
        if roll == 10:
            total += rolls[index + 1]
            total += rolls[index + 2]
            frame += 1
        elif not newframe:
            if rolls[index - 1] + roll == 10:
                total += rolls[index + 1]
            frame += 1
            newframe = True
        else:
            newframe = False
        total += roll

    return total

print(bowling_score([10,10,10,10,4,6,2,2]))