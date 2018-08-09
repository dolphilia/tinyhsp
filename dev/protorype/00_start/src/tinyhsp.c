#include "tinyhsp.h"

int32_t width = 640;
int32_t height = 480;
uint8_t pixel_data[640 * 480 * 3];

int main(int argc, char* argv[])
{
	int line_length_max; // 行の長さ
    int line_number_max; // 行の個数
    char** line_buffer = NULL; // 読み込み領域を指すポインタ
    char* file_name;
    double result_value;

    // ファイル名を特定する
    if (argc >= 2) {
    	file_name = argv[1];
    } else {
    	file_name = "../test/start.hsp";
    }
    
    // ファイルから行ごとに二次元配列に格納して返す
    line_buffer = malloc_file_to_buffer(file_name, line_buffer, &line_length_max, &line_number_max);

    // 計算のテスト
    for (int i = 0; i < line_number_max; i++) {
        set_line(line_buffer[i]);
		set_st_token_exists(0);
		result_value = parser_expression();
		printf(">>%f\n", result_value);
    }

	// 確保した二次元配列を解放する
	free_line_buffer(line_buffer, line_number_max);
    
    
    //--- ここから描画処理
    
    
    GLFWwindow* window;

    // GLFWライブラリを初期化する
    if (!glfwInit())
        return -1;

    // ウインドウを生成する
    window = glfwCreateWindow(width, height, "Hello World", NULL, NULL);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }

    // ウインドウのコンテキストを生成する
    glfwMakeContextCurrent(window);
    
    // 
    int index = 0;
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            pixel_data[index] = 200;
            pixel_data[index + 1] = 200;
            pixel_data[index + 2] = 200;
            index += 3;
         }
    }

    // ユーザーがウィンドウを閉じるまでループ
    while (!glfwWindowShouldClose(window))
    {
        // 描画処理をここに描く
        glClear(GL_COLOR_BUFFER_BIT);
        glRasterPos2i(-1, -1);
        glDrawPixels(width, height, GL_RGB, GL_UNSIGNED_BYTE, pixel_data);

        // フロントバッファとバックバッファを交換する
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwTerminate();
    return 0;
}
