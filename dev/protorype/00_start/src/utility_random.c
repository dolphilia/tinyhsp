#include "utility_random.h"

unsigned long
xor128()
{
    static unsigned long x = 123456789,
        y = 362436069,
        z = 521288629,
        w = 88675123;
    unsigned long t;
    t = (x ^ (x << 11));
    x = y;
    y = z;
    z = w;
  return (w = (w ^ (w >> 19)) ^ (t ^ (t >> 8)));
}

unsigned long
random_ul_range(unsigned long _min, unsigned long _max)
{
    return (xor128() % (_max - _min + 1) + _min);
}

int
rand_xor128(int min_value, int max_value)
{
  if (min_value < 0) {
    unsigned long ul = random_ul_range(0, (unsigned long)(max_value + (-1) * min_value));
    return (int)(ul) + min_value;
  } else {
    return random_ul_range((unsigned long)(min_value), (unsigned long)(max_value));
  }
}