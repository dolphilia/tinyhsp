# coding: UTF-8
import sys
from enum import Enum

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

# 擬似構造体
global_struct_index = 0

def new_list_node_t(prev_ = 0, next_ = 0, value_ = 0):
    res = {
        global_struct_index : { 
            'type': 'list_node_t',
            'prev_': prev_, # *list_node_t
            'next_': next_, # *list_node_t
            'value_': value_, # *void
        },
    }
    global_struct_index += 1
    return res

def new_list_node_t(head_ = 0, tail_ = 0):
    res = {
        global_struct_index : { 
            'type': 'list_t',
            'head_': head_, # *list_node_t
            'tail_': tail_,  # *list_node_t
        },
    }
    global_struct_index += 1
    return res

def new_token_t(tag_ = 0, content_ = '', cursor_begin_ = 0, cursor_end_ = 0, appear_line_ = 0, left_space_ = None, right_space_ = None):
    res = {
        global_struct_index : { 
            'type': 'token_t',
            'tag_': tag_, # token_tag
            'content_': content_, # string //*char
            'cursor_begin_': cursor_begin_, #int
            'cursor_end_': cursor_end_, #int
            'appear_line_': appear_line_, #int
            'left_space_': left_space_, #bool
            'right_space_': right_space_, #bool
        },
    }
    global_struct_index += 1
    return res

def new_tokenize_context_t(script_ = '', cursor_ = 0, line_ = 0, line_head_=''):
    res = {
        global_struct_index : {
            'type': 'tokenize_context_t', # stract
            'script_': script_, # string //const
	        'cursor_': cursor_, # int
	        'line_': line_, # int
	        'line_head_': line_head_, # string //const
        },
    }
    global_struct_index += 1
    return res

def new_ast_node_t(tag_ = 0, token_ = 0, left_ = 0, right_ = 0, flag_ = 0, ext_ = 0):
    res = {
        global_struct_index : {
            'type': 'ast_node_t',
            'tag_': tag_, # node_tag
            'token_': token_, # *token_t
            'left_': left_, # *ast_node_t
            'right_': right_, # *ast_node_t
            'flag_': flag_, # uint
            'ext_': ext_, # *void
        },
    }
    global_struct_index += 1
    return res

def new_parse_context_t():
    res = {
        global_struct_index : {
            'type': 'parse_context_t',
            'token_list_': 0, # *list_t
            'token_current_': 0, # *list_node_t
            'tokenize_context_': 0, # *tokenize_context_t
        },
    }
    global_struct_index += 1
    return res

def new_value_t_(value_t_ = 0):
    res = {
        global_struct_index : {
            'type': 'value_t_',
            'value_t_': value_t_,
        },
    }
    global_struct_index += 1
    return res

def new_variable_t(name_ = '', type_ = 0, granule_size_ = 0, length_ = 0, data_ = 0):
    res = {
        global_struct_index : {
            'type': 'variable_t',
            'name_': name_, # string
            'type_': type_, # value_tag
            'granule_size_': granule_size_, # int
            'length_': length_, #int
            'data_': data_, #*void
        },
    }
    global_struct_index += 1
    return res

def new_value_t(type_ = 0, ivalue_ = 0, dvalue_ = 0.0, svalue_ = '', variable_ = 0, index_ = 0, value_ = 0):
    res = {
        global_struct_index : {
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
    }
    global_struct_index += 1
    return res

def new_value_stack_t(stack_ = 0, top_ = 0, max_ = 0):
    res = {
        global_struct_index : {
            'type': 'value_stack_t',
            'stack_': stack_, #**value_t
            'top_': top_, #int
            'max_': max_, #int
        },
    }
    global_struct_index += 1
    return res

def new_label_node_t(name_ = '', statements_ = 0):
    res = {
        global_struct_index : {
            'type': 'label_node_t',
            'name_': name_, #string //char*
            'statement_': statements_, #*list_node_t
        },
    }
    global_struct_index += 1
    return res

def new_call_frame_t(caller_ = 0):
    res = {
        global_struct_index : {
            'type': 'call_frame_t',
            'caller_': caller_, #*list_node_t
        },
    }
    global_struct_index += 1
    return res

def new_loop_frame_t(start_ = 0, counter_ = 0, max_ = 0, cnt_ = 0):
    res = {
        global_struct_index : {
            'type': 'loop_frame_t',
            'start_': 0, #list_node_t
            'counter_': 0, # int
            'max_': 0, #int
            'cnt_': 0, #int
        },
    }
    global_struct_index += 1
    return res

def new_execute_environment_t(parser_list_ = 0, ast_list_ = 0, statement_list_ = 0, label_table_ = 0, variable_table_ = 0):
    res = {
        global_struct_index : {
            'type': 'execute_environment_t',
            'parser_list_': parser_list_, # *list_t
            'ast_list_': ast_list_, # *list_t
            'statement_list_': statement_list_, # *list_t
            'label_table_': label_table_, # *list_t
            'variable_table_': variable_table_, # *list_t
        },
    }
    global_struct_index += 1
    return res

def new_execute_status_t(stack_ = 0, node_cur_ = 0, call_frame_ = [], current_call_frame_ = 0, loop_frame_ = [], current_loop_frame_ = 0, is_end_ = None, stat_ = 0, refdval_ = 0, refstr_ = 0, strsize_ = 0):
    res = {
        global_struct_index : {
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
    }
    global_struct_index += 1
    return res

struct_model = {}

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
	res = new_list_node_t()
	res['prev_'] = None
	res['next_'] = None
	res['value_'] = None
	return res

def unlink_list_node(node):
	if node['prev_'] == None and node['next_'] == None:
		return False
	if node['prev_'] != None:
		node['prev_']['next_'] = node['next_']
	if node['next_'] != None:
		node['next_']['prev_'] = node['prev_']
	node['prev_'] = None
	node['next_'] = None
	return True

def destroy_list_node(node):
	unlink_list_node(node)
	node = None

def link_next(node, list):
	if node['prev_'] != None or node['next_'] != None:
		sys.stdout.write('error')
	node['prev_'] = list
	node['next_'] = list['next_']
	list['next_'] = node

def link_prev(node, list):
	if node['prev_'] != None or node['next_'] != None:
		sys.stdout.write('error')
	node['prev_'] = list['prev_']
	node['next_'] = list
	list['prev_'] = node

print(struct_model)
print(command_delegate)