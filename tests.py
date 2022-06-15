from rule import Rule
from grammar import ContextFreeGrammar
from unittest import TestCase


class TestGrammars(TestCase):
    def test_remove_unreachable1(self):
        rules = [
            Rule("S->a"), Rule("S->A"), Rule("A->AB"), Rule("B->b"), Rule("C->c"), Rule("E->Ff")]
        new_rules = rules[:-2]
        new_terminals = {'_', 'a', 'b'}
        new_nonterminals = {'S', 'A', 'B'}
        
        grammar = ContextFreeGrammar(rules)
        grammar.remove_unreachable()

        self.assertEqual(grammar.rules, new_rules) # Last two rules should be unreachable
        self.assertEqual(grammar.terminals, new_terminals)
        self.assertEqual(grammar.nonterminals, new_nonterminals)
    
    def test_remove_unreachable2(self):
        rules = [Rule("S->BbB"), Rule("S->AaA"), Rule("B->ABC"), Rule("C->Dc"), Rule("D->_")]

        grammar = ContextFreeGrammar(rules)
        new_terminals, new_nonterminals = grammar.terminals, grammar.nonterminals
        grammar.remove_unreachable()

        self.assertEqual(grammar.rules, rules) # All rules should be reachable
        self.assertEqual(grammar.terminals, new_terminals)
        self.assertEqual(grammar.nonterminals, new_nonterminals)
