import numpy as np
import MySQLdb
from collections import Counter
import datetime

class PricingScore:
	def __init__(self): 
		self.scoreMax = 1.0
		self.budget = 'Minimum_Price'
		self.price = 'price'
		self.bhk = 'No_Of_Bedroom'
		self.locationName = 'locality_name'
		self.projectConfigNumber = "Project_Config_No"
		self.filterArray = [1]
		self.websiteLeadFactor = 0.33
		self.cherryPickPreFactor = 1.4
		self.cherryPickPostFactor = 1.5
		self.minPricingLead = 250
		self.posession = 'Possession'
		self.sixmonths = 190
		self.oneYear = 370
		self.twoYear = 900
		self.price_weight=0.7
		self.cost_weight=0.25
		self.CPLCostMax = 3000
		self.CPLCostMin = 250
		self.db=MySQLdb.connect(host="52.35.25.23" , port = 3306, user = "ITadmin",passwd = "ITadmin" ,db ="REDADMIN2")
		self.CPLdb=MySQLdb.connect(host="52.35.25.23" , port = 3306, user = "ITadmin",passwd = "ITadmin" ,db ="CPL")

 
	def cost_factor(self,relList):
		cursor=self.CPLdb.cursor()
		currDate = datetime.date.today()
		# print currDate
		prevMonth =  currDate - datetime.timedelta(days=90)
		query = "Select project_id,sum(cost),sum(lead_ad) from cost_output_july where date >= \""+ str(prevMonth) + "\" group by project_id"
		print query
