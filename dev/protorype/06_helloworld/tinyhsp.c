// -lglfw -framework OpenGL
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
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

// ピクセル操作

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

// 文字列操作

int
utf8len(uint8_t c)
{
	if (c >= 0 && c < 128) { return 1; }
	if (c >= 128 && c < 192) { return 2; }
	if (c >= 192 && c < 224) { return 2; }
	if (c >= 224 && c < 240) { return 3; }
	if (c >= 240 && c < 248) { return 4; }
	if (c >= 248 && c < 252) { return 5; }
	if (c >= 252 && c < 254) { return 6; }
	if (c >= 254 && c <= 255) { return 6; }
	return 0;
}

int
utf8strlen(const char* s)
{
    int length = 0;
    for (int i = 0; i < strlen(s); i++) {
        if (s[i] == '\0') {
            break;
        }
        i += utf8len(s[i]) - 1;
        length++;
    }
    return length;
}

void
utf8char_at(char* dest, const char* src, int index)
{
    int count = 0;
    for (int i = 0; i < strlen(src); i++) {
        if (src[i] == '\0') {
            break;
        }
        if (count == index) {
            for (int j = 0; j < utf8len(src[i]); j++) {
                dest[j] = src[i + j];
            }
            return;
        }
        i += utf8len(src[i]) - 1;
        count++;
    }
    return;
}

void
init_str(char* str, int size)
{
    for (int i = 0; i < size; i++) {
        str[i] = '\0';
    }
}

// utf8 -> utf16変換

// カウント
int
utf8_count(const char *p_utf8,
           int n_utf8_num)
{
    int n_utf8 = 0;
    int count = 0;
    for (n_utf8 = 0; n_utf8 < n_utf8_num; ) {
        if ((p_utf8[n_utf8] & 0x80) == 0x00) { // 最上位ビット = 0
            n_utf8 += 1;
        } else if ((p_utf8[n_utf8] & 0xe0) == 0xc0) { // 上位3ビット = 110
            n_utf8 += 2;
        } else {
            n_utf8 += 3;
        }
        count += 1;
    }
    return count;
}

// UTF-8 -> Unicode(UCS-2) 下請け
void
utf8_to_utf16be_sub(wchar_t *p_utf16,
                    const char *p_utf8,
                    int n_utf8_num,
                    bool b_big_endian)
{
    int n_utf8 = 0;
    int n_utf16 = 0;
    char c_high;
    char c_low;
    for (n_utf8 = 0; n_utf8 < n_utf8_num; ) {
        if ((p_utf8[n_utf8] & 0x80) == 0x00) { // 最上位ビット = 0
            p_utf16[n_utf16] = (p_utf8[n_utf8] & 0x7f);
            n_utf8 += 1;
        } else if ((p_utf8[n_utf8] & 0xe0) == 0xc0) { // 上位3ビット = 110
            p_utf16[n_utf16] = (p_utf8[n_utf8] & 0x1f) << 6;
            p_utf16[n_utf16] |= (p_utf8[n_utf8+1] & 0x3f);
            n_utf8 += 2;
        } else {
            p_utf16[n_utf16] = (p_utf8[n_utf8] & 0x0f) << 12;
            p_utf16[n_utf16] |= (p_utf8[n_utf8+1] & 0x3f) << 6;
            p_utf16[n_utf16] |= (p_utf8[n_utf8+2] & 0x3f);
            n_utf8 += 3;
        }
        if (!b_big_endian) {
            // リトルエンディアンにする処理
            c_high = (p_utf16[n_utf16] & 0xff00) >> 8;
            c_low = (p_utf16[n_utf16] & 0x00ff);
            p_utf16[n_utf16] = (c_low << 8) | c_high;
        }
        n_utf16 += 1;
    }
    p_utf16[n_utf16] = '\0';
}

// UTF-8 -> UTF-16(BE/LE) へ文字列のコード変換
wchar_t* // 変換後文字列へのポインタ
utf8_to_utf16be(const char* p_utf8_str, // 変換元UTF-8文字列へのポインタ
                int* n_num_out, // 変換結果のUTF-16文字数．Byte数ではない
                bool b_big_endian) // ビッグエンディアンに変換するならtrue
{
    int n_utf8_num;
    wchar_t* pUcsStr;
    n_utf8_num = strlen(p_utf8_str); // UTF-8文字列には，'\0' がない
    *n_num_out = utf8_count(p_utf8_str,
                            n_utf8_num);
    pUcsStr = (wchar_t *)calloc((*n_num_out + 1), sizeof(wchar_t));
    utf8_to_utf16be_sub(pUcsStr,
                        p_utf8_str,
                        n_utf8_num,
                        b_big_endian);
    return pUcsStr;
}

