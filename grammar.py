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
        print(f"R{i} = {sorted(reachable, key=sort_nt)}")
        while reachable != reachable_prev:
            reachable_prev = reachable.copy()
            reachable |= {
                nt
                for nonterminal in reachable
                for rule in self.rules
                if nonterminal in rule.lhs
                for nt in set(re.findall(NONTERMINAL_PATTERN, rule.rhs))
            }

            i += 1
            print(f"R{i} = {sorted(reachable, key=sort_nt)}")

        unreachable_terminals = self.terminals - ({
            t
            for rule in self.rules
            for t in set(re.findall(TERMINAL_PATTERN, rule.rhs))
            if rule.lhs in reachable
        } | {EPS})
        unreachable_nonterminals = self.nonterminals - reachable
        unreachable_rules = [r for r in self.rules if r.lhs in unreachable_nonterminals]
        
        print(f"Found unreachable nonterminals: {', '.join(unreachable_nonterminals)}")

        for rule in unreachable_rules:
            self.rules.remove(rule)
            print(f"Removed rule {rule}")
        
        for terminal in unreachable_terminals:
            self.terminals.remove(terminal)

        for nonterminal in unreachable_nonterminals:
            self.nonterminals.remove(nonterminal)

        print(f"Removed terminals {', '.join(unreachable_terminals)}")
        print(f"Removed nonterminals {', '.join(unreachable_nonterminals)}")
    
    def remove_unproductive(self):
        productive = {
            rule.lhs
            for rule in self.rules
            if all(c in self.terminals for c in rule.rhs)
        }
        productive_prev = None
        i = 0
        
        print("Scanning through productive nonterminals...")
        print(f"Pr{i} = {sorted(productive, key=sort_nt)}")
        while productive != productive_prev:
            productive_prev = productive.copy()
            productive |= {
                rule.lhs
                for rule in self.rules
                if all(c in productive | self.terminals for c in rule.rhs)
            }
            
            i += 1
            print(f"Pr{i} = {sorted(productive, key=sort_nt)}")
        
        unproductive_terminals = self.terminals - ({
            t
            for rule in self.rules
            for t in set(re.findall(TERMINAL_PATTERN, rule.rhs))
            if rule.lhs in productive
        } | {EPS})
        unproductive_nonterminals = self.nonterminals - productive
        unproductive_rules = [r for r in self.rules for nt in unproductive_nonterminals if nt in r.lhs or nt in r.rhs]
        print(f"Found unproductive nonterminals: {', '.join(unproductive_nonterminals)}")

        for rule in unproductive_rules:
            self.rules.remove(rule)
            print(f"Removed rule {rule}")
        
        for terminal in unproductive_terminals:
            self.terminals.remove(terminal)
        
        for nonterminal in unproductive_nonterminals:
            self.nonterminals.remove(nonterminal)
        
        
        print(f"Removed terminals {', '.join(unproductive_terminals)}")
        print(f"Removed nonterminals {', '.join(unproductive_nonterminals)}")


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
