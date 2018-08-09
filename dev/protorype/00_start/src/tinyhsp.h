#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdint.h>
#include <GLFW/glfw3.h>
#ifdef __APPLE__
#include <OpenGL/gl.h>
#else
#include <GL/gl.h>
#endif
#include "token.h"
#include "lexer.h"
#include "parser.h"
#include "utility_random.h"
#include "utility_file.h"