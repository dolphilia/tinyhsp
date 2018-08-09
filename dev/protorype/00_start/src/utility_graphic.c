#include "utility_graphic.h"

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
    int index = point_y * canvas_size_width * 3 + point_x * 3;
    pixel_data[index] = color_red;
    pixel_data[index+1] = color_green;
    pixel_data[index+2] = color_blue;
}