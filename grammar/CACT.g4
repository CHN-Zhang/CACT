grammar CACT;
compUnit: (decl | funcDef)+ EOF;
decl: constDecl | varDecl;
constDecl: CONST bType constDef (COMMA constDef)* SEMI;
bType: INT | FLOAT | DOUBLE | CHAR;
constDef: IDENT (LBRACKET INT_CONST RBRACKET)* ASSIGN constInitVal;
constInitVal: constant | LBRACE (constInitVal (COMMA constInitVal)*)? RBRACE;
constant: (PLUS | MINUS)? (INT_CONST | FLOAT_CONST) | CHAR_CONST;
varDecl: bType varDef (COMMA varDef)* SEMI;
varDef: IDENT (LBRACKET INT_CONST RBRACKET)* (ASSIGN constInitVal)?;
funcDef: funcType IDENT LPAREN funcFParams? RPAREN block;
funcType: VOID | bType;
funcFParams: funcFParam (COMMA funcFParam)*;
funcFParam: bType IDENT (LBRACKET INT_CONST? RBRACKET (LBRACKET INT_CONST RBRACKET)*)?;
block: LBRACE blockItem* RBRACE;
blockItem: decl | stmt;
stmt
    : lVal ASSIGN exp SEMI | exp? SEMI | block
    | IF LPAREN cond RPAREN stmt (ELSE stmt)?
    | WHILE LPAREN cond RPAREN stmt
    | BREAK SEMI | CONTINUE SEMI | RETURN exp? SEMI
    ;
exp: addExp;
cond: lOrExp;
lVal: IDENT (LBRACKET exp RBRACKET)*;
primaryExp: LPAREN exp RPAREN | lVal | number;
number: INT_CONST | FLOAT_CONST | CHAR_CONST;
unaryExp: primaryExp | IDENT LPAREN funcRParams? RPAREN | (PLUS | MINUS) unaryExp;
funcRParams: exp (COMMA exp)*;
mulExp: unaryExp ((MUL | DIV | MOD) unaryExp)*;
addExp: mulExp ((PLUS | MINUS) mulExp)*;
// Mirror arithmetic precedence for conditions, adding ! and grouped conditions.
condPrimaryExp: LPAREN cond RPAREN | lVal | number;
condUnaryExp: condPrimaryExp | IDENT LPAREN funcRParams? RPAREN | (PLUS | MINUS | NOT) condUnaryExp;
condMulExp: condUnaryExp ((MUL | DIV | MOD) condUnaryExp)*;
condAddExp: condMulExp ((PLUS | MINUS) condMulExp)*;
relExp: condAddExp ((LT | GT | LE | GE) condAddExp)?;
eqExp: relExp ((EQ | NE) relExp)?;
lAndExp: eqExp (AND eqExp)*;
lOrExp: lAndExp (OR lAndExp)*;
CONST: 'const';
INT: 'int';
FLOAT: 'float';
CHAR: 'char';
VOID: 'void';
IF: 'if';
ELSE: 'else';
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';
RETURN: 'return';
DOUBLE: 'double';
PLUS: '+';
MINUS: '-';
NOT: '!';
MUL: '*';
DIV: '/';
MOD: '%';
LE: '<=';
GE: '>=';
LT: '<';
GT: '>';
EQ: '==';
NE: '!=';
AND: '&&';
OR: '||';
ASSIGN: '=';
LPAREN: '(';
RPAREN: ')';
LBRACKET: '[';
RBRACKET: ']';
LBRACE: '{';
RBRACE: '}';
COMMA: ',';
SEMI: ';';
FLOAT_CONST
    : (DIGIT+ '.' DIGIT* | '.' DIGIT+) EXPONENT? [fF]?
    | DIGIT+ EXPONENT [fF]?
    ;
INT_CONST: '0' [xX] HEX_DIGIT+ | '0' [0-7]* | [1-9] DIGIT*;
CHAR_CONST: '\'' ('\\' [nt\\'"0] | [\u0000-\u0009\u000B-\u000C\u000E-\u0026\u0028-\u005B\u005D-\u007F]) '\'';
IDENT: [a-zA-Z_] [a-zA-Z_0-9]*;
fragment DIGIT: [0-9];
fragment HEX_DIGIT: [0-9a-fA-F];
fragment EXPONENT: [eE] [+-]? DIGIT+;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
WS: [ \t\r\n\f\u000B]+ -> skip;
