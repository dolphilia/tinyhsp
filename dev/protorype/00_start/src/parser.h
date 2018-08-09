#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "token.h"
#include "lexer.h"

#define LINE_BUF_SIZE (1024)

void set_st_token_exists(int value);
double parser_main(void);
double parser_expression(void);