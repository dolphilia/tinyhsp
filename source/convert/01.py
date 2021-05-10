# coding: UTF-8
import sys
from enum import Enum
import pprint

# キーワード
class keyword_tag(Enum):
    KEYWORD_END = 0
    KEYWORD_RETURN = 1
    KEYWORD_GOTO = 2
    KEYWORD_GOSUB = 3
    KEYWORD_REPEAT = 4
    KEYWORD_LOOP = 5
    KEYWORD_CONTINUE = 6
    KEYWORD_BREAK = 7
    KEYWORD_IF = 8
    KEYWORD_ELSE = 9
    MAX_KEYWORD = 10

# トークナイザ
class token_tag(Enum):
	TOKEN_UNKNOWN  = -1
	TOKEN_EOF = 0
	TOKEN_EOL = 1
	TOKEN_EOS = 2
	TOKEN_LBRACE = 3
	TOKEN_RBRACE = 4
	TOKEN_LPARENTHESIS = 5
	TOKEN_RPARENTHESIS = 6
	TOKEN_COMMA = 7
	TOKEN_INTEGER = 8
	TOKEN_REAL = 9
	TOKEN_STRING = 10
	TOKEN_OP_BOR = 11
	TOKEN_OP_BAND = 12
	TOKEN_OP_EQ = 13
	TOKEN_OP_NEQ = 14
	TOKEN_OP_GT = 15
	TOKEN_OP_GTOE = 16
	TOKEN_OP_LT = 17
	TOKEN_OP_LTOE = 18
	TOKEN_OP_ADD = 19
	TOKEN_OP_SUB = 20
	TOKEN_OP_MUL = 21
	TOKEN_OP_DIV = 22
	TOKEN_OP_MOD = 23
	TOKEN_ASSIGN = 24
	TOKEN_IDENTIFIER = 25
	MAX_TOKEN = 26

# パーサ
class node_tag(Enum):
	NODE_EMPTY = 0
	NODE_LABEL = 1
	NODE_BLOCK_STATEMENTS = 2
	NODE_COMMAND = 3
	NODE_ARGUMENTS = 4
	NODE_ASSIGN = 5
	NODE_VARIABLE = 6
	NODE_EXPRESSION = 7
	NODE_BOR = 8
	NODE_BAND = 9
	NODE_EQ = 10
	NODE_NEQ = 11
	NODE_GT = 12
	NODE_GTOE = 13
	NODE_LT = 14
	NODE_LTOE = 15
	NODE_ADD = 16
	NODE_SUB = 17
	NODE_MUL = 18
	NODE_DIV = 19
	NODE_MOD = 20
	NODE_UNARY_MINUS = 21
	NODE_PRIMITIVE_VALUE = 22
	NODE_IDENTIFIER_EXPR = 23
	NODE_END = 24
	NODE_RETURN = 25
	NODE_GOTO = 26
	NODE_GOSUB = 27
	NODE_REPEAT = 28
	NODE_REPEAT_CHECK = 29
	NODE_LOOP = 30
	NODE_CONTINUE = 31
	NODE_BREAK = 32
	NODE_IF = 33
	NODE_IF_DISPATCHER = 34
	NODE_IF_CHECK = 35
	NODE_JUMP_LABEL = 36
	NODE_JUMP_INTERNAL = 37
	MAX_NODE = 38

class ast_node_flag_tag(Enum):
	NODE_FLAG_ADDITIONAL = 1

# 変数
class value_tag(Enum):
	VALUE_NONE = 0
	VALUE_INT = 1
	VALUE_DOUBLE = 2
	VALUE_STRING = 3
	VALUE_VARIABLE = 4

# システム変数
class sysvar_tag(Enum):
	SYSVAR_CNT = 0
	SYSVAR_STAT = 1
	SYSVAR_REFDVAL = 2
	SYSVAR_REFSTR = 3
	SYSVAR_STRSIZE = 4
	MAX_SYSVAR = 5

# コマンド
class builtin_command_tag(Enum):
	COMMAND_DEVTERM  = 0 # デバッグ用の隠し
	COMMAND_DIM = 1
	COMMAND_DDIM = 2
	COMMAND_SDIM = 3
	COMMAND_RANDOMIZE = 4
	COMMAND_BLOAD = 5
	COMMAND_POKE = 6
	COMMAND_INPUT = 7
	COMMAND_MES = 8
	MAX_COMMAND = 9

class builtin_function_tag(Enum):
	FUNCTION_INT  = 0
	FUNCTION_DOUBLE = 1
	FUNCTION_STR = 2
	FUNCTION_RND = 3
	FUNCTION_ABS = 4
	FUNCTION_POWF = 5
	FUNCTION_PEEK = 6
	MAX_FUNCTION = 7

# 定数
MAX_CALL_FRAME = 16
MAX_LOOP_FRAME = 16

# グローバルな擬似メモリ
class Global:
    pass

_g = Global()
_g.index = 0
_g.dict = {}

# _g = {
#     'index': 0,
#     'dict': {},
#     'keyword': [],
# }

def new_char_t(content_ = None):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'char_t',
            'content_': content_,
        },
    })
    _g.index += 1
    return _g.index - 1

def new_data_t(content_ = None):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'data_t',
            'content_': content_,
        },
    })
    _g.index += 1
    return _g.index - 1

def new_list_node_t(prev_ = None, next_ = None, value_ = None):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'list_node_t',
            'prev_': prev_, # *list_node_t
            'next_': next_, # *list_node_t
            'value_': value_, # *void
        },
    })
    _g.index += 1
    return _g.index - 1

def new_list_t(head_ = None, tail_ = None):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'list_t',
            'head_': head_, # *list_node_t
            'tail_': tail_,  # *list_node_t
        },
    })
    _g.index += 1
    return _g.index - 1

def new_token_t(tag_ = 0, content_ = '', cursor_begin_ = 0, cursor_end_ = 0, appear_line_ = 0, left_space_ = None, right_space_ = None):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'token_t',
            'tag_': tag_, # token_tag
            'content_': content_, # string //*char
            'cursor_begin_': cursor_begin_, #int
            'cursor_end_': cursor_end_, #int
            'appear_line_': appear_line_, #int
            'left_space_': left_space_, #bool
            'right_space_': right_space_, #bool
        },
    })
    _g.index += 1
    return _g.index - 1

def new_tokenize_context_t(script_ = '', cursor_ = 0, line_ = 0, line_head_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'tokenize_context_t', # stract
            'script_': script_, # string //const
	        'cursor_': cursor_, # int
	        'line_': line_, # int
	        'line_head_': line_head_, # string //const
        },
    })
    _g.index += 1
    return _g.index - 1

def new_ast_node_t(tag_ = 0, token_ = 0, left_ = 0, right_ = 0, flag_ = 0, ext_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'ast_node_t',
            'tag_': tag_, # node_tag
            'token_': token_, # *token_t
            'left_': left_, # *ast_node_t
            'right_': right_, # *ast_node_t
            'flag_': flag_, # uint
            'ext_': ext_, # *void
        },
    })
    _g.index += 1
    return _g.index - 1

def new_parse_context_t():
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'parse_context_t',
            'token_list_': 0, # *list_t
            'token_current_': 0, # *list_node_t
            'tokenize_context_': 0, # *tokenize_context_t
        },
    })
    _g.index += 1
    return _g.index - 1

def new_value_t_(value_t_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'value_t_',
            'value_t_': value_t_,
        },
    })
    _g.index += 1
    return _g.index - 1

def new_variable_t(name_ = '', type_ = 0, granule_size_ = 0, length_ = 0, data_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'variable_t',
            'name_': name_, # string
            'type_': type_, # value_tag
            'granule_size_': granule_size_, # int
            'length_': length_, #int
            'data_': data_, #*void
        },
    })
    _g.index += 1
    return _g.index - 1

def new_value_t(type_ = 0, ivalue_ = 0, dvalue_ = 0.0, svalue_ = '', variable_ = 0, index_ = 0, value_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'value_t',
            'type_': type_, #value_tag
            'union': {
                'ivalue_': ivalue_, # int
                'dvalue_': dvalue_, # float64 //double
                'svalue_': svalue_, # string  //char*
                'struct': {
                    'variable_': variable_, #*variable_t
                    'index_': index_, #int
                },
                'value_' : value_, #uint64
            },
        },
    })
    _g.index += 1
    return _g.index - 1

def new_value_stack_t(stack_ = 0, top_ = 0, max_ = 0):
    global _g
    _g.dict.update({
        _g.index : {
            'type': 'value_stack_t',
            'stack_': [], #**value_t
            'top_': top_, #int
            'max_': max_, #int
        },
    })
    _g.index += 1
    return _g.index - 1

def new_label_node_t(name_ = '', statements_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'label_node_t',
            'name_': name_, #string //char*
            'statement_': statements_, #*list_node_t
        },
    })
    _g.index += 1
    return _g.index - 1

def new_call_frame_t(caller_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'call_frame_t',
            'caller_': caller_, #*list_node_t
        },
    })
    _g.index += 1
    return _g.index - 1

def new_loop_frame_t(start_ = 0, counter_ = 0, max_ = 0, cnt_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'loop_frame_t',
            'start_': 0, #list_node_t
            'counter_': 0, # int
            'max_': 0, #int
            'cnt_': 0, #int
        },
    })
    _g.index += 1
    return _g.index - 1

def new_execute_environment_t(parser_list_ = 0, ast_list_ = 0, statement_list_ = 0, label_table_ = 0, variable_table_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type': 'execute_environment_t',
            'parser_list_': parser_list_, # *list_t
            'ast_list_': ast_list_, # *list_t
            'statement_list_': statement_list_, # *list_t
            'label_table_': label_table_, # *list_t
            'variable_table_': variable_table_, # *list_t
        },
    })
    _g.index += 1
    return _g.index - 1

def new_execute_status_t(stack_ = 0, node_cur_ = 0, call_frame_ = [], current_call_frame_ = 0, loop_frame_ = [], current_loop_frame_ = 0, is_end_ = None, stat_ = 0, refdval_ = 0, refstr_ = 0, strsize_ = 0):
    global _g
    _g.dict.update({
        _g.index : { 
            'type':'execute_status_t' ,
            'stack_': stack_, #              *value_stack_t
            'node_cur_': node_cur_, #           *list_node_t
            'call_frame_': call_frame_, #         [MAX_CALL_FRAME]call_frame_t
            'current_call_frame_': current_call_frame_, # int
            'loop_frame_ ': loop_frame_, #        [MAX_LOOP_FRAME]loop_frame_t
            'current_loop_frame_': current_loop_frame_, # int
            'is_end_': is_end_, #             bool
            'stat_': stat_, #               int
            'refdval_': refdval_, #            float64
            'refstr_': refstr_, #             string //char*
            'strsize_': strsize_, #            int
        },
    })
    _g.index += 1
    return _g.index - 1

# ビルトイン
def command_devterm(e, s, arg_num): #execute_environment_t* , execute_status_t* , int
    pass
def command_dim(e, s, arg_num):
    pass
def dommand_ddim(e, s, arg_num):
    pass
def command_sdim(e, s, arg_num):
    pass
def command_randomize(e, s, arg_num):
    pass
def command_bload(e, s, arg_num):
    pass
def command_poke(e, s, arg_num):
    pass
def command_input(e, s, arg_num):
    pass
def command_mes(e, s, arg_num):
    pass

command_delegate = [
    command_devterm,
    command_dim,
    dommand_ddim,
    command_sdim,
    command_randomize,
    command_bload,
    command_poke,
    command_input,
    command_mes,
]

def function_int(e, s, arg_num):
    pass
def function_double(e, s, arg_num):
    pass
def function_str(e, s, arg_num):
    pass
def function_rnd(e, s, arg_num):
    pass
def function_abs(e, s, arg_num):
    pass
def function_powf(e, s, arg_num):
    pass
def function_peek(e, s, arg_num):
    pass

function_delegate = [
    function_int,
    function_double,
    function_str,
    function_rnd,
    function_abs,
    function_powf,
    function_peek,
]

# リスト
def create_list_node():
    global _g
    res = new_list_node_t()
    _g.dict[res]['prev_'] = None
    _g.dict[res]['next_'] = None
    _g.dict[res]['value_'] = None
    return res

def unlink_list_node(node):
    global _g
    if _g.dict[node]['prev_'] == None and _g.dict[node]['next_'] == None:
        return False
    if _g.dict[node]['prev_'] != None:
        tmp = _g.dict[node]['prev_']
        _g.dict[tmp]['next_'] = _g.dict[node]['next_']
    if _g.dict[node]['next_'] != None:
        tmp = _g.dict[node]['next_']
        _g.dict[tmp]['prev_'] = _g.dict[node]['prev_']
    node['prev_'] = None
    node['next_'] = None
    return True

def destroy_list_node(node):
    global _g
    unlink_list_node(node)
    del _g.dict[node]

