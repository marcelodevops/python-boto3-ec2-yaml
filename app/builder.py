#!/usr/bin/env python3

import boto3
from botocore import exceptions
import os
import sys
import yaml
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')
region = config['DEFAULT']['AWSREGION']

print("> running on region: {0}".format(region))


def ec2_session(reg=None):
    if reg is None:
        reg = region
    s = boto3.session.Session(profile_name=reg)
    return s.resource('ec2')


def blockdev(vol):
    print('creating ebs vols')
    ebs = {}
    if 'device' in vol:
        ebs = {
            'DeviceName': vol['device'],
            'Ebs': {
                'VolumeSize': vol['size_gb'],
                'DeleteOnTermination': True,
            }
        }

    else:
        print("{0} volumes not found.".format(sys.argv[2]))
    return ebs





def user_data(volumes):
    userdata = '#!/bin/bash \n'
    for vol in volumes:
        userdata = userdata + 'mkdir -p ' + vol['mount'] +'\n'
        userdata = userdata + 'mount -t ' + vol['type'] + ' ' + vol['device'] + ' ' + vol['mount'] + '\n'
    return userdata
# build the instance


def build():
    if validate_template() == True:

        try:
            with open(sys.argv[2], 'r') as f:
                yt = yaml.safe_load(f.read())
        except IOError:
            print("{0} not found.".format(sys.argv[2]))
            sys.exit(1)
        #
        for profile in yt:  # profiles loop
            ec2 = ec2_session(profile)
            blockdevmap = []
            for server in yt[profile]:  # loop through servers list
                for vol in server['volumes']:  # loop through AZ
                    blockdevmap.append(blockdev(vol))
                for user in server['users']:
                    try:
                        kp = ec2.import_key_pair(KeyName=user['login'],PublicKeyMaterial=user['ssh_key'])
                    except exceptions.ClientError:
                        pass
                server_id = create_instance(server, ec2, blockdevmap,user['login'])
                print("Created server id {0}".format(server_id))


# creating the EC2 instance
def create_instance(server, ec2, blockdevmap,user_login):

    rc = ec2.create_instances(
        MinCount=1,
        MaxCount=1,
        KeyName = user_login,
        InstanceType=server['server_type'],
        ImageId='ami-042760c4b14cf6044',
        BlockDeviceMappings=blockdevmap,
        UserData=user_data(server['volumes'])
    )
    server_id = rc[0].id
    ec2.create_tags(
        Resources=[server_id],
        Tags=name_tag(server['server_name'])
    )
    return server_id


def delete():
    if len(sys.argv) < 3:
        print("usage: {0} delete <aws instance id>")
        sys.exit(1)

    ec2 = ec2_session()

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
