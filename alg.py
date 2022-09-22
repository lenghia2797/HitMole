SHOW_LOG = False

def errorType(type):
    if type==1: return 'Rule 1 Violation: Have a color repeat more than twice.'
    if type==2: return 'Rule 2 Violation: The amount of black is different from the amount of white.'
    if type==3: return 'Rule 3 Violation: Rows or columns are not unique.'
    return 'Ok'

def find_empty(state):
    size = len(state)
    for row in range(size):
        for col in range(size):
            if state[row][col] == 0: 
                return row, col
    return None, None

def appendTolist(trace_state, states):
    p1 = []
    for i in range(len(states)):
        p1 += states[i]
    trace_state.append(p1)

def backtrackingDFS(trace_state, trace_pos_list, state, n):
    if SHOW_LOG: print('\nCell ',n,':')
    row, col = find_empty(state)
    if row == None or col == None:
        return state
    res = state
    # Try choose white
    state[row][col] = 1
    if SHOW_LOG: print('Try: p[',row,',',col,'] = ', 1)
    
    # Check error
    haveE = haveError(state,row,col)
    if haveE == 0:
        # Trace for game demo
        trace_pos_list.append((row,col))
        appendTolist(trace_state, state)
        # Choose next cell
        res = backtrackingDFS(trace_state, trace_pos_list, state, n+1)
        if isOk(res): return res
    else:
        if SHOW_LOG: print('Error: ', errorType(haveE))
        
    # Try choose black
    state[row][col] = -1
    if SHOW_LOG: print('Try: p[', row,',', col, '] = ', -1)
    
    # Check error
    haveE = haveError(state,row,col)
    if haveE == 0:
        # Trace for game demo
        trace_pos_list.append((row,col))
        appendTolist(trace_state, state)
        # Choose next cell
        res = backtrackingDFS(trace_state, trace_pos_list,state, n+1)
        if isOk(res): return res
    else:
        if SHOW_LOG: print('Error: ', errorType(haveE))
        
    # Return color
    state[row][col] = 0
    return state

def checkHeuristic(state, row, col):
    size = len(state)
    total = 0
    for r in range(size):
        total += state[r][col]
    for c in range(size):
        total += state[row][c]
    if total > 0: return 1
    elif total < 0: return -1
    else: return 0

def backtrackingHeuristic(trace_state, trace_pos_list, state, n):
    if SHOW_LOG: print('\nCell ',n,':')
    row, col = find_empty(state)
    if row == None or col == None:
        return state
    res = state
    state[row][col] = 1
    haveE = haveError(state,row,col)
    if haveE == 0:
        state[row][col] = -1
        haveE = haveError(state,row,col)
        if haveE == 0:
            state[row][col] = 0
            if checkHeuristic(state,row,col) <= 0: 
                # Try choose white color before black color
                if SHOW_LOG: print('Try: p[',row,',',col,'] = ', 1)
                state[row][col] = 1
                trace_pos_list.append((row,col))
                appendTolist(trace_state, state)
                res = backtrackingHeuristic(trace_state, trace_pos_list, state, n+1)
                if isOk(res): return res
                
                if SHOW_LOG: print('Try: p[',row,',',col,'] = ', -1)
                state[row][col] = -1
                trace_pos_list.append((row,col))
                appendTolist(trace_state, state)
                res = backtrackingHeuristic(trace_state, trace_pos_list, state, n+1)
                if isOk(res): return res
            else: 
                # Try choose black color before white color
                if SHOW_LOG: print('Try: p[',row,',',col,'] = ', -1)
                state[row][col] = -1
                trace_pos_list.append((row,col))
                appendTolist(trace_state, state)
                res = backtrackingHeuristic(trace_state, trace_pos_list, state, n+1)
                if isOk(res): return res
                
                if SHOW_LOG: print('Try: p[',row,',',col,'] = ', 1)
                state[row][col] = 1
                trace_pos_list.append((row,col))
                appendTolist(trace_state, state)
                res = backtrackingHeuristic(trace_state, trace_pos_list, state, n+1)
                if isOk(res): return res
        else: 
            if SHOW_LOG: print('Try: p[',row,',',col,'] = ', 1)
            state[row][col] = 1
            trace_pos_list.append((row,col))
            appendTolist(trace_state, state)
            res = backtrackingHeuristic(trace_state, trace_pos_list, state, n+1)
            if isOk(res): return res
    else: 
        if SHOW_LOG: print('Try: p[',row,',',col,'] = ', -1)
        state[row][col] = -1
        haveE = haveError(state,row,col)
        if haveE == 0:
            trace_pos_list.append((row,col))
            appendTolist(trace_state, state)
            res = backtrackingHeuristic(trace_state, trace_pos_list,state, n+1)
            if isOk(res): return res
        
    state[row][col] = 0
    return state

def isOk(state):
    size = len(state)
    for row in range(size):
        for col in range(size):
            if haveError(state,row,col) != 0:
                return False
    return True

def print_puzzle(state):
    size = len(state)
    for row in range(size):
        for col in range(size):
            print(state[row][col], " ", end = " ")
        print("\n")
    print("--------------------")

def haveError(state, row, col):
    if haveAdjError(state, row, col):
        return 1
    if haveCountError(state, row, col):
        return 2
    if haveUniqueError(state, row, col):
        return 3
    return 0

def haveAdjError(state,row,col):
    size = len(state)
    if row>1:
        if state[row-2][col] == state[row][col] and state[row-1][col] == state[row][col]:
            return True
    if col>1:
        if state[row][col-2] == state[row][col] and state[row][col-1] == state[row][col]:
            return True
    
    if row<size-1: 
        if state[row-1][col] == state[row][col] and state[row+1][col] == state[row][col]:
            return True
    
    if col<size-1: 
        if state[row][col-1] == state[row][col] and state[row][col+1] == state[row][col]:
            return True
        
    if row<size-2: 
        if state[row+1][col] == state[row][col] and state[row+2][col] == state[row][col]:
            return True
    
    if col<size-2: 
        if state[row][col+1] == state[row][col] and state[row][col+2] == state[row][col]:
            return True
             
    return False

def haveCountError(state, row, col):
    size = len(state)
    count = 0
    for c in range(col+1):
        count += state[row][c]
        if count>size/2 or count<-size/2: return True
        
    if count != 0 and col == size-1: return True
    
    count = 0
    for r in range(row+1):
        count += state[r][col]
        if count>size/2 or count<-size/2: return True
        
    if count != 0 and row == size-1: return True
    
    return False

def haveUniqueError(state, row, col):
    size = len(state)
    if col == size-1 and row>0 : 
        for crow in range(row):
            for row in range(crow+1,row+1):
                isU = True
                for col in range(size):
                    if state[crow][col] != state[row][col]: 
                        isU = False
                        break
                if isU:
                    return True
    if row == size-1 and col>0 : 
        for ccol in range(col):
            for col in range(ccol+1,col+1):
                isU = True
                for row in range(size):
                    if state[row][ccol] != state[row][col]: 
                        isU = False
                        break
                if isU:
                    return True
    return False