"""
pkgutil.iter_modules / pkgutil.walk_packages 使用示例

说明：
- 演示如何列出某个包目录下的模块（不递归）
- 演示如何递归遍历包下的子模块/子包
- 演示如何根据发现的模块名用 importlib 导入模块

运行：
    python3 pkgutil_examples.py

脚本会在同一目录下包含的 `sample_pkg` 包上运行（仓库已创建用于演示的小包）。
"""

import pkgutil
import sample_pkg
import os

print("sample_pkg path:", sample_pkg.__path__)
print()

# ========== 列出 sample_pkg 下的顶级模块（非递归） ==========
print("Top-level modules under sample_pkg (non-recursive) using pkgutil.iter_modules:")
for finder, name, ispkg in pkgutil.iter_modules(sample_pkg.__path__):
    print(f"  name={name}, ispkg={ispkg}")
print()

# ========== 递归遍历 package 下所有子模块/子包 ==========
print("All modules under sample_pkg (recursive) using pkgutil.walk_packages:")
for finder, name, ispkg in pkgutil.walk_packages(sample_pkg.__path__, prefix=sample_pkg.__name__ + "."):
    print(f"  {name} (ispkg={ispkg})")
print()

# ========== 列出发现的顶级模块（不导入，仅显示） ==========
print("Discovered top-level modules under sample_pkg (non-recursive):")
for _finder, name, ispkg in pkgutil.iter_modules(sample_pkg.__path__):
    print(f"  {name} (ispkg={ispkg})")
print()

# ========== 演示：遍历子包并导入子模块 ==========
print("Discovered modules under sample_pkg (recursive) (listing only, no import):")
for _finder, name, ispkg in pkgutil.walk_packages(sample_pkg.__path__, prefix=sample_pkg.__name__ + "."):
    print(f"  {name} (ispkg={ispkg})")

print()
print("Demo finished.")


# Note: importlib usage removed from this tutorial to keep focus on pkgutil.
print('\n(importlib examples removed; this tutorial focuses on pkgutil.iter_modules / walk_packages)')

# ---------- 可选示例：使用 prefix 直接导入并做接口检查 ----------
print('\nExample: iter_modules with prefix -> list full module names (no import)')

# More readable, step-by-step version of the one-liner list comprehension:
pkg_prefix = sample_pkg.__name__ + '.'
iterator = pkgutil.iter_modules(sample_pkg.__path__, prefix=pkg_prefix)
full_names = []
for finder, module_name, is_pkg in iterator:
    # `module_name` already includes the prefix, e.g. 'sample_pkg.a'
    full_names.append(module_name)

# Debug prints requested: show prefix and iterator (repr/type)
print('\nDEBUG: pkg_prefix =', repr(pkg_prefix))
print('DEBUG: iterator repr =', repr(iterator))
print('DEBUG: iterator type =', type(iterator))
print(f"full name: {full_names}")

for nm in full_names:
    print(f"  {nm}")

print('\n(prefix listing only; no dynamic import performed)')

