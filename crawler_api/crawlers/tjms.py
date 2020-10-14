import re

from crawler_api.crawlers.base import BaseCrawler
from crawler_api.crawlers.helper import sanitize_string


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
        parties_involved = data.xpath('//table[@id="tableTodasPartes"]|//table[@id="tablePartesPrincipais"]')[-1]
        details['parties_involved'] = self.parse_parties_involved(parties_involved)
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

    def parse_parties_involved(self, trs):
        parties_involved = []
        for tr in trs.css('tr'):
            td_label, td_value = tr.xpath('./td')
            type_ = td_label.xpath('./span/text()').get()
            td_value.xpath('br').remove()

            all_types = map(sanitize_string, td_value.xpath('span/text()').getall())

            all_texts = map(sanitize_string, td_value.xpath('text()').getall())
            all_texts = list(filter(lambda x: x and True, all_texts))

            representatives = [
                {
                    "type": item and re.sub(':|&nbsp', '', item),
                    "name": all_texts[index]
                }
                for index, item in enumerate(filter(lambda x: x and True, all_types), start=1)
            ]
            item = {
                'type': type_ and type_.strip().replace(":", ""),
                'name': (all_texts and all_texts[0]) or None,
                "representatives": representatives
            }
            parties_involved.append(item)
        return parties_involved
