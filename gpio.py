
def gpio_setup(pin):
    open('/sys/class/gpio/export', 'w').write(str(pin))

def gpio_cleanup(pin):
    open('/sys/class/gpio/unexport', 'w').write(str(pin))

def gpio_read(pin):
    return int(open(f'/sys/class/gpio/gpio{pin}/value').read())
