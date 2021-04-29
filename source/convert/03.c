#include <stdio.h>
#include <stdlib.h>

typedef struct tokenize_context_tag tokenize_context_t;
struct tokenize_context_tag
{
	const char* script_;
	int cursor_;
	int line_;
	const char* line_head_;
};

int main() {
    tokenize_context_t* token = (tokenize_context_t*)malloc(sizeof(tokenize_context_t));
    token->cursor_ = 0;
    token->line_ = 0;
    token->line_head_ = NULL;
    token->script_ = NULL;

    ++token->line_;
    printf("%d", token->line_);
}
		// この位置はマーキング
		//++c->line_;
		//++p;
		//c->line_head_ = p;
		//res->tag_ = TOKEN_EOL;