#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <stack>
#include <regex>
using namespace std;

// Struct for Token from the Scanner
struct Token {
    string value;
    int lineNumber;
};

// Function for Tokenization (from previous scanner code)
vector<Token> tokenizeLine(const string& line, int lineNumber);

// Grammar Parsing Logic
class GrammarParser {
    unordered_map<string, vector<string>> grammar; // Stores rules for each non-terminal
    unordered_set<string> nonTerminals;           // Set of non-terminals

    // Function to check for left recursion
    bool hasLeftRecursion() {
        for (const auto& rule : grammar) {
            const string& nonTerminal = rule.first;
            for (const string& production : rule.second) {
                if (!production.empty() && production[0] == nonTerminal[0]) {
                    return true; // Left recursion detected
                }
            }
        }
        return false;
    }

    // Helper function to print the parse tree
    void printParseTree(const vector<pair<string, string>>& tree) {
        cout << "Parse Tree:\n";
        for (const auto& node : tree) {
            cout << node.first << " -> " << node.second << endl;
        }
    }

public:
    // Input Grammar from user
    void inputGrammar() {
        grammar.clear();
        nonTerminals.clear();

        cout << "Enter grammar rules (enter an empty line to stop):\n";
        string nonTerminal, production;

        while (true) {
            cout << "Non-terminal: ";
            getline(cin, nonTerminal);
            if (nonTerminal.empty()) break;

            nonTerminals.insert(nonTerminal);

            vector<string> productions;
            while (true) {
                cout << "Enter production for " << nonTerminal << " (or empty to stop): ";
                getline(cin, production);
                if (production.empty()) break;
                productions.push_back(production);
            }
            grammar[nonTerminal] = productions;
        }

        if (hasLeftRecursion()) {
            cout << "The Grammar isn't simple (contains left recursion). Try again.\n";
            inputGrammar();
        } else {
            cout << "Grammar accepted as simple.\n";
        }
    }

    // Check if a string is accepted by the grammar
    bool parseString(const string& input) {
        stack<string> parseStack; // Parsing stack
        vector<pair<string, string>> parseTree; // To store the parse tree
        parseStack.push("S");   // Start symbol

        size_t index = 0;
        while (!parseStack.empty() && index < input.size()) {
            string top = parseStack.top();
            parseStack.pop();

            if (nonTerminals.find(top) != nonTerminals.end()) {
                // Non-terminal
                bool matched = false;
                for (const string& production : grammar[top]) {
                    if (!production.empty() && production[0] == input[index]) {
                        matched = true;
                        parseTree.emplace_back(top, production);
                        for (int i = production.size() - 1; i >= 0; --i) {
                            parseStack.push(string(1, production[i]));
                        }
                        break;
                    }
                }
                if (!matched) return false;
            } else {
                // Terminal
                if (top[0] == input[index]) {
                    parseTree.emplace_back(top, string(1, input[index]));
                    ++index;
                } else {
                    return false; // Mismatch
                }
            }
        }

        if (parseStack.empty() && index == input.size()) {
            printParseTree(parseTree);
            return true;
        }
        return false;
    }

    void displayGrammar() {
        cout << "Current Grammar:\n";
        for (const auto& rule : grammar) {
            cout << rule.first << " -> ";
            for (size_t i = 0; i < rule.second.size(); ++i) {
                cout << rule.second[i];
                if (i != rule.second.size() - 1) cout << " | ";
            }
            cout << endl;
        }
    }
};

// Main Function
int main() {
    GrammarParser parser;

    while (true) {
        cout << "1- Input Grammar\n2- Check String\n3- Exit\nEnter your choice: ";
        int choice;
        cin >> choice;
        cin.ignore(); // To ignore newline after choice

        if (choice == 1) {
            parser.inputGrammar();
        } else if (choice == 2) {
            string input;
            cout << "Enter the string to be checked: ";
            cin >> input;

            if (parser.parseString(input)) {
                cout << "The string is Accepted.\n";
            } else {
                cout << "The string is Rejected.\n";
            }
        } else if (choice == 3) {
            break;
        } else {
            cout << "Invalid choice. Try again.\n";
        }
    }

    return 0;
}
