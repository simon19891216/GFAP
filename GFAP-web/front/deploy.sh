pnpm run build
host=43.139.112.84
port=22
ssh -p $port ubuntu@$host rm -rf /home/ubuntu/www
scp -P $port -r ./dist ubuntu@$host:/home/ubuntu/www