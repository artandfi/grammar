from rule import Rule
from grammar import ContextFreeGrammar
from unittest import TestCase


class TestGrammars(TestCase):
    def test_remove_unreachable1(self):
        rules = [
            Rule("S->a"), Rule("S->A"), Rule("A->AB"), Rule("B->b"), Rule("C->c"), Rule("E->Ff")]
        new_rules = rules[:-2]
        
        grammar = ContextFreeGrammar(rules)
        grammar.remove_unreachable()

        self.assertEqual(grammar.rules, new_rules) # Last two rules should be unreachable
    
    def test_remove_unreachable2(self):
        rules = [Rule("S->BbB"), Rule("S->AaA"), Rule("B->ABC"), Rule("C->Dc"), Rule("D->_")]
        
        grammar = ContextFreeGrammar(rules)
        grammar.remove_unreachable()

        self.assertEqual(grammar.rules, rules) # All rules should be reachable
