import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["biggeek.ru"]
    start_urls = [f"https://biggeek.ru/catalog/smartfony?page={i}" for i in range(1, 12)]

    def parse(self, response):
        heads = response.xpath('//div[@class="catalog-card"]')
        for head in heads:
            # yield {
            #     'url': 'https://biggeek.ru' + head.xpath('.//a/@href').get()
            # }
            link = ('https://biggeek.ru' + head.xpath('.//a/@href').get())
            yield scrapy.Request(url=link, callback=self.parse_product)

    #
    def parse_product(self, response):
        # Извлечение информации с карточки товара
        title = response.xpath('//h1[@class="produt-section__title cart-modal-title"]/text()').get()
        price = response.xpath('//span[@class="total-prod-price"]/text()').get()  # Примерный селектор для цены
        articul = response.xpath(
            '//span[@class="vendor-code"]/text()').get()  # Примерный селектор для описания
        params = response.xpath('//div[@class="tabs-content__txt-row"]')
        keys = []
        values = []
        for param in params:
            key = param.xpath('.//div[@class="descr"]/text()').get()
            value = param.xpath('.//div[@class="value"]/text()').get()
            if key and value:  # Убедимся, что описание не пустое
                keys.append(key.strip())  # Уберем лишние пробелы в параметре
                values.append(value.strip())  # Уберем лишние пробелы в параметрe
        # Создадим словарь из keys и values
        product_parameters = dict(zip(keys, values))
        # Преобразуем словарь в массив строк
        product_parameters_list = [f"{k}: {v}" for k, v in product_parameters.items()]


        # Возвращаем информацию в виде словаря и добавляем параметры
        yield {
            'title': title,
            'price': price,
            'articul': articul,
            'params': product_parameters_list,
            'url': response.url
        }
