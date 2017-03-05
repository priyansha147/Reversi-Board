import copy

# Create Matrix consisting of Weights
weights = [[], [99, -8, 8, 6, 6, 8, -8, 99], [-8, -24, -4, -3, -3, -4, -24, -8], [8, -4, 7, 4, 4, 7, -4, 8], [6, -3, 4, 0, 0, 4, -3, 6], [6, -3, 4, 0, 0, 4, -3, 6], [8, -4, 7, 4, 4, 7, -4, 8], [-8, -24, -4, -3, -3, -4, -24, -8], [99, -8, 8, 6, 6, 8, -8, 99]]
fo = open("input.txt")
player = fo.read(1)
depth = fo.read(2)
state = fo.read()
fo.close()
stateMatrix = map(list, state.splitlines())  # Get Board State in the form of Matrix
maxDepth = int(depth)   # Convert depth into integer
conv = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']    # Create a list for mapping col indices from 0-7 to a-h
outputLogs = []     # Create a list to store final log values


# Creates a copy of board state
def getfreshboard(board):
    freshboard = copy.deepcopy(board)
    return freshboard


# Calculates evaluation function
def calcvalue(p, board):
    if p == 'X':
        value = 0
        for x in range(1,9):
            for y in range(0,8):
               if board[x][y]=='X':
                   value = value - weights[x][y]
               if board[x][y]=='O':
                   value = value + weights[x][y]

    else:
        value = 0
        for x in range(1, 9):
            for y in range(0, 8):
                if board[x][y] == 'O':
                    value = value - weights[x][y]
                if board[x][y] == 'X':
                    value = value + weights[x][y]

    return value


# Creates a dictionary with key as valid moves and corresponding tile flips as value list
def createdict(a, b, c, d):
    d[a, b] = c
    return d


# Checks if location is on the board
def isonboard(m, n):
    if m >= 1 and m <= 8 and n >= 0 and n <= 7:
        return 1
    else:
        return 0


# Returns all the possible valid moves and the corresponding tile flips in the form of dictionary for a board state
def isvalidmove(p, board, i, j, flip):
    d = flip
    for xd, yd in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:   # Checks in all 8 directions
        cnt = 0
        xin, yin = i, j
        if isonboard(xin + xd, yin + yd) == 1:
            if board[xin+xd][yin+yd] == '*':
                while isonboard(xin, yin) == 1 and board[xin][yin] != p:
                    if board[xin][yin] == '*':
                        cnt = 0
                        break
                    else:
                        cnt += 1            # Stores the number of tile flips for a possible valid move
                    xin -= xd
                    yin -= yd
        else:
            continue
        l = []       # List stores all tiles to be flipped for a valid move
        if isonboard(xin, yin) == 0 or board[xin][yin] == '*':
            continue

        elif cnt > 0 and board[xin][yin] == p:
            for x in range(1, cnt+1):
                a, b = (i+xd)-x*xd, (j+yd)-x*yd           # Logic to store tile flips
                l.append([a, b])
                d = createdict(i + xd, j + yd, l, d)
    return d


