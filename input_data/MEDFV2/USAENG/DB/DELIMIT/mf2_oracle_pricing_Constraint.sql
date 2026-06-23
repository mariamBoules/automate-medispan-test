  
alter table mf2ndcm
 add (constraint mf2ndcm_pk primary key 
  (ndc_upc_hri
  ,modifier_code))
/

alter table mf2ndc
 add (constraint mf2ndc_pk primary key 
  (ndc_upc_hri))
/

alter table mf2lab
 add (constraint mf2lab_pk primary key 
  (medispan_labeler_id))
/

alter table mf2tcgpi
 add (constraint mf2tcgpi_pk primary key 
  (tcgpi_id
  ,record_type))
/

alter table mf2dict
 add (constraint mf2dict_pk primary key 
  (field_identifier))
/

alter table mf2sec
 add (constraint mf2sec_pk primary key 
  (external_drug_id
  ,external_drug_id_type_code
  ,alternate_drug_id))
/

alter table mf2prc
 add (constraint mf2prc_pk primary key 
  (ndc_upc_hri
  ,price_code
  ,price_effective_date))
/

alter table mf2mod
 add (constraint mf2mod_pk primary key 
  (modifier_code))
/

alter table mf2err
 add (constraint mf2err_pk primary key 
  (key_identifier
  ,data_element_code
  ,unique_key))
/

alter table mf2gppc
 add (constraint mf2gppc_pk primary key 
  (generic_product_pack_code))
/

alter table mf2name
 add (constraint mf2name_pk primary key 
  (drug_descriptor_id))
/

alter table mf2gpr
 add (constraint mf2gpr_pk primary key 
  (generic_product_pack_code
  ,gppc_price_code
  ,effective_date))
/


                


exit
/
