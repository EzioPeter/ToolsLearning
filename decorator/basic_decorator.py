"""
最基础的装饰器讲解
装饰器就是一个函数，用来"包装"另一个函数
"""

# ========== 第一步：最简单的装饰器 ==========
def my_decorator(func):
    """
    这是一个装饰器函数
    它接收一个函数作为参数
    """
    def wrapper():
        print("执行函数前的准备")
        func()  # 执行原始函数
        print("执行函数后的清理")
    return wrapper


# 使用装饰器的方式 1：直接调用
def say_hello():
    print("你好！")

# 手动应用装饰器
decorated_say_hello = my_decorator(say_hello)
decorated_say_hello()


print("\n" + "="*50 + "\n")

# ========== 第二步：使用 @ 语法应用装饰器（推荐方式） ==========
@my_decorator
def say_goodbye():
    print("再见！")

# 现在调用 say_goodbye 时，它已经被装饰器包装了
say_goodbye()


print("\n" + "="*50 + "\n")

# ========== 第三步：装饰器可以处理有参数的函数 ==========
def my_decorator_v2(func):
    """
    支持有参数的函数的装饰器
    """
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        print(f"参数: {args}, {kwargs}")
        result = func(*args, **kwargs)  # 执行原始函数并获取返回值
        print(f"返回值: {result}")
        return result
    return wrapper


@my_decorator_v2
def add(a, b):
    """两个数相加"""
    return a + b


result = add(5, 3)


print("\n" + "="*50 + "\n")

# ========== 第四步：装饰器可以有参数 ==========
def repeat(times):
    """
    这是一个装饰器工厂（返回装饰器的函数）
    它可以让你自定义装饰器的行为
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(times):
                print(f"第 {i+1} 次执行:")
                func(*args, **kwargs)
        return wrapper
    return decorator


@repeat(times=3)
def greet(name):
    print(f"  你好，{name}！")


greet("小明")


print("\n" + "="*50 + "\n")

# ========== 第五步：实际应用 - 计时装饰器 ==========
import time

def timer(func):
    """测量函数执行时间的装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行耗时: {end_time - start_time:.4f} 秒")
        return result
    return wrapper


@timer
def slow_function():
    """一个比较耗时的函数"""
    time.sleep(1)
    print("  函数执行完成")


slow_function()


print("\n" + "="*50 + "\n")

# ========== 第六步：实际应用 - 日志装饰器 ==========
def log_decorator(func):
    """记录函数调用的装饰器"""
    def wrapper(*args, **kwargs):
        print(f"[日志] 开始调用: {func.__name__}{args}{kwargs}")
        try:
            result = func(*args, **kwargs)
            print(f"[日志] 调用成功: {func.__name__} -> {result}")
            return result
        except Exception as e:
            print(f"[日志] 调用失败: {func.__name__} 出错 {e}")
            raise
    return wrapper


@log_decorator
def divide(a, b):
    return a / b


print("正常除法:")
divide(10, 2)

print("\n异常除法:")
try:
    divide(10, 0)
except ZeroDivisionError:
    pass


print("\n" + "="*50 + "\n")

# ========== 第七步：使用 functools.wraps ==========
from functools import wraps

def simple_decorator(func):
    """一个不使用 functools.wraps 的装饰器（会覆盖原函数的元数据）"""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@simple_decorator
def no_wrap(x):
    """原函数 doc: 这是没有使用 wraps 的函数"""
    return x * 2


def decorator_with_wraps(func):
    """使用 functools.wraps 的装饰器（保留原函数的元数据）"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@decorator_with_wraps
def with_wrap(x):
    """原函数 doc: 这是使用 wraps 的函数"""
    return x * 2


print("不使用 wraps 的情况:")
print(f"  函数名: {no_wrap.__name__}")
print(f"  文档: {no_wrap.__doc__}")
print(f"  是否有 __wrapped__: {hasattr(no_wrap, '__wrapped__')}")
try:
    print(f"  __wrapped__: {no_wrap.__wrapped__}")
except Exception:
    pass

print("\n使用 wraps 的情况:")
print(f"  函数名: {with_wrap.__name__}")
print(f"  文档: {with_wrap.__doc__}")
print(f"  是否有 __wrapped__: {hasattr(with_wrap, '__wrapped__')}")
print(f"  __wrapped__: {getattr(with_wrap, '__wrapped__', None)}")

