import re
from operator import add
from functools import reduce
from constants import AXIOM, EPS, TERMINAL_PATTERN, NONTERMINAL_PATTERN
from rule import Rule


ERROR_NO_RULES = 'Rules not specified'
ERROR_NO_AXIOM = f'Grammar must contain at least one rule starting with axiom {AXIOM}'
ERROR_RULES_TYPE_0 = 'Rules must be of form aAb -> ayb, where A is a nonterminal, a and b are words, and y is a non-empty word.'
ERROR_RULES_TYPE_1 = 'Rules must be of form '

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

        self.rules = sorted(rules, key=lambda r: 0 if str(r)[0]==AXIOM else ord(str(r)[0]))
        self.terminals = set(list(reduce(add, [re.findall(TERMINAL_PATTERN, str(r)) for r in rules])) + [EPS])
        self.nonterminals = set(list(reduce(add, [re.findall(NONTERMINAL_PATTERN, str(r)) for r in rules])))
    
    def __str__(self):
        return '\n'.join([
                f'Terminals: {sorted(self.terminals)}',
                f'Nonterminals: {sorted(self.nonterminals)}',
                f'Rules:'
        ] + [f'{i+1}) {rule}' for i, rule in enumerate(self.rules)])



class ContextSensitiveGrammar(Grammar):
    """
        Type-1 (context-sensitive) grammar.
        Rules must be of form aAb -> ayb, where A is a nonterminal, a and b are words,
        and y is a non-empty word.
    """

    def __init__(self, rules):
        super().__init__(rules)

        if 
