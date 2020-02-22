
def setup(pin):
    open('/sys/class/gpio/export', 'w').write(str(pin))

def cleanup(pin):
    open('/sys/class/gpio/unexport', 'w').write(str(pin))

def read(pin):
    return int(open(f'/sys/class/gpio/gpio{pin}/value').read())
