#include <exception>
#include <fstream>
#include <iostream>
#include "antlr4-runtime.h"
#include "CACTLexer.h"
#include "CACTParser.h"

class ErrorListener final : public antlr4::BaseErrorListener {
public:
    bool failed = false;
    void syntaxError(antlr4::Recognizer *, antlr4::Token *, size_t line,
                     size_t column, const std::string &message,
                     std::exception_ptr) override {
        failed = true;
        std::cerr << line << ':' << column + 1 << ": " << message << '\n';
    }
};

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <source.cact>\n";
        return 2;
    }
    std::ifstream source(argv[1], std::ios::binary);
    if (!source) {
        std::cerr << "Cannot open input: " << argv[1] << '\n';
        return 2;
    }
    try {
        antlr4::ANTLRInputStream input(source);
        CACTLexer lexer(&input);
        ErrorListener errors;
        lexer.removeErrorListeners();
        lexer.addErrorListener(&errors);
        antlr4::CommonTokenStream tokens(&lexer);
        // Read all tokens so even invalid trailing characters are checked.
        tokens.fill();
        if (errors.failed) return 1;
        CACTParser parser(&tokens);
        parser.removeErrorListeners();
        parser.addErrorListener(&errors);
        parser.compUnit();
        return errors.failed || parser.getNumberOfSyntaxErrors() != 0 ? 1 : 0;
    } catch (const std::exception &error) {
        std::cerr << "Analysis failed: " << error.what() << '\n';
        return 2;
    }
}
