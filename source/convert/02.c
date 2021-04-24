/*
 * linklist.c : 連結リスト
 *
 *              Copyright (C) 2015 Makoto Hiroi
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// セル
typedef struct cell {
  int item;
  struct cell *next;
} Cell;

// リスト
typedef struct {
  Cell *top;
} List;

// コンストラクタ
Cell *make_cell(int val, Cell *cp)
{
  Cell *newcp = malloc(sizeof(Cell));
  if (newcp != NULL) {
    newcp->item = val;
    newcp->next = cp;
  }
  return newcp;
}

List *make_list(void)
{
  List *ls = malloc(sizeof(List));
  if (ls != NULL) {
    ls->top = make_cell(0, NULL);  // ヘッダセルをセット
    if (ls->top == NULL) {
      free(ls);
      return NULL;
    }
  }
  return ls;
}

// 解放
void delete_cell(Cell *cp)
{
  while (cp != NULL) {
    Cell *temp = cp->next;
    free(cp);
    cp = temp;
  }
}

void delete_list(List *ls)
{
  delete_cell(ls->top);
  free(ls);
}

// n 番目のセルを返す
Cell *nth_cell(Cell *cp, int n)
{
  for (int i = -1; cp != NULL; i++, cp = cp->next)
    if (i == n) break;
  return cp;
}

// n 番目の要素を返す
int nth(List *ls, int n, bool *err)
{
  Cell *cp = nth_cell(ls->top, n);
  if (cp == NULL) {
    *err = false;
    return 0;
  }
  *err = true;
  return cp->item;
}

// n 番目に x を挿入
bool insert_nth(List *ls, int n, int x)
{
  Cell *cp = nth_cell(ls->top, n - 1);
  if (cp == NULL) return false;
  cp->next = make_cell(x, cp->next);
  return true;
}

// n 番目の要素を削除
bool delete_nth(List *ls, int n)
{
  Cell *cp = nth_cell(ls->top, n - 1);
  if (cp == NULL || cp->next == NULL) return false;
  Cell *temp = cp->next;
  cp->next = cp->next->next;
  free(temp);
  return true;
}

// 先頭に追加
bool push(List *ls, int x)
{
  return insert_nth(ls, 0, x);
}

// 先頭から要素を取り出す
int pop(List *ls, bool *err)
{
  int x = nth(ls, 0, err);
  if (*err) delete_nth(ls, 0);
  return x;
}

// リストは空か
bool empty_list(List *ls)
{
  return ls->top->next == NULL;
}

// リストの表示
void print_list(List *ls)
{
  printf("( ");
  for (Cell *cp = ls->top->next; cp != NULL; cp = cp->next)
    printf("%d ", cp->item);
  printf(")\n");
}

int main(void)
{
  List *ls = make_list();
  bool err;
  for (int i = 0; i < 8; i++) {
    push(ls, i + 10);
    print_list(ls);
  }
  insert_nth(ls, 3, 100);
  print_list(ls);
  insert_nth(ls, 9, 200);
  print_list(ls);
  for (int i = 0; i < 11; i++) {
    int x = nth(ls, i, &err);
    printf("%d, %d\n", x, err);
  }
  delete_nth(ls, 0);
  print_list(ls);
  delete_nth(ls, 5);
  print_list(ls);
  delete_nth(ls, 7);
  print_list(ls);
  while (!empty_list(ls)) {
    int x = pop(ls, &err);
    printf("%d, %d\n", x, err);
    print_list(ls);
  }
  delete_list(ls);
  return 0;
}