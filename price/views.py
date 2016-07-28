from django.shortcuts import render
from rest_framework.response import Response
from models import AllProjectInfo
from serializers import AllProjectInfoSerializer
from datetime import datetime as dtime
import datetime
from pricingRel import PricingScore
from priceEstimate import pricingEstimate
from cityPriceEstimate import cityPricingEstimate

# Create your views here.

pricingScore = PricingScore()

class Location:  

    def getLocationName(self,locationId):
        data= AllProjectInfo.objects.filter(project_area__in=locationId).values_list('project_area_name',flat=True).distinct()
        print data
        return data
        
    def getCityName(self,locationId):
        return AllProjectInfo.objects.filter(project_area=locationId).values('project_city_name').distinct()[0]['project_city_name']
    
location = Location()

def getPossessionDays(possessionDate):
    try:
        d1 = dtime.strptime(possessionDate, "%Y-%m-%d")
    except:
        return 0
    d2 = dtime.strptime(str(datetime.date.today()), "%Y-%m-%d")
    days = (d1 - d2).days
    if days<0:
        return 0
    else:
        return days

def getAllProjectInfo(cityName,locationId):
    allData = list(AllProjectInfo.objects.filter(project_area__in=locationId))
    print len(allData)
    
    allProperties = []
    for propert in allData:
        if propert.no_of_bedroom=='':
            propert.no_of_bedroom=-1
        propDict = AllProjectInfoSerializer(propert).data
        propDict['No_Of_Bedroom'] = float(str(propDict['No_Of_Bedroom']))
#         print propDict['No_Of_Bedroom']
        propDict['Possession'] = getPossessionDays(propDict['Possession'])
        propDict['locality_name'] = propDict['Project_Area_Name'] +', '+ propDict['Project_Suburb_Name'] +', ' +propDict['Project_City_Name']
        if propDict['amenities']:
            propDict['amenities']=propDict['amenities'][1:-1].split(',')
        else:
            propDict['amenities']=None
        allProperties.append(propDict)
    return allProperties

from rest_framework.decorators import api_view

@api_view(['GET'])
def price(request):
    locations = request.GET.get('location',None)
    budget = request.GET.get('budget',5000000)
    bhk = request.GET.get('bhk',-1)
    possession = request.GET.get('possession',-1)
    cityName = ''
    locationName = []


    locationList = locations.split(',')
    cityName = location.getCityName(locationList[0])
#         for locationId in locationList:
    locationName = location.getLocationName(locationList)
#             if len(tempLoc)>0:
#                 locationName.append(tempLoc[0])
    allProjectInfo = getAllProjectInfo(cityName,locationList)
    print len(allProjectInfo)
    result = pricingScore.pricingLeads(int(budget),locationName,float(bhk),possession,allProjectInfo)

#     dummyResult = {'544':'250','545':'300','546':'350'}
    return Response(result)

pEstimate = pricingEstimate()
cpEstimate = cityPricingEstimate()


@api_view(['GET'])
def estimate(request):
    budget= int(request.GET.get('budget',None))
    project = int(request.GET.get('project',None))
    result = pEstimate.getPriceEstimate(budget, project)
    return Response(result)


@api_view(['GET'])
def cityEstimator(request):
    budget= int(request.GET.get('budget',None))
    city = int(request.GET.get('city',None))
    result = cpEstimate.getPriceEstimate(budget, city)
    return Response(result)
    
