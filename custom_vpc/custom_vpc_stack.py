from multiprocessing import connection
from aws_cdk import (
    # Duration,
    CfnTag,
    Stack,
    # aws_sqs as sqs,
    aws_ec2 as ec2
)
from constructs import Construct
config_file = "D:\23-2\cdk-project\cdk_project\config.json"
import json
with open(config_file, 'r') as myfile:
    data=myfile.read()
config = json.loads(data)

class CustomVpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = ec2.Vpc(
                self, config["vpc"]["id"],
                cidr= config["vpc"]["cidr"],
                max_azs=1,subnet_configuration=[])
        cfn_internet_gateway = ec2.CfnInternetGateway(self,config["igw"]["id"],tags=[CfnTag(key="Name",value=config["igw"]["name"])])
        cfn_vPCGateway_attachment = ec2.CfnVPCGatewayAttachment(self,config["igwAttachment"]["id"],vpc_id=vpc.vpc_id,internet_gateway_id= cfn_internet_gateway.attr_internet_gateway_id)


        cfn_elasticIp = ec2.CfnEIP(self,id= config["elasticIp"]["id"],
                            tags=[CfnTag(key="Name",
                            value=config["elasticIp"]["name"])])
        

        publicSubnet = ec2.Subnet(self,
                            id=config["publicSubnet"]["id"],
                            availability_zone=vpc.availability_zones[0],
                            cidr_block=config["publicSubnet"]["cidr"],
                            vpc_id=vpc.vpc_id,
                            map_public_ip_on_launch=True,

                        )

        privateSubnet = ec2.Subnet(self,
                            id=config["privateSubnet"]["id"],
                            availability_zone=vpc.availability_zones[0],
                            cidr_block=config["privateSubnet"]["cidr"],
                            vpc_id=vpc.vpc_id,
                            map_public_ip_on_launch=False
                        )
       

        cfn_nat_gateway = ec2.CfnNatGateway(self,
                            id=config["natgw"]["id"],
                            subnet_id=publicSubnet.subnet_id,
                            connectivity_type="public",
                            allocation_id= cfn_elasticIp.attr_allocation_id,
                            tags=[CfnTag(
                                    key="Name",
                                    value=config["natgw"]["name"]
                                    )
                                ]
                        )
        cfn_route_nat_gateway = ec2.CfnRoute(self,
                                    id=config["natgwRoute"]["id"],
                                    route_table_id=privateSubnet.route_table.route_table_id,
                                    destination_cidr_block=config["natgwRoute"]["cidr"],
                                    nat_gateway_id=cfn_nat_gateway.ref)

        cfn_route_internet_gateway = ec2.CfnRoute(self,
                                    id=config["igwRoute"]["id"],
                                    route_table_id=publicSubnet.route_table.route_table_id,
                                    destination_cidr_block=config["igwRoute"]["cidr"],
                                    gateway_id=cfn_internet_gateway.attr_internet_gateway_id)
        
        securityGroup = ec2.SecurityGroup(self,
                            id=config["securityGroup"]["id"],
                            vpc = vpc,
                            security_group_name=config["securityGroup"]["name"],
                            description=config["securityGroup"]["description"])
        securityGroup.add_ingress_rule(peer=config["inboundRule"]["peer"],
                                        connection=config["inboundRule"]["connection"],
                                        description=config["inboundRule"]["description"])
        
        Tag.of(securityGroup).add("Name",config["securityGroup"]["displayName"])
        publicSubnetInstance = ec2.Instance(self,
                                config["publicInstance"]["id"], 
                                instance_type= config["publicInstance"]["type"], 
                                machine_image= config["publicInstance"]["image"],
                                vpc=vpc,
                                security_group= securityGroup,
                                key_name=config["publicInstance"]["keyName"],
                                vpc_subnets=ec2.SubnetSelection(subnets=[publicSubnet],
                                
                                )
                                ) 
        privateSubnetInstance = ec2.Instance(self,
                                config["privateInstance"]["id"], 
                                instance_type= config["privateInstance"]["type"], 
                                machine_image= config["privateInstance"]["image"],
                                vpc=vpc,
                                security_group= securityGroup,
                                key_name=config["privateInstance"]["keyName"],
                                vpc_subnets=ec2.SubnetSelection(subnets=[privateSubnet])
                                ) 
        metric = cloudwatch.Metric(
                                    namespace=config["metric"]["namespace"],
                                    metric_name=config["metric"]["metric_name"],
                                    period=Duration.minutes(1),
                                    dimensions_map={
                                                "Name" : "publicInstance",
                                                "Value" : "publicInstance"
                                            }
                                    )
        alarm = cloudwatch.Alarm(self, "Alarm",
                                    metric=metric,
                                    threshold=config["alarm"]["threshold"],
                                    evaluation_periods=config["alarm"]["evaluation_periods"],
                                    datapoints_to_alarm=config["alarm"]["datapoints_to_alarm"]
                                    
                                )
