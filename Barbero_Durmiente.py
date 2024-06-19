
### version con sincronizacion

import threading
import time
import random

class BarberShop:
    def __init__(self, num_chairs,num_customers):
        self.num_chairs = num_chairs
        self.waiting_customers = 0
        self.barber_ready = threading.Semaphore(0)
        self.customer_ready = threading.Semaphore(0)
        self.mutex = threading.Lock()
        self.total = 0
        self.num_customers = num_customers

    def open_shop(self):
        while True:
            self.customer_ready.acquire()  # Esperar a que llegue un cliente
            self.mutex.acquire()
            self.waiting_customers -= 1 
            self.mutex.release()
            self.barber_ready.release()  # Avisar al barbero que hay un cliente listo
            self.cut_hair()  # Cortar el cabello del cliente
            if(self.total == self.num_customers):
                break

    def cut_hair(self):
        print("El barbero está cortando el cabello")
        time.sleep(random.uniform(0.5, 1.5))
        self.total += 1
        print("El barbero ha terminado de cortar el cabello")

    def enter_shop(self, customer_id):
        self.mutex.acquire()
        if self.waiting_customers < self.num_chairs:
            self.waiting_customers += 1
            print(f"Cliente {customer_id} está esperando")
            self.customer_ready.release()  # Avisar al barbero que hay un cliente
            self.mutex.release()
            self.barber_ready.acquire()  # Esperar a que el barbero esté listo
            print(f"Cliente {customer_id} está siendo atendido")
        else:
            print(f"Cliente {customer_id} se va porque no hay sillas disponibles")
            self.mutex.release()

def customer(barber_shop, customer_id):
    while True:
        time.sleep(random.uniform(1, 3))
        barber_shop.enter_shop(customer_id)
        # Si el cliente es atendido, salir del bucle
        if barber_shop.waiting_customers < barber_shop.num_chairs:
            break

if __name__ == "__main__":
    num_chairs = 2
    num_customers = 6  # Número de clientes a ser atendidos
    barber_shop = BarberShop(num_chairs, num_customers)
    barber_t = threading.Thread(target=barber_shop.open_shop).start()

    customer_threads = []
    for i in range(num_customers):
        t = threading.Thread(target=customer, args=(barber_shop, i))
        t.start()
        customer_threads.append(t)

    for t in customer_threads:
        t.join()  # Esperar a que todos los clientes sean atendidos
        
    
        
        
### Version sin Sincronizacion 

''' 
import threading
import time
import random

class BarberShop:
    def __init__(self, num_chairs, max_customers):
        self.num_chairs = num_chairs
        self.waiting_customers = []
        self.customers_served = 0
        self.max_customers = max_customers
        self.shop_open = True

    def enter_shop(self, customer_id):
        if self.customers_served >= self.max_customers:
            self.shop_open = False
            return False
        if len(self.waiting_customers) < self.num_chairs:
            self.waiting_customers.append(customer_id)
            print(f"Cliente {customer_id} se sienta en la sala de espera. {len(self.waiting_customers)}/{self.num_chairs} sillas ocupadas.")
            return True
        else:
            print(f"Cliente {customer_id} se va porque no hay sillas disponibles.")
            return False

    def get_next_customer(self):
        if self.waiting_customers:
            customer_id = self.waiting_customers.pop(0)
            print(f"El barbero comienza a atender al cliente {customer_id}.")
            return customer_id
        else:
            return None

def barber(shop):
    while shop.shop_open or shop.waiting_customers:
        customer_id = shop.get_next_customer()
        if customer_id is not None:
            print(f"El barbero está cortando el cabello del cliente {customer_id}.")
            time.sleep(random.uniform(0.5, 2))  # Tiempo para cortar el cabello
            print(f"El barbero ha terminado con el cliente {customer_id}.")
            shop.customers_served += 1
            if shop.customers_served >= shop.max_customers:
                shop.shop_open = False
        else:
            if shop.shop_open:
                print("El barbero está durmiendo.")
                time.sleep(1)  # El barbero duerme por un tiempo antes de verificar nuevamente

def customer(shop, customer_id):
    if shop.enter_shop(customer_id):
        while customer_id in shop.waiting_customers:
            time.sleep(0.1)  # Espera hasta que sea atendido
        print(f"Cliente {customer_id} está siendo atendido y luego se va.")
    else:
        print(f"Cliente {customer_id} se ha ido sin ser atendido.")

if __name__ == "__main__":
    num_chairs = 3
    max_customers = 5
    shop = BarberShop(num_chairs, max_customers)

    barber_thread = threading.Thread(target=barber, args=(shop,))
    barber_thread.start()

    customer_id = 1
    while shop.shop_open:
        time.sleep(random.uniform(0.1, 1))  # Tiempo entre la llegada de clientes
        threading.Thread(target=customer, args=(shop, customer_id)).start()
        customer_id += 1

    barber_thread.join()
    print("La barbería ha cerrado después de atender al número máximo de clientes.")

'''











