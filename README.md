# CACT 编译器实验

本项目基于课程 CACT 框架，使用 ANTLR 4.13.1 实现 CACT 语言的词法和语法分析。

目前已完成 **PR001** 的分析器、命令行接口和公开样例测试。PR002 的语义分析、IR 与解释执行，以及 PR003 的 RISC-V 代码生成尚未实现。

## 环境要求

- Linux 环境（Windows 可使用 WSL）
- 支持 C++17 的编译器、CMake 3.16 或更高版本
- Java 11 或更高版本
- Python 3（用于运行测试）

ANTLR 4.13.1 的生成器和 C++ runtime 已包含在 `deps/` 中。

## 构建和运行

在仓库根目录执行：

```bash
cmake -S . -B build
cmake --build build -j 4
./build/compiler test/samples_lex_and_syntax/00_true_main.cact
echo $?
```

编译器接收一个 CACT 源文件路径。词法、语法正确时返回 `0`，词法或语法错误返回 `1`，参数、文件或其他分析异常返回 `2`。诊断信息输出到标准错误，包含行号和列号。

## 测试

```bash
ctest --test-dir build --output-on-failure
```

也可以直接运行测试脚本并保存逐项结果：

```bash
python3 test/test_pr001.py build/compiler results.json
```

加入 `double` 后，本地通过课程原有脚本的 27 个公开样例，以及 64 个边界用例和 3 个命令行用例。此前版本在课程集群的测试结果保留在记录中；更新后的版本尚未在集群复测。隐藏样例尚未验证，详见 [TESTING.md](TESTING.md)。

## PR001

支持关键字、标识符、常量、注释，变量和常量声明、多维数组、函数定义及调用，以及控制语句、算术表达式和条件表达式。按小组要求，文法允许 `double` 类型的声明、数组和函数；这是一项相对于课程规范中三种基本类型说明的扩展。程序检查完整输入并匹配文件结束符；赋值作为语句处理，不支持连续赋值。

本阶段不检查标识符定义、类型匹配和 `break` 所处上下文等语义问题。课程规范中初始化相关描述存在不一致，当前实现结合说明和公开样例，允许字面量及嵌套初始化列表，拒绝使用变量、函数调用或算术表达式作为声明初值。其他取舍见 [实验报告](实验报告.md)。

## 项目结构

| 路径 | 内容 |
| --- | --- |
| `grammar/CACT.g4` | CACT 词法与语法规则 |
| `src/main.cpp` | 文件输入与错误处理 |
| `deps/` | ANTLR 生成器和 C++ runtime |
| `test/samples_lex_and_syntax/` | 课程公开词法语法样例 |
| `test/test_pr001.py` | 公开样例、边界和命令行测试 |
| `TESTING.md` | 测试记录与限制 |
| `report/main.tex`、`report/main.pdf` | PR001 实验报告及 LaTeX 源码 |
| `实验报告.md` | PR001 实验报告 Markdown 草稿 |
| `README.course.md` | 课程原始框架说明 |

`grammar/Hello.g4` 是课程入门示例，当前编译器使用 `CACT.g4`。ANTLR 生成的分析器文件位于构建目录，不需要手工修改。
