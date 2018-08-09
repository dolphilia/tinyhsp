#pragma once

typedef enum {
    BAD_TOKEN,
    NUM_TOKEN,
    ADD_TOKEN,
    SUB_TOKEN,
    MUL_TOKEN,
    DIV_TOKEN,
    STRING_TOKEN,
    LP_TOKEN,
    RP_TOKEN,
    EQUAL_TOKEN,
    EOF_TOKEN,
    COMMENT_TOKEN,
    COMMAND_TOKEN
} TokenGroup;

#define MAX_TOKEN_SIZE (1024)

typedef struct {
    TokenGroup group;
    double value;
    char string[MAX_TOKEN_SIZE];
} Token;