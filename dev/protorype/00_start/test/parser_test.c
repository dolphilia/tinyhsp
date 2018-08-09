#include "../src/parser.h"

double
parse_line(void)
{
	double value;
	set_st_token_exists(0);
	value = parser_main();
	//value = parser_expression();
	return value;
}

int
main(int argc, char** argv)
{
	char line[LINE_BUF_SIZE];
	double value;
	while (fgets(line, LINE_BUF_SIZE, stdin) != NULL) {
		set_line(line);
		value = parse_line();
		printf(">>%f\n", value);
	}
	return 0;
}