
import numpy as np
import MySQLdb
from collections import Counter

class PricingScore:
	def __init__(self): 
		self.scoreMax = 1.0
		self.budget = 'Minimum_Price'
		self.price = 'price'
		self.bhk = 'No_Of_Bedroom'
		self.locationName = 'locality_name'
		self.projectNumber = "Project_No"
		self.filterArray = [1]



	def pricingLeads(self,budget,location,BHK,propList):
		x = self.pricingRelScore(budget,location,BHK,propList)
		y = self.quality_factor(x)
		z = self.price1(y)
		returnDict = {}
		for key,value in z.iteritems() :
			returnDict[key] = int(value[0]*value[1]*value[2])
		return returnDict

	def pricingRelScore(self,budget,location,BHK,propList):
		self.filterArray = [1]*(len(propList))
		pricingRelScoreArr = self.getBudgetScore(budget,propList)+self.getBHKScore(BHK,propList)
		self.getLocationScore(location,propList)
		pricingRelScoreArr =  pricingRelScoreArr/2.0

		projectNoList = map (lambda x:x[self.projectNumber],propList)
		d = {}
		for i,projectNo in enumerate(projectNoList):
			
			if(self.filterArray[i]==1):
				if(pricingRelScoreArr[i] > 7):
					d[projectNo] = [pricingRelScoreArr[i]/10.0]
		return d



	def getBudgetScore(self,searchBudget,propList):
		budgetScore = 0
		propPriceList = map (lambda x:x[self.price],propList)
		budgetScoreList = []
		for i,propPrice in enumerate(propPriceList):
			if(propPrice > searchBudget*1.2 or propPrice < searchBudget*0.8):
				self.filterArray[i] = 0
				budgetScoreList.append(0)
				continue
				
			if(searchBudget >= propPrice):
				budgetScore = self.getLineValueAll(searchBudget,10,searchBudget*0.4,2,propPrice)
			else:
				budgetScore = self.getLineValueAll(searchBudget,10,searchBudget*1.2,2,propPrice)
			budgetScore = min(budgetScore,10)
			budgetScore = max(budgetScore,0)

			budgetScoreList.append(budgetScore)
		budgetScoreList = np.array(budgetScoreList)
		return  budgetScoreList



	def getLocationScore(self,searchLocations,propList):
		locationScore = 0
		locationScoreList = []
		searchLocations = [i.lower() for i in searchLocations]
		propLocationList = map (lambda x:x[self.locationName],propList)
		for i,propLocation in enumerate(propLocationList) : 
			flag  = 0
			for x in searchLocations:
				if x in propLocation.lower():
					flag = 1
					locationScore =10
			if flag == 0:
				self.filterArray[i] = 0
				locationScore = 0

			locationScoreList.append(locationScore)
		locationScoreList = np.array(locationScoreList)
		return locationScoreList

	def getBHKScore(self,searchBHK,propList):
		bhkScore = 0 
		propBHKList = map (lambda x:x[self.bhk],propList)
		bhkScoreList = []
		for i,propBHK in enumerate(propBHKList) : 
			if(propBHK >= searchBHK ):
				bhkScore = 10

			else:
				self.filterArray[i] = 0
				bhkScore = 0

			bhkScoreList.append(bhkScore)


		bhkScoreList = np.array(bhkScoreList)
		return bhkScoreList


	def getLineValueAll(self,p1x,p1y,p2x,p2y,query):
		slope = float((p1y - p2y))/(p1x - p2x)
		constant = float(((p2y*p1x) - (p1y*p2x))) / (p1x - p2x)
		return ((slope * query) + constant)


	def price1(self,lst):
		db=MySQLdb.connect(host="52.35.25.23" , port = 3306, user = "ITadmin",passwd = "ITadmin" ,db ="REDADMIN2")
		cur=db.cursor()
		cur.execute("Select city_id,min_cpl,max_cpl,min_price_range,max_price_range from insta_lead_cpl ")
		cplPricing = []
		for row in cur.fetchall():
			cplPricing.append(row)

		cursor=db.cursor()
		cursor.execute("Select Project_No, Project_City,Minimum_Price,Maximum_Price from all_project_info")
		projectCityMap = []
		for rows in cursor.fetchall():
			projectCityMap.append(rows)

		for key in lst:
			for rows in projectCityMap:
				X = (float(rows[2])+float(rows[3]))/2
				if rows[0]==key:
					city=rows[1]
					for row in cplPricing:

						if city == row[0]:
							mincpl=row[1]
							maxcpl=row[2]
							min_price_range=row[3]
							max_price_range=row[4]
						#projectName = arr['Project_Name']
							min_price = row[3]#arr['Min_Price']
							max_price = row[4]#arr['Max_Price']
							X = X/100000 
							x1 = float(row[3])#arr['min_price_range']
							x2 = float(row[4])#arr['max_price_range']
							y1 = float(row[1])#arr['min_cpl']
							y2 = float(row[2])#arr['max_cpl']
							

							if(X < x1):
								Y = y1
							elif(X > x2):
								Y = y2
							else:
								Y= (y2-y1)/(x2-x1)*X + y1 - (y2-y1)/(x2-x1)*x1

							cpl_amount_basic = Y
			lst[key].append(cpl_amount_basic)
		return lst


	def quality_factor(self,lst):
	
		db=MySQLdb.connect(host="52.35.25.23" , port = 3306, user = "ITadmin",passwd = "ITadmin" ,db ="REDADMIN2")
		cur=db.cursor()
		cur.execute("Select Project_No from project_enquiry_requests Where Created_Dt >= '2016-06-01' ")

		list_project_lead= []
		for row in cur.fetchall():
			list_project_lead.append(row[0])

		freq_project=Counter(list_project_lead)
		
		proj_relevant=[]
		for key in lst:
			proj_relevant.append(key)
		total=0.0
		for proj in proj_relevant:
			total+= freq_project[proj]

		for proj in proj_relevant:
			lst[proj].append(max(0.5,round(1.0-float(freq_project[proj])/total,2)))

		return lst

