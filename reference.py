import scripts


def d_plant_scripts():
    return [[scripts.StayStill()], [scripts.StayStill()], [scripts.StayStill()]]


def d_herbivore_scripts():
    return [[scripts.MoveTowardPlants(), scripts.MoveLikeSquawker()],
                         [scripts.MoveTowardPlants(), scripts.MoveLikeSquawker()],
                         [scripts.StayStill()]]


def d_omnivore_scripts():
    return [[scripts.HuntHerbivores(), scripts.MoveTowardPlants(), scripts.StayStill()],
                        [scripts.HuntHerbivores(), scripts.MoveTowardPlants(), scripts.MoveLikeSquawker()],
                        [scripts.StayStill()]]


def d_versatile_scripts():
    return[[scripts.MoveLikeSquawker()], [scripts.MoveTowardPlants()], [scripts.StayStill()]]
