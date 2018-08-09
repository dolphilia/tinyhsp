#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// ファイル中の最大の行の文字列長と行数を返す
void
get_matrix_with_file(FILE* fp,
                     int* line_length,
                     int* line_number)
{
    int len = 0; // 字数
    int len_max = -1; // 最大字数
    int num = 0; // 行数
    int c = '\n'; // 現在の文字
    rewind(fp); // ファイル位置を巻き戻す
    for (;;) { // ファイルを１文字ずつ終わりまで読み込む
        c = getc(fp);
        if (c == EOF) {
            break;
        }
        len++; // 1字増やす
        if (c == '\n') { // 改行であれば
            num++; // 1行増やす
            if (len > len_max) { // 字数が最大字数を超えていれば
                len_max = len; // 最大字数を更新する
            }
            len = 0; // 次の行に備えて字数を初期化
        }
    }
    if (len > 0 && c == EOF) { // EOF に達したが何かしらの文字があった場合
        num++; // 1行とみなす
        if (len > len_max) { // 字数が最大字数を超えているならば
            len_max = len; // 最大字数を更新する
        }
    }
    if (len_max == 0 && num == 0) { // 最大字数と行数がいずれも 0 を超えていれば「正常」終了
        fprintf(stderr, "ファイルのマトリクス情報を取得できませんでした\n");
        exit(1);
    }
    *line_length = len_max;
    *line_number = num;
    return;
}

// ファイルの内容を各行に読み込む
void
buffer_read_with_fp(FILE* fp,
                    char** line_buffer,
                    int line_number,
                    int line_length)
{
    int i = 0; // index
    int n = 0; // line number 行数
    int c = '\0';
    rewind(fp); // ファイル位置を巻き戻す
    for (;;) {
        c = getc(fp);
        if (c == EOF) {
            break;
        }
        if (c == '\n') {
            line_buffer[n][i] = '\0';
            i = 0;
            n++;
            continue;
        }
        line_buffer[n][i] = c;
        i++;
    }
    if (c == EOF && n + 1 != line_number) {
        fprintf(stderr, "ファイルの内容の読み込みに失敗しました\n");
        exit(1);
    }
}

// ファイルの行数分の文字列用配列領域を確保する
char**
malloc_line_length(FILE* fp,
                   char** line_buffer,
                   int line_number,
                   int line_length)
{
	for (int i = 0; i < line_number; i++) {
		line_buffer[i] = malloc(line_length + 1); //ヌル文字分
        if (line_buffer[i] == NULL) {
            fprintf(stderr, "ポインタ領域を確保できませんでした\n");
        	exit(1);
        }
    }
    return line_buffer;
}

// ファイルの行数分のポインタ領域を確保する
char**
malloc_line_number(FILE* fp,
                   char** line_buffer,
                   size_t size)
{
	line_buffer = malloc(size);
	if (line_buffer == NULL) {
        fprintf(stderr, "ポインタ領域を確保できませんでした\n");
        exit(1);
    }
    return line_buffer;
}

// ファイル名からファイルを読み込み専用でオープンする
FILE*
file_open_read(const char* file_name)
{
	FILE* fp = fopen(file_name, "r");
	if (fp == NULL) {
    	fprintf(stderr, "ファイルのオープンに失敗しました\n");
        exit(1);
    }
    return fp;
}

// 確保した二次元配列を解放する
void
free_line_buffer(char** line_buffer,
                 int line_num)
{
    for (int i = 0; i < line_num; i++) { // 各行の文字列用配列領域を解放する
        free(line_buffer[i]);
    }
    free(line_buffer); // ポインタ領域を解放する
}

// ファイルから行ごとに二次元配列に格納して返す
char**
malloc_file_to_buffer(const char* file_name,
                      char** line_buffer,
                      int* line_length,
                      int* line_number)
{
	FILE* fp = file_open_read(file_name);
    get_matrix_with_file(fp, line_length, line_number);
	line_buffer = malloc_line_number(fp, line_buffer, *line_number * sizeof(char*));
	line_buffer = malloc_line_length(fp, line_buffer, *line_number, *line_length);
	buffer_read_with_fp(fp, line_buffer, *line_number, *line_length);
    fclose(fp); // ファイルをクローズする
    return line_buffer;
}

int
main(int argc, char* argv[])
{
	int line_length_max; // 行の最大の長さ
    int line_number_max; // 最大の行数
    char** line_buffer = NULL; // ファイルの文字列を格納する二次元配列
    char* file_name;

    // ファイル名を特定する
    if (argc >= 2) {
    	file_name = argv[1];
    } else {
    	file_name = "./start.hsp";
    }
    
    // ファイルから行ごとに二次元配列に格納して返す
    line_buffer = malloc_file_to_buffer(file_name,
                                        line_buffer,
                                        &line_length_max,
                                        &line_number_max);

    for (int i = 0; i < line_number_max; i++) {
        printf("%s\n", line_buffer[i]);
    }

	// 確保した二次元配列を解放する
	free_line_buffer(line_buffer,
	                 line_number_max);
    return 0;
}