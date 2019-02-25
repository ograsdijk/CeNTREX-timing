from spinapi import *

class PulseBlaster:
    def __init__(self, time_offset, board_number, clock):
        self.time_offset = time_offset
        self.board_number = board_number
        self.clock = clock

        self.verification_string = self.description()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return

    def description(self):
        try:
            pb_select_board(board_number)
            pb_init()
            pb_core_clock(self.clock)
            pb_close()
            return pb_get_firmware_id()
        except RuntimeError as e:
            logging.warning(e)
            return False

    def connect(self):
        try:
            pb_select_board(self.board_number)
            pb_init()
        except RuntimeError as e:
            logging.warning(e)
            return False
        try:
            pb_core_clock(self.clock)
        except RuntimeError as e:
            logging.warning(e)
            self.disconnect()
            return False
        return True

    def disconnect(self):
        try:
            pb_close()
        except RuntimeError as e:
            logging.warning(e)
            return False
        return True

    def ProgramSequenceList(self, sequence):
        if not self.connect():
            return

        if not isinstance(sequence, list):
            logging.warning('sequence needs to be a list')
            return
        if not len(sequence) >= 2:
            logging.warning('need at least two instructions')
            return

        pb_start_programming(PULSE_PROGRAM)
        for seq in sequence:

            flags = seq[0]
            if (isinstance(flags, list)) or (isinstance(flags, tuple)):
                flags = sum([2**b for b in flags])
            elif isinstance(flags, str):
                if flags == 'ALL':
                    flags = 0xFFFFF
                elif flags = 'NONE':
                    flags = 0x0
                else:
                    logging.warning('flags string invalid: ALL or NONE')
                    self.disconnect()
                    return
            else:
                logging.warning('flags requires a list, tuple or string')
                self.disconnect()
                return

            opcode = seq[1]
            if (isinstance(opcode, str)):
                opcode = eval(opcode)
            else:
                logging.warning('opcode requires a string')
                self.disconnect()
                return

            opcode_data = seq[2]:
            if not isinstance(opcode_data, int):
                logging.warning('opcode_data requires integer')
                self.disconnect()
                return

            length = seq[3]
            if not (isinstance(length, str) or isinstance(lenght, float)):
                logging.warning('lenght requires string or integer')
                self.disconnect()
                return
            else:
                if isinstance(length, str):
                    try:
                        length = eval(length)
                    except Exception as e:
                        logging.warning(e)
                        self.disconnect()
                        return

            pb_inst_pbonly(flags, opcode, opcode_data, length)

        pb_stop_programming()
        pb_close()

    def StartPulsing(self):
        if not self.connect():
            return
        try:
            pb_start()
        except RuntimeError as e:
            logging.warning(e)
            self.disconnect()
            return
        if not self.disconnect():
            return

    def StopPulsing(self):
        if not self.connect():
            return
        try:
            pb_stop()
        except RuntimeError as e:
            logging.warning(e)
            self.disconnect()
            return
        if not self.disconnect():
            return
