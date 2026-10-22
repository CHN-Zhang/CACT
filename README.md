# 实验二 CACT 编译器 PR001

本项目实现 CACT 词法与语法检查，基于课程 CACT-PR0-2026S 框架和 ANTLR 4.13.1。
Java 生成器与 C++ runtime 随源码提供，首次构建不需要下载第三方依赖。

## 构建与运行

需要 Linux、C++17 编译器、Java 11+、CMake 3.16+；测试脚本需要 Python 3。

```bash
cmake -S . -B build
cmake --build build -j 4
./build/compiler test/samples_lex_and_syntax/00_true_main.cact
echo $?
ctest --test-dir build --output-on-failure
```

也可以运行课程原测试脚本：

```bash
cd test
bash test_syntax.sh
```

Windows 用户使用已部署的 D 盘 CompilerLab WSL 环境，在 PowerShell 中执行本目录的 `build.ps1`。
构建产物放在 Linux `/opt/compiler-lab/build/pr001`，实际磁盘位于 D 盘。

```powershell
.\build.ps1
wsl -d CompilerLab -- /opt/compiler-lab/build/pr001/compiler /mnt/e/编译原理lab/hw1/CACT-PR001/test/samples_lex_and_syntax/00_true_main.cact
```

## 接口与范围

`compiler <source.cact>`：正确输入返回 0，词法或语法错误返回 1；参数、文件或其他分析异常返回 2。
诊断写入 stderr，包含从 1 开始的行号、列号。程序会读取完整文件并匹配 EOF。

支持声明、字面量初始化、多维数组、函数定义和调用、控制流、算术表达式及条件表达式。
赋值、普通表达式、条件表达式分别建模；不支持赋值表达式和连续赋值。
声明初值只接受常量字面量（数值可带正负号）及嵌套列表，数组维度只接受整数字面量。
条件中支持括号分组与逻辑非；逻辑非与算术一元运算同级，高于乘除。
`else` 由 ANTLR 的可选分支优先匹配到最近的未匹配 `if`。

不进行符号表、类型匹配、函数是否定义、break 所处上下文等 PR002 语义检查。
不生成 IR 或 RISC-V 汇编。

## 规范取舍

课程规范中的初始化文法与例子不完全一致；按文字说明及公开样例执行严格字面量初始化。
`return` 按正常语句要求分号；十进制整数允许多位。
关键字表中的 `double` 保留为关键字，但基本类型按 BType 只支持 int、float、char。
无 f 后缀的十进制浮点格式在词法阶段接受；赋值类型是否匹配留待 PR002。
这些选择均写入边界测试，便于后续按课程澄清调整。

## 文件

- `grammar/CACT.g4`：语言文法；ANTLR 生成文件位于 build/generated，不手工修改。
- `src/main.cpp`：文件输入、词法及语法错误处理。
- `test/test_pr001.py`：自动检查公开样例、边界输入和命令行行为。
- `test-results-local.json`、`test-results-cluster.json`：本地与集群逐项验证结果，两端均 91/91 通过。
- `TESTING.md`：验证范围与限制。
- `实验报告.md`：技术报告，组号、成员和分工需按真实信息补齐。
- `README.course.md`：保留的课程原始说明，包含后续实验信息。

`grammar/Hello.g4` 是保留的课程入门示例，不参与当前 compiler 构建。

集群最终源码位于 `/root/compiler-lab/pr001-final/CACT-PR001`，独立 Release 编译器位于
`/root/compiler-lab/pr001-final-build/compiler`。已使用集群 G++ 11.4.0 完成构建和全部测试。

## 提交

尚未创建远程仓库或提交到课程平台。按任务书创建小组 CACT 仓库，推送完整源码并标记 `CACT-PR1`。
提交前补全报告的组号与成员信息；隐藏测试需要课程验收环境，当前不能声称已通过。
