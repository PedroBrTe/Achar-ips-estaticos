import threading
import subprocess
import time

ips = []
threads = []

tempo = time.time()

def pingar(ip: str):
    p = subprocess.run(f'ping {ip}', shell=True, capture_output=True, text=True)
    resultado = p.stdout

    print(f'Pingando: {ip}')

    if 'Host de destino inacess' in resultado or 'Esgotado o tempo limite do pedido.' in resultado or '100%' in resultado:
        pass
    else:
        ips.append(f'''{ip}
                    (
                    {resultado}
                    )''')

base_ip: str = input('Digite a base do seu IP (ex: 192.168.1): ')

octets = base_ip.split('.')
if base_ip == '' or len(octets) < 2 or len(octets) > 4:
    raise Exception('Passe uma base de IP válida')

if len(octets) == 1:
    for i in range(1, 256):
        for j in range(1, 256):
            for k in range(1, 256):
                ip = f"{base_ip}.{i}.{j}.{k}"
                t = threading.Thread(target=pingar, args=(ip,))
                t.daemon = True
                threads.append(t)

elif len(octets) == 2:
    for i in range(1, 256):
        for j in range(1, 256):
            ip = f"{base_ip}.{i}.{j}"
            t = threading.Thread(target=pingar, args=(ip,))
            t.daemon = True
            threads.append(t)

elif len(octets) == 3:
    for i in range(1, 256):
        ip = f"{base_ip}.{i}"
        t = threading.Thread(target=pingar, args=(ip,))
        t.daemon = True
        threads.append(t)

else:
    raise Exception('Passe uma base de IP válida')

tamanho_pacote = 255
num_pacotes = (len(threads) - 1) // tamanho_pacote + 1

for indice_pacote in range(num_pacotes):
    inicio_pacote = indice_pacote * tamanho_pacote
    fim_pacote = min((indice_pacote + 1) * tamanho_pacote, len(threads))
    pacote_threads = threads[inicio_pacote:fim_pacote]

    for thread in pacote_threads:
        thread.start()

    for thread in pacote_threads:
        thread.join()


final = '\n'.join(ips)

with open('ips.txt', 'w+') as file:
    file.write(final)
    file.write(f'\n{len(ips) - 1}')

print(f'Demorou: {time.time() - tempo}s')
