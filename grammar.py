import re
from operator import add
from functools import reduce
from constants import AXIOM, EPS, RULE_PATTERN_TYPE_1, RULE_PATTERN_TYPE_2, RULE_PATTERN_TYPE_3L, RULE_PATTERN_TYPE_3R, TERMINAL_PATTERN, NONTERMINAL_PATTERN
from rule import Rule


ERROR_NO_RULES = 'Rules not specified'
ERROR_NO_AXIOM = f'Grammar must contain at least one rule starting with axiom {AXIOM}'
ERROR_RULES_TYPE_1 = 'Rules must be of form a -> b where a is not longer than b, a is a word containing at least one nonterminal, and b is a non-empty word.'
ERROR_RULES_TYPE_2 = 'Rules must be of form A -> b where A is a nonterminal, and b is a word.'
ERROR_RULES_TYPE_3L = 'Rules must be of form A -> By or A -> y where A, B are nonterminals, and y is a word.'
ERROR_RULES_TYPE_3R = 'Rules must be of form A -> yB or A -> y where A, B are nonterminals, and y is a word.'

class Grammar:
    """
        Type-0 (recursively enumerable) grammar class.
        Does not put any constraints on its rules.
    """
    def __init__(self, rules):
        if not rules:
            raise ValueError(ERROR_NO_RULES)
        
        if not any(AXIOM in r.lhs for r in rules):
            raise ValueError(ERROR_NO_AXIOM)

        self._check_rules(rules)

        self.rules = sorted(rules, key=lambda r: 0 if str(r)[0]==AXIOM else ord(str(r)[0]))
        self.terminals = set(list(reduce(add, [re.findall(TERMINAL_PATTERN, str(r)) for r in rules])) + [EPS])
        self.nonterminals = set(list(reduce(add, [re.findall(NONTERMINAL_PATTERN, str(r)) for r in rules])))
    
    def _check_rules(self, rules):
        pass

    def __str__(self):
        return '\n'.join([
                f'Terminals: {sorted(self.terminals)}',
                f'Nonterminals: {sorted(self.nonterminals)}',
                f'Rules:'
        ] + [f'{i+1}) {rule}' for i, rule in enumerate(self.rules)])


class NoncontractingGrammar(Grammar):
    """
        Type-1 (noncontracting) grammar.
        Rules must be of form a -> b where a is not longer than b,
        a is a word containing at least one nonterminal,
        and b is a non-empty word.
    """

    def _check_rules(self, rules):
        if not any(re.compile(RULE_PATTERN_TYPE_1).match(r) for r in rules):
            raise ValueError(ERROR_RULES_TYPE_1)


class ContextFreeGrammar(Grammar):
    """
        Type-2 (context-free) grammar.
        Rules must be of form A -> b where A is a nonterminal, and b is a word.
    """

    def _check_rules(self, rules):
        if not any(re.compile(RULE_PATTERN_TYPE_2).match(r) for r in rules):
            raise ValueError(ERROR_RULES_TYPE_2)


class LeftLinearGrammar(Grammar):
    """
        Type-3 (regular) left-linear grammar.
        Rules must be of form A -> By or A -> y where A, B are nonterminals, and y is a word.
    """

    def _check_rules(self, rules):
        if not any(re.compile(RULE_PATTERN_TYPE_3L).match(r) for r in rules):
            raise ValueError(ERROR_RULES_TYPE_3L)


class RightLinearGrammar(Grammar):
    """
        Type-3 (regular) right-linear grammar.
        Rules must be of form A -> yB or A -> y where A, B are nonterminals, and y is a word.
    """

    def _check_rules(self, rules):
        if not any(re.compile(RULE_PATTERN_TYPE_3R).match(r) for r in rules):
            raise ValueError(ERROR_RULES_TYPE_3R)
