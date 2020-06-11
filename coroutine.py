import time

if 0:
    from greenlet import greenlet
    import time


    def task_1():
        while True:
            print("--This is task 1!--")
            g2.switch()  # 切换到g2中运行
            time.sleep(0.5)


    def task_2():
        while True:
            print("--This is task 2!--")
            g1.switch()  # 切换到g1中运行
            time.sleep(0.5)


    if __name__ == "__main__":
        g1 = greenlet(task_1)  # 定义greenlet对象
        g2 = greenlet(task_2)

        g1.switch()  # 切换到g1中运行

if 0:
    from gevent import monkey
    import gevent
    import time


    def task_1(name):
        for i in range(5):
            print(name, i)
            time.sleep(1)  # 协程遇到耗时操作后会自动切换其他协程运行


    def task_2(name):
        for i in range(3):
            print(name, i)
            time.sleep(0.3)


    if __name__ == "__main__":
        monkey.patch_all()  # 给所有的耗时操作打上补丁

        gevent.joinall([  # 等到协程运行完毕
            gevent.spawn(task_1, "task_1"),  # 创建协程
            gevent.spawn(task_2, "task_2")
        ])
        print("the main thread!")

if 0:
    import gevent
    import time
    from gevent import monkey
    from urllib import request

    monkey.patch_all()  # 把当前程序的所有 IO 操作标记起来，否则模块无法知道 IO 操作
    # 异步耗时： 6.794851064682007
    # 异步耗时： 5.948604106903076 with monkey.patch_all()


    def func(url):
        print('GET:', url)
        resp = request.urlopen(url)
        data = resp.read()
        print('%i bytes received from %s' % (len(data), url))


    urls = [
        'http://www.python.org/',
        'https://www.python.org/about/help/',
        'https://www.python.org/news/security',
    ]

    time_start = time.time()
    for item in urls:
        func(item)
    print('同步耗时：', time.time() - time_start)


    async_time_start = time.time()
    gevent.joinall([
        gevent.spawn(func, 'http://www.python.org/'),
        gevent.spawn(func, 'https://www.python.org/about/help/'),
        gevent.spawn(func, 'https://www.python.org/news/security'),
    ])
    print('异步耗时：', time.time() - async_time_start)

if 0:
    import asyncio
    import time


    async def a():
        print("1")
        print("----++++")
        return "b"


    b = asyncio.ensure_future(a())
    print("b", b)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(b)


    # 运行到这里产生了一个已经执行完毕的task-b

    async def do_some_work(x):
        time.sleep(0.01)
        print("waiting:", time.time())
        await asyncio.sleep(x)
        return "Done after {}s".format(x)


    async def main():
        coroutine1 = do_some_work(2)
        coroutine2 = do_some_work(2)
        coroutine3 = do_some_work(6)

        tasks = [
            coroutine1,
            coroutine2,
            b,
            coroutine3,
        ]  # 故意在这个tasks列表中加入已经完成的task-b
        for task in asyncio.as_completed(tasks):  # 这条语句会首先将tasks列表中的coro转为task
            print("----", task, time.time())
            result = await task  # 挂起当前携程，转而执行别的携程，直到所有的携程全部挂起的时候，本携程才能再次拿到执行权，因为最早完成的是b,所以result是8
            print("Task ret: {}".format(result), time.time())


    loop.run_until_complete(main())  # 这条语句首先将main()转为task,目前只有这一个pending状态的task,和之前finished状态的b，所以先执行这个。
    # 我这里两次运行了run_until_complete


if 0:
    import asyncio

    async def a():
        print("a")

    async def b():
        print("b")
        return("--b--")

    asyncio.ensure_future(a())
    bb = asyncio.ensure_future(b())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bb)  # 虽然传入的参数是task-bb,但是task-a却会执行，
    # 并且是第一个执行，首先打印a,其次打印b
    print(bb.result())

if 0:
    def consumer():
        print('--4、开始执行生成器代码--')
        response = None
        while True:
            print('--5、yield，中断，保存上下文--')
            n = yield response  # 4、yield，中断，保存上下文
            print('--8、获取上下文，继续往下执行--')
            if not n:
                return
            print("[Consumer]: consuming {} ..".format(n))
            response = "OK"


    def produce(c):
        print("--3、启动生成器，开始执行生成器consumer--")
        c.send(None)  # 3、启动生成器，开始执行生成器consumer
        print("--6、继续往下执行--")
        n = 0
        while n < 5:
            n += 1
            print("[Producer]: producing {} ..".format(n))
            print("--7、第{}次唤醒生成器，从yield位置继续往下执行！--".format(n + 1))
            r = c.send(n)  # 第二次唤醒生成器
            print("--9、从第8步往下--")
            print("[Producer]: consumer return {} ..".format(r))

        c.close()


    if __name__ == "__main__":
        c = consumer()  # 1、定义生成器，consumer并不执行
        produce(c)  # 2、运行produce函数


