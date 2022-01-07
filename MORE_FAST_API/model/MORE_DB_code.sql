-- CREATE DATABASE more;
--
-- CREATE SCHEMA IF NOT EXISTS more_table;
-- SET SEARCH_PATH TO more_table, public;

CREATE TABLE IF NOT EXISTS "country" (
  "idcountry" serial PRIMARY KEY,
  "name" varchar(30) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "product" (
  "idproduct" serial PRIMARY KEY,
  "name" text NOT NULL UNIQUE,
  "unit" varchar(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS "saplier" (
  "idsaplier" serial PRIMARY KEY,
  "name" text NOT NULL,
  "email" text NOT NULL ,
  "tel" text NOT NULL,
  CONSTRAINT  uniq_sap UNIQUE ("name", email, tel)
);

CREATE TABLE IF NOT EXISTS "delivery" (
  "iddelivery" serial,
  "idproduct" int NOT NULL ,
  "idcountry" int NOT NULL ,
  "idsumplier" int NOT NULL ,
  "unit_price" float NOT NULL ,
  quantity int NOT NULL,
  "date" timestamp NOT NULL DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS "warehouse" (
  "idstatemant" serial PRIMARY KEY,
  "idproduct" int,
  "quantity" float,
  "date" timestamp
);

CREATE TABLE IF NOT EXISTS "sale_price" (
  "idsale_price" serial PRIMARY KEY,
  "idproduct" int NOT NULL ,
  "price" float NOT NULL
);

CREATE TABLE IF NOT EXISTS "sale" (
  "idsale" serial,
  "idsale_price" int,
  "quantity" float,
  date timestamp NOT NULL DEFAULT current_timestamp
);

ALTER TABLE "delivery" ADD FOREIGN KEY ("idproduct") REFERENCES "product" ("idproduct");

ALTER TABLE "delivery" ADD FOREIGN KEY ("idsumplier") REFERENCES "saplier" ("idsaplier");

ALTER TABLE "delivery" ADD FOREIGN KEY ("idcountry") REFERENCES "country" ("idcountry");

ALTER TABLE "warehouse" ADD FOREIGN KEY ("idproduct") REFERENCES "product" ("idproduct");

ALTER TABLE "sale" ADD FOREIGN KEY ("idsale_price") REFERENCES "sale_price" ("idsale_price");

ALTER TABLE "sale_price" ADD FOREIGN KEY ("idproduct") REFERENCES "product" ("idproduct");


CREATE OR REPLACE FUNCTION insert_deliver_warehouse (prod_name text,c_name text, sup_name text,
                                                    u_price float, quant float)
RETURNS void
LANGUAGE plpgsql AS $$
    DECLARE
        id_prod int := (SELECT idproduct FROM product WHERE name=prod_name);

    BEGIN
        INSERT INTO delivery (idproduct, idcountry, idsumplier, unit_price, quantity)
        VALUES (
                 id_prod,
                 (SELECT idcountry FROM country WHERE name=c_name),
                 (SELECT idsaplier FROM saplier WHERE name=sup_name),
                 u_price,
                 quant
                );

        IF id_prod IN (SELECT idproduct FROM warehouse)
        THEN
            UPDATE warehouse
            SET quantity = quantity+quant
            WHERE idproduct=id_prod;
        ELSE
            INSERT INTO warehouse (idproduct, quantity)
            VALUES (
                    (SELECT idproduct FROM product WHERE name=prod_name),
                    quant
                   );
        END IF;
        END;
    $$;

CREATE OR REPLACE FUNCTION sale_transaction ( prod_name text, qunt int)
RETURNS void
LANGUAGE sql AS $$


    SELECT idproduct
    FROM product
    WHERE name = prod_name;

    INSERT INTO sale (idsale_price, quantity)
    VALUES (
            (SELECT idsale_price FROM sale_price WHERE idproduct=(SELECT idproduct
                                                                FROM product
                                                                WHERE name = prod_name)),
            qunt
            );

    UPDATE warehouse
    SET quantity= quantity-qunt
    WHERE idproduct=(SELECT idproduct
                    FROM product
                    WHERE name = prod_name);

    TRUNCATE  id_prod;
    $$;



