import dolphindb as ddb
import time
import asyncio
import threading

# 在该例子中主线程负责创建协程对象传入自定义脚本并调用自定义的对象去运行，并新起子线程运行事件循环防止阻塞主线程。
class DolphinDBHelper(object):
    pool = ddb.DBConnectionPool("localhost", 8900, 10, "admin", "123456")
    @classmethod
    async def test_run(cls,script):
        print(f"run script: [{script}]")
        return await cls.pool.run(script)

    @classmethod
    async def runTest(cls,script):
        start = time.time()
        task = loop.create_task(cls.test_run(script))
        result = await asyncio.gather(task)
        print(f"""[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] time: {time.time()-start} result: {result}""")
        return result

# 定义一个跑事件循环的线程函数
def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__=="__main__":
    start = time.time()
    print("In main thread",threading.current_thread())
    loop = asyncio.get_event_loop()
    # 在子线程中运行事件循环, 让它 run_forever
    t = threading.Thread(target= start_thread_loop, args=(loop,))
    t.start()
    task1 = asyncio.run_coroutine_threadsafe(DolphinDBHelper.runTest("sleep(1000);1+1"),loop)
    task2 = asyncio.run_coroutine_threadsafe(DolphinDBHelper.runTest("sleep(3000);1+2"),loop)
    task3 = asyncio.run_coroutine_threadsafe(DolphinDBHelper.runTest("sleep(5000);1+3"),loop)
    task4 = asyncio.run_coroutine_threadsafe(DolphinDBHelper.runTest("sleep(1000);1+4"),loop)

    end = time.time()
    print("main thread time: ", end - start)