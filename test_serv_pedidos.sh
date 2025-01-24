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

# roda cliente de estoque
terminator -e "source env_py/bin/activate; 
zsh -c '
{
  printf \"P 10 produto1\n\";
  printf \"P 15 produto2\n\";
  printf \"P 5 produto 3 com espaço\n\";
  
  sleep 1;
} | make run_cli_estoque arg1=localhost:12345 2>&1;
exec zsh
'"

terminator -e "
source env_py/bin/activate; 
zsh -c 'make run_serv_pedidos arg1=54321 arg2=localhost:12345; 
exec zsh'" &

sleep 3 # wait to compile the stubs and start the server

# roda cliente de estoque. Comandos executaods automaticamente e saida salva em cli_estoque.log
EXPECTED_LOG="expected_pedidos.log"
cat << EOF > $EXPECTED_LOG
1 10 produto1
2 15 produto2
3 5 produto 3 com espaço
1 0
2 -1
4 -2
1 0
0
-1
3 1
EOF

# Run the stock client and save its output
CLI_LOG="cli_pedidos.log"
terminator -e "source env_py/bin/activate; 
zsh -c '
{
  echo -e \"Iniciando teste de pedidos. Comandos a serem executados estão abaixo nos comandos de printf\" >&2;
  printf \"P 1 1 2 50 4 1\n\";
  printf \"P 1 1\n\";
  printf \"X 2\n\";
  printf \"X 5\n\";
  printf \"T\n\";
  
  sleep 1;
} | make run_cli_pedidos arg1=localhost:12345 arg2=localhost:54321 > $CLI_LOG 2>&1;
exec zsh
'"

# Compare the files and output the result
sleep 1
echo "Comparing client output with expected log:"
if diff $CLI_LOG $EXPECTED_LOG > diff_output_pedidos.log; then
  echo "PASS: Output matches expected log."
else
  echo "FAIL: Output differs. See diff_output_pedidos.log for details."
  cat diff_output_pedidos.log
fi