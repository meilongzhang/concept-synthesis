import sys
sys.path.insert(0, '../libraries')

from LOTlib3.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib3.DataAndObjects import FunctionData, Obj
from LOTlib3.DefaultGrammars import DNF
from LOTlib3.Miscellaneous import q, random
from LOTlib3.Grammar import Grammar

def set_grammar():
    DEFAULT_FEATURE_WEIGHT = 5
    grammar = Grammar()
    grammar.add_rule('START', '', ['DISJ'], 1.0)
    grammar.add_rule('START', '', ['PRE-PREDICATE'], DEFAULT_FEATURE_WEIGHT)
    grammar.add_rule('START', 'True', None, DEFAULT_FEATURE_WEIGHT)
    grammar.add_rule('START', 'False', None, DEFAULT_FEATURE_WEIGHT)

    grammar.add_rule('DISJ', '',     ['CONJ'], 1.0)
    grammar.add_rule('DISJ', '',     ['PRE-PREDICATE'], DEFAULT_FEATURE_WEIGHT)
    grammar.add_rule('DISJ', '(%s or %s)',  ['PRE-PREDICATE', 'DISJ'], 1.0)

    grammar.add_rule('CONJ', '',     ['PRE-PREDICATE'], DEFAULT_FEATURE_WEIGHT)
    grammar.add_rule('CONJ', '(%s and %s)', ['PRE-PREDICATE', 'CONJ'], 1.0)

    # A pre-predicate is how we treat negation
    grammar.add_rule('PRE-PREDICATE', 'not(%s)', ['PREDICATE'], DEFAULT_FEATURE_WEIGHT)
    grammar.add_rule('PRE-PREDICATE', '',     ['PREDICATE'], DEFAULT_FEATURE_WEIGHT)

    grammar.add_rule('PREDICATE', "x['color']==%s", ['COLOR'], 1.0)
    grammar.add_rule('PREDICATE', "x['shape']==%s", ['SHAPE'], 1.0)

    # Some colors/shapes each (for this simple demo)
    # These are written in quotes so they can be evaled
    grammar.add_rule('COLOR', q('red'), None, 1.0)
    grammar.add_rule('COLOR', q('blue'), None, 1.0)
    grammar.add_rule('COLOR', q('green'), None, 1.0)

    grammar.add_rule('SHAPE', q('square'), None, 1.0)
    grammar.add_rule('SHAPE', q('circle'), None, 1.0)
    grammar.add_rule('SHAPE', q('triangle'), None, 1.0)
    return grammar

# generate 100000 rules of varying depths
def generate_rules():
    rules = {i: set() for i in range(15)}
    for _ in range(100000):
        rule = LOTHypothesis(grammar=grammar)
        depth = rule.value.depth() #rule.depth()
        rules[depth].add(rule)
    rules = {depth: list(depth_rules) for depth, depth_rules in rules.items()}
    return rules

# generate the set of possible stimuli
def get_all_stimuli():
    colors = ['red', 'blue', 'green']
    shapes = ['circle', 'square', 'triangle']
    all_stimuli = []

    for color in colors:
        for shape in shapes:
            all_stimuli.append({'shape':shape, 'color':color})

    return all_stimuli

# apply rule on list of stimuli
def apply_rule(rule, stimuli):
    results = []
    for stim in stimuli:
        results.append(rule(stimuli))
    return results

# 
def 