# 		query = "Select Project_No from project_enquiry_requests Where Created_Dt >= \"" + str(prevMonth) +"\""
		cursor.execute(query)

		proj_cost=[]
		for rows in cursor.fetchall():
			proj_cost.append(rows)

		for project in relList:
			for row in proj_cost:
				if project==row[0]:
					x = (float(row[1])/(float(row[2])+1.0))
					x = x * self.cost_weight  + relList[project] * self.price_weight
					x = max(self.CPLCostMin,min(self.CPLCostMax,x))
					relList[project] = x
		return relList

	def pricingLeads(self,budget,location,BHK,possesion,propList):
		x = self.pricingRelScore(budget,location,BHK,possesion,propList)
		x = self.price1(x)
		returnDict = self.quality_factor(x)
		returnDict = self.cost_factor(returnDict)
		returnDict = self.getPrices(returnDict)
		return returnDict

	def getPrices(self,propList):
		for proj in propList:
			x = propList[proj]
			propList[proj] = [max(self.minPricingLead, int(self.websiteLeadFactor*x)) , max(self.minPricingLead,int(x)) ,max(self.minPricingLead,int(self.cherryPickPreFactor * x )), max(self.minPricingLead,int(self.cherryPickPostFactor * x ))]

		return propList

	def pricingRelScore(self,budget,location,BHK,possesion,propList):
		self.filterArray = [1]*(len(propList))
		pricingRelScoreArr = self.getBudgetScore(budget,propList)+self.getBHKScore(BHK,propList) +self.getPossessionScore(possesion,propList)
		
		# self.getPossessionScore	(possesion,propList)
		self.getLocationScore(location,propList)
		pricingRelScoreArr =  pricingRelScoreArr/3.0


		projectConfigNoList = map (lambda x:x[self.projectConfigNumber],propList)
		d = {}
		for i,projectConfigNo in enumerate(projectConfigNoList):
			# print projectConfigNo
			if(self.filterArray[i]==1):
				if(pricingRelScoreArr[i] > 6.5):
					d[projectConfigNo] = (pricingRelScoreArr[i] +3)/10.0
		return d

	def getPossessionScore (self,possesion,propList):
		possesionScorelist = []
		possesionScore = 0
		possesion = int(possesion)
		possesionList = map (lambda x:x[self.posession],propList)
		for i,poss in enumerate(possesionList):
			diff = int(poss) - possesion

			if(possesion == -1):
				possesionScorelist.append(10)
				continue
			if(possesion > self.twoYear ):
				if(poss > possesion ):
					possesionScore = 10
				else:
					possesionScore = self.getLineValueAll(self.twoYear,10,self.oneYear,1,poss)

				possesionScore = max(0,min(10,possesionScore))
				possesionScorelist.append(possesionScore)
				continue

			if(diff <=0 ):
				possesionScore = 10


			elif possesion <= self.sixmonths:
				if(diff > self.sixmonths):
					possesionScore = 0
				else:
					possesionScore = self.getLineValueAll(0,10,self.sixmonths,1,diff)

			else:
				if(diff > self.oneYear):
					possesionScore = 0
				else:
					possesionScore = self.getLineValueAll(0,10,self.oneYear,1,diff)

			possesionScore = max(0,min(10,possesionScore))
			possesionScorelist.append(possesionScore)
		possesionScorelist = np.array(possesionScorelist)
		return possesionScorelist
		


	def getBudgetScore(self,searchBudget,propList):
		budgetScore = 0
		propPriceList = map (lambda x:x[self.price],propList)
		budgetScoreList = []
		for i,propPrice in enumerate(propPriceList):
			if(propPrice > searchBudget*1.2 or propPrice < searchBudget*0.7):
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



	def price1(self,relList):
		cur=self.db.cursor()
		cur.execute("Select city_id,min_cpl,max_cpl,max_cpl_second,min_price_range,max_price_range,max_price_range_second from insta_lead_cpl ")
		cplPricingCity = []
		for row in cur.fetchall():
			cplPricingCity.append(row)

		cur=self.db.cursor()
		cur.execute("Select Project_No, Project_Config_No,Project_City, Minimum_Price,Maximum_Price from all_project_info")
		projectCityMap = []
		for row in cur.fetchall():
			projectCityMap.append(row)

		priceDict = {}
		for projectConfigNo in relList:
			for projectDetails in projectCityMap:
				if projectConfigNo == projectDetails[1]:
					projectNo = projectDetails[0]
					city = projectDetails[2]
					priceProject = (float(projectDetails[3])+float(projectDetails[4]))/2
					for row in cplPricingCity:
						if city == row[0]:
							min_cpl=float(row[1])
							max_cpl=float(row[2])
							max_cpl_second=float(row[3])
							min_price_range=float(row[4])
							max_price_range=float(row[5])
							max_price_range_second=float(row[6])
							priceProject = priceProject/100000 

							if (priceProject < min_price_range):
								cpl_amount_basic = min_cpl
							elif(priceProject<max_price_range):
								cpl_amount_basic= (max_cpl-min_cpl)/(max_price_range-min_price_range)*priceProject + min_cpl - (max_cpl-min_cpl)/(max_price_range-min_price_range)*min_price_range
							elif(priceProject<max_price_range_second):
								cpl_amount_basic=(max_cpl_second-max_cpl)/(max_price_range_second-max_price_range)*priceProject + max_cpl - (max_cpl_second-max_cpl)/(max_price_range_second-max_price_range)*max_price_range
							elif(priceProject > max_price_range_second):
								cpl_amount_basic = max_cpl_second

							break

					priceDict[projectNo] = relList[projectConfigNo]*cpl_amount_basic
					break
		return priceDict

	
	def quality_factor(self,priceDict):
		cur=self.db.cursor()
		currDate = datetime.date.today()
		# print currDate
		prevMonth =  currDate - datetime.timedelta(days=90)

		query = "Select Project_No from project_enquiry_requests Where Created_Dt >= \"" + str(prevMonth) +"\""
		# print query
		cur.execute(query)

		list_project_lead= []
		for row in cur.fetchall():
			list_project_lead.append(row[0])

		freq_project=Counter(list_project_lead)
		
		total=0.0
		for proj in priceDict:
			total+= freq_project[proj]
		for proj in priceDict:
			if total!=0:
				x = round(priceDict[proj]* (max(0.8,1.0-float(freq_project[proj])/total)),0) / 2
			else:
				x = (priceDict[proj]) / 2

			priceDict[proj] = int(x)
		return priceDict

