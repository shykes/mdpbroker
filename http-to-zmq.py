#!/usr/bin/env python

"""WSGI server example"""

import msgpack
import sys
import random
import gevent
from gevent.pywsgi import WSGIServer
from gevent_zeromq import zmq


def pack(msg):
    return msgpack.Packer().pack(msg)           

def unpack(msg):
    unpacker = msgpack.Unpacker()               
    unpacker.feed(msg)
    return unpacker.unpack() 


def task(task_id):
    while True:
        print task_id
        gevent.sleep(1)

def application(env, start_response, zmq_socket):
    packed_req = env['wsgi.input'].read()
    print "HTTP RECV| {0}".format(repr(packed_req))
    req = unpack(packed_req)
    print "ZMQ SEND| {0}".format(repr(req))
    zmq_socket.send_multipart(req[2:])
    response = pack([req[0], ''] + list(zmq_socket.recv_multipart()))
    print "RECV| {0}".format(repr(response))
    start_response('200 OK', [('Content-Type', 'application/octet-stream')])
    return [response]

if __name__ == '__main__':
    http_port, zmq_addr = sys.argv[1:]
    ctx = zmq.Context()
    s = ctx.socket(zmq.REQ)
    s.connect(zmq_addr)
    print 'Serving on {0}...'.format(http_port)
    WSGIServer(
        ('', int(http_port)),
        lambda *args, **kw: application(zmq_socket=s, *args, **kw)
    ).serve_forever()
