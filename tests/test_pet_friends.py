from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос ключа возвращает статус 200 и в тезультате содержится слово ключ"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем вход пользователя c неверным паролем """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "This user wasn't found in database" in result


def test_get_api_key_with_invalid_email(email=invalid_email, password=valid_password):
    """ Проверяем вход пользователя c неверным логином """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "This user wasn't found in database" in result


def test_add_or_change_photo_of_first_pet_in_list_of_my_pets_with_valid_data():
    """ Проверяем запрос добавление или изменение фото у первого питомца """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]
    if len(list_of_my_pets["pets"]) > 0:
        id_of_first_pet = list_of_my_pets["pets"][0]["id"]
        status, result = pf.add_photo_of_pet(auth_key,
                                             pet_id=id_of_first_pet,
                                             pet_photo='images\cat-myau.jpg')

        assert status == 200
        assert result['id'] == id_of_first_pet
        assert result['pet_photo'] != ''
    else:
        raise Exception('У вас нет добавленных питомцев')


def test_add_new_pet_without_photo_with_valid_data():
    """ Проверяем запрос добавление питомца без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = 'Пикси'
    animal_type = 'кошка'
    age = '3'
    status, result = pf.add_information_about_new_pet_without_photo(auth_key,
                                                                    name=name,
                                                                    animal_type=animal_type,
                                                                    age=age)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем запрос все питомцы позитивный"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert 'pets' in result.keys()


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем запрос мои питомцы позитивный """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert 'pets' in result.keys()


def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем запрос всех питомцев негативный """

    auth_key = {'key': 'invalid_key'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert "Please provide 'auth_key' Header" in result


def test_add_new_pet_without_photo_with_invalid_age():
    """ Проверяем запрос добавление питомца без фото с отрицательным возрастом """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = 'Микси'
    animal_type = 'заяц'
    age = '-33'
    status, result = pf.add_information_about_new_pet_without_photo(auth_key,
                                                                    name=name,
                                                                    animal_type=animal_type,
                                                                    age=age)

    assert status == 400
    assert "Parameter 'age' cannot be negative." in result


def test_add_or_change_photo_of_first_pet_in_list_of_my_pets_with_invalid_pet_id():
    """ Проверяем запрос добавление или изменение фото у первого питомца с invalid_pet_id """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]
    if len(list_of_my_pets["pets"]) > 0:
        status, result = pf.add_photo_of_pet(auth_key,
                                             pet_id='invalid_pet_id',
                                             pet_photo='images\wild-rabbit.jpg')

        assert status == 400
        assert "Pet with this id wasn't found!" in result
    else:
        raise Exception('У вас нет добавленных питомцев')


def test_add_new_pet_with_photo_with_valid_data():
    """ Проверяем запрос добавление питомца с фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key,
                                                      name='Микси',
                                                      animal_type='заяц',
                                                      age='2',
                                                      pet_photo='images\wild-rabbit.jpg')

    assert status == 200
    assert result['name'] == 'Микси'
    assert result['animal_type'] == 'заяц'
    assert result['age'] == '2'
    assert result['pet_photo'] != ''


def test_update_information_about_first_pet_in_list_of_my_pets_with_valid_data():
    """ Проверяем запрос обновление информации у первого питомца """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]

    if len(list_of_my_pets["pets"]) > 0:
        id_of_first_pet = list_of_my_pets["pets"][0]["id"]
        status, result = pf.update_information_about_pet(auth_key,
                                                         pet_id=id_of_first_pet,
                                                         name='V',
                                                         animal_type='vvv',
                                                         age='1')

        assert status == 200
        assert result['id'] == id_of_first_pet
        assert result['name'] == 'V'
        assert result['animal_type'] == 'vvv'
        assert result['age'] == '1'
    else:
        raise Exception('У вас нет добавленных питомцев')


def test_update_information_about_first_pet_in_list_of_my_pets_with_invalid_pet_id():
    """ Проверяем запрос обновление информации у первого питомца с invalid_pet_id """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]

    if len(list_of_my_pets["pets"]) > 0:
        status, result = pf.update_information_about_pet(auth_key,
                                                         pet_id='invalid_pet_id',
                                                         name='Шнурок',
                                                         animal_type='луговой',
                                                         age='7')

        assert status == 400
        assert "Pet with this id wasn't found!" in result
    else:
        raise Exception('У вас нет добавленных питомцев')


def test_delete_first_pet_in_list_of_me_pets_from_database():
    """Проверяем возможность удаления первого питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    list_of_my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')[1]

    if len(list_of_my_pets["pets"]) > 0:
        id_of_first_pet = list_of_my_pets["pets"][0]["id"]
        status, result = pf.delete_pet_from_database(auth_key,
                                                     pet_id=id_of_first_pet)

        assert status == 200
        assert result == ''
        my_pets_list = pf.get_list_of_pets(auth_key, filter="my_pets")[1]["pets"]
        for pet in range(len(my_pets_list)):
            assert id_of_first_pet not in my_pets_list[pet].values()
    else:
        raise Exception('У вас нет добавленных питомцев')

def test_add_new_pet_without_photo_with_no_name():
    """ Проверяем запрос добавление питомца без фото и без имени """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = ''
    animal_type = 'кролик'
    age = '3'
    status, result = pf.add_information_about_new_pet_without_photo(auth_key,
                                                                    name=name,
                                                                    animal_type=animal_type,
                                                                    age=age)

    assert status == 400
    assert "Parameter 'name' cannot be none." in result
