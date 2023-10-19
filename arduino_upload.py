from intelhex import IntelHex, AddressOverlapError, HexRecordError
from arduinobootloader import ArduinoBootloader


def uploadHex(port, hexPath, logOut=print):
    ih = IntelHex()
    ab = ArduinoBootloader()
    prg = ab.select_programmer("Stk500v1")
    try:
        if prg.open(port=port, speed=115200):
            if not prg.board_request():
                raise Exception(-1, "invalid_bootloader")
            logOut("bootloader", ab.programmer_name, ab.sw_version, ab.hw_version)
            if not prg.cpu_signature():
                raise Exception(-2, "invalid_cpu_name")
            logOut("cpu name: {}".format(ab.cpu_name))
            try:
                ih.fromfile(hexPath, format="hex")
            except (FileNotFoundError, AddressOverlapError, HexRecordError):
                raise Exception(-3, "hex_open_fail")
            for address in range(0, ih.maxaddr(), ab.cpu_page_size):
                logOut("flash %s/%s" %(address, ih.maxaddr()))
                buffer = ih.tobinarray(start=address, size=ab.cpu_page_size)
                if not prg.write_memory(buffer, address):
                    prg.leave_bootloader()
                    raise Exception(-4, "write_error")

            for address in range(0, ih.maxaddr(), ab.cpu_page_size):
                logOut("check %s/%s" %(address, ih.maxaddr()))
                buffer = ih.tobinarray(start=address, size=ab.cpu_page_size)
                read_buffer = prg.read_memory(address, ab.cpu_page_size)
                if read_buffer is None:
                    raise Exception(-5, "read_back_error")

                if buffer != read_buffer:
                    raise Exception(-6, "file_not_match")
            logOut("flash done! leaving bootloader~")
            prg.leave_bootloader()
        else:
            raise Exception(-99, "can not find board")
    except Exception as err:
        return (err.args[0], err.args[1])
    finally:
        try:
            prg.close()
        except:
            pass
    return (0, None)


if __name__ == "__main__":
    uploadHex("/dev/ttyAMA0","rosbot.hex")