def link_next(node, list):
    global _g
    if _g.dict[node]['prev_'] != None or _g.dict[node]['next_'] != None:
        sys.stdout.write('error1')
        sys.exit()
    _g.dict[node]['prev_'] = list
    _g.dict[node]['next_'] = _g.dict[list]['next_']
    _g.dict[list]['next_'] = node

def link_prev(node, list):
    global _g
    if _g.dict[node]['prev_'] != None or _g.dict[node]['next_'] != None:
        sys.stdout.write('error2')
        sys.exit()
    _g.dict[node]['prev_'] = _g.dict[list]['prev_']
    _g.dict[node]['next_'] = list
    _g.dict[list]['prev_'] = node

def create_list():
    global _g
    res = new_list_t()
    _g.dict[res]['head_'] = None
    _g.dict[res]['tail_'] = None
    return res

def destroy_list(list):
    global _g
    del _g.dict[list]

def list_prepend(list, node):
    global _g
    if _g.dict[list]['head_'] == None:
        if _g.dict[list]['tail_'] == None:
            sys.stdout.write('error3')
            sys.exit()
        _g.dict[list]['head_'] = node
        _g.dict[list]['tail_'] = node
        return
    link_prev(node, _g.dict[list]['head_'])
    _g.dict[list]['head_'] = node

def list_append(list, node):
    global _g
    if _g.dict[list]['tail_'] == None:
        if _g.dict[list]['head_'] == None:
            sys.stdout.write('リストのtail_とhead_がNoneです\n')
            #sys.exit()
        _g.dict[list]['head_'] = node
        _g.dict[list]['tail_'] = node
        return
    link_next(node, _g.dict[list]['tail_'])
    _g.dict[list]['tail_'] = node

def list_erase(list, node):
    global _g
    if _g.dict[list]['head_'] == node:
        _g.dict[list]['head_'] = _g.dict[node]['next_']
    if _g.dict[list]['tail_'] == node:
        _g.dict[list]['tail_'] = _g.dict[node]['prev_']
    unlink_list_node(node)

def list_find(list, value):
    global _g
    node = _g.dict[list]['head_']
    while node != None:
        if _g.dict[node]['value_'] == value:
            return node
        node = _g.dict[node]['nest_']

def list_free_all(list):
    global _g
    node = _g.dict[list]['head_']
    while node != None:
        next = _g.dict[node]['next_']
        list_erase(list, node)
        del _g.dict[node]
        node = next

# 文字列
def create_string(len):
	res = ''
	return res

def create_string2(s, len):
	return s

def create_string3(s):
	return s

def destroy_string(s):
	s = None

def create_string_from(v):
	return str(v)

def create_string_from2(v):
	return str(v)

def tol(c):
	return c.lower()

def string_equal_igcase(sl, r, len = None):
	return sl == r

# 値
def clear_value(t):
    global _g
    if _g.dict[t]['type_'] == value_tag.VALUE_STRING:
        destroy_string(_g.dict[t]['svalue_'])

# 実行環境ユーティリティ
def search_label(e, name):
    global _g
    tmp = _g.dict[e]['label_table_']
    node = _g.dict[tmp]['head_']
    while node != None:
        label = _g.dict[node]['value_']
        if string_equal_igcase(_g.dict[label]['name_'], name, -1):
            return _g.dict[label]['statement_']
        node = _g.dict[node]['next_']

# キーワード
def query_keyword(s):
    table = {
        keyword_tag.KEYWORD_END: "end",
        keyword_tag.KEYWORD_RETURN: "return",
        keyword_tag.KEYWORD_GOTO: "goto",
        keyword_tag.KEYWORD_GOSUB: "gosub",
        keyword_tag.KEYWORD_REPEAT: "repeat",
        keyword_tag.KEYWORD_LOOP: "loop",
        keyword_tag.KEYWORD_CONTINUE: "continue",
        keyword_tag.KEYWORD_BREAK: "break",
        keyword_tag.KEYWORD_IF: "if",
        keyword_tag.KEYWORD_ELSE: "else",
    }
	# 全探索
    for key in table:
        if string_equal_igcase(s, table[key], -1):
            return key

# トークナイザ
def query_token_shadow(c, ident, len):
    global _g
    shadows = {
        token_tag.TOKEN_OP_BAND: "and",
		token_tag.TOKEN_OP_BOR: "or",
    }
    for key in shadows:
        if string_equal_igcase(shadows[key], _g.dict[c]['script_'][ident:ident+len]):
            return key

def initialize_tokenize_context(c, script):
    global _g
    _g.dict[c]['script_'] = script
    _g.dict[c]['cursor_'] = 0
    _g.dict[c]['line_'] = 0
    _g.dict[c]['line_head_'] = 0

def uninitialize_tokenize_context(c):
    global _g
    _g.dict[c]['script_'] = None
    _g.dict[c]['cursor_'] = 0
    _g.dict[c]['line_'] = 0
    _g.dict[c]['line_head_'] = 0

def is_space(c):
    return c == ' ' or c == '\t'

def is_number(c):
	return c >= '0' and c <= '9'

def is_alpha(c):
    return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')

def is_rest_ident(c):
    return is_number(c) or is_alpha(c) or c == '_'

def get_token(c):
    global _g
    res = new_token_t()
    _g.dict[res]['tag_'] = token_tag.TOKEN_UNKNOWN
    _g.dict[res]['content_'] = None
    _g.dict[res]['cursor_begin_'] = _g.dict[c]['cursor_']
    _g.dict[res]['cursor_end_'] = _g.dict[c]['cursor_']
    _g.dict[res]['left_space_'] = False
    _g.dict[res]['right_space_'] = False
    p_tmp = _g.dict[c]['cursor_']
    p = _g.dict[c]['cursor_']
    while True: #restart:
        prev_p = p
        prev_cursor = p
        _g.dict[res]['appear_line_'] = _g.dict[c]['line_']
        goto_flag = False
        for i in range(1):
            if _g.dict[c]['script_'][p] == '\0': #EOF
                _g.dict[res]['tag_'] = token_tag.TOKEN_EOF
                # 行終わり
                break
            elif _g.dict[c]['script_'][p] == '\r' or _g.dict[c]['script_'][p] == '\f':
                p += 1
                goto_flag = True
                break
            elif _g.dict[c]['script_'][p] == '\n':
                # この位置はマーキング
                _g.dict[c]['line_'] += 1
                p += 1
                _g.dict[c]['line_head_'] = p
                _g.dict[res]['tag_'] = token_tag.TOKEN_EOL
                break
            elif _g.dict[c]['script_'][p] == ':': # ステートメント終わり
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_EOS
                break
            elif _g.dict[c]['script_'][p] == '{': # 微妙な文字
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_LBRACE
                break
            elif _g.dict[c]['script_'][p] == '}':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_RBRACE
                break
            elif _g.dict[c]['script_'][p] == '(':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_LPARENTHESIS
                break
            elif _g.dict[c]['script_'][p] == ')':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_RPARENTHESIS
                break
            elif _g.dict[c]['script_'][p] == ',':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_COMMA
                break
            elif _g.dict[c]['script_'][p] == '|': # 演算子
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_OP_BOR
                break
            elif _g.dict[c]['script_'][p] == '&':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_OP_BAND
                break
            elif _g.dict[c]['script_'][p] == '!':
                p += 1
                if _g.dict[c]['script_'][p] == '=':
                    p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_OP_NEQ
                break
            elif _g.dict[c]['script_'][p] == '>':
                p += 1
                if _g.dict[c]['script_'][p] == '=':
                    p += 1
                    _g.dict[res]['tag_'] = token_tag.TOKEN_OP_GTOE
                else:
                    _g.dict[res]['tag_'] = token_tag.TOKEN_OP_GT
                break
            elif _g.dict[c]['script_'][p] == '<':
                p += 1
                if _g.dict[c]['script_'][p] == '=':
                    p += 1
                    _g.dict[res]['tag_'] = token_tag.TOKEN_OP_LTOE
                else:
                    _g.dict[res]['tag_'] = token_tag.TOKEN_OP_LT
                break
            elif _g.dict[c]['script_'][p] == '+':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_OP_ADD
                break
            elif _g.dict[c]['script_'][p] == '-':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_OP_SUB
                break
            elif _g.dict[c]['script_'][p] == '*':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_OP_MUL
                break
            elif _g.dict[c]['script_'][p] == '/':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_OP_DIV
                break
            elif _g.dict[c]['script_'][p] == '\\':
                p += 1
                _g.dict[res]['tag_'] = token_tag.TOKEN_OP_MOD
                break
            elif _g.dict[c]['script_'][p] == '=': # 代入
                p += 1
                if _g.dict[c]['script_'][p] == '=':
                    p += 1
                    _g.dict[res]['tag_'] = token_tag.TOKEN_OP_EQ
                else:
                    _g.dict[res]['tag_'] = token_tag.TOKEN_ASSIGN
                break
            elif _g.dict[c]['script_'][p] == '\"': # 文字列
                p += 1
                s = p
                while _g.dict[c]['script_'][p]  != '\"':
                    if _g.dict[c]['script_'][p]  == '\0':
                        print("EOF detected in string.@@ %d Row", _g.dict[c]['line_'])
                        sys.exit()
                        # 文字列の読み取り中にEOFが検出されました@@ %d行目", c->line_);
                    if _g.dict[c]['script_'][p]  == '\\' and _g.dict[c]['script_'][p + 1] == '\"':
                        p += 1
                    p += 1
                e = p
                _g.dict[res]['content_'] = create_token_string(s, e - s)
                _g.dict[res]['tag_'] = token_tag.TOKEN_STRING
                p += 1
                break
            elif _g.dict[c]['script_'][p] == ';': # コメント
                p += 1
                while _g.dict[c]['script_'][p] != '\n' and _g.dict[c]['script_'][p] != '\0':
                    p += 1
                goto_flag = True
                break
            else:
                if is_space(_g.dict[c]['script_'][p]): # スペース
                    p += 1
                    _g.dict[res]['left_space_'] = True
                    while is_space(_g.dict[c]['script_'][p]):
                        p += 1
                    goto_frag = True
                    break
                elif is_number(_g.dict[c]['script_'][p]): # 数値
                    if _g.dict[c]['script_'][p] == '0':
                        p += 1
                    else:
                        while is_number(_g.dict[c]['script_'][p]):
                            p += 1
                    if _g.dict[c]['script_'][p] == '.':
                        p += 1
                        while is_number(_g.dict[c]['script_'][p]):
                            p += 1
                        _g.dict[res]['tag_'] = token_tag.TOKEN_REAL
                    else:
                        _g.dict[res]['tag_'] = token_tag.TOKEN_INTEGER
                elif is_alpha(_g.dict[c]['script_'][p]): # 何らかの識別子
                    p += 1
                    while is_rest_ident(_g.dict[c]['script_'][p]):
                        p += 1
                    _g.dict[res]['tag_'] = token_tag.TOKEN_IDENTIFIER
                    shadow = query_token_shadow(c, prev_cursor, p - prev_p)
                    if shadow != -1:
                        _g.dict[res]['tag_'] = shadow
                else: # もう読めない
                    print("Unknown character[%c]@@ %d Row", _g.dict[c]['script_'][p], _g.dict[c]['line_']) # 読み取れない文字
                    sys.exit()
                break
        if goto_flag == True:
            continue
        break

    if is_space(_g.dict[c]['script_'][p]):
        _g.dict[res]['right_space_'] = True
    _g.dict[c]['cursor_'] += p - p_tmp
    _g.dict[res]['cursor_begin_'] = prev_cursor
    _g.dict[res]['cursor_end_'] = _g.dict[c]['cursor_']
    # contentが埋まってないなら埋める
    if _g.dict[res]['content_'] == None:
        length = _g.dict[res]['cursor_end_'] - _g.dict[res]['cursor_begin_']
        index = _g.dict[res]['cursor_begin_']
        _g.dict[res]['content_'] = _g.dict[c]['script_'][index: index+length]
    return res

def destroy_token(t):
    global _g
    if _g.dict[t]['content_'] != None:
        destroy_string(_g.dict[t]['content_'])
        _g.dict[t]['content_'] = None
    del _g.dict[t]

def create_token_string(str, len):
    res = ''
    w = 0
    i = 0
    while i < len:
        if str[i] == '\\' and (i + 1) < len:
            if str[i + 1] == 't':
                res[w] = '\t'
            elif str[i + 1] == 'n':
                res[w] = '\n'
            elif str[i + 1] == '\"':
                res[w] = '\"'
            else:
                print("Unknown escape sequence@@ %c%c", str[i], str[i + 1]) # 読み取れないエスケープシーケンス
                sys.exit()
            i += 1
        else:
            res[w] = str[i]
        i += 1
        w += 1
    return res

# パーサ
def create_parse_context():
    res = new_parse_context_t()
    return res

