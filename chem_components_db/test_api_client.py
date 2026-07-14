# import requests

# BASE_URL = "http://127.0.0"

# def test_search(query):
#     print(f"\n--- Поиск по запросу: '{query}' ---")
#     response = requests.get(BASE_URL, params={"search": query})
#     if response.status_code == 200:
#         results = response.json()
#         print(f"Найдено компонентов: {len(results)}")
#         for comp in results:
#             print(f"[{comp['id']}] {comp['name']} ({comp['formula']}) | CAS: {comp['cas_number']}")
#             # Если нашли, запросим полную карточку
#             fetch_detail(comp['id'])
#     else:
#         print(f"Ошибка запроса: {response.status_code}")

# def fetch_detail(component_id):
#     response = requests.get(f"{BASE_URL}{component_id}/")
#     if response.status_code == 200:
#         data = response.json()
#         print(f"  -> Критическая температура: {data['critical_temperature']} K")
#         print(f"  -> Синонимы: {[a['alias_name'] for a in data['aliases']]}")
#         print(f"  -> Доступно свойств в БД: {len(data['properties'])}")

# if __name__ == "__main__":
#     # Примеры тестов (запустите, когда Участник 3 импортирует тестовый датасет)
#     test_search("74-82-8")  # Поиск по CAS (Метан)
#     test_search("CH4")     # Поиск по формуле
#     test_search("METHANE") # Поиск по имени Aspen
    