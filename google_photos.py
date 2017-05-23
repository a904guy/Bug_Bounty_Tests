import concurrent.futures
import multiprocessing, threading
import math, time
import subprocess
from pprint import pprint as pp, pformat

import requests

from crunch import Crunch


def run_cmd(cmd: str) -> bytes:
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=open('/dev/null')).communicate()[0].strip()


def brute_force(free_ports, start_n):
    print(f"Start_N: {start_n}")
    r = requests.Session()
    cpu_count = multiprocessing.cpu_count()
    # threads_limit = math.ceil(free_ports / multiprocessing.cpu_count())
    threads_limit = 500
    c = Crunch(min_length=75, max_length=75, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-',
               start_n=start_n)  # allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-'
    print('Stating Crunch')

    time.sleep(2)  # Let all the processes spin up
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_limit) as executor:
        for code, n in c.brute_force():
            # used_port_count = int(run_cmd("netstat -antp 2> /dev/null | grep 'tcp' | grep -v 'LISTEN' | wc -l"))

            def worker(code, r):
                print('Testing: http://lh3.googleusercontent.com/%s | threading_count: %s | process_name: %s | n:%s\r' % (
                    code, threading.active_count(), multiprocessing.current_process().name.ljust(11), n * cpu_count), end='')  # free_ports - used_port_count
                try:
                    resp = r.head('http://lh3.googleusercontent.com/%s' % code, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                    })
                except:
                    # pp(e)
                    return
                # print(resp.status_code)
                if resp.status_code == 200:
                    print('\n\nFound: http://lh3.googleusercontent.com/%s\n\n' % code)
                    return

            e = executor.submit(worker, code, r)

            # try:
            # while threading.active_count() >= threads_limit:
            #     time.sleep(0.0001)
            # threading.Thread(target=worker, args=(code,)).start()  # free_ports - used_port_count

            # except:
            # pp(e)
            # threads_limit -= 1
            # pass


if __name__ == '__main__':
    max_free_ports = int(run_cmd("sysctl net.ipv4.ip_local_port_range | awk '{print $4-$3}'"))

    permutations = Crunch(min_length=75, max_length=75, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-').n_permutations()
    pp("Total Permutations: %s" % permutations)
    permutations /= multiprocessing.cpu_count()
    for x in range(0, multiprocessing.cpu_count()):
        pp("Launching Start_N: %s" % (permutations * x))
        multiprocessing.Process(target=brute_force, args=(max_free_ports, (x * permutations),)).start()
