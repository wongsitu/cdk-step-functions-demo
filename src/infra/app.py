#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.cdk_step_functions_demo_stack import CdkStepFunctionsDemoStack


app = cdk.App()
CdkStepFunctionsDemoStack(app, "CdkStepFunctionsDemoStack")

app.synth()
