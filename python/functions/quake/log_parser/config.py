from infra.services import Services

class LogParserConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="LogParser",
            path="./functions/quake",
            description="Read the log file, group game data of each match and collect kill data",
            directory="log_parser",
            layers=[services.layers.quake_parser_layer],
        )

        services.api_gateway.create_endpoint("GET", "/quake", function, public=True)

            