"""
collections.abc.Callable 使用示例

说明（中文注释）:
- `Callable` 常用来做类型提示（type hints），表示一个可调用对象（函数、实现 __call__ 的对象等）。
- 可以在运行时用 `isinstance(obj, Callable)` 检查对象是否可调用。
- 在类型提示中可以写成 `Callable[[Arg1Type, Arg2Type], ReturnType]` 或 `Callable[..., ReturnType]`。

运行: `python3 collections/callable_examples.py`
"""

from collections.abc import Callable
from typing import Any

# ---------- 示例 1：基本类型提示 ----------
# 表示 f 接受两个 int，返回 int
def apply_func(f: Callable[[int, int], int], a: int, b: int) -> int:
    return f(a, b)


def add(x: int, y: int) -> int:
    return x + y

print("示例 1: 基本类型提示")
print("  add(2,3) ->", apply_func(add, 2, 3))
print()

# ---------- 示例 2：可变参数的 Callable ----------
# Callable[..., Any] 表示任意参数，任意返回类型（常用于不知道签名时）
def call_any(f: Callable[..., Any], *args, **kwargs) -> Any:
    return f(*args, **kwargs)

print("示例 2: Callable[..., Any]")
print("  upper ->", call_any(str.upper, "hello"))
print("  pow ->", call_any(pow, 2, 5))
print()

# ---------- 示例 3：运行时检查是否可调用 ----------
class A:
    def __call__(self, x):
        return f"A called with {x}"


a = A()
print("示例 3: 运行时检查")
print("  is add callable?", isinstance(add, Callable))
print("  is a callable?", isinstance(a, Callable))
print("  call a ->", a(10))
print()

# ---------- 示例 4：高阶函数的类型 ----------
# 表示返回一个可调用对象：接收 str 返回一个接受 int 的函数，该函数返回 str
H = Callable[[str], Callable[[int], str]]

def make_prefixer(prefix: str) -> Callable[[int], str]:
    def prefixer(n: int) -> str:
        return f"{prefix}:{n}"
    return prefixer


def use_higher(h: H) -> None:
    f = h("tag")
    print("示例 4: 高阶函数 ->", f(7))

use_higher(make_prefixer)
print()

# ---------- 示例 5：在注释中和运行时的区别 ----------
# 右侧的类型注解主要用于静态类型检查 (mypy / IDE)，运行时并不会阻止传错类型。
# 如果需要在运行时强制类型检查，需要额外代码或第三方库。

print("示例 5: 注解只是提示，运行时不会阻止错误类型")
print("  apply_func(add, 'x', 'y') 会在运行时抛出 TypeError 或产生不可预期结果")

# 测试：故意传入不匹配的参数以展示运行时行为（注释掉以避免真实错误）
print(apply_func(add, 'x', 'y'))

print('\n示例脚本执行完毕')


# ================= 实践场景示例 =================
print('\n' + '='*30 + ' 实践场景 ' + '='*30 + '\n')

# ---------- 场景 A：插件/命令注册器 ----------
print('场景 A: 插件/命令注册器')
registry: dict[str, Callable[..., Any]] = {}

def register(name: str, fn: Callable[..., Any]) -> None:
    registry[name] = fn

def run_command(name: str, *args, **kwargs) -> Any:
    if name not in registry:
        raise KeyError(f'命令未注册: {name}')
    return registry[name](*args, **kwargs)

register('sum', add)
register('pow', pow)
print('  registry keys ->', list(registry.keys()))
print('  run_command("sum", 4, 5) ->', run_command('sum', 4, 5))
print('  run_command("pow", 2, 8) ->', run_command('pow', 2, 8))
print()


# ---------- 场景 B：事件/回调系统 ----------
print('场景 B: 事件/回调系统')
listeners: list[Callable[[str], None]] = []

def add_listener(fn: Callable[[str], None]) -> None:
    listeners.append(fn)

def emit_event(msg: str) -> None:
    for l in listeners:
        l(msg)

def listener1(m: str) -> None:
    print('  listener1 got', m)

def listener2(m: str) -> None:
    print('  listener2 got', m.upper())

add_listener(listener1)
add_listener(listener2)
emit_event('hello listeners')
print()


# ---------- 场景 C：任务执行器（接受多个无参可调用任务） ----------
print('场景 C: 简单任务执行器')
from time import sleep

def task1() -> None:
    print('  task1 running')

def task2() -> None:
    print('  task2 running (sleep 0.1s)')
    sleep(0.1)

def run_tasks(tasks: list[Callable[[], Any]]) -> None:
    for t in tasks:
        t()

run_tasks([task1, task2])
print()


# ---------- 场景 D：重试装饰器（接受任意可调用） ----------
print('场景 D: 重试装饰器示例')
from functools import wraps
from random import random

def retry(times: int):
    def decorator(fn: Callable[..., Any]):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for i in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
            raise last_exc
        return wrapper
    return decorator


@retry(3)
def flaky(x: int) -> int:
    """偶发失败的函数：50% 概率失败"""
    if random() < 0.5:
        raise RuntimeError('random fail')
    return x * 10

# 多次尝试展示重试效果
for _ in range(5):
    try:
        print('  flaky ->', flaky(3))
    except Exception as e:
        print('  flaky failed after retries:', e)

print('\n实践场景示例运行完毕')
