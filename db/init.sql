CREATE DATABASE taxData;
use taxData;

CREATE TABLE IF NOT EXISTS taxables (
    `id` int AUTO_INCREMENT,
    `Item` VARCHAR(14) CHARACTER SET utf8,
    `Cost` NUMERIC(4, 2),
    `Tax` NUMERIC(3, 2),
    `Total` NUMERIC(4, 2),
    PRIMARY KEY (`id`)

);
INSERT INTO taxables (Item,Cost,Tax,Total) VALUES
    ('Socks',7.97,0.6,8.57),
    ('Baseball',2.97,0.22,3.19),
    ('Antiperspirant',1.29,0.1,1.39),
    ('DVD',14.96,1.12,16.08),
    ('Coffee',7.28,0.55,7.83),
    ('Sunscreen',6.68,0.5,7.18),
    ('Wrench Set',10,0.75,10.75),
    ('Chocolate',8.98,0.67,9.65),
    ('Sauce',2.12,0.16,2.28),
    ('Paperclips',6.19,0.46,6.65);