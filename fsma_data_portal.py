import scrapy
from datetime import datetime

class ManagerTransaction(scrapy.Spider):
    name = "ManagerTransaction"
    base_url = "https://www.fsma.be"
    start_urls = [
        f"{base_url}/en/data-portal?f%5B0%5D=fa_content_type%3Actmanagertransaction&f%5B1%5D=fa_content_type%3Actshortselling&f%5B2%5D=fa_mts_ct%3Actmanagertransaction&page=157"
    ]

    def parse_node_details(self, response):
        details = response.css(""".node--type-ct-manager-transaction""")
        yield {
            "date_of_publication":      details.css(".field--name-field-ct-date-time").css(".field__item::text").get(),
            "notifying_person":         details.css(".field--name-field-ct-declarer-name").css(".field__item::text").get(),
            "declarer_type":            details.css(".field--name-field-ct-declarer-type").css(".field__item::text").get(),
            "declarer_related_persons": details.css(".field--name-field-ct-description").css(".field__item::text").get(),
            "issuer":                   details.css(".field--name-field-ct-issuer").css(".field__item::text").get(),
            "instrument_type":          details.css(".field--name-field-ct-instrument-type").css(".field__item::text").get(),
            "instrument_isin_code":     details.css(".field--name-field-ct-instrument-isin-code").css(".field__item::text").get(),
            "transaction_type":         details.css(".field--name-field-ct-transaction-type").css(".field__item::text").get(),
            "transaction_place":        details.css(".field--name-field-ct-transaction-place").css(".field__item::text").get(),
            "transaction_date":         details.css(".field--name-field-ct-transaction-date").xpath(".//div[2]/time/@datetime").get(),
            "transaction_currency":     details.css(".field--name-field-ct-transaction-currency").css(".field__item::text").get(),
            "transaction_quantity":     details.css(".field--name-field-ct-transaction-quantity").css(".field__item::text").get(),
            "transaction_price":        details.css(".field--name-field-ct-price").css(".field__item::text").get(),
            "transaction_amount":       details.css(".field--name-field-ct-amount").css(".field__item::text").get(),
            "body":                     details.css(".field--name-field-ct-body").css(".field__item").xpath(".//p/text()").get(),
            "date_of_extraction":       str(datetime.now()),
            "url": response.url
        }


    def parse(self, response):
        transaction_links = response.css(".search-result-teaser__link")
        yield from response.follow_all(transaction_links, self.parse_node_details)


        for next_page in response.css(".pager__item--next").xpath(".//a"):
            yield response.follow(next_page, self.parse)
