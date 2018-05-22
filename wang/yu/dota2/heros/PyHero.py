class PyHero:
    def __init__(self):
        pass

    def __init__(self, hero):
        self.hero_id = hero['hero_id']
        self.hero_name = hero['hero_name']

    def __str__(self):
        return "ID[%d]NAME[%s]" % (self.hero_id, self.hero_name)
