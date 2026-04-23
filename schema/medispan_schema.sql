-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: medispan_rxmax_april
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `mf2desc_u`
--

DROP TABLE IF EXISTS `mf2desc_u`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2desc_u` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `Type_Code` int NOT NULL,
  `Transaction_CD` varchar(1) DEFAULT NULL,
  `Description` varchar(250) DEFAULT NULL,
  `Reserve` varchar(67) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`,`Type_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2dfdrg_r`
--

DROP TABLE IF EXISTS `mf2dfdrg_r`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2dfdrg_r` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Drug_Name_ID` bigint DEFAULT NULL,
  `Dose_Form_ID` int DEFAULT NULL,
  `Status` int DEFAULT NULL,
  `Link_Value` bigint DEFAULT NULL,
  `Link_Date` bigint DEFAULT NULL,
  `Reserve` varchar(28) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2drg_t`
--

DROP TABLE IF EXISTS `mf2drg_t`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2drg_t` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Routed_Drug_ID` bigint DEFAULT NULL,
  `Dose_Form_ID` int DEFAULT NULL,
  `Strength` varchar(15) DEFAULT NULL,
  `Strength_Unit_Of_Measure` varchar(15) DEFAULT NULL,
  `Name_Source` int DEFAULT NULL,
  `Device_Flag` int DEFAULT NULL,
  `Status` int DEFAULT NULL,
  `Link_Value` bigint DEFAULT NULL,
  `Link_Date` bigint DEFAULT NULL,
  `Routed_Drug_Form_ID` bigint DEFAULT NULL,
  `Drug_Dose_Form_ID` bigint DEFAULT NULL,
  `Strength_Strength_UOM_ID` bigint DEFAULT NULL,
  `Reserve` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2drgnm_p`
--

