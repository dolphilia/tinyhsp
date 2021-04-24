#include <stdio.h>
#include <stdlib.h>

typedef struct list_node_tag list_node_t;
struct list_node_tag
{
	list_node_t* prev_;
	list_node_t* next_;
	void* value_;
};

list_node_t*
create_list_node()
{
	list_node_t* res = (list_node_t*)malloc(sizeof(list_node_t));
	res->prev_ = res->next_ = NULL;
	res->value_ = NULL;
	return res;
}

int main() {

    list_node_t* a = create_list_node();

    return 0;
}