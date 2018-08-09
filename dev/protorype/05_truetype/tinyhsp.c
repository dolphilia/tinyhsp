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
#define STB_TRUETYPE_IMPLEMENTATION
#include "stb_truetype.h"

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
main(int argc, char **argv)
{
    char ttf_buffer[2000000];
    unsigned char *bitmap;
    int w, h = 0;
    int c = 0x3042; // 表示する文字
    int s = 100; // フォントサイズ
    stbtt_fontinfo font;

    FILE* fp = fopen("./mplus-1c-regular.ttf", "rb");
    fread(ttf_buffer, 1, 2000000, fp);
    fclose(fp);

    int offset = stbtt_GetFontOffsetForIndex(ttf_buffer, 0);
    stbtt_InitFont(&font, ttf_buffer, offset);

    float scale = stbtt_ScaleForPixelHeight(&font, s);
    bitmap = stbtt_GetCodepointBitmap(&font, 0, scale, c, &w, &h, 0, 0);
    
    // GLFWでの描画処理
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
        
        //
        for (int y = 0; y < h; ++y) {
            for (int x = 0; x < w; ++x) {
                int color = 255 - bitmap[y * w + x];
                set_pixel_rgb(pixel_data,
                              x, y,
                              color, color, color,
                              width, height);
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