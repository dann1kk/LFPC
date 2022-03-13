package Lab3;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public enum Token {

    MINUS ("-"),
    PLUS ("\\+"),
    MULTIPLY ("\\*"),
    DIVIDE ("/"),
    TILDE ("~"),
    AND ("&"),
    OR ("\\|"),
    LESS ("<"),
    BANG("!"),
    LESS_OR_EQUAL ("<="),
    GREATER (">"),
    GREATER_OR_EQUAL (">="),
    EQUAL ("=="),
    NOT_EQUAL("!="),
    ASSIGN ("="),
    ROUND_BRACKET_LEFT ("\\("),
    ROUND_BRACKET_RIGHT ("\\)"),
    SEMICOLON (";"),
    COMMA (","),
    KEY_DEFINE ("define"),
    KEY_FOR("for"),
    KEY_AS ("as"),
    KEY_IS ("is"),
    KEY_IF ("if"),
    KEY_THEN ("then"),
    KEY_ELSE ("else"),
    KEY_ENDIF ("endif"),
    KEY_TRUE("true"),
    KEY_FALSE("false"),
    KEY_RETURN("return"),
    KEY_FUNCTION("function"),
    CURLY_BRACKET_LEFT ("\\{"),
    CURLY_BRACKET_RIGHT ("\\}"),
    SQUARE_BRACKET_LEFT("\\["),
    SQUARE_BRACKET_RIGHT("\\]"),
    DIFFERENT ("<>"),
    APOSTROPHE("'" ),
    MATRIX("matrix"),
    STRING ("\"[^\"]+\""),
    INTEGER ("\\d+"),
    IDENTIFIER ("\\w+"),
    REAL ("(\\d*)\\.\\+d+");

    private final Pattern pattern;

    Token(String regex) {
        pattern = Pattern.compile("^" + regex);
    }

    int endOfMatch(String s) {
        Matcher m = pattern.matcher(s);

        if (m.find()) {
            return m.end();
        }
        return -1;
    }
}