import re
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

        self.rules = rules
        self.terminals = set(list(filter(re.compile(TERMINAL_PATTERN).match, [str(r) for r in rules])) + [EPS])
        self.nonterminals = set(list(filter(re.compile(NONTERMINAL_PATTERN).match, [str(r) for r in rules])))
    
    def __str__(self):
        return '\n'.join([
                f'Terminals: {self.terminals}',
                f'Nonterminals: {self.nonterminals}',
                f'Rules:'
            ] + [f'{i+1}) {rule}' for i, rule in enumerate(self.rules)])


rules = ['S -> Aa', 'A -> bc', 'S -> ABCaA', 'B -> Ca', 'C -> _']
g = Grammar([Rule(r) for r in rules])
print(g)