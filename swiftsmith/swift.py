from swiftsmith.grammar.pcfg import Nonterminal, PProduction, PCFG
from swiftsmith.grammar.parsetree import ParseTree
from .scope import Scope
from .tokens import *


class SemanticParseTree(ParseTree):
    def string(self, scope=Scope()):
        """
        Get the string of terminals represented by this parse tree.
        """
        if self.isleaf():
            if isinstance(self.value, Token):
                return self.value.string(scope)
            return str(self.value)
        
        scope.push_deferred()
        children = [child.string(scope=scope.next_scope) for child in self.children]
        scope.pop_deferred()
        return "".join(children)


class SemanticPCFG(PCFG):
    """
    Represents a probabalistic context free grammar where parse trees have attached
    semantic information, in order to constrain the allowable strings.
    """
    ParseTree = SemanticParseTree

S = Nonterminal("S")
statement = Nonterminal("STATEMENT")
expression = Nonterminal("EXPRESSION")
declaration = Nonterminal("DECLARATION")
funcdeclaration = Nonterminal("FUNC_DECLARATION")
conditional = Nonterminal("CONDITIONAL")
block = Nonterminal("BLOCK")
returnstatement = Nonterminal("RETURN")

swift = SemanticPCFG(
    S,
    [
        # Allow variable declarations and functions at the top level of a program.
        PProduction(S, (declaration, S), 0.3),
        PProduction(S, (funcdeclaration, S), 0.3),
        PProduction(S, (funcdeclaration,), 0.4), # Guarantee at least one function

        PProduction(statement, (expression,), 0.1),
        PProduction(statement, (declaration,), 0.5),
        #PProduction(statement, (conditional,), 0.5),
        PProduction(statement, (returnstatement,), 0.),

        PProduction(expression, (expression, " + ", expression), 0.2),
        PProduction(expression, (expression, " * ", expression), 0.2),
        PProduction(expression, (Int(),), 0.3),
        PProduction(expression, (Variable(),), 0.3),

        PProduction(declaration, (EOL(), "let ", Variable(declaration=True), " = ", expression), 0.3),
        PProduction(declaration, (EOL(), "var ", Variable(declaration=True, mutable=True), " = ", expression), 0.7),

        #PProduction(conditional, ("if ", Variable(), " > ", expression, " {\n", statement, "}\n"), 1.0),

        PProduction(returnstatement, (EOL(), "return ", expression), 1.0),

        PProduction(funcdeclaration, (EOL(), EOL(), "func ", Function(), " {", block, EOL(), "}"), 1.0),

        PProduction(block, (Block(), statement, statement, returnstatement), 1.0),
    ]
)
