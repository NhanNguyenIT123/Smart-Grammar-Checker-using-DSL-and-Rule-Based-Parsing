grammar GrammarDSL;

command
    : grammarCheckCmd EOF
    | showTokensCmd EOF
    | revisionPlanCmd EOF
    | historyCmd EOF
    | resetHistoryCmd EOF
    | spellCmd EOF
    | verbCmd EOF
    | synonymCmd EOF
    | helpCmd EOF
    ;

grammarCheckCmd
    : CHECK GRAMMAR paragraph
    ;

showTokensCmd
    : SHOW TOKENS paragraph
    ;

revisionPlanCmd
    : REVISION PLAN
    ;

historyCmd
    : HISTORY limit=NUMBER?
    ;

resetHistoryCmd
    : RESET HISTORY
    ;

spellCmd
    : SPELL lookupWord
    ;

verbCmd
    : VERB lookupWord
    ;

synonymCmd
    : SYNONYM lookupWord
    ;

helpCmd
    : HELP
    ;

paragraph
    : paragraphToken+
    ;

lookupWord
    : WORD
    | PROSE
    | CHECK
    | GRAMMAR
    | SHOW
    | TOKENS
    | REVISION
    | PLAN
    | HISTORY
    | RESET
    | VERB
    | SPELL
    | SYNONYM
    | HELP
    ;

paragraphToken
    : WORD
    | PROSE
    | NUMBER
    | PERIOD
    | COMMA
    | QUESTION
    | EXCLAMATION
    | APOSTROPHE
    | QUOTE
    | HYPHEN
    | COLON
    | SEMICOLON
    | LEFT_PAREN
    | RIGHT_PAREN
    | CHECK
    | GRAMMAR
    | SHOW
    | TOKENS
    | REVISION
    | PLAN
    | HISTORY
    | RESET
    | VERB
    | SPELL
    | SYNONYM
    | HELP
    ;

CHECK       : [cC] [hH] [eE] [cC] [kK] ;
GRAMMAR     : [gG] [rR] [aA] [mM] [mM] [aA] [rR] ;
SHOW        : [sS] [hH] [oO] [wW] ;
TOKENS      : [tT] [oO] [kK] [eE] [nN] [sS] ;
REVISION    : [rR] [eE] [vV] [iI] [sS] [iI] [oO] [nN] ;
PLAN        : [pP] [lL] [aA] [nN] ;
HISTORY     : [hH] [iI] [sS] [tT] [oO] [rR] [yY] ;
RESET       : [rR] [eE] [sS] [eE] [tT] ;
VERB        : [vV] [eE] [rR] [bB] ;
SPELL       : [sS] [pP] [eE] [lL] [lL] ;
SYNONYM     : [sS] [yY] [nN] [oO] [nN] [yY] [mM] ;
HELP        : [hH] [eE] [lL] [pP] ;

NUMBER      : [0-9]+ ;
WORD        : LETTER+ (WORD_APOSTROPHE LETTER+)* WORD_APOSTROPHE? ;
PROSE       : ~[ \t\r\n.,?!'"\u2018\u2019\u201C\u201D()\-:;]+ ;
PERIOD      : '.' ;
COMMA       : ',' ;
QUESTION    : '?' ;
EXCLAMATION : '!' ;
APOSTROPHE  : '\'' | '\u2018' | '\u2019' ;
QUOTE       : '"' | '\u201C' | '\u201D' ;
HYPHEN      : '-' | '\u2013' | '\u2014' ;
COLON       : ':' ;
SEMICOLON   : ';' ;
LEFT_PAREN  : '(' ;
RIGHT_PAREN : ')' ;

WS          : [ \t\r\n]+ -> skip ;

fragment LETTER : [a-zA-Z] ;
fragment WORD_APOSTROPHE : '\'' | '\u2018' | '\u2019' ;