if __name__ == '__main__':
	recoPropAttrList = 	[{'Possession': 594, 'Built_Up_Area': 680, 'Project_No': 2236, 'amenities': None, 'price': 6460000, 'Project_Config_No': 48213, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.827567000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.194291000000000'}, {'Possession': 198, 'Built_Up_Area': 700, 'Project_No': 6496, 'amenities': [u'Rain Water Harvesting', u'24 Hours Security', u'Lifts', u'Parking'], 'price': 6300000, 'Project_Config_No': 27985, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.813032868700000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.178373065700000'}, {'Possession': 594, 'Built_Up_Area': 868, 'Project_No': 11393, 'amenities': [u'Party Hall', u'24 Hours Power Backup', u"Children's Play Area", u'Club house', u'Garden', u'Gym', u'Indoor Games', u'Intercom'], 'price': 8549800, 'Project_Config_No': 41639, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.821083100000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.203794400000000'}, {'Possession': 15, 'Built_Up_Area': 719, 'Project_No': 1521, 'amenities': [u'Video Door Intercom', u'Swimming Pool', u'Parking', u'Park', u'Lifts', u'Landscape Garden', u'Gym', u'Club house', u"Children's Play Area", u'24 Hours Security'], 'price': 9311050, 'Project_Config_No': 36963, 'Project_City_Name': u'Mumbai', 'posessionDate': u'May 2016', 'Map_Longitude': u'72.818635000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.207123000000000'}, {'Possession': 229, 'Built_Up_Area': 485, 'Project_No': 6199, 'amenities': [u'Club house', u'Park'], 'price': 6402000, 'Project_Config_No': 37630, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.846489000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.156782000000000'}, {'Possession': 106, 'Built_Up_Area': 475, 'Project_No': 7727, 'amenities': [u'Fire Fighting Arrangements', u'Garden', u'Lifts', u'Parking', u'Rain Water Harvesting'], 'price': 6887500, 'Project_Config_No': 32466, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.839944000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.165087000000000'}, {'Possession': 594, 'Built_Up_Area': 720, 'Project_No': 4876, 'amenities': [u'Restaurant', u'Party Hall', u'Park', u'Library', u'Landscape Garden', u'Jogging Track', u'Indoor Games', u'Gym', u'Club house', u"Children's Play Area", u'Amphitheatre', u'Sauna', u'Swimming Pool', u'Tennis Court', u'Wifi Coverage', u'Yoga'], 'price': 7560000, 'Project_Config_No': 20336, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Contact Seller For Possession', 'Map_Longitude': u'72.827919000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.194557000000000'}, {'Possession': 226, 'Built_Up_Area': 645, 'Project_No': 12833, 'amenities': [u'24 Hours Power Backup', u'24 Hours Security', u"Children's Play Area", u'Lifts', u'Security System'], 'price': 9400000, 'Project_Config_No': 41989, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.832754686400000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.206685585500000'}, {'Possession': 594, 'Built_Up_Area': 775, 'Project_No': 20465, 'amenities': [u'24 Hours Power Backup', u'Fire Fighting Arrangements', u'Gas Line', u'Gym', u'Lifts', u'Security System'], 'price': 7962500, 'Project_Config_No': 54931, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.863927728800000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.184186000000000'}, {'Possession': 410, 'Built_Up_Area': 997, 'Project_No': 176, 'amenities': [u'Jogging Track', u'Lifts', u'Park', u'Podium Car Parking', u'Sauna', u'Security System', u'Swimming Pool', u'Tennis Court', u'Video Door Intercom', u'Gym', u'Cricketnet', u'Club house', u'24 Hours Security', u"Children's Play Area"], 'price': 11500000, 'Project_Config_No': 61529, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Jun 2017', 'Map_Longitude': u'72.822090000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.205676000000000'}, {'Possession': 349, 'Built_Up_Area': 725, 'Project_No': 6906, 'amenities': [u'24 Hours Security', u'Club house', u'Gym', u'Landscape Garden', u'Lifts', u'Parking'], 'price': 10000000, 'Project_Config_No': 37896, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Apr 2017', 'Map_Longitude': u'72.841774000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.182239000000000'}, {'Possession': 684, 'Built_Up_Area': 592, 'Project_No': 18154, 'amenities': [u'Indoor Games', u'Gym', u'Lifts', u'Garbage Disposable System', u"Children's Play Area", u'Outdoor Games', u'Parking', u'24 Hours Security'], 'price': 8033440, 'Project_Config_No': 56296, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2018', 'Map_Longitude': u'72.862601728800000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.182739733800000'}, {'Possession': 684, 'Built_Up_Area': 359, 'Project_No': 20291, 'amenities': [u'Gym', u'Intercom', u'Lifts', u'Park', u'Podium Car Parking', u'Swimming Pool', u'Wifi Coverage', u'24 Hours Power Backup', u'24 Hours Security', u'Club house'], 'price': 6856000, 'Project_Config_No': 53910, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2018', 'Map_Longitude': u'72.858999953400000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.186225066500000'}, {'Possession': 229, 'Built_Up_Area': 370, 'Project_No': 5692, 'amenities': [u'Earthquake Resistant', u'24 Hours Security', u'Fire Fighting Arrangements', u'Lifts', u'Rain Water Harvesting', u'Parking', u'Security System'], 'price': 7500000, 'Project_Config_No': 24519, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.839528904300000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.162141994500000'}, {'Possession': 199, 'Built_Up_Area': 650, 'Project_No': 8948, 'amenities': [u'24 Hours Security', u"Children's Play Area", u'Fire Fighting Arrangements', u'Gym', u'Intercom', u'Jogging Track', u'Lifts', u'Parking', u'Restaurant', u'Swimming Pool'], 'price': 10000000, 'Project_Config_No': 45531, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.836896058400000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.165833120900000'}, {'Possession': 684, 'Built_Up_Area': 275, 'Project_No': 16152, 'amenities': [u'24 Hours Power Backup', u'Club house', u'Fire Fighting Arrangements', u'Garden', u'Gym', u'Intercom', u'Lifts', u'Park', u'Parking', u'Swimming Pool', u'Vastu Compliant', u'Wifi Coverage'], 'price': 4757500, 'Project_Config_No': 53971, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2018', 'Map_Longitude': u'72.865197177900000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.181591333000000'}, {'Possession': 168, 'Built_Up_Area': 304, 'Project_No': 20290, 'amenities': [u'Park', u'Lifts', u'Intercom', u'Garden', u'Club house', u'24 Hours Security', u'24 Hours Power Backup', u'Parking', u'Rain Water Harvesting', u'Vastu Compliant', u'Wifi Coverage'], 'price': 5289600, 'Project_Config_No': 53973, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Oct 2016', 'Map_Longitude': u'72.865094728800000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.181282000000000'}, {'Possession': 106, 'Built_Up_Area': 680, 'Project_No': 17621, 'amenities': [u'Yoga', u'Tennis Court', u'Swimming Pool', u'Spa', u'Security System', u'Security Cabin', u'Landscape Garden', u'Lifts', u'Parking', u'Party Hall', u'Rain Water Harvesting', u'Basket Ball Court', u"Children's Play Area", u'Club house', u'Earthquake Resistant', u'Fire Fighting Arrangements', u'Gas Line', u'Gym', u'Indoor Games', u'Intercom'], 'price': 9520000, 'Project_Config_No': 54939, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Aug 2016', 'Map_Longitude': u'72.852954300000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon East', 'locality_name': u'Goregaon East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.170920300000000'}, {'Possession': 594, 'Built_Up_Area': 805, 'Project_No': 18505, 'amenities': [u"Children's Play Area", u'Garden', u'Gym', u'Lifts', u'Intercom', u'Parking', u'Rain Water Harvesting'], 'price': 11100000, 'Project_Config_No': 50716, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.858419000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Borivali East', 'locality_name': u'Borivali East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.220513000000000'}, {'Possession': 136, 'Built_Up_Area': 458, 'Project_No': 14993, 'amenities': [u'Swimming Pool', u'Rain Water Harvesting', u'24 Hours Security', u"Children's Play Area", u'Club house', u'Gym', u'Parking', u'Lifts', u'Landscape Garden', u'Intercom', u'Indoor Games', u'24 Hours Power Backup'], 'price': 10076000, 'Project_Config_No': 43669, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.839082100000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.182463800000000'}, {'Possession': 229, 'Built_Up_Area': 450, 'Project_No': 12022, 'amenities': [u'Indoor Games', u'24 Hours Power Backup', u"Children's Play Area", u'Garden'], 'price': 9000000, 'Project_Config_No': 43194, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.849569500000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Borivali West', 'locality_name': u'Borivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.222606100000000'}, {'Possession': 387, 'Built_Up_Area': 690, 'Project_No': 7115, 'amenities': [u'Security Cabin', u'Security System', u'Rain Water Harvesting', u'Lifts', u'Intercom', u'Gym', u'Fire Fighting Arrangements', u"Children's Play Area", u'24 Hours Security'], 'price': 9000000, 'Project_Config_No': 43293, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.869480000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon East', 'locality_name': u'Goregaon East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.177190400000000'}, {'Possession': 594, 'Built_Up_Area': 432, 'Project_No': 19616, 'amenities': [u'24 Hours Power Backup', u'24 Hours Security', u"Children's Play Area", u'Fire Fighting Arrangements', u'Garden', u'Gym', u'Intercom', u'Lifts', u'Parking', u'Security System', u'Wifi Coverage'], 'price': 10000000, 'Project_Config_No': 51682, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.845003093300000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.181821133200000'}, {'Possession': 45, 'Built_Up_Area': 650, 'Project_No': 6474, 'amenities': [u'Fire Fighting Arrangements', u'Gym', u'Jogging Track', u'Lifts', u'Park', u'Parking', u'Sewerage Treatment Plant', u'Rain Water Harvesting', u"Children's Play Area", u'Bicycle Track', u'24 Hours Security'], 'price': 6175000, 'Project_Config_No': 27754, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Jun 2016', 'Map_Longitude': u'72.871882000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.252242000000000'}, {'Possession': 46, 'Built_Up_Area': 551, 'Project_No': 974, 'amenities': [u'Senior Citizens Corner', u'Tennis Court', u"Children's Play Area", u'Park', u'Malls', u'Landscape Garden', u'Jogging Track', u'Gym', u'Club house', u'Swimming Pool'], 'price': 6000000, 'Project_Config_No': 2539, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Contact Seller For Possession', 'Map_Longitude': u'72.874261000000000', 'No_Of_Bedroom': 1.5, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.261703000000000'}, {'Possession': 1049, 'Built_Up_Area': 1070, 'Project_No': 11391, 'amenities': [u'Lifts', u'Rain Water Harvesting', u'Swimming Pool', u'24 Hours Power Backup', u'24 Hours Security', u'Amphitheatre', u"Children's Play Area", u'Club house', u'Garden', u'Gym'], 'price': 11235000, 'Project_Config_No': 46059, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2019', 'Map_Longitude': u'72.851372000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Borivali West', 'locality_name': u'Borivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.251331000000000'}, {'Possession': 137, 'Built_Up_Area': 900, 'Project_No': 1178, 'amenities': [u'Swimming Pool', u'24 Hours Security', u'Amphitheatre', u'Club house', u'Gym', u'Indoor Games', u'Library', u'Lifts', u'Park', u'Party Hall', u'Restaurant', u'Yoga', u'Temple', u'School'], 'price': 7470000, 'Project_Config_No': 33504, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.877657100000000', 'No_Of_Bedroom': 1.5, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.267367300000000'}, {'Possession': 229, 'Built_Up_Area': 850, 'Project_No': 18455, 'amenities': [u'Earthquake Resistant', u'Fire Fighting Arrangements', u'Lifts'], 'price': 6120000, 'Project_Config_No': 50174, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.874557000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.271596000000000'}, {'Possession': 76, 'Built_Up_Area': 650, 'Project_No': 17741, 'amenities': [u'Video Door Intercom', u'Security System', u'Solar Water Heating', u'Lifts', u'Earthquake Resistant', u'Gym', u'Intercom'], 'price': 4850000, 'Project_Config_No': 59864, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.885938775500000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.272170489000000'}, {'Possession': 76, 'Built_Up_Area': 600, 'Project_No': 17740, 'amenities': [u'Solar Water Heating'], 'price': 4100000, 'Project_Config_No': 59832, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.888870796300000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.272286681000000'}, {'Possession': 319, 'Built_Up_Area': 495, 'Project_No': 20015, 'amenities': [u'Earthquake Resistant', u'Intercom', u'Lifts', u'24 Hours Security'], 'price': 6200000, 'Project_Config_No': 53259, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2017', 'Map_Longitude': u'72.860194084700000', 'No_Of_Bedroom': 0.5, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.248849499900000'}, {'Possession': 594, 'Built_Up_Area': 810, 'Project_No': 6465, 'amenities': [u'Club house', u'Parking', u'Fire Fighting Arrangements', u'Gym', u'Jogging Track', u'Lifts', u'Park', u'Rain Water Harvesting', u'Swimming Pool', u"Children's Play Area", u'24 Hours Security'], 'price': 8800000, 'Project_Config_No': 27941, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.868317000000000', 'No_Of_Bedroom': 1.5, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.248323000000000'}, {'Possession': 46, 'Built_Up_Area': 650, 'Project_No': 2324, 'amenities': [u'Rain Water Harvesting', u'Intercom', u"Children's Play Area", u'Garden', u'Gym', u'24 Hours Security'], 'price': 4800000, 'Project_Config_No': 37789, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.881666000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.281667000000000'}, {'Possession': 140, 'Built_Up_Area': 935, 'Project_No': 6517, 'amenities': [u'Rain Water Harvesting', u'Parking', u'Lifts', u'Gym', u'Garden', u'24 Hours Security', u"Children's Play Area", u'Fire Fighting Arrangements'], 'price': 11500000, 'Project_Config_No': 27935, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.871844242900000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Borivali East', 'locality_name': u'Borivali East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.236363556200000'}, {'Possession': 15, 'Built_Up_Area': 700, 'Project_No': 2232, 'amenities': [u'Club house', u'Skating Rink', u'Squash Court', u'Swimming Pool', u'24 Hours Security', u'Badminton Court', u"Children's Play Area", u'Garden', u'Gym', u'Indoor Games', u'Intercom', u'Jogging Track', u'Lifts', u'Rain Water Harvesting', u'Park', u'Pool Table', u'Tennis Court', u'Wifi Coverage', u'Sewerage Treatment Plant'], 'price': 4900000, 'Project_Config_No': 20308, 'Project_City_Name': u'Mumbai', 'posessionDate': u'May 2016', 'Map_Longitude': u'72.881438200000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.283163800000000'}, {'Possession': 168, 'Built_Up_Area': 890, 'Project_No': 7111, 'amenities': [u'Party Hall', u'Vastu Compliant', u'Swimming Pool', u'Rain Water Harvesting', u'Park', u'Parking', u'Lifts', u'Intercom', u'Club house', u'Fire Fighting Arrangements', u'Gym', u'24 Hours Security', u"Children's Play Area"], 'price': 7500000, 'Project_Config_No': 46368, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Oct 2016', 'Map_Longitude': u'72.882871000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.281105000000000'}]
	p = PricingScore()

	p.pricingLeads(6460000,['Malad'],0,recoPropAttrList)


