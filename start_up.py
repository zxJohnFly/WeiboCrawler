from setting import *
from crawler.Parser import Parser
from time import sleep

while True:
    for category in Catogeries:
        p = Parser(username, password, category)
        res = p.loadpages()

        if ~res:
            p = Parser(username, password, category)

        sleep(10)

    print 'crawler system rest for 1,800s'
    sleep(1800)
