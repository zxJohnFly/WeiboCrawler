from setting import *
from crawler.Parser import Parser
from time import sleep

while True:
    for category in Catogeries:
        p = Parser(username, password, category)
        p.loadpages()
        sleep(10)

    sleep(600)
