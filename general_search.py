# format for search taken from project prompt, all functions developed by Tyson Loveless

from heapq import heappush, heappop # for priority queue structure
import puzzle

printing = True
diameter = 31
MAX_QUEUE_SIZE = 0      # keeps track of queue size
TOTAL_EXPANDED = 0      # keeps track of total nodes expanded


# updates maximum depth when puzzle size is changed
def setDiameter():
    global diameter
    if puzzle.size == 9:
        diameter = 31
    elif puzzle.size == 16:
        diameter = 80
    elif puzzle.size == 25:
        diameter = 208
    else:
        diameter = float('inf')


# helper function to print the current state of the puzzle
def printPuzzle(state):
    j = 0
    for i in range(0, puzzle.edge):
        print '      ',
        while j < puzzle.edge:
            if state[j + puzzle.edge * i] == 0:
                print '*',
            else:
                print state[j + puzzle.edge * i],
            print "\t",
            j += 1
        print ""
        j = 0


# expand does the work of expanding a node using the given operators for the problem
# the node is the current node, the operators are the legal moves on the current node
def expand(node, operators):
    children = []
    blankPosition = node.STATE.index(0)       # finds the index of the blank tile (0)
    for oper in operators:
        child = oper(node, blankPosition)     # gets child from position using operator, if illegal child = 0
        if child:                             # if operator was legal move
            children.append(child)            # append child node to list of nodes
    return children


# general form of search function based on project instructions
def search(problem, function):
    global diameter
    global TOTAL_EXPANDED
    global MAX_QUEUE_SIZE
    # in case you enter a custom puzzle that is already solved
    if problem.GOAL_TEST(problem.INITIAL_STATE.STATE):
        print "\n\nThe puzzle isn't mixed up yet!"
        return problem.INITIAL_STATE, TOTAL_EXPANDED, MAX_QUEUE_SIZE
    nodes = []   # our priority queue
    closed = {}  # positions that have been marked off as too costly to continue with
    heappush(nodes, [float('inf'), problem.INITIAL_STATE])    # root node pushed to pqueue
    while True:
        if not nodes: # nodes is empty, no soln found, we lose
            return 0, 0, 0
        # keep track of max queue size
        MAX_QUEUE_SIZE = max(MAX_QUEUE_SIZE, nodes.__len__())
        cost, node = heappop(nodes) # queue is popped with highest priority first (least cost)
        closed[tuple(node.STATE)] = True
        if printing:
            if function is 1:
                print "The best state to expand with a g(n) = %d and h(n) = %d is..." % (node.DEPTH, 0)
            elif function is 2:
                print "The best state to expand with a g(n) = %d and h(n) = %d is..." % (node.DEPTH, node.mis())
            else:
                print "The best state to expand with a g(n) = %d and h(n) = %d is..." % (node.DEPTH, node.man())
            printPuzzle(node.STATE)
            print '          Expanding this node...'
        else:
            if function is 2:
                node.mis()
            elif function is 3:
                node.man()
        # for every child to be expanded, we check if its state has already been visited
        #   if so, we do nothing, otherwise we push it to our priority queue based on our
        #   given queueing function heuristics
        for child in expand(node, problem.OPERATORS):
            if tuple(child.STATE) not in closed:
                if child.DEPTH <= diameter:
                    if function is 1:
                        heappush(nodes, [child.DEPTH, child])
                    elif function is 2:
                        heappush(nodes, [child.DEPTH + child.mis(), child])
                    else:
                        heappush(nodes, [child.DEPTH + child.man(), child])
                    TOTAL_EXPANDED += 1
            # success is checked once a node is expanded, to avoid expanding extra nodes
            if problem.GOAL_TEST(child.STATE):
                return child, TOTAL_EXPANDED, MAX_QUEUE_SIZE
