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

    def __init__(self):
        self.__cache_vault: list = []  # хранилище
        self.__optimization: bool = True  # оптимизация добавления данных
        self.__vault_size: int = 5  # максимальный размер хранилища
    
    def insert(self, data: dict[str, Any]) -> Nothing:
        # проверяем, есть ли уже запрос в хранилище
        for item in self.__cache_vault:
            if item['request'] == data['request']:
                return None  # если уже есть, то ничего не добавляем
        
        # добавляем новые данные в хранилище
        self.__cache_vault.append(data)

        if self.__optimization:
            # проверяем, не превышает ли размер хранилища максимальный размер
            if len(self.__cache_vault) >= self.__vault_size:
                self.__cache_vault.pop(0)  # удаляем самые старые данные
        else:
            # проверяем, не превышает ли размер хранилища максимальный размер
            if len(self.__cache_vault) >= self.__vault_size:
                self.clear_vault()  # полностью очищаем хранилище
    
    def exists(self, request: Any) -> Cache:
        # проверяем, есть ли такой запрос в хранилище
        for item in self.__cache_vault:
            if item['request'] == request:
                return True, item['response']  # если есть, возвращаем True и данные
        
        return False, []
    
    def get_value(self, request: Any) -> list[Any] | None:
        # проверяем, есть ли такой запрос в хранилище
        for item in self.__cache_vault:
            if item['request'] == request:
                return item['response']  # если есть, возвращаем данные
        return None  # Возвращаем None, если такого запроса нет в хранилище
    
    def settings(self, **option) -> Nothing:
        for key, value in option.items():
            if key == 'optimization' or 'O' and isinstance(value, bool):
                self.__optimization = value
            elif key == 'vault_size' or 'S' and isinstance(value, int):
                self.__vault_size = value
 
    def clear_vault(self) -> Nothing: self.__cache_vault.clear()
