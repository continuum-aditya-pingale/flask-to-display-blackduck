import argparse
#import csv
from dateutil import parser as dt_parser
#import json
#import pprint
#from blackduck.HubRestApi import HubInstance
import argparse
import json
import logging
import sys
import pprint
from blackduck.HubRestApi import HubInstance
from pymongo import MongoClient
import schedule
import time 

def test():
    result=[]
    '''
    project_name_list=[]
    project_name_example="dev_platform-agent-configuration-service"
    project_name_list.append(project_name_example)
    project_name_list.append("dev_platform-itsm-sync-service")
    #project_name_list.append("dev_qa-platform-profiling")
    '''
    hub = HubInstance()
    projects = hub.get_projects(limit=10)
    project_name_list=[]
    for arrayname in projects['items']:
        project_name_list.append(arrayname['name'])
    print(project_name_list)
    for project_name in project_name_list:
        # the name query returns all projects that begin with the provided name so we have to handle that later
        project_list = hub.get_projects(parameters={"q":"name:{}".format(project_name)})

        def write_to_csv_file(filename, version_list):
            with open(filename, 'w', newline='') as csvfile:
                project_versions_writer = csv.writer(csvfile)
                for project_name, version in version_list:
                    project_versions_writer.writerow([
                        project_name, 
                        version['versionName']
                    ])

        if 'totalCount' in project_list and project_list['totalCount'] > 0:
            all_versions = list()
            for project in project_list['items']:
                # project = project_list['items'][0]
                if project_name != 'all' and project['name'] != project_name:
                    # skip project unless it's name is same as one we are looking for
                    continue
                versions = hub.get_project_versions(project)
                if 'totalCount' in versions and versions['totalCount'] > 0:
                    version_list = versions['items']
                    sorted_version_list = sorted(version_list, key=lambda k: dt_parser.parse(k['createdAt']))

                    all_versions.extend([(project['name'], v) for v in sorted_version_list])
                else:
                    pprint.pprint("No versions found for project {}".format(project['name']))
            
            result = all_versions
        else:
            if project_name == "all":
                pprint.pprint("Did not find any projects")
            else:
                pprint.pprint("Did not find any project with name {}".format(project_name))
        version_count = len(result)
        version_list = []
        for i in range(0,version_count):
            version_list.append(result[i][1]['versionName'])

        print(version_list)














        hub = HubInstance()
        for version_from_list in version_list:
            print(version_from_list)
            project = hub.get_project_by_name(project_name)
            version = hub.get_version_by_name(project, str(version_from_list))

            bom_components = hub.get_version_components(version)

            logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', stream=sys.stderr, level=logging.DEBUG)
            logging.getLogger("requests").setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)

            all_risk_profile_info = list()

            for bom_component in bom_components['items']:
                all_risk_profile_info.append({
                        "{}:{}".format(bom_component['componentName'], bom_component['componentVersionName']):
                            {
                                'url': bom_component['_meta']['href'],
                                'licenseRiskProfile': bom_component['licenseRiskProfile'],
                                'operationalRiskProfile': bom_component['operationalRiskProfile'],
                                'securityRiskProfile': bom_component['securityRiskProfile']
                                
                            }
                    })
            #pprint.pprint(all_risk_profile_info)
            if len(all_risk_profile_info) == 0:
                continue
            result_length = len(all_risk_profile_info)
            operational_medium = 0
            operational_low = 0
            operational_high = 0
            license_high = 0 
            license_low = 0
            license_medium = 0
            security_high = 0
            security_low = 0
            security_medium = 0

            for i in range(0,result_length):

                for component in all_risk_profile_info[i]:
                    if all_risk_profile_info[i][component]['operationalRiskProfile']['counts'][4]['count']>0:
                        operational_high = operational_high + 1
                    elif all_risk_profile_info[i][component]['operationalRiskProfile']['counts'][3]['count']>0:
                        operational_medium = operational_medium + 1
                    elif all_risk_profile_info[i][component]['operationalRiskProfile']['counts'][2]['count']>0:
                        operational_low = operational_low + 1
                    if all_risk_profile_info[i][component]['licenseRiskProfile']['counts'][4]['count']>0:
                        license_high = license_high + 1
                    elif all_risk_profile_info[i][component]['licenseRiskProfile']['counts'][3]['count']>0:
                        license_medium = license_medium + 1
                    elif all_risk_profile_info[i][component]['licenseRiskProfile']['counts'][2]['count']>0:
                        license_low = license_low + 1

                    if all_risk_profile_info[i][component]['securityRiskProfile']['counts'][4]['count']>0:
                        security_high = security_high + 1
                        
                    elif all_risk_profile_info[i][component]['securityRiskProfile']['counts'][3]['count']>0:
                        security_medium = security_medium + 1
                        
                    elif all_risk_profile_info[i][component]['securityRiskProfile']['counts'][2]['count']>0:
                        security_low = security_low + 1

            print("operational_medium " )
            print(operational_medium)
            print("operational_high " )
            print(operational_high)
            print("operational_low " )
            print(operational_low)
            print("license_medium " )
            print(license_medium)
            print("license_high " )
            print(license_high)
            print("license_low ")
            print(license_low)
            print("security_medium " )
            print(security_medium)
            print("security_high " )
            print(security_high)
            print("security_low ")
            print(security_low)


            try:
                conn = MongoClient()
                print("Connected successfully!!!")
            except:
                print("Could not connect to MongoDB")

        # database 
            db = conn.dashboarddb

        # Created or Switched to collection names: my_gfg_collection 
            collection = db.blackduck
            '''
            emp_rec1 = {
                    "name":project_name,
                    "version" : version_from_list,
                    "SR" : [{"H" : security_high}, {"M" : security_medium}, {"L" : security_low}],
                    "OR" : [{"H" : operational_high}, {"M" : operational_medium}, {"L" : operational_low}],
                    "LR" : [{"H" : license_high}, {"M" : license_medium}, {"L" : license_low}]
                    }


        # Insert Data 
            rec_id1 = collection.insert_one(emp_rec1)
            '''
            result = collection.update_many( 
                {
                    "name":project_name,
                    "version":version_from_list
                }, 
                { 
                        "$set":{ 
                                    "name":project_name,
                                    "version" : version_from_list,
                                    "SR" : [{"H" : security_high}, {"M" : security_medium}, {"L" : security_low}],
                                    "OR" : [{"H" : operational_high}, {"M" : operational_medium}, {"L" : operational_low}],
                                    "LR" : [{"H" : license_high}, {"M" : license_medium}, {"L" : license_low}]
                                }, 
                        "$currentDate":{"lastModified":True} 
                        
                },
                upsert=True 
                ) 

    #    print("Data inserted with record ids",rec_id1)



def sched_job():
    schedule.every(600).seconds.do(test)
    return schedule.CancelJob

schedule.every().day.at('16:01').do(sched_job)

while True:
    schedule.run_pending()
    time.sleep(1)

