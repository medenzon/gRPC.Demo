package services

import (
	gfx "app/graphics"
	pb "app/protos"
)

// Server is a protos.TransformServer instance.
type Server struct {
	pb.TransformServer
}

// Flip executes a bidirectional stream, which receives a stream of points
// points and returns a stream of points that have been flipped along their
// horizontal axis.
func (s *Server) Flip(stream pb.Transform_FlipServer) error {

	for {

		in, err := stream.Recv()

		if err != nil {
			return err
		}

		if (in.X >= 0) && (in.Y >= 0) {

			out := gfx.Mirror(in)
			err := stream.Send(&out)

			if err != nil {
				return err
			}
		}
	}
}
