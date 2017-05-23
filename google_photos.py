import multiprocessing
import sys
import subprocess
from pprint import pprint as pp, pformat

import requests

from Async import Run_Async
from crunch import Crunch


def run_cmd(cmd: str) -> bytes:
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=open('/dev/null')).communicate()[0].strip()


def brute_force(free_ports):
    print('Init Crunch')
    c = Crunch(min_length=75, max_length=75, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-')  # allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-'
    print('Stating Crunch')
    r = requests.Session()
    for code, n in c.iterate():
        # used_port_count = int(run_cmd("netstat -antp 2> /dev/null | grep 'tcp' | grep -v 'LISTEN' | wc -l"))

        def worker(code, r):
            print('Testing: http://lh3.googleusercontent.com/%s | n:%s | available_ports:%s\r' % (pformat(code), n * multiprocessing.cpu_count(), free_ports), end='')  #free_ports - used_port_count
            try:
                resp = r.get('http://lh3.googleusercontent.com/%s' % code, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                })
            except Exception as e:
                pp(e)
                return
            # print(resp.status_code)
            if resp.status_code == 200:
                print('\n\nFound: http://lh3.googleusercontent.com/%s\n\n' % code)
                return

        try:
            Run_Async('threading', 10000).start(worker, (code, r,))  #free_ports - used_port_count
        except:
            pass
    Run_Async('threading').join_all()


if __name__ == '__main__':
    max_free_ports = int(run_cmd("sysctl net.ipv4.ip_local_port_range | awk '{print $4-$3}'"))
    for x in range(1, multiprocessing.cpu_count()):
        multiprocessing.Process(target=brute_force, args=(max_free_ports,)).start()