from functools import wraps

from GradeHubPlusApp.handlers.common.types import Any, Cache, Nothing

# проверка на единственный экземляр
def singleton(cls):
    @wraps(cls)
    def get_instance():
        if not hasattr(get_instance, 'instance'):
            get_instance.instance = cls()
        return get_instance.instance
    return get_instance

@singleton
class Menippe:
    """
    Menippe - это алгоритм кэширования. 
    Работает только в единичном экземляре.
    """

    def __init__(self):
        self.__cache_vault: list = []
        self.__optimization: bool = True
        self.__cache_size: int = 5

    def settings(self, **options) -> Nothing:
        for key, val in options.items():
            if key == 'optimization' and isinstance(val, bool):
                self.__optimization = val
            elif key == 'cache_size' and isinstance(val, int):
                self.__cache_size = val

    def insert(self, data: dict[str, Any]) -> Nothing:
        if data not in self.__cache_vault:
            if not self.__optimization:
                if len(self.__cache_vault) < self.__cache_size:
                    self.__cache_vault.append(data)
                else:
                    self.clear_vault()
                    self.__cache_vault.append(data)
            else:
                if len(self.__cache_vault) < self.__cache_size:
                    self.__cache_vault.append(data)
                else:
                    self.__cache_vault.remove(self.__cache_vault[0])
                    self.__cache_vault.append(data)

    def clear_vault(self) -> Nothing:
        self.__cache_vault.clear()

    def exists(self, request: Any) -> Cache:
        _match = False
        response = []

        for i in self.__cache_vault:
            if request == i['request']:
                _match = True
                response = i['response']
                break
            else:
                _match = False
                continue
        
        return _match, response
