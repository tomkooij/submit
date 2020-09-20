# use `docker ps` to figure out container name
# (this is just a quick hack)
# restore? https://gist.github.com/spalladino/6d981f7b33f6e0afe6bb
CONTAINER="567e4"
MYSQLPASSWORD="donotpushpasswordstogithub"
docker exec $CONTAINER /usr/bin/mysqldump -u root --password=$MYSQLPASSWORD submit > backup.sql

