#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "token.h"

#define get_keyword_count(a) ((int)(sizeof a / sizeof(char*)))
#define get_array_count(a,b) ((int)(sizeof a / sizeof(b)))

typedef enum {
    INITIAL_STATUS,
    INT_STATUS,
    DOT_STATUS,
    FRAC_STATUS,
    STRING_STATUS,
    LP_STATUS, //(
    RP_STATUS, //)
    EQUAL_STATUS
} LexerStatus;

void set_line(char* line);
void get_token(Token* token);