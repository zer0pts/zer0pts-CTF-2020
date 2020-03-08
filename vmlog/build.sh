rm -rf distfiles
mkdir distfiles
cat challenge/flag | tr -d '\n' | python3 challenge/vm.py > distfiles/log.txt
cp challenge/vm.py distfiles/
