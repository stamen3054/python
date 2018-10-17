from wang.yu.renren.RenrenUtil import RenrenUtil


def run():
    renren_util = RenrenUtil()
    renren_util.download_albums()

    if __name__ == '__main__':
        run()
