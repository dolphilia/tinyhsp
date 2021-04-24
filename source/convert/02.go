package main

import (
	"fmt"
)

func main() {
	mapEx := make(map[string]string) //マップの宣言

	// 2次元連想配列
	test2 := make(map[string]map[string]int)
	test2["a"] = make(map[string]int)

	fmt.Println(mapEx) //=> map[] //宣言された空のマップ

	mapEx["firstName"] = "Mike" //マップにkeyとvalueを挿入する。
	mapEx["lastName"] = "Smith"

	fmt.Println(mapEx) //=> map[lastName:Smith firstName:Mike]
}
