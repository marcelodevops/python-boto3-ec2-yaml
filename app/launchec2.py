import boto3
import yaml

ec2 = boto3.client("ec2", region_name="us-west-2")

def buildInstance():
#for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
#    print(status)

    response = ec2.run_instances(
                                    BlockDeviceMappings=[
                                        {
                                            'DeviceName': '/dev/xvda',
                                            'Ebs': {
                                                'DeleteOnTermination': True,
                                                'VolumeSize': 10,
                                                'VolumeType': 'standard',
                                                'Encrypted': False
                                            },

                                        }
                                    ],
                                    ImageId='ami-09587790ad4ba4002',
                                    InstanceType='t2.small',
                                    MinCount=1,
                                    MaxCount=1)
    print(response)


buildInstance()