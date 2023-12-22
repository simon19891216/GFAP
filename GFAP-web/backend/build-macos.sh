#CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build  -ldflags "-s -w"
CGO_ENABLED=0 GOOS=darwin GOARCH=arm64 go build  -ldflags "-s -w"

