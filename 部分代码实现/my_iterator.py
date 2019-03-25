'''
    实现自己的迭代器
'''
from collections.abc import Iterator


class MyIterator:
    def __init__(self, employee):
        self.employee = employee
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            content = self.employee[self.index]
        except IndexError as e:
            raise StopIteration
        self.index += 1
        return content


my_iterator = MyIterator(['shiyue', 'qiyue'])
print(isinstance(my_iterator, Iterator))

for i in my_iterator:
    print(i)
