Este repositório contém os arquivos utilizados para a contrução de uma ferramenta para análise de logs da nuvem privada de contêineres utilizada no Instituto Federal de Santa Catarina câmpus São José (IFSC/SJ). Esta ferrmaneta foi desenvolvida como forma de atender o objetivo proposto no Trabalho de Conclusão de Curso apresentado à Coordenadoria do Curso de Engenharia de Telecomunicações do IFSC/SJ para a obtenção do diploma de Engenheira de Telecomunicações.

# Como usar
Este é um _plugin_ do Errbot. Para instalar, recomenda-se [transferi-lo diretamente do GitHub](http://errbot.io/en/latest/user_guide/administration.html#installing-plugins).

Como há dependências específicas do _plugin_, como por exemplo PyBrain, é preciso estar ativado o suporte a autoinstalação de dependências. No arquivo de configuração (`config.py`) adicione a seguinte linha:
```python
AUTOINSTALL_DEPS = True
```
As dependências listadas no arquivo `requirements.txt` serão instaladas automaticamente. Caso o bot não recarregue o _plugin_, reinicie o bot direto via _chat_ através do comando `restart`.
