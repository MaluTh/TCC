from requests import get
from json import loads
from pymongo import MongoClient
import datetime


class ImportData:
    # função onde são definidas as métricas que serão coletadas, depois cria-se uma coleção
    # em um banco de dados e, por fim, chama-se as duas funções que farão a coleta e que irão
    # gerar o arquivo csv
    def __init__(self):
        print('Coletando dados...')

        metrics = [
            'container_cpu_usage_seconds_total',
            'container_memory_usage_bytes',
            'container_fs_reads_bytes_total',
            'container_fs_writes_bytes_total',
            'container_network_receive_bytes_total',
            'container_network_transmit_bytes_total'
        ]

        client = MongoClient(host='mongodb').prometheus.containers

        self.prometheus2mongo(metrics, client)
        self.mongo2csv(metrics, client)

    # função que fará a coleta dos dados no Prometheus, através de uma URL e, posteriormente,
    # armazenará esta coleta na coleção do banco de dados criada na função anterior
    def prometheus2mongo(self, metrics, client, start_time=None, end_time=None):
        prefix = 'http://prometheus.sj.ifsc.edu.br/api/v1/query_range?query='
        if end_time:
            end = end_time
        else:
            end_datetime = datetime.datetime.now()
            end = str(end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if start_time:
            start = start_time
        else:
            start_datetime = end_datetime - datetime.timedelta(seconds=1800)
            start = str(start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))

        step = '1h'

        client.drop()

        for metric in metrics:
            url = prefix + metric + '&start=' + start + '&end=' + end + '&step=' + step
            response = get(url).text
            try:
                result = loads(response)['data']['result']
            except:
                print("Métrica com problema: " + metric)
            else:
                for item in result:
                    for value in item['values']:
                        document = {}
                        try:
                            document['metric'] = item['metric']['__name__']
                            document['name'] = item['metric']['id']
                            document['namespace'] = item['metric']['namespace']
                            document['timestamp'] = value[0]
                            document['value'] = value[1]
                        except:
                            pass
                        else:
                            if metric == 'container_network_receive_bytes_total' or metric == 'container_network_transmit_bytes_total':
                                if item['metric']['interface'] == 'eth0':
                                    client.insert_one(document)
                            else:
                                client.insert_one(document)

    # esta função irá acessar a coleção banco para ter acesso aos dados, depois fará
    # a normalização desses novos dados e, por fim, irá gerar o arquivo csv
    def mongo2csv(self, metrics, client):
        query = {}
        keys = {"_id": False, "name": True,
                "namespace": True, "timestamp": True}
        cursor = client.find(query, keys)

        containers = set()
        for item in cursor:
            containers.add(item['name'] + ',' +
                           item['namespace'] + ',' + str(item['timestamp']))

        output = open('data/plugins/MaluTh/tcc/nova_saida.csv', 'w')
        output.write('pod,namespace,timestamp')
        for metric in metrics:
            output.write(',' + metric)
        output.write('\n')

        counter = 0
        for container in containers:
            name, namespace, timestamp = container.split(',')
            csv = str(counter) + ',' + namespace + ',' + timestamp
            keys = {"_id": False, "value": True}
            for metric in metrics:
                query = {"name": name, "timestamp": int(
                    timestamp), "metric": metric}
                cursor = client.find_one(query, keys)
                if cursor:

                    if metric == 'container_cpu_usage_seconds_total':
                        teste = float(cursor['value'])/571271.996154514
                        if teste > 1:
                            csv += ',' + str(1)
                        else:
                            csv += ',' + str(teste)

                    elif metric == 'container_memory_usage_bytes':
                        teste = float(cursor['value'])/12707532800
                        if teste > 1:
                            csv += ',' + str(1)
                        else:
                            csv += ',' + str(teste)

                    elif metric == 'container_fs_reads_bytes_total':
                        teste = float(cursor['value'])/1372745728
                        if teste > 1:
                            csv += ',' + str(1)
                        else:
                            csv += ',' + str(teste)

                    elif metric == 'container_fs_writes_bytes_total':
                        teste = float(cursor['value'])/54412820480
                        if teste > 1:
                            csv += ',' + str(1)
                        else:
                            csv += ',' + str(teste)

                    elif metric == 'container_network_receive_bytes_total':
                        teste = float(cursor['value'])/177387492901
                        if teste > 1:
                            csv += ',' + str(1)
                        else:
                            csv += ',' + str(teste)

                    elif metric == 'container_network_transmit_bytes_total':
                        teste = float(cursor['value'])/176517691053
                        if teste > 1:
                            csv += ',' + str(1)
                        else:
                            csv += ',' + str(teste)

                    else:
                        csv += ',' + cursor['value']
                else:
                    csv += ','
            output.write(csv + '\n')
            counter += 1
        output.close()
