from functions.for_working_with_API.get_photo import get_photo


def getting_information_about_the_hotel(hotel_info: dict, photo_quantity: int) -> list:
    """Функция для формирования информации об отеле
    принимает
        hotel_info: dict - словарь с информацией об отеле
        photo_quantity: int - количество фото для каждого отеля

    возвращает
        список из 3 элементов:
            сообщение с информацией
            id отеля
            список с url фотогорафий
    """

    info_dict = {'name': hotel_info.get("name", '-'),
                 'id': f'https://www.hotels.com/h{hotel_info["id"]}.Hotel-Information',
                 'rating_total': hotel_info.get('reviews', {}).get('total', '-'),
                 'rating': hotel_info.get('reviews', {}).get('score', '-'),

                 'ratePlan_current': hotel_info.get('price', {}).get("displayMessages", {})[0].get(
                     "lineItems", {})[-1].get('price', {}).get('accessibilityLabel', '-').split(' ')[-1],

                 'full_price': hotel_info.get('price', {}).get(
                     "displayMessages", {})[1].get("lineItems", {})[-1].get("value", '-').split()[0]}
    detail_info = get_photo(hotel_info["id"])
    massage_exp = False
    photo = []
    if not isinstance(detail_info, str):
        star = detail_info.get('data', {}).get("propertyInfo", {}).get(
                'summary', {}).get("overview", {}).get("propertyRating", {})
        if star:
            info_dict['starRating'] = star.get("rating", '-')
        else:
            info_dict['starRating'] = '-'

        info_dict['streetAddress'] = detail_info.get('data', {}).get('propertyInfo', {}).get(
            'summary', {}).get("location", {}).get('address', {}).get('addressLine', '-')
        for image in detail_info['data']['propertyInfo']['propertyGallery']["images"]:
            if len(photo) == photo_quantity:
                break
            photo.append(image['image']['url'])
    else:
        info_dict['starRating'] = '-'
        info_dict['streetAddress'] = '-'
        massage_exp = True

    info_massage = f'Название отеля: {info_dict["name"]}\n' \
                   f'Количество звезд: {info_dict["starRating"]}\n' \
                   f'Адрес: {info_dict["streetAddress"]}\n' \
                   f'Рейтинг Hotels.com: {info_dict["rating"]}\n' \
                   f'Всего оценок: {info_dict["rating_total"]}\n' \
                   f'Цена за ночь: {info_dict["ratePlan_current"]}\n' \
                   f'Цена за выбранные даты: {info_dict["full_price"]}\n'
    website = info_dict["id"]

    return [info_massage, website, photo, massage_exp]
