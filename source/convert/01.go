package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

// キーワード
type keyword_tag int

const (
	KEYWORD_END keyword_tag = iota
	KEYWORD_RETURN
	KEYWORD_GOTO
	KEYWORD_GOSUB
	KEYWORD_REPEAT
	KEYWORD_LOOP
	KEYWORD_CONTINUE
	KEYWORD_BREAK
	KEYWORD_IF
	KEYWORD_ELSE
	MAX_KEYWORD
)

// トークナイザ
type token_tag int

const (
	TOKEN_UNKNOWN token_tag = iota - 1
	TOKEN_EOF
	TOKEN_EOL
	TOKEN_EOS
	TOKEN_LBRACE
	TOKEN_RBRACE
	TOKEN_LPARENTHESIS
	TOKEN_RPARENTHESIS
	TOKEN_COMMA
	TOKEN_INTEGER
	TOKEN_REAL
	TOKEN_STRING
	TOKEN_OP_BOR
	TOKEN_OP_BAND
	TOKEN_OP_EQ
	TOKEN_OP_NEQ
	TOKEN_OP_GT
	TOKEN_OP_GTOE
	TOKEN_OP_LT
	TOKEN_OP_LTOE
	TOKEN_OP_ADD
	TOKEN_OP_SUB
	TOKEN_OP_MUL
	TOKEN_OP_DIV
	TOKEN_OP_MOD
	TOKEN_ASSIGN
	TOKEN_IDENTIFIER
	MAX_TOKEN
)

// パーサ
type node_tag int

const (
	NODE_EMPTY node_tag = iota
	NODE_LABEL
	NODE_BLOCK_STATEMENTS
	NODE_COMMAND
	NODE_ARGUMENTS
	NODE_ASSIGN
	NODE_VARIABLE
	NODE_EXPRESSION
	NODE_BOR
	NODE_BAND
	NODE_EQ
	NODE_NEQ
	NODE_GT
	NODE_GTOE
	NODE_LT
	NODE_LTOE
	NODE_ADD
	NODE_SUB
	NODE_MUL
	NODE_DIV
	NODE_MOD
	NODE_UNARY_MINUS
	NODE_PRIMITIVE_VALUE
	NODE_IDENTIFIER_EXPR
	NODE_END
	NODE_RETURN
	NODE_GOTO
	NODE_GOSUB
	NODE_REPEAT
	NODE_REPEAT_CHECK
	NODE_LOOP
	NODE_CONTINUE
	NODE_BREAK
	NODE_IF
	NODE_IF_DISPATCHER
	NODE_IF_CHECK
	NODE_JUMP_LABEL
	NODE_JUMP_INTERNAL
	MAX_NODE
)

type ast_node_flag_tag int

const (
	NODE_FLAG_ADDITIONAL = iota + 1
)

// 変数
type value_tag int

const (
	VALUE_NONE value_tag = iota
	VALUE_INT
	VALUE_DOUBLE
	VALUE_STRING
	VALUE_VARIABLE
)

// システム変数
type sysvar_tag int

const (
	SYSVAR_CNT sysvar_tag = iota
	SYSVAR_STAT
	SYSVAR_REFDVAL
	SYSVAR_REFSTR
	SYSVAR_STRSIZE
	MAX_SYSVAR
)

// 構造体
type void_value_t struct {
	value_label    *label_node_t
	value_token    *token_t
	value_ast      *ast_node_t
	value_variable *variable_t
	value_parse    *parse_context_t
	value_list     *list_t
	value_void     interface{}
}

type list_node_t struct {
	prev_  *list_node_t
	next_  *list_node_t
	value_ *void_value_t //*void
}

type list_t struct {
	head_ *list_node_t
	tail_ *list_node_t
}

type token_t struct {
	tag_          token_tag
	content_      string //*char
	cursor_begin_ int
	cursor_end_   int
	appear_line_  int
	left_space_   bool
	right_space_  bool
}

type tokenize_context_t struct {
	script_    string //const
	cursor_    int
	line_      int
	line_head_ string //const
}

