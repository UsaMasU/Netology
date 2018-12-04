import requests

def translate_it(src_file, res_file, src_lang, res_lang = 'ru'):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    #key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    key = 'trnsl.1.1.20181204T195305Z.b262d9ab0b9188d9.cffda24c39d664eb46f86ce5364be598f6c80747'

    try:
        with open(src_file, encoding='utf8') as read_file:
            src_text = []
            for line in read_file:
                src_text.append(line)
    except FileNotFoundError:
        print('Нет файла')

    langs = [src_lang, res_lang]
    lang = '-'.join(langs)

    params = {
        'key': key,
        'lang': lang,
        'text': src_text,
    }

    response = requests.get(url, params=params).json()
    res_text = ''.join(response['text'])

    with open(res_file, 'w', encoding='utf8') as write_file:
        write_file.write(res_text)

    return ' '.join(response.get('text', []))

if __name__ == '__main__':
    print('\nВыполняется перевод...')
    de_ru = translate_it('DE.txt','DE-RU.txt', 'de', 'ru')
    es_ru = translate_it('ES.txt','ES_RU.txt', 'es', 'ru')
    fr_ru = translate_it('FR.txt','FR-RU.txt', 'fr', 'ru')
    print('Перевод выполнен!')