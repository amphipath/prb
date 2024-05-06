from pynput.keyboard import Key, Controller, Listener
from time import sleep

keyboard = Controller()

class Step:
    def __init__(self, *funcs):
        self.funcs = [*funcs]
    
    def do(self):
        for f in self.funcs:
            f()
    
    def __add__(self, step):
        return Step(*self.funcs, *step.funcs)
    
class Wait(Step):
    def __init__(self, waitTime):
        self.__interval = waitTime
        super().__init__(lambda : sleep(waitTime))

class Input(Step):
    def __init__(self, *args, **kwargs):
        if 'interval' in kwargs:
            self.__interval = kwargs['interval']
        else:
            self.__interval = 0.05
        def execute():
            for key in args:
                print(str(key))
                keyboard.press(key)
                sleep(0.05)
                keyboard.release(key)
                sleep(self.__interval)
        super().__init__(execute)

class UseBall():
    def __init__(self):
        self.__lastUsed = 0
        self.poke = Step(lambda : self.use(0))
        self.great = Step(lambda : self.use(1))
        self.ultra = Step(lambda : self.use(2))
        self.rogue = Step(lambda : self.use(3))
        self.master = Step(lambda : self.use(4))
    
    def use(self, ballId):
        diff = ballId - self.__lastUsed
        if diff < 0:
            inputs = [Key.up] * (-diff)
            Input(*inputs).do()
        elif diff > 0:
            inputs = [Key.down] * diff
            Input(*inputs).do()
        Input('z').do()
        self.__lastUsed = ballId
        Wait(2).do()
        
startGame = Input('z')

startWave = Wait(5)
doNotSwitch = Input('x')

fight = Input(Key.left, Key.up, 'z')

ball = Input(Key.right, Key.up, 'z')

chgPokemon = Input(Key.left, Key.down, 'z')
def swap(slot):
    inputs = [Key.left] + (slot - 1) * [Key.down] + ['z', 'z']
    return Input('z') + Wait(0.5) + Input(*inputs) + Wait(2)

def selectMon(slot):
    inputs = [Key.left] + (slot - 1) * [Key.down] + ['z', 'z']
    return Input(*inputs)

def doublesSelectMon(slot):
    inputs = [Key.left, Key.up, Key.left] + (slot - 1) * [Key.down] + ['z', 'z']  
    return Input(*inputs)

playOutTurn = Wait(3)
move1 = Input(Key.left, Key.up, 'z') 
move2 = Input(Key.right, Key.up, 'z')
move3 = Input(Key.down, Key.left, 'z') 
move4 = Input(Key.down, Key.right, 'z')



useBall = UseBall()

pokemonCaught = Input('x')
gainedExp = Input('x') + Wait(0.3)
rejectNewMon = Input('x')
fainted = Input('x')

expFill = Wait(3)
levelledUp = Input('z','z','z') + Wait(3)
rejectNewMove = Input('x','x','x','z','x', interval=0.5) + Wait(3)


startTrainerBattle = Wait(1) + Input('x', 'x', interval=1) + Wait(3)
endTrainerBattle = Input('x') + Wait(1.5) + Input('x', 'x', interval=0.5) 

def doublesTarget(target):
    inputs = [Key.down]
    if target != 3:
        inputs = inputs + [Key.up]
        if target == 2:
            inputs = inputs + [Key.right]
    inputs = inputs + ['z']
    return Input(*inputs)

rerollReward = Input(Key.down,'z') + Wait(1)
def selectReward(i):
    k = i - 1
    inputs = [Key.right] * k + ['z']
    return Input(*inputs)


evolve = Wait(8) + Input('z')