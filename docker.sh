rm -rf index/migrations
docker rm -f scoreboard postgresql
docker-compose up -d postgresql
sleep 2
docker-compose up -d scoreboard
sleep 3
docker exec -i postgresql psql scoreboard < postgresql/user.sql