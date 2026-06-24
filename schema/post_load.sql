DROP TABLE IF EXISTS medispan_ndc_mapping;
CREATE TABLE `medispan_ndc_mapping` (
  `NDC_UPC_HRI` varchar(11) NOT NULL,
  `NDC_10` varchar(10) NOT NULL,
  PRIMARY KEY (`NDC_UPC_HRI`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `medispan_ndc_mapping` ADD INDEX `medispan_ndc_10` USING BTREE (`NDC_10` ASC);
ALTER TABLE `medispan_ndc_mapping` ADD INDEX `medispan_NDC_UPC_HRI` USING BTREE (`NDC_UPC_HRI` ASC);
ALTER TABLE `mf2prc_m` ADD INDEX `mf2prc_m_Price_Code_idx` USING BTREE (`Price_Code` ASC);

INSERT INTO medispan_ndc_mapping (NDC_UPC_HRI, NDC_10)
SELECT NDC_UPC_HRI,
CASE
WHEN ID_Number_Format_Code = 1 THEN SUBSTRING(NDC_UPC_HRI,2,10)
WHEN ID_Number_Format_Code = 2 THEN CONCAT(SUBSTRING(NDC_UPC_HRI,1,5), SUBSTRING(NDC_UPC_HRI,7,5))
WHEN ID_Number_Format_Code = 3 THEN CONCAT(SUBSTRING(NDC_UPC_HRI,1,9), SUBSTRING(NDC_UPC_HRI,11,1))
END AS NDC_10
FROM mf2ndc_h
WHERE ID_Number_Format_Code IN (1, 2, 3);
