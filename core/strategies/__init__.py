from .base_strategy import ParsingStrategy


class StrategyFactory:
    _strategies = {}

    @classmethod
    def register(cls, report_id: str):
        def decorator(strategy_class):
            cls._strategies[report_id] = strategy_class
            return strategy_class

        return decorator

    @classmethod
    def get_strategy(cls, report_id: str) -> type[ParsingStrategy]:
        return cls._strategies.get(report_id)


# Decorador para auto-registro
def register_strategy(report_id: str):
    return StrategyFactory.register(report_id)
