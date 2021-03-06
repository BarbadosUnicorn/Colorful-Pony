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
  `L` double DEFAULT NULL,
  `a` double DEFAULT NULL,
  `b` double DEFAULT NULL,
  `RGB` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `color`
--

LOCK TABLES `color` WRITE;
/*!40000 ALTER TABLE `color` DISABLE KEYS */;
INSERT INTO `color` VALUES (1,'\'Синий-синий иней\'',84.3659496028465,-12.124794829152297,-20.805895434839194,'#9EDBF9'),(5,'\'Очень глубокий пурпурно-красный\'',12.19305434527326,33.99055089684958,-3.0532750479519755,'#460025'),(6,'\'Баклажановый\'',42.993573076307584,70.94821455480243,-4.262843487134083,'#C6006F'),(7,'\'Карминно-розовый\'',54.422741762651356,65.42052687696798,38.4455290417378,'#EE4144'),(8,'\'Морковный\'',62.40793223078636,46.92166821798993,55.805889570537104,'#F37033'),(9,'\'Светло-песочный\'',95.95084207871201,-8.109454663914828,35.07319452283368,'#FDF6AF'),(10,'\'Темный желто-зеленый\'',68.82286811173445,-48.01497291689088,47.05179530109548,'#62BC4D'),(11,'\'Лазурный Крайола\'',59.375410735695795,-10.978787114108378,-39.03315777255578,'#1E98D3'),(12,'\'Глубокий фиолетовый\'',31.167194572555353,41.27764157400537,-40.12148986834389,'#672F89'),(13,'\'Гридеперлевый\'',94.20366097633274,-0.9624977564869353,-1.439083252676543,'#EBEFF1'),(14,'\'Королевский пурпурный Крайола\'',38.86437222429026,27.15624197561303,-43.046758527008755,'#5E4FA2'),(15,'\'Полуночный синий Крайола\'',29.788578211206364,0.8907690911158506,-27.677058945770995,'#214871'),(16,'\'Темно-голубой\'',49.36321452990187,2.022930689081992,-41.142074371711644,'#3978BB'),(17,'\'Пурпурное горное величие\'',63.348284501969275,28.451865441257052,-26.045583068395196,'#B689C8'),(18,'\'Сигнальный синий\'',24.896899625743863,14.260440941468138,-36.7335131782912,'#263773'),(19,'\'Глубокий пурпурно-розовый\'',55.94113032637668,69.28950611106276,-0.7719066794492857,'#ED438A'),(20,'\'Глубокий фиолетовый\'',30.727630652322176,42.28924393035677,-41.45488757516617,'#662D8A'),(21,'\'Глубокий фиолетово-черный\'',8.078256216193989,25.798874542734094,-29.07893606798732,'#22093F'),(22,'\'Глубокий фиолетовый\'',31.302304745676878,41.752126731249675,-41.142125191094394,'#672F8B'),(23,'\'Амарантово-розовый\'',80.1883552351843,25.80383843003059,-3.9420133589926465,'#F3B6CF'),(24,'\'Глубокий пурпурно-розовый\'',56.21257909850212,68.70859059438533,-0.9661341117462419,'#ED458B'),(25,'\'Небесно-синий\'',43.988235725952144,-9.642473456103973,-29.20658972916028,'#186F98'),(26,'\'Светло-голубой\'',80.11115606975538,-15.17442824834797,-24.74151086889369,'#82D1F4'),(27,'\'Светло-песочный\'',95.95084207871201,-8.109454663914828,35.07319452283368,'#FDF6AF'),(28,'\'Амарантово-розовый\'',80.1883552351843,25.80383843003059,-3.9420133589926465,'#F3B6CF'),(29,'\'Опаловый зеленый\'',31.31249680106928,-22.002044939514242,-4.429299781857043,'#035350'),(30,'\'Персидский зеленый\'',63.92890034745665,-37.47276880388129,-8.010730009849066,'#00ADA8'),(31,'\'Насыщенный красно-оранжевый\'',82.22078236899769,11.867773999231057,56.18461576798364,'#FFC261'),(32,'\'Светло-песочный\'',95.95084207871201,-8.109454663914828,35.07319452283368,'#FDF6AF'),(33,'\'Сигнальный зеленый\'',45.71726109994036,-38.06309796824173,26.87622042721677,'#2D7B3D'),(34,'\'Темный желто-зеленый\'',68.88405268496341,-47.49698164564548,46.21349531045418,'#63BC4F'),(35,'\'Глициния (Глициниевый)\'',66.5458038000655,29.641473144478237,-21.574014768908878,'#C590C9'),(36,'\'Зеленый чай\'',90.28465506393567,-16.767329344617888,27.475926173552057,'#D7EBAE'),(37,'\'Изумрудный\'',70.44939033313702,-54.57759321104305,45.08568330669669,'#50C355'),(38,'\'Сигнальный зеленый\'',46.056049760229364,-38.47630732069271,27.299733877368304,'#2D7C3D'),(39,'\'Темный желто-зеленый\'',68.57546580976454,-47.09024298457343,45.85507194273271,'#63BB4F'),(40,'\'Зелено-желтый Крайола\'',94.44090790387222,-12.822093052439643,42.90575217383817,'#F4F49B'),(41,'\'Глубокий желто-розовый\'',56.64740104965652,69.7088751608092,25.973289598000882,'#F8415F'),(42,'\'Светлый карминово-розовый\'',56.279729340206956,55.519947256680304,23.094989029809952,'#E45762'),(43,'\'Пастельно-желтый\'',76.11405348202786,15.242979290511105,58.16690846851631,'#F2AF4D'),(44,'\'Насыщенный красно-оранжевый\'',79.92420449035207,14.598793217717121,52.02445828445577,'#FBBA64'),(45,'\'Фанданго\'',53.031472912157156,45.97554087612954,-12.378081881550429,'#BF5D95'),(46,'\'Насыщенный фиолетовый\'',22.367681344130844,30.413799453564096,-30.273274957192264,'#4A2463'),(47,'\'Пурпурное горное величие \'',63.9461503091939,23.02770428057427,-20.663573207484596,'#B38EC0'),(48,'\'Кадетский синий Крайола\'',80.27580218124554,1.1920582258238555,-8.059756254632333,'#C2C7D6'),(49,'\'Бананомания\'',96.48020655551576,-10.710340765728743,35.7350418195371,'#FAF9AF'),(50,'\'Насыщенный желтый\'',69.85223814119477,16.92311068946045,61.319045409321305,'#E29D35'),(51,'\'Канареечный (Ярко-желтый)\'',95.8800333567077,-22.470298425955104,53.21912449232569,'#EBFD89'),(52,'\'Дымчато-белый\'',93.92280668727992,0.8496444336765219,-0.2565683899132587,'#EFEDEE'),(53,'\'Пурпурное горное величие\'',63.60689519057276,23.258354870911212,-21.189833493638854,'#B28DC0'),(54,'\'Амарантово-розовый\'',81.03087794699252,26.263017198607518,-4.285680846187412,'#F6B8D2'),(55,'\'Спаржа Крайола\'',63.231860581175866,-29.24929887946964,24.614090915623276,'#71A66C'),(56,'\'Темный зеленый чай\'',82.40310715062562,-22.994459151186252,24.601653839682804,'#B2D89E'),(57,'\'Кремовый\'',98.8640651492026,-3.3487285584392623,10.639670207796904,'#FEFDE7'),(58,'\'Синий цвета яиц странствующего дрозда\'',83.50313312969486,-43.93921004057688,-12.956322732331493,'#18E7E7'),(59,'\'Светлый джинсовый\'',45.03419824487175,18.721198307832477,-57.85925972713217,'#3366CC'),(60,'\'Очень глубокий пурпурно-красный\'',12.19305434527326,33.99055089684958,-3.0532750479519755,'#460025'),(61,'\'Баклажановый\'',42.993573076307584,70.94821455480243,-4.262843487134083,'#C6006F'),(62,'\'Аквамариновый\'',92.94325502554685,-39.29017607400992,7.502323947107525,'#93FFDB'),(63,'\'Белый\'',100,0.00526049995830391,-0.010408184525267927,'#FFFFFF'),(64,'\'Пыльный голубой\'',88.25501700099187,-18.182504634448925,-5.410959019260875,'#AFE8E7'),(65,'\'Шафраново-желтый\'',85.58510209456435,-2.4886376182896575,69.69645666132844,'#F6D449'),(66,'\'Яркий оранжевый\'',60.19281800666907,57.485328853058185,69.86213083317337,'#FB5D00');
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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pony`
--

LOCK TABLES `pony` WRITE;
/*!40000 ALTER TABLE `pony` DISABLE KEYS */;
INSERT INTO `pony` VALUES (1,'\'Rainbow Dash\''),(2,'\'Rarity\''),(3,'\'Twilight Sparkle\''),(4,'\'Pinkie Pie\''),(5,'\'Fluttershy\''),(6,'\'Applejack\''),(7,'\'Spike\''),(8,'\'Apple Bloom\''),(9,'\'Scootaloo\''),(10,'\'Derpy Hooves\''),(11,'\'Sweetie Belle\''),(12,'\'Vinyl Scratch / DJ PON-3\''),(13,'\'Lyra Heartstrings\'');
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

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(45) NOT NULL,
  `time_stamp` varchar(29) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES (1,'\'R1hRjRdnkHOOmkN7ZksE7BHm7B6HWXPrUWtGa5YYoqf\'','Fri, 22-Jun-2018 19:03:36 GMT',18),(12,'\'MzRth7ukqvocAp87WBHtDNQMBvZ1rkmE92jTtPs5CUp\'','Fri, 22-Jun-2018 19:26:04 GMT',18),(13,'\'n4WGTVUggtFw7X1EmW5nh3LgZY5aNGvhZNel4LxoHbO\'','Fri, 22-Jun-2018 19:27:34 GMT',18),(14,'\'ggti3MC39A9JyUZRyG6rN24ztlfH5IBAcAbqUVlscXr\'','Fri, 22-Jun-2018 19:27:42 GMT',18),(18,'\'PLqRYYsPkQYiglt5wid6Q26StvMoY1GAY6LYSlNtLiY\'','Wed, 27-Jun-2018 17:22:06 GMT',18),(21,'\'EaLGlqIuKIOQoFBUtuqlKb0FTSsoJwPy3cdB98RFz2M\'','Wed, 27-Jun-2018 17:24:33 GMT',18),(29,'\'XNDwHyD9k3UAlA46sNNcqPSTUle2ClfaQp4j5M5lmhf\'','Wed, 27-Jun-2018 19:11:36 GMT',18),(30,'\'t78E189fSPspHJyAImtutCBFIvWVQZNJlJa8Q7JmjJT\'','Wed, 27-Jun-2018 19:13:30 GMT',18),(31,'\'NSCm55bLDiwb3yNwIUoCXJxIf0wLCg3TriDOal7udcz\'','Wed, 27-Jun-2018 19:15:34 GMT',18),(32,'\'atYEOI3Lhvpi3umP3H7jbfkdSk9ETTPR1VwpY4KxQ2O\'','Wed, 27-Jun-2018 19:16:54 GMT',18),(38,'\'nPBmNMm3pXi7JDxCdQmAJaJutud5KSlbVbyNIRVDGY6\'','Wed, 27-Jun-2018 19:21:32 GMT',18),(42,'\'Q7GZuq6E1nHg40yXnmoI7foLf8eIrARlXpSYw2soRrD\'','Wed, 27-Jun-2018 19:26:36 GMT',18),(43,'\'MS4f1b7HzMbxLUrz8UCzqFb2gkbanbwm3ikY4eRJVTS\'','Wed, 27-Jun-2018 19:27:53 GMT',18),(44,'\'hImrj60Zr9ztRbpP8f4pHGtoG3uxTRgj8mTuuORDQXP\'','Wed, 27-Jun-2018 19:28:42 GMT',18),(45,'\'uS7edfH1xZvNjhI5AIQ6HzQlcwtclzaThqSLMdhVLzq\'','Wed, 27-Jun-2018 19:32:21 GMT',18),(46,'\'PtGLVzspcEerEUJt1XBSwvmr4qJFAqj4FJCX5sTP5vy\'','Wed, 27-Jun-2018 19:36:53 GMT',18),(47,'\'QjE1V4kQI59KxRqXIUhiwGEFQK8ddMkK4D2YgdKhUT7\'','Wed, 27-Jun-2018 19:41:50 GMT',18),(48,'\'pW1AYsMEQqT5BE83TfSNhKmej7QeQUh9xPn0pNCFz2S\'','Wed, 27-Jun-2018 19:42:44 GMT',18),(49,'\'qKMxRJFjUyHc4gmb5SCZsiuE19TDYI0lqcCvt3HEhVw\'','Wed, 27-Jun-2018 19:44:17 GMT',18),(50,'\'T6SWD80qdUMZNuGn6WvwnSoGuxfBD3P8mW1lNnhvyoW\'','Wed, 27-Jun-2018 19:45:57 GMT',18),(51,'\'TIMGIZAdVGCUJsDBB4jkZ1rmERTz8eI1y3QPsu6Xhy2\'','Wed, 27-Jun-2018 19:46:54 GMT',18),(52,'\'P1NhnGaowiLxn0DrJUM3z3ZUIxSav3urqggmNctVQwm\'','Wed, 27-Jun-2018 19:47:37 GMT',18),(53,'\'ewUZKdyZirAyatw4q3JmaPybXraOEdBMGldzYUGC2p0\'','Wed, 27-Jun-2018 19:48:45 GMT',18),(54,'\'tEdSoqGbFmBGNvBq3DdsSZHzdrMQzJ9FZE6FB5Stnv3\'','Wed, 27-Jun-2018 19:51:13 GMT',18),(55,'\'H2c7tX4jS1QA1RJgTQrmPmBOSaDV1qWIHOnyhSI5YFU\'','Wed, 27-Jun-2018 19:53:10 GMT',18),(56,'\'xSjlYdq7YQNXutotde739GccBBFZgZBsarMIOuf0y7A\'','Wed, 27-Jun-2018 19:55:42 GMT',18),(57,'\'V6jhXtN4XL2f6EoWWKyNFStVBp0OYx19YVkx7CeSZxq\'','Wed, 27-Jun-2018 19:56:40 GMT',18),(58,'\'6DrcLvl957azui9AiF5RNeBi4NktC7iz2aNQzCJ3zuc\'','Wed, 27-Jun-2018 19:57:24 GMT',18),(59,'\'XXq4fE5UWrbkLudx3lmv6jlNX4Elq8vsRUciqfMfllq\'','Wed, 27-Jun-2018 19:58:28 GMT',18),(60,'\'oGgkyytBTLeNkI4r7pJugSsyZhJWEjIsTIOKcVaeM5p\'','Wed, 27-Jun-2018 19:59:52 GMT',18),(69,'\'03Wk2Pyzg4fGO6y09sB30rfG3uXNh2mZBgi3r9HCPas\'','Wed, 27-Jun-2018 20:19:45 GMT',18),(74,'\'nX751loCtRgl6U4nMFqwvSDj7wktxLERsKwYFNlZCMc\'','Mon, 22-Oct-2018 10:14:38 GMT',18),(75,'\'2ao0JPcYTMWKCKfha1SQfVuQpKIHiWXcD8GpHqywefS\'','Mon, 22-Oct-2018 10:32:45 GMT',23),(76,'\'z3Cjg4jdnxflXcnikOPuVhddFvQPCWodY0VA4J8s0LM\'','Mon, 22-Oct-2018 10:32:53 GMT',23),(77,'\'pPNX7fWNAFA0GHmrWu5hcVlbKF6PE40GHs85HIqUjA3\'','Mon, 22-Oct-2018 10:33:09 GMT',23);
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(256) NOT NULL,
  `hash` varchar(60) NOT NULL,
  `salt_one` varchar(32) NOT NULL,
  `verification_code` varchar(72) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `role` varchar(16) NOT NULL,
  `ban` bigint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (18,'\'xtraand0ne@gmail.com\'','$2b$12$oG6OZeeyYArkO8uj/Drc4OdYgFjLuYj6Zh4kXLQM8RGcqoHmVjspy','UcM6V49fYOE29Iat15LVhIqtehn4qBRx','\'zMZAADT4S6aRhOhThtx8Uy8oXTatiQvVecgGN2w9TKkfYrlEWXkZtlGRQrDRYgbayt2BrR\'',1,'admin',0),(20,'\'pcolorfulpony@gmail.com\'','$2b$12$OHn/0k7sJaFlhPacQQaw..jY.OEJrcNDLTBOD1aclSi5wqzHb/GWu','F8TLpWaRgjkgpIKGFYUz3biwjoNT6gR5','\'L1aUahLch4uK9aTAVwQPHB12LWKy7aJnw742rAXa0lWa1wCcf2D6aCVoeIIXDRFuhHe99d\'',0,'user',0),(22,'\'temp.banned@gmail.com\'','$2b$12$4F8rUsDbuoqyfU758uJkyOPgA8Ml94EoYhuy28p1FqKkSQwxZUmYK','RPG5UxEyJoOSQAHkCCjTaEGZuJOLd4Bv','0',1,'user',4670438400),(23,'\'perm.banned@gmail.com\'','$2b$12$dNSzjFMyXELBLHiYILoJ.uZ1Pdr8htJ6vHUMuolbxT4QlauBGgvnC','8vMoqLZPjVF0sQjG47HTxdU92eOM1oPf','11',2,'user',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-21 14:44:57
