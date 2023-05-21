import threading
import subprocess
import time

ips = []

threads = []

tempo = time.time()


def pingar(ip:int):
    p = subprocess.run(f'ping 192.168.1.{ip}', shell=True, capture_output = True, text=True)
    resultado = p.stdout
    
    print(f'Pingando: 192.168.1.{ip}')
    
    if 'Host de destino inacess' in resultado or 'Esgotado o tempo limite do pedido.' in resultado or '100%' in resultado:
        pass
    else:
        ips.append(f'''192.168.1.{ip}
                    (
                    {resultado}
                    )''')
    
    
for ip in range(1,256):
    # Cria as threads
    t = threading.Thread(target=pingar, args=(ip,))
    t.daemon = True
    threads.append(t)

for thread in threads:
    # Iniciando as threads
    thread.start()
    
for thread in threads:
    # Esperando elas acabarem
    thread.join()
    
final = '\n'.join(ips)

with open('ips.txt', 'w+') as file:
    file.write(final)
    file.write(f'\n {len(ips)-1}')
    
print(f'Demorou: {time.time() - tempo}s')