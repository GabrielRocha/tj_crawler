from crawler_api.crawlers.base import BaseCrawler


class TJALCrawler(BaseCrawler):
    urls = (
        (
            'https://www2.tjal.jus.br/cpopg/search.do?'
            'cbPesquisa=NUMPROC&dadosConsulta.tipoNuProcesso=UNIFICADO&dadosConsulta.valorConsulta={number}'
        ),
        (
            'https://www2.tjal.jus.br/cposg5/search.do?'
            'cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&dePesquisaNuUnificado={number}'
        )
    )

    def parse(self, data):
        details = self.parse_legal_process_detail(data.xpath("//table[@class='secaoFormBody'][ @id='']")[0])
        return details

    def parse_legal_process_detail(self, data):
        class_ = data.xpath(".//tr[td[label[contains(text(), 'Classe')]]]/td[2]//span//span/text()").get()
        area = data.xpath(".//tr/td[span[contains(text(), 'Área:')]]/text()[2]").get()
        subject = data.xpath(".//tr[td[label[contains(text(), 'Assunto')]]]/td[2]//span/text()").get()
        distribution = data.xpath(".//tr[td[label[contains(text(), 'Distribuição')]]]/td[2]//span/text()").get()
        judge = data.xpath(".//tr[td[label[contains(text(), 'Juiz')]]]/td[2]//span/text()").get()
        value = data.xpath(".//tr[td[label[contains(text(), 'Valor da ação')]]]/td[2]//span/text()").get()
        return {
            "class": class_,
            "area": area and area.strip(),
            "subject": subject,
            "distribution": distribution,
            "judge": judge,
            "value": value and value.replace("  ", "")
        }
