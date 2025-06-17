class EMA_shift_no_round:
    def __init__(self, shiftfac: int):
        self.shiftfac = shiftfac
        self.accu = 0

    def __call__(self, x: int):
#        print(self.z, x)
        # set lowest bit in Accu to zero
        self.accu += x
        shifted = self.accu >> self.shiftfac
        self.accu -= shifted
##        if self.accu% 2 != 0:
##            self.accu -= 1        
        return shifted

class EMA_round:
    def __init__(self, shiftfac: int):
        self.shiftfac = shiftfac
        self.fixedPointOneHalf = 1 << (shiftfac - 1)
        self.accu = 0

    def __call__(self, x: int):
        self.accu += x
        shifted = (self.accu + self.fixedPointOneHalf) >> self.shiftfac
        self.accu -= shifted
        return shifted

class EMA_shift_no_round_HWlike:
    def __init__(self, shiftfac: int, accubits: int):
        self.shiftfac = shiftfac
        self.accubits = accubits
        self.accu = 0
        self.accumax = (1 << (accubits - 1)) - 1  # e.g. 1023
        self.accumin = -(1 << (accubits - 1))     # e.g. -1024
#        print(self.accumax, self.accumin)

    def __call__(self, x: int):
        # Eingangsbegrenzung (optional, simuliere 8-bit signed input)
        x = max(-128, min(127, x))

        # Akkumulator-Update
        self.accu += x

        # Saturation check (falls gewünscht – kann auch wrap-around sein in HW)
        if self.accu > self.accumax:
            self.accu = self.accumax
        elif self.accu < self.accumin:
            self.accu = self.accumin

        # Bitshift ist "kostenlos"
        shifted = self.accu >> self.shiftfac

        # Die Ausgabe wird vom Akkumulator abgezogen – nur eine Subtraktion
        self.accu -= shifted
#        print(self.accu)

        return shifted
