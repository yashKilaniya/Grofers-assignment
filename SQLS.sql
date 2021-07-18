CREATE DATABASE OrderData OWNER postgres;

CREATE TABLE vehicles (
    vid character varying(128) NOT NULL PRIMARY KEY,
    partner_name character varying(128) NOT NULL,
    vtype character varying(128),
    capacity INTEGER,
    orders_attached character varying(128)[]
);


CREATE SEQUENCE order_id_seq;
ALTER SEQUENCE order_id_seq RESTART;
CREATE TABLE orders (
    order_id character varying(128) NOT NULL,
    order_no BIGINT DEFAULT NEXTVAL('order_id_seq'),
    vid character varying(128),
    weight INTEGER,
    slot INTEGER NOT NULL,
    is_scheduled BOOLEAN,
    PRIMARY KEY (order_id),
    FOREIGN KEY(vid) REFERENCES vehicles(vid)
);
