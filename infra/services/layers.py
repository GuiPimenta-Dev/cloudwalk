from aws_cdk import aws_lambda as _lambda
from lambda_forge import Path


class Layers:
    def __init__(self, scope) -> None:

        self.parser_layer = _lambda.LayerVersion(
            scope,
            id='ParserLayer',
            code=_lambda.Code.from_asset(Path.layer('layers/parser')),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description='Quake Logs Parser Layer',
         )
