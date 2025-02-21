CREATE TABLE "stock_news" (
  "id" uuid PRIMARY KEY,
  "title" varchar,
  "link" varchar,
  "published_date" varchar,
  "source" varchar,
  "created_at" timestamptz NOT NULL DEFAULT(now()),
  "updated_at" timestamptz NOT NULL DEFAULT(now()),
  "deleted_at" timestamptz DEFAULT NULL
);


ALTER TABLE stock_news ADD CONSTRAINT unique_link UNIQUE (link);