# Main Function
def recurdfs(player, currd, parent, curr, currstate, alpha, beta, level):
    if level == 1:
        val = -1000
    else:
        val = 1000

    if maxDepth == currd:
        val = calcvalue(player, currstate)
        #print 7, curr, currd, val, alpha, beta
        outputLogs.append(curr+','+str(currd)+','+str(val)+','+str(alpha)+','+str(beta))
        return (val, currstate)

    flip = {}   # This is a dictionary for storing valid moves as key and corresponding tile flips as value list

    # Level == 1 specifies maximizing player
    if level == 1:
        vtemp = -1000
        stemp = getfreshboard(currstate)
        if player == 'X':
            for x in range(1, 9):
                for y in range(0, 8):
                    if currstate[x][y] == 'O':
                        isvalidmove(player, currstate, x, y, flip)

            if not (parent == 'pass' and bool(flip) == 0):
                #print 500,curr, currd, val, alpha, beta
                outputLogs.append(curr + ',' + str(currd) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta))

            if bool(flip) == 0:    # Checks for pass condition
                if parent == 'pass':    # Checks for double pass condition
                    val = calcvalue('O', currstate)
                    #print 1000, curr, currd, val, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta))
                    return (val, currstate)
                nxt = 'pass'
                (val, newstate) = recurdfs('O', currd+1, curr,nxt, currstate, alpha, beta, 0)
                # alpha beta pruning starts
                #print 1001, vtemp, val
                if vtemp < val:
                    vtemp = val
                if vtemp >= beta:
                    #print 1002, curr, currd, vtemp, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))
                    return (vtemp, stemp)
                if alpha < vtemp:
                    alpha = vtemp
                #print 1003, curr,currd,vtemp,alpha,beta
                outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))

            else:
                # Iterates for all the valid moves in order of priority
                for k, v in sorted(flip.iteritems()):   # Play moves
                    savedstate = getfreshboard(currstate)
                    savedstate[k[0]][k[1]] = 'X'
                    nxt = conv[k[1]] + str(k[0])
                    flat = [val for sublist in v for val in sublist]

                    for i in range(0, len(flat)):
                        if i%2 == 0:
                            savedstate[flat[i]][flat[i+1]] = 'X'

                    (val, newstate) = recurdfs('O', currd+1, curr, nxt, savedstate, alpha, beta, 0)
                    # alpha beta pruning starts
                    #print 1500, curr, currd, vtemp,val, alpha, beta
                    if vtemp < val:
                        vtemp = val
                    if vtemp >= beta:
                        #print 1501,curr, currd, vtemp, alpha, beta
                        outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))
                        return (vtemp, stemp)
                    if alpha < vtemp:
                        alpha = vtemp
                        stemp = getfreshboard(savedstate)
                    #print 1502,curr, currd, vtemp, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))


        else:
            for x in range(1, 9):
                for y in range(0, 8):
                    if currstate[x][y] == 'X':
                        isvalidmove(player, currstate, x, y, flip)

            if not (parent == 'pass' and bool(flip) == 0):
                #print 1800,curr, currd, val, alpha, beta
                outputLogs.append(curr + ',' + str(currd) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta))

            if bool(flip) == 0:     # Checks for pass condition
                if parent == 'pass':       # Checks for double pass condition
                    val = calcvalue('O', currstate)
                    #print 2000, curr, currd, val, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta))
                    return (val, currstate)
                nxt = 'pass'
                (val, newstate) = recurdfs('X', currd+1, curr,nxt, currstate, alpha, beta, 0)
                # alpha beta pruning starts
                #print 2001, vtemp, val
                if vtemp < val:
                    vtemp = val
                if vtemp >= beta:
                    #print 2002, curr, currd, vtemp, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))
                    return (vtemp, stemp)
                if alpha < vtemp:
                    alpha = vtemp
                #print 2003, curr, currd, vtemp, alpha, beta
                outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))

            else:
                # Iterates for all the valid moves in order of priority
                for k, v in sorted(flip.iteritems()):   #Play moves
                    savedstate = getfreshboard(currstate)
                    savedstate[k[0]][k[1]] = 'O'
                    nxt = conv[k[1]] + str(k[0])
                    flat = [val for sublist in v for val in sublist]

                    for i in range(0, len(flat)):
                        if i%2 == 0:
                            savedstate[flat[i]][flat[i+1]] = 'O'

                    (val, newstate) = recurdfs('X', currd+1, curr, nxt, savedstate, alpha, beta, 0)
                    #print 2501, curr, currd, vtemp, alpha, beta
                    # alpha beta pruning starts
                    if vtemp < val:
                        vtemp = val
                    if vtemp >= beta:
                        #print 2502,curr, currd, vtemp, alpha, beta
                        outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))
                        return (vtemp, stemp)
                    if alpha < vtemp:
                        alpha = vtemp
                        stemp = getfreshboard(savedstate)
                    #print 2503,curr, currd, vtemp, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))


    # Level == 0 specifies minimizing player
    elif level == 0:
        vtemp = 1000
        stemp = getfreshboard(currstate)
        if player == 'X':
            for x in range(1, 9):
                for y in range(0, 8):
                    if currstate[x][y] == 'O':
                        isvalidmove(player, currstate, x, y, flip)

            if not (parent == 'pass' and bool(flip) == 0):
                #print 2801,curr, currd, val, alpha, beta
                outputLogs.append(curr + ',' + str(currd) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta))

            if bool(flip) == 0:         # Checks for pass condition
                if parent == 'pass':    # Checks for double pass condition
                    val = calcvalue('O', currstate)
                    #print 3000, curr, currd, val, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta))
                    return (val, currstate)
                nxt = 'pass'
                (val, newstate) = recurdfs('O', currd+1, curr, nxt, currstate, alpha, beta, 1)
                # alpha beta pruning starts
                #print 3001, vtemp, val
                if vtemp > val:
                    vtemp = val
                if vtemp <= alpha:
                    #print 3002, curr, currd, vtemp, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))
                    return (vtemp, stemp)
                if beta > vtemp:
                    beta = vtemp
                #print 3003, curr, currd, vtemp, alpha, beta
                outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))


            else:
                # Iterates for all the valid moves in order of priority
                for k, v in sorted(flip.iteritems()):  # Play moves
                    savedstate = getfreshboard(currstate)
                    savedstate[k[0]][k[1]] = 'X'
                    nxt = conv[k[1]] + str(k[0])
                    flat = [val for sublist in v for val in sublist]

                    for i in range(0, len(flat)):
                        if i % 2 == 0:
                            savedstate[flat[i]][flat[i + 1]] = 'X'

                    (val, newstate) = recurdfs('O', currd+1, curr, nxt, savedstate, alpha, beta, 1)
                    # alpha beta pruning starts
                    #print 3501, curr, currd, vtemp,val, alpha, beta
                    if vtemp > val:
                        vtemp = val
                    if vtemp <= alpha:
                        #print 3502,curr, currd, vtemp, alpha, beta
                        outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))
                        return (vtemp, stemp)
                    if beta > vtemp:
                        beta = vtemp
                        stemp = getfreshboard(savedstate)
                    #print 3503,curr, currd, vtemp, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))


        else:
            for x in range(1, 9):
                for y in range(0, 8):
                    if currstate[x][y] == 'X':
                        isvalidmove(player, currstate, x, y, flip)

            if not (parent == 'pass' and bool(flip) == 0):
                #print 3800,curr, currd, val, alpha, beta
                outputLogs.append(curr + ',' + str(currd) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta))

            if bool(flip) == 0:     # Checks for pass condition
                if parent == 'pass':    # Checks for double pass condition
                    val = calcvalue('O', currstate)
                    #print 4000, curr, currd, val, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(val) + ',' + str(alpha) + ',' + str(beta))
                    return (val, currstate)
                nxt = 'pass'
                (val, newstate) = recurdfs('X', currd+1, curr, nxt, currstate, alpha, beta, 1)
                # alpha beta pruning starts
                #print 4001, vtemp, val
                if vtemp > val:
                    vtemp = val
                if vtemp <= alpha:
                    #print 4002, curr, currd, vtemp, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))
                    return (vtemp, stemp)
                if beta > vtemp:
                    beta = vtemp
                #print 4003,curr, currd, vtemp, alpha, beta
                outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))

            else:
                # Iterates for all the valid moves in order of priority
                for k, v in sorted(flip.iteritems()):  # Play moves
                    savedstate = getfreshboard(currstate)
                    savedstate[k[0]][k[1]] = 'O'
                    nxt = conv[k[1]] + str(k[0])
                    flat = [val for sublist in v for val in sublist]

                    for i in range(0, len(flat)):
                        if i % 2 == 0:
                            savedstate[flat[i]][flat[i + 1]] = 'O'

                    (val, newstate) = recurdfs('X', currd+1, curr, nxt, savedstate, alpha, beta, 1)
                    #print 4501, curr, currd, vtemp, val,alpha, beta
                    # alpha beta pruning starts
                    if vtemp > val:
                        vtemp = val
                    if vtemp <= alpha:
                        #print 4502,curr, currd, vtemp, alpha, beta
                        outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))
                        return (vtemp, stemp)
                    if beta > vtemp:
                        beta = vtemp
                        stemp = getfreshboard(savedstate)
                    #print 4503,curr, currd, vtemp, alpha, beta
                    outputLogs.append(curr + ',' + str(currd) + ',' + str(vtemp) + ',' + str(alpha) + ',' + str(beta))


    return (vtemp, stemp)

# First call to dfs passing root as current node and n specifies that the parent of root is null
(value, outputboard) = recurdfs(player, 0,'n','root', stateMatrix, -1000, 1000, 1)
fo = open("output.txt", "a")
for row in outputboard:
    if not("".join(map(str, row)) == ""):       # Convert board to a string and write in file
        fo.write("".join(map(str, row)))
        fo.write("\n")
fo.write("Node,Depth,Value,Alpha,Beta\n")

for word in outputLogs:
    fo.write(word.replace("1000", "Infinity"))
    fo.write("\n")



