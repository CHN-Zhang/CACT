# PR001 验证记录

验证日期：2026-10-17。

| 检查 | 结果 |
| --- | --- |
| 课程公开词法语法样例 | 27/27 |
| 独立边界用例 | 61/61 |
| 参数缺失、多余参数、文件不存在 | 3/3 |
| PowerShell build.ps1 构建入口 | 通过 |
| CTest 自动测试入口 | 通过 |
| 源码压缩包解压到 D 盘新目录后独立 Release 构建 | 通过 |
| 独立 Release 构建的全部 91 项测试 | 通过 |
| 课程集群独立 Release 构建（G++ 11.4.0） | 通过 |
| 课程集群公开 / 边界 / 命令行测试 | 27/27、61/61、3/3 |
| 课程 deps 与原始框架逐文件比对 | 相同 |
| 公开样例与原始框架逐文件比对 | 相同 |

本地工具：Ubuntu 24.04 WSL，G++ 13.3.0，Java 17.0.20.1，CMake 3.28.3，ANTLR 4.13.1。
完整逐项结果在 test-results-local.json 中。

公开样例共 9 个语法正确用例、18 个语法错误用例。
其中 15_true_syntax_false_semantic.cact 应判为语法正确，本次不提前实施 PR002 语义检查。

PR001 最终源码包已在课程集群独立解压、构建和验证，逐项结果在 test-results-cluster.json。
集群源码目录为 /root/compiler-lab/pr001-final/CACT-PR001，构建目录为 /root/compiler-lab/pr001-final-build。
隐藏样例无法在本地取得，未作通过声明。
