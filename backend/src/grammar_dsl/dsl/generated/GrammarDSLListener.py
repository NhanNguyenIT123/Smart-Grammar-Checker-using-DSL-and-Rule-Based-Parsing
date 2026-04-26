# Generated from C:\GITHUB\Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing\backend\src\grammar_dsl\dsl\grammar\GrammarDSL.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GrammarDSLParser import GrammarDSLParser
else:
    from GrammarDSLParser import GrammarDSLParser

# This class defines a complete listener for a parse tree produced by GrammarDSLParser.
class GrammarDSLListener(ParseTreeListener):

    # Enter a parse tree produced by GrammarDSLParser#command.
    def enterCommand(self, ctx:GrammarDSLParser.CommandContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#command.
    def exitCommand(self, ctx:GrammarDSLParser.CommandContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#grammarCheckCmd.
    def enterGrammarCheckCmd(self, ctx:GrammarDSLParser.GrammarCheckCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#grammarCheckCmd.
    def exitGrammarCheckCmd(self, ctx:GrammarDSLParser.GrammarCheckCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#showTokensCmd.
    def enterShowTokensCmd(self, ctx:GrammarDSLParser.ShowTokensCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#showTokensCmd.
    def exitShowTokensCmd(self, ctx:GrammarDSLParser.ShowTokensCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#revisionPlanCmd.
    def enterRevisionPlanCmd(self, ctx:GrammarDSLParser.RevisionPlanCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#revisionPlanCmd.
    def exitRevisionPlanCmd(self, ctx:GrammarDSLParser.RevisionPlanCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#historyCmd.
    def enterHistoryCmd(self, ctx:GrammarDSLParser.HistoryCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#historyCmd.
    def exitHistoryCmd(self, ctx:GrammarDSLParser.HistoryCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#resetHistoryCmd.
    def enterResetHistoryCmd(self, ctx:GrammarDSLParser.ResetHistoryCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#resetHistoryCmd.
    def exitResetHistoryCmd(self, ctx:GrammarDSLParser.ResetHistoryCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#spellCmd.
    def enterSpellCmd(self, ctx:GrammarDSLParser.SpellCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#spellCmd.
    def exitSpellCmd(self, ctx:GrammarDSLParser.SpellCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#verbCmd.
    def enterVerbCmd(self, ctx:GrammarDSLParser.VerbCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#verbCmd.
    def exitVerbCmd(self, ctx:GrammarDSLParser.VerbCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#synonymCmd.
    def enterSynonymCmd(self, ctx:GrammarDSLParser.SynonymCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#synonymCmd.
    def exitSynonymCmd(self, ctx:GrammarDSLParser.SynonymCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#helpCmd.
    def enterHelpCmd(self, ctx:GrammarDSLParser.HelpCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#helpCmd.
    def exitHelpCmd(self, ctx:GrammarDSLParser.HelpCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#paragraph.
    def enterParagraph(self, ctx:GrammarDSLParser.ParagraphContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#paragraph.
    def exitParagraph(self, ctx:GrammarDSLParser.ParagraphContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#lookupWord.
    def enterLookupWord(self, ctx:GrammarDSLParser.LookupWordContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#lookupWord.
    def exitLookupWord(self, ctx:GrammarDSLParser.LookupWordContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#paragraphToken.
    def enterParagraphToken(self, ctx:GrammarDSLParser.ParagraphTokenContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#paragraphToken.
    def exitParagraphToken(self, ctx:GrammarDSLParser.ParagraphTokenContext):
        pass



del GrammarDSLParser