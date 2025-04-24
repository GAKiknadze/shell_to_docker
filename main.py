import docker
import termios
import sys
import tty
import os
import select

def interactive_shell(client: docker.DockerClient):
    container = client.containers.run("ubuntu", detach=True, tty=True)
    
    container.reload()
    
    exec_id = client.api.exec_create(
        container.id,
        "sh -c 'exec /bin/sh -l'",
        tty=True,
        stdin=True,
        stdout=True,
        stderr=True,
    )['Id']
    sock = client.api.exec_start(
        exec_id,
        socket=True,
        tty=True,
        demux=False
    )
    oldtty = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    
    try:
        print("Добро пожаловать")
        while True:
            r, w, e = select.select([sock, sys.stdin], [], [])
            
            if sock in r:
                try:
                    data = sock.read(1024)
                    if not data:
                        break
                    sys.stdout.write(data.decode())
                    sys.stdout.flush()
                except KeyboardInterrupt:
                    break

            if sys.stdin in r:
                data = os.read(sys.stdin.fileno(), 1024)
                if not data:
                    break
                sock._sock.send(data)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        sock.close()
        container.stop()
        container.remove()

if __name__ == "__main__":
    client = docker.from_env()
    interactive_shell(client)
