import json
import os
import signal
import socket
import threading

import time

import speedtest_cli
from speedtest_cli import build_user_agent, getConfig, closestServers, getBestServers, ctrl_c, downloadSpeed, \
    uploadSpeed


def speedtest():
    """Run the full speedtest.net test"""

    speedtest_cli.shutdown_event = threading.Event()

    signal.signal(signal.SIGINT, ctrl_c)

    socket.setdefaulttimeout(1000)

    # Pre-cache the user agent string
    build_user_agent()

    config = getConfig()
    servers = closestServers(config['client'])
    servers = getBestServers(servers)

    for latency, server in servers.items():
        test = {'server': server, 'latency': latency, 'time': time.time(), 'speed': {}}
        sizes = [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
        urls = []
        for size in sizes:
            for i in range(0, 4):
                urls.append('%s/random%sx%s.jpg' %
                            (os.path.dirname(server['url']), size, size))
        test['download_urls'] = urls
        dlspeed = downloadSpeed(urls, True)
        test['speed']['download'] = dlspeed

        sizesizes = [int(.25 * 1000 * 1000), int(.5 * 1000 * 1000)]
        sizes = []
        for size in sizesizes:
            for i in range(0, 25):
                sizes.append(size)
        test['upload_sizes'] = sizesizes
        ulspeed = uploadSpeed(server['url'], sizes, True)
        test['speed']['upload'] = ulspeed
        print json.dumps(test)

def main():
    speedtest()
