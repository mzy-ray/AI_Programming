import copy

ValueBoard = []
MoveX = (-1, -1, -1, 0, 0, 1, 1, 1)     #eight directions to check for a valid move
MoveY = (-1, 0, 1, -1, 1, -1, 0, 1)
global traverse_log
global both_pass                        #to check for terminal when both players made pass
global ini_player
global cutoff_depth


def InitValueBoard():
	ValueBoard.append([99, -8, 8, 6, 6, 8, -8, 99])
	ValueBoard.append([-8, -24, -4, -3, -3, -4, -24, -8])
	ValueBoard.append([8, -4, 7, 4, 4, 7, -4, 8])
	ValueBoard.append([6, -3, 4, 0, 0, 4, -3, 6])
	ValueBoard.append([6, -3, 4, 0, 0, 4, -3, 6])
	ValueBoard.append([8, -4, 7, 4, 4, 7, -4, 8])
	ValueBoard.append([-8, -24, -4, -3, -3, -4, -24, -8])
	ValueBoard.append([99, -8, 8, 6, 6, 8, -8, 99])


class State:
    def __init__(self, b, p, d):
        self.board = copy.deepcopy(b)
        self.player = p
        self.depth = d
	

class Action:
    def __init__(self, x, y):
        self.position = (x, y)
        self.flips = []


def ActionResult(state, action):
    next_state = State(state.board, state.player, state.depth)
    if action.position[0] == -2:                                 #when it is a pass action
        next_state.player = 1 - next_state.player
        next_state.depth += 1
    else:                                                       #when it is a valid action
        next_state.board[action.position[0]][action.position[1]] = state.player
        for (i, j) in action.flips:
            next_state.board[i][j] = state.player
        next_state.player = 1 - next_state.player
        next_state.depth += 1
    return next_state


def FindOptionalActions(state):
    actions = []
    actions_hash = {}
    for i in range(8):
        for j in range(8):
            if state.board[i][j] == -1:
                for k in range(8):
                    mx = MoveX[k]
                    my = MoveY[k]
                    x = i
                    y = j
                    if x + mx < 8 and x + mx >= 0 and y + my < 8 and y + my >= 0:
                        if state.board[x + mx][y + my] == 1 - state.player:
                            x += mx
                            y += my
                            while x + mx < 8 and x + mx >= 0 and y + my < 8 and y + my >= 0:
                                if state.board[x + mx][y + my] == state.player:
                                    action = Action(i, j)
                                    if mx != 0:
                                        m = (x - i) * mx + 1
                                    else:
                                        m = (y - j) * my + 1
                                    for t in range(1, m):
                                        action.flips.append((i + t * mx, j + t * my))
                                    if not actions_hash.has_key((i, j)):
                                        actions_hash[((i,j))] = action
                                        actions.append(action)
                                    else:
                                        actions_hash.get((i,j)).flips.extend(action.flips)
                                    break
                                elif state.board[x + mx][y + my] == -1:
                                    break
                                x += mx
                                y += my

    def cmp(a1, a2):                                        #sort the actions in positional order
        if a1.position > a2.position:
            return 1
        else:
            return -1

    actions = sorted(actions, cmp)
    return actions


def CutoffTest(state):
    global both_pass
    if state.depth == cutoff_depth or both_pass == 2:
        return True
    else:
        return False


def EVAL(state, ini_player):
    value = 0
    for i in range(8):
        for j in range(8):
            if state.board[i][j] == ini_player:
                value += ValueBoard[i][j]
            elif state.board[i][j] == 1 - ini_player:
                value -= ValueBoard[i][j]
    return value


def AlphaBetaSearch(state):
    action_start = Action(-1, -1)
    optimal_action = MaxValue(state, action_start, float("-inf"), float("inf"))
    return optimal_action


