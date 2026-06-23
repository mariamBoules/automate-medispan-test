 


create table mf2ndcm
 (ndc_upc_hri varchar2(11) not null
 ,modifier_code varchar2(6) not null
 ,reserve varchar2(6) null
 ,transaction_code varchar2(1) null
 ,last_change_date varchar2(10) null
 )
/

create table mf2sum
 (record_type varchar2(3) null
 ,reserve_1 varchar2(1) null
 ,sequence_number number(3) null
 ,reserve_2 varchar2(1) null
 ,comment_marker varchar2(1) null
 ,data_comment varchar2(87) null
 )
/

create table mf2ndc
 (ndc_upc_hri varchar2(11) not null
 ,drug_descriptor_id number(6) null
 ,tee_code varchar2(2) null
 ,dea_class_code varchar2(1) null
 ,reserve3 varchar2(1) null
 ,rx_otc_indicator_code varchar2(1) null
 ,generic_product_pack_code varchar2(8) null
 ,old_ndc_upc_hri varchar2(11) null
 ,new_ndc_upc_hri varchar2(11) null
 ,repackaged_code varchar2(1) null
 ,id_number_format_code varchar2(1) null
 ,third_party_restriction_code varchar2(1) null
 ,kdc number(10) null
 ,kdc_flag varchar2(1) null
 ,medispan_labeler_id number(5) null
 ,multi_source_code varchar2(1) null
 ,name_type_code varchar2(1) null
 ,item_status_flag varchar2(1) null
 ,innerpack_code varchar2(1) null
 ,clinic_pack_code varchar2(1) null
 ,reserve1 varchar2(2) null
 ,ppg_indicator_code varchar2(1) null
 ,hfpg_indicatory_code varchar2(1) null
 ,dispensing_unit_code varchar2(1) null
 ,dollar_rank_code varchar2(1) null
 ,rx_rank_code varchar2(1) null
 ,storage_condition_code varchar2(1) null
 ,limited_distribution_coe varchar2(2) null
 ,old_effective_date varchar2(10) null
 ,new_effective_date varchar2(10) null
 ,next_smaller_ndc_suffix varchar2(2) null
 ,next_larger_ndc_suffix varchar2(2) null
 ,reserve2 varchar2(13) null
 ,transaction_code varchar2(1) null
 ,last_change_date varchar2(10) null
 )
/

create table mf2lab
 (medispan_labeler_id number(5) not null
 ,manufacturer_name varchar2(30) null
 ,manufacturer_abbr_name varchar2(10) null
 ,labeler_type_code varchar2(1) null
 ,reserve varchar2(9) null
 ,transaction_code varchar2(1) null
 ,last_change_date varchar2(10) null
 )
/

create table mf2tcgpi
 (tcgpi_id varchar2(14) not null
 ,record_type varchar2(1) not null
 ,tcgpi_name varchar2(60) null
 ,tc_level_code varchar2(2) null
 ,reserve varchar2(10) null
 ,transaction_code varchar2(1) null
 ,last_change_date varchar2(10) null
 )
/

create table mf2copy
 (copyright_statement varchar2(128) null
 )
/

create table mf2dict
 (field_identifier varchar2(4) not null
 ,field_description varchar2(35) null
 ,field_type varchar2(1) null
 ,field_length number(3) null
 ,implied_decimal_flag varchar2(1) null
 ,decimal_places number(2) null
 ,field_validation_flag varchar2(1) null
 ,field_abbreviation_flag varchar2(1) null
 ,reserve varchar2(16) null
 )
/

create table mf2val
 (field_identifier varchar2(4) null
 ,field_value varchar2(15) null
 ,language_code number(2) null
 ,value_description varchar2(40) null
 ,value_abbreviation varchar2(15) null
 ,reserve varchar2(20) null
 )
/

create table mf2sec
 (external_drug_id varchar2(20) not null
 ,external_drug_id_type_code varchar2(1) not null
 ,alternate_drug_id varchar2(20) not null
 ,alternate_drug_id_fomat_code varchar2(1) null
 ,transaction_code varchar2(1) null
 ,reserve varchar2(21) null
 )
/

create table mf2read
 (read_me_text varchar2(80) null
 )
/

create table mf2prc
 (ndc_upc_hri varchar2(11) not null
 ,price_code varchar2(1) not null
 ,price_effective_date varchar2(10) not null
 ,unit_price number(11,6) null
 ,extended_unit_price number(13,5) null
 ,package_price number(10,2) null
 ,awp_indicator_code varchar2(1) null
 ,transaction_code varchar2(1) null
 ,last_change_date varchar2(10) null
 )
/

create table mf2mod
 (modifier_code varchar2(6) not null
 ,modifier_description varchar2(25) null
 ,reserve varchar2(24) null
 ,transaction_code varchar2(1) null
 ,last_change_date varchar2(10) null
 )
/

create table mf2err
 (key_identifier varchar2(1) not null
 ,unique_key varchar2(19) not null
 ,data_element_code varchar2(4) not null
 ,data_element_length number(3) default 3 null
 ,reserve varchar2(5) null
 )
/

create table mf2gppc
 (generic_product_pack_code varchar2(8) not null
 ,package_size number(9,3) null
 ,package_size_uom varchar2(2) null
 ,package_quantity number(5) null
 ,unit_dose_unit_use_pkg_code varchar2(1) null
 ,package_description_code varchar2(2) null
 ,generic_product_identifier varchar2(14) null
 ,reserve varchar2(14) null
 ,transaction_code varchar2(1) null
 ,last_change_date varchar2(10) null
 )
/

create table mf2name
 (drug_descriptor_id number(6) not null
 ,drug_name varchar2(30) null
 ,route_of_administration varchar2(2) null
 ,dosage_form varchar2(4) null
 ,strength varchar2(15) null
 ,strength_unit_of_measure varchar2(10) null
 ,bioequivalence_code varchar2(1) null
 ,controlled_substance_code varchar2(1) null
 ,reserve1 varchar2(1) null
 ,legend_indicator_code varchar2(1) null
 ,multi_source_code varchar2(1) null
 ,brand_name_code varchar2(1) null
 ,name_source_code varchar2(1) null
 ,generic_product_identifier varchar2(14) null
 ,kdc number(10) null
 ,new_drug_descriptor_identifier number(6) null
 ,screenable_flag varchar2(1) null
 ,kdc_flag varchar2(1) null
 ,local_systemic_flag varchar2(1) null
 ,maintenance_drug_code varchar2(1) null
 ,form_type_code varchar2(1) null
 ,internal_external_code varchar2(1) null
 ,single_combination_code varchar2(1) null
 ,representative_gpi_flag varchar2(1) null
 ,representative_kdc_flag varchar2(1) null
 ,reserve varchar2(6) null
 ,transaction_code varchar2(1) null
 ,last_change_date varchar2(10) null
 )
/

create table mf2gpr
 (generic_product_pack_code varchar2(8) not null
 ,gppc_price_code varchar2(1) not null
 ,effective_date varchar2(10) not null
 ,unit_price number(11,6) null
 ,reserve varchar2(27) null
 ,transaction_code varchar2(1) null
 ,last_change_date varchar2(10) null
 )
/

exit
/
