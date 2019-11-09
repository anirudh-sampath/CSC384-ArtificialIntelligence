# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
#Author: Anirudh Sampath (2019 Fall CSC384)
import util
import pdb
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem): #need to implement logic for path checking
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    start_state = problem.getStartState()
    OPEN_LIST = util.Stack()
    solution_set = []
    if problem.isGoalState(start_state):
        return solution_set
    OPEN_LIST.push(([start_state], solution_set))
    while not OPEN_LIST.isEmpty():
        popper = OPEN_LIST.pop()
        terminal_state = popper[0][-1]
        current_path = popper[0]
        solution_set = popper[1]
        if problem.isGoalState(terminal_state):
            return solution_set
        for successor in problem.getSuccessors(terminal_state):
            if successor[0] not in current_path:
                path = copy.deepcopy(current_path)
                sol_set = copy.deepcopy(solution_set)
                path.append(successor[0])
                sol_set.append(successor[1])
                OPEN_LIST.push((path, sol_set))
    return []

def breadthFirstSearch(problem): #implementation breaks under eightpuzzle
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    OPEN_LIST = util.Queue()
    solution_set = []
    visited_nodes = []
    pushed_paths = []
    if problem.isGoalState(start_state):
        return solution_set
    OPEN_LIST.push(([start_state], solution_set))
    while not OPEN_LIST.isEmpty():
        popper = OPEN_LIST.pop()
        terminal_state = popper[0][-1]
        current_path = popper[0]
        solution_set = popper[1]
        visited_nodes.append(terminal_state)
        if problem.isGoalState(terminal_state):
            return solution_set
        for successor in problem.getSuccessors(terminal_state):
            if successor[0] not in visited_nodes:
                path = copy.deepcopy(current_path)
                sol_set = copy.deepcopy(solution_set)
                path.append(successor[0])
                sol_set.append(successor[1])
                OPEN_LIST.push((path, sol_set))
                visited_nodes.append(successor[0])
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    OPEN_LIST = util.PriorityQueue()
    solution_set = []
    visited_nodes = []
    cost_dict = {}
    if problem.isGoalState(start_state):
        return solution_set
    current_path = [start_state]
    OPEN_LIST.push(([start_state], solution_set), 0)
    while not OPEN_LIST.isEmpty():
        popper = OPEN_LIST.pop()
        terminal_state = popper[0][-1]
        current_path = popper[0]
        solution_set = popper[1]
        visited_nodes.append(terminal_state)
        if terminal_state == start_state:
            cost = 0
        else:
            cost = cost_dict[', '.join(map(str, current_path))]
        if problem.isGoalState(terminal_state):
            return solution_set
        for successor in problem.getSuccessors(terminal_state):
            path = copy.deepcopy(current_path)
            sol_set = copy.deepcopy(solution_set)
            path.append(successor[0])
            sol_set.append(successor[1])
            cost_new_path = cost + successor[2]
            if successor[0] not in visited_nodes:
                insert_dict = ', '.join(map(str, path))
                cost_dict[insert_dict] = cost_new_path
                OPEN_LIST.push((path, sol_set),cost_new_path)
                visited_nodes.append(successor[0])
                if problem.isGoalState(successor[0]):
                    current_goal_path = insert_dict
            if problem.isGoalState(successor[0]) and successor[0] in visited_nodes:
                if cost_new_path < cost_dict[current_goal_path]:
                    insert_dict = ', '.join(map(str, path))
                    cost_dict[insert_dict] = cost_new_path
                    OPEN_LIST.push((path, sol_set),cost_new_path)
                    visited_nodes.append(successor[0])
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    OPEN_LIST = util.PriorityQueue()
    solution_set = []
    visited_nodes = []
    cost_dict = {}
    if problem.isGoalState(start_state):
        return solution_set
    current_path = [start_state]
    OPEN_LIST.push(([start_state], solution_set), 0)
    while not OPEN_LIST.isEmpty():
        popper = OPEN_LIST.pop()
        terminal_state = popper[0][-1]
        current_path = popper[0]
        solution_set = popper[1]
        visited_nodes.append(terminal_state)
        if terminal_state == start_state:
            cost = 0
        else:
            cost = cost_dict[', '.join(map(str, current_path))]
        if problem.isGoalState(terminal_state):
            return solution_set
        for successor in problem.getSuccessors(terminal_state):
            path = copy.deepcopy(current_path)
            sol_set = copy.deepcopy(solution_set)
            path.append(successor[0])
            sol_set.append(successor[1])
            cost_new_path_heuristic = cost + successor[2] + heuristic(successor[0], problem)
            cost_new_path = cost + successor[2]
            if successor[0] not in visited_nodes:
                insert_dict = ', '.join(map(str, path))
                cost_dict[insert_dict] = cost_new_path
                OPEN_LIST.update((path, sol_set),cost_new_path_heuristic)
                visited_nodes.append(successor[0])
                if problem.isGoalState(successor[0]):
                    current_goal_path = insert_dict
            if problem.isGoalState(successor[0]) and successor[0] in visited_nodes:
                if cost_new_path < cost_dict[current_goal_path]:
                    insert_dict = ', '.join(map(str, path))
                    cost_dict[insert_dict] = cost_new_path
                    OPEN_LIST.push((path, sol_set),cost_new_path)
                    visited_nodes.append(successor[0])
    return []
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
