from infra.services import Services
from aws_cdk.aws_lambda import Code, Function, Runtime

class NodeLogParserConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="NodeLogParser",
            path="./functions/quake",
            description="Parse quake",
            directory="node_log_parser",
            runtime=Runtime.NODEJS_16_X,            
        )

        services.api_gateway.create_endpoint("GET", "/node/quake", function, public=True)

            