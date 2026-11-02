from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology():
    net = Mininet(controller=None, switch=OVSSwitch)

    c1 = net.addHost('c1', ip='10.0.0.1/24')
    c2 = net.addHost('c2', ip='10.0.0.2/24')
    c3 = net.addHost('c3', ip='10.0.0.3/24')

    s1 = net.addHost('hserver1', ip='10.0.0.4/24')
    s2 = net.addHost('hserver2', ip='10.0.0.5/24')

    sw1 = net.addSwitch('sw1', protocols='OpenFlow13')

    net.addLink(c1, sw1)
    net.addLink(c2, sw1)
    net.addLink(c3, sw1)
    net.addLink(s1, sw1)
    net.addLink(s2, sw1)

    net.addController('c0', controller=RemoteController,
                      ip='127.0.0.1', port=6653)

    net.start()
    print("*** Network started")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
