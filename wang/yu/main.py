import wang.yu.bilibili.main as bilibili_main
import wang.yu.boss.main as boss_main
import wang.yu.dianping.main as dianping_main
import wang.yu.dota2.main as dota2_main
import wang.yu.renren.main as renren_main
import wang.yu.test51.main as test51_main

print('1. b站')
print('2. boss直聘')
print('3. 大众点评')
print('4. DOTA2英雄爬取')
print('5. 人人网相册下载')
print('6. 无忧考网模拟试题爬取')

num = int(input('输入:\n'))
if num == 1:
    bilibili_main.run()
elif num == 2:
    boss_main.run()
elif num == 3:
    dianping_main.run()
elif num == 4:
    dota2_main.run()
elif num == 5:
    renren_main.run()
elif num == 6:
    test51_main.run()
else:
    raise Exception('错误的选择')
