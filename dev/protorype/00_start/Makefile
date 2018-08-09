#
# Makefile for TinyHSP
#

# コンパイラの設定
COMPILER = clang
#COMPILER = gcc
# コンパイルオプション
CFLAGS   = -Wall -O2
#CFLAGS   = -Wall -O2 -std=c99
# リンク
LDFLAGS  = -lglfw -framework OpenGL
#LDFLAGS  = -lm -ldl -lglfw3 -lGL -lX11 -lXxf86vm -lXrandr -lXinerama -lXcursor -lpthread -lXi
# ライブラリ
LIBS     =
# インクルード
INCLUDE  =

# ソースの拡張子
SRC_EXT  = .c
# オブジェクトの拡張子
OBJ_EXT  = .o

# 出力ファイル
TARGET   = ./bin/tinyhsp
# ソースのディレクトリ
SRC_DIR  = ./src
# オブジェクトのディレクトリ
OBJ_DIR  = ./obj

# ソースを探索（全てコンパイル）
SOURCES  = $(wildcard $(SRC_DIR)/*$(SRC_EXT))
# ソースに対応するオブジェクトファイル名を設定
OBJECTS  = $(addprefix $(OBJ_DIR)/, $(notdir $(SOURCES:%$(SRC_EXT)=%$(OBJ_EXT))))

# ターゲットをビルド
$(TARGET): $(OBJECTS) $(LIBS)
	$(COMPILER) -o $@ $^ $(LDFLAGS)
	rm -f $(OBJECTS)

# 各種ソースをコンパイル
$(OBJ_DIR)/%$(OBJ_EXT): $(SRC_DIR)/%$(SRC_EXT)
	$(COMPILER) $(CFLAGS) $(INCLUDE) -o $@ -c $<

all: clean $(TARGET)

clean:
	rm -f $(OBJECTS) $(TARGET)
