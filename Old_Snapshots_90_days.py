#!/usr/bin/python3.8
import boto3
import datetime
import sys
from pprint import pprint
import os
import csv

ArgLen=len(sys.argv)
if ArgLen < 3:
   print("Need Parameters: AccountId  Region")
   print("Example: ./"+os.path.basename(sys.argv[0])+" 699183880494/897860998156 us-east-1")
   sys.exit()

outputfile="/tmp/old_snapshot_ids-"+sys.argv[1]+"-"+sys.argv[2]+".csv"
csv_ob=open(outputfile,'w',newline="")
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S No","Snapshot Name","Snapshot_ID","CreationTime","Region"])
cnt=1

client = boto3.client(service_name='ec2',region_name=sys.argv[2])
snapshots = client.describe_snapshots(OwnerIds=[sys.argv[1]])
for snapshot in snapshots['Snapshots']:
       #pprint(snapshot['Description'].split())
       if snapshot['Description'].split()[0] == 'Created':
          AMIID=snapshot['Description'].split()[4]
          #print(AMIID)
       if snapshot['Description'].split()[0] == 'Copied':
          AMIID=snapshot['Description'].split()[3]
          #print(AMIID)

       try:
        response=client.describe_images(ImageIds=[AMIID,])
        for item in response['Images']:
          if 'AwsBackup_' not in item['Name']:
              famiid=AMIID
          else:
              famiid="nothing"

        a= snapshot['StartTime']
        b=a.date()
        c=datetime.datetime.now().date()
        d=c-b

        for tag in snapshot['Tags']:
          if  tag['Key'] == 'Name' and d.days>90 and famiid in snapshot['Description']:
                 Name=tag['Value']
                 SnapshotId=snapshot['SnapshotId']
                 creationtime=snapshot['StartTime'].strftime("%Y-%m-%d")
                 print(cnt,Name,SnapshotId,creationtime,sys.argv[2])
                 csv_w.writerow([cnt,Name,SnapshotId,creationtime,sys.argv[2]])
                 cnt +=1
       except Exception as error:
          continue

csv_ob.close()

'''
object=open(outputfile,'w',newline="")
if os.path.getsize(outputfile)==0:
    object.write(f"There are no 90 day's old Snapshots in {sys.argv[1]} Account {sys.argv[2]} Region")
object.close()
'''
