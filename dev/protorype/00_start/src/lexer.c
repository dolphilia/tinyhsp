#include "lexer.h"

static bool is_operator(char c);
static bool is_number_status(LexerStatus lex_status);
static void set_operater_token(Token* token, char current_char);
static bool check_status_set_token(Token* token, LexerStatus lex_status, char current_char);
static bool check_char_set_status(LexerStatus* lex_status, char current_char);

static char* st_line;
static int st_line_pos;

const char* keyword_command[] = {"pset", "color", "redraw", "title", "wait"};
const char* keyword_branch[] = {"if", ":"};
const char* keyword_routine[] = {"goto", "gosub", "return"};
const char* keyword_repeat[] = {"repeat", "loop"};
const char* keyword_function[] = {"rnd"};
const char* keyword_variable[] = {"key"};
const char* keyword_comment[] = {";"};
const char* keyword_compare[] = {"==",">=", ">", "<=", "<"};
const char* keyword_operator[] = {"-", "+", "*", "/", "(", ")"};
const char* keyword_array[] = {"@"};

//void init_string(char* str, int size) {
//    for (int i = 0; i < size; i++) {
//        str[i] = '\0';
//    }
//}

//
bool is_command(const char* str, const char* line, int index) {
    int compare_flag = 0;
    int compare_count = 0;
    char compare_string[8];
    for (int i = 0; i < 8; i++) {
        compare_string[i] = '\0';
    }
    //
    for (int i = 0; i < 8; i++) {
        if (line[index] == '\0') {
            break;
        }
        compare_string[i] = line[index + i];
        if (strcmp(compare_string, str) == 0) {
            compare_flag = 1;
            compare_count = i;
        }
    }
    if (compare_flag == 1) {
        if (isspace(line[index + compare_count + 1])) {
            return true;
        }
    }
    return false;
}

void set_token_string(Token* token, const char* str) {
    int len = strlen(str);
    for (int i = 0; i < len; i++) {
        token->string[i] = str[i];
    }
    token->string[len + 1] = '\0';
}

//

void
set_line(char* line)
{
    st_line = line;
    st_line_pos = 0;
}

void
get_token(Token* token)
{
    int out_pos = 0;
    char current_char = ' ';
    LexerStatus lex_status = INITIAL_STATUS;
    token->group = BAD_TOKEN;
    
    while (st_line[st_line_pos] != '\0') {
        current_char = st_line[st_line_pos];
        
        // 字句解析器の状態をチェックしてトークンをセットする
        if (check_status_set_token(token, lex_status, current_char)) {
            return;
        }
        
        // 空白は無視して次に進む
        if (isspace(current_char)) {
            st_line_pos += 1;
            continue;
        }
        
        // トークンが長すぎる場合
        if (out_pos >= MAX_TOKEN_SIZE - 1) {
            fprintf(stderr, "トークンが長すぎます\n");
            exit(1);
        }
        
        // 命令かどうかチェックする
        for (int i = 0; i < get_keyword_count(keyword_command); i++) {
            if (is_command(keyword_command[i], st_line, st_line_pos)) {
                set_token_string(token, keyword_command[i]);
                token->group = COMMAND_TOKEN;
                st_line_pos += strlen(keyword_command[i]);
                return;
            }
        }
        
        // 1文字進める
        token->string[out_pos] = st_line[st_line_pos];
        token->string[out_pos + 1] = '\0';
        st_line_pos += 1;
        out_pos += 1;
        
        // 算術演算子なら算術演算子トークンを返す
        if (is_operator(current_char)) { //[\+\-\*\/]
            set_operater_token(token, current_char);
            return;
        }
        
        // 文字をチェックして状態をセットする
        if (check_char_set_status(&lex_status, current_char)) {
            continue;
        }
        
        fprintf(stderr, "不正な文字です:%c\n", current_char);
        exit(1);
    }
}

// 内部関数

static bool
is_operator(char c)
{
    if (c == '+' || c == '-' || c == '*' || c == '/') {
        return true;
    } else {
        return false;
    }
}

static bool
is_number_status(LexerStatus lex_status)
{
    if ((lex_status == INT_STATUS
        || lex_status == FRAC_STATUS)) {
        return true;
    } else {
        return false;
    }
}

static void
set_operater_token(Token* token, char current_char)
{
    if (current_char == '+') {
        token->group = ADD_TOKEN;
    } else if (current_char == '-') {
        token->group = SUB_TOKEN;
    } else if (current_char == '*') {
        token->group = MUL_TOKEN;
    } else if (current_char == '/') {
        token->group = DIV_TOKEN;
    } else {
    }
}

static bool
check_status_set_token(Token* token, LexerStatus lex_status, char current_char)
{
    if (st_line_pos == 0
        && current_char == ';')
    {
        token->group = COMMENT_TOKEN;
        return true;
    }
        
    if (is_number_status(lex_status)
        && !isdigit(current_char)
        && current_char != '.')
    {
        token->group = NUM_TOKEN;
        sscanf(token->string, "%lf", &token->value);
        return true;
    }
        
    if (lex_status == LP_STATUS) {
        if (!is_operator(current_char)
            && current_char != '.'
            && current_char != '=')
        {
            token->group = LP_TOKEN;
            return true;
        }
        else {
            fprintf(stderr, "シンタックスエラー\n");
            exit(1);
        }
    }
        
    if (lex_status == RP_STATUS) {
        if (current_char != '.'
            && current_char != '=')
        {
            token->group = RP_TOKEN;
            return true;
        }
        else {
            fprintf(stderr, "シンタックスエラー\n");
            exit(1);
        }
    }
        
    if (lex_status == EQUAL_STATUS) {
        token->group = EQUAL_TOKEN;
        return true;
    }
        
    if (current_char == '\n') {
        token->group = EOF_TOKEN;
        return true;
    }
    
    return false;
}

static bool
check_char_set_status(LexerStatus* lex_status, char current_char)
{
    if (isdigit(current_char)) { //[0-9]
        if (*lex_status == INITIAL_STATUS) {
            *lex_status = INT_STATUS;
        } else if (*lex_status == DOT_STATUS) {
            *lex_status = FRAC_STATUS;
        } else {}
        return true;
    }
        
    if (current_char == '(') {
        *lex_status = LP_STATUS;
        return true;
    }
        
    if (current_char == ')') {
        *lex_status = RP_STATUS;
        return true;
    }
        
    if (current_char == '=') {
        *lex_status = EQUAL_STATUS;
        return true;
    }
        
    if (current_char == '.') {
        if (*lex_status == INT_STATUS) {
            *lex_status = DOT_STATUS;
            return true;
        } else {
            fprintf(stderr, "シンタックスエラー\n");
            exit(1);
        }
    }
        
    if (current_char == '"') {
        if (*lex_status != STRING_STATUS) {
            *lex_status = STRING_STATUS;
            return true;
        } else {
        }
    }
        
    if (*lex_status == STRING_STATUS) {
        return true;
    }
    
    return false;
}