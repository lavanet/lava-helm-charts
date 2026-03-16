package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"regexp"
)

func main() {
	var metricsPort, apiPort int
	flag.IntVar(&metricsPort, "metrics-port", 9090, "Port where Prometheus metrics are exposed")
	flag.IntVar(&apiPort, "api-port", 8081, "Port to expose health check API")
	flag.Parse()

	http.HandleFunc("/overall_health", func(w http.ResponseWriter, r *http.Request) {
		healthCheckHandler(w, r, metricsPort)
	})

	log.Printf("Checking health on port %d", metricsPort)
	log.Printf("Starting health check API server on port %d", apiPort)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", apiPort), nil))
}

func healthCheckHandler(w http.ResponseWriter, r *http.Request, metricsPort int) {
	resp, err := http.Get(fmt.Sprintf("http://localhost:%d/metrics", metricsPort))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	re := regexp.MustCompile(`lava_consumer_overall_health (\d+)`)
	matches := re.FindStringSubmatch(string(body))
	if len(matches) > 1 && matches[1] == "1" {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Healthy"))
	} else {
		http.Error(w, "Unhealthy", http.StatusServiceUnavailable)
	}
}
