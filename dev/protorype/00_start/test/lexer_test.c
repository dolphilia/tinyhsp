#include "../src/lexer.h"

static void parse_line(char* buf);

int
main(int argc, char **argv) {
   char buf[1024];
    
    while (fgets(buf, 1024, stdin) != NULL) {
        parse_line(buf);
    }
	
	return 0;
}

static void
parse_line(char* buf) {
    Token token;
    
    set_line(buf);
    
    for (;;) {
        get_token(&token);
        if (token.group == EOF_TOKEN) {
            break;
        } else if (token.group == COMMENT_TOKEN) {
            printf("トークン:%d, 文字列:%s\n", token.group, token.string);
            break;
        } else {
            printf("トークン:%d, 文字列:%s\n", token.group, token.string);
        }
    }
}