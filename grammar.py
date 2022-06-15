import re
from operator import add
from functools import reduce
from typing import Callable, List
from constants import AXIOM, EPS, RULE_PATTERN_TYPE_1, RULE_PATTERN_TYPE_2, RULE_PATTERN_TYPE_3L, RULE_PATTERN_TYPE_3R, TERMINAL_PATTERN, NONTERMINAL_PATTERN
from rule import Rule


ERROR_NO_RULES = 'Rules not specified'
ERROR_NO_AXIOM = f'Grammar must contain at least one rule starting with axiom {AXIOM}'

sort_nt = lambda nt: 0 if nt == AXIOM else ord(nt)


class Grammar:
    """
        Type-0 (recursively enumerable) grammar.
        Does not put any constraints on its rules.
    """
    check_rules: Callable = lambda _: True
    error_rules: str = ""

    def __init__(self, rules: List[Rule]):
        if not rules:
            raise ValueError(ERROR_NO_RULES)
        
        if not any(AXIOM in r.lhs for r in rules):
            raise ValueError(ERROR_NO_AXIOM)

        if not self.__class__.check_rules(rules):
            raise ValueError(self.error_rules)

        self.rules = sorted(rules, key=lambda r: sort_nt(r[0]))
        self.terminals = set(list(reduce(add, [re.findall(TERMINAL_PATTERN, str(r)) for r in rules])) + [EPS])
        self.nonterminals = set(list(reduce(add, [re.findall(NONTERMINAL_PATTERN, str(r)) for r in rules])))
    
    def _check_rules(self, rules):
        if not self.check_rules(rules):
            raise ValueError(self.error_rules)

    def delete_rule(self, rule):
        terminals = set(re.findall(TERMINAL_PATTERN, str(rule)))
        nonterminals = set(re.findall(NONTERMINAL_PATTERN, str(rule)))

        for terminal in [t for t in terminals if t in self.terminals]:
            self.terminals.remove(terminal)
        
        for nonterminal in [nt for nt in nonterminals if nt in self.nonterminals]:
            self.nonterminals.remove(nonterminal)
        
        self.rules.remove(rule)

        print(f"Removed rule {rule}, terminals {', '.join(terminals)} and nonterminals {', '.join(nonterminals)}")

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
    check_rules = lambda rules: any(re.compile(RULE_PATTERN_TYPE_1).match(str(r)) for r in rules)
    error_rules = "Rules must be of form a -> b where a is not longer than b, a is a word containing at least one nonterminal, and b is a non-empty word."


class ContextFreeGrammar(Grammar):
    """
        Type-2 (context-free) grammar.
        Rules must be of form A -> b where A is a nonterminal, and b is a word.
    """
    check_rules = lambda rules: any(re.compile(RULE_PATTERN_TYPE_2).match(str(r)) for r in rules)
    error_rules = "Rules must be of form A -> b where A is a nonterminal, and b is a word."
    
    def remove_unreachable(self):
        reachable, reachable_prev = {AXIOM}, None
        i = 0

        print("Scanning through reachable nonterminals...")
        while reachable != reachable_prev:
            print(f"R{i} = {sorted(reachable, key=sort_nt)}")
            i += 1

            reachable_prev = reachable.copy()
            reachable |= {
                nt
                for nonterminal in reachable
                for rule in self.rules
                if nonterminal in rule.lhs
                for nt in set(re.findall(NONTERMINAL_PATTERN, rule.rhs))
            }
        
        unreachable = self.nonterminals - reachable
        print(f"Found unreachable nonterminals: {', '.join(unreachable)}")

        for rule in [r for r in self.rules if r.lhs in unreachable]:
            self.delete_rule(rule)


class LeftLinearGrammar(Grammar):
    """
        Type-3 (regular) left-linear grammar.
        Rules must be of form A -> By or A -> y where A, B are nonterminals, and y is a word.
    """
    check_rules = lambda rules: any(re.compile(RULE_PATTERN_TYPE_3L).match(str(r)) for r in rules)
    error_rules = "Rules must be of form A -> By or A -> y where A, B are nonterminals, and y is a word."


class RightLinearGrammar(Grammar):
    """
        Type-3 (regular) right-linear grammar.
        Rules must be of form A -> yB or A -> y where A, B are nonterminals, and y is a word.
    """
    check_rules = lambda rules: any(re.compile(RULE_PATTERN_TYPE_3R).match(str(r)) for r in rules)
    error_rules = "Rules must be of form A -> yB or A -> y where A, B are nonterminals, and y is a word."


