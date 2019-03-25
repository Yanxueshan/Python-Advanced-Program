'''
    生成器 栈帧
'''
import inspect
import dis

frame = None


def func2():
    func1()


def func1():
    global frame
    frame = inspect.currentframe()


func2()
print(frame.f_code.co_name)
frame_callback = frame.f_back
print(frame_callback.f_code.co_name)


def gen_func():
    yield 1
    name = "shiyue"
    yield 2
    age = 24
    return "qiyue"


gen = gen_func()
dis.dis(gen)
print(gen.gi_frame.f_lasti)
print(gen.gi_frame.f_locals)
print(next(gen))
print(gen.gi_frame.f_lasti)
print(gen.gi_frame.f_locals)
print(next(gen))
print(gen.gi_frame.f_lasti)
print(gen.gi_frame.f_locals)
