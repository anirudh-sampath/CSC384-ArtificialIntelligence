# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import datetime
import random, util
import pdb

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #Generate an array of the manhattan distance to the ghosts
        neg_inf = -99999999
        pos_inf =  99999999
        n = 0
        current_closest_ghost_distance = pos_inf
        current_closest_ghost = []
        current_closest_ghost_index = 0
        current_closest_food_value = pos_inf #opportunity cost
        current_closest_food = []
        for ghost in successorGameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost)
            if distance < current_closest_ghost_distance:
                current_closest_ghost = ghost
                current_closest_ghost_distance = distance
                current_closest_ghost_index = n
            n += 1
        for food in newFood.asList():
            distance = util.manhattanDistance(newPos, food)
            if distance < current_closest_food_value:
                current_closest_food = food
                current_closest_food_value = distance

        score = -current_closest_food_value #opportunity cost
        if newPos in currentGameState.getFood().asList():
            score += current_closest_food_value
        if newScaredTimes[current_closest_ghost_index] ==0 and current_closest_ghost_distance < 2:
            score = neg_inf


        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        num_agents = gameState.getNumAgents()
        depth_bound = self.depth
        neg_inf = -99999999
        pos_inf =  99999999

        def miniMaxSearch(current_state, turn_number):
            turn = turn_number % num_agents #returns the person whose turn it is
            best_move = None
            if current_state.isWin() or current_state.isLose() or turn_number == depth_bound * num_agents:
                return self.evaluationFunction(current_state), best_move
            if turn ==0:
                value = neg_inf
            else:
                value = pos_inf
            for move in current_state.getLegalActions(turn):
                next_position = current_state.generateSuccessor(turn, move)
                next_value, next_move = miniMaxSearch(next_position, turn_number+1)
                if turn==0:
                    if value < next_value:
                        value, best_move = next_value, move
                else:
                    if value > next_value:
                        value, best_move = next_value, move
            return value, best_move
        value, move = miniMaxSearch(gameState, 0)
        return move

        #pdb.set_trace()
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        num_agents = gameState.getNumAgents()
        depth_bound = self.depth
        neg_inf = -99999999
        pos_inf =  99999999

        def alphaBetaPruning(current_state, turn_number, alpha, beta):
            turn = turn_number % num_agents #returns the person whose turn it is
            best_move = None
            if current_state.isWin() or current_state.isLose() or turn_number == depth_bound * num_agents:
                return self.evaluationFunction(current_state), best_move
            if turn ==0:
                value = neg_inf
            else:
                value = pos_inf
            for move in current_state.getLegalActions(turn):
                next_position = current_state.generateSuccessor(turn, move)
                next_value, next_move = alphaBetaPruning(next_position, turn_number+1, alpha, beta)
                if turn==0:
                    if value < next_value:
                        value, best_move = next_value, move
                    if value >= beta:
                        return value, best_move
                    alpha = max(alpha, value)
                else:
                    if value > next_value:
                        value, best_move = next_value, move
                    if value <= alpha:
                        return value, best_move
                    beta = min(beta, value)
            return value, best_move
        #print(datetime.datetime.now())
        value, move = alphaBetaPruning(gameState, 0, neg_inf, pos_inf)
        #print(datetime.datetime.now())
        return move

        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        num_agents = gameState.getNumAgents()
        depth_bound = self.depth
        neg_inf = -99999999
        pos_inf =  99999999

        def expectiMaxSearch(current_state, turn_number):
            turn = turn_number % num_agents #returns the person whose turn it is
            best_move = None
            if current_state.isWin() or current_state.isLose() or turn_number == depth_bound * num_agents:
                return self.evaluationFunction(current_state), best_move
            if turn ==0:
                value = neg_inf
            else:
                value = 0
            for move in current_state.getLegalActions(turn):
                number_of_options = len(current_state.getLegalActions(turn))
                next_position = current_state.generateSuccessor(turn, move)
                next_value, next_move = expectiMaxSearch(next_position, turn_number+1)
                if turn==0:
                    if value < next_value:
                        value, best_move = next_value, move
                        #print value
                else:
                    division = 1.0/number_of_options
                    value = value + division*next_value
                    #print value
            #print value
            return value, best_move
        #print(datetime.datetime.now())
        value, move = expectiMaxSearch(gameState, 0)
        #print(datetime.datetime.now())
        return move
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: This evaluation function makes use of the manhattan distances
      between the pacman and the food, pellets and ghosts to determine whether
      a proposed move is the most ideal at a given time. We calculate the minimum
      distance to the food and the pellet first. Since the food and the pellet are
      worth a lot of points we assign the food a priority of 4, and the pellet a priority
      of 8. We add to the score priority/min(distance to food or pellet). This would mean
      that the proposed move is moving pacman closer to food or a pellet, so we want to
      incentivize that movement. Similarly, we want to deincentivize movement towards
      ghosts during times when they are not scared, as we want to win the game. However, when
      the ghosts are scared, they are worth the most points on the board so we want to
      prioritize eating the scared ghosts. The priorities were chosen by trial and error, and
      were finalized when the autograder gave 100% score.
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    pellets = currentGameState.getCapsules()
    ghostPositions = currentGameState.getGhostPositions()
    ghostStates = currentGameState.getGhostStates()
    current_score = currentGameState.getScore()
    ghostScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    food_list = food.asList()
    food_distances = []
    pellet_distances = []
    ghost_distances = []

    for pellet in pellets:
        pellet_distances.append(util.manhattanDistance(position, pellet))

    for morsel in food:
        food_distances.append(util.manhattanDistance(position, morsel))


    if len(pellet_distances) != 0:
        current_score += 8/min(pellet_distances)

    if len(food_distances)!=0:
        current_score += 4/min(food_distances)

    for ghost in ghostPositions:
        ghost_distances.append(util.manhattanDistance(position,ghost))

    for i in range(len(ghost_distances)):
        x = 8 - ghost_distances[i]
        if ghostScaredTimes[i] >0:
            if x  > 0:
                current_score += x*5
        else:
            if x > 0:
                current_score -= x*5

    #pdb.set_trace()
    return current_score
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
