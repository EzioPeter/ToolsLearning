"""
Generator examples

- Simple generator function (countdown)
- Generator expression
- Generator used with next(), send(), close()
"""

def countdown(n):
    print("generator countdown() started")
    while n > 0:
        yield n
        n -= 1
    print("generator countdown() finished")


def demo_generator_function():
    print("-- demo_generator_function --")
    gen = countdown(3)
    print("next(gen):", next(gen))
    print("next(gen):", next(gen))
    print("for remaining in gen:")
    for v in gen:
        print("  ", v)
    print()


def demo_generator_expression():
    print("-- demo_generator_expression --")
    # Use a named generator function instead of an inline generator expression
    def gen_squares():
        for i in range(4):
            # place to add logging or complex logic if needed
            yield i * i

    gen_expr = gen_squares()
    print("type:", type(gen_expr))
    print("list(gen_expr):", list(gen_expr))
    print()


def coroutine_echo():
    """A tiny coroutine-style generator that echoes values sent to it.

    Protocol: first advance to the first yield (prime it), then send values.
    Sending None will terminate.
    """
    try:
        val = yield 'ready'
        while True:
            if val is None:
                return 'closed'
            val = yield f'got {val}'
    finally:
        print('coroutine_echo: generator closed')


def demo_send_close():
    print("-- demo_send_close --")
    g = coroutine_echo()
    print('prime ->', next(g))        # prime, gets 'ready'
    print('send A ->', g.send('A'))   # receives 'A', yields 'got A'
    print('send B ->', g.send('B'))
    try:
        ret = g.send(None)  # causes coroutine to return/close; StopIteration carries return value
        print('send None ->', ret)
    except StopIteration as e:
        # generator returned a value (available as e.value in Python 3.3+)
        print('send None -> StopIteration (generator returned):', getattr(e, 'value', None))

    try:
        print('after close next ->', next(g))
    except StopIteration:
        print('-> StopIteration after coroutine closed')
    print()


if __name__ == '__main__':
    demo_generator_function()
    demo_generator_expression()
    demo_send_close()
