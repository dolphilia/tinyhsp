#include "utility_file.h"

static FILE* file_open_read(const char* file_name); // ファイルを読み込み専用でオープンする
static char** malloc_line_number(FILE* fp, char** line_buffer, size_t size); // ファイルの行数分のポインタ領域を確保する
static char** malloc_line_length(FILE* fp, char** line_buffer, int line_number, int line_length); // ファイルの行数分の文字列用配列領域を確保する
static void buffer_read_with_fp(FILE* fp, char** line_buffer, int line_number, int line_length); // ファイルの内容を各行に読み込む
static void get_matrix_with_file(FILE* fp, int* line_length, int* line_number); // ファイル中の最大の行の文字列長と行数を返す

char**
malloc_file_to_buffer(const char* file_name, char** line_buffer, int* line_length, int* line_number)
{
	FILE* fp = file_open_read(file_name);
    get_matrix_with_file(fp, line_length, line_number);
	line_buffer = malloc_line_number(fp, line_buffer, *line_number * sizeof(char*));
	line_buffer = malloc_line_length(fp, line_buffer, *line_number, *line_length);
	buffer_read_with_fp(fp, line_buffer, *line_number, *line_length);
    fclose(fp); // ファイルをクローズする
    return line_buffer;
}

void
free_line_buffer(char** line_buffer, int line_num)
{
    for (int i = 0; i < line_num; i++) { // 各行の文字列用配列領域を解放する
        free(line_buffer[i]);
    }
    free(line_buffer); // ポインタ領域を解放する
}

static FILE*
file_open_read(const char* file_name)
{
	FILE* fp = fopen(file_name, "r");
	if (fp == NULL) {
    	fprintf(stderr, "ファイルのオープンに失敗しました\n");
        exit(1);
    }
    return fp;
}

static char**
malloc_line_number(FILE* fp, char** line_buffer, size_t size)
{
	line_buffer = malloc(size);
	if (line_buffer == NULL) {
        // 解放してエラー終了
        fclose(fp);
        fprintf(stderr, "ポインタ領域を確保できませんでした\n");
        exit(1);
    }
    return line_buffer;
}

static char**
malloc_line_length(FILE* fp, char** line_buffer, int line_number, int line_length)
{
	for (int i = 0; i < line_number; i++) {
		line_buffer[i] = malloc(line_length + 1);
        if (line_buffer[i] == NULL) {
            // 解放してエラー終了
            free(line_buffer);
            fclose(fp);
            fprintf(stderr, "ポインタ領域を確保できませんでした\n");
        	exit(1);
        }
    }
    return line_buffer;
}

static void
buffer_read_with_fp(FILE* fp, char** line_buffer, int line_number, int line_length)
{
	for (int i = 0; i < line_number; i++) {
        if (NULL == fgets(line_buffer[i], line_length, fp)) {
            // 解放してエラー終了
            for (i = 0; i < line_number; i++) {
                free(line_buffer[i]);
            }
            free(line_buffer);
            fclose(fp);
            fprintf(stderr, "ファイルの内容の読み込みに失敗しました\n");
        	exit(1);
        }
    }
}

static void
get_matrix_with_file(FILE* fp, int* line_length, int* line_number)
{
    int len = 0; // 字数
    int len_max = -1; // 最大字数
    int num = 0; // 行数
    int c; // 現在の文字
    rewind(fp); // ファイル位置を巻き戻す
    
    // ファイルを１文字ずつ終わりまで読み込む
    while ((c = getc(fp)) != EOF) {
        len++; // fgets() は改行も含むので、EOF 以外ならばとにかく 1字増やす
        if (c == '\n') { // 改行であれば
            num++; // 1行増やす
            if (len > len_max) { // 字数が最大字数を超えていれば
                len_max = len; // 最大字数を更新する
            }
            len = 0; // 次の行に備えて字数を初期化
        }
    }
    
    // EOF に達したが何かしらの文字があった場合
    if (len > 0 && c == EOF) {
        num++; // それも最後の 1行とみなす
        if (len > len_max) { // 字数が最大字数を超えているならば
            len_max = len; // 最大字数を更新する
        }
    }

    // 最大字数と行数がいずれも 0 を超えていれば「正常」終了
    if (len_max > 0 && num > 0) {
        rewind(fp); // ファイル位置を巻き戻す
        *line_length = len_max;
        *line_number = num;
        return;
    }

	// 解放してエラー終了
    fclose(fp);
    fprintf(stderr, "ファイルのマトリクス情報を取得できませんでした\n");
    exit(1);
}