int
utf8_to_utf16_int(const char* str) {
    int* num = malloc(sizeof(int));
    wchar_t* utf16_wchar = utf8_to_utf16be(str, num, true);
    int utf16_int = (int)utf16_wchar[0];
    free(utf16_wchar);
    free(num);
    return utf16_int;
}

// メイン関数

int
main(int argc, char **argv)
{
    stbtt_fontinfo font;
    unsigned char *font_bitmap;
    int font_w = 0;
    int font_h = 0;
    float font_scale = 0.0;
    int font_baseline = 0;
    
    {
        char ttf_buffer[5000000]; // フォント情報
        int font_size = 40; // フォントサイズ
        int font_ascent = 0;
    
        FILE* fp = fopen("./mgenplus-1c-regular.ttf", "rb");
        fread(ttf_buffer, 1, 5000000, fp);
        fclose(fp);

        int offset = stbtt_GetFontOffsetForIndex((unsigned char *)ttf_buffer, 0);
        stbtt_InitFont(&font, (unsigned char *)ttf_buffer, offset);

        font_scale = stbtt_ScaleForPixelHeight(&font, font_size);
        stbtt_GetFontVMetrics(&font, &font_ascent, 0, 0);
        font_baseline = (int)(font_ascent * font_scale);
    }
    
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
        
        // 文字列を描画
        {
            char* src_str = "Hello!こんにちは！你好！";
            char dest_str[8];
            int codepoint_utf16;
            int pos_x = 0; // 文字表示のX座標
            float xpos = 0.0;
            int font_buffer_h = 128;
            int font_buffer_w = 128;
            int out_stride = 128;
            unsigned char font_buffer[128][128];
            // font_bufferのメモリを確保
            //unsigned char** font_buffer;
            //font_buffer = calloc(30, sizeof(unsigned char*));
            //for (int i = 0; i < 30; i++) {
            //    font_buffer[i] = calloc(30, sizeof(unsigned char));
            //}
            
            for (int i = 0; i < utf8strlen(src_str); i++) {
                // 文字を取得してutf16に変換
                init_str(dest_str, 8); // 取得用の変数を初期化 
                utf8char_at(dest_str, src_str, i); // 任意の位置の１文字を取得
                codepoint_utf16 = utf8_to_utf16_int(dest_str); // utf16に変換
                // font_bufferを初期化
                for (int y = 0; y < font_buffer_h; y++) {
                    for (int x = 0; x < font_buffer_w; x++) {
                        font_buffer[x][y] = 0;
                    }
                }
            
                // フォントをレンダリングする
                //
                //font_bitmap = stbtt_GetCodepointBitmap(&font, 0, font_scale, codepoint_utf16, &font_w, &font_h, 0, 0);
                //
                int font_advance = 0;
                int lsb = 0;
                int x0, y0, x1, y1 = 0;
                float x_shift = xpos - (float)floor(xpos);
                stbtt_GetCodepointHMetrics(&font, codepoint_utf16, &font_advance, &lsb);
                stbtt_GetCodepointBitmapBoxSubpixel(&font, codepoint_utf16,
                                                    font_scale, font_scale,
                                                    x_shift, 0,
                                                    &x0, &y0, &x1, &y1);
                stbtt_MakeCodepointBitmapSubpixel(&font, // info
                                                  &font_buffer[font_baseline + y0][(int)xpos + x0], // output
                                                  x1 - x0, // out_w
                                                  y1 - y0, // out_h
                                                  out_stride, // out_stride
                                                  font_scale, font_scale, x_shift, 0,
                                                  codepoint_utf16
                                                  );

                // １文字分を描画
                for (int y = 0; y < font_buffer_h; ++y) {
                    for (int x = 0; x < font_buffer_w; ++x) {
                        int color = 255 - font_buffer[y][x];
                        set_pixel_rgb(pixel_data,
                                      pos_x + x, y,
                                      color, color, color,
                                      width, height);
                    }
                }

                free(font_bitmap);
                pos_x += x1;
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