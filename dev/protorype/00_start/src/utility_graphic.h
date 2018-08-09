#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void set_pixel_rgb(uint8_t *pixel_data,
                   int32_t point_x, int32_t point_y,
                   uint8_t color_red, uint8_t color_green, uint8_t color_blue,
                   int32_t canvas_size_width, int32_t canvas_size_height);