import RPi.GPIO as GPIO
from spidev import SpiDev
import time
from db_handler import DBHandler
from schemas import PWLogData
import datetime
from pytz import timezone
from db_session import SessionLocal

"""
  complete GPIO-PIN assignment:
  PIN2=5V BREADBOARD
  PIN4=5V RELAY
  PIN6=GROUND BREADBOARD
  PIN9=GROUND RELAY
  PIN19=ADC DIN
  PIN21=ADC DOUT
  PIN23=ADC CLK
  PIN24=ADC CS/SHDN
"""

# declarations for GPIO pin assignments
ADC_CHIP_SELECT = 24
RELAY1 = 11


class MCP3008:
    def __init__(self, bus=0, device=0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000

    def read(self, channel=0):
        __adc = self.spi.xfer2([1, (0x18 + channel) << 4, 0])
        data = ((__adc[1] & 3) << 8) + __adc[2]
        return data

    def close(self):
        self.spi.close()


class GPIOHandler:
    def __init__(self):
        self.adc = MCP3008()
        self.db_handler = DBHandler()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(RELAY1, GPIO.OUT)
        GPIO.setup(ADC_CHIP_SELECT, GPIO.OUT)
        self.__write_log("START", "GPIO handler starts running")

    def __del__(self):
        self.__write_log("STOP", "GPIO handler stops running")
        GPIO.cleanup()

    def __write_log(self, status_type: str, message: str):
        current_utc_time = datetime.datetime.now(timezone('UTC'))
        current_utc_string = current_utc_time.strftime('%Y-%m-%d %H:%M:%S.%f %Z')                       
        logging_data = PWLogData(
            id=-1,
            time_stamp=current_utc_string,
            status_type=status_type,
            message=message,
        )
        self.db_handler.add_log(logging_data, SessionLocal())

    def __read_data(self) -> float:
        GPIO.output(ADC_CHIP_SELECT, GPIO.LOW)
        ch0_data = self.adc.read(channel=0)
        GPIO.output(ADC_CHIP_SELECT, GPIO.HIGH)
        return ch0_data * 5 / 1024.0  # returns value in volt

    def __do_watering(self, relay_no: int, duration: float):
        GPIO.output(relay_no, False)
        self.__write_log("PUMP_ON", f"Relay {relay_no} turned on")
        time.sleep(duration)
        GPIO.output(relay_no, True)
        self.__write_log("PUMP_OFF", f"Relay {relay_no} turned off")

    def do_routine(self):
        measurements = 5
        voltage_sum = 0

        for i in range(measurements):
            voltage_sum += self.__read_data()
        voltage_avg = (voltage_sum/measurements)

        self.__write_log("DATA", f"Measured moisture: {voltage_avg:.2f}")
        if voltage_avg > 2.7:
            self.__do_watering(RELAY1, 4)
