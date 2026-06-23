 


create table mf2ndcm
 (ndc_upc_hri varchar(11) not null
 ,modifier_code varchar(6) not null
 ,reserve varchar(6) null
 ,transaction_code varchar(1) null
 ,last_change_date varchar(10) null
 )
go

create table mf2sum
 (record_type varchar(3) null
 ,reserve_1 varchar(1) null
 ,sequence_number integer null
 ,reserve_2 varchar(1) null
 ,comment_marker varchar(1) null
 ,data_comment varchar(87) null
 )
go

create table mf2ndc
 (ndc_upc_hri varchar(11) not null
 ,drug_descriptor_id integer null
 ,tee_code varchar(2) null
 ,dea_class_code varchar(1) null
 ,reserve3 varchar(1) null
 ,rx_otc_indicator_code varchar(1) null
 ,generic_product_pack_code varchar(8) null
 ,old_ndc_upc_hri varchar(11) null
 ,new_ndc_upc_hri varchar(11) null
 ,repackaged_code varchar(1) null
 ,id_number_format_code varchar(1) null
 ,third_party_restriction_code varchar(1) null
 ,kdc bigint null
 ,kdc_flag varchar(1) null
 ,medispan_labeler_id integer null
 ,multi_source_code varchar(1) null
 ,name_type_code varchar(1) null
 ,item_status_flag varchar(1) null
 ,innerpack_code varchar(1) null
 ,clinic_pack_code varchar(1) null
 ,reserve1 varchar(2) null
 ,ppg_indicator_code varchar(1) null
 ,hfpg_indicatory_code varchar(1) null
 ,dispensing_unit_code varchar(1) null
 ,dollar_rank_code varchar(1) null
 ,rx_rank_code varchar(1) null
 ,storage_condition_code varchar(1) null
 ,limited_distribution_coe varchar(2) null
 ,old_effective_date varchar(10) null
 ,new_effective_date varchar(10) null
 ,next_smaller_ndc_suffix varchar(2) null
 ,next_larger_ndc_suffix varchar(2) null
 ,reserve2 varchar(13) null
 ,transaction_code varchar(1) null
 ,last_change_date varchar(10) null
 )
go

create table mf2lab
 (medispan_labeler_id integer not null
 ,manufacturer_name varchar(30) null
 ,manufacturer_abbr_name varchar(10) null
 ,labeler_type_code varchar(1) null
 ,reserve varchar(9) null
 ,transaction_code varchar(1) null
 ,last_change_date varchar(10) null
 )
go

create table mf2tcgpi
 (tcgpi_id varchar(14) not null
 ,record_type varchar(1) not null
 ,tcgpi_name varchar(60) null
 ,tc_level_code varchar(2) null
 ,reserve varchar(10) null
 ,transaction_code varchar(1) null
 ,last_change_date varchar(10) null
 )
go

create table mf2copy
 (copyright_statement varchar(128) null
 )
go

create table mf2dict
 (field_identifier varchar(4) not null
 ,field_description varchar(35) null
 ,field_type varchar(1) null
 ,field_length integer null
 ,implied_decimal_flag varchar(1) null
 ,decimal_places integer null
 ,field_validation_flag varchar(1) null
 ,field_abbreviation_flag varchar(1) null
 ,reserve varchar(16) null
 )
go

create table mf2val
 (field_identifier varchar(4) null
 ,field_value varchar(15) null
 ,language_code integer null
 ,value_description varchar(40) null
 ,value_abbreviation varchar(15) null
 ,reserve varchar(20) null
 )
go

create table mf2sec
 (external_drug_id varchar(20) not null
 ,external_drug_id_type_code varchar(1) not null
 ,alternate_drug_id varchar(20) not null
 ,alternate_drug_id_fomat_code varchar(1) null
 ,transaction_code varchar(1) null
 ,reserve varchar(21) null
 )
go

create table mf2read
 (read_me_text varchar(80) null
 )
go

create table mf2prc
 (ndc_upc_hri varchar(11) not null
 ,price_code varchar(1) not null
 ,price_effective_date varchar(10) not null
 ,unit_price numeric(11,6) null
 ,extended_unit_price numeric(13,5) null
 ,package_price numeric(10,2) null
 ,awp_indicator_code varchar(1) null
 ,transaction_code varchar(1) null
 ,last_change_date varchar(10) null
 )
go

create table mf2mod
 (modifier_code varchar(6) not null
 ,modifier_description varchar(25) null
 ,reserve varchar(24) null
 ,transaction_code varchar(1) null
 ,last_change_date varchar(10) null
 )
go

create table mf2err
 (key_identifier varchar(1) not null
 ,unique_key varchar(19) not null
 ,data_element_code varchar(4) not null
 ,data_element_length integer default 3 null
 ,reserve varchar(5) null
 )
go

create table mf2gppc
 (generic_product_pack_code varchar(8) not null
 ,package_size numeric(9,3) null
 ,package_size_uom varchar(2) null
 ,package_quantity integer null
 ,unit_dose_unit_use_pkg_code varchar(1) null
 ,package_description_code varchar(2) null
 ,generic_product_identifier varchar(14) null
 ,reserve varchar(14) null
 ,transaction_code varchar(1) null
 ,last_change_date varchar(10) null
 )
go

create table mf2name
 (drug_descriptor_id integer not null
 ,drug_name varchar(30) null
 ,route_of_administration varchar(2) null
 ,dosage_form varchar(4) null
 ,strength varchar(15) null
 ,strength_unit_of_measure varchar(10) null
 ,bioequivalence_code varchar(1) null
 ,controlled_substance_code varchar(1) null
 ,reserve1 varchar(1) null
 ,legend_indicator_code varchar(1) null
 ,multi_source_code varchar(1) null
 ,brand_name_code varchar(1) null
 ,name_source_code varchar(1) null
 ,generic_product_identifier varchar(14) null
 ,kdc bigint null
 ,new_drug_descriptor_identifier integer null
 ,screenable_flag varchar(1) null
 ,kdc_flag varchar(1) null
 ,local_systemic_flag varchar(1) null
 ,maintenance_drug_code varchar(1) null
 ,form_type_code varchar(1) null
 ,internal_external_code varchar(1) null
 ,single_combination_code varchar(1) null
 ,representative_gpi_flag varchar(1) null
 ,representative_kdc_flag varchar(1) null
 ,reserve varchar(6) null
 ,transaction_code varchar(1) null
 ,last_change_date varchar(10) null
 )
go

create table mf2gpr
 (generic_product_pack_code varchar(8) not null
 ,gppc_price_code varchar(1) not null
 ,effective_date varchar(10) not null
 ,unit_price numeric(11,6) null
 ,reserve varchar(27) null
 ,transaction_code varchar(1) null
 ,last_change_date varchar(10) null
 )
go

