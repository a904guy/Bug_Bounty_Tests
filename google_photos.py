import concurrent.futures
import multiprocessing, threading
import math, time
import subprocess
from pprint import pprint as pp, pformat

import requests

from crunch import Crunch


def run_cmd(cmd: str) -> bytes:
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=open('/dev/null')).communicate()[0].strip()


def brute_force(free_ports,):
    print("Starting Brute Force")
    print(f"FreePorts: {free_ports}")
    r = requests.Session()
    cpu_count = multiprocessing.cpu_count()
    # threads_limit = math.ceil(free_ports / multiprocessing.cpu_count())
    threads_limit = 500
    c = Crunch(min_length=75, max_length=75, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-')  # allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-'
    print('Stating Crunch')

    time.sleep(2)  # Let all the processes spin up
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_limit) as executor:
        for code, n in c.brute_force():
            # used_port_count = int(run_cmd("netstat -antp 2> /dev/null | grep 'tcp' | grep -v 'LISTEN' | wc -l"))

            def worker(code, r):
                try:
                    resp = r.head('http://lh3.googleusercontent.com/%s' % code, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                    })
                except Exception as e:
                    del resp
                    pp(e)
                    return worker(code, r)
                # print(resp.status_code)
                print('Testing: http://lh3.googleusercontent.com/%s | response_code: %s | threading_count: %s | process_name: %s | n:%s\r' % (
                    code, resp.status_code, threading.active_count(), multiprocessing.current_process().name.ljust(11), n * cpu_count), end='')  # free_ports - used_port_count
                if resp.status_code == 200:
                    print('\n\nFound: http://lh3.googleusercontent.com/%s\n\n' % code)
                del resp, code
                return

            executor.submit(worker, code, r)
            del code, n
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

    # permutations = Crunch(min_length=75, max_length=75, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-').n_permutations()
    # pp("Total Permutations: %s" % permutations)
    # permutations /= multiprocessing.cpu_count()
    for x in range(0, multiprocessing.cpu_count()):
    # with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        multiprocessing.Process(target=brute_force, args=(max_free_ports,)).start()
        # executor.submit(brute_force, max_free_ports)  #permutations
