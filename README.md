# Como usar
Este é um _plugin_ do Errbot. Para instalar, recomenda-se [transferi-lo diretamente do GitHub](http://errbot.io/en/latest/user_guide/administration.html#installing-plugins).

Como há dependências específicas do _plugin_, como por exemplo PyBrain, é preciso estar ativado o suporte a autoinstalação de dependências. No arquivo de configuração (`config.py`) adicione a seguinte linha:
```python
AUTOINSTALL_DEPS = True
```
As dependências listadas no arquivo `requirements.txt` serão instaladas automaticamente. Caso o bot não recarregue o _plugin_, reinicie o bot direto via _chat_ através do comando `restart`.
