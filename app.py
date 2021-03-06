#!/usr/bin/env python3
import os

import aws_cdk as cdk

from custom_vpc.custom_vpc_stack import CustomVpcStack

from custom_vpc.config import config
app = cdk.App()
CustomVpcStack(app, "TaskVpc01",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    env=cdk.Environment(region=config["region"]), stack_name =config["stack"]["name"],  

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
