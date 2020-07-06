import time
from concurrent.futures import ThreadPoolExecutor

def demo(i,x):
    s = time.time()
    time.sleep(1)
    print(time.time()-s)

def main():
    with ThreadPoolExecutor (3) as tr:
        for i in range(100):
            tr.submit(demo,*(1,2))
if __name__ == '__main__':
    main()