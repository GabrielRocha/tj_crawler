import os

import pytest
from asynctest import Mock
from parsel import Selector

from crawler_api.crawlers import TJALCrawler
from crawler_api.crawlers.base import BaseCrawler


@pytest.fixture
def tjal_result_html():
    path = os.path.dirname(__file__)
    with open(f'{path}/fixtures/tjal.html') as f:
        return Selector(text=f.read())


@pytest.fixture
def tjal_parties_involved_html():
    path = os.path.dirname(__file__)
    with open(f'{path}/fixtures/tjal_parties_involved.html') as f:
        return Selector(text=f.read()).css("table")[0]


@pytest.fixture
def tjal_detail_html():
    path = os.path.dirname(__file__)
    with open(f'{path}/fixtures/tjal_detail_legal_process.html') as f:
        return Selector(text=f.read()).css("table")[0]


@pytest.fixture
def tjal_crawler():
    return TJALCrawler(Mock())


def test_tjalcrawler_subclass():
    assert issubclass(TJALCrawler, BaseCrawler)


def test_tjalcrawler_parse_legal_process_detail(tjal_crawler, tjal_detail_html):
    result = tjal_crawler.parse_legal_process_detail(tjal_detail_html)
    expected_result = {
        'class': 'Procedimento Comum Cível',
        'area': 'Cível',
        'subject': 'Dano Material',
        'distribution': '02/05/2018 às 19:01 - Sorteio',
        'judge': 'José Cícero Alves da Silva',
        'value': 'R$ 281.178,42'
    }
    assert expected_result == result


def test_tjalcrawler_parse_legal_process_detail_return_empty_value(tjal_crawler):
    result = tjal_crawler.parse_legal_process_detail(Selector(text='<html></html>'))
    expected_result = {
        'class': None,
        'area': None,
        'subject': None,
        'distribution': None,
        'judge': None,
        'value': None
    }
    assert expected_result == result


def test_tjalcrawler_parse_parties_involved(tjal_crawler, tjal_parties_involved_html):
    result = tjal_crawler.parse_parties_involved(tjal_parties_involved_html)
    expected_result = [
        {
            'type': 'Autor',
            'name': 'José Carlos Cerqueira Souza Filho',
            'representatives': [
                {
                    'type': 'Advogado',
                    'name': 'Vinicius Faria de Cerqueira'
                }
            ]
        },
        {
            'type': 'Ré',
            'name': 'Cony Engenharia Ltda.',
            'representatives': [
                {
                    'type': 'Advogado',
                    'name': 'Marcus Vinicius Cavalcante Lins Filho'
                },
                {
                    'type': 'Advogado',
                    'name': 'Thiago Maia Nobre Rocha'
                },
            ]
        },
    ]
    assert expected_result == result


def test_tjalcrawler_parse_parties_involved_return_empty_value(tjal_crawler):
    selector = Selector(text='<table><tbody><tr><td></td><td></td></tr></tbody></table>')
    result = tjal_crawler.parse_parties_involved(selector)
    expected_result = [
        {
            'type': None,
            'name': None,
            'representatives': []
        }
    ]
    assert expected_result == result


def test_tjalcrawler_parse(tjal_crawler, tjal_result_html):
    result = tjal_crawler.parse(tjal_result_html)
    expected_result = {
        'class': 'Procedimento Comum Cível',
        'area': 'Cível',
        'subject': 'Dano Material',
        'distribution': '02/05/2018 às 19:01 - Sorteio',
        'judge': 'José Cícero Alves da Silva',
        'value': 'R$ 281.178,42',
        'parties_involved': [
            {
                'type': 'Autor',
                'name': 'José Carlos Cerqueira Souza Filho',
                'representatives': [
                    {
                        'type': 'Advogado',
                        'name': 'Vinicius Faria de Cerqueira'
                    }
                ]
            },
            {
                'type': 'Ré',
                'name': 'Cony Engenharia Ltda.',
                'representatives': [
                    {
                        'type': 'Advogado',
                        'name': 'Marcus Vinicius Cavalcante Lins Filho'
                    },
                    {
                        'type': 'Advogado',
                        'name': 'Thiago Maia Nobre Rocha'
                    },
                ]
            },
        ]
    }
    assert expected_result == result
