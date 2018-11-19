-- Adminer 4.6.3 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

CREATE DATABASE `nvm` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE `nvm`;

DROP TABLE IF EXISTS `autotype`;
CREATE TABLE `autotype` (
  `autotype_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`autotype_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `autotype` (`autotype_id`, `name`, `description`) VALUES
(1,	'Погрузчик',	''),
(2,	'Легковое авто',	''),
(3,	'Газель',	''),
(4,	'Автобус',	'');

DROP TABLE IF EXISTS `cars`;
CREATE TABLE `cars` (
  `car_id` int(11) NOT NULL AUTO_INCREMENT,
  `gosnomer` varchar(6) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `gruzopodemnost` float NOT NULL,
  `autotype_id` int(11) NOT NULL,
  `driver_id` int(11) NOT NULL,
  PRIMARY KEY (`car_id`),
  KEY `autotype_id` (`autotype_id`),
  KEY `driver_id` (`driver_id`),
  CONSTRAINT `cars_ibfk_1` FOREIGN KEY (`autotype_id`) REFERENCES `autotype` (`autotype_id`),
  CONSTRAINT `cars_ibfk_2` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`driver_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `cars` (`car_id`, `gosnomer`, `model`, `gruzopodemnost`, `autotype_id`, `driver_id`) VALUES
(1,	'A111AA',	'ВАЗ-2101',	0.7,	2,	1),
(2,	'B222BB',	'ВАЗ-2105',	0.8,	2,	2),
(3,	'C333CC',	'ВАЗ-21099',	1,	2,	3),
(4,	'E444EE',	'МАЗ-11',	11,	1,	4),
(5,	'H555HH',	'МАЗ-22',	22,	1,	5),
(6,	'K666KK',	'МАЗ-33',	33,	1,	6),
(7,	'E217TC',	'ГАЗ-3310',	3,	3,	7),
(8,	'T489CC',	'ГАЗ-3901',	5,	3,	8),
(9,	'M312CT',	'ГАЗ-3303',	3.7,	3,	9);

DROP TABLE IF EXISTS `drivers`;
CREATE TABLE `drivers` (
  `driver_id` int(11) NOT NULL AUTO_INCREMENT,
  `fio` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `vozrast` int(11) NOT NULL,
  PRIMARY KEY (`driver_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `drivers` (`driver_id`, `fio`, `vozrast`) VALUES
(1,	'Иванов Иван Иваныч',	25),
(2,	'Петров Петр Петрович',	30),
(3,	'Сидоров Сидор Сидорович',	35),
(4,	'Гончаренко Эдуард Петрович',	22),
(5,	'Филимонов Василий Викторович',	43),
(6,	'Садилов Александр Дмитриевич',	40),
(7,	'Зорин Максим Олегович',	29),
(8,	'Игнатьев Аркадий Алексеевич',	32),
(9,	'Бурков Иван Иванович',	37);

DROP TABLE IF EXISTS `logins`;
CREATE TABLE `logins` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `logins` (`login_id`, `login`, `password`) VALUES
(2,	'admin',	'admin'),
(3,	'user',	'qxCVh7Plxbj/.');

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `destination` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `car_id` int(11) NOT NULL,
  `driver_id` int(11) NOT NULL,
  `login_id` int(11) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `car_id` (`car_id`),
  KEY `driver_id` (`driver_id`),
  KEY `login_id` (`login_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`driver_id`),
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`login_id`) REFERENCES `logins` (`login_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- 2018-11-18 17:21:28
