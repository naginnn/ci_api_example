import asyncio
import sys
import threading
import time
import tasks
import redis
from celery import app
from celery import Celery

class A(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = False

    async def _main(self):
        tasks = []
        function_list = [func for func in dir(self) if callable(getattr(self, func)) and func.startswith('_') is False and func != 'run' and func.startswith('a_') is True]
        print(function_list)
        for func in function_list:
            tasks.append(asyncio.create_task(getattr(self, func)()))
        await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self._main())


class B(A):
    def __init__(self):
        super().__init__()

    async def a_test1(self):
        for i in range(5):
            print('B -> a_test1', i)
            await asyncio.sleep(0)
        # self.result_test1 = 100

    async def a_test2(self):
        for i in range(10):
            print('B -> a_test2', i)
            await asyncio.sleep(0)
        # self.result_test2 = 100

    def test3(self):
        return 300


class C(A):

    saved_value = None

    async def a_test1(self):
        for i in range(5):
            print('C -> a_test1', i)
            await asyncio.sleep(0)
        # self.result_test1 = 100

    async def a_test2(self):
        for i in range(10):
            self.saved_value = 100
            print('C -> a_test2', i)
            await asyncio.sleep(0)
        # self.result_test2 = 100

    def test3(self):
        return 300

    def get_value(self):
        return f'Saved value: {self.saved_value}'

if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')
    print(r.get('foo').decode("utf-8"))
    tasks.add.delay(2, 200)



    # b = B()
    # b.start()
    # c = C()
    # c.start()
    # time.sleep(2)
    # print(c.get_value())
    # print('MAIN THREAD')

    # c = C()
    # c.run()
    # print(b.result_test1)
    # print(b.result_test2)
    # print(b.test3())