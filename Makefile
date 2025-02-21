DB_URL= postgresql://root:secret@localhost:5432/stock_news?sslmode=disable

posgresql:
	docker start db_postgres_1

createdb:
	docker exec -it  db_postgres_1 createdb --username=root --owner=root stock_news

migrateup:
	migrate -path db/migration -database "$(DB_URL)" -verbose up

dropdb:
	docker exec -it  db_postgres_1 dropdb --username=root stock_news

migratedown:
	migrate -path db/migration -database "$(DB_URL)" -verbose down

migration:
	migrate create -ext sql -dir db/migration -seq init_schema

new_migration:
	migrate create -ext sql -dir db/migration -seq $(name)