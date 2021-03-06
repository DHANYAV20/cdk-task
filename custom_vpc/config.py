from aws_cdk import aws_ec2 as ec2 

config={
"region":"us-west-2",
"stack":{
    "name":"TaskStack01"
},
"vpc":{
    "id" : "TaskVpc01",
    "cidr":"10.20.0.0/16",
},
"igw":{
    "id":"IGWPublicSubnet01",
    "name":"IGWPublicSubnet01"
},
"igwAttachment":{
    "id":"IGWPublicSubnet01vpcattachment"
},
"elasticIp":{
    "id":"ElasticIp01",
    "name":"ElasticIp01"    
},
"publicSubnet":{
    "id":"PublicSubnet01",
    "cidr":"10.20.1.0/24"
},
"privateSubnet":{
    "id":"PrivateSubnet01",
    "cidr":"10.20.2.0/24"
},
"natgw" : {
    "id":"NatGatewayPrivateSubnet01",
    "name" : "NatGatewayPrivateSubnet01"
},
"natgwRoute" :{
    "id" :"privateSubnetgatewayRoute",   
    "cidr" : "0.0.0.0/0"
},
"igwRoute" :{
    "id" :"publicSubnetgatewayRoute",   
    "cidr" : "0.0.0.0/0"
},
"securityGroup":{
    "displayName" :"TaskVPCSecurityGroup01",
    "id" : "TheSecurityGroup",
    "name" : "TaskVPCSecurityGroup01",
    "description" : "TaskVPCSecurityGroup01"
},
"inboundRule":{
    "peer":ec2.Peer.any_ipv4(),
    "connection" : ec2.Port.tcp(22),
    "description" :"allow ssh from anywhere"
},
"publicInstance":{
    "id":"publicInstance",
    "type":ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,ec2.InstanceSize.MICRO),
    "image":ec2.MachineImage.latest_amazon_linux(),
    "keyName":"DhanyaKey"
    
},
"privateInstance":{
    "id":"privateInstance",
    "type":ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,ec2.InstanceSize.MICRO),
    "image":ec2.MachineImage.latest_amazon_linux(),
    "keyName":"DhanyaKey"
    
},
"metric":{
    "namespace":"AWS/EC2",
    "metric_name":"MyMetric"
},
"alarm":{
    "threshold":100,
    "evaluation_periods":3,
    "datapoints_to_alarm":2,
},
"sns":{
    "display_name":"Konstone 24x7 on whatsapp support",
    "topic_name":"KonstoneOpsTeam"
},
"rds":{
    "database_name":"MyDatabase",
    "allocated_storage":30, 
    "port":3308, 
    "multi_az":False, 
    "instance_identifier":"publicSubnetInstance",
    "instance_type":ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
    "deletion_protection":False, 
    "delete_automated_backups":True, 
    "id":"RDS"
},
"alb":{
    "id":"MyElb",
    "internet_facing":False, 
    "load_balancer_name":"FirstLoadBalancer",
}
}
