package graphics

import (
	pb "app/protos"
)

// Mirror returns a point flipped along the specified 2-dimensional axis.
func Mirror(point *pb.Point) pb.Point {

	var cpt = center(point.Canvas)

	x := cpt.X - point.X
	y := point.Y

	return pb.Point{X: cpt.X + x, Y: y}
}

// center calculates and returns the center point of
// the specified canvas.
func center(canvas *pb.Canvas) pb.Point {

	x := float64(canvas.Width) / 2
	y := float64(canvas.Height) / 2

	return pb.Point{X: x, Y: y}
}
