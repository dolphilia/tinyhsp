# coding: UTF-8

# グローバルな擬似構造体
_g = {
    'index': 0,
    'dict': {}
}

# セル
def new_cell(item = None, next = None):
    global _g
    _g['dict'].update({
        _g['index'] : { 
            'type': 'cell',
            'item': item, # int
            'next': next, # *cell
        },
    })
    _g['index'] += 1
    return _g['index'] - 1

# リスト
def new_list(top = None):
    global _g
    _g['dict'].update({
        _g['index'] : { 
            'type': 'list',
            'top': top, # *cell
        },
    })
    _g['index'] += 1
    return _g['index'] - 1

# セルの生成
def make_cell(item, next):
    global _g
    res = new_cell()
    _g['dict'][res]["item"] = item
    _g['dict'][res]["next"] = next
    return res

# リストの生成
def make_list():
    global _g
    res = new_list()
    _g['dict'][res]["top"] = make_cell(0, None) # ヘッダセルをセット
    return res

# セルの削除
def delete_cell(cell):
    global _g
    while cell != None:
        tmp = _g['dict'][cell]['next']
        del _g['dict'][cell]
        cell = tmp

# リストの削除
def delete_list(list):
    global _g
    delete_cell(_g['dict'][list]['top'])
    del _g['dict'][list]

# n 番目のセルを返す
def nth_cell(cell, n):
    global _g
    i = -1
    while cell != None:
        if i == n:
            break
        cell = _g['dict'][cell]['next']
        i += 1
    return cell

def nth(list, n):
    global _g
    cell = nth_cell(_g['dict'][list]['top'], n)
    if cell == None:
        return None
    return _g['dict'][cell]['item']

def insert_nth(list, n, x):
    global _g
    cell = nth_cell(_g['dict'][list]['top'], n - 1)
    if cell == None:
        return False
    _g['dict'][cell]['next'] = make_cell(x, _g['dict'][cell]['next'])
    return True

# 先頭に追加
def push(list, x):
    return insert_nth(list, 0, x)

# n 番目の要素を削除
def delete_nth(list, n):
    global _g
    cell = nth_cell(_g['dict'][list]['top'], n - 1)
    if cell == None or _g['dict'][cell]['next'] == None:
        return False
    tmp = _g['dict'][cell]['next']
    _g['dict'][cell]['next'] = _g['dict'][tmp]['next']
    return True

# 先頭から要素を取り出す
def pop(list):
  x = nth(list, 0)
  delete_nth(list, 0)
  return x

# リストは空か
def empty_list(list):
    global _g
    tmp = _g['dict'][list]['top']
    res = _g['dict'][tmp]['next'] == None
    return res

# リストの表示
def print_list(list):
    global _g
    mes = "("
    tmp = _g['dict'][list]['top']
    cell = _g['dict'][tmp]['next']
    while cell != None:
        mes += " " + str(_g['dict'][cell]['item'])
        cell = _g['dict'][cell]['next']
    mes += ")"
    print(mes)

def main():
    ls = make_list()
    print(ls)
    for i in range(8):
        push(ls, i+10)
        print_list(ls)
    insert_nth(ls, 3, 100)
    print_list(ls)
    insert_nth(ls, 9, 200)
    print_list(ls)
    for i in range(11):
        x = nth(ls, i)
        print(x)
    delete_nth(ls, 0)
    print_list(ls)
    delete_nth(ls, 5)
    print_list(ls)
    delete_nth(ls, 7)
    print_list(ls)
    while empty_list(ls) == False:
        x = pop(ls)
        print(x)
        print_list(ls)
    delete_list(ls)


if __name__ == '__main__':
    main()