import numpy as np

def func(myl, setl, np_seed = 6):
    np.random.seed(np_seed)
    np.random.shuffle(myl)
    print(np.random.choice(5,3))
    randstate1 = np.random.RandomState(seed=np_seed)
    randstate2 = np.random.RandomState(seed=np_seed)
    r = roll_die(np.random.choice)
    s = roll_die(randstate1.choice)
    t = roll_die(randstate2.choice)
    k = np.random.random_integers(1,6)
    die_state = (1, 2, 3, 4, 5, 6)
    print(die_state[k])
    print(myl)
    print(r,s, t)

def roll_die(choice):
    print 'rolling die...'
    die_state = (1,2,3,4,5,6)
    res = []
    for i in range(2):
        res.append(choice(a=die_state))
    return res

runs = 10
while(runs>0):
    myl = [1,2,3,4]
    setl = (1,2,3,4,5)
    func(myl,setl, 7)
    runs-=1