def destroy_parse_context(p):
    global _g
    del _g.dict[p]

def initialize_parse_context(c, t):
    global _g
    _g.dict[c]['token_list_'] = create_list()
    _g.dict[c]['token_current_'] = None
    _g.dict[c]['tokenize_context_'] = t

def uninitialize_parse_context(c):
    global _g
    if _g.dict[c]['token_list_'] != None:
        tmp = _g.dict[c]['token_list_']
        iter = _g.dict[tmp]['head_']
        while iter != None:
            next = _g.dict[iter]['next_']
            token = _g.dict[iter]['value_']
            destroy_token(token)
            destroy_list_node(iter)
            iter = next
        destroy_list(_g.dict[c]['token_list_'])
    _g.dict[c]['token_list_'] = None
    _g.dict[c]['token_current_'] = None

def read_token(c):
    global _g
    if _g.dict[c]['token_current_'] == None:
        node = create_list_node()
        _g.dict[node]['value_'] = get_token(_g.dict[c]['tokenize_context_'])
        list_append(_g.dict[c]['token_list_'], node)
        _g.dict[c]['token_current_'] = node
    if _g.dict[c]['token_current_'] != None:
        sys.stdout.write('parse_context_tのtoken_current_がNoneです\n')
        #sys.exit()
    res = _g.dict[c]['token_current_']
    tmp = _g.dict[c]['token_current_']
    _g.dict[c]['token_current_'] = _g.dict[tmp]['next_']
    return _g.dict[res]['value_']

def unread_token(c, num):
    global _g
    if num <= 0:
        return
    if _g.dict[c]['token_current_'] == None:
        tmp = _g.dict[c]['token_list_']
        _g.dict[c]['token_current_'] = _g.dict[tmp]['tail_']
        num -= 1
    while num > 0:
        if _g.dict[c]['token_current_'] != None:
            sys.stdout.write('error6')
            sys.exit()
        tmp = _g.dict[c]['token_current_']
        _g.dict[c]['token_current_'] = _g.dict[tmp]['prev_']
        num -= 1

def prev_token(c, num):
    global _g
    current = _g.dict[c]['token_current_']
    if current == None:
        tmp = _g.dict[c]['token_list_']
        current = _g.dict[tmp]['tail_']
    while num > 0:
        if current != None:
            sys.stdout.write('error7')
            sys.exit()
        current = _g.dict[current]['prev_']
        num -= 1
    return _g.dict[current]['value_']

def create_ast_node(tag, left, right):
    global _g
    res = new_ast_node_t()
    _g.dict[res]['tag_'] = tag
    _g.dict[res]['token_'] = None
    _g.dict[res]['left_'] = left
    _g.dict[res]['right_'] = right
    _g.dict[res]['flag_'] = 0
    _g.dict[res]['ext_'] = None
    return res

def create_ast_node2(tag, token, left):
    global _g
    res = new_ast_node_t()
    _g.dict[res]['tag_'] = tag
    _g.dict[res]['token_'] = token
    _g.dict[res]['left_'] = left
    _g.dict[res]['right_'] = None
    _g.dict[res]['flag_'] = 0
    _g.dict[res]['ext_'] = None
    return res

def destroy_ast_node(node):
    global _g
    if node != None:
        sys.stdout.write('error8')
        sys.exit()
    if _g.dict[node]['left_'] != None:
        destroy_ast_node(_g.dict[node]['left_'])
    if _g.dict[node]['right_'] != None:
        destroy_ast_node(_g.dict[node]['right_'])
    del _g.dict[node]

def is_eos_like_token(tag):
    return tag == token_tag.TOKEN_EOF or tag == token_tag.TOKEN_EOL or tag == token_tag.TOKEN_EOS or tag == token_tag.TOKEN_RBRACE

def parse_script(c):
    global _g
    res = create_list()
    while True:
        statement = parse_statement(c)
        if statement == None:
            break
        node = create_list_node()
        _g.dict[node]['value_'] = statement
        list_append(res, node)
        token = read_token(c)
        if _g.dict[token]['tag_'] != token_tag.TOKEN_EOF:
            print("Script couldn't be parsed successfully.@@ %d Row", _g.dict[token]['appear_line_']) # スクリプトを最後まで正しくパースできませんでした
            sys.exit()
    return res

def destroy_ast(ast):
    node = _g.dict[ast]['head_']
    while node != None:
        ast_node = _g.dict[node]['value_']
        destroy_ast_node(ast_node)
        node = _g.dict[node]['next_']
    list_free_all(ast)
    destroy_list(ast)

def parse_statement(c):
    # 何もない？
    token = read_token(c)
    if _g.dict[token]['tag_'] == token_tag.TOKEN_EOF:
        return None
    if is_eos_like_token(_g.dict[token]['tag_']):
        return create_ast_node(node_tag.NODE_EMPTY, None, None)
    unread_token(c, 1)
    statement = None
    # ラベルを試す
    if statement == None:
        statement = parse_label_safe(c)
    # 制御構文を試す
    if statement == None:
        statement = parse_control_safe(c)
    # コマンドを試す
    if statement == None:
        statement = parse_command_safe(c)
    # それ以外は全て代入
    if statement == None:
        statement = parse_assign_safe(c)
    # ここまで来て何もないなら、パース不能
    if statement == None:
        token = read_token(c)
        sys.stdout.write("ステートメントが解析できません:" + str(_g.dict[token]['appear_line_']) + "行目")
        sys.exit()
        # Statement cannot be parsed
        # ステートメントが解析できません@@ %d行目", token->appear_line_);
    # 最後の改行チェック
    token = read_token(c)
    if not is_eos_like_token(_g.dict[token]['tag_']):
        print("Statement couldn't be parsed successfully.@@ %d Row", _g.dict[token]['appear_line_'])
        # ステートメントをすべて正しく解析できませんでした@@ %d行目", token->appear_line_);
        sys.exit()
    return statement

def parse_label_safe(c):
    global _g
    token = read_token(c)
    if _g.dict[token]['tag_'] != token_tag.TOKEN_OP_MUL:
        unread_token(c, 1)
        return None
    ident = read_token(c)
    if _g.dict[ident]['tag_'] != token_tag.TOKEN_IDENTIFIER:
        unread_token(c, 2)
        return None
    return create_ast_node2(node_tag.NODE_LABEL, ident, None)

def is_else_token(n):
    global _g
    if _g.dict[n]['tag_'] == token_tag.TOKEN_IDENTIFIER and query_keyword(_g.dict[n]['content_']) == keyword_tag.KEYWORD_ELSE:
        return True
    return False

def parse_control_safe(c):
    global _g
    ident = read_token(c)
    if _g.dict[ident]['tag_'] != token_tag.TOKEN_IDENTIFIER:
        unread_token(c, 1)
        return None
    keyword = query_keyword(_g.dict[ident]['content_'])
    if keyword < 0:
        unread_token(c, 1)
        return None

    if keyword == keyword_tag.KEYWORD_END:
        return create_ast_node(node_tag.NODE_END, None, None)
    elif keyword == keyword_tag.KEYWORD_RETURN:
        next = read_token(c)
        unread_token(c, 1)
        expr = None
        if not is_eos_like_token(_g.dict[next]['tag_']):
            expr = parse_expression(c)
        return create_ast_node(node_tag.NODE_RETURN, expr, None)
    elif keyword == keyword_tag.KEYWORD_GOTO or keyword == keyword_tag.KEYWORD_GOSUB:
        label = parse_label_safe(c)
        if label == None:
            print("Labels must be specified for goto or gosub.@@ %d Row", _g.dict[ident]['appear_line_']) # gotoまたはgosubにはラベルの指定が必須です
            sys.exit()
        if keyword == keyword_tag.KEYWORD_GOTO:
            tmp = node_tag.NODE_GOTO
        else:
            tmp = node_tag.NODE_GOSUB
        return create_ast_node(tmp, label, None)
    elif keyword == keyword_tag.KEYWORD_REPEAT:
        next = read_token(c)
        unread_token(c, 1)
        expr = None
        if not is_eos_like_token(_g.dict[next]['tag_']):
            expr = parse_expression(c)
        return create_ast_node(node_tag.NODE_REPEAT, expr, None)
    elif keyword == keyword_tag.KEYWORD_LOOP:
        return create_ast_node(node_tag.NODE_LOOP, None, None)
    elif keyword == keyword_tag.KEYWORD_CONTINUE:
        return create_ast_node(node_tag.NODE_CONTINUE, None, None)
    elif keyword == keyword_tag.KEYWORD_BREAK:
        return create_ast_node(node_tag.NODE_BREAK, None, None)
    elif keyword == keyword_tag.KEYWORD_IF:
        expr = parse_expression(c)
        next = read_token(c)
        repair_token = False
        true_statements = create_ast_node(node_tag.NODE_BLOCK_STATEMENTS, None, None)
        false_statements = None
        if _g.dict[next]['tag_'] == token_tag.TOKEN_LBRACE:
            while True:
                pp = prev_token(c, 0)
                if _g.dict[pp]['tag_'] == token_tag.TOKEN_RBRACE:
                    # RBRACEは食われてた
                    break
                statement = parse_statement(c)
                if statement == None:
                    print("if contains statements that cannot be parsed.@@ %d to %d Row", _g.dict[pp]['appear_line_'], _g.dict[ident]['appear_line_']) # if文の解析中、解析できないステートメントに到達しました
                    sys.exit()
                true_statements = create_ast_node(node_tag.NODE_BLOCK_STATEMENTS, true_statements, statement)
        else:
            unread_token(c, 1)
            nn = read_token(c)
            if _g.dict[nn]['tag_'] != token_tag.TOKEN_EOS:
                print("After if conditional, only { or : @@ %d Row", _g.dict[nn]['appear_line_']) # if文の解析中：ifの条件式の後は { か : しか置けません
                sys.exit()
            while True:
                pp = prev_token(c, 0)
                if _g.dict[pp]['tag_'] == token_tag.TOKEN_EOL:
                    # EOLは食われてた
                    repair_token = True
                    break
                nn = read_token(c)
                unread_token(c, 1)
                if is_else_token(nn):
                    break
                statement = parse_statement(c)
                if statement == None:
                    print("if contains statements that cannot be parsed.@@ %d to %d Row", _g.dict[nn]['appear_line_'], _g.dict[ident]['appear_line_']) # if文の解析中、解析できないステートメントに到達しました
                    sys.exit()
                true_statements = create_ast_node(node_tag.NODE_BLOCK_STATEMENTS, true_statements, statement)
        # elseはあるか？
        nn = read_token(c)
        if is_else_token(nn):
            repair_token = False
            false_statements = create_ast_node(node_tag.NODE_BLOCK_STATEMENTS, None, None)
            nextf = read_token(c)
            if _g.dict[nextf]['tag_'] == token_tag.TOKEN_LBRACE:
                while True:
                    ppf = prev_token(c, 0)
                    if _g.dict[ppf]['tag_'] == token_tag.TOKEN_RBRACE:
                        # RBRACEは食われてた
                        break
                    statement = parse_statement(c)
                    if statement == None:
                        print("else contains statements that cannot be parsed.@@ %d to %d Row", _g.dict[nn]['appear_line_'], _g.dict[ident]['appear_line_']) # ifのelse文の解析中、解析できないステートメントに到達しました
                        sys.exit()
                    false_statements = create_ast_node(node_tag.NODE_BLOCK_STATEMENTS, false_statements, statement)
            else:
                unread_token(c, 1)
                nnf = read_token(c)
                if _g.dict[nnf]['tag_'] != token_tag.TOKEN_EOS:
                    print("After else, only { or : @@ %d Row", _g.dict[nnf]['appear_line_']) # ifのelse文の解析中：elseの後は { か : しか置けません
                    sys.exit()
                while True:
                    pp = prev_token(c, 0)
                    if _g.dict[pp]['tag_'] == token_tag.TOKEN_EOL:
                        # EOLは食われてた
                        repair_token = True
                        break
                    nnf = read_token(c)
                    unread_token(c, 1)
                    if is_else_token(nnf):
                        break
                    statement = parse_statement(c)
                    if statement == None:
                        print("else contains statements that cannot be parsed.@@ %d to %d Row", _g.dict[nnf]['appear_line_'], _g.dict[ident]['appear_line_']) # ifのelse文の解析中、解析できないステートメントに到達しました
                        sys.exit()
                    false_statements = create_ast_node(node_tag.NODE_BLOCK_STATEMENTS, false_statements, statement)
        else:
            unread_token(c, 1)
        # EOLを食いすぎてしまった場合用
        if repair_token:
            unread_token(c, 1)
        dispatcher = create_ast_node(node_tag.NODE_IF_DISPATCHER, true_statements, false_statements)
        return create_ast_node(node_tag.NODE_IF, expr, dispatcher)
    elif keyword == keyword_tag.KEYWORD_ELSE:
        print("Detected an unprocessed else.@@ %d Row", _g.dict[ident]['appear_line_']) # ハンドルされないelseを検出しました
        sys.exit()
    unread_token(c, 1)
    return None

