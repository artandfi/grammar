import re
from operator import add
from functools import reduce
from constants import AXIOM, EPS, TERMINAL_PATTERN, NONTERMINAL_PATTERN
from rule import Rule


ERROR_NO_AXIOM = f'Grammar must contain at least one rule starting with axiom {AXIOM}'
ERROR_NO_RULES = f'Rules not specified'


class Grammar:
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


rules = ['S -> Aa', 'A -> bc', 'S -> ABCaA', 'B -> Ca', 'C -> _']
g = Grammar([Rule(r) for r in rules])
print(g)