if 0:
    import asyncio


    async def work(x):  # 通过async关键字定义一个协程
        for _ in range(3):
            print('Work {} is running ..'.format(x))
        return (0)


    coroutine_1 = asyncio.ensure_future(work(1))  # 协程是一个对象，不能直接运行
    # coroutine_1 = work(1)# 协程是一个对象，不能直接运行
    # 方式一：
    loop = asyncio.get_event_loop()  # 创建一个事件循环
    result = loop.run_until_complete(coroutine_1)  # 将协程对象加入到事件循环中，并执行
    print(result)  # 协程对象并没有返回结果，打印None
    # 方式二：

if 0:
    import asyncio


    async def work(x):
        for _ in range(3):
            print('Work {} is running ..'.format(x))
        return "Work {} is finished".format(x)


    def call_back(future):
        print("Callback: {}".format(future.result()))


    coroutine = work(1)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(coroutine)
    task.add_done_callback(call_back)
    loop.run_until_complete(task)


if 0:
    import asyncio
    import functools


    async def work(x):
        for _ in range(3):
            print('Work {} is running ..'.format(x))
        return "Work {} is finished".format(x)


    def call_back_2(num, future):
        print("Callback_2: {}, the num is {}".format(future.result(), num))


    coroutine = work(1)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(coroutine)
    task.add_done_callback(functools.partial(call_back_2, 100))
    loop.run_until_complete(task)

if 0:
    # 并发运行任务的案例

    import asyncio


    async def factorial(name, number):
        f = 1
        for i in range(2, number + 1):
            print(f"Task {name}: Compute factorial({i})...")  # python3.7新语法，了解一波
            await asyncio.sleep(1)  # await后面是 可等待对象
            f *= i
        print(f"Task {name}: factorial({number}) = {f}")

        return f"Task {name}: Finished!"


    async def main():
        # Schedule three calls *concurrently*:
        results = await asyncio.gather(  # results包含所有任务的返回结果，是一个列表，按执行顺序返回结果
            factorial("A", 2),  # 协程，会自动调度为任务
            factorial("B", 3),
            factorial("C", 4),
        )
        print(results)


    asyncio.run(main())

if 0:
    # 使用事件循环和asyncio.wait、asyncio.gather实现并发运行任务

    import asyncio, time


    async def work_1(x):
        print(f"Starting {x}")
        time.sleep(1)
        print(f"Starting {x}")
        for _ in range(3):
            print(f"Work {x} is running ..")
            await asyncio.sleep(2)  # 耗时操作，此时挂起该协程，执行其他协程
        return f"Work {x} is finished"


    async def work_2(x):
        print(f"Starting {x}")
        for _ in range(3):
            await asyncio.sleep(1)  # 耗时操作，此时挂起该协程，执行其他协程
            print(f"Work {x} is running ..")
        return f"Work {x} is finished"


    coroutine_1 = work_1(1)
    coroutine_2 = work_2(2)

    loop = asyncio.get_event_loop()  # 创建一个事件循环

    # 方式一，asyncio.wait(tasks)接受一个task列表  执行的顺序与列表里的任务顺序有关
    tasks = [
        asyncio.ensure_future(coroutine_1),
        asyncio.ensure_future(coroutine_2),
    ]
    # 注册到事件循环中，并执行
    dones, pendings = loop.run_until_complete(
        asyncio.wait(tasks))  # loop.run_until_complete(asyncio.wait(tasks))的作用相当于：await asyncio.wait(tasks)
    for task in dones:
        print(task.result())

    # 方式二，使用asyncio.gather(*tasks)，接受一堆tasks，tasks也可以是一个列表，使用*解包
    # task_1 = asyncio.ensure_future(coroutine_1)
    # task_2 = asyncio.ensure_future(coroutine_2)
    # task_result_list = loop.run_until_complete(asyncio.gather(task_1, task_2))  # 返回一个列表，里面包含所有task的result()的结果


if 0:
    import asyncio, time


    async def work(x):
        for _ in range(3):
            print("Work {} is running ..".format(x))
            await asyncio.sleep(1)  # 当执行某个协程时，在任务阻塞的时候用await挂起
        return "Work {} is finished!".format(x)


    async def main_work():
        coroutine_1 = work(1)
        coroutine_2 = work(2)
        coroutine_3 = work(3)

        tasks = [
            asyncio.ensure_future(coroutine_1),
            asyncio.ensure_future(coroutine_2),
            asyncio.ensure_future(coroutine_3),
        ]

        dones, pendings = await asyncio.wait(tasks)

        for task in dones:
            print("The task's result is : {}".format(task.result()))


    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main_work())











