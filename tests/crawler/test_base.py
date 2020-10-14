import os
from unittest.mock import Mock

import pytest
from asynctest import CoroutineMock, call
from parsel import Selector

from crawler_api.crawlers.base import BaseCrawler, BaseSoftplanTJCrawler


@pytest.fixture
def fake_crawler():
    class FakeCrawler(BaseCrawler):
        urls = ['localhost/{id}', '127.0.0.1/{id}']
        parse = Mock()
    session = CoroutineMock()
    session.get.return_value.__aenter__.return_value.text = CoroutineMock(return_value='<html><h1>Test</h1></html>')
    return FakeCrawler(session)


@pytest.fixture
def softplan_crawler():
    return BaseSoftplanTJCrawler(Mock())


@pytest.fixture
def softplan_updates():
    path = os.path.dirname(__file__)
    with open(f'{path}/fixtures/softplan_updates.html') as f:
        return Selector(text=f.read()).css("tbody")[0]


@pytest.fixture
def softplan_parties_involved_html():
    path = os.path.dirname(__file__)
    with open(f'{path}/fixtures/softplan_parties_involved.html') as f:
        return Selector(text=f.read()).css("table")[0]


@pytest.mark.asyncio
async def test_session_call_on_execute(fake_crawler):
    await fake_crawler.execute(id=123)
    calls = [call('localhost/123'), call('127.0.0.1/123')]
    fake_crawler.session.get.assert_has_calls(calls, any_order=True)


@pytest.mark.asyncio
async def test_session_call_on_execute_with_multiple_kwargs(fake_crawler):
    fake_crawler.urls = ['localhost/{id}/{name}', '127.0.0.1/{id}']
    await fake_crawler.execute(id=123, name='987')
    calls = [call('localhost/123/987'), call('127.0.0.1/123')]
    fake_crawler.session.get.assert_has_calls(calls, any_order=True)


@pytest.mark.asyncio
async def test_parser_call_for_each_request_on_execute(fake_crawler):
    await fake_crawler.execute(id=123, name='987')
    args1, args2 = fake_crawler.parse.call_args_list
    assert isinstance(args1[0][0], Selector)
    assert args1[0][0].get(), '<html><h1>Test</h1></html>'
    assert isinstance(args2[0][0], Selector)
    assert args2[0][0].get(), '<html><h1>Test</h1></html>'


def test_type_error_when_create_a_instance_without_implement_abstract_method():
    class FakeCrawler(BaseCrawler):
        urls = ['localhost/{id}', '127.0.0.1/{id}']
    with pytest.raises(TypeError) as error:
        FakeCrawler(Mock())
    assert str(error.value) == "Can't instantiate abstract class FakeCrawler with abstract methods parse"


def test_raise_exception_for_parse_method():
    with pytest.raises(NotImplementedError):
        BaseCrawler.parse(Mock(), "")


@pytest.mark.asyncio
async def test_return_of_execute(fake_crawler):
    fake_crawler.parse = Mock(side_effect=['One', 'Two'])
    result = await fake_crawler.execute(id=123, name='987')
    assert list(result) == ['One', 'Two']


@pytest.mark.asyncio
async def test_execute_ignore_empty_results(fake_crawler):
    fake_crawler.parse = Mock(side_effect=['One', '', None, []])
    result = await fake_crawler.execute(id=123, name='987')
    assert list(result) == ['One']


def test_softplan_crawler_parse_parties_involved(softplan_crawler, softplan_parties_involved_html):
    result = softplan_crawler.parse_parties_involved(softplan_parties_involved_html)
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


def test_softplan_crawler_parse_parties_involved_return_empty_value(softplan_crawler):
    selector = Selector(text='<table id="tablePartesPrincipais"><tr><td></td><td></td></tr></table>')
    result = softplan_crawler.parse_parties_involved(selector)
    expected_result = [
        {
            'type': None,
            'name': None,
            'representatives': []
        }
    ]
    assert expected_result == result


def test_softplan_crawler_parse_parties_involved_xpath_not_found(softplan_crawler):
    selector = Selector(text='<table><tr><td></td><td></td></tr></table>')
    result = softplan_crawler.parse_parties_involved(selector)
    assert result == []


def test_softplan_crawler_parse_updates(softplan_crawler, softplan_updates):
    result = softplan_crawler.parse_updates(softplan_updates)
    expected_result = [
        {'date': '23/09/2020', 'description': 'Conclusos'},
        {'date': '16/08/2020', 'description': 'Visto em Autoinspeção   Despacho Visto em Autoinspeção'},
        {'date': '11/05/2020', 'description': 'Documento  Nº Protocolo: WMAC.20.70092549-0 Data: 11/05/2020 13:28'},
        {'date': '10/12/2019', 'description': 'Conclusos'},
    ]
    assert expected_result == result


def test_softplan_crawler_parse_updates_return_empty_value(softplan_crawler):
    selector = Selector(text='<table><tbody><tr><td></td><td></td></tr></tbody></table>')
    result = softplan_crawler.parse_updates(selector)
    assert result == []


def test_softplan_crawler_parse_updates_xpath_not_found(softplan_crawler):
    selector = Selector(text='<tbody id="tabelaTodasMovimentacoes"><tr><td></td><td></td></tr></tbody>')
    result = softplan_crawler.parse_updates(selector)
    expected_result = [{'date': None, 'description': ''}]
    assert expected_result == result
