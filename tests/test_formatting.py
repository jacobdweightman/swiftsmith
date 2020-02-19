import unittest
from swiftsmith.formatting import Block, EOL
from swiftsmith.grammar import Nonterminal
from swiftsmith.scope import Scope
from swiftsmith.semantics import SemanticParseTree

class TestFormatting(unittest.TestCase):
    def test_eol_tabs_by_scope_depth(self):
        # depth = 0
        scope = Scope()
        eol = EOL()
        eol.annotate(scope)
        self.assertEqual(eol.string(), "\n")

        # depth = 1
        scope = Scope(parent=scope)
        eol.annotate(scope)
        self.assertEqual(eol.string(), "\n\t")

        # depth = 2
        scope = Scope(parent=scope)
        eol.annotate(scope)
        self.assertEqual(eol.string(), "\n\t\t")
    
    def test_block_creates_child_scope(self):
        scope = Scope()
        block = Block()
        scope.push_deferred()
        block.annotate(scope)
        self.assertEqual(scope, scope.next_scope.parent)
        scope.pop_deferred()
        self.assertEqual(scope, scope.next_scope)

    def test_blocks_indent_in_tree(self):
        myeol = EOL()
        tree = SemanticParseTree(Nonterminal("foo"), [
            SemanticParseTree(Block()),
            SemanticParseTree(Nonterminal("foo"), [
                SemanticParseTree(myeol)
            ])
        ])
        tree.annotate(scope=Scope())
        self.assertEqual(tree.string(), "\n\t")
