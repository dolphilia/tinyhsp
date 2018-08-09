// -lglfw -framework OpenGL
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
//
#ifdef __APPLE__
#include <OpenGL/gl.h>
#else
#include <GL/gl.h>
#endif
#include <GLFW/glfw3.h>
//

uint32_t
xor128()
{
    static uint32_t x = 123456789;
    static uint32_t y = 362436069;
    static uint32_t z = 521288629;
    static uint32_t w = 88675123;
    uint32_t t;
    t = (x ^ (x << 11));
    x = y;
    y = z;
    z = w;
    return (w = (w ^ (w >> 19)) ^ (t ^ (t >> 8)));
}

uint32_t
random_ul_range(uint32_t min_value,
                uint32_t max_value)
{
    return (xor128() % (max_value - min_value + 1) + min_value);
}

int32_t
rand_xor128(int32_t min_value, int32_t max_value)
{
    if (min_value < 0) {
        uint32_t ul = random_ul_range(0, (uint32_t)(max_value + (-1) * min_value));
        return (int)(ul) + min_value;
    } else {
        return random_ul_range((uint32_t)(min_value), (uint32_t)(max_value));
    }
}

void set_pixel_rgb(uint8_t *pixel_data,
                   int32_t point_x, int32_t point_y,
                   uint8_t color_red, uint8_t color_green, uint8_t color_blue,
                   int32_t canvas_size_width, int32_t canvas_size_height)
{
    if (point_x < 0 ||
    	point_y < 0 ||
    	point_x >= canvas_size_width ||
    	point_y >= canvas_size_height)
    {
        return;
    }
    int index = (480 - point_y) * canvas_size_width * 3 + point_x * 3;
    pixel_data[index] = color_red;
    pixel_data[index+1] = color_green;
    pixel_data[index+2] = color_blue;
}

int
main(int argc, char* argv[])
{
    // 変数の初期化
    char script[1024][1024]; // スクリプト格納用の配列
    int line_number_max = 0; // スクリプトの行数
    
    // ファイルから配列にスクリプトを格納する
    {
        // start.hspをオープンする
        FILE* fp = fopen("./start.hsp", "r");
        
        // ファイルの内容を配列に読み込む
        {
            int i = 0; // 字数
            int n = 0; // 行数
            int c = '\0';
            for (;;) {
                c = getc(fp);
                if (c == EOF) {
                    n++;
                    break;
                }
                if (c == '\n') {
                    script[n][i] = '\0';
                    i = 0;
                    n++;
                    continue;
                }
                script[n][i] = c;
                i++;
            }
            line_number_max = n;
        }
        // ファイルをクローズする
        fclose(fp);
    }
    
    // 描画処理
    {
        int width = 640;
        int height = 480;
        char* title = "Untitled";
        unsigned char pixel_data[640 * 480 * 3];
        for (int i = 0; i < width * height * 3; i++) {
            pixel_data[i] = 255;
        }
        GLFWwindow* window;
        
        // GLFWライブラリの初期化
        {
            //初期化して、ウインドウを生成する
            glfwInit();
            window = glfwCreateWindow(width,
                                      height,
                                      title,
                                      NULL,
                                      NULL);
            glfwMakeContextCurrent(window);
        }

        // スクリプトを実行する
        for (int i = 0; i < line_number_max; i++) {
            if (script[i][0] == '\0') {
                continue;
            }
            if (strcmp(script[i], "print") == 0) {
                printf("%s\n", script[i + 1]);
                i++;
            }
            if (strcmp(script[i], "pset") == 0) {
                int point_x = atoi(script[i + 1]);
                int point_y = atoi(script[i + 2]);
                set_pixel_rgb(pixel_data,
                              point_x, point_y,
                              0, 0, 0,
                              width, height);
                i += 2;
            }
        }

        // ウィンドウを閉じるまでループ
        while (!glfwWindowShouldClose(window))
        {      
            // 描画の準備
            glClear(GL_COLOR_BUFFER_BIT);
            glRasterPos2i(-1, -1);
            
            // ピクセルを描画
            glDrawPixels(width,
                         height,
                         GL_RGB,
                         GL_UNSIGNED_BYTE,
                         pixel_data);

            // フロントバッファとバックバッファを交換する
            glfwSwapBuffers(window);

            // イベント待ち
            glfwPollEvents();
        }
        glfwTerminate();
    }
    return 0;
}