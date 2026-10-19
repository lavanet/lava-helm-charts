# Start from a base image with Go installed
FROM golang:1.21-alpine as builder

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module
COPY go.mod ./

# Download Go module dependencies
RUN go mod download

# Copy the source code into the container
COPY main.go ./

# Compile the application
RUN go build -o healthcheck

#########################  RUNTIME ########################
FROM scratch

# Copy the Pre-built binary file from the previous stage
COPY --from=builder /app/healthcheck .
ENV PATH="/"

# Run the executable
CMD ["./healthcheck"]
