all:
	gcc wysinwyg.c -o wysinwyg -masm=intel -O0 -Wno-unused-result
	strip --strip-all wysinwyg
	mv wysinwyg ../distfiles
