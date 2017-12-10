import sys
sys.path.append("../src")
from org.tbollmeier.transfero import *

code = """
SELECT * FROM users where name="drbolle";
"""

print(code)
print()

sql = Grammar(case_sensitive = False)\
    .add_comment("(*", "*)")\
    .add_comment("--", "\n")\
    .add_keyword("SELECT")\
    .add_keyword("FROM")\
    .add_keyword("WHERE")\
    .add_token("ASTERISK", r"\*")\
    .add_token("ASSIGN", "=")\
    .add_token("SEMICOLON", ";")\
    .add_token("ID", "[a-zA-Z_][a-zA-Z_0-9]*")\
    .add_token("STRING", '"[^"]*"')

sql.rule('select',
         Sequence(
            TokenType('SELECT'),
            Rule('field_list', 'fields'),
            TokenType('FROM'),
            TokenType('ID', 'table'),
            Optional(Rule('where_clause', 'where'))),
        is_root=True)
@sql.ast_transform('select')
def select(ast):
    ret = Ast('select_stmt')
    fields = ast.find_children_by_id('fields')[0]
    fields.id = ""
    ret.add_child(fields)
    table = ast.find_children_by_id('table')[0]
    table.id = ""
    ret.add_child(table)
    where = ast.find_children_by_id('where')
    if where:
        where = where[0]
        where.id = ""
        ret.add_child(where)
    return ret

sql.rule('field_list', TokenType('ASTERISK'))
@sql.ast_transform('field_list')
def field_list(ast):
    children = ast.get_children()
    if len(children) == 1 and children[0].name == 'ASTERISK':
        return Ast("all_fields")
    else:
        return ast

sql.rule('where_clause',
         Sequence(
            TokenType('WHERE'),
            TokenType('ID', 'field'),
            TokenType('ASSIGN'),
            OneOf(
                TokenType('ID', 'rhs'),
                TokenType('STRING', 'rhs'))))

ast = Parser(sql).parse(code)

print(ast.to_json())



