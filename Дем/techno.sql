-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: techno
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `equipment_id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(255) DEFAULT NULL,
  `serial_number` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
INSERT INTO `equipment` VALUES (1,'Laptop','SN123456','Office 1'),(2,'Printer','SN654321','Office 2'),(3,'Router','SN111222','Server Room'),(4,'Projector','SN333444','Conference Room');
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `executionreport`
--

DROP TABLE IF EXISTS `executionreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `executionreport` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `execution_id` int DEFAULT NULL,
  `resources_used` text,
  `fault_cause` text,
  `assistance_provided` text,
  `report_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`report_id`),
  KEY `execution_id` (`execution_id`),
  CONSTRAINT `executionreport_ibfk_1` FOREIGN KEY (`execution_id`) REFERENCES `requestexecution` (`execution_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `executionreport`
--

LOCK TABLES `executionreport` WRITE;
/*!40000 ALTER TABLE `executionreport` DISABLE KEYS */;
INSERT INTO `executionreport` VALUES (1,1,'Power supply unit','Power surge','Technical support from vendor','2024-06-11 07:28:37'),(2,2,'None','Paper jam','None','2024-06-11 07:28:37'),(3,3,'None','Misconfiguration','Network team support','2024-06-11 07:28:37'),(4,4,'Projector bulb','Wear and tear','None','2024-06-11 07:28:37');
/*!40000 ALTER TABLE `executionreport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitoring`
--

DROP TABLE IF EXISTS `monitoring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monitoring` (
  `monitoring_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int DEFAULT NULL,
  `response_time` time DEFAULT NULL,
  `processing_time` time DEFAULT NULL,
  `execution_time` time DEFAULT NULL,
  `total_cost` decimal(10,2) DEFAULT NULL,
  `quality_rating` int DEFAULT NULL,
  `monitoring_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`monitoring_id`),
  KEY `request_id` (`request_id`),
  CONSTRAINT `monitoring_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `repairrequest` (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitoring`
--

LOCK TABLES `monitoring` WRITE;
/*!40000 ALTER TABLE `monitoring` DISABLE KEYS */;
INSERT INTO `monitoring` VALUES (1,1,'00:30:00','01:00:00','01:30:00',100.00,5,'2024-06-11 07:28:37'),(2,2,'00:15:00','00:45:00','01:00:00',50.00,4,'2024-06-11 07:28:37'),(3,3,'01:00:00','02:00:00','03:00:00',75.00,3,'2024-06-11 07:28:37'),(4,4,'00:45:00','01:15:00','02:00:00',25.00,5,'2024-06-11 07:28:37');
/*!40000 ALTER TABLE `monitoring` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repairrequest`
--

DROP TABLE IF EXISTS `repairrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repairrequest` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `equipment_id` int DEFAULT NULL,
  `requester_name` varchar(255) DEFAULT NULL,
  `description` text,
  `priority` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `creation_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`request_id`),
  KEY `equipment_id` (`equipment_id`),
  CONSTRAINT `repairrequest_ibfk_1` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repairrequest`
--

LOCK TABLES `repairrequest` WRITE;
/*!40000 ALTER TABLE `repairrequest` DISABLE KEYS */;
INSERT INTO `repairrequest` VALUES (1,1,'John Doe','Laptop not turning on','high','в ожидании','2024-06-11 07:28:37','2024-06-11 07:28:37'),(2,2,'Jane Smith','Printer not printing','medium','в работе','2024-06-11 07:28:37','2024-06-11 07:28:37'),(3,3,'Alice Johnson','Router not connecting','high','в ожидании','2024-06-11 07:28:37','2024-06-11 07:28:37'),(4,4,'Bob Brown','Projector bulb blown','low','выполнено','2024-06-11 07:28:37','2024-06-11 07:28:37'),(5,1,'вааккуку','мекмекмекмкем','средний','выполнено','2024-06-11 07:31:34','2024-06-11 07:31:54');
/*!40000 ALTER TABLE `repairrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requestexecution`
--

DROP TABLE IF EXISTS `requestexecution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requestexecution` (
  `execution_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int DEFAULT NULL,
  `executor_name` varchar(255) DEFAULT NULL,
  `execution_details` text,
  `execution_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `parts_ordered` text,
  `parts_received` text,
  `coordination_required` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`execution_id`),
  KEY `request_id` (`request_id`),
  CONSTRAINT `requestexecution_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `repairrequest` (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requestexecution`
--

LOCK TABLES `requestexecution` WRITE;
/*!40000 ALTER TABLE `requestexecution` DISABLE KEYS */;
INSERT INTO `requestexecution` VALUES (1,1,'John Doe','Replaced power supply','2024-06-11 07:28:37','Power supply','Yes',0),(2,2,'Jane Smith','Cleared paper jam','2024-06-11 07:28:37','None','N/A',0),(3,3,'Alice Johnson','Reconfigured network settings','2024-06-11 07:28:37','None','N/A',1),(4,4,'Bob Brown','Replaced projector bulb','2024-06-11 07:28:37','Bulb','Yes',0);
/*!40000 ALTER TABLE `requestexecution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requestprocessing`
--

DROP TABLE IF EXISTS `requestprocessing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requestprocessing` (
  `processing_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int DEFAULT NULL,
  `processor_name` varchar(255) DEFAULT NULL,
  `analysis` text,
  `assigned_to` varchar(255) DEFAULT NULL,
  `processing_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`processing_id`),
  KEY `request_id` (`request_id`),
  CONSTRAINT `requestprocessing_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `repairrequest` (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requestprocessing`
--

LOCK TABLES `requestprocessing` WRITE;
/*!40000 ALTER TABLE `requestprocessing` DISABLE KEYS */;
INSERT INTO `requestprocessing` VALUES (1,1,'Michael Green','Power issue suspected','John Doe','2024-06-11 07:28:37'),(2,2,'Michael Green','Paper jam issue','Jane Smith','2024-06-11 07:28:37'),(3,3,'Sarah Blue','Network issue suspected','Alice Johnson','2024-06-11 07:28:37'),(4,4,'Sarah Blue','Bulb needs replacement','Bob Brown','2024-06-11 07:28:37');
/*!40000 ALTER TABLE `requestprocessing` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-11 10:32:54
