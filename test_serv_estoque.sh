#!/bin/bash

# PRA RODAR: (supondo nome do arquivo como test_serv_estoque.sh)
# chmod +x test_serv_estoque.sh
# ./test_serv_estoque.sh

# roda servidor de estoque
terminator -e "bash -c 'make run_serv_estoque arg1=12345; exec bash'" &

sleep 1

# roda cliente de estoque. Comandos executaods automaticamente e saida salva em cli_estoque.log
terminator -e "bash -c '
{
  echo -e \"Iniciando teste de estoque. Comandos a serem executados estão abaixo nos comandos de printf\" >&2;
  printf \"L\n\";
  printf \"P 10 produto1\n\";
  printf \"P 15 produto2\n\";
  printf \"P 15 produto2\n\";
  printf \"P 5 produto 3 com espaço\n\";
  printf \"L\n\";
  printf \"Q 1 3\n\";
  printf \"Q 2 -3\n\";
  printf \"Q 50 1\n\";
  printf \"Q 3 -10\n\";
  printf \"L\n\";
  printf \"F\n\";
  
  echo -e \"Saida deve ser:\" >&2;
  echo -e \" (linha vazia mesmo, listei sem ter nada) \" >&2;
  echo -e \"1 \" >&2;
  echo -e \"2 \" >&2;
  echo -e \"2 \" >&2;
  echo -e \"1 10 produto1 \" >&2;
  echo -e \"2 30 produto2 \" >&2;
  echo -e \"3 5 produto 3 com espaço\" >&2;
  echo -e \"13 (agora produto 1 tem 13 unidades) \" >&2;
  echo -e \"27 (agora produto 2 tem 27 unidades) \" >&2;
  echo -e \"-2 (não tem produto de id 50) \" >&2;
  echo -e \"-1 (produto 3 não tem 10 unidades)\" >&2;
  echo -e \"1 13 produto1 \" >&2;
  echo -e \"2 27 produto2 \" >&2;
  echo -e \"3 5 produto 3 com espaço\" >&2;
  echo -e \"3 (3 produtos no fim da execucao)\" >&2;
  echo -e \"Fim do teste de estoque\\n\" >&2;
  
  sleep 1;
} | make run_cli_estoque arg1=localhost:12345 > cli_estoque.log 2>&1;
cat cli_estoque.log;
exec bash
'"

