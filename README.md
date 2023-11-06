# udpstream

## Requisitos

- Implementar um servidor de streams UDP.
- Implementar um cliente de streams UDP.
- Natureza do stream: livre para escolha.
- O servidor deve ser capaz de atender múltiplos clientes simultaneamente.
- Deve ser possível configurar via linha de comando o intervalo de tempo em que cada mensagem do stream é transmitida.
- O número de campos é no mínimo 2, pois obrigatoriamente cada pacote informa sua ordem no stream, começando por 1.
- Ao encerrar o cliente ele deve produzir estatísticas sobre o uso do UDP: quantos pacotes foram perdidos e quantos chegaram fora de ordem.
- O cliente deve implementar uma operação sobre os dados recebidos. Exemplo: calcular a média dos valores recebidos.
- Devem ser apresentados logs para múltiplas execuções.
- Pelo menos uma das execuções deve ter obrigatoriamente 3 clientes recebendo o stream.
- Relatório de como foi feito o trabalho e quais foram os resultados obtidos em uma página HTML
- Na entrega:
  - link da página web.
  - Acrescente a todo programa a terminação ".txt" para ser possível visualizar o código fonte no navegador.
  - Logs de execução dos processos cliente/servidores, que demonstrem a execução correta destes processos.
