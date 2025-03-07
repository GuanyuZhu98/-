from main.workspace import easytest_module
import time,os
mytest = easytest_module()
dur = input("请输入测试时长")
if input("是否开始测试？") == "y":
    start_time = time.time()
    while True:
        if time.time() - start_time > dur:
            break
        res = mytest.runTest()

        print(f"千分表当前读数为{res}cm")
        time.sleep(0.01)
        os.system('clear')
    mytest.endTest()

