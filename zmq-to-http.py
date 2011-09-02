
import sys
import json
import msgpack
import gevent
from gevent import monkey
monkey.patch_all()

from gevent_zeromq import zmq

import requests

def pack(msg):
    return msgpack.Packer().pack(msg)

def unpack(msg):
    unpacker = msgpack.Unpacker()
    unpacker.feed(msg)
    return unpacker.unpack()

def send_http(http_addr, req):
    packed_req = pack(list(req))
    print "HTTP SEND | {0}".format(repr(packed_req))
    return unpack(requests.post(http_addr, data=packed_req).content)

if __name__ == '__main__':
    zmq_addr, http_addr = sys.argv[1:]
    ctx = zmq.Context()
    s = ctx.socket(zmq.XREP)
    s.bind(zmq_addr)
    while True:
        req = s.recv_multipart()
        print "ZMQ RECV| {0}".format(repr(req))
        resp = send_http(http_addr, req)
        print "ZMQ SEND| {0}".format(repr(resp))
        s.send_multipart(resp)
