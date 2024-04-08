from infra.services import Services

class LogParserConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="PythonLogParser",
            path="./functions/log_parser",
            description="Read the log file, group game data of each match and collect kill data",
        )

        services.api_gateway.create_endpoint("GET", "/quake", function, public=True)

            