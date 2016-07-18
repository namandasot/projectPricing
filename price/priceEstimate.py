import MySQLdb

class pricingEstimate:
    def __init__(self):
        self.websiteLeadFactor = 0.33
        self.minPricingLead = 250
        
    def getPriceEstimate(self,budget,city):
        budget = budget
        db=MySQLdb.connect(host="52.35.25.23" , port = 3306, user = "ITadmin",passwd = "ITadmin" ,db ="REDADMIN2")
        cur=db.cursor()
        cur.execute("Select city_id,min_cpl,max_cpl,max_cpl_second,min_price_range,max_price_range,max_price_range_second from insta_lead_cpl ")
        
        cplPricingCity = []
        for row in cur.fetchall():
            cplPricingCity.append(row)
        
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
        
        returnDict = {}
        returnDict["allWebsite"] = int(max(self.minPricingLead,cpl_amount_basic*self.websiteLeadFactor))
        returnDict["allTelephonic"] =  int(cpl_amount_basic)                    
        return returnDict
    
if __name__ == '__main__':
    p = pricingEstimate()
    print p.getPriceEstimate(8000000, 1)
    
    