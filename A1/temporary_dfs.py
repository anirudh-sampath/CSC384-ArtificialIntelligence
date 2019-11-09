"*** YOUR CODE HERE ***"
start_state = problem.getStartState()
open_list = util.Stack()
solution_set = []
visited_states = {}

current_state = None
open_list.push(problem.getStartState()) #get started with the stack
while not open_list.isEmpty():

    previous_state = current_state
    popped_state = open_list.pop()
    if popped_state != start_state:
        current_state = popped_state[0]
    else:
        current_state = popped_state

    visited_states[current_state] = previous_state #building a hash where you store the visited state and its parent

    visited_states.append(current_state)

    if current_state != start_state:
        solution_set.append(popped_state[1])
    if problem.isGoalState(current_state):
        #solution_set.append(popped_state[1])
        return solution_set
    else:
        for successor_state in problem.getSuccessors(current_state):
            if successor_state[0] not in visited_states:
                open_list.push(successor_state)

return solution_set
print "i have executed this with no syntax errors"
#util.raiseNotDefined()