type ast_node_t struct {
	tag_   node_tag
	token_ *token_t
	left_  *ast_node_t
	right_ *ast_node_t
	flag_  uint
	ext_   interface{} //*void
}

type parse_context_t struct {
	token_list_       *list_t
	token_current_    *list_node_t
	tokenize_context_ *tokenize_context_t
}

type value_t_ struct{}

type variable_t struct {
	name_         string
	type_         value_tag
	granule_size_ int
	length_       int
	data_         interface{} //*void
}

// 値（即値）
type value_t struct {
	type_ value_tag
	// union {
	ivalue_ int
	dvalue_ float64 //double
	svalue_ string  //char*
	// struct {
	variable_ *variable_t
	index_    int
	// }
	value_ uint64
	//}
}

// スタック
type value_stack_t struct {
	stack_ **value_t
	top_   int
	max_   int
}

// 実行環境
type label_node_t struct {
	name_      string //char*
	statement_ *list_node_t
}

type call_frame_t struct {
	caller_ *list_node_t
}

type loop_frame_t struct {
	start_   list_node_t
	counter_ int
	max_     int
	cnt_     int
}

type execute_environment_t struct {
	parser_list_    *list_t
	ast_list_       *list_t
	statement_list_ *list_t
	label_table_    *list_t
	variable_table_ *list_t
}

const (
	MAX_CALL_FRAME = 16
	MAX_LOOP_FRAME = 16
)

type execute_status_t struct {
	stack_              *value_stack_t
	node_cur_           *list_node_t
	call_frame_         [MAX_CALL_FRAME]call_frame_t
	current_call_frame_ int
	loop_frame_         [MAX_LOOP_FRAME]loop_frame_t
	current_loop_frame_ int
	is_end_             bool
	stat_               int
	refdval_            float64
	refstr_             string //char*
	strsize_            int
}

// ビルトイン
type command_delegate func(e *execute_environment_t, s *execute_status_t, arg_num int)
type builtin_command_tag int

const (
	COMMAND_DEVTERM builtin_command_tag = iota // デバッグ用の隠し
	COMMAND_DIM
	COMMAND_DDIM
	COMMAND_SDIM
	COMMAND_RANDOMIZE
	COMMAND_BLOAD
	COMMAND_POKE
	COMMAND_INPUT
	COMMAND_MES
	MAX_COMMAND
)

type function_delegate func(e *execute_environment_t, s *execute_status_t, arg_num int)
type builtin_function_tag int

const (
	FUNCTION_INT builtin_function_tag = iota
	FUNCTION_DOUBLE
	FUNCTION_STR
	FUNCTION_RND
	FUNCTION_ABS
	FUNCTION_POWF
	FUNCTION_PEEK
	MAX_FUNCTION
)

// リスト
func create_list_node() *list_node_t {
	var res *list_node_t = new(list_node_t)
	res.prev_ = nil
	res.next_ = nil
	res.value_ = nil
	return res
}

func destroy_list_node(node *list_node_t) {
	unlink_list_node(node)
	node = nil //free(node);
}

func link_next(node *list_node_t, list *list_node_t) {
	if node.prev_ != nil || node.next_ != nil { //assert
		fmt.Fprintln(os.Stderr, "error")
		os.Exit(1)
	}
	node.prev_ = list
	node.next_ = list.next_
	list.next_ = node
}

func link_prev(node *list_node_t, list *list_node_t) {
	if node.prev_ != nil || node.next_ != nil { //assert
		fmt.Fprintln(os.Stderr, "error")
		os.Exit(1)
	}
	node.prev_ = list.prev_
	node.next_ = list
	list.prev_ = node
}

func unlink_list_node(node *list_node_t) bool {
	if node.prev_ == nil && node.next_ == nil {
		return false
	}
	if node.prev_ != nil {
		node.prev_.next_ = node.next_
	}
	if node.next_ != nil {
		node.next_.prev_ = node.prev_
	}
	node.prev_ = nil
	node.next_ = nil
	return true
}

func create_list() *list_t {
	var res *list_t = new(list_t)
	res.head_ = nil
	res.tail_ = nil
	return res
}

