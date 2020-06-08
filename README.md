# GMail classifier

## Create DB

```
$ docker-compose up -d
$ docker exec -it mail_classifier_db_1 bash
# mysql -uroot -p
mysql> create database mail_classifier;
mysql> use mail_classifier;
mysql> create table mails(id INT(11) AUTO_INCREMENT NOT NULL, title VARCHAR(128) NOT NULL, to_user VARCHAR(32) NOT NULL, from_user VARCHAR(32) NOT NULL, text VARCHAR(1024) NOT NULL, PRIMARY KEY(id));
```