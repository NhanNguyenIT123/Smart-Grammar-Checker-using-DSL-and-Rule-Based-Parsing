# Generated from C:\GITHUB\Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing\backend\src\grammar_dsl\dsl\grammar\GrammarDSL.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarDSLParser import GrammarDSLParser
else:
    from GrammarDSLParser import GrammarDSLParser

# This class defines a complete generic visitor for a parse tree produced by GrammarDSLParser.

class GrammarDSLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GrammarDSLParser#command.
    def visitCommand(self, ctx:GrammarDSLParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#grammarCheckCmd.
    def visitGrammarCheckCmd(self, ctx:GrammarDSLParser.GrammarCheckCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#revisionPlanCmd.
    def visitRevisionPlanCmd(self, ctx:GrammarDSLParser.RevisionPlanCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#historyCmd.
    def visitHistoryCmd(self, ctx:GrammarDSLParser.HistoryCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#resetHistoryCmd.
    def visitResetHistoryCmd(self, ctx:GrammarDSLParser.ResetHistoryCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#spellCmd.
    def visitSpellCmd(self, ctx:GrammarDSLParser.SpellCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#verbCmd.
    def visitVerbCmd(self, ctx:GrammarDSLParser.VerbCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#synonymCmd.
    def visitSynonymCmd(self, ctx:GrammarDSLParser.SynonymCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#helpCmd.
    def visitHelpCmd(self, ctx:GrammarDSLParser.HelpCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#paragraph.
    def visitParagraph(self, ctx:GrammarDSLParser.ParagraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#lookupWord.
    def visitLookupWord(self, ctx:GrammarDSLParser.LookupWordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#paragraphToken.
    def visitParagraphToken(self, ctx:GrammarDSLParser.ParagraphTokenContext):
        return self.visitChildren(ctx)



del GrammarDSLParser