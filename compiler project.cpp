#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <unordered_set>

using namespace std;

// Enum for token types
enum TokenType {
    KEYWORD, IDENTIFIER, OPERATOR, NUMBER, CHARACTER_CONSTANT, SPECIAL_CHARACTER, COMMENT, WHITESPACE, NEWLINE, OTHER
};

// Struct to store information about each token
struct Token {
    TokenType type;
    string value;
    int lineNumber;
};

// Set of C++ keywords
const unordered_set<string> keywords = {
    "int", "float", "double", "char", "return", "if", "else", "for", "while",
    "do", "switch", "case", "break", "continue", "class", "public", "private",
    "protected", "void", "const", "static", "struct", "true", "false", "new", "delete"
};

// Set of operators
const unordered_set<string> operators = {
    "+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!",
    "++", "--", "+=", "-=", "*=", "/=", "&", "|", "^", "%", "<<", ">>", "->", ".", "::"
};

// Function to check if a string is a keyword
bool isKeyword(const string& word) {
    return keywords.find(word) != keywords.end();
}

// Function to check if a string is an operator
bool isOperator(const string& word) {
    return operators.find(word) != operators.end();
}

// Function to tokenize a line of code
vector<Token> tokenizeLine(const string& line, int lineNumber) {
    vector<Token> tokens;
    regex tokenPattern(R"(\s+|(\d+)|(\".*?\"|\'.*?\')|(\w+)|([^\w\s]))");
    smatch match;

    string::const_iterator searchStart(line.cbegin());
    while (regex_search(searchStart, line.cend(), match, tokenPattern)) {
        string tokenValue = match[0];
        searchStart = match.suffix().first;

        Token token;
        token.value = tokenValue;
        token.lineNumber = lineNumber;

        // Determine the token type
        if (regex_match(tokenValue, regex(R"(\s+)"))) {
            token.type = WHITESPACE;
        } else if (isKeyword(tokenValue)) {
            token.type = KEYWORD;
        } else if (regex_match(tokenValue, regex(R"(\d+)"))) {
            token.type = NUMBER;
        } else if (isOperator(tokenValue)) {
            token.type = OPERATOR;
        } else if (regex_match(tokenValue, regex(R"(^'.*'$)"))) {
            token.type = CHARACTER_CONSTANT;
        } else if (regex_match(tokenValue, regex(R"(\w+)"))) {
            token.type = IDENTIFIER;
        } else if (tokenValue == "\n") {
            token.type = NEWLINE;
        } else {
            token.type = SPECIAL_CHARACTER;
        }

        tokens.push_back(token);
    }
    return tokens;
}

// Function to analyze C++ code
void analyzeCode(const string& code) {
    istringstream codeStream(code);
    string line;
    int lineNumber = 0;

    cout << "Token Analysis:\n";
    while (getline(codeStream, line)) {
        lineNumber++;
        vector<Token> tokens = tokenizeLine(line, lineNumber);

        for (const Token& token : tokens) {
            cout << "Line " << token.lineNumber << ": ";
            switch (token.type) {
                case KEYWORD: cout << "Keyword"; break;
                case IDENTIFIER: cout << "Identifier"; break;
                case OPERATOR: cout << "Operator"; break;
                case NUMBER: cout << "Numeric constant"; break;
                case CHARACTER_CONSTANT: cout << "Character constant"; break;
                case SPECIAL_CHARACTER: cout << "Special character"; break;
                case WHITESPACE: cout << "White space"; break;
                case NEWLINE: cout << "Newline"; break;
                default: cout << "Other";
            }
            cout << " -> " << token.value << endl;
        }
    }
}

int main() {
    cout << "Enter the C++ code to analyze (end with EOF):\n";
    string code;
    string line;
    while (getline(cin, line)) {
        code += line + "\n";
    }

    analyzeCode(code);
    return 0;
}