def parse_command_safe(c):
    global _g
    ident = read_token(c)
    if _g.dict[ident]['tag_'] != token_tag.TOKEN_IDENTIFIER:
        unread_token(c, 1)
        return None
    next = read_token(c)
    is_not_command = False
    if _g.dict[next]['tag_'] == token_tag.TOKEN_ASSIGN:
        is_not_command = True
    # "("チェック
    if not _g.dict[ident]['right_space_'] and _g.dict[next]['tag_'] == token_tag.TOKEN_LPARENTHESIS:
        is_not_command = True
    if (is_not_command):
        unread_token(c, 2)
        return None
    # あるなら引数の解析
    args = None
    if not is_eos_like_token(_g.dict[next]['tag_']):
        unread_token(c, 1)
        args = parse_arguments(c)
    else:
        unread_token(c, 1)
    command = create_ast_node2(node_tag.NODE_COMMAND, ident, args)
    return command

def parse_arguments(c):
    global _g
    arg = parse_expression(c)
    res = create_ast_node(node_tag.NODE_ARGUMENTS, arg, None)
    args = res
    while True:
        token = read_token(c)
        if _g.dict[token]['tag_'] != token_tag.TOKEN_COMMA:
            unread_token(c, 1)
            break
        next = parse_expression(c)
        _g.dict[args]['right_'] = create_ast_node(node_tag.NODE_ARGUMENTS, next, None)
        args = _g.dict[args]['right_']
    return res

def parse_assign_safe(c):
    variable = parse_variable_safe(c)
    if variable == None:
        return None
    next = read_token(c)
    if _g.dict[next]['tag_'] != token_tag.TOKEN_ASSIGN:
        print("Value substitution: = is required.@@ %d Row", _g.dict[next]['appear_line_']) # 代入 : =が必要です
        sys.exit()
    expr = parse_expression(c)
    assign = create_ast_node(node_tag.NODE_ASSIGN, variable, expr)
    return assign

def parse_variable_safe(c):
    global _g
    ident = read_token(c)
    if _g.dict[ident]['tag_'] != token_tag.TOKEN_IDENTIFIER:
        unread_token(c, 1)
        return None
    next = read_token(c)
    if _g.dict[next]['tag_'] != token_tag.TOKEN_LPARENTHESIS:
        unread_token(c, 1)
        return create_ast_node2(node_tag.NODE_VARIABLE, ident, None)
    idx = parse_expression(c)
    nn = read_token(c)
    if _g.dict[nn]['tag_'] != token_tag.TOKEN_RPARENTHESIS:
        # 多そうなので個別対処
        if _g.dict[nn]['tag_'] == token_tag.TOKEN_COMMA:
            print("Array variable is one dimension only.@@ %d Row", _g.dict[nn]['appear_line_']) # 配列変数 : 二次元以上の配列はサポートしていません
            sys.exit()
        print("Array variable: Parentheses are not closed.@@ %d Row", _g.dict[nn]['appear_line_']) # 配列変数 : 括弧が正しく閉じられていません
        sys.exit()
    return create_ast_node2(node_tag.NODE_VARIABLE, ident, idx)

def parse_expression(c):
    # ただの関数転送
    return parse_borand(c)

def parse_borand(c):
    global _g
    node = parse_eqneq(c)
    while True:
        is_continue = True
        token = read_token(c)
        if (_g.dict[token]['tag_'] == token_tag.TOKEN_OP_BOR) or (_g.dict[token]['tag_'] == token_tag.TOKEN_OP_BAND):
            r = parse_eqneq(c)
            if r == None:
                print("|,& Operator analysis failed.@@ %d Row", _g.dict[token]['appear_line_']) # |,&の演算子で、右項の解析が出来ません
                sys.exit()
            if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_BOR:
                node = create_ast_node(node_tag.NODE_BOR, node, r)
            elif _g.dict[token]['tag_'] == token_tag.TOKEN_OP_BAND:
                node = create_ast_node(node_tag.NODE_BAND, node, r)
            else:
                #assert(false)
                #sys.stdout.write('error')
                #sys.exit()
                pass
        else:
            is_continue = False
        if not is_continue:
            unread_token(c, 1)
            break
    return node

def parse_eqneq(c):
    global _g
    node = parse_gtlt(c)
    while True:
        is_continue = True
        token = read_token(c)
        if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_EQ or _g.dict[token]['tag_'] == token_tag.TOKEN_OP_NEQ or _g.dict[token]['tag_'] == token_tag.TOKEN_ASSIGN:
            r = parse_gtlt(c)
            if r == None:
                print("==,!= Operator analysis failed.@@ %d Row", _g.dict[token]['appear_line_']) # ==,!=の演算子で、右項の解析が出来ません
                sys.exit()
            if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_EQ or _g.dict[token]['tag_'] == token_tag.TOKEN_ASSIGN:
                node = create_ast_node(node_tag.NODE_EQ, node, r)
            elif _g.dict[token]['tag_'] == token_tag.TOKEN_OP_NEQ:
                node = create_ast_node(node_tag.NODE_NEQ, node, r)
                break
            else:
                #assert(false);
                pass
        else:
            is_continue = False
        if not is_continue:
            unread_token(c, 1)
            break
    return node

def parse_gtlt(c):
    global _g
    node = parse_addsub(c)
    while True:
        is_continue = True
        token = read_token(c)
        if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_GT or _g.dict[token]['tag_'] == token_tag.TOKEN_OP_GTOE or _g.dict[token]['tag_'] == token_tag.TOKEN_OP_LT or _g.dict[token]['tag_'] == token_tag.TOKEN_OP_LTOE:
            r = parse_addsub(c)
            if r == None:
                print(">,>=,<,<= Operator analysis failed.@@ %d Row", _g.dict[token]['appear_line_']) # >,>=,<,<=の演算子で、右項の解析が出来ません
                sys.exit()
            if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_GT:
                node = create_ast_node(node_tag.NODE_GT, node, r)
            elif _g.dict[token]['tag_'] == token_tag.TOKEN_OP_GTOE:
                node = create_ast_node(node_tag.NODE_GTOE, node, r)
            elif _g.dict[token]['tag_'] == token_tag.TOKEN_OP_LT:
                node = create_ast_node(node_tag.NODE_LT, node, r)
            elif _g.dict[token]['tag_'] == token_tag.TOKEN_OP_LTOE:
                node = create_ast_node(node_tag.NODE_LTOE, node, r)
            else:
                #assert(false)
                pass
        else:
            is_continue = False
        if not is_continue:
            unread_token(c, 1)
            break
    return node

def parse_addsub(c):
    global _g
    node = parse_muldivmod(c)
    while True:
        is_continue = True
        token = read_token(c)
        if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_ADD or _g.dict[token]['tag_'] == TOKEN_OP_SUB:
            r = parse_muldivmod(c)
            if r == None:
                print("+- Operator analysis failed.@@ %d Row", _g.dict[token]['appear_line_']) # +-の演算子で、右項の解析が出来ません
                sys.exit()
            if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_ADD:
                node = create_ast_node(node_tag.NODE_ADD, node, r)
            elif _g.dict[token]['tag_'] == token_tag.TOKEN_OP_SUB:
                node = create_ast_node(node_tag.NODE_SUB, node, r)
            else:
                #assert(false);
                pass
        else:
            is_continue = False
        if not is_continue:
            unread_token(c, 1)
            break
    return node

def parse_muldivmod(c):
    global _g
    node = parse_term(c)
    while True:
        is_continue = True
        token = read_token(c)
        if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_MUL or _g.dict[token]['tag_'] == token_tag.TOKEN_OP_DIV or _g.dict[token]['tag_'] == token_tag.TOKEN_OP_MOD:
            r = parse_term(c)
            if r == None:
                print("*/\\ Operator analysis failed.@@ %d Row", _g.dict[token]['appear_line_']) # */\\の演算子で、右項の解析が出来ません
                sys.exit()
            if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_MUL:
                node = create_ast_node(node_tag.NODE_MUL, node, r)
            elif _g.dict[token]['tag_'] == token_tag.TOKEN_OP_DIV:
                node = create_ast_node(node_tag.NODE_DIV, node, r)
            elif _g.dict[token]['tag_'] == token_tag.TOKEN_OP_MOD:
                node = create_ast_node(node_tag.NODE_MOD, node, r)
            else:
                #assert(false)
                pass
        else:
            is_continue = False
        if not is_continue:
            unread_token(c, 1)
            break
    return node

def parse_term(c):
    global _g
    token = read_token(c)
    if _g.dict[token]['tag_'] == token_tag.TOKEN_OP_SUB:
        return create_ast_node(node_tag.NODE_UNARY_MINUS, parse_primitive(c), None)
    else:
        pass
    unread_token(c, 1)
    return parse_primitive(c)

def parse_primitive(c):
    global _g
    token = read_token(c)
    if _g.dict[token]['tag_'] == token_tag.TOKEN_LPARENTHESIS:
        node = parse_expression(c)
        next = read_token(c)
        if _g.dict[next]['tag_'] != token_tag.TOKEN_RPARENTHESIS:
            print("Parentheses are not closed.@@ %d Row", _g.dict[token]['appear_line_']) # 括弧が閉じられていません
            sys.exit()
        return create_ast_node(node_tag.NODE_EXPRESSION, node, None)
    elif _g.dict[token]['tag_'] == token_tag.TOKEN_INTEGER or _g.dict[token]['tag_'] == token_tag.TOKEN_REAL or _g.dict[token]['tag_'] == token_tag.TOKEN_STRING:
        return create_ast_node2(node_tag.NODE_PRIMITIVE_VALUE, token, None)
    elif _g.dict[token]['tag_'] == token_tag.TOKEN_OP_MUL:
        unread_token(c, 1)
        label = parse_label_safe(c)
        if label == None:
            print("Label cannot be parsed.@@ %d Row", _g.dict[token]['appear_line_']) # ラベルが正しく解析できませんでした
            sys.exit()
        print("Labels cannot be used for expressions.@@ %d Row", _g.dict[token]['appear_line_']) # 式中にラベル型を使うことはできません
        sys.exit()
        #return label
    elif _g.dict[token]['tag_'] == token_tag.TOKEN_IDENTIFIER:
        unread_token(c, 1)
        expr = parse_identifier_expression(c)
        if expr == None:
            print("Function or Variable cannot be parsed.@@ %d Row", _g.dict[token]['appear_line_']) # 関数または変数を正しく解析できませんでした
            sys.exit()
        return expr
    else:
        pass
    print("Primitive values cannot be acquired.@@ %d Row[%s]", _g.dict[token]['appear_line_'], _g.dict[token]['content_']) # プリミティブな値を取得できません
    sys.exit()
    return None

def parse_identifier_expression(c):
    global _g
    ident = read_token(c)
    if _g.dict[ident]['tag_'] != token_tag.TOKEN_IDENTIFIER:
        unread_token(c, 1)
        return None
    next = read_token(c)
    if _g.dict[next]['tag_'] != token_tag.TOKEN_LPARENTHESIS:
        unread_token(c, 1)
        return create_ast_node2(node_tag.NODE_IDENTIFIER_EXPR, ident, None)
    # 引数なしの即閉じ？
    nn = read_token(c)
    if _g.dict[nn]['tag_'] == token_tag.TOKEN_RPARENTHESIS:
        return create_ast_node2(node_tag.NODE_IDENTIFIER_EXPR, ident, create_ast_node(node_tag.NODE_ARGUMENTS, None, None))
    unread_token(c, 1)
    # 引数あり
    idx = parse_arguments(c)
    nn = read_token(c)
    if _g.dict[nn]['tag_'] != token_tag.TOKEN_RPARENTHESIS:
        print("Function or Array variable: Parentheses are not closed.@@ %d Row", _g.dict[nn]['appear_line_']) # 関数または配列変数 : 括弧が正しく閉じられていません
        sys.exit()
    return create_ast_node2(node_tag.NODE_IDENTIFIER_EXPR, ident, idx)

# 変数
def create_variable(name):
    global _g
    res = new_variable_t()
    _g.dict[res]['name_'] = create_string3(name)
    _g.dict[res]['type_'] = value_tag.VALUE_NONE
    _g.dict[res]['granule_size_'] = 0
    _g.dict[res]['length_'] = 0
    _g.dict[res]['data_'] = None
    prepare_variable(res, value_tag.VALUE_INT, 64, 16)
    return res

def destroy_variable(v):
    global _g
    _g.dict[v]['name_'] = None
    _g.dict[v]['data_'] = None
    del _g.dict[v]

