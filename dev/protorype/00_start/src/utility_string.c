#include "utility_string.h"

void init_string(char* str, int size) {
    for (int i = 0; i < size; i++) {
        str[i] = '\0';
    }
}

bool is_equal_string(const char* s1, const char* s2) {
    if (strcmp(s1, s2) == 0) {
        return true;
    } else {
        return false;
    }
}
