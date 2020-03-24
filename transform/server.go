package main

import (
	pb "app/protos"
	tf "app/services"
	"context"
	"log"
	"net"

	"google.golang.org/grpc"
)

const (
	network = "tcp"
	port    = ":9901"
	url     = "localhost"
)

func main() {

	log.Println("transform server starting up...")

	ctx := context.Background()

	listener, err := net.Listen(network, port)

	if err != nil {
		log.Printf("Listening error: %v", err)
	}

	defer func() {
		if err := listener.Close(); err != nil {
			log.Printf("Failed to close %s %s: %v", network, port, err)
		}
	}()

	server := grpc.NewServer()

	pb.RegisterTransformServer(server, &tf.Server{})

	go func() {
		defer server.GracefulStop()
		<-ctx.Done()
	}()

	server.Serve(listener)
}
