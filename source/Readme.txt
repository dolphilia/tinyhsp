# �R���p�C�����@
MinGW�̏ꍇ:

�R���\�[����:
gcc tinyhsp.c -o tinyhsp_cui

�W����:
gcc tinyhsp.c -o tinyhsp_std -lopengl32 -lglfw3dll -mwindows

�g����:
gcc -c tinyhsp.c stb_vorbis.c
gcc tinyhsp.o stb_vorbis.o -o tinyhsp_ext -lopengl32 -lglfw3dll -lopenal32 -mwindows

---

TinyHSP�͈ȉ��̃��C�u�������g�p���Ă��܂��B

GLFW3
http://www.glfw.org/

OpenAL
http://www.openal.org/

exrd / neteruhsp
https://github.com/exrd/neteruhsp

kikeroga3/tinyhsp
https://github.com/kikeroga3/tinyhsp

nothings / stb
https://github.com/nothings/stb

M+ FONTS
http://mplus-fonts.osdn.jp/

Mgen+
http://jikasei.me/font/mgenplus/