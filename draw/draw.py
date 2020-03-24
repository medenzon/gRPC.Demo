channel = grpc.insecure_channel('localhost:9901')
stub = protos.demo_pb2_grpc.TransformStub(channel)

norm_points, flip_points = [], []

def draw(event):
    
    event_point = pb.Point( x = event.x,
                            y = event.y,                # create point from
                            canvas = c )                # mouse-down event

    norm_points.append( event_point )

    draw( from = norm_points[-2],                       # draw normal line
          to   = norm_points[-1] )

    for flip_point in stub.flip(send([mouse_point])):   # stream event point
        
            flip_points.append(flip_point)
        
            draw_line( from = flip_points[-2],          # draw flipped line
                       to   = flip_points[-1] )

master = tk.Tk()

view = tk.Canvas( master,
                  width = 1100,
                  height = 800 )

view.pack( expand = tk.YES,
           fill = tk.BOTH )

view.bind('<B1-Motion>', paint)

if connected:
    tk.mainloop()