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
                self, "TaskVpc011",
                cidr="10.20.0.0/16",
                max_azs=1,subnet_configuration=[])
                #nat_gateways=1,
                #internet_gateway_id="internetGatewayId",
                #nat_gateway_provider=ec2.NatProvider.gateway(),
                
        elastic_ip = ec2.CfnEIP(self, 
                                "EIP",
                                tags=[CfnTag(key="Name", value="elasticIp")]
                                )
    
        cfn_internet_gateway = ec2.CfnInternetGateway(self, 
                                    "IGWPublicSubnet01")
        cfn_vPCGateway_attachment = ec2.CfnVPCGatewayAttachment(self, 
                                        "IGWPublicSubnet01vpcattachement", 
                                        vpc_id=vpc.vpc_id, 
                                        internet_gateway_id=cfn_internet_gateway.attr_internet_gateway_id)

        publicSubnet= ec2.Subnet(self,
                             id="PublicSubnet01", 
                             availability_zone=vpc.availability_zones[0], 
                             cidr_block="10.20.1.0/24",
                             vpc_id=vpc.vpc_id , 
                             map_public_ip_on_launch=True)
        privateSubnet= ec2.Subnet(self, 
                            id="PrivateSubnet01", 
                            availability_zone=vpc.availability_zones[0],
                            cidr_block="10.20.2.0/24", 
                            vpc_id=vpc.vpc_id ,
                            map_public_ip_on_launch=False)
        cfn_nat_gateway= ec2.CfnNatGateway(self,
                                 "NatGatewayPrivateSubnet01", 
                                 subnet_id=publicSubnet.subnet_id, 
                                 connectivity_type="public",
                                 allocation_id=elastic_ip.attr_allocation_id,
                                 tags=[CfnTag(key="Name", value="NatGatewayPrivateSubnet01")]
                                 )
        cfn_route_internet_gateway = ec2.CfnRoute(self,
                                        id = "publicSubnetgateway", 
                                        route_table_id=publicSubnet.route_table.route_table_id,
                                        destination_cidr_block="0.0.0.0/0",
                                        gateway_id=cfn_internet_gateway.attr_internet_gateway_id
                                        
                                        )
        cfn_route_nat_gateway = ec2.CfnRoute(self, 
                                    id = "privateSubnetgateway", 
                                    route_table_id=privateSubnet.route_table.route_table_id,
                                    destination_cidr_block="0.0.0.0/0",
                                    nat_gateway_id=cfn_nat_gateway.ref)
        sec_group = ec2.SecurityGroup(self,
                        id="sg-securitygroup01",
                        security_group_name="CDKSecurity",
                        description="sec-group-allow-ssh",
                        vpc=vpc,
                        allow_all_outbound=True
        )
        sec_group.add_ingress_rule(peer=ec2.Peer.any_ipv4(),
                    description="Allow SSH connection", 
                    connection=ec2.Port.tcp(22))

        # define a new ec2 instance
        publicSubnetInstance = ec2.Instance(self,
                        "MyPublicInstance",
                        instance_name="MyInstance1",
                        machine_image=ec2.MachineImage.latest_amazon_linux(),
                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,ec2.InstanceSize.MICRO),
                        vpc=vpc,
                        key_name="DhanyaKey",
                        vpc_subnets=ec2.SubnetSelection(subnets=[publicSubnet]),
                        security_group=sec_group
                                             
        )
        privateSubnetInstance = ec2.Instance(self, 
                        "MyPrivateInstance",
                        instance_name="MyInstance2",
                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2,ec2.InstanceSize.MICRO),
                        machine_image=ec2.MachineImage.latest_amazon_linux(),
                        vpc=vpc,
                        key_name="DhanyaKey",
                        vpc_subnets=ec2.SubnetSelection(subnets=[privateSubnet]),
                        security_group=sec_group
                        )
