import sys
sys.path.append("../src")
from org.tbollmeier.transfero.scanner import Scanner

code = """
SELECT * FROM users where name="drbolle";
"""

print(code)
print()

scanner = Scanner(case_sensitive = False)\
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

tokens = scanner.find_tokens(code)

for token in tokens:
    print("Token: ", token)





