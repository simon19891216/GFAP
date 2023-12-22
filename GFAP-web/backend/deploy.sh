rm -rf ./build

CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags "-s -w" -o ./build/backend

host=43.139.112.84
port=22

scp -P $port config.yml ubuntu@$host:/home/ubuntu/

ssh -p $port ubuntu@$host sudo systemctl stop gfap_backend.service
scp -P $port ./build/backend ubuntu@$host:/home/ubuntu/
ssh -p $port ubuntu@$host sudo systemctl start gfap_backend.service