def prepare_variable(v, type, granule_size, length):
    global _g
    if _g.dict[v]['data_'] != None:
        tmp = _g.dict[v]['data_']
        del _g.dict[tmp]
    _g.dict[v]['type_'] = type
    _g.dict[v]['granule_size_'] = granule_size
    _g.dict[v]['length_'] = length
    areasize = 0
    if type == value_tag.VALUE_INT:
        areasize = sys.getsizeof(1) * _g.dict[v]['length_']
    elif type == value_tag.VALUE_DOUBLE:
        areasize = sys.getsizeof(0.1) * _g.dict[v]['length_']
    elif type == value_tag.VALUE_STRING:
        areasize = sys.getsizeof(u'a') * _g.dict[v]['granule_size_'] * _g.dict[v]['length_']
    else:
        #assert(false);
        pass
    if areasize > 0:
        sys.stdout.write('error10')
        sys.exit()
    _g.dict[v]['data_'] = new_data_t()

def create_variable_table():
    return create_list()

def destroy_variable_table(table):
    global _g
    node = _g.dict[table]['head_']
    while node != None:
        var = _g.dict[node]['value_']
        destroy_variable(var)
        node = _g.dict[node]['next_']
    list_free_all(table)
    destroy_list(table)

def search_variable(table, name):
    global _g
    node = _g.dict[table]['head_']
    while node != None:
        var = _g.dict[node]['value_']
        if name == None:
            if string_equal_igcase(_g.dict[var]['name_'], "", -1):
                return var
        else:
            if string_equal_igcase(_g.dict[var]['name_'], name, -1):
                return var
        node = _g.dict[node]['next_']
    return None

def variable_set(table, v, name, idx):
    global _g
    var = search_variable(table, name)
    if var == None:
        var = create_variable(name)
        node = create_list_node()
        _g.dict[node]['value_'] = var
        list_append(table, node)
    if var != None:
        sys.stdout.write('error11')
        sys.exit()
    if _g.dict[var]['type_'] != _g.dict[v]['type_']:
        if idx > 0:
            print("Variable type is different.@@ %s(%d)", name, idx) # 型の異なる変数への代入
            sys.exit()
        prepare_variable(var, _g.dict[v]['type_'], 64, 16)
    init_required = False
    granule_size = 0
    if _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        granule_size = len(_g.dict[v]['svalue_']) + 1
    tmp = _g.dict[v][var]
    if _g.dict[tmp]['granule_size_'] < granule_size:
        init_required = True
    len = _g.dict[var]['length_']
    if idx < 0 or len <= idx:
        print("Invalid value.@@ %s(%d)", name, idx) # 負の添え字、あるいは存在しない添え字への代入
        sys.exit()
    if init_required:
        prepare_variable(var, _g.dict[v]['type_'], granule_size, len)
    if _g.dict[var]['type_'] == _g.dict[v]['type_']:
        sys.stdout.write('error12')
        sys.exit()
    data_ptr = variable_data_ptr(var, idx)
    if _g.dict[var]['type_'] == value_tag.VALUE_INT:
        _g.dic[data_ptr]['content_'] = _g.dict[v]['ivalue_']
    elif _g.dict[var]['type_'] == value_tag.VALUE_DOUBLE:
        _g.dic[data_ptr]['content_'] = _g.dict[v]['dvalue_']
    elif _g.dict[var]['type_'] == value_tag.VALUE_STRING:
        _g.dic[data_ptr]['content_'] = _g.dict[v]['svalue_']
    else:
        #assert(false)
        pass

def variable_data_ptr(v, idx):
    global _g
    if v == None:
        if idx < 0 or idx >= 0:
            print("Variable is out of range.@@ %s(%d)", "???", idx) # 変数への配列アクセスが範囲外です
            sys.exit()
    else:
        if idx < 0 or idx >= _g.dict[v]['length_']:
            print("Variable is out of range.@@ %s(%d)", _g.dict[v]['name_'], idx) # 変数への配列アクセスが範囲外です
            sys.exit()
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        return _g.dict[v]['data_'] + idx
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        return _g.dict[v]['data_'] + idx
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        return _g.dict[v]['data_'] + _g.dict[v]['granule_size_'] * idx
    else:
        #assert(false);
        pass
    return None

