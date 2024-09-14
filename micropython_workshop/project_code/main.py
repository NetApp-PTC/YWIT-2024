def wifi_connect(interface):
    import network
    import time
    interface.active(True)
    print("Scanning for networks...")
    networks = interface.scan()
    for index, network in enumerate(networks):
        print("%s. %s" % (index + 1, network[0]))
    while True:
        try:
            network = input("Connect to which network? ")
            try:
                network = int(network) - 1
                if not 0 < network < len(networks):
                    network += 1
                    raise ValueError
            except ValueError:
                print("%s is not a valid choice" % network)
                continue
            network = networks[network][0]
            password = input("What's the password? ").strip()
            print("Connecting to %s..." % network)
            if password:
                interface.connect(network, password)
            else:
                interface.connect(network)
            tries = 10 # isconnected seems to need some time to become true
            while tries > 0:
                if not interface.isconnected():
                    tries -= 1
                    time.sleep(1)
                else:
                    print("Connected to %s successfully" % network)
                    break
            else:
                print("Failed to connect to %s. Is the password correct?" % network)
            break
        except KeyboardInterrupt:
            break

interface = network.WLAN(network.STA_IF)
if not interface.isconnected():
    wifi_connect(interface)
