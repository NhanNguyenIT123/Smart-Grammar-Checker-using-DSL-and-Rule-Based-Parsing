# Generated from C:\GITHUB\Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing\backend\src\grammar_dsl\dsl\grammar\GrammarDSL.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\35")
        buf.write("`\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16\t")
        buf.write("\16\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\5\28\n\2\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\5\3\5")
        buf.write("\3\5\3\6\3\6\5\6G\n\6\3\7\3\7\3\7\3\b\3\b\3\b\3\t\3\t")
        buf.write("\3\t\3\n\3\n\3\n\3\13\3\13\3\f\6\fX\n\f\r\f\16\fY\3\r")
        buf.write("\3\r\3\16\3\16\3\16\2\2\17\2\4\6\b\n\f\16\20\22\24\26")
        buf.write("\30\32\2\4\4\2\3\16\20\21\3\2\3\34\2\\\2\67\3\2\2\2\4")
        buf.write("9\3\2\2\2\6=\3\2\2\2\bA\3\2\2\2\nD\3\2\2\2\fH\3\2\2\2")
        buf.write("\16K\3\2\2\2\20N\3\2\2\2\22Q\3\2\2\2\24T\3\2\2\2\26W\3")
        buf.write("\2\2\2\30[\3\2\2\2\32]\3\2\2\2\34\35\5\4\3\2\35\36\7\2")
        buf.write("\2\3\368\3\2\2\2\37 \5\6\4\2 !\7\2\2\3!8\3\2\2\2\"#\5")
        buf.write("\b\5\2#$\7\2\2\3$8\3\2\2\2%&\5\n\6\2&\'\7\2\2\3\'8\3\2")
        buf.write("\2\2()\5\f\7\2)*\7\2\2\3*8\3\2\2\2+,\5\16\b\2,-\7\2\2")
        buf.write("\3-8\3\2\2\2./\5\20\t\2/\60\7\2\2\3\608\3\2\2\2\61\62")
        buf.write("\5\22\n\2\62\63\7\2\2\3\638\3\2\2\2\64\65\5\24\13\2\65")
        buf.write("\66\7\2\2\3\668\3\2\2\2\67\34\3\2\2\2\67\37\3\2\2\2\67")
        buf.write("\"\3\2\2\2\67%\3\2\2\2\67(\3\2\2\2\67+\3\2\2\2\67.\3\2")
        buf.write("\2\2\67\61\3\2\2\2\67\64\3\2\2\28\3\3\2\2\29:\7\3\2\2")
        buf.write(":;\7\4\2\2;<\5\26\f\2<\5\3\2\2\2=>\7\5\2\2>?\7\6\2\2?")
        buf.write("@\5\26\f\2@\7\3\2\2\2AB\7\7\2\2BC\7\b\2\2C\t\3\2\2\2D")
        buf.write("F\7\t\2\2EG\7\17\2\2FE\3\2\2\2FG\3\2\2\2G\13\3\2\2\2H")
        buf.write("I\7\n\2\2IJ\7\t\2\2J\r\3\2\2\2KL\7\f\2\2LM\5\30\r\2M\17")
        buf.write("\3\2\2\2NO\7\13\2\2OP\5\30\r\2P\21\3\2\2\2QR\7\r\2\2R")
        buf.write("S\5\30\r\2S\23\3\2\2\2TU\7\16\2\2U\25\3\2\2\2VX\5\32\16")
        buf.write("\2WV\3\2\2\2XY\3\2\2\2YW\3\2\2\2YZ\3\2\2\2Z\27\3\2\2\2")
        buf.write("[\\\t\2\2\2\\\31\3\2\2\2]^\t\3\2\2^\33\3\2\2\2\5\67FY")
        return buf.getvalue()


