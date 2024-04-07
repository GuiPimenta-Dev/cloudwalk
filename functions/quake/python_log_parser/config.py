from infra.services import Services

class LogParserConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="PythonLogParser",
            path="./functions/quake",
            description="Read the log file, group game data of each match and collect kill data",
            directory="python_log_parser",
            layers=[services.layers.quake_parser_layer],
        )

        services.api_gateway.create_endpoint("GET", "/python/quake", function, public=True)

            