def variable_calc_int(r, idx):
    global _g
    data_ptr = variable_data_ptr(r, idx)
    if _g.dict[r]['type_'] == value_tag.VALUE_INT:
        return int(_g.dict[data_ptr]['content_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_DOUBLE:
        return int(_g.dict[data_ptr]['content_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_STRING:
        return int(_g.dict[data_ptr]['content_'])
    else:
        #assert(false);
        pass
    return 0

def variable_calc_double(r, idx):
    global _g
    data_ptr = variable_data_ptr(r, idx)
    if _g.dict[r]['type_'] == value_tag.VALUE_INT:
        return float(_g.dict[data_ptr]['content_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_DOUBLE:
        return float(_g.dict[data_ptr]['content_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_STRING:
        return float(_g.dict[data_ptr]['content_'])
    else:
        #assert(false);
        pass
    return 0.0

def variable_calc_string(r, idx):
    global _g
    data_ptr = variable_data_ptr(r, idx)
    if _g.dict[r]['type_'] == value_tag.VALUE_INT:
        return str(_g.dict[data_ptr]['content_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_DOUBLE:
        return str(_g.dict[data_ptr]['content_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_STRING:
        return str(_g.dict[data_ptr]['content_'])
    else:
        #assert(false);
        pass
    return create_string3("")

# 値
def alloc_value():
    return new_value_t()

def create_value(v):
    global _g
    res = alloc_value()
    _g.dict[res]['type_'] = value_tag.VALUE_INT
    _g.dict[res]['ivalue_'] = v
    return res

def create_value2(v):
    global _g
    res = alloc_value()
    _g.dict[res]['type_'] = value_tag.VALUE_DOUBLE
    _g.dict[res]['dvalue_'] = v
    return res

def create_value3(v):
    global _g
    res = alloc_value()
    _g.dict[res]['type_'] = value_tag.VALUE_STRING
    _g.dict[res]['svalue_'] = create_string3(v)
    return res

def create_value4(v, idx):
    global _g
    res = alloc_value()
    _g.dict[res]['type_'] = value_tag.VALUE_VARIABLE
    _g.dict[res]['variable_'] = v
    _g.dict[res]['index_'] = idx
    return res

def create_value5(v):
    res = alloc_value()
    _g.dict[res]['type_'] = _g.dict[v]['type_']
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        _g.dict[res]['ivalue_'] = _g.dict[v]['ivalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        _g.dict[res]['dvalue_'] = _g.dict[v]['dvalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        _g.dict[res]['svalue_'] = create_string3(_g.dict[v]['svalue_'])
    elif _g.dict[v]['type_'] == value_tag.VALUE_VARIABLE:
        _g.dict[res]['variable_'] = _g.dict[v]['variable_']
        _g.dict[res]['index_'] = _g.dict[v]['index_']
    else:
        print("Copying an empty value and failed.@@ ptr=%p", v); # 中身が入ってない値をコピーして作ろうとしました
    return res

def create_value_move(v):
    global _g
    res = alloc_value()
    _g.dict[res]['type_'] = value_tag.VALUE_STRING
    _g.dict[res]['svalue_'] = v
    return res

def destroy_value(t):
    global _g
    clear_value(t)
    _g.dict[t]['type_'] = value_tag.VALUE_NONE
    _g.dict[t]['value_'] = 0
    del _g.dict[t]

def value_set(v, i):
    global _g
    clear_value(v)
    _g.dict[v]['type_'] = value_tag.VALUE_INT
    _g.dict[v]['ivalue_'] = i

def value_set2(v, d):
    global _g
    clear_value(v)
    _g.dict[v]['type_'] = value_tag.VALUE_DOUBLE
    _g.dict[v]['dvalue_'] = d

def value_set3(v, s):
    global _g
    clear_value(v)
    _g.dict[v]['svalue_'] = create_string3(s)
    _g.dict[v]['type_'] = value_tag.VALUE_STRING

def value_move(v, s):
    global _g
    clear_value(v)
    _g.dict[v]['type_'] =value_tag.VALUE_STRING
    _g.dict[v]['svalue_'] = s

def value_move2(to_, from_):
    global _g
    clear_value(to_)
    _g.dict[to_]['type_'] = _g.dict[from_]['type_']
    _g.dict[to_]['value_'] = _g.dict[from_]['value_']
    _g.dict[from_]['type_'] = value_tag.VALUE_NONE
    _g.dict[from_]['value_'] = 0

def value_get_primitive_tag(r):
    global _g
    if _g.dict[r]['type_'] == value_tag.VALUE_VARIABLE:
        tmp = _g.dict[r]['variable_']
        return _g.dict[tmp]['type_']
    return _g.dict[r]['type_']

def value_calc_boolean(r):
    if value_get_primitive_tag(r) == value_tag.VALUE_INT:
        return value_calc_int(r) != 0
    elif value_get_primitive_tag(r) == value_tag.VALUE_DOUBLE:
        return value_calc_double(r) != 0.0
    elif value_get_primitive_tag(r) == value_tag.VALUE_STRING:
        return value_calc_int(r) != 0
    else:
        #assert(false)
        pass
    return False

def value_calc_int(r):
    global _g
    if _g.dict[r]['type_'] == value_tag.VALUE_INT:
        return _g.dict[r]['ivalue_']
    elif _g.dict[r]['type_'] == value_tag.VALUE_DOUBLE:
        return int(_g.dict[r]['dvalue_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_STRING:
        return int(_g.dict[r]['svalue_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_VARIABLE:
        return variable_calc_int(_g.dict[r]['variable_'], _g.dict[r]['index_'])
    else:
        #assert(false);
        pass
    return 0

def value_calc_double(r):
    global _g
    if _g.dict[r]['type_']==value_tag.VALUE_INT:
        return float(_g.dict[r]['ivalue_'])
    elif _g.dict[r]['type_']==value_tag.VALUE_DOUBLE:
        return float(_g.dict[r]['dvalue_'])
    elif _g.dict[r]['type_']==value_tag.VALUE_STRING:
        return float(_g.dict[r]['svalue_'])
    elif _g.dict[r]['type_']==value_tag.VALUE_VARIABLE:
        return variable_calc_double(_g.dict[r]['variable_'], _g.dict[r]['index_'])
    else:
        #assert(false);
        pass
    return 0.0

def value_calc_string(r):
    global _g
    s = ''
    if _g.dict[r]['type_'] == value_tag.VALUE_INT:
        s = create_string_from(_g.dict[r]['ivalue_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_DOUBLE:
        s = create_string_from2(_g.dict[r]['dvalue_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_STRING:
        s = create_string3(_g.dict[r]['svalue_'])
    elif _g.dict[r]['type_'] == value_tag.VALUE_VARIABLE:
        s = variable_calc_string(_g.dict[r]['variable_'], _g.dict[r]['index_'])
    else:
        #assert(false)
        pass
    return s

def value_convert_type(to, r):
    global _g
    if to == _g.dict[r]['type_']:
        return create_value5(r)
    if to == value_tag.VALUE_INT:
        return create_value(value_calc_int(r))
    if to == value_tag.VALUE_DOUBLE:
        return create_value2(value_calc_double(r))
    if to == value_tag.VALUE_STRING:
        s = value_calc_string(r)
        res = create_value_move(s)
        return res
    else:
        #assert(false)
        pass
    return None

def value_isolate(v):
    global _g
    if _g.dict[v]['type_'] != value_tag.VALUE_VARIABLE:
        return
    if _g.dict[v]['variable_'] != None:
        tmp = _g.dict[v]['variable_']
        if _g.dict[tmp]['type_'] == value_tag.VALUE_INT:
            value_set(v, variable_calc_int(_g.dict[v]['variable_'], _g.dict[v]['index_']))
        elif _g.dict[tmp]['type_'] == value_tag.VALUE_DOUBLE:
            value_set2(v, variable_calc_double(_g.dict[v]['variable_'], _g.dict[v]['index_']))
        elif _g.dict[tmp]['type_'] == value_tag.VALUE_STRING:
            value_move(v, variable_calc_string(_g.dict[v]['variable_'], _g.dict[v]['index_']))
        else:
            #assert(false);
            pass

def value_bor(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        value_set(v, _g.dict[v]['ivalue_'] | _g.dict[t]['ivalue_'])
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        print("| operator for the floating point is not defined.") # 浮動小数点同士の|演算子は挙動が定義されていません
        sys.exit()
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print("| operator for the string is not defined.") # 文字列同士の|演算子は挙動が定義されていません
        sys.exit()
    else:
        #assert(false)
        #break
        pass
    destroy_value(t)

def value_band(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        value_set(v, _g.dict[v]['ivalue_'] & _g.dict[t]['ivalue_'])
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        print("& operator for the floating point is not defined.") # 浮動小数点同士の&演算子は挙動が定義されていません
        sys.exit()
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print("& operator for the string is not defined."); # 文字列同士の&演算子は挙動が定義されていません
        sys.exit()
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_eq(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        if _g.dict[v]['ivalue_'] == _g.dict[t]['ivalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        if _g.dict[v]['dvalue_'] == _g.dict[t]['dvalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        if _g.dict[v]['svalue_'] == _g.dict[t]['svalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_neq(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        if _g.dict[v]['ivalue_'] != _g.dict[t]['ivalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        if _g.dict[v]['dvalue_'] != _g.dict[t]['dvalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        if _g.dict[v]['svalue_'] != _g.dict[t]['svalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_gt(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        if _g.dict[v]['ivalue_'] > _g.dict[t]['ivalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        if _g.dict[v]['dvalue_'] > _g.dict[t]['dvalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print("> operator for the string is not defined."); # 文字列同士の>演算子は挙動が定義されていません
        sys.exit()
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_gtoe(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        if _g.dict[v]['ivalue_'] >= _g.dict[t]['ivalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        if _g.dict[v]['dvalue_'] >= _g.dict[t]['dvalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print(">= operator for the string is not defined."); # 文字列同士の>=演算子は挙動が定義されていません
        sys.exit()
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_lt(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        if _g.dict[v]['ivalue_'] < _g.dict[t]['ivalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        if _g.dict[v]['dvalue_'] < _g.dict[t]['dvalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print("< operator for the string is not defined."); # 文字列同士の<演算子は挙動が定義されていません
        sys.exit()
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_ltoe(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        if _g.dict[v]['ivalue_'] <= _g.dict[t]['ivalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        if _g.dict[v]['dvalue_'] <= _g.dict[t]['dvalue_']:
            value_set(v, 1)
        else:
            value_set(v, 0)
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print("<= operator for the string is not defined."); # 文字列同士の<演算子は挙動が定義されていません
        sys.exit()
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_add(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        _g.dict[v]['ivalue_'] += _g.dict[t]['ivalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        _g.dict[v]['dvalue_'] += _g.dict[t]['dvalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        _g.dict[v]['svalue_'] += _g.dict[t]['svalue_']
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_sub(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        _g.dict[v]['ivalue_'] -= _g.dict[t]['ivalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        _g.dict[v]['dvalue_'] -= _g.dict[t]['dvalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print("- operator for the string is not defined."); # 文字列同士の*演算子は挙動が定義されていません
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_mul(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        _g.dict[v]['ivalue_'] *= _g.dict[t]['ivalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        _g.dict[v]['dvalue_'] *= _g.dict[t]['dvalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print("* operator for the string is not defined."); # 文字列同士の*演算子は挙動が定義されていません
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_div(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        _g.dict[v]['ivalue_'] /= _g.dict[t]['ivalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        _g.dict[v]['dvalue_'] /= _g.dict[t]['dvalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print("/ operator for the string is not defined."); # 文字列同士の/演算子は挙動が定義されていません
    else:
        #assert(false);
        pass
    destroy_value(t)

def value_mod(v, r):
    global _g
    t = value_convert_type(_g.dict[v]['type_'], r)
    if _g.dict[v]['type_'] == value_tag.VALUE_INT:
        _g.dict[v]['ivalue_'] %= _g.dict[t]['ivalue_']
    elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
        print("\\ operator for the double is not defined."); # double同士の\\演算子は挙動が定義されていません
    elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
        print("\\ operator for the string is not defined."); # 文字列同士の\\演算子は挙動が定義されていません
    else:
        #assert(false);
        pass
    destroy_value(t)

# スタック
def create_value_stack():
    res = new_value_stack_t()
    initialize_value_stack(res)
    return res

def destroy_value_stack(st):
    global _g
    uninitialize_value_stack(st)
    del _g.dict['st']

def initialize_value_stack(st):
    global _g
    l = 16; # 初期サイズ
    _g.dict[st]['stack_'] = [] # new_value_t()
    _g.dict[st]['top_'] = 0
    _g.dict[st]['max_'] = l

def uninitialize_value_stack(st):
    global _g
    _g.dict[st] = None
    #  stack_pop(st, _g.dict[st]['top_'])
    #  del _g.dict[st]['stack_']
    #  _g.dict[st]['stack_'] = None
    #  _g.dict[st]['top_'] = 0
    #  _g.dict[st]['max_'] = 0

def stack_push(st, v):
    global _g
    _g.dict[st].append(v)
    # global _g
    # if _g.dict[st]['top_'] + 1 > _g.dict[st]['max_']:
    #     _g.dict[st]['max_'] = _g.dict[st]['max_'] * 2; # 貪欲
    #     _g.dict[st]['stack_'] = new_value_t()
    # _g.dict[st]['stack_'][_g.dict[st]['top_']] = v #要修正
    # _g.dict[st]['top_'] += 1

def stack_push2(st, v):
    global _g
    _g.dict[st].append(v)
    # vp = create_value5(v)
    # stack_push(st, vp)

def stack_peek(st, i):
    global _g
    return _g.dict[st][len(_g.dict[st])-1]
    # idx = 0
    # if i < 0:
    #     idx = _g.dict[st]['top_'] + i
    # else:
    #     idx = i
    # assert(idx >= 0 && idx < st->top_);
    # return st->stack_[idx];

def stack_pop(st, n):
    global _g
    _g.dict[st].pop()
    # assert(n <= (size_t)st->top_);
    # while (n-- > 0) {
    #     --st->top_;
    #     assert(st->stack_[st->top_] != NULL);
    #     destroy_value(st->stack_[st->top_]);
    #     st->stack_[st->top_] = NULL;

# キーワード
def query_keyword(s):
    table = {
        keyword_tag.KEYWORD_END: "end",
        keyword_tag.KEYWORD_RETURN: "return",
        keyword_tag.KEYWORD_GOTO: "goto",
        keyword_tag.KEYWORD_GOSUB: "gosub",
        keyword_tag.KEYWORD_REPEAT: "repeat",
        keyword_tag.KEYWORD_LOOP: "loop",
        keyword_tag.KEYWORD_CONTINUE: "continue",
        keyword_tag.KEYWORD_BREAK: "break",
        keyword_tag.KEYWORD_IF: "if",
        keyword_tag.KEYWORD_ELSE: "else",
    }
	# 全探索
    for key in table:
        if string_equal_igcase(s, table[key], -1):
            return key

# システム変数
def query_sysvar(s):
    table = {
        sysvar_tag.SYSVAR_CNT: "cnt",
        sysvar_tag.SYSVAR_STAT: "stat",
        sysvar_tag.SYSVAR_REFDVAL: "refdval",
        sysvar_tag.SYSVAR_REFSTR: "refstr", 
        sysvar_tag.SYSVAR_STRSIZE: "strsize",
    }
    # 全探索
    for key in table:
        if string_equal_igcase(s, table[key], -1):
             return key
    return -1

# 実行環境
def create_execute_environment():
    global _g
    res = new_execute_environment_t()
    _g.dict[res]['parser_list_'] = create_list()
    _g.dict[res]['ast_list_'] = create_list()
    _g.dict[res]['statement_list_'] = create_list()
    _g.dict[res]['label_table_'] = create_list()
    _g.dict[res]['variable_table_'] = create_variable_table()
    return res

def destroy_execute_environment(e):
    global _g

    # 自分でallocしたものだけ先に消す
    tmp = _g.dict[e]['statement_list_']
    node = _g.dict[e]['head_']
    while node != None:
        ast = _g.dict[node]['value_']
        if _g.dict[ast]['flag_'] and ast_node_flag_tag.NODE_FLAG_ADDITIONAL:
            destroy_ast_node(ast)
        node = _g.dict[node]['next_']
    list_free_all(_g.dict[e]['statement_list_'])
    destroy_list(_g.dict[e]['statement_list_'])

    tmp = _g.dict[e]['parser_list_']
    node = _g.dict[tmp]['head_']
    while node != None:
        parser = _g.dict[node]['value_']
        uninitialize_parse_context(parser)
        destroy_parse_context(parser)
        node = _g.dict[node]['next_']
    list_free_all(_g.dict[e]['parser_list_'])
    destroy_list(_g.dict[e]['parser_list_'])

    tmp = _g.dict[e]['ast_list_']
    node = _g.dict[tmp]['head_']
    while node != None:
        ast = _g.dict[node]['value_']
        destroy_ast(ast)
        node = _g.dict[node]['next_']
    list_free_all(_g.dict[e]['ast_list_'])
    destroy_list(_g.dict[e]['ast_list_'])

    tmp = _g.dict[e]['label_table_']
    node = _g.dict[tmp]['head_']
    while node != None:
        label_node = _g.dict[node]['value_']
        _g.dict[label_node]['name_'] = None
        del _g.dict[label_node]
        _g.dict[node]['value_'] = None
        node = _g.dict[node]['next_']
    list_free_all(_g.dict[e]['label_table_'])
    destroy_list(_g.dict[e]['label_table_'])

    destroy_variable_table(_g.dict[e]['variable_table_'])
    del _g.dict[e]

def initialize_execute_status(s):
    global _g
    _g.dict[s]['stack_'] = create_value_stack()
    _g.dict[s]['node_cur_'] = None
    _g.dict[s]['current_call_frame_'] = 0
    _g.dict[s]['call_frame_'][0]['caller_'] = None
    _g.dict[s]['current_loop_frame_'] = 0
    loop_frame = _g.dict[s]['loop_frame_']
    _g.dict[s]['loop_frame_'][0]['counter_'] = 0
    _g.dict[s]['loop_frame_'][0]['max_'] = 0
    _g.dict[s]['loop_frame_'][0]['cnt_'] = 0
    _g.dict[s]['is_end_'] = False
    _g.dict[s]['stat_'] = 0
    _g.dict[s]['refdval_'] = 0.0
    _g.dict[s]['refstr_'] = create_string3("")
    _g.dict[s]['strsize_'] = 0

def uninitialize_execute_status(s):
    global _g
    destroy_value_stack(_g.dict[s]['stack_'])
    destroy_string(_g.dict[s]['refstr_'])
    _g.dict[s]['refstr_'] = None

def _cl():
    global _g
    n = create_ast_node(node_tag.NODE_JUMP_LABEL, None, None)
    _g.dict[n]['flag_'] |= ast_node_flag_tag.NODE_FLAG_ADDITIONAL
    return n

def _cj():
    global _g
    n = create_ast_node(node_tag.NODE_JUMP_INTERNAL, None, None)
    _g.dict[n]['flag_'] |= ast_node_flag_tag.NODE_FLAG_ADDITIONAL
    return n

def _aj(tail, e):
    global _g
    j = _cj()
    _g.dict[j]['ext_'] = tail
    jumper = create_list_node()
    _g.dict[jumper]['value_'] = j
    list_append(_g.dict[e]['statement_list_'], jumper)

def flatten(e, node):
    global _g
    is_add = True
    # 前処理
    if _g.dict[node]['tag_'] == node_tag.NODE_BLOCK_STATEMENTS:
        if _g.dict[node]['left_']:
            flatten(e, _g.dict[node]['left_'])
        if _g.dict[node]['right_']:
            flatten(e, _g.dict[node]['right_'])
        is_add = False
    elif _g.dict[node]['tag_'] == node_tag.NODE_IF:
        # 処理用のノードを付け足す
        check_node = create_list_node()
        checker = create_ast_node(node_tag.NODE_IF_CHECK, None, None)
        _g.dict[checker]['flag_'] |= ast_node_flag_tag.NODE_FLAG_ADDITIONAL
        _g.dict[checker]['ext_'] = _g.dict[node]['left_']
        _g.dict[check_node]['value_'] = checker
        list_append(_g.dict[e]['statement_list_'], check_node)
        #
        # 各ブロックを線形に貼りなおす
        dispatcher = _g.dict[node]['right_']
        if _g.dict[dispatcher]['tag_'] == node_tag.NODE_IF_DISPATCHER:
            sys.stdout.write('error13')
            sys.exit()
        true_head = create_list_node()
        _g.dict[true_head]['value_'] = _cl()
        false_head = create_list_node()
        _g.dict[false_head]['value_'] = _cl()
        tail = create_list_node()
        _g.dict[tail]['value_'] = _cl()
        # 分岐
        _aj(true_head, e)
        _aj(false_head, e)
        # 真
        list_append(_g.dict[e]['statement_list_'], true_head)
        flatten(e, _g.dict[dispatcher]['left_'])
        _aj(tail, e)
        # 偽
        list_append(_g.dict[e]['statement_list_'], false_head)
        if _g.dict[dispatcher]['right_']:
            flatten(e, _g.dict[dispatcher]['right_'])
            _aj(tail, e)
        # 合流
        list_append(_g.dict[e]['statement_list_'], tail)
        #
        is_add = False
    # 後処理
    if is_add:
        list_node = create_list_node()
        _g.dict[list_node]['value_'] = node
        list_append(_g.dict[e]['statement_list_'], list_node)
        if _g.dict[node]['tag_'] == node_tag.NODE_LABEL:
            label_node = create_list_node()
            label = new_label_node_t()
            tmp = _g.dict[node]['token_']
            _g.dict[label]['name_'] = create_string3(_g.dict[tmp]['content_'])
            _g.dict[label]['statement_'] = list_node
            _g.dict[label_node]['value_'] = label
            list_append(_g.dict[e]['label_table_'], label_node)
        elif _g.dict[node]['tag_'] == node_tag.NODE_REPEAT:
            # 処理用のノードを付け足す
            check_node = create_list_node()
            checker = create_ast_node(node_tag.NODE_REPEAT_CHECK, None, None)
            _g.dict[checker]['flag_'] |= ast_node_flag_tag.NODE_FLAG_ADDITIONAL
            _g.dict[check_node]['value_'] = checker
            list_append(_g.dict[e]['statement_list_'], check_node)

def walk(e, node):
    global _g
    if _g.dict[node]['tag_'] == node_tag.NODE_VARIABLE or _g.dict[node]['tag_'] == node_tag.NODE_IDENTIFIER_EXPR: # 変数配列の可能性あり
        tmp = _g.dict[node]['token_']
        var_name = _g.dict[tmp]['content_'];
        if search_variable(_g.dict[e]['variable_table_'], var_name) == None:
            # 適当な変数として初期化しておく
            v = new_value_t()
            _g.dict[v]['variable_'] = new_variable_t()
            _g.dict[v]['type_'] = value_tag.VALUE_INT
            _g.dict[v]['ivalue_'] = 0
            variable_set(_g.dict[e]['variable_table_'], v, var_name, 0)
    if _g.dict[node]['left_'] != None:
        walk(e, _g.dict[node]['left_'])
    if _g.dict[node]['right_'] != None:
        walk(e, _g.dict[node]['right_'])

def load_script(e, script):
    global _g
    if len(script) == 0:
        sys.stdout.write("ERROR: スクリプトの内容が空です")
        sys.exit()
    tokenizer = new_tokenize_context_t()
    initialize_tokenize_context(tokenizer, script)
    parser = create_parse_context()
    initialize_parse_context(parser, tokenizer)
    # スクリプトをパースする
    ast = parse_script(parser)
    uninitialize_tokenize_context(tokenizer)
    # ASTを繋げたりラベルを持っておいたり
    st = _g.dict[ast]['head_']
    while st != None:
        node = _g.dict[st]['value_']
        flatten(e, node)
        st = _g.dict[st]['next_']
    # 特定の部分木マッチング
    st = _g.dict[ast]['head_']
    while st != None:
        node = _g.dict[st]['value_']
        walk(e, node)
        st = _g.dict[st]['next_']
    # パーサーとASTを保存しておく
    parser_node = create_list_node()
    _g.dict[parser_node]['value_'] = parser
    list_append(_g.dict[e]['parser_list_'], parser_node)

    ast_node = create_list_node()
    _g.dict[ast_node]['value_'] = ast
    list_append(_g.dict[e]['ast_list_'], ast_node)

def evaluate(e, s, n):
    global _g
    if _g.dict[s]['is_end_']: # もう実行おわってる
        return
    if _g.dict[n]['tag_'] == node_tag.NODE_EMPTY or node_tag.NODE_LABEL:
        pass
    elif _g.dict[n]['tag_'] == node_tag.NODE_BLOCK_STATEMENTS:
        if _g.dict[n]['left_']:
            evaluate(e, s, _g.dict[n]['left_'])
        if _g.dict[n]['right_']:
            evaluate(e, s, _g.dict[n]['right_'])
    elif _g.dict[n]['tag_'] == node_tag.NODE_COMMAND:
        tmp = _g.dict[n]['token_']
        if _g.dict[tmp]['tag_'] == token_tag.TOKEN_IDENTIFIER:
            sys.stdout.write('error14')
            sys.exit()
        tmp = _g.dict[n]['token_']
        command_name = _g.dict[tmp]['content_']
        command = query_command(command_name)
        if command == -1:
            print("Command not found:%s", command_name) # コマンドが見つかりません
        delegate = get_command_delegate(command)
        if delegate != None:
            sys.stdout.write('error15')
            sys.exit()
        tmp = _g.dict[s]['stack_']
        top = _g.dict[tmp]['top_']
        if _g.dict[n]['left_'] != None:
            evaluate(e, s, _g.dict[n]['left_'])
        tmp = _g.dict[s]['stack_']
        arg_num = _g.dict[tmp]['top_'] - top
        delegate(e, s, arg_num)
        tmp = _g.dict[s]['stack_']
        if _g.dict[tmp]['top_'] == top: # 戻り値がないことを確認
            sys.stdout.write('error16')
            sys.exit()
    elif _g.dict[n]['tag_'] == node_tag.NODE_ARGUMENTS:
        if _g.dict[n]['left_'] != None:
            evaluate(e, s, _g.dict[n]['left_'])
        if _g.dict[n]['right_'] != None:
            evaluate(e, s, _g.dict[n]['right_'])
    elif _g.dict[n]['tag_'] == node_tag.NODE_ASSIGN:
        evaluate(e, s, _g.dict[n]['left_'])
        evaluate(e, s, _g.dict[n]['right_'])
        var = stack_peek(_g.dict[s]['stack_'], -2)
        if _g.dict[var]['type_'] != value_tag.VALUE_VARIABLE:
            print("Substitution: Please specify a variable.") # 変数代入：代入先が変数ではありませんでした
        v = stack_peek(_g.dict[s]['stack_'], -1)

        value_isolate(v)
        if _g.dict[var]['variable_'] == None:
            variable_set(_g.dict[e]['variable_table_'], v, None, _g.dict[var]['index_']) # var->variable_->name_, var->index_);
        else:
            tmp = _g.dict[var]['variable_']
            variable_set(_g.dict[e]['variable_table_'], v, _g.dict[tmp]['name_'], _g.dict[var]['index_'])
        stack_pop(_g.dict[s]['stack_'], 2)
    elif _g.dict[n]['tag_'] == node_tag.NODE_VARIABLE:
        tmp = _g.dict[n]['token_']
        var_name = _g.dict[tmp]['content_']
        var = search_variable(_g.dict[e]['variable_table_'], var_name)
        if var != None:
            sys.stdout.write('error17')
            sys.exit()
        idx = 0
        idx_node = _g.dict[n]['left_']
        if idx_node:
            evaluate(e, s, idx_node)
            i = stack_peek(_g.dict[s]['stack_'], -1)
            idx = value_calc_int(i)
            stack_pop(_g.dict[s]['stack_'], 1)
        v = create_value4(var, idx)
        stack_push(_g.dict[s]['stack_'], v)
    elif _g.dict[n]['tag_'] == node_tag.NODE_EXPRESSION:
        evaluate(e, s, _g.dict[n]['left_'])
    elif _g.dict[n]['tag_'] == node_tag.NODE_BOR or _g.dict[n]['tag_'] == node_tag.NODE_BAND or _g.dict[n]['tag_'] == node_tag.NODE_EQ or _g.dict[n]['tag_'] == node_tag.NODE_NEQ or _g.dict[n]['tag_'] == node_tag.NODE_GT or _g.dict[n]['tag_'] == node_tag.NODE_GTOE or _g.dict[n]['tag_'] == node_tag.NODE_LT or _g.dict[n]['tag_'] == node_tag.NODE_LTOE or _g.dict[n]['tag_'] == node_tag.NODE_ADD or _g.dict[n]['tag_'] == node_tag.NODE_SUB or _g.dict[n]['tag_'] == node_tag.NODE_MUL or _g.dict[n]['tag_'] == node_tag.NODE_DIV or _g.dict[n]['tag_'] == node_tag.NODE_MOD:
        evaluate(e, s, _g.dict[n]['left_'])
        evaluate(e, s, _g.dict[n]['right_'])
        l = stack_peek(_g.dict[s]['stack_'], -2)
        r = stack_peek(_g.dict[s]['stack_'], -1)
        value_isolate(l)
        if _g.dict[n]['tag_'] == node_tag.NODE_BOR:
            value_bor(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_BAND:
            value_band(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_EQ:
            value_eq(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_NEQ:
            value_neq(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_GT:
            value_gt(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_GTOE:
            value_gtoe(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_LT:
            value_lt(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_LTOE:
            value_ltoe(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_ADD:
            value_add(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_SUB:
            value_sub(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_MUL:
            value_mul(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_DIV:
            value_div(l, r)
        elif _g.dict[n]['tag_'] == node_tag.NODE_MOD:
            value_mod(l, r)
        else:
            if _g.dict[n]['tag_'] == False:
                sys.stdout.write('error18')
                sys.exit()
        stack_pop(_g.dict[s]['stack_'], 1)
    elif _g.dict[n]['tag_'] == node_tag.NODE_UNARY_MINUS:
        if _g.dict[n]['left_'] != None:
            sys.stdout.write('error19')
            sys.exit()
        evaluate(e, s, _g.dict[n]['left_'])
        v = stack_peek(_g.dict[s]['stack_'], -1)
        value_isolate(v)
        if _g.dict[v]['type_'] == value_tag.VALUE_INT:
            _g.dict[v]['ivalue_'] = 0 - _g.dict[v]['ivalue_']
        elif _g.dict[v]['type_'] == value_tag.VALUE_DOUBLE:
            _g.dict[v]['dvalue_'] = 0.0 - _g.dict[v]['dvalue_']
        elif _g.dict[v]['type_'] == value_tag.VALUE_STRING:
            print("no minus value in the string.[%s]", _g.dict[v]['svalue_']) # 文字列に負値は存在しません
        else:
            if _g.dict[v]['type_'] == False:
                sys.stdout.write('error20')
                sys.exit()
    elif _g.dict[n]['tag_'] == node_tag.NODE_PRIMITIVE_VALUE:
        tmp = _g.dict[n]['token_']
        if _g.dict[tmp]['tag_'] == token_tag.TOKEN_INTEGER:
            tmp2 = _g.dict[n]['token_']
            stack_push(_g.dict[s]['stack_'], create_value(int(_g.dict[tmp2]['content_'])))
        elif _g.dict[tmp]['tag_'] == token_tag.TOKEN_REAL:
            tmp2 = _g.dict[n]['token_']
            stack_push(_g.dict[s]['stack_'], create_value2(float(_g.dict[tmp2]['content_'])))
        elif _g.dict[tmp]['tag_'] == token_tag.TOKEN_STRING:
            tmp2 = _g.dict[n]['token_']
            stack_push(_g.dict[s]['stack_'], create_value3(_g.dict[tmp2]['content_']))
        else:
            if _g.dict[tmp]['tag_'] == token_tag.False:
                sys.stdout.write('error21')
                sys.exit()
    elif _g.dict[n]['tag_'] == node_tag.NODE_IDENTIFIER_EXPR:
        tmp = _g.dict[n]['token_']
        if _g.dict[tmp]['tag_'] == token_tag.TOKEN_IDENTIFIER:
            sys.stdout.write('error22')
            sys.exit()
        tmp = _g.dict[n]['token_']
        ident = _g.dict[tmp]['content_']
        tmp = _g.dict[s]['stack_']
        top = _g.top_
        if _g.dict[n]['left_'] != None:
            evaluate(e, s, _g.dict[n]['left_'])
        tmp = _g.dict[s]['stack_']
        arg_num = _g.dict[tmp]['top_'] - top
        function = query_function(ident)
        if function >= 0:
            # 関数呼び出し
            delegate = get_function_delegate(function)
            if delegate != None:
                sys.stdout.write('error23')
                sys.exit()
            delegate(e, s, arg_num)
            tmp = _g.dict[s]['stack_']
            if _g.dict[tmp]['top_'] == top + 1: # 戻り値が入っていることを確認する
                sys.stdout.write('error24')
                sys.exit()
        else:
            # システム変数
            sysvar = query_sysvar(ident)
            if sysvar >= 0:
                if arg_num > 0:
                    print("cannot arrays in the system variable.", ident) # システム変数に添え字はありません
                # 後々のことも考えて、一応
                stack_pop(_g.dict[s]['stack_'], arg_num)
                if sysvar == sysvar_tag.SYSVAR_CNT:
                    if _g.dict[s]['current_loop_frame_'] <= 0:
                        print("System variable(cnt): cannot refer outside the repeat-loop.") # システム変数cnt：repeat-loop中でないのに参照しました
                    stack_push(_g.dict[s]['stack_'], create_value(_g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1].cnt_))
                elif sysvar == sysvar_tag.SYSVAR_STAT:
                    stack_push(_g.dict[s]['stack_'], create_value(_g.dict[s]['stat_']))
                elif sysvar == sysvar_tag.SYSVAR_REFDVAL:
                    stack_push(_g.dict[s]['stack_'], create_value2(_g.dict[s]['refdval_']))
                elif sysvar == sysvar_tag.SYSVAR_REFSTR:
                    stack_push(_g.dict[s]['stack_'], create_value3(_g.dict[s]['refstr_']))
                elif sysvar == sysvar_tag.SYSVAR_STRSIZE:
                    stack_push(_g.dict[s]['stack_'], create_value(_g.dict[s]['strsize_']))
                else:
                    # assert(false)
                    stack_push(_g.dict[s]['stack_'], create_value(0))
            else:
                # 配列変数
                if arg_num > 1:
                    print("Function not found, Array variable is one dimension only.@@ %s", ident) # 関数がみつかりません、配列変数の添え字は1次元までです
                var = search_variable(_g.dict[e]['variable_table_'], ident)
                if var != None:
                    sys.stdout.write('error25')
                    sys.exit()
                idx = 0
                if arg_num > 0:
                    i = stack_peek(_g.dict[s]['stack_'], -1)
                    idx = value_calc_int(i)
                v = create_value4(var, idx)
                stack_pop(_g.dict[s]['stack_'], arg_num)
                stack_push(_g.dict[s]['stack_'], v)
    elif _g.dict[n]['tag_'] == node_tag.NODE_END:
        _g.dict[s]['is_end_'] = True
    elif _g.dict[n]['tag_'] == node_tag.NODE_RETURN:
        if _g.dict[s]['current_call_frame_'] <= 0:
            print("Return from outside the subroutine is invalid.") # サブルーチン外からのreturnは無効です
        if _g.dict[n]['left_']:
            evaluate(e, s, _g.dict[n]['left_'])
            res = stack_peek(_g.dict[s]['stack_'], -1)
            if value_get_primitive_tag(res) == value_tag.VALUE_INT:
                _g.dict[s]['stat_'] = value_calc_int(res)
            elif value_get_primitive_tag(res) == value_tag.VALUE_DOUBLE:
                _g.dict[s]['refdval_'] = value_calc_double(res)
            elif value_get_primitive_tag(res) == value_tag.VALUE_STRING:
                destroy_string(_g.dict[s]['refstr_'])
                _g.dict[s]['refstr_'] = value_calc_string(res)
            else:
                #assert(false);
                pass
            stack_pop(_g.dict[s]['stack_'], 1)
        _g.dict[s]['current_call_frame_'] -= 1
        _g.dict[s]['node_cur_'] = _g.dict[s]['call_frame_'][_g.dict[s]['current_call_frame_']]['caller_']
    elif _g.dict[n]['tag_'] == node_tag.NODE_GOTO:
        label_node = _g.dict[n]['left_']
        if label_node != None:
            sys.stdout.write('error26')
            sys.exit()
        if _g.dict[label_node]['tag_'] == node_tag.NODE_LABEL:
            sys.stdout.write('error27')
            sys.exit()
        tmp = _g.dict[label_node]['token_']
        label_name = _g.dict[tmp]['content_']
        label = search_label(e, label_name)
        if label == None:
            print("goto: Label not found.@@ %s", label_name) # goto：ラベルがみつかりません
            sys.exit()
        _g.dict[s]['node_cur_'] = label
    elif _g.dict[n]['tag_'] == node_tag.NODE_GOSUB:
        label_node = _g.dict[n]['left_']
        if label_node != None:
            sys.stdout.write('error28')
            sys.exit()
        if _g.dict[label_node]['tag_'] == node_tag.NODE_LABEL:
            sys.stdout.write('error29')
            sys.exit()
        tmp = _g.dict[label_node]['token_']
        label_name = _g.dict[tmp]['content_']
        label = search_label(e, label_name)
        if label == None:
            print("gosub: Label not found.@@ %s", label_name) # gosub：ラベルがみつかりません
            sys.exit()
        if (_g.dict[s]['current_call_frame_'] + 1) >= MAX_CALL_FRAME:
            print("gosub: Nesting is too deep.") # gosub：ネストが深すぎます
            sys.exit()
        _g.dict[s]['current_call_frame_'] += 1
        _g.dict[s]['call_frame_'][_g.dict[s]['current_call_frame_'] - 1]['caller_'] = _g.dict[s]['node_cur_']
        _g.dict[s]['node_cur_'] = label
    elif _g.dict[n]['tag_'] == node_tag.NODE_REPEAT:
        if _g.dict[s]['current_loop_frame_'] + 1 >= MAX_LOOP_FRAME:
            print("repeat: Nesting is too deep.") # repeat：ネストが深すぎます
            sys.exit()
        _g.dict[s]['current_loop_frame_'] += 1
        _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['start_'] = _g.dict[s]['node_cur_']
        _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['cnt_'] = 0
        _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['counter_'] = 0
        _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['max_'] = 0
        loop_num = -1
        if _g.dict[n]['left_']:
            evaluate(e, s, _g.dict[n]['left_'])
            v = stack_peek(_g.dict[s]['stack_'], -1)
            loop_num = value_calc_int(v)
            stack_pop(_g.dict[s]['stack_'], 1)
        _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['max_'] = loop_num
    elif _g.dict[n]['tag_'] == node_tag.NODE_REPEAT_CHECK:
        if _g.dict[s]['current_loop_frame_'] > 0:
            sys.stdout.write('error30')
            sys.exit()
        if _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['max_'] >= 0 and _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['counter_'] >= _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['max_']:
            depth = 0
            while _g.dict[s]['node_cur_'] != None:
                tmp = _g.dict[s]['node_cur_']
                ex = _g.dict[tmp]['value_']
                if _g.dict[ex]['tag_'] == node_tag.NODE_REPEAT:
                    depth += 1
                elif _g.dict[ex]['tag_'] == node_tag.NODE_LOOP:
                    if depth == 0:
                        depth -= 1
                        break
                tmp = _g.dict[s]['node_cur_']
                _g.dict[s]['node_cur_'] = _g.dict[tmp]['next_']
            if _g.dict[s]['node_cur_'] != None:
                sys.stdout.write('error31')
                sys.exit()
            _g.dict[s]['current_loop_frame_'] -= 1
    elif _g.dict[n]['tag_'] == node_tag.NODE_LOOP or _g.dict[n]['tag_'] == node_tag.NODE_CONTINUE:
        if _g.dict[s]['current_loop_frame_'] <= 0:
            print("loop,continue: is not in repeat-loop.") # loop,continue：repeat-loopの中にありません
            sys.exit()
        _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['counter_'] += 1
        _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['cnt_'] += 1
        _g.dict[s]['node_cur_'] = _g.dict[s]['loop_frame_'][_g.dict[s]['current_loop_frame_'] - 1]['start_']
    elif _g.dict[n]['tag_'] == node_tag.NODE_BREAK:
        if _g.dict[s]['current_loop_frame_'] <= 0:
            print("break: is not in repeat-loop.") # break：repeat-loopの中にありません
        depth = 0
        while _g.dict[s]['node_cur_'] != None:
            tmp = _g.dict[s]['node_cur_']
            ex = _g.dict[tmp]['value_']
            if _g.dict[ex]['tag_'] == node_tag.NODE_REPEAT:
                depth -= 1
            elif _g.dict[ex]['tag_'] == node_tag.NODE_LOOP:
                if depth == 0:
                    depth -= 1
                    break
            tmp = _g.dict[s]['node_cur_']
            _g.dict[s]['node_cur_'] = _g.dict[tmp]['next_']
        if _g.dict[s]['node_cur_'] == None:
            print("break: couldn't repeat-loop in goto, and break."); # break：repeat-loopをうまく抜けられませんでした、repeat-loop間でのgoto後にbreakなどはできません
            sys.exit()
        _g.dict[s]['current_loop_frame_'] -= 1
    elif _g.dict[n]['tag_'] == node_tag.NODE_IF:
        if _g.dict[n]['left_'] != None:
            sys.stdout.write('error32')
            sys.exit()
        evaluate(e, s, _g.dict[n]['left_'])
        if _g.dict[n]['right_'] != None:
            sys.stdout.write('error33')
            sys.exit()
        dispatcher = _g.dict[n]['right_']
        if _g.dict[dispatcher]['tag_'] == node_tag.NODE_IF_DISPATCHER:
            sys.stdout.write('error34')
            sys.exit()
        cond = stack_peek(_g.dict[s]['stack_'], -1)
        is_cond = value_calc_boolean(cond)
        stack_pop(_g.dict[s]['stack_'], 1)
        if is_cond:
            evaluate(e, s, _g.dict[dispatcher]['left_'])
        else:
            if _g.dict[dispatcher]['right_']:
                evaluate(e, s, _g.dict[dispatcher]['right_'])
    elif _g.dict[n]['tag_'] == node_tag.NODE_IF_DISPATCHER:
        #assert(false);
        pass
    elif _g.dict[n]['tag_'] == node_tag.NODE_IF_CHECK:
        if _g.dict[n]['ext_'] != None:
            sys.stdout.write('error35')
            sys.exit()
        c = _g.dict[n]['ext_']
        evaluate(e, s, c)
        cond = stack_peek(_g.dict[s]['stack_'], -1)
        is_cond = value_calc_boolean(cond)
        stack_pop(_g.dict[s]['stack_'], 1)
        if not is_cond:
            tmp = _g.dict[s]['node_cur_']
            _g.dict[s]['node_cur_'] = _g.dict[tmp]['next_']
    elif _g.dict[n]['tag_'] == node_tag.NODE_JUMP_LABEL:
        pass
    elif _g.dict[n]['tag_'] == node_tag.NODE_JUMP_INTERNAL:
        if _g.dict[n]['ext_'] != None:
            sys.stdout.write('error36')
            sys.exit()
        _g.dict[s]['node_cur_'] = _g.dict[n]['ext_']
    else:
        #assert(false)
        pass
    return

def execute(e):
    global _g
    s = new_execute_status_t()
    initialize_execute_status(s)
    tmp = _g.dict[e]['statement_list_']
    s.node_cur_ = _g.dict[tmp]['head_']
    if _g.dict[s]['node_cur_'] == None:
        print("No executable node.@@ [%p]", e) # 実行できるノードがありません
    while True:
        ex = _g.dict[s]['node_cur_']['value_']
        tmp = _g.dict[s]['stack_']
        top = _g.dict[tmp]['top_']
        evaluate(e, s, ex)
        tmp = _g.dict[s]['stack_']
        if top == _g.dict[tmp]['top_']:
            sys.stdout.write('error37')
            sys.exit()
        if _g.dict[s]['is_end_']: # もう実行終わったらしい、帰る
            break
        tmp = _g.dict[s]['node_cur_']
        _g.dict[s]['node_cur_'] = _g.dict[tmp]['next_']
        if _g.dict[s]['node_cur_'] == None: # もう実行できるastがない、帰る
            break
    uninitialize_execute_status(s)

# ビルトイン
def query_command(s):
    table = {
        builtin_command_tag.COMMAND_DEVTERM: "devterm",
        builtin_command_tag.COMMAND_DIM: "dim",
        builtin_command_tag.COMMAND_DDIM: "ddim",
        builtin_command_tag.COMMAND_SDIM: "sdim",
        builtin_command_tag.COMMAND_RANDOMIZE: "randomize",
        builtin_command_tag.COMMAND_BLOAD: "bload",
        builtin_command_tag.COMMAND_POKE: "poke",
        builtin_command_tag.COMMAND_INPUT: "input",
        builtin_command_tag.COMMAND_MES: "mes",
    }
	# 全探索
    for key in table:
        if string_equal_igcase(s, table[key], -1):
            return key
    return -1

def get_command_delegate(command):
    global command_delegate
    return command_delegate[command]

def query_function(s):
    table = {
        builtin_function_tag.FUNCTION_INT: "int",
        builtin_function_tag.FUNCTION_DOUBLE: "double",
        builtin_function_tag.FUNCTION_STR: "str",
        builtin_function_tag.FUNCTION_RND: "rnd",
        builtin_function_tag.FUNCTION_ABS: "abs",
        builtin_function_tag.FUNCTION_POWF: "powf",
        builtin_function_tag.FUNCTION_PEEK: "peek",
    }
    # 全探索
    for key in table:
        if string_equal_igcase(s, table[key], -1):
            return key
    return -1

def get_function_delegate(function):
    global function_delegate
    return function_delegate[function]


def main():
    args = sys.argv
    filename = None
    if len(args) >= 2:
        filename = args[1]
    else:
        filename = "start.hsp"
    script = None
    file = open(filename, 'r')
    if file == None:
        print("ERROR: スクリプトファイルの読み込みに失敗しました %s\n", filename) #cannot read such file
        return -1
    script = file.read()
    file.close()
    if script == None:
        sys.stdout.write('ERROR: スクリプトファイルを正常に読み込めませんでした')
        sys.exit()
    script += '\0'
    # 実行
    env = create_execute_environment()
    load_script(env, script)
    execute(env)
    destroy_execute_environment(env)
    # 各種解放
    del script

if __name__ == "__main__":
    main()