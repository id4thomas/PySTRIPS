from domain_tools import *
import heapq
from time import time

def heuristic(node):
    return 0

def planner(domain,init_node,goals):
    states_explored = 0
    closed = set()
    opened = [(heuristic(init_node), -init_node.cost, init_node)]
    heapq.heapify(opened)
    start = time()
    #a-star search
    while True:
        if len(opened) == 0:
            print('States Explored: %d'%(states_explored))
            return None

        #Get node with minimum cost value
        h, _, node = heapq.heappop(opened)
        states_explored += 1

        # Goal test
        if node.contains(goals):
            print('\nGoal Reached at level: %d'%(node.cost))
            for a in node.path:
                print(a)
            break

        #Expand if not closed
        if node not in closed:
            closed.add(node)
            #create successor nodes by applying possible actions
            successors = set(node.apply(action)
                             for action in domain.actions.values()
                             if node.can_apply(action))

            #get cost of each successor & add to opneed
            for successor in successors:
                if successor not in closed:
                    f = successor.cost + heuristic(successor)
                    heapq.heappush(opened, (f, -successor.cost, successor))


problem=Problem('./domain/diaper_domain.pddl','./problem/diaper_story.pddl')
domain=problem.domain
init_node=problem.init_state
goals=problem.goals

planner(domain,init_node,goals)
