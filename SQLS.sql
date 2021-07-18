CREATE DATABASE OrderData OWNER postgres;

CREATE TABLE vehicles (
    vid character varying(128) NOT NULL PRIMARY KEY,
    partner_name character varying(128),
    type character varying(128),
    capacity INTEGER
);


CREATE SEQUENCE order_id_seq;
CREATE TABLE orders (
    order_id character varying(128) NOT NULL,
    order_no BIGINT DEFAULT NEXTVAL('order_id_seq'),
    vid character varying(128),
    weight INTEGER,
    PRIMARY KEY (order_id),
    FOREIGN KEY(vid) REFERENCES vehicles(vid)
);
