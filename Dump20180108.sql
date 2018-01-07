-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: pony_color_db
-- ------------------------------------------------------
-- Server version	5.7.20-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `body_part`
--

DROP TABLE IF EXISTS `body_part`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `body_part` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `body_part`
--

LOCK TABLES `body_part` WRITE;
/*!40000 ALTER TABLE `body_part` DISABLE KEYS */;
INSERT INTO `body_part` VALUES (1,'body'),(2,'hair'),(3,'eye'),(4,'wing');
/*!40000 ALTER TABLE `body_part` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `color`
--

DROP TABLE IF EXISTS `color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `color` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `value` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `color`
--

LOCK TABLES `color` WRITE;
/*!40000 ALTER TABLE `color` DISABLE KEYS */;
INSERT INTO `color` VALUES (1,'Синий-синий иней','9EDBF9'),(5,'Очень глубокий пурпурно-красный','460025'),(6,'Баклажановый','C6006F'),(7,'Карминно-розовый','EE4144'),(8,'Морковный','F37033'),(9,'Светло-песочный','FDF6AF'),(10,'Темный желто-зеленый','62BC4D'),(11,'Лазурный Крайола','1E98D3'),(12,'Глубокий фиолетовый','672F89'),(13,'Гридеперлевый','EBEFF1'),(14,'Королевский пурпурный Крайола','5E4FA2'),(15,'Полуночный синий Крайола','214871'),(16,'Темно-голубой','3978BB'),(17,'Пурпурное горное величие','B689C8'),(18,'Сигнальный синий','263773'),(19,'Глубокий пурпурно-розовый','ED438A'),(20,'Глубокий фиолетовый','662D8A'),(21,'Глубокий фиолетово-черный','22093F'),(22,'Глубокий фиолетовый','672F8B'),(23,'Амарантово-розовый','F3B6CF'),(24,'Глубокий пурпурно-розовый','ED458B'),(25,'Небесно-синий','186F98'),(26,'Светло-голубой','82D1F4'),(27,'Светло-песочный','FDF6AF'),(28,'Амарантово-розовый','F3B6CF'),(29,'Опаловый зеленый','35350'),(30,'Персидский зеленый','00ADA8'),(31,'Насыщенный красно-оранжевый','FFC261'),(32,'Светло-песочный','FDF6AF'),(33,'Сигнальный зеленый','2D7B3D'),(34,'Темный желто-зеленый','63BC4F'),(35,'Глициния (Глициниевый)','C590C9'),(36,'Зеленый чай','D7EBAE'),(37,'Изумрудный','50C355'),(38,'Сигнальный зеленый','2D7C3D'),(39,'Темный желто-зеленый','63BB4F'),(40,'Зелено-желтый Крайола','F4F49B'),(41,'Глубокий желто-розовый','F8415F'),(42,'Светлый карминово-розовый','E45762'),(43,'Пастельно-желтый','F2AF4D'),(44,'Насыщенный красно-оранжевый','FBBA64'),(45,'Фанданго','BF5D95'),(46,'Насыщенный фиолетовый','4A2463'),(47,'Пурпурное горное величие ','B38EC0'),(48,'Кадетский синий Крайола','C2C7D6'),(49,'Бананомания','FAF9AF'),(50,'Насыщенный желтый','E29D35'),(51,'Канареечный (Ярко-желтый)','EBFD89'),(52,'Дымчато-белый','EFEDEE'),(53,'Пурпурное горное величие','B28DC0'),(54,'Амарантово-розовый','F6B8D2'),(55,'Спаржа Крайола','71A66C'),(56,'Темный зеленый чай','B2D89E'),(57,'Кремовый','FEFDE7'),(58,'Синий цвета яиц странствующего дрозда','18E7E7'),(59,'Светлый джинсовый','3366CC'),(60,'Очень глубокий пурпурно-красный','460025'),(61,'Баклажановый','C6006F'),(62,'Аквамариновый','93FFDB'),(63,'Белый','FFFFFF'),(64,'Пыльный голубой','AFE8E7'),(65,'Шафраново-желтый','F6D449'),(66,'Яркий оранжевый','FB5D00');
/*!40000 ALTER TABLE `color` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pony`
--

DROP TABLE IF EXISTS `pony`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pony` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pony`
--

LOCK TABLES `pony` WRITE;
/*!40000 ALTER TABLE `pony` DISABLE KEYS */;
INSERT INTO `pony` VALUES (1,'Rainbow Dash'),(2,'Rarity'),(3,'Twilight Sparkle'),(4,'Pinkie Pie'),(5,'Fluttershy'),(6,'Applejack'),(7,'Spike'),(8,'Apple Bloom'),(9,'Scootaloo'),(10,'Derpy Hooves'),(11,'Sweetie Belle'),(12,'Vinyl Scratch / DJ PON-3'),(13,'Lyra Heartstrings');
/*!40000 ALTER TABLE `pony` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pony_color`
--

DROP TABLE IF EXISTS `pony_color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pony_color` (
  `color_id` int(11) NOT NULL,
  `pony_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  KEY `  color_id_fk_idx` (`color_id`),
  KEY `pony_id_fk_idx` (`pony_id`),
  KEY `type_id_fk_idx` (`type_id`),
  CONSTRAINT `  color_id_fk` FOREIGN KEY (`color_id`) REFERENCES `color` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pony_id_fk` FOREIGN KEY (`pony_id`) REFERENCES `pony` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `type_id_fk` FOREIGN KEY (`type_id`) REFERENCES `body_part` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pony_color`
--

LOCK TABLES `pony_color` WRITE;
/*!40000 ALTER TABLE `pony_color` DISABLE KEYS */;
INSERT INTO `pony_color` VALUES (1,1,1),(7,1,2),(8,1,2),(9,1,2),(10,1,2),(11,1,2),(12,1,2),(5,1,3),(6,1,3),(13,2,1),(14,2,2),(15,2,3),(16,2,3),(17,3,1),(18,3,2),(19,3,2),(20,3,2),(21,3,3),(22,3,3),(23,4,1),(24,4,2),(25,4,3),(26,4,3),(27,5,1),(28,5,2),(29,5,3),(30,5,3),(31,6,1),(32,6,2),(33,6,3),(34,6,3),(35,7,1),(36,7,1),(37,7,2),(38,7,3),(39,7,3),(40,8,1),(41,8,2),(42,8,3),(43,8,3),(44,9,1),(45,9,2),(46,9,3),(47,9,3),(48,10,1),(49,10,2),(50,10,3),(51,10,3),(52,11,1),(53,11,2),(54,11,2),(55,11,3),(56,11,3),(57,12,1),(58,12,2),(59,12,2),(60,12,3),(61,12,3),(62,13,1),(63,13,2),(64,13,2),(65,13,3),(66,13,3);
/*!40000 ALTER TABLE `pony_color` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-08  0:43:04