DROP TABLE IF EXISTS `mf2drgnm_p`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2drgnm_p` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Name_Type` varchar(1) DEFAULT NULL,
  `Status` int DEFAULT NULL,
  `Link_Value` bigint DEFAULT NULL,
  `Link_Date` bigint DEFAULT NULL,
  `Reserve` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2err_k`
--

DROP TABLE IF EXISTS `mf2err_k`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2err_k` (
  `Key_Identifier` varchar(1) DEFAULT NULL,
  `Unique_Key` varchar(19) DEFAULT NULL,
  `Data_Element_Code` varchar(4) DEFAULT NULL,
  `Data_Element_Length` int DEFAULT NULL,
  `Reserve` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2frm_w`
--

DROP TABLE IF EXISTS `mf2frm_w`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2frm_w` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `Transaction_CD` varchar(1) DEFAULT NULL,
  `Status` int DEFAULT NULL,
  `Link_Value` bigint DEFAULT NULL,
  `Link_Date` bigint DEFAULT NULL,
  `Reserve` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2gppc_j`
--

DROP TABLE IF EXISTS `mf2gppc_j`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2gppc_j` (
  `Generic_Product_Packaging_Code` varchar(8) NOT NULL,
  `Package_Size` float DEFAULT NULL,
  `Package_Size_Unit_of_Measure` varchar(2) DEFAULT NULL,
  `Package_Quantity` int DEFAULT NULL,
  `Unit_DoseUnit_of_Use_Package` varchar(1) DEFAULT NULL,
  `Package_Description_Code` varchar(2) DEFAULT NULL,
  `Generic_Product_Identifier` varchar(14) DEFAULT NULL,
  `Reserve` varchar(14) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Last_Change_Date` bigint DEFAULT NULL,
  PRIMARY KEY (`Generic_Product_Packaging_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2gpr_l`
--

DROP TABLE IF EXISTS `mf2gpr_l`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2gpr_l` (
  `Generic_Product_Packaging_Code` varchar(8) NOT NULL,
  `GPPC_Price_Code` varchar(1) NOT NULL,
  `Effective_Date` bigint NOT NULL,
  `Unit_Price` float DEFAULT NULL,
  `Reserve` varchar(27) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Last_Change_Date` bigint DEFAULT NULL,
  PRIMARY KEY (`Generic_Product_Packaging_Code`,`GPPC_Price_Code`,`Effective_Date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2idrg_2`
--

DROP TABLE IF EXISTS `mf2idrg_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2idrg_2` (
  `Ingredient_Drug_ID` bigint NOT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `CAS_Number` varchar(20) DEFAULT NULL,
  `Knowledge_Base_Drug_Code_7` bigint DEFAULT NULL,
  `Reserve_1` varchar(3) DEFAULT NULL,
  `Ingredient_Drug_Name` varchar(60) DEFAULT NULL,
  `Generic_ID` varchar(10) DEFAULT NULL,
  `Reserve_2` varchar(17) DEFAULT NULL,
  PRIMARY KEY (`Ingredient_Drug_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2ings_z`
--

DROP TABLE IF EXISTS `mf2ings_z`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2ings_z` (
  `Ingredient_Set_ID` bigint NOT NULL,
  `Ingredient_Indentifier` bigint NOT NULL,
  `ActiveInactive_Ingredient_Flag` varchar(1) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Reserve` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Ingredient_Set_ID`,`Ingredient_Indentifier`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2lab_i`
--

DROP TABLE IF EXISTS `mf2lab_i`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2lab_i` (
  `Medi_Span_Labeler_Identifier` int DEFAULT NULL,
  `Manufacturers_Labeler_Name` varchar(30) DEFAULT NULL,
  `Manufacturers_Abbreviated_Name` varchar(10) DEFAULT NULL,
  `Labeler_Type_Code` varchar(1) DEFAULT NULL,
  `Reserve` varchar(9) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Last_Change_Date` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2mod_n`
--

DROP TABLE IF EXISTS `mf2mod_n`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2mod_n` (
  `Modifier_Code` varchar(6) NOT NULL,
  `Modifier_Description` varchar(25) DEFAULT NULL,
  `Reserve` varchar(24) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Last_Change_Date` bigint DEFAULT NULL,
  PRIMARY KEY (`Modifier_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2name_f`
--

DROP TABLE IF EXISTS `mf2name_f`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2name_f` (
  `Drug_Descriptor_Identifier` int NOT NULL,
  `Drug_Name` varchar(30) DEFAULT NULL,
  `Route_of_Administration` varchar(2) DEFAULT NULL,
  `Dosage_Form` varchar(4) DEFAULT NULL,
  `Strength` varchar(15) DEFAULT NULL,
  `Strength_Unit_of_Measure` varchar(10) DEFAULT NULL,
  `Bioequivalence_Code` varchar(1) DEFAULT NULL,
  `Controlled_Substance_Code` varchar(1) DEFAULT NULL,
  `Efficacy_Code` varchar(1) DEFAULT NULL,
  `Legend_Indicator_Code` varchar(1) DEFAULT NULL,
  `Multi_Source_Summary_Code` varchar(1) DEFAULT NULL,
  `Brand_Name_Code` varchar(1) DEFAULT NULL,
  `Name_Source_Code` varchar(1) DEFAULT NULL,
  `Generic_Product_Identifier` varchar(14) DEFAULT NULL,
  `Knowledge_Base_Drug_Code` bigint DEFAULT NULL,
  `New_Drug_Descriptor_Identifier` int DEFAULT NULL,
  `Screenable_Flag` varchar(1) DEFAULT NULL,
  `KDC_Flag` varchar(1) DEFAULT NULL,
  `LocalSystemic_Code` varchar(1) DEFAULT NULL,
  `Maintenance_Drug_Code` varchar(1) DEFAULT NULL,
  `Form_Type_Code` varchar(1) DEFAULT NULL,
  `Internal_External_Code` varchar(1) DEFAULT NULL,
  `Single_Combination_Code` varchar(1) DEFAULT NULL,
  `Representative_GPI_Flag` varchar(1) DEFAULT NULL,
  `Representative_KDC_Flag` varchar(1) DEFAULT NULL,
  `Reserve` varchar(6) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Last_Change_Date` bigint DEFAULT NULL,
  PRIMARY KEY (`Drug_Descriptor_Identifier`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2ndc_h`
--

DROP TABLE IF EXISTS `mf2ndc_h`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2ndc_h` (
  `NDC_UPC_HRI` varchar(11) NOT NULL,
  `Drug_Descriptor_Identifier` int DEFAULT NULL,
  `TEE_Code` varchar(2) DEFAULT NULL,
  `DEA_Class_Code` varchar(1) DEFAULT NULL,
  `DESI_Code` varchar(1) DEFAULT NULL,
  `RX_OTC_Indicator_Code` varchar(1) DEFAULT NULL,
  `Generic_Product_Packaging_Code` varchar(8) DEFAULT NULL,
  `Old_NDC_UPC_HRI` varchar(11) DEFAULT NULL,
  `New_NDC_UPC_HRI` varchar(11) DEFAULT NULL,
  `Repackage_Code` varchar(1) DEFAULT NULL,
  `ID_Number_Format_Code` varchar(1) DEFAULT NULL,
  `Third_Party_Restriction_Code` varchar(1) DEFAULT NULL,
  `Knowledge_Base_Drug_Code` bigint DEFAULT NULL,
  `KDC_Flag` varchar(1) DEFAULT NULL,
  `Medi_Span_Labeler_Identifier` int DEFAULT NULL,
  `Multi_Source_Code` varchar(1) DEFAULT NULL,
  `Name_Type_Code` varchar(1) DEFAULT NULL,
  `Item_Status_Flag` varchar(1) DEFAULT NULL,
  `Innerpack_Code` varchar(1) DEFAULT NULL,
  `Clinic_Pack_Code` varchar(1) DEFAULT NULL,
  `Reserve_1` varchar(2) DEFAULT NULL,
  `PPG_Indicator_Code` varchar(1) DEFAULT NULL,
  `HFPG_Indicator_Code` varchar(1) DEFAULT NULL,
  `Dispensing_Unit_Code` varchar(1) DEFAULT NULL,
  `Dollar_Rank_Code` varchar(1) DEFAULT NULL,
  `Rx_Rank_Code` varchar(1) DEFAULT NULL,
  `Storage_Condition_Code` varchar(1) DEFAULT NULL,
  `Limited_Distribution_Code` varchar(2) DEFAULT NULL,
  `Old_Effective_Date` bigint DEFAULT NULL,
  `New_Effective_Date` bigint DEFAULT NULL,
  `Next_Smaller_NDC_Suffix_Number` varchar(2) DEFAULT NULL,
  `Next_Larger_NDC_Suffix_Number` varchar(2) DEFAULT NULL,
  `Reserve_2` varchar(13) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Last_Change_Date` bigint DEFAULT NULL,
  PRIMARY KEY (`NDC_UPC_HRI`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2ndcm_o`
--

DROP TABLE IF EXISTS `mf2ndcm_o`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2ndcm_o` (
  `NDC_UPC_HRI` varchar(11) NOT NULL,
  `Modifier_Code` varchar(6) NOT NULL,
  `Reserve` varchar(6) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Last_Change_Date` bigint DEFAULT NULL,
  PRIMARY KEY (`NDC_UPC_HRI`,`Modifier_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2prc_m`
--

DROP TABLE IF EXISTS `mf2prc_m`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2prc_m` (
  `NDC_UPC_HRI` varchar(11) NOT NULL,
  `Price_Code` varchar(1) NOT NULL,
  `Effective_Date` bigint NOT NULL,
  `Unit_Price` float DEFAULT NULL,
  `Unit_Price___Extended` float DEFAULT NULL,
  `Package_Price` float DEFAULT NULL,
  `AWP_Indicator_Code` varchar(1) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Last_Change_Date` bigint DEFAULT NULL,
  PRIMARY KEY (`NDC_UPC_HRI`,`Price_Code`,`Effective_Date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2rnm_4`
--

DROP TABLE IF EXISTS `mf2rnm_4`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2rnm_4` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `ID_for_Generic_Named_Drug` bigint NOT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Medi_Span_Reference_Flag` varchar(1) DEFAULT NULL,
  `Reserve` varchar(19) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`,`ID_for_Generic_Named_Drug`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2rtdf_s`
--

DROP TABLE IF EXISTS `mf2rtdf_s`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2rtdf_s` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Routed_Drug_ID` bigint DEFAULT NULL,
  `Dose_Form_ID` int DEFAULT NULL,
  `Status` int DEFAULT NULL,
  `Link_Value` bigint DEFAULT NULL,
  `Link_Date` bigint DEFAULT NULL,
  `Reserve` varchar(28) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2rtdrg_q`
--

DROP TABLE IF EXISTS `mf2rtdrg_q`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2rtdrg_q` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `Transaction_CD` varchar(1) DEFAULT NULL,
  `Drug_Name_ID` bigint DEFAULT NULL,
  `Route_ID` int DEFAULT NULL,
  `Status` int DEFAULT NULL,
  `Link_Value` bigint DEFAULT NULL,
  `Link_Date` bigint DEFAULT NULL,
  `Reserve` varchar(28) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2rte_v`
--

DROP TABLE IF EXISTS `mf2rte_v`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2rte_v` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `Transaction_CD` varchar(1) DEFAULT NULL,
  `Status` int DEFAULT NULL,
  `Link_Value` bigint DEFAULT NULL,
  `Link_Date` bigint DEFAULT NULL,
  `Reserve` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2sec_3`
--

DROP TABLE IF EXISTS `mf2sec_3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2sec_3` (
  `External_Drug_ID` varchar(20) NOT NULL,
  `External_Drug_ID_Format_Code` varchar(1) NOT NULL,
  `Alternate_Drug_ID` varchar(20) NOT NULL,
  `Alternate_Drug_ID_Format_Code` varchar(1) NOT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Reserve` varchar(21) DEFAULT NULL,
  PRIMARY KEY (`External_Drug_ID`,`External_Drug_ID_Format_Code`,`Alternate_Drug_ID`,`Alternate_Drug_ID_Format_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2set_y`
--

DROP TABLE IF EXISTS `mf2set_y`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2set_y` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` varchar(20) NOT NULL,
  `Ingredient_Set_ID` bigint DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Representative_Set_Indicator` varchar(1) DEFAULT NULL,
  `Reserve` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2str_1`
--

DROP TABLE IF EXISTS `mf2str_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2str_1` (
  `Ingredient_Indentifier` bigint NOT NULL,
  `Reserve_1` varchar(2) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Ingredient_Drug_ID` bigint DEFAULT NULL,
  `Ingredient_Strength_Value` float DEFAULT NULL,
  `Ingredient_Strength_UOMcombin` varchar(11) DEFAULT NULL,
  `Ingredient_Strength_UOMindivi` varchar(11) DEFAULT NULL,
  `Volume_Value` float DEFAULT NULL,
  `Volume_Unit_of_Measure` varchar(11) DEFAULT NULL,
  `Reserve_2` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`Ingredient_Indentifier`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2stuom_x`
--

DROP TABLE IF EXISTS `mf2stuom_x`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2stuom_x` (
  `Concept_Type` int NOT NULL,
  `Country_Code` int NOT NULL,
  `Concept_ID` bigint NOT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Strength` varchar(15) DEFAULT NULL,
  `Strength_Unit_of_Measure` varchar(15) DEFAULT NULL,
  `Status` int DEFAULT NULL,
  `Link_Value` bigint DEFAULT NULL,
  `Link_Date` bigint DEFAULT NULL,
  `Reserve` varchar(29) DEFAULT NULL,
  PRIMARY KEY (`Concept_Type`,`Country_Code`,`Concept_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2sum_a`
--

DROP TABLE IF EXISTS `mf2sum_a`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2sum_a` (
  `Record_Type` varchar(3) NOT NULL,
  `Reserve_1` varchar(1) DEFAULT NULL,
  `Sequence_Number` int NOT NULL,
  `Reserve_2` varchar(1) DEFAULT NULL,
  `Comment_Marker` varchar(1) DEFAULT NULL,
  `Data_or_Comment` varchar(87) DEFAULT NULL,
  PRIMARY KEY (`Record_Type`,`Sequence_Number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2tcgpi_g`
--

DROP TABLE IF EXISTS `mf2tcgpi_g`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2tcgpi_g` (
  `TC_GPI_Key` varchar(14) NOT NULL,
  `Record_Type_Code` varchar(1) NOT NULL,
  `TC_GPI_Name` varchar(60) DEFAULT NULL,
  `TC_Level_Code` varchar(2) DEFAULT NULL,
  `Reserve` varchar(10) DEFAULT NULL,
  `Transaction_Code` varchar(1) DEFAULT NULL,
  `Last_Change_Date` bigint DEFAULT NULL,
  PRIMARY KEY (`TC_GPI_Key`,`Record_Type_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mf2val_d`
--

DROP TABLE IF EXISTS `mf2val_d`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mf2val_d` (
  `Field_Identifier` varchar(4) DEFAULT NULL,
  `Field_Value` varchar(15) DEFAULT NULL,
  `Language_Code` int DEFAULT NULL,
  `Value_Description` varchar(40) DEFAULT NULL,
  `Value_Abbreviation` varchar(15) DEFAULT NULL,
  `Reserve` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-21 20:00:29
