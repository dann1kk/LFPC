package Lab3;

public class Main {

    public static void main(String[] args) {

        Lexer lexer = new Lexer("C:\\Users\\Daniel\\IdeaProjects\\LFPC\\src\\Lab3\\Input.txt");

        while (!lexer.isExhausted()) {
            System.out.printf("%-6s :: | %s |\n",lexer.currentLexeme() , lexer.currentToken());
            lexer.moveAhead();
        }

        if (lexer.isSuccessful()) {
            System.out.println("O dat Dumnezeu!");
        } else {
            System.out.println(lexer.errorMessage());
        }
    }
}
