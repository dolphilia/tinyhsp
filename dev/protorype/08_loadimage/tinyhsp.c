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
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

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
    int index = (canvas_size_height - point_y) * canvas_size_width * 3 + point_x * 3;
    pixel_data[index] = color_red;
    pixel_data[index+1] = color_green;
    pixel_data[index+2] = color_blue;
}

int
main(int argc, char **argv)
{
    // GLFWでの描画処理
    {
        int canvas_width = 640;
        int canvas_height = 480;
        char* title = "Untitled";
        unsigned char pixel_data[640 * 480 * 3 * 2];
        for (int i = 0; i < canvas_width * canvas_height * 3; i++) {
            pixel_data[i] = 255;
        }
        GLFWwindow* window;
        
        // GLFWライブラリの初期化
        {
            //初期化して、ウインドウを生成する
            glfwInit();
            window = glfwCreateWindow(canvas_width,
                                      canvas_height,
                                      title,
                                      NULL,
                                      NULL);
            glfwMakeContextCurrent(window);
        }
        
        // 画像を読み込む
        {
            char* image_file_name = "./miyuzu.jpg";
            uint8_t *image_pixels;
            int image_width;
            int image_height;
            int image_bpp;//色数 3 or 4
            image_pixels = stbi_load(image_file_name,
                                     &image_width,
                                     &image_height,
                                     &image_bpp,
                                     0);
            int i = 0;
            for (int y = 0; y < image_height; y++) {
                for (int x = 0; x < image_width; x++) {
                    int r = image_pixels[i];
                    int g = image_pixels[i + 1];
                    int b = image_pixels[i + 2];
                    set_pixel_rgb(pixel_data,
                                  x, y,
                                  r, g, b,
                                  canvas_width, canvas_height);
                    i += 3;
                }
            }
            free(image_pixels);
        }

        // ウィンドウを閉じるまでループ
        while (!glfwWindowShouldClose(window))
        {      
            // 描画の準備
            glClear(GL_COLOR_BUFFER_BIT);
            glRasterPos2i(-1, -1);
            
            // ピクセルを描画
            glDrawPixels(canvas_width,
                         canvas_height,
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