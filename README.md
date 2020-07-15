# python-boto3-ec2-yaml
python boto3 exercise

server:
  server_type: t3.small # 1                                     server.server_type
  volumes:                                                      server.volumes   
  - device: /dev/xvda # 2                                       server.volumes.device
    size_gb: 10 # 3                                             server.volumes.size_gb
    type: ext4 # 4                                              server.volumes.type
    mount: / # 5                                                server.volumes.mount
  - device: /dev/xvdf
    size_gb: 100
    type: xfs
    mount: /data
  users:  # 6                                                   server.users
  - login: user1                                                server.users.login
    ssh_key: <user ssh public key goes here> user1@localhost    server.users.ssh_key