class GrammarDSLParser ( Parser ):

    grammarFileName = "GrammarDSL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'.'", "','", "'?'", "'!'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "':'", "';'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "CHECK", "GRAMMAR", "SHOW", "TOKENS", 
                      "REVISION", "PLAN", "HISTORY", "RESET", "VERB", "SPELL", 
                      "SYNONYM", "HELP", "NUMBER", "WORD", "PROSE", "PERIOD", 
                      "COMMA", "QUESTION", "EXCLAMATION", "APOSTROPHE", 
                      "QUOTE", "HYPHEN", "COLON", "SEMICOLON", "LEFT_PAREN", 
                      "RIGHT_PAREN", "WS" ]

    RULE_command = 0
    RULE_grammarCheckCmd = 1
    RULE_showTokensCmd = 2
    RULE_revisionPlanCmd = 3
    RULE_historyCmd = 4
    RULE_resetHistoryCmd = 5
    RULE_spellCmd = 6
    RULE_verbCmd = 7
    RULE_synonymCmd = 8
    RULE_helpCmd = 9
    RULE_paragraph = 10
    RULE_lookupWord = 11
    RULE_paragraphToken = 12

    ruleNames =  [ "command", "grammarCheckCmd", "showTokensCmd", "revisionPlanCmd", 
                   "historyCmd", "resetHistoryCmd", "spellCmd", "verbCmd", 
                   "synonymCmd", "helpCmd", "paragraph", "lookupWord", "paragraphToken" ]

    EOF = Token.EOF
    CHECK=1
    GRAMMAR=2
    SHOW=3
    TOKENS=4
    REVISION=5
    PLAN=6
    HISTORY=7
    RESET=8
    VERB=9
    SPELL=10
    SYNONYM=11
    HELP=12
    NUMBER=13
    WORD=14
    PROSE=15
    PERIOD=16
    COMMA=17
    QUESTION=18
    EXCLAMATION=19
    APOSTROPHE=20
    QUOTE=21
    HYPHEN=22
    COLON=23
    SEMICOLON=24
    LEFT_PAREN=25
    RIGHT_PAREN=26
    WS=27

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class CommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def grammarCheckCmd(self):
            return self.getTypedRuleContext(GrammarDSLParser.GrammarCheckCmdContext,0)


        def EOF(self):
            return self.getToken(GrammarDSLParser.EOF, 0)

        def showTokensCmd(self):
            return self.getTypedRuleContext(GrammarDSLParser.ShowTokensCmdContext,0)


        def revisionPlanCmd(self):
            return self.getTypedRuleContext(GrammarDSLParser.RevisionPlanCmdContext,0)


        def historyCmd(self):
            return self.getTypedRuleContext(GrammarDSLParser.HistoryCmdContext,0)


        def resetHistoryCmd(self):
            return self.getTypedRuleContext(GrammarDSLParser.ResetHistoryCmdContext,0)


        def spellCmd(self):
            return self.getTypedRuleContext(GrammarDSLParser.SpellCmdContext,0)


        def verbCmd(self):
            return self.getTypedRuleContext(GrammarDSLParser.VerbCmdContext,0)


        def synonymCmd(self):
            return self.getTypedRuleContext(GrammarDSLParser.SynonymCmdContext,0)


        def helpCmd(self):
            return self.getTypedRuleContext(GrammarDSLParser.HelpCmdContext,0)


        def getRuleIndex(self):
            return GrammarDSLParser.RULE_command

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommand" ):
                listener.enterCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommand" ):
                listener.exitCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommand" ):
                return visitor.visitCommand(self)
            else:
                return visitor.visitChildren(self)




    def command(self):

        localctx = GrammarDSLParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_command)
        try:
            self.state = 53
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [GrammarDSLParser.CHECK]:
                self.enterOuterAlt(localctx, 1)
                self.state = 26
                self.grammarCheckCmd()
                self.state = 27
                self.match(GrammarDSLParser.EOF)
                pass
            elif token in [GrammarDSLParser.SHOW]:
                self.enterOuterAlt(localctx, 2)
                self.state = 29
                self.showTokensCmd()
                self.state = 30
                self.match(GrammarDSLParser.EOF)
                pass
            elif token in [GrammarDSLParser.REVISION]:
                self.enterOuterAlt(localctx, 3)
                self.state = 32
                self.revisionPlanCmd()
                self.state = 33
                self.match(GrammarDSLParser.EOF)
                pass
            elif token in [GrammarDSLParser.HISTORY]:
                self.enterOuterAlt(localctx, 4)
                self.state = 35
                self.historyCmd()
                self.state = 36
                self.match(GrammarDSLParser.EOF)
                pass
            elif token in [GrammarDSLParser.RESET]:
                self.enterOuterAlt(localctx, 5)
                self.state = 38
                self.resetHistoryCmd()
                self.state = 39
                self.match(GrammarDSLParser.EOF)
                pass
            elif token in [GrammarDSLParser.SPELL]:
                self.enterOuterAlt(localctx, 6)
                self.state = 41
                self.spellCmd()
                self.state = 42
                self.match(GrammarDSLParser.EOF)
                pass
            elif token in [GrammarDSLParser.VERB]:
                self.enterOuterAlt(localctx, 7)
                self.state = 44
                self.verbCmd()
                self.state = 45
                self.match(GrammarDSLParser.EOF)
                pass
            elif token in [GrammarDSLParser.SYNONYM]:
                self.enterOuterAlt(localctx, 8)
                self.state = 47
                self.synonymCmd()
                self.state = 48
                self.match(GrammarDSLParser.EOF)
                pass
            elif token in [GrammarDSLParser.HELP]:
                self.enterOuterAlt(localctx, 9)
                self.state = 50
                self.helpCmd()
                self.state = 51
                self.match(GrammarDSLParser.EOF)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GrammarCheckCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHECK(self):
            return self.getToken(GrammarDSLParser.CHECK, 0)

        def GRAMMAR(self):
            return self.getToken(GrammarDSLParser.GRAMMAR, 0)

        def paragraph(self):
            return self.getTypedRuleContext(GrammarDSLParser.ParagraphContext,0)


        def getRuleIndex(self):
            return GrammarDSLParser.RULE_grammarCheckCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGrammarCheckCmd" ):
                listener.enterGrammarCheckCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGrammarCheckCmd" ):
                listener.exitGrammarCheckCmd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGrammarCheckCmd" ):
                return visitor.visitGrammarCheckCmd(self)
            else:
                return visitor.visitChildren(self)




    def grammarCheckCmd(self):

        localctx = GrammarDSLParser.GrammarCheckCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_grammarCheckCmd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.match(GrammarDSLParser.CHECK)
            self.state = 56
            self.match(GrammarDSLParser.GRAMMAR)
            self.state = 57
            self.paragraph()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ShowTokensCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SHOW(self):
            return self.getToken(GrammarDSLParser.SHOW, 0)

        def TOKENS(self):
            return self.getToken(GrammarDSLParser.TOKENS, 0)

        def paragraph(self):
            return self.getTypedRuleContext(GrammarDSLParser.ParagraphContext,0)


        def getRuleIndex(self):
            return GrammarDSLParser.RULE_showTokensCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterShowTokensCmd" ):
                listener.enterShowTokensCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitShowTokensCmd" ):
                listener.exitShowTokensCmd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitShowTokensCmd" ):
                return visitor.visitShowTokensCmd(self)
            else:
                return visitor.visitChildren(self)




    def showTokensCmd(self):

        localctx = GrammarDSLParser.ShowTokensCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_showTokensCmd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(GrammarDSLParser.SHOW)
            self.state = 60
            self.match(GrammarDSLParser.TOKENS)
            self.state = 61
            self.paragraph()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RevisionPlanCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REVISION(self):
            return self.getToken(GrammarDSLParser.REVISION, 0)

        def PLAN(self):
            return self.getToken(GrammarDSLParser.PLAN, 0)

        def getRuleIndex(self):
            return GrammarDSLParser.RULE_revisionPlanCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRevisionPlanCmd" ):
                listener.enterRevisionPlanCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRevisionPlanCmd" ):
                listener.exitRevisionPlanCmd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRevisionPlanCmd" ):
                return visitor.visitRevisionPlanCmd(self)
            else:
                return visitor.visitChildren(self)




    def revisionPlanCmd(self):

        localctx = GrammarDSLParser.RevisionPlanCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_revisionPlanCmd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(GrammarDSLParser.REVISION)
            self.state = 64
            self.match(GrammarDSLParser.PLAN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HistoryCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.limit = None # Token

        def HISTORY(self):
            return self.getToken(GrammarDSLParser.HISTORY, 0)

        def NUMBER(self):
            return self.getToken(GrammarDSLParser.NUMBER, 0)

        def getRuleIndex(self):
            return GrammarDSLParser.RULE_historyCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHistoryCmd" ):
                listener.enterHistoryCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHistoryCmd" ):
                listener.exitHistoryCmd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHistoryCmd" ):
                return visitor.visitHistoryCmd(self)
            else:
                return visitor.visitChildren(self)




    def historyCmd(self):

        localctx = GrammarDSLParser.HistoryCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_historyCmd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(GrammarDSLParser.HISTORY)
            self.state = 68
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==GrammarDSLParser.NUMBER:
                self.state = 67
                localctx.limit = self.match(GrammarDSLParser.NUMBER)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ResetHistoryCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RESET(self):
            return self.getToken(GrammarDSLParser.RESET, 0)

        def HISTORY(self):
            return self.getToken(GrammarDSLParser.HISTORY, 0)

        def getRuleIndex(self):
            return GrammarDSLParser.RULE_resetHistoryCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterResetHistoryCmd" ):
                listener.enterResetHistoryCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitResetHistoryCmd" ):
                listener.exitResetHistoryCmd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitResetHistoryCmd" ):
                return visitor.visitResetHistoryCmd(self)
            else:
                return visitor.visitChildren(self)




    def resetHistoryCmd(self):

        localctx = GrammarDSLParser.ResetHistoryCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_resetHistoryCmd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self.match(GrammarDSLParser.RESET)
            self.state = 71
            self.match(GrammarDSLParser.HISTORY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SpellCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SPELL(self):
            return self.getToken(GrammarDSLParser.SPELL, 0)

        def lookupWord(self):
            return self.getTypedRuleContext(GrammarDSLParser.LookupWordContext,0)


        def getRuleIndex(self):
            return GrammarDSLParser.RULE_spellCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpellCmd" ):
                listener.enterSpellCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpellCmd" ):
                listener.exitSpellCmd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSpellCmd" ):
                return visitor.visitSpellCmd(self)
            else:
                return visitor.visitChildren(self)




    def spellCmd(self):

        localctx = GrammarDSLParser.SpellCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_spellCmd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(GrammarDSLParser.SPELL)
            self.state = 74
            self.lookupWord()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VerbCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VERB(self):
            return self.getToken(GrammarDSLParser.VERB, 0)

        def lookupWord(self):
            return self.getTypedRuleContext(GrammarDSLParser.LookupWordContext,0)


        def getRuleIndex(self):
            return GrammarDSLParser.RULE_verbCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVerbCmd" ):
                listener.enterVerbCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVerbCmd" ):
                listener.exitVerbCmd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVerbCmd" ):
                return visitor.visitVerbCmd(self)
            else:
                return visitor.visitChildren(self)




    def verbCmd(self):

        localctx = GrammarDSLParser.VerbCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_verbCmd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(GrammarDSLParser.VERB)
            self.state = 77
            self.lookupWord()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SynonymCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYNONYM(self):
            return self.getToken(GrammarDSLParser.SYNONYM, 0)

        def lookupWord(self):
            return self.getTypedRuleContext(GrammarDSLParser.LookupWordContext,0)


        def getRuleIndex(self):
            return GrammarDSLParser.RULE_synonymCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSynonymCmd" ):
                listener.enterSynonymCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSynonymCmd" ):
                listener.exitSynonymCmd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSynonymCmd" ):
                return visitor.visitSynonymCmd(self)
            else:
                return visitor.visitChildren(self)




    def synonymCmd(self):

        localctx = GrammarDSLParser.SynonymCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_synonymCmd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(GrammarDSLParser.SYNONYM)
            self.state = 80
            self.lookupWord()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HelpCmdContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def HELP(self):
            return self.getToken(GrammarDSLParser.HELP, 0)

        def getRuleIndex(self):
            return GrammarDSLParser.RULE_helpCmd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHelpCmd" ):
                listener.enterHelpCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHelpCmd" ):
                listener.exitHelpCmd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHelpCmd" ):
                return visitor.visitHelpCmd(self)
            else:
                return visitor.visitChildren(self)




    def helpCmd(self):

        localctx = GrammarDSLParser.HelpCmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_helpCmd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(GrammarDSLParser.HELP)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParagraphContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def paragraphToken(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarDSLParser.ParagraphTokenContext)
            else:
                return self.getTypedRuleContext(GrammarDSLParser.ParagraphTokenContext,i)


        def getRuleIndex(self):
            return GrammarDSLParser.RULE_paragraph

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParagraph" ):
                listener.enterParagraph(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParagraph" ):
                listener.exitParagraph(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParagraph" ):
                return visitor.visitParagraph(self)
            else:
                return visitor.visitChildren(self)




    def paragraph(self):

        localctx = GrammarDSLParser.ParagraphContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_paragraph)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 84
                self.paragraphToken()
                self.state = 87 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarDSLParser.CHECK) | (1 << GrammarDSLParser.GRAMMAR) | (1 << GrammarDSLParser.SHOW) | (1 << GrammarDSLParser.TOKENS) | (1 << GrammarDSLParser.REVISION) | (1 << GrammarDSLParser.PLAN) | (1 << GrammarDSLParser.HISTORY) | (1 << GrammarDSLParser.RESET) | (1 << GrammarDSLParser.VERB) | (1 << GrammarDSLParser.SPELL) | (1 << GrammarDSLParser.SYNONYM) | (1 << GrammarDSLParser.HELP) | (1 << GrammarDSLParser.NUMBER) | (1 << GrammarDSLParser.WORD) | (1 << GrammarDSLParser.PROSE) | (1 << GrammarDSLParser.PERIOD) | (1 << GrammarDSLParser.COMMA) | (1 << GrammarDSLParser.QUESTION) | (1 << GrammarDSLParser.EXCLAMATION) | (1 << GrammarDSLParser.APOSTROPHE) | (1 << GrammarDSLParser.QUOTE) | (1 << GrammarDSLParser.HYPHEN) | (1 << GrammarDSLParser.COLON) | (1 << GrammarDSLParser.SEMICOLON) | (1 << GrammarDSLParser.LEFT_PAREN) | (1 << GrammarDSLParser.RIGHT_PAREN))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LookupWordContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORD(self):
            return self.getToken(GrammarDSLParser.WORD, 0)

        def PROSE(self):
            return self.getToken(GrammarDSLParser.PROSE, 0)

        def CHECK(self):
            return self.getToken(GrammarDSLParser.CHECK, 0)

        def GRAMMAR(self):
            return self.getToken(GrammarDSLParser.GRAMMAR, 0)

        def SHOW(self):
            return self.getToken(GrammarDSLParser.SHOW, 0)

        def TOKENS(self):
            return self.getToken(GrammarDSLParser.TOKENS, 0)

        def REVISION(self):
            return self.getToken(GrammarDSLParser.REVISION, 0)

        def PLAN(self):
            return self.getToken(GrammarDSLParser.PLAN, 0)

        def HISTORY(self):
            return self.getToken(GrammarDSLParser.HISTORY, 0)

        def RESET(self):
            return self.getToken(GrammarDSLParser.RESET, 0)

        def VERB(self):
            return self.getToken(GrammarDSLParser.VERB, 0)

        def SPELL(self):
            return self.getToken(GrammarDSLParser.SPELL, 0)

        def SYNONYM(self):
            return self.getToken(GrammarDSLParser.SYNONYM, 0)

        def HELP(self):
            return self.getToken(GrammarDSLParser.HELP, 0)

        def getRuleIndex(self):
            return GrammarDSLParser.RULE_lookupWord

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLookupWord" ):
                listener.enterLookupWord(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLookupWord" ):
                listener.exitLookupWord(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLookupWord" ):
                return visitor.visitLookupWord(self)
            else:
                return visitor.visitChildren(self)




    def lookupWord(self):

        localctx = GrammarDSLParser.LookupWordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_lookupWord)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarDSLParser.CHECK) | (1 << GrammarDSLParser.GRAMMAR) | (1 << GrammarDSLParser.SHOW) | (1 << GrammarDSLParser.TOKENS) | (1 << GrammarDSLParser.REVISION) | (1 << GrammarDSLParser.PLAN) | (1 << GrammarDSLParser.HISTORY) | (1 << GrammarDSLParser.RESET) | (1 << GrammarDSLParser.VERB) | (1 << GrammarDSLParser.SPELL) | (1 << GrammarDSLParser.SYNONYM) | (1 << GrammarDSLParser.HELP) | (1 << GrammarDSLParser.WORD) | (1 << GrammarDSLParser.PROSE))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParagraphTokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORD(self):
            return self.getToken(GrammarDSLParser.WORD, 0)

        def PROSE(self):
            return self.getToken(GrammarDSLParser.PROSE, 0)

        def NUMBER(self):
            return self.getToken(GrammarDSLParser.NUMBER, 0)

        def PERIOD(self):
            return self.getToken(GrammarDSLParser.PERIOD, 0)

        def COMMA(self):
            return self.getToken(GrammarDSLParser.COMMA, 0)

        def QUESTION(self):
            return self.getToken(GrammarDSLParser.QUESTION, 0)

        def EXCLAMATION(self):
            return self.getToken(GrammarDSLParser.EXCLAMATION, 0)

        def APOSTROPHE(self):
            return self.getToken(GrammarDSLParser.APOSTROPHE, 0)

        def QUOTE(self):
            return self.getToken(GrammarDSLParser.QUOTE, 0)

        def HYPHEN(self):
            return self.getToken(GrammarDSLParser.HYPHEN, 0)

        def COLON(self):
            return self.getToken(GrammarDSLParser.COLON, 0)

        def SEMICOLON(self):
            return self.getToken(GrammarDSLParser.SEMICOLON, 0)

        def LEFT_PAREN(self):
            return self.getToken(GrammarDSLParser.LEFT_PAREN, 0)

        def RIGHT_PAREN(self):
            return self.getToken(GrammarDSLParser.RIGHT_PAREN, 0)

        def CHECK(self):
            return self.getToken(GrammarDSLParser.CHECK, 0)

        def GRAMMAR(self):
            return self.getToken(GrammarDSLParser.GRAMMAR, 0)

        def SHOW(self):
            return self.getToken(GrammarDSLParser.SHOW, 0)

        def TOKENS(self):
            return self.getToken(GrammarDSLParser.TOKENS, 0)

        def REVISION(self):
            return self.getToken(GrammarDSLParser.REVISION, 0)

        def PLAN(self):
            return self.getToken(GrammarDSLParser.PLAN, 0)

        def HISTORY(self):
            return self.getToken(GrammarDSLParser.HISTORY, 0)

        def RESET(self):
            return self.getToken(GrammarDSLParser.RESET, 0)

        def VERB(self):
            return self.getToken(GrammarDSLParser.VERB, 0)

        def SPELL(self):
            return self.getToken(GrammarDSLParser.SPELL, 0)

        def SYNONYM(self):
            return self.getToken(GrammarDSLParser.SYNONYM, 0)

        def HELP(self):
            return self.getToken(GrammarDSLParser.HELP, 0)

        def getRuleIndex(self):
            return GrammarDSLParser.RULE_paragraphToken

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParagraphToken" ):
                listener.enterParagraphToken(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParagraphToken" ):
                listener.exitParagraphToken(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParagraphToken" ):
                return visitor.visitParagraphToken(self)
            else:
                return visitor.visitChildren(self)




    def paragraphToken(self):

        localctx = GrammarDSLParser.ParagraphTokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_paragraphToken)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << GrammarDSLParser.CHECK) | (1 << GrammarDSLParser.GRAMMAR) | (1 << GrammarDSLParser.SHOW) | (1 << GrammarDSLParser.TOKENS) | (1 << GrammarDSLParser.REVISION) | (1 << GrammarDSLParser.PLAN) | (1 << GrammarDSLParser.HISTORY) | (1 << GrammarDSLParser.RESET) | (1 << GrammarDSLParser.VERB) | (1 << GrammarDSLParser.SPELL) | (1 << GrammarDSLParser.SYNONYM) | (1 << GrammarDSLParser.HELP) | (1 << GrammarDSLParser.NUMBER) | (1 << GrammarDSLParser.WORD) | (1 << GrammarDSLParser.PROSE) | (1 << GrammarDSLParser.PERIOD) | (1 << GrammarDSLParser.COMMA) | (1 << GrammarDSLParser.QUESTION) | (1 << GrammarDSLParser.EXCLAMATION) | (1 << GrammarDSLParser.APOSTROPHE) | (1 << GrammarDSLParser.QUOTE) | (1 << GrammarDSLParser.HYPHEN) | (1 << GrammarDSLParser.COLON) | (1 << GrammarDSLParser.SEMICOLON) | (1 << GrammarDSLParser.LEFT_PAREN) | (1 << GrammarDSLParser.RIGHT_PAREN))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





