from os import environ
import boto3, sys, subprocess
from botocore.exceptions import ClientError
from models import c


def change_ec2_ip():
    print("["+c.OKBLUE+"*"+c.ENDC+"] Changing EC2 Proxy IP")
    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=environ['AWS_ELASTIC_IP_KEY'],
        aws_secret_access_key=environ['AWS_ELASTIC_IP_SECRET']
    )

    try:
        # Current Elastic IP
        address = ec2.describe_addresses()['Addresses'][0]
        instance_id = address['InstanceId']
        public_ip = address['PublicIp']
        #private_ip = address['PrivateIpAddress']

        print("\t["+c.WARNING+"*"+c.ENDC+"] Current IP: %s" % public_ip)

        # Release Elastic IP
        print("\t["+c.WARNING+"-"+c.ENDC+"] Releasing IP...")
        response = ec2.release_address(AllocationId=address['AllocationId'])

        # Get new Elastic IP
        print("\t["+c.WARNING+"+"+c.ENDC+"] Getting new IP... ", end=""); sys.stdout.flush()
        allocation = ec2.allocate_address(Domain='vpc')
        new_ip = allocation['PublicIp']
        print(new_ip)

        # Associate address
        print("\t["+c.WARNING+"*"+c.ENDC+"] Attaching IP to instance... ", end=""); sys.stdout.flush()
        response = ec2.associate_address(
            AllocationId=allocation['AllocationId'],
            InstanceId=instance_id
        )
        print(c.OKGREEN+"SUCCESS"+c.ENDC)
    except ClientError as e:
        print(e)
    else:
        subprocess.run(["killall", "ssh"])
        # Create local ssh tunnel proxy to EC2 instance
        subprocess.check_output(["ssh", "-D", "1080", "-fCqN",
                                 "-i", "~/.ssh/ec2-ubuntu.pem",
                                 "-o", "StrictHostKeyChecking=no",
                                 "ubuntu@{}".format(new_ip)
                                ])

if __name__ == "__main__":
    change_ec2_ip()