func destroy_list(list *list_t) {
	list = nil //free(list)
}

func list_prepend(list *list_t, node *list_node_t) {
	if list.head_ == nil {
		if list.tail_ != nil { //assert
			fmt.Fprintln(os.Stderr, "error")
			os.Exit(1)
		}
		list.head_ = node
		list.tail_ = node
		return
	}
	link_prev(node, list.head_)
	list.head_ = node
}

func list_append(list *list_t, node *list_node_t) {
	if list.tail_ == nil {
		if list.head_ != nil { //assert
			fmt.Fprintln(os.Stderr, "error")
			os.Exit(1)
		}
		list.head_ = node
		list.tail_ = node
		return
	}
	link_next(node, list.tail_)
	list.tail_ = node
}

func list_erase(list *list_t, node *list_node_t) {
	if list.head_ == node {
		list.head_ = node.next_
	}
	if list.tail_ == node {
		list.tail_ = node.prev_
	}
	unlink_list_node(node)
}

func list_find(list *list_t, value interface{}) *list_node_t { //*void
	var node *list_node_t = list.head_
	for node != nil {
		if node.value_ == value {
			return node
		}
		node = node.next_
	}
	return nil
}

func list_free_all(list *list_t) {
	var node *list_node_t = list.head_
	for node != nil {
		var next *list_node_t = node.next_
		list_erase(list, node)
		node = nil //free(node);
		node = next
	}
}

// 文字列
func create_string(len int) *string { //size_t
	var res = new(string)
	return res
}

func create_string2(s string, len int) string { // const char* , size_t
	return s
}

func create_string3(s string) string { //const char* -> char*
	return s
}

func destroy_string(s *string) {
	s = nil //free(s);
}

func create_string_from(v int) string {
	return strconv.Itoa(v)
}

func create_string_from2(v float64) string {
	return strconv.FormatFloat(v, 'f', -1, 64)
}

func tol(c string) string {
	return strings.ToLower(c)
}

func string_equal_igcase(sl string, r string, len int /* = -1*/) bool { //※ 引数の初期値
	return sl == r
}

// 値
func clear_value(t *value_t) {
	switch t.type_ {
	case VALUE_STRING:
		destroy_string(&t.svalue_)
		break
	default:
		break
	}
}

// 実行環境ユーティリティ
func search_label(e *execute_environment_t, name string) *list_node_t {
	var node *list_node_t = e.label_table_.head_
	for node != nil {
		var label *label_node_t = node.value_.value_label
		if string_equal_igcase(label.name_, name, -1) {
			return label.statement_
		}
		node = node.next_
	}
	return nil
}

type keyword_t struct {
	tag_  keyword_tag
	word_ string
}

type keywords_t []*keyword_t

func set_keyword(t *keyword_t, tag_ keyword_tag, word_ string) {
	t.tag_ = tag_
	t.word_ = word_
}

// キーワード
func query_keyword(s string) keyword_tag {
	var table keywords_t
	set_keyword(table[0], KEYWORD_END, "end")
	set_keyword(table[1], KEYWORD_END, "end")
	set_keyword(table[2], KEYWORD_RETURN, "return")
	set_keyword(table[3], KEYWORD_GOTO, "goto")
	set_keyword(table[4], KEYWORD_GOSUB, "gosub")
	set_keyword(table[5], KEYWORD_REPEAT, "repeat")
	set_keyword(table[6], KEYWORD_LOOP, "loop")
	set_keyword(table[7], KEYWORD_CONTINUE, "continue")
	set_keyword(table[8], KEYWORD_BREAK, "break")
	set_keyword(table[9], KEYWORD_IF, "if")
	set_keyword(table[10], KEYWORD_ELSE, "else")
	set_keyword(table[11], -1, "")
	// 全探索
	for i := 0; table[i].tag_ != -1; i++ {
		if string_equal_igcase(s, table[i].word_, -1) {
			return table[i].tag_
		}
	}
	return -1
}

func main() {
	var l *list_node_t = create_list_node()
	l.next_ = nil
	fmt.Println("Finish!")
}
