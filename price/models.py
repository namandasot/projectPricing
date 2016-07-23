from __future__ import unicode_literals

from django.db import models


class AllProjectInfo(models.Model):
    project_no = models.IntegerField(db_column='Project_No')  # Field name made lowercase.
    developer_id = models.IntegerField(db_column='Developer_id')  # Field name made lowercase.
    developer_acc_no = models.IntegerField(db_column='Developer_Acc_No')  # Field name made lowercase.
    developer_name = models.CharField(db_column='Developer_Name', max_length=255)  # Field name made lowercase.
    project_name = models.CharField(db_column='Project_Name', max_length=50)  # Field name made lowercase.
    developer_acc_name = models.CharField(db_column='Developer_Acc_Name', max_length=255)  # Field name made lowercase.
    project_logo_file = models.CharField(db_column='Project_logo_File', max_length=255)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255)  # Field name made lowercase.
    road = models.IntegerField(db_column='Road')  # Field name made lowercase.
    road_name = models.CharField(db_column='Road_Name', max_length=255)  # Field name made lowercase.
    project_city = models.IntegerField(db_column='Project_City')  # Field name made lowercase.
    project_city_name = models.CharField(db_column='Project_City_Name', max_length=50)  # Field name made lowercase.
    project_suburb = models.IntegerField(db_column='Project_Suburb')  # Field name made lowercase.
    project_suburb_name = models.CharField(db_column='Project_Suburb_Name', max_length=50)  # Field name made lowercase.
    project_area = models.IntegerField(db_column='Project_Area')  # Field name made lowercase.
    project_area_name = models.CharField(db_column='Project_Area_Name', max_length=50)  # Field name made lowercase.
    project_location = models.IntegerField(db_column='Project_Location')  # Field name made lowercase.
    project_location_name = models.CharField(db_column='Project_Location_Name', max_length=50)  # Field name made lowercase.
    pincode = models.CharField(db_column='Pincode', max_length=10)  # Field name made lowercase.
    project_status = models.CharField(db_column='Project_Status', max_length=50)  # Field name made lowercase.
    project_possession = models.DateField(db_column='Project_Possession')  # Field name made lowercase.
    listing_factor = models.DecimalField(db_column='Listing_Factor', max_digits=10, decimal_places=4)  # Field name made lowercase.
    realty_banner_flag = models.CharField(max_length=10)
    project_subscription = models.IntegerField(db_column='Project_Subscription')  # Field name made lowercase.
    display_price = models.CharField(db_column='Display_Price', max_length=3)  # Field name made lowercase.
    display_area = models.CharField(db_column='Display_Area', max_length=3)  # Field name made lowercase.
    display_possession = models.CharField(db_column='Display_Possession', max_length=5, blank=True, null=True)  # Field name made lowercase.
    display_under_construction = models.CharField(db_column='Display_Under_Construction', max_length=3)  # Field name made lowercase.
    map_latitude = models.FloatField(db_column='Map_Latitude')  # Field name made lowercase.
    hdfc_banner_flag = models.CharField(max_length=10)
    display_possession_month = models.CharField(max_length=3)
    hdfc_approved = models.CharField(db_column='HDFC_Approved', max_length=50)  # Field name made lowercase.
    sub_type = models.CharField(db_column='Sub_Type', max_length=50)  # Field name made lowercase.
    booking_start_dt = models.DateField(db_column='Booking_Start_Dt')  # Field name made lowercase.
    possession = models.DateField(db_column='Possession')  # Field name made lowercase.
    possession_text = models.CharField(db_column='Possession_Text', max_length=50, blank=True, null=True)  # Field name made lowercase.
    display_instahomeloan = models.CharField(max_length=3)
    neighbour_status = models.CharField(db_column='Neighbour_Status', max_length=3)  # Field name made lowercase.
    map_longitude = models.FloatField(db_column='Map_Longitude')  # Field name made lowercase.
    project_config_no = models.IntegerField(db_column='Project_Config_No', primary_key=True)  # Field name made lowercase.
    config_type = models.CharField(db_column='Config_Type', max_length=50)  # Field name made lowercase.
    carpet_area = models.IntegerField(db_column='Carpet_Area')  # Field name made lowercase.
    built_up_area = models.IntegerField(db_column='Built_Up_Area')  # Field name made lowercase.
    no_of_balconies = models.IntegerField(db_column='No_Of_Balconies')  # Field name made lowercase.
    configuration_name = models.CharField(db_column='Configuration_Name', max_length=50)  # Field name made lowercase.
    config_feature = models.CharField(max_length=50, blank=True, null=True)
    no_of_floors = models.IntegerField(db_column='No_Of_floors')  # Field name made lowercase.
    no_of_bedroom = models.CharField(db_column='No_Of_Bedroom', max_length=50)  # Field name made lowercase.
    no_of_bathroom = models.IntegerField(db_column='No_Of_Bathroom')  # Field name made lowercase.
    no_of_units_available = models.IntegerField(db_column='No_Of_Units_available')  # Field name made lowercase.
    floor_rise = models.IntegerField(db_column='Floor_Rise')  # Field name made lowercase.
    super_open_area = models.IntegerField(db_column='Super_open_area')  # Field name made lowercase.
    minimum_price = models.IntegerField(db_column='Minimum_Price')  # Field name made lowercase.
    maximum_price = models.IntegerField(db_column='Maximum_Price')  # Field name made lowercase.
    monthly_maintenance = models.FloatField(db_column='Monthly_Maintenance')  # Field name made lowercase.
    area_type = models.CharField(db_column='Area_Type', max_length=50)  # Field name made lowercase.
    area_value = models.CharField(db_column='Area_Value', max_length=15)  # Field name made lowercase.
    area_unit = models.CharField(db_column='Area_Unit', max_length=50)  # Field name made lowercase.
    base_price = models.IntegerField(db_column='Base_Price')  # Field name made lowercase.
    status_dt = models.DateField(db_column='Status_Dt')  # Field name made lowercase.
    project_image_file = models.CharField(db_column='Project_Image_File', max_length=500)  # Field name made lowercase.
    map_config = models.CharField(max_length=50)
    area_value_sort = models.FloatField(db_column='Area_Value_Sort')  # Field name made lowercase.
    video_walkthrough = models.CharField(db_column='Video_Walkthrough', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_views = models.IntegerField(db_column='Project_Views', blank=True, null=True)  # Field name made lowercase.
    store_views = models.IntegerField(db_column='Store_Views', blank=True, null=True)  # Field name made lowercase.
    hasstore = models.CharField(db_column='HasStore', max_length=10, blank=True, null=True)  # Field name made lowercase.
    possesiontext = models.CharField(db_column='PossesionText', max_length=10)  # Field name made lowercase.
    gallery_count = models.IntegerField(db_column='Gallery_Count')  # Field name made lowercase.
    hasdeal = models.CharField(db_column='HasDeal', max_length=10)  # Field name made lowercase.
    p_minprice = models.IntegerField(db_column='P_MinPrice')  # Field name made lowercase.
    p_maxprice = models.IntegerField(db_column='P_MaxPrice')  # Field name made lowercase.
    p_config_string = models.CharField(db_column='P_Config_String', max_length=50)  # Field name made lowercase.
    img_project_plan = models.CharField(db_column='Img_Project_Plan', max_length=2)  # Field name made lowercase.
    img_site_plan = models.CharField(db_column='Img_Site_Plan', max_length=2)  # Field name made lowercase.
    img_floor_plan = models.CharField(db_column='Img_Floor_Plan', max_length=2)  # Field name made lowercase.
    img_config_plan = models.CharField(db_column='Img_Config_Plan', max_length=2)  # Field name made lowercase.
    img_uc = models.CharField(db_column='Img_UC', max_length=2)  # Field name made lowercase.
    img_sample_flat = models.CharField(db_column='Img_Sample_Flat', max_length=2)  # Field name made lowercase.
    developer_logo_file = models.CharField(db_column='Developer_Logo_File', max_length=100)  # Field name made lowercase.
    price_change = models.CharField(db_column='Price_Change', max_length=50)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=15)  # Field name made lowercase.
    broker_developer_name = models.CharField(db_column='Broker_Developer_Name', max_length=60)  # Field name made lowercase.
    broker_developer_logo_file = models.CharField(db_column='Broker_Developer_Logo_File', max_length=100)  # Field name made lowercase.
    brochure_filename = models.CharField(db_column='Brochure_Filename', max_length=100)  # Field name made lowercase.
    emi = models.IntegerField(blank=True, null=True)
    srno = models.IntegerField(db_column='SrNo', blank=True, null=True)  # Field name made lowercase.
    priceperunit = models.CharField(db_column='PricePerUnit', max_length=45, blank=True, null=True)  # Field name made lowercase.
    project_description = models.CharField(max_length=500)
    project_remarks = models.TextField(db_column='Project_Remarks', blank=True, null=True)  # Field name made lowercase.
    amenity_code = models.CharField(max_length=250, blank=True, null=True)
    amenities = models.CharField(max_length=1000, blank=True, null=True)
    nearest_station_distance = models.IntegerField(blank=True, null=True)
    developer_overview = models.TextField(db_column='Developer_Overview', blank=True, null=True)  # Field name made lowercase.
    ppu_metric = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_project_info'
        
