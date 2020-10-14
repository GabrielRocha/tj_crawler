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
        details['parties_involved'] = self.parse_parties_involved(data.xpath('//table[@id="tableTodasPartes"]'))
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

    def parse_parties_involved(self, trs):
        parties_involved = []
        for tr in trs.css('tr'):
            td_label, td_value = tr.xpath('./td')
            type_ = td_label.xpath('./span/text()').get()
            td_value.xpath('br').remove()
            all_texts = list(map(lambda x: x and str(x).strip(), td_value.xpath('text()').getall()))
            all_types = list(map(lambda x: x and str(x).strip(), td_value.xpath('span/text()').getall()))
            representatives = [
                {
                    "type": item and item.replace(":", ""),
                    "name": all_texts[index]
                }
                for index, item in enumerate(all_types, start=1)
            ]
            item = {
                'type': type_ and type_.strip().replace(":", ""),
                'name': (all_texts and all_texts[0]) or None,
                "representatives": representatives
            }
            parties_involved.append(item)
        return parties_involved
