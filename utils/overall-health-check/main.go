package main

import (
	"io"
	"log"
	"net/http"
	"regexp"
)

func main() {
	http.HandleFunc("/health", healthCheckHandler)
	log.Fatal(http.ListenAndServe(":8081", nil))
}

func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	resp, err := http.Get("http://localhost:9090/metrics")
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