class ProjectEnquiryRequests(models.Model):
    project_enquiry_no = models.AutoField(db_column='Project_Enquiry_No', primary_key=True)  # Field name made lowercase.
    project_no = models.IntegerField(db_column='Project_No')  # Field name made lowercase.
    project_config_no = models.IntegerField(db_column='Project_Config_No')  # Field name made lowercase.
    ad_banner_id = models.IntegerField(db_column='Ad_Banner_Id', blank=True, null=True)  # Field name made lowercase.
    spotlight_id = models.IntegerField(db_column='Spotlight_Id', blank=True, null=True)  # Field name made lowercase.
    deal_id = models.IntegerField(db_column='Deal_Id', blank=True, null=True)  # Field name made lowercase.
    store_id = models.IntegerField(db_column='Store_Id', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=10)  # Field name made lowercase.
    city = models.IntegerField(db_column='City')  # Field name made lowercase.
    mobile_code = models.CharField(db_column='Mobile_Code', max_length=5)  # Field name made lowercase.
    mobile_no = models.CharField(db_column='Mobile_No', max_length=20)  # Field name made lowercase.
    mobile_verified_flag = models.CharField(db_column='Mobile_Verified_Flag', max_length=100)  # Field name made lowercase.
    ivr_order_id = models.CharField(db_column='IVR_order_id', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ivr_call_id = models.CharField(db_column='IVR_call_id', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tel_country_code = models.CharField(db_column='Tel_Country_Code', max_length=5)  # Field name made lowercase.
    tel_std_code = models.CharField(db_column='Tel_STD_Code', max_length=10)  # Field name made lowercase.
    tel_no = models.CharField(db_column='Tel_No', max_length=20)  # Field name made lowercase.
    email_id = models.CharField(db_column='Email_ID', max_length=100)  # Field name made lowercase.
    purchase_timeframe = models.CharField(db_column='Purchase_Timeframe', max_length=50, blank=True, null=True)  # Field name made lowercase.
    homeloan_amount = models.CharField(db_column='Homeloan_Amount', max_length=30)  # Field name made lowercase.
    user_question = models.TextField(db_column='User_Question', blank=True, null=True)  # Field name made lowercase.
    email_verified_flag = models.CharField(db_column='Email_Verified_Flag', max_length=100)  # Field name made lowercase.
    preferred_call_time = models.DateTimeField(db_column='Preferred_Call_Time')  # Field name made lowercase.
    promotional_offer_flag = models.CharField(db_column='Promotional_Offer_Flag', max_length=3)  # Field name made lowercase.
    terms_accepted_flag = models.CharField(db_column='Terms_Accepted_Flag', max_length=3)  # Field name made lowercase.
    created_by = models.CharField(db_column='Created_By', max_length=50)  # Field name made lowercase.
    created_dt = models.DateField(db_column='Created_Dt')  # Field name made lowercase.
    created_time = models.DateTimeField(db_column='Created_Time')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=13)  # Field name made lowercase.
    status_by = models.CharField(db_column='Status_By', max_length=50)  # Field name made lowercase.
    status_dt = models.DateField(db_column='Status_Dt')  # Field name made lowercase.
    referral_code = models.CharField(db_column='Referral_Code', max_length=400)  # Field name made lowercase.
    referral_code_media = models.CharField(db_column='Referral_Code_Media', max_length=100, blank=True, null=True)  # Field name made lowercase.
    referral_code_bid = models.CharField(db_column='Referral_Code_Bid', max_length=100, blank=True, null=True)  # Field name made lowercase.
    utm_refcode = models.CharField(db_column='UTM_Refcode', max_length=200, blank=True, null=True)  # Field name made lowercase.
    enquiry_type = models.CharField(db_column='Enquiry_Type', max_length=22, blank=True, null=True)  # Field name made lowercase.
    identified_property = models.CharField(db_column='Identified_Property', max_length=3)  # Field name made lowercase.
    other_country = models.CharField(max_length=50)
    other_city = models.CharField(max_length=50)
    lead_sended_flag = models.CharField(max_length=3)
    lead_sended_date = models.DateField()
    hdfc_bill_status = models.CharField(max_length=15)
    hdfc_bill_status_dt = models.DateField(blank=True, null=True)
    user_status = models.CharField(db_column='User_Status', max_length=50)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TimeStamp')  # Field name made lowercase.
    user_ip = models.CharField(db_column='User_IP', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dev_leads_sent = models.CharField(max_length=4, blank=True, null=True)
    realty_rb0_sent = models.DateField(blank=True, null=True)
    homeloan_wanted = models.CharField(max_length=5, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    allow_marketing = models.CharField(max_length=5, blank=True, null=True)
    package = models.CharField(max_length=30)
    lead_verification_status = models.CharField(db_column='Lead_Verification_Status', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lead_verification_date = models.DateField(db_column='Lead_Verification_Date', blank=True, null=True)  # Field name made lowercase.
    lead_followup_date = models.DateTimeField(db_column='Lead_Followup_Date', blank=True, null=True)  # Field name made lowercase.
    proj_lead_veri_status = models.CharField(db_column='Proj_Lead_Veri_Status', max_length=20)  # Field name made lowercase.
    proj_lead_veri_date = models.DateTimeField(db_column='Proj_Lead_Veri_Date')  # Field name made lowercase.
    proj_lead_veri_by = models.CharField(db_column='Proj_Lead_Veri_By', max_length=50)  # Field name made lowercase.
    guidance_needed = models.CharField(max_length=20)
    developer_called = models.DateField()

    class Meta:
        managed = False
        db_table = 'project_enquiry_requests'



class ProjectMaster(models.Model):
    project_no = models.AutoField(db_column='Project_No', primary_key=True)  # Field name made lowercase.
    developer_id = models.IntegerField(db_column='Developer_id', blank=True, null=True)  # Field name made lowercase.
    developer_name = models.CharField(db_column='Developer_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    brokers_developer_id = models.IntegerField(db_column='Brokers_Developer_id', blank=True, null=True)  # Field name made lowercase.
    brokers_developer_name = models.CharField(db_column='Brokers_Developer_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    developer_acc_no = models.IntegerField(db_column='Developer_Acc_No', blank=True, null=True)  # Field name made lowercase.
    developer_acc_name = models.CharField(db_column='Developer_Acc_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_name = models.CharField(db_column='Project_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    project_overview = models.TextField(db_column='Project_Overview', blank=True, null=True)  # Field name made lowercase.
    project_logo_file = models.CharField(db_column='Project_logo_File', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_image_file = models.CharField(db_column='Project_Image_File', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    road = models.CharField(db_column='Road', max_length=255, blank=True, null=True)  # Field name made lowercase.
    road_name = models.CharField(db_column='Road_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_city = models.IntegerField(db_column='Project_City', blank=True, null=True)  # Field name made lowercase.
    project_city_name = models.CharField(db_column='Project_City_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_suburb = models.IntegerField(db_column='Project_Suburb', blank=True, null=True)  # Field name made lowercase.
    project_suburb_name = models.CharField(db_column='Project_Suburb_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_area = models.IntegerField(db_column='Project_Area', blank=True, null=True)  # Field name made lowercase.
    project_area_name = models.CharField(db_column='Project_Area_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_location = models.IntegerField(db_column='Project_Location', blank=True, null=True)  # Field name made lowercase.
    project_location_name = models.CharField(db_column='Project_Location_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pincode = models.CharField(db_column='Pincode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    project_status = models.CharField(db_column='Project_Status', max_length=100, blank=True, null=True)  # Field name made lowercase.
    project_possession = models.DateField(db_column='Project_Possession', blank=True, null=True)  # Field name made lowercase.
    created_by = models.CharField(db_column='Created_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    created_dt = models.DateField(db_column='Created_Dt', blank=True, null=True)  # Field name made lowercase.
    service_by = models.CharField(db_column='Service_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    on_behalf_of = models.CharField(db_column='On_Behalf_Of', max_length=50, blank=True, null=True)  # Field name made lowercase.
    on_behalf_of_dt = models.DateField(db_column='On_Behalf_Of_Dt', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=22, blank=True, null=True)  # Field name made lowercase.
    status_by = models.CharField(db_column='Status_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status_dt = models.DateField(db_column='Status_Dt', blank=True, null=True)  # Field name made lowercase.
    sub_status = models.CharField(db_column='Sub_Status', max_length=50, blank=True, null=True)  # Field name made lowercase.
    display_project = models.CharField(db_column='Display_Project', max_length=20, blank=True, null=True)  # Field name made lowercase.
    approved_by = models.CharField(db_column='Approved_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    approved_dt = models.DateField(db_column='Approved_Dt', blank=True, null=True)  # Field name made lowercase.
    activated_by = models.CharField(db_column='Activated_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    activated_dt = models.DateField(db_column='Activated_Dt', blank=True, null=True)  # Field name made lowercase.
    inactivated_by = models.CharField(db_column='Inactivated_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inactivated_dt = models.DateField(db_column='Inactivated_Dt', blank=True, null=True)  # Field name made lowercase.
    inactivation_remarks = models.TextField(db_column='Inactivation_Remarks', blank=True, null=True)  # Field name made lowercase.
    no_of_hits = models.IntegerField(db_column='No_of_Hits', blank=True, null=True)  # Field name made lowercase.
    project_subscription = models.IntegerField(db_column='Project_Subscription', blank=True, null=True)  # Field name made lowercase.
    listing_type = models.IntegerField(db_column='Listing_Type', blank=True, null=True)  # Field name made lowercase.
    no_of_application = models.IntegerField(db_column='No_of_application', blank=True, null=True)  # Field name made lowercase.
    listing_factor = models.FloatField(db_column='Listing_Factor', blank=True, null=True)  # Field name made lowercase.
    no_of_application = models.IntegerField(db_column='No_of_application', blank=True, null=True)  # Field name made lowercase.
    listing_type = models.IntegerField(db_column='Listing_Type', blank=True, null=True)  # Field name made lowercase.
    no_of_application = models.IntegerField(db_column='No_of_application', blank=True, null=True)  # Field name made lowercase.
    listing_factor = models.FloatField(db_column='Listing_Factor', blank=True, null=True)  # Field name made lowercase.
    hdfc_approved = models.CharField(db_column='HDFC_Approved', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hdfc_approved_by = models.CharField(db_column='HDFC_Approved_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hdfc_approved_dt = models.DateField(db_column='HDFC_Approved_Dt', blank=True, null=True)  # Field name made lowercase.
    display_price = models.CharField(db_column='Display_Price', max_length=3)  # Field name made lowercase.
    display_area = models.CharField(db_column='Display_Area', max_length=50, blank=True, null=True)  # Field name made lowercase.
    display_possession = models.CharField(db_column='Display_Possession', max_length=5, blank=True, null=True)  # Field name made lowercase.
    liases_no = models.IntegerField(db_column='Liases_No', blank=True, null=True)  # Field name made lowercase.
    min_price = models.IntegerField(db_column='Min_Price', blank=True, null=True)  # Field name made lowercase.
    max_price = models.IntegerField(db_column='Max_Price', blank=True, null=True)  # Field name made lowercase.
    bdm_id = models.IntegerField(db_column='Bdm_Id', blank=True, null=True)  # Field name made lowercase.
    project_contact_name = models.CharField(db_column='Project_Contact_Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone_no = models.CharField(db_column='Phone_No', max_length=100, blank=True, null=True)  # Field name made lowercase.
    email_id = models.CharField(db_column='Email_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pan = models.CharField(max_length=15, blank=True, null=True)
    master_fileno = models.CharField(db_column='Master_FileNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hdfc_remarks = models.TextField(db_column='HDFC_Remarks', blank=True, null=True)  # Field name made lowercase.
    project_remarks = models.TextField(db_column='Project_Remarks', blank=True, null=True)  # Field name made lowercase.
    map_latitude = models.FloatField(db_column='Map_Latitude', blank=True, null=True)  # Field name made lowercase.
    map_longitude = models.FloatField(db_column='Map_Longitude', blank=True, null=True)  # Field name made lowercase.
    hdfc_banner_flag = models.CharField(max_length=10, blank=True, null=True)
    realty_banner_flag = models.CharField(max_length=10, blank=True, null=True)
    data_entered_by = models.CharField(db_column='Data_Entered_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    data_entered_dt = models.DateField(db_column='Data_Entered_Dt', blank=True, null=True)  # Field name made lowercase.
    data_entry_flag = models.CharField(db_column='Data_Entry_Flag', max_length=10, blank=True, null=True)  # Field name made lowercase.
    booking_start_dt = models.DateField(db_column='Booking_Start_Dt', blank=True, null=True)  # Field name made lowercase.
    display_possession_month = models.CharField(max_length=3)
    display_instahomeloan = models.CharField(max_length=50, blank=True, null=True)
    insta_banner_by = models.CharField(db_column='Insta_Banner_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    insta_banner_dt = models.DateField(db_column='Insta_Banner_Dt', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    category_by = models.CharField(db_column='Category_By', max_length=100, blank=True, null=True)  # Field name made lowercase.
    category_dt = models.DateField(db_column='Category_Dt', blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(max_length=3000, blank=True, null=True)
    reference_url = models.CharField(max_length=3000, blank=True, null=True)
    timestamp = models.DateTimeField()
    mobile_no = models.CharField(db_column='Mobile_No', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_source = models.CharField(db_column='Project_Source', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_source_link = models.CharField(db_column='Project_Source_Link', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gallery_imgs = models.TextField(blank=True, null=True)
    other_imgs = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_master'