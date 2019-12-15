import pddlpy
import copy

class Problem():
    def __init__(self,domain_file,problem_file):
        print('Domain: ',domain_file)
        print('Problem: ',problem_file)
        domprob = pddlpy.DomainProblem(domain_file,problem_file)
        self.domain=Domain(domprob)
        #print(domprob.initialstate())
        #print(domprob.goals())
        #print(list( domprob.operators()))
        purchase=Action(list(domprob.ground_operator('purchase'))[0])
        purchase2=Action(list(domprob.ground_operator('purchase'))[1])
        '''print(purchase.pos_precondition)
        print(list( domprob.ground_operator('purchase') )[0].precondition_pos)
        #_pos / _neg , positive/negative predicate
        print(list( domprob.ground_operator('purchase') )[0].variable_list)
        print(list( domprob.ground_operator('purchase') )[0].operator_name)
        print(list( domprob.ground_operator('purchase') ))'''
        #effect_pos = set( [ a.ground( st ) for a in op.effect_pos ] )
        #gop.effect_neg
        print(purchase)
        init=set(Predicate(p.predicate) for p in domprob.initialstate())
        self.init_state=State(init,0,None,[])
        self.goals=init=set(Predicate(p.predicate) for p in domprob.goals())
        goal_state=State(self.goals,0,None,[])
        print('goal',goal_state)
        '''
        print('can apply',self.init_state.can_apply(purchase))
        print('applied',self.init_state.apply(purchase))
        print(self.init_state==goal_state)
        print(goal_state.contains(self.goals))'''

class Predicate():
    def __init__(self,p):
        self.predicate=tuple(p)
        self.p=p[0]
        if len(p)>1:
            self.arguments=p[1:-1]

    def __hash__(self):
        return hash(tuple(self.predicate))

    def __eq__(self,other):
        return self.predicate==other.predicate

    def __str__(self):
        return str(self.predicate)

class Action():
    #grounded action
    def __init__(self,action):
        self.operator=action.operator_name
        self.variables=action.variable_list
        self.pos_effects=set(Predicate(p) for p in action.effect_pos)
        self.neg_effects=set(Predicate(p) for p in action.effect_neg)
        self.pos_precondition=set(Predicate(p) for p in action.precondition_pos)
        #self.neg_precondition=set(Predicate(p) for p in action.precondition_neg)
    
    def __str__(self):
        return self.operator+str(self.variables)
    
    def __eq__(self,other):
        return (self.operator==other.operator) and (self.variables==other.variables)

class State():
    def __init__(self,predicates,cost,predecessor,path):
        self.predicates=frozenset(predicates)
        self.cost = cost
        self.predecessor=predecessor
        self.path=path

    def apply(self,action):
        predicates = self.predicates
        predicates |= set(action.pos_effects)
        predicates -= set(action.neg_effects)
        cost=self.cost+1
        path=self.path.copy()
        path.append(action)
        return State(predicates,cost,self,path)

    def can_apply(self,action):
        return all(p in self.predicates for p in action.pos_precondition)

    def contains(self,predicates):
        return all(p in self.predicates for p in predicates)

    def __str__(self):
        preds=""
        for p in self.predicates:
            preds+=str(p.predicate)+" "
        return 'predicates: '+preds

    def __eq__(self,other):
        return self.predicates==other.predicates

    def __hash__(self):
        return hash(tuple(self.predicates))

    def __lt__(self, other):
        return hash(self) < hash(other)

class Domain():
    def __init__(self,domprob):
        #action key format op_name+str(dict)
        self.actions={}
        #grounded actions
        print('Operators: ',domprob.operators())
        for op in domprob.operators():
            gop=list(domprob.ground_operator(op))
            for ga in gop:
                action=Action(ga)
                self.actions[str(action)]=action
        print(self.actions)

'''
class Problem():
'''

