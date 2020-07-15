#!/usr/bin/env python3

import boto3
import os
import sys
import yaml

region = os.environ.get('AWSREGION')

if region is None:
    print ("Please set the AWSREGION environment variable.")
    sys.exit(1)

print ("> working on region: {0}".format(region))

def init_session(r = None):
    if r is None:
        r = region
    s = boto3.session.Session(profile_name=r)
    return s.resource('ec2')


def build():
    if validate_template() == True:
        try:
            with open(sys.argv[2], 'r') as f:
                y = yaml.safe_load(f.read())
        except IOError:
            print( "{0} not found.".format(sys.argv[2]))
            sys.exit(1)
        for reg in y: # loop through regions
            ec2 = init_session(reg)
            for azlst in y[reg]: # loop through AZ list
                for az in azlst: # loop through AZ
                    for instance in azlst[az]:    
                        print(instance['name'])

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