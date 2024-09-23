from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    BundlingOptions,
    aws_iam as iam,
    aws_s3 as s3,
    RemovalPolicy,
    Duration
)
from constructs import Construct
import os


class CdkStepFunctionsDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        current_dir = os.path.dirname(__file__)

        demo_bucket = s3.Bucket(self, "StepFunctionsDemoBucket",
                                block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                encryption=s3.BucketEncryption.S3_MANAGED,
                                versioned=False,
                                removal_policy=RemovalPolicy.DESTROY
                                )

        bundling = BundlingOptions(
            image=_lambda.Runtime.PYTHON_3_10.bundling_image,
            command=[
                "bash", "-c",
                "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output"
            ],
        )

        submit_lambda_dir = os.path.join(
            current_dir, "..", "..", "lambdas", "submit_lambda")
        submit_lambda = _lambda.Function(self, 'SubmitLambdaFunction',
                                         runtime=_lambda.Runtime.PYTHON_3_10,
                                         code=_lambda.Code.from_asset(submit_lambda_dir,
                                                                      bundling=bundling),
                                         handler='submit_lambda.handler',
                                         timeout=Duration.seconds(900),
                                         )

        process_entity_dir = os.path.join(
            current_dir, "..", "..", "lambdas", "process_entity")
        process_entity = _lambda.Function(self, 'ProcessEntityFunction',
                                          runtime=_lambda.Runtime.PYTHON_3_10,
                                          code=_lambda.Code.from_asset(process_entity_dir,
                                                                       bundling=bundling),
                                          handler='process_entity.handler',
                                          environment={
                                              "BUCKET_NAME": demo_bucket.bucket_name
                                          },
                                          timeout=Duration.seconds(900),
                                          )
        demo_bucket.grant_read_write(process_entity)

        generate_excel_dir = os.path.join(
            current_dir, "..", "..", "lambdas", "generate_excel")
        generate_excel = _lambda.Function(self, 'GenerateExcelFunction',
                                          runtime=_lambda.Runtime.PYTHON_3_10,
                                          code=_lambda.Code.from_asset(generate_excel_dir,
                                                                       bundling=bundling),
                                          handler='generate_excel.handler',
                                          environment={
                                              "BUCKET_NAME": demo_bucket.bucket_name
                                          },
                                          timeout=Duration.seconds(900),
                                          )
        demo_bucket.grant_read_write(generate_excel)

        state_machine_dir = os.path.join(
            current_dir, "statemachine.asl.json")
        state_machine_role = iam.Role(self, "StateMachineRole",
                                      assumed_by=iam.ServicePrincipal(
                                          "states.amazonaws.com"),
                                      )
        submit_lambda.grant_invoke(state_machine_role)
        process_entity.grant_invoke(state_machine_role)
        generate_excel.grant_invoke(state_machine_role)
        
        workflow = sfn.StateMachine(self, "StateMachine",
                                    definition_body=sfn.DefinitionBody.from_file(
                                        state_machine_dir),
                                    role=state_machine_role,
                                    definition_substitutions={
                                        "SubmitLambdaArn": submit_lambda.function_arn,
                                        "ProcessEntityLambdaArn": process_entity.function_arn,
                                        "GenerateExcelLambdaArn": generate_excel.function_arn,
                                    }
                                    )
