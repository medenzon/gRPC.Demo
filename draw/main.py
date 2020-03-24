from __future__ import print_function
import os
import sys
import grpc
import tkinter as tk
import protos.demo_pb2_grpc
import protos.demo_pb2 as pb

if os.environ.get('http_proxy'):
    del os.environ['http_proxy']
    print('deleted http proxy')

if os.environ.get('https_proxy'):
    del os.environ['https_proxy']
    print('deleted https proxy')

url = 'localhost:9901'

connected = True
channel = grpc.insecure_channel(url)
stub = protos.demo_pb2_grpc.TransformStub(channel)

w = 1100
h = 800

def send(points):
    '''
    Necessary function for utilizing gRPC bidirectional streaming.
    '''
    for point in points:
        yield point

def draw_line(point_a,point_b):
    '''
    Draws a Tkinter line from point a to point b.
    '''
    x1,y1 = point_a.x,point_a.y
    x2,y2 = point_b.x,point_b.y
    view.create_line(x1,y1,x2,y2, fill="blue", width=5)

def paint(event):
    '''drack points to draw on the canvas
    while bidirectionally streaming the same points to a service
    that returns a the points flipped on a horizontal axis. The
    flipped drawing is simultaneously displayed in real time next
    to the original drawing.
    '''
    event_point = pb.Point(x=event.x,y=event.y,canvas=c)
    norm_points.append(event_point)

    if len(norm_points) > 1:
        draw_line(norm_points[-2],norm_points[-1])

    for flip_point in stub.flip(send([event_point])):
        sys.stdout.write('\rSent: ({0},{1})  Received: ({2},{3})'.format(event_point.x,event_point.y,flip_point.x,flip_point.y))
        sys.stdout.flush()

        if len(flip_points) > 1:
            draw_line(flip_points[-2],flip_points[-1])

        flip_points.append(flip_point)

def clip(event):
    '''
    Empties the list of current drawing points, normal and flipped.
    '''
    clip_point = pb.Point(x=-1,y=-1,canvas=None)

    for _ in stub.flip(send([clip_point])):
        pass

    norm_points.clear()
    flip_points.clear()


c = pb.Canvas(width=w,height=h)

norm_points = []
flip_points = []

master = tk.Tk()
master.title('gRPC Bidirectional Streaming')
view = tk.Canvas(master,width=w,height=h)
view.pack(expand=tk.YES,fill=tk.BOTH)
view.bind('<B1-Motion>',paint)
view.bind('<ButtonRelease-1>',clip)

if connected:
    tk.mainloop()