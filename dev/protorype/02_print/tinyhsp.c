#include <stdio.h>
#include <string.h>

int
main(int argc, char* argv[])
{
    // 変数の初期化
    char script[1024][1024]; // スクリプト格納用の配列
    int line_number_max = 0; // スクリプトの行数
    
    // ファイルから配列にスクリプトを格納する
    {
        FILE* fp;
        // ファイル名を特定してオープンする
        {
            char* file_name;
            // ファイル名を設定する
            if (argc >= 2) {
    	        file_name = argv[1];
            } else {
    	        file_name = "./start.hsp";
            }
            // ファイルをオープンする
            fp = fopen(file_name, "r"); // エラー処理は省く
        }
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
    
    // スクリプトを実行する
    for (int i = 0; i < line_number_max; i++) {
        if (script[i][0] == '\0') {
            continue;
        }
        if (strcmp(script[i], "print") == 0) {
            printf("%s\n", script[i + 1]);
            i++;
        }
    }
    
    return 0;
}