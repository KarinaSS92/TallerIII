from tqdm import tqdm
from time import sleep
from random import randint
for i in tqdm(range(20)):
    sleep(randint(1, 5))