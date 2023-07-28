from flask import Blueprint as FlaskBlueprint


class Blueprint(FlaskBlueprint):
    def __init__(self, name: str) -> None:
        super().__init__(name, __name__, template_folder="../templates", static_folder="../static")