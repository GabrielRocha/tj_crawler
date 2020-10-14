from crawler_api.crawlers.base import BaseCrawler


class TJMSCrawler(BaseCrawler):
    urls = (
        (
            'https://esaj.tjms.jus.br/cpopg5/search.do?cbPesquisa=NUMPROC&'
            'dadosConsulta.tipoNuProcesso=UNIFICADO&dadosConsulta.valorConsulta={number}'
        ),
        (
            'https://esaj.tjms.jus.br/cposg5/search.do?cbPesquisa=NUMPROC&'
            'tipoNuProcesso=UNIFICADO&dePesquisaNuUnificado={number}'
        ),
    )

    def parse(self, data):
        div_header = data.xpath("//div[@class='unj-entity-header']")
        if not div_header:
            return
        details = self.parse_legal_process_detail(div_header)
        return details

    def parse_legal_process_detail(self, data):
        class_ = data.xpath(".//div[span[contains(text(), 'Classe')]]/div/span/text()").get()
        area = data.xpath(".//div[span[contains(text(), 'Área')]]/div/span/text()").get()
        subject = data.xpath(".//div[span[contains(text(), 'Assunto')]]/div/span/text()").get()
        distribution = data.xpath(".//div[span[contains(text(), 'Distribuição')]]/div/text()").get()
        judge = data.xpath(".//div[span[contains(text(), 'Juiz')]]/div/span/text()").get()
        value_div = data.xpath(".//div[span[contains(text(), 'Valor da ação')]]")
        value = value_div.xpath('./div/text()').get() or value_div.xpath('./div/span/text()').get()
        return {
            "class": class_,
            "area": area,
            "subject": subject,
            "distribution": distribution,
            "judge": judge,
            "value": value and value.replace("  ", "")
        }
