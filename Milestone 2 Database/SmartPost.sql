CREATE DATABASE  IF NOT EXISTS `smartpost` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `smartpost`;
-- MySQL dump 10.13  Distrib 8.0.15, for Win64 (x86_64)
--
-- Host: localhost    Database: smartpost
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `admin` (
  `gebruikersnaam` varchar(100) NOT NULL,
  `wachtwoord` varchar(500) NOT NULL,
  PRIMARY KEY (`gebruikersnaam`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eigenaar`
--

DROP TABLE IF EXISTS `eigenaar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `eigenaar` (
  `eigenaarID` int(11) NOT NULL AUTO_INCREMENT,
  `voornaam` varchar(50) DEFAULT NULL,
  `achternaam` varchar(45) DEFAULT NULL,
  `email` varchar(200) NOT NULL,
  `straat` varchar(200) DEFAULT NULL,
  `huisnummer` varchar(5) DEFAULT NULL,
  `postcode` varchar(10) DEFAULT NULL,
  `gemeente` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`eigenaarID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eigenaar`
--

LOCK TABLES `eigenaar` WRITE;
/*!40000 ALTER TABLE `eigenaar` DISABLE KEYS */;
/*!40000 ALTER TABLE `eigenaar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `geschiedenis`
--

DROP TABLE IF EXISTS `geschiedenis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `geschiedenis` (
  `geschiedenisID` int(11) NOT NULL,
  `sensorID` int(11) NOT NULL,
  `actie` varchar(200) DEFAULT NULL,
  `tijd_van_actie` datetime DEFAULT CURRENT_TIMESTAMP,
  `lockerID` int(11) DEFAULT NULL,
  `eigenaarID` int(11) DEFAULT NULL,
  PRIMARY KEY (`geschiedenisID`),
  KEY `fk_geschiedenis_eigenaar_idx` (`eigenaarID`),
  KEY `fk_geschiedenis_locker` (`lockerID`),
  KEY `fk_geschiedenis_sensor` (`sensorID`),
  CONSTRAINT `fk_geschiedenis_eigenaar` FOREIGN KEY (`eigenaarID`) REFERENCES `eigenaar` (`eigenaarID`),
  CONSTRAINT `fk_geschiedenis_locker` FOREIGN KEY (`lockerID`) REFERENCES `locker` (`lockerID`),
  CONSTRAINT `fk_geschiedenis_sensor` FOREIGN KEY (`sensorID`) REFERENCES `sensor` (`sensorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `geschiedenis`
--

LOCK TABLES `geschiedenis` WRITE;
/*!40000 ALTER TABLE `geschiedenis` DISABLE KEYS */;
/*!40000 ALTER TABLE `geschiedenis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inhoud`
--

DROP TABLE IF EXISTS `inhoud`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `inhoud` (
  `inhoudID` int(11) NOT NULL AUTO_INCREMENT,
  `EigenaarID` int(11) NOT NULL,
  `code` varchar(100) NOT NULL,
  PRIMARY KEY (`inhoudID`),
  KEY `fk_eigenaar_inhoud_idx` (`EigenaarID`),
  CONSTRAINT `fk_inhoud_eigenaar` FOREIGN KEY (`EigenaarID`) REFERENCES `eigenaar` (`eigenaarID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inhoud`
--

LOCK TABLES `inhoud` WRITE;
/*!40000 ALTER TABLE `inhoud` DISABLE KEYS */;
/*!40000 ALTER TABLE `inhoud` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locker`
--

DROP TABLE IF EXISTS `locker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `locker` (
  `lockerID` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(4) NOT NULL,
  `inhoudID` int(11) NOT NULL,
  PRIMARY KEY (`lockerID`),
  KEY `fk_locker_inhoud` (`inhoudID`),
  CONSTRAINT `fk_locker_inhoud` FOREIGN KEY (`inhoudID`) REFERENCES `inhoud` (`inhoudID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locker`
--

LOCK TABLES `locker` WRITE;
/*!40000 ALTER TABLE `locker` DISABLE KEYS */;
/*!40000 ALTER TABLE `locker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor`
--

DROP TABLE IF EXISTS `sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sensor` (
  `sensorID` int(11) NOT NULL AUTO_INCREMENT,
  `naam` varchar(45) NOT NULL,
  `functie` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`sensorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor`
--

LOCK TABLES `sensor` WRITE;
/*!40000 ALTER TABLE `sensor` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'smartpost'
--

--
-- Dumping routines for database 'smartpost'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-13 20:46:44
