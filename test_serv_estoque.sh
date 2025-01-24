#!/bin/zsh

# PRA RODAR: (supondo nome do arquivo como test_serv_estoque.sh)
# chmod +x test_serv_estoque.sh
# ./test_serv_estoque.sh


# roda servidor de estoque
terminator -e "
source env_py/bin/activate; 
zsh -c 'make run_serv_estoque arg1=12345; 
exec zsh'" &

sleep 3 # wait to compile the stubs and start the server

# roda cliente de estoque. Comandos executaods automaticamente e saida salva em cli_estoque.log
EXPECTED_LOG="expected_estoque.log"
cat << EOF > $EXPECTED_LOG
1
2
2
3
1 10 produto1
2 30 produto2
3 5 produto 3 com espaço
13
27
-2
-1
1 13 produto1
2 27 produto2
3 5 produto 3 com espaço
3
EOF

# Run the stock client and save its output
CLI_LOG="cli_estoque.log"
terminator -e "source env_py/bin/activate; 
zsh -c '
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
  
  sleep 1;
} | make run_cli_estoque arg1=localhost:12345 > $CLI_LOG 2>&1;
exec zsh
'"

# Compare the files and output the result
sleep 1
echo "Comparing client output with expected log:"
if diff $CLI_LOG $EXPECTED_LOG > diff_output_estoque.log; then
  echo "PASS: Output matches expected log."
else
  echo "FAIL: Output differs. See diff_output_estoque.log for details."
  cat diff_output_estoque.log
fi