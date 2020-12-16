import Levenshtein
import json
from mediawiki import MediaWiki

wikipedia = MediaWiki(lang='ru')

result_data = []
i = 0

with open("query_result.json", "r") as read_file:
    data = json.load(read_file)
    for value in data['elements']:
        data_found = False
        p = ''

        # Проверим, возможно ссылка на википедию уже есть
        if "wikipedia" in value['tags']:
            p = wikipedia.page(value['tags']['wikipedia'])
            data_found = True
        else:
            # Проверим по геоположению и полю name
            geo = wikipedia.geosearch(latitude=value['lat'], longitude=value['lon'])
            if "name" in value['tags']:
                for geo_res in geo:
                    if Levenshtein.distance(geo_res, value['tags']['name']) <= 3:
                        p = wikipedia.page(geo_res)
                        data_found = True
                        break
            # Проверим по геоположению и полю alt_name
            if not data_found and "alt_name" in value['tags']:
                for geo_res in geo:
                    if Levenshtein.distance(geo_res, value['tags']['alt_name']) <= 3:
                        p = wikipedia.page(geo_res)
                        data_found = True
                        break

            # Предпоследняя попытка. Поиск по имени
            if not data_found:
                if "name" in value['tags']:
                    name_search = wikipedia.search(value['tags']['name'])

                    for name_res in name_search:
                        if Levenshtein.distance(geo_res, value['tags']['name']) <= 3:
                            p = wikipedia.page(name_res)
                            data_found = True
                            break

            # Последняя попытка. Поиск по альтернативному имени
            if not data_found:
                if "alt_name" in value['tags']:
                    name_search = wikipedia.search(value['tags']['alt_name'])

                    for name_res in name_search:
                        if Levenshtein.distance(geo_res, value['tags']['alt_name']) <= 3:
                            p = wikipedia.page(name_res)
                            data_found = True
                            break

        # Добавляем только достопримечательности с данными
        if data_found:
            result_data.append(value)
            result_data[i]['wiki_summary'] = p.summary
            result_data[i]['wiki_catrgories'] = p.categories
            result_data[i]['wiki_images'] = p.images
            i += 1

    # Записываем результат
    with open("result_with_wiki_data.json", "w") as write_file:
        json.dump(result_data, write_file)
