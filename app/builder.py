#!/usr/bin/env python3

import boto3
import os
import sys
import yaml

region = os.environ.get('AWSREGION')

if region is None:
    print ("Please set the AWSREGION environment variable.")
    sys.exit(1)

print ("> runing on region: {0}".format(region))

def profile_session(reg = None):
    if reg is None:
        reg = region
    s = boto3.session.Session(profile_name=reg)
    return s.resource('ec2')

def blockdev(vol):
    ebs = {}
    if 'device' in vol:
        ebs= {
                'DeviceName': vol['device'],
                'Ebs': {
                    'VolumeSize': vol['size_gb'],
                    'DeleteOnTermination': True,
                }
            }
            
        
    else:
        print("{0} volumes not found.".format(sys.argv[2]))
    return ebs


def build():
    if validate_template() == True:
        try:
            with open(sys.argv[2], 'r') as f:
                yt = yaml.safe_load(f.read())
        except IOError:
            print( "{0} not found.".format(sys.argv[2]))
            sys.exit(1)
        for profile in yt: # profiles loop
            ec2 = profile_session(profile)
            map = []
            for server in yt[profile]: # loop through servers list
                print(server['server_name'])
                i = 0
                for vol in server['volumes']: # loop through AZ
                    map.append(blockdev(vol))
                    #for instance in server[vol]:    
                     #   print(instance['name'])
                print("creating instance {0}".format(server['server_name']))
def delete():
    if len(sys.argv) < 3:
        print("usage: {0} delete <aws instance id>")
        sys.exit(1)

    ec2 = profile_session()

    try:
        ec2.instances.filter(InstanceIds=[sys.argv[2]]).terminate()
    except:
        print('error deleting {0}'.format(sys.argv[2]))
        sys.exit(1)

def validate_template():
    return True

def get_id_by_name(ec2obj, tag):
    for o in ec2obj.filter(Filters=[{'Name': 'tag:Name', 'Values': [tag]}]):
        return o.id

    return None

def name_tag(val):
    return [{'Key': 'Name', 'Value': val}]



if __name__ == '__main__':
    getattr(sys.modules[__name__], sys.argv[1])()