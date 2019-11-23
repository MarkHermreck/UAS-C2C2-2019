import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

while True:
    _, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if temperature is not None:
        print("Temp={0:0.1f}*C".format(temperature))
    else:
        print("Failed to retrieve data from humidity sensor")