def MaxValue(state, last_action, alpha, beta):
    global traverse_log
    global both_pass
    global ini_player
    global cutoff_depth
    if last_action.position[0] == -1:
        node_position = "root"
    elif last_action.position[0] == -2:
        node_position = "pass"
    else:                                    #record to the last action to build the traverselog
        node_position = ""
        node_position += chr(last_action.position[1] + 97)
        node_position += "%d" % (last_action.position[0] + 1)
    value = float("-inf")
    optional_action = Action(-1, -1)

    if CutoffTest(state):
        value = EVAL(state, ini_player)
        traverse_log += "%s,%d,%.0f,%.0f,%.0f\n" % (node_position, state.depth, value, alpha, beta)
        return value

    traverse_log += "%s,%d,%.0f,%.0f,%.0f\n" % (node_position, state.depth, value, alpha, beta)
    actions = FindOptionalActions(state)
    if len(actions) == 0:                             #create a pass action when there is no valid action
        action_pass = Action(-2, -2)
        actions.append(action_pass)
        both_pass += 1
    else:
        both_pass = 0
    for action in actions:
        action_value = MinValue(ActionResult(state, action), action, alpha, beta)
        if action_value > value:
            value = action_value
            optional_action = action
        if value >= beta:
            traverse_log += "%s,%d,%.0f,%.0f,%.0f\n" % (node_position, state.depth, value, alpha, beta)
            return value
        alpha = max(alpha, value)
        traverse_log += "%s,%d,%.0f,%.0f,%.0f\n" % (node_position, state.depth, value, alpha, beta)
    if(node_position == "root"):              #return the optimal action rather than optimal value when it is the root
        return optional_action
    else:
        return value


def MinValue(state, last_action, alpha, beta):
    global traverse_log
    global both_pass
    global ini_player
    global cutoff_depth

    if last_action.position[0] == -2:
        node_position = "pass"
    else:
        node_position = ""
        node_position += chr(last_action.position[1] + 97)
        node_position += "%d" % (last_action.position[0] + 1)
    value = float("inf")

    if CutoffTest(state):
        value = EVAL(state, ini_player)
        traverse_log += "%s,%d,%.0f,%.0f,%.0f\n" % (node_position, state.depth, value, alpha, beta)
        return value

    traverse_log += "%s,%d,%.0f,%.0f,%.0f\n" % (node_position, state.depth, value, alpha, beta)
    actions = FindOptionalActions(state)
    if len(actions) == 0:
        action_pass = Action(-2, -2)
        actions.append(action_pass)
        both_pass += 1
    else:
        both_pass = 0
    for action in actions:
        value = min(value, MaxValue(ActionResult(state, action), action, alpha, beta))
        if value <= alpha:
            traverse_log += "%s,%d,%.0f,%.0f,%.0f\n" % (node_position, state.depth, value, alpha, beta)
            return value
        beta = min(beta, value)
        traverse_log += "%s,%d,%.0f,%.0f,%.0f\n" % (node_position, state.depth, value, alpha, beta)
    return value


if __name__=="__main__":
    global traverse_log
    global both_pass
    global ini_player
    global cutoff_depth
    InitValueBoard()
    traverse_log = "Node,Depth,Value,Alpha,Beta\n"
    both_pass = 0
    
    lines = []
    input_file = open("input.txt", 'r')
    while True:
        line = input_file.readline()
        lines.append(line.strip())
        if not line:
            break
    input_file.close()

    if lines[0][0]== "X":
        ini_player = 0
    else:
        ini_player = 1
    cutoff_depth = int(lines[1][0])
    start_board = []
    for i in range(8):
        start_board.append([])
    for i in range(2,10):
        for j in range(8):
            if lines[i][j] == "X":
                start_board[i - 2].append(0)
            elif lines[i][j] == "O":
                start_board[i - 2].append(1)
            else:
                start_board[i - 2].append(-1)

    start_state = State(start_board, ini_player, 0)
    optimal_action = AlphaBetaSearch(start_state)          #AlphaBetaSearch

    if optimal_action.position[0] > -1:                 #conduct the optimal action to get the next state
        start_board[optimal_action.position[0]][optimal_action.position[1]] = ini_player
        for (i, j) in optimal_action.flips:
            start_board[i][j] = ini_player
    output_text = ""
    for i in range(8):
        for j in range(8):
            if start_board[i][j] == 0:
                output_text += 'X'
            elif start_board[i][j] == 1:
                output_text += 'O'
            else:
                output_text += '*'
        output_text += '\n'
    traverse_log = traverse_log.replace("inf", "Infinity")
    traverse_log = traverse_log.rstrip('\n')
    output_text += traverse_log

    output_file = open('output.txt', 'w')
    output_file.write(output_text)
    output_file.close()

