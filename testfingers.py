import getfingers

getfingers.init()

while True:
    forces = getfingers.getforces()
    print(forces)
