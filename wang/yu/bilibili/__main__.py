import wang.yu.bilibili.BiliBiliUtil as bilibili_util


print('1. 根据番号爬取b站视频合集')
print('2. b站用户年龄段报告')
num = int(input('输入:\n'))
if num == 1:
    bilibili_util.download_videos()
elif num == 2:
    bilibili_util.user_age_graph()
else:
    raise Exception('错误的选择')