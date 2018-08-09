#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

char** malloc_file_to_buffer(const char* file_name, char** line_buffer, int* line_length, int* line_number); // ファイルから行ごとに二次元配列に格納して返す
void free_line_buffer(char** line_buffer, int line_num); // 確保した二次元配列を解放する