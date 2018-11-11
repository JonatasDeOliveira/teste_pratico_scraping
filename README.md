# teste_pratico_scraping

Projeto de um Crawler para o Mercado Livre (mercadolivre.com.br), com o objetivo de um teste prático para startup Intelivix.

## Arquitetura 

Foi utlizado o Scrapy para realizar o crawler, utilizando uma spider com parsers diferentes para cada página do site.

## Executando

Para executar basta executar os comandos através do diretório principal:
```
$ cd MercadoLivreScraping
$ mkdir MercadoLivreScraping/data
$ scrapy runspider MercadoLivreScraping/spiders/MercadoLivre.py
```

## Autores

Este Crawler foi desenvolvido por:
**Jônatas de Oliveira Clementino** - joc@cin.ufpe.br
