import re
from constants import RULE_PATTERN_TYPE_0, ARROW


ERROR_RULE_INCORRECT = 'Rule must be in form p -> q where p and q are words, and p has at least one nonterminal character.'


class Rule:
    def __init__(self, rule):
        if not re.match(RULE_PATTERN_TYPE_0, rule):
            raise ValueError(ERROR_RULE_INCORRECT)
        
        rule = re.sub('\\s*', '', rule)
        self.lhs, self.rhs = rule.split(ARROW)
    
    def __str__(self):
        return f'{self.lhs} {ARROW} {self.rhs}'

    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.__str__()}\')'