if __name__ == '__main__':
	recoPropAttrList = 	[{'Possession': 594, 'Built_Up_Area': 680, 'Project_No': 2236, 'amenities': None, 'price': 6460000, 'Project_Config_No': 48213, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.827567000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.194291000000000'}, {'Possession': 198, 'Built_Up_Area': 700, 'Project_No': 6496, 'amenities': [u'Rain Water Harvesting', u'24 Hours Security', u'Lifts', u'Parking'], 'price': 6300000, 'Project_Config_No': 27985, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.813032868700000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.178373065700000'}, {'Possession': 594, 'Built_Up_Area': 868, 'Project_No': 11393, 'amenities': [u'Party Hall', u'24 Hours Power Backup', u"Children's Play Area", u'Club house', u'Garden', u'Gym', u'Indoor Games', u'Intercom'], 'price': 8549800, 'Project_Config_No': 41639, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.821083100000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.203794400000000'}, {'Possession': 15, 'Built_Up_Area': 719, 'Project_No': 1521, 'amenities': [u'Video Door Intercom', u'Swimming Pool', u'Parking', u'Park', u'Lifts', u'Landscape Garden', u'Gym', u'Club house', u"Children's Play Area", u'24 Hours Security'], 'price': 9311050, 'Project_Config_No': 36963, 'Project_City_Name': u'Mumbai', 'posessionDate': u'May 2016', 'Map_Longitude': u'72.818635000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.207123000000000'}, {'Possession': 229, 'Built_Up_Area': 485, 'Project_No': 6199, 'amenities': [u'Club house', u'Park'], 'price': 6402000, 'Project_Config_No': 37630, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.846489000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.156782000000000'}, {'Possession': 106, 'Built_Up_Area': 475, 'Project_No': 7727, 'amenities': [u'Fire Fighting Arrangements', u'Garden', u'Lifts', u'Parking', u'Rain Water Harvesting'], 'price': 6887500, 'Project_Config_No': 32466, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.839944000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.165087000000000'}, {'Possession': 594, 'Built_Up_Area': 720, 'Project_No': 4876, 'amenities': [u'Restaurant', u'Party Hall', u'Park', u'Library', u'Landscape Garden', u'Jogging Track', u'Indoor Games', u'Gym', u'Club house', u"Children's Play Area", u'Amphitheatre', u'Sauna', u'Swimming Pool', u'Tennis Court', u'Wifi Coverage', u'Yoga'], 'price': 7560000, 'Project_Config_No': 20336, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Contact Seller For Possession', 'Map_Longitude': u'72.827919000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.194557000000000'}, {'Possession': 226, 'Built_Up_Area': 645, 'Project_No': 12833, 'amenities': [u'24 Hours Power Backup', u'24 Hours Security', u"Children's Play Area", u'Lifts', u'Security System'], 'price': 9400000, 'Project_Config_No': 41989, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.832754686400000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.206685585500000'}, {'Possession': 594, 'Built_Up_Area': 775, 'Project_No': 20465, 'amenities': [u'24 Hours Power Backup', u'Fire Fighting Arrangements', u'Gas Line', u'Gym', u'Lifts', u'Security System'], 'price': 7962500, 'Project_Config_No': 54931, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.863927728800000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.184186000000000'}, {'Possession': 410, 'Built_Up_Area': 997, 'Project_No': 176, 'amenities': [u'Jogging Track', u'Lifts', u'Park', u'Podium Car Parking', u'Sauna', u'Security System', u'Swimming Pool', u'Tennis Court', u'Video Door Intercom', u'Gym', u'Cricketnet', u'Club house', u'24 Hours Security', u"Children's Play Area"], 'price': 11500000, 'Project_Config_No': 61529, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Jun 2017', 'Map_Longitude': u'72.822090000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.205676000000000'}, {'Possession': 349, 'Built_Up_Area': 725, 'Project_No': 6906, 'amenities': [u'24 Hours Security', u'Club house', u'Gym', u'Landscape Garden', u'Lifts', u'Parking'], 'price': 10000000, 'Project_Config_No': 37896, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Apr 2017', 'Map_Longitude': u'72.841774000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.182239000000000'}, {'Possession': 684, 'Built_Up_Area': 592, 'Project_No': 18154, 'amenities': [u'Indoor Games', u'Gym', u'Lifts', u'Garbage Disposable System', u"Children's Play Area", u'Outdoor Games', u'Parking', u'24 Hours Security'], 'price': 8033440, 'Project_Config_No': 56296, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2018', 'Map_Longitude': u'72.862601728800000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.182739733800000'}, {'Possession': 684, 'Built_Up_Area': 359, 'Project_No': 20291, 'amenities': [u'Gym', u'Intercom', u'Lifts', u'Park', u'Podium Car Parking', u'Swimming Pool', u'Wifi Coverage', u'24 Hours Power Backup', u'24 Hours Security', u'Club house'], 'price': 6856000, 'Project_Config_No': 53910, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2018', 'Map_Longitude': u'72.858999953400000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.186225066500000'}, {'Possession': 229, 'Built_Up_Area': 370, 'Project_No': 5692, 'amenities': [u'Earthquake Resistant', u'24 Hours Security', u'Fire Fighting Arrangements', u'Lifts', u'Rain Water Harvesting', u'Parking', u'Security System'], 'price': 7500000, 'Project_Config_No': 24519, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.839528904300000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.162141994500000'}, {'Possession': 199, 'Built_Up_Area': 650, 'Project_No': 8948, 'amenities': [u'24 Hours Security', u"Children's Play Area", u'Fire Fighting Arrangements', u'Gym', u'Intercom', u'Jogging Track', u'Lifts', u'Parking', u'Restaurant', u'Swimming Pool'], 'price': 10000000, 'Project_Config_No': 45531, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.836896058400000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.165833120900000'}, {'Possession': 684, 'Built_Up_Area': 275, 'Project_No': 16152, 'amenities': [u'24 Hours Power Backup', u'Club house', u'Fire Fighting Arrangements', u'Garden', u'Gym', u'Intercom', u'Lifts', u'Park', u'Parking', u'Swimming Pool', u'Vastu Compliant', u'Wifi Coverage'], 'price': 4757500, 'Project_Config_No': 53971, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2018', 'Map_Longitude': u'72.865197177900000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.181591333000000'}, {'Possession': 168, 'Built_Up_Area': 304, 'Project_No': 20290, 'amenities': [u'Park', u'Lifts', u'Intercom', u'Garden', u'Club house', u'24 Hours Security', u'24 Hours Power Backup', u'Parking', u'Rain Water Harvesting', u'Vastu Compliant', u'Wifi Coverage'], 'price': 5289600, 'Project_Config_No': 53973, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Oct 2016', 'Map_Longitude': u'72.865094728800000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.181282000000000'}, {'Possession': 106, 'Built_Up_Area': 680, 'Project_No': 17621, 'amenities': [u'Yoga', u'Tennis Court', u'Swimming Pool', u'Spa', u'Security System', u'Security Cabin', u'Landscape Garden', u'Lifts', u'Parking', u'Party Hall', u'Rain Water Harvesting', u'Basket Ball Court', u"Children's Play Area", u'Club house', u'Earthquake Resistant', u'Fire Fighting Arrangements', u'Gas Line', u'Gym', u'Indoor Games', u'Intercom'], 'price': 9520000, 'Project_Config_No': 54939, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Aug 2016', 'Map_Longitude': u'72.852954300000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon East', 'locality_name': u'Goregaon East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.170920300000000'}, {'Possession': 594, 'Built_Up_Area': 805, 'Project_No': 18505, 'amenities': [u"Children's Play Area", u'Garden', u'Gym', u'Lifts', u'Intercom', u'Parking', u'Rain Water Harvesting'], 'price': 11100000, 'Project_Config_No': 50716, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.858419000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Borivali East', 'locality_name': u'Borivali East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.220513000000000'}, {'Possession': 136, 'Built_Up_Area': 458, 'Project_No': 14993, 'amenities': [u'Swimming Pool', u'Rain Water Harvesting', u'24 Hours Security', u"Children's Play Area", u'Club house', u'Gym', u'Parking', u'Lifts', u'Landscape Garden', u'Intercom', u'Indoor Games', u'24 Hours Power Backup'], 'price': 10076000, 'Project_Config_No': 43669, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.839082100000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.182463800000000'}, {'Possession': 229, 'Built_Up_Area': 450, 'Project_No': 12022, 'amenities': [u'Indoor Games', u'24 Hours Power Backup', u"Children's Play Area", u'Garden'], 'price': 9000000, 'Project_Config_No': 43194, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.849569500000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Borivali West', 'locality_name': u'Borivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.222606100000000'}, {'Possession': 387, 'Built_Up_Area': 690, 'Project_No': 7115, 'amenities': [u'Security Cabin', u'Security System', u'Rain Water Harvesting', u'Lifts', u'Intercom', u'Gym', u'Fire Fighting Arrangements', u"Children's Play Area", u'24 Hours Security'], 'price': 9000000, 'Project_Config_No': 43293, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.869480000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon East', 'locality_name': u'Goregaon East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.177190400000000'}, {'Possession': 594, 'Built_Up_Area': 432, 'Project_No': 19616, 'amenities': [u'24 Hours Power Backup', u'24 Hours Security', u"Children's Play Area", u'Fire Fighting Arrangements', u'Garden', u'Gym', u'Intercom', u'Lifts', u'Parking', u'Security System', u'Wifi Coverage'], 'price': 10000000, 'Project_Config_No': 51682, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.845003093300000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.181821133200000'}, {'Possession': 45, 'Built_Up_Area': 650, 'Project_No': 6474, 'amenities': [u'Fire Fighting Arrangements', u'Gym', u'Jogging Track', u'Lifts', u'Park', u'Parking', u'Sewerage Treatment Plant', u'Rain Water Harvesting', u"Children's Play Area", u'Bicycle Track', u'24 Hours Security'], 'price': 6175000, 'Project_Config_No': 27754, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Jun 2016', 'Map_Longitude': u'72.871882000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.252242000000000'}, {'Possession': 46, 'Built_Up_Area': 551, 'Project_No': 974, 'amenities': [u'Senior Citizens Corner', u'Tennis Court', u"Children's Play Area", u'Park', u'Malls', u'Landscape Garden', u'Jogging Track', u'Gym', u'Club house', u'Swimming Pool'], 'price': 6000000, 'Project_Config_No': 2539, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Contact Seller For Possession', 'Map_Longitude': u'72.874261000000000', 'No_Of_Bedroom': 1.5, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.261703000000000'}, {'Possession': 1049, 'Built_Up_Area': 1070, 'Project_No': 11391, 'amenities': [u'Lifts', u'Rain Water Harvesting', u'Swimming Pool', u'24 Hours Power Backup', u'24 Hours Security', u'Amphitheatre', u"Children's Play Area", u'Club house', u'Garden', u'Gym'], 'price': 11235000, 'Project_Config_No': 46059, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2019', 'Map_Longitude': u'72.851372000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Borivali West', 'locality_name': u'Borivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.251331000000000'}, {'Possession': 137, 'Built_Up_Area': 900, 'Project_No': 1178, 'amenities': [u'Swimming Pool', u'24 Hours Security', u'Amphitheatre', u'Club house', u'Gym', u'Indoor Games', u'Library', u'Lifts', u'Park', u'Party Hall', u'Restaurant', u'Yoga', u'Temple', u'School'], 'price': 7470000, 'Project_Config_No': 33504, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.877657100000000', 'No_Of_Bedroom': 1.5, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.267367300000000'}, {'Possession': 229, 'Built_Up_Area': 850, 'Project_No': 18455, 'amenities': [u'Earthquake Resistant', u'Fire Fighting Arrangements', u'Lifts'], 'price': 6120000, 'Project_Config_No': 50174, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.874557000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.271596000000000'}, {'Possession': 76, 'Built_Up_Area': 650, 'Project_No': 17741, 'amenities': [u'Video Door Intercom', u'Security System', u'Solar Water Heating', u'Lifts', u'Earthquake Resistant', u'Gym', u'Intercom'], 'price': 4850000, 'Project_Config_No': 59864, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.885938775500000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.272170489000000'}, {'Possession': 76, 'Built_Up_Area': 600, 'Project_No': 17740, 'amenities': [u'Solar Water Heating'], 'price': 4100000, 'Project_Config_No': 59832, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.888870796300000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.272286681000000'}, {'Possession': 319, 'Built_Up_Area': 495, 'Project_No': 20015, 'amenities': [u'Earthquake Resistant', u'Intercom', u'Lifts', u'24 Hours Security'], 'price': 6200000, 'Project_Config_No': 53259, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2017', 'Map_Longitude': u'72.860194084700000', 'No_Of_Bedroom': 0.5, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.248849499900000'}, {'Possession': 594, 'Built_Up_Area': 810, 'Project_No': 6465, 'amenities': [u'Club house', u'Parking', u'Fire Fighting Arrangements', u'Gym', u'Jogging Track', u'Lifts', u'Park', u'Rain Water Harvesting', u'Swimming Pool', u"Children's Play Area", u'24 Hours Security'], 'price': 8800000, 'Project_Config_No': 27941, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.868317000000000', 'No_Of_Bedroom': 1.5, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.248323000000000'}, {'Possession': 46, 'Built_Up_Area': 650, 'Project_No': 2324, 'amenities': [u'Rain Water Harvesting', u'Intercom', u"Children's Play Area", u'Garden', u'Gym', u'24 Hours Security'], 'price': 4800000, 'Project_Config_No': 37789, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.881666000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.281667000000000'}, {'Possession': 140, 'Built_Up_Area': 935, 'Project_No': 6517, 'amenities': [u'Rain Water Harvesting', u'Parking', u'Lifts', u'Gym', u'Garden', u'24 Hours Security', u"Children's Play Area", u'Fire Fighting Arrangements'], 'price': 11500000, 'Project_Config_No': 27935, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.871844242900000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Borivali East', 'locality_name': u'Borivali East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.236363556200000'}, {'Possession': 15, 'Built_Up_Area': 700, 'Project_No': 2232, 'amenities': [u'Club house', u'Skating Rink', u'Squash Court', u'Swimming Pool', u'24 Hours Security', u'Badminton Court', u"Children's Play Area", u'Garden', u'Gym', u'Indoor Games', u'Intercom', u'Jogging Track', u'Lifts', u'Rain Water Harvesting', u'Park', u'Pool Table', u'Tennis Court', u'Wifi Coverage', u'Sewerage Treatment Plant'], 'price': 4900000, 'Project_Config_No': 20308, 'Project_City_Name': u'Mumbai', 'posessionDate': u'May 2016', 'Map_Longitude': u'72.881438200000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.283163800000000'}, {'Possession': 168, 'Built_Up_Area': 890, 'Project_No': 7111, 'amenities': [u'Party Hall', u'Vastu Compliant', u'Swimming Pool', u'Rain Water Harvesting', u'Park', u'Parking', u'Lifts', u'Intercom', u'Club house', u'Fire Fighting Arrangements', u'Gym', u'24 Hours Security', u"Children's Play Area"], 'price': 7500000, 'Project_Config_No': 46368, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Oct 2016', 'Map_Longitude': u'72.882871000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.281105000000000'}]
	p = PricingScore()

	print p.pricingLeads(6460000,['Malad'],0,90,recoPropAttrList)


"""
				priceDict[proj] = [max(self.minPricingLead, int(self.websiteLeadFactor*x)) , int(x) ,int(self.cherryPickPreFactor * x ), int(self.cherryPickPostFactor * x )]


"""
