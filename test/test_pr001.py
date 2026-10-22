#!/usr/bin/env python3
"""Run official syntax fixtures and independent language boundary cases."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

CASES = [
    ("minimal", True, "int main(){return 0;}"),
    ("integers", True, "int a=0,b=123,c=077,d=0xFA,e=-12;"),
    ("floats", True, "float a=.5f,b=8.f,c=1e3F,d=-43.0e-4F,e=9.00,f=3E2f;"),
    ("characters", True, r"char a='a',b='\n',c='\t',d='\\',e='\'',f='\"',g='\0';"),
    ("arrays", True, "const int a[2][2]={{1,2},{3,4}}; int b[4]={};"),
    ("parameters", True, "int f(int x,char y[][3],float z[2][3]){return x;}"),
    ("operators", True, "int main(){int a; a=-1+2*3%4/2; return +(a-1);}"),
    ("condition", True, "int main(){if(!(1<2)||3>=4&&5!=6)return 1;else return 0;}"),
    ("arithmetic_in_condition", True, "int main(){if((1+2)*3<10)return 0;}"),
    ("dangling_else", True, "int main(){if(1)if(0)return 0;else return 1;}"),
    ("loop", True, "void f(){while(1){if(0)break;else continue;}return;}"),
    ("calls", True, "int main(){f(1,2+3);return get_int();}"),
    ("comments", True, "// header\r\nint/* gap */main(){/**/return 0;}// eof"),
    ("keyword_prefix", True, "int returnValue=1,ifx=2,_a2=3,IF=4;"),
    ("empty_statement", True, "void f(){;{};return;}"),
    ("syntax_only", True, "int main(){unknown=other();break;return 0;}"),
    ("empty_file", False, ""),
    ("comment_only", False, "/* comment */"),
    ("trailing_character", False, "int main(){return 0;}@"),
    ("trailing_identifier", False, "int main(){return 0;}garbage"),
    ("missing_semicolon", False, "int main(){return 0}"),
    ("missing_brace", False, "int main(){return 0;"),
    ("missing_paren", False, "int main({return 0;}"),
    ("incomplete_expr", False, "int main(){return 1+;}"),
    ("hex_no_digits", False, "int a=0x;"),
    ("hex_bad_digit", False, "int a=0x3fG;"),
    ("bad_octal", False, "int a=08;"),
    ("integer_suffix", False, "int a=1u;"),
    ("integer_separator", False, "int a=1_000;"),
    ("float_integer_suffix", False, "float a=3f;"),
    ("float_missing_exp", False, "float a=1e+;"),
    ("float_no_digits", False, "float a=.f;"),
    ("bad_identifier", False, "int 7a=1;"),
    ("reserved_identifier", False, "int return=1;"),
    ("string", False, 'char a="a";'),
    ("empty_char", False, "char a='';"),
    ("long_char", False, "char a='ab';"),
    ("unicode_char", False, "char a='中';"),
    ("bad_escape", False, r"char a='\q';"),
    ("unterminated_char", False, "char a='a;"),
    ("unterminated_comment", False, "int main(){return 0;}/*"),
    ("nested_comment", False, "/* outer /* inner */ */ int main(){return 0;}"),
    ("initializer_variable", False, "const int a=1; int b=a;"),
    ("initializer_expression", False, "int a=2*3;"),
    ("initializer_call", False, "int a=f();"),
    ("dimension_expression", False, "int a[1+2];"),
    ("dimension_identifier", False, "const int n=2; int a[n];"),
    ("unsized_variable", False, "int a[];"),
    ("unsized_inner_parameter", False, "void f(int a[][]){}"),
    ("function_prototype", False, "int f();"),
    ("nested_function", False, "void f(){void g(){}}"),
    ("chained_assignment", False, "void f(){a=b=c;}"),
    ("comparison_assignment", False, "void f(){a=b<c;}"),
    ("logic_in_return", False, "int f(){return !a;}"),
    ("comma_expression", False, "void f(){a=1,2;}"),
    ("array_comma", False, "void f(){a[1,2]=0;}"),
    ("for_loop", False, "void f(){for(;;);}"),
    ("increment", False, "void f(){a++;}"),
    ("double_type", False, "double a=1.0;"),
    ("const_missing_init", False, "const int a;"),
    ("initializer_trailing_comma", False, "int a[2]={1,2,};"),
]


def main():
    exe = Path(sys.argv[1]).resolve()
    results = []

    def check(name, expected, path, group):
        run = subprocess.run([str(exe), str(path)], capture_output=True, text=True, timeout=15)
        passed = (run.returncode == 0) == expected
        results.append({"name": name, "group": group, "expected_valid": expected,
                        "returncode": run.returncode, "passed": passed})
        if not passed:
            print("FAIL", name, "returncode=", run.returncode, run.stderr)

    fixtures = Path(__file__).resolve().parent / "samples_lex_and_syntax"
    for path in sorted(fixtures.glob("*.cact")):
        match = re.match(r"\d+_(true|false)_", path.name)
        if not match:
            raise ValueError("Fixture has no validity label: " + path.name)
        check(path.name, match[1] == "true", path, "official")
    with tempfile.TemporaryDirectory(prefix="cact-pr001-") as directory:
        root = Path(directory)
        for name, expected, code in CASES:
            path = root / (name + ".cact")
            path.write_text(code, encoding="utf-8")
            check(name, expected, path, "boundary")
        for name, args in (("no_argument", []), ("extra_argument", ["a", "b"]),
                           ("missing_file", [str(root / "missing.cact")])):
            run = subprocess.run([str(exe), *args], capture_output=True, timeout=15)
            passed = run.returncode != 0
            results.append({"name": name, "group": "cli", "passed": passed,
                            "returncode": run.returncode})
            if not passed:
                print("FAIL", name)
    for group in ("official", "boundary", "cli"):
        selected = [r for r in results if r["group"] == group]
        print(f"{group}: {sum(r['passed'] for r in selected)}/{len(selected)} passed")
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
