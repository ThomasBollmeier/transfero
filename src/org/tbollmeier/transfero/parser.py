from .scanner import Scanner
from .translators import Rule

class Parser(object):
    
    def __init__(self, grammar):
        self._grammar = grammar
        self._root = Rule(self._grammar.get_root_rule())
        self._scanner = Scanner(self._grammar)
        
    def parse(self, source):
        token_stream = self._scanner.find_tokens(source)
        nodes = self._root.translate(self._grammar, token_stream)
        return nodes and nodes[0] or None
