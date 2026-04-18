# Generated from C:\GITHUB\Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing\backend\src\grammar_dsl\dsl\grammar\GrammarDSL.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\33")
        buf.write("\u00a3\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\3\2\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3")
        buf.write("\6\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t")
        buf.write("\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13")
        buf.write("\3\13\3\13\3\13\3\13\3\f\6\fy\n\f\r\f\16\fz\3\r\6\r~\n")
        buf.write("\r\r\r\16\r\177\3\16\6\16\u0083\n\16\r\16\16\16\u0084")
        buf.write("\3\17\3\17\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\24")
        buf.write("\3\24\3\25\3\25\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31")
        buf.write("\3\32\6\32\u009e\n\32\r\32\16\32\u009f\3\32\3\32\2\2\33")
        buf.write("\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31")
        buf.write("\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31")
        buf.write("\61\32\63\33\3\2\32\4\2EEee\4\2JJjj\4\2GGgg\4\2MMmm\4")
        buf.write("\2IIii\4\2TTtt\4\2CCcc\4\2OOoo\4\2XXxx\4\2KKkk\4\2UUu")
        buf.write("u\4\2QQqq\4\2PPpp\4\2RRrr\4\2NNnn\4\2VVvv\4\2[[{{\4\2")
        buf.write("DDdd\3\2\62;\4\2C\\c|\5\2\13\f\17\17\"\"\4\2))\u201a\u201b")
        buf.write("\4\2$$\u201e\u201f\4\2//\u2015\u2016\2\u00a6\2\3\3\2\2")
        buf.write("\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2")
        buf.write("\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25")
        buf.write("\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3")
        buf.write("\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write("\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2")
        buf.write("\2\61\3\2\2\2\2\63\3\2\2\2\3\65\3\2\2\2\5;\3\2\2\2\7C")
        buf.write("\3\2\2\2\tL\3\2\2\2\13Q\3\2\2\2\rY\3\2\2\2\17_\3\2\2\2")
        buf.write("\21d\3\2\2\2\23j\3\2\2\2\25r\3\2\2\2\27x\3\2\2\2\31}\3")
        buf.write("\2\2\2\33\u0082\3\2\2\2\35\u0086\3\2\2\2\37\u0088\3\2")
        buf.write("\2\2!\u008a\3\2\2\2#\u008c\3\2\2\2%\u008e\3\2\2\2\'\u0090")
        buf.write("\3\2\2\2)\u0092\3\2\2\2+\u0094\3\2\2\2-\u0096\3\2\2\2")
        buf.write("/\u0098\3\2\2\2\61\u009a\3\2\2\2\63\u009d\3\2\2\2\65\66")
        buf.write("\t\2\2\2\66\67\t\3\2\2\678\t\4\2\289\t\2\2\29:\t\5\2\2")
        buf.write(":\4\3\2\2\2;<\t\6\2\2<=\t\7\2\2=>\t\b\2\2>?\t\t\2\2?@")
        buf.write("\t\t\2\2@A\t\b\2\2AB\t\7\2\2B\6\3\2\2\2CD\t\7\2\2DE\t")
        buf.write("\4\2\2EF\t\n\2\2FG\t\13\2\2GH\t\f\2\2HI\t\13\2\2IJ\t\r")
        buf.write("\2\2JK\t\16\2\2K\b\3\2\2\2LM\t\17\2\2MN\t\20\2\2NO\t\b")
        buf.write("\2\2OP\t\16\2\2P\n\3\2\2\2QR\t\3\2\2RS\t\13\2\2ST\t\f")
        buf.write("\2\2TU\t\21\2\2UV\t\r\2\2VW\t\7\2\2WX\t\22\2\2X\f\3\2")
        buf.write("\2\2YZ\t\7\2\2Z[\t\4\2\2[\\\t\f\2\2\\]\t\4\2\2]^\t\21")
        buf.write("\2\2^\16\3\2\2\2_`\t\n\2\2`a\t\4\2\2ab\t\7\2\2bc\t\23")
        buf.write("\2\2c\20\3\2\2\2de\t\f\2\2ef\t\17\2\2fg\t\4\2\2gh\t\20")
        buf.write("\2\2hi\t\20\2\2i\22\3\2\2\2jk\t\f\2\2kl\t\22\2\2lm\t\16")
        buf.write("\2\2mn\t\r\2\2no\t\16\2\2op\t\22\2\2pq\t\t\2\2q\24\3\2")
        buf.write("\2\2rs\t\3\2\2st\t\4\2\2tu\t\20\2\2uv\t\17\2\2v\26\3\2")
        buf.write("\2\2wy\t\24\2\2xw\3\2\2\2yz\3\2\2\2zx\3\2\2\2z{\3\2\2")
        buf.write("\2{\30\3\2\2\2|~\t\25\2\2}|\3\2\2\2~\177\3\2\2\2\177}")
        buf.write("\3\2\2\2\177\u0080\3\2\2\2\u0080\32\3\2\2\2\u0081\u0083")
        buf.write("\n\26\2\2\u0082\u0081\3\2\2\2\u0083\u0084\3\2\2\2\u0084")
        buf.write("\u0082\3\2\2\2\u0084\u0085\3\2\2\2\u0085\34\3\2\2\2\u0086")
        buf.write("\u0087\7\60\2\2\u0087\36\3\2\2\2\u0088\u0089\7.\2\2\u0089")
        buf.write(" \3\2\2\2\u008a\u008b\7A\2\2\u008b\"\3\2\2\2\u008c\u008d")
        buf.write("\7#\2\2\u008d$\3\2\2\2\u008e\u008f\t\27\2\2\u008f&\3\2")
        buf.write("\2\2\u0090\u0091\t\30\2\2\u0091(\3\2\2\2\u0092\u0093\t")
        buf.write("\31\2\2\u0093*\3\2\2\2\u0094\u0095\7<\2\2\u0095,\3\2\2")
        buf.write("\2\u0096\u0097\7=\2\2\u0097.\3\2\2\2\u0098\u0099\7*\2")
        buf.write("\2\u0099\60\3\2\2\2\u009a\u009b\7+\2\2\u009b\62\3\2\2")
        buf.write("\2\u009c\u009e\t\26\2\2\u009d\u009c\3\2\2\2\u009e\u009f")
        buf.write("\3\2\2\2\u009f\u009d\3\2\2\2\u009f\u00a0\3\2\2\2\u00a0")
        buf.write("\u00a1\3\2\2\2\u00a1\u00a2\b\32\2\2\u00a2\64\3\2\2\2\7")
        buf.write("\2z\177\u0084\u009f\3\b\2\2")
        return buf.getvalue()


class GrammarDSLLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    CHECK = 1
    GRAMMAR = 2
    REVISION = 3
    PLAN = 4
    HISTORY = 5
    RESET = 6
    VERB = 7
    SPELL = 8
    SYNONYM = 9
    HELP = 10
    NUMBER = 11
    WORD = 12
    PROSE = 13
    PERIOD = 14
    COMMA = 15
    QUESTION = 16
    EXCLAMATION = 17
    APOSTROPHE = 18
    QUOTE = 19
    HYPHEN = 20
    COLON = 21
    SEMICOLON = 22
    LEFT_PAREN = 23
    RIGHT_PAREN = 24
    WS = 25

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'.'", "','", "'?'", "'!'", "':'", "';'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "CHECK", "GRAMMAR", "REVISION", "PLAN", "HISTORY", "RESET", 
            "VERB", "SPELL", "SYNONYM", "HELP", "NUMBER", "WORD", "PROSE", 
            "PERIOD", "COMMA", "QUESTION", "EXCLAMATION", "APOSTROPHE", 
            "QUOTE", "HYPHEN", "COLON", "SEMICOLON", "LEFT_PAREN", "RIGHT_PAREN", 
            "WS" ]

    ruleNames = [ "CHECK", "GRAMMAR", "REVISION", "PLAN", "HISTORY", "RESET", 
                  "VERB", "SPELL", "SYNONYM", "HELP", "NUMBER", "WORD", 
                  "PROSE", "PERIOD", "COMMA", "QUESTION", "EXCLAMATION", 
                  "APOSTROPHE", "QUOTE", "HYPHEN", "COLON", "SEMICOLON", 
                  "LEFT_PAREN", "RIGHT_PAREN", "WS" ]

    grammarFileName = "GrammarDSL.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


