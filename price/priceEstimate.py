import MySQLdb
import datetime
from collections import Counter
from _sqlite3 import Row
from price.models import *

class pricingEstimate:
    def __init__(self):
        self.websiteLeadFactor = float(1.0/3)
        self.minPricingLead = 250
        self.redAdminDB = "52.66.177.232"

        
    def quality_factor(self,projList,projectNum):
        cur=self.db.cursor()
        currDate = datetime.date.today()
        prevMonth =  currDate - datetime.timedelta(days=90)
        freq = ProjectEnquiryRequests.objects.filter(created_dt__gte = prevMonth).filter(project_no__in=projList).values_list('project_no',flat=True)
        freq_project=Counter(freq)    
        total = sum(freq_project.itervalues())
        if total > 0:
            return max(0.8,1-float(freq_project[projectNum])/total)
        return 1
        
    
    
    def getPriceEstimate(self,budget,projectNo):
        self.db = MySQLdb.connect(host=self.redAdminDB , port = 3306, user = "ITadmin",passwd = "ITadmin" ,db ="REDADMIN2")
        budget = budget
        cur=self.db.cursor()
        cur.execute("Select city_id,min_cpl,max_cpl,max_cpl_second,min_price_range,max_price_range,max_price_range_second from insta_lead_cpl ")
        
        cplPricingCity = []
        for row in cur.fetchall():
            cplPricingCity.append(row)
            
        cur=self.db.cursor()
        query = "Select Project_No,Project_City,Project_Area from project_master where Project_No="+str(projectNo)
        cur.execute(query)
        projectDetails = []
        for row in cur.fetchall():
            projectDetails.append(row)
        city = projectDetails[0][1]
        projectAreaCode = projectDetails[0][2]
        
        """
        For quality Score. 
        """
        
        sameAreaProj = list(AllProjectInfo.objects.filter(project_area=projectAreaCode).values_list('project_no',flat=True).distinct())        
        qualityFact = self.quality_factor(sameAreaProj,projectNo)


#         print cplPricingCity
        cpl_amount_basic = 1500
        
        for row in cplPricingCity:
            if city == row[0]:
                min_cpl=float(row[1])
                max_cpl=float(row[2])
                max_cpl_second=float(row[3])
                min_price_range=float(row[4])
                max_price_range=float(row[5])
                max_price_range_second=float(row[6])
                priceProject = budget/100000 

                if (priceProject < min_price_range):
                    cpl_amount_basic = min_cpl
                elif(priceProject<max_price_range):
                    cpl_amount_basic= (max_cpl-min_cpl)/(max_price_range-min_price_range)*priceProject + min_cpl - (max_cpl-min_cpl)/(max_price_range-min_price_range)*min_price_range
                elif(priceProject<max_price_range_second):
                    cpl_amount_basic=(max_cpl_second-max_cpl)/(max_price_range_second-max_price_range)*priceProject + max_cpl - (max_cpl_second-max_cpl)/(max_price_range_second-max_price_range)*max_price_range
                elif(priceProject > max_price_range_second):
                    cpl_amount_basic = max_cpl_second
        
        cpl_amount_basic = cpl_amount_basic/2
        cpl_amount_basic *= qualityFact
        returnDict = {}
        returnDict["allWebsite"] = int(max(self.minPricingLead,cpl_amount_basic*self.websiteLeadFactor))
        returnDict["allTelephonic"] =  int(cpl_amount_basic)  
        self.db.close()                  
        return returnDict
    
    
    
if __name__ == '__main__':
    p = pricingEstimate()
    print p.getPriceEstimate(8000000, 43)
    
    