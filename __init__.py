from binaryninja import *

import subprocess

def demangle_swift(bv):
    i = 0
    for fn in bv.functions:
        function_name = fn.name
        demangled = ""

        out = subprocess.check_output(["swift", "demangle", "-compact", function_name])
        if len(out) == 0:
            continue
        try:
            demangled = out[:-1].decode("utf-8")
        except:
            continue

         # If the demangler produces a complicated output, try to use the simpler version.
        if len(demangled.split()) > 1:
            out = subprocess.check_output(["swift", "demangle", "-compact", "-simplified", function_name])
            if len(out) == 0:
                continue
            try:
                demangled = out[:-1].decode("utf-8")
            except:
                continue

        print("old: " + fn.name  + ", new: " + demangled)

        bv.functions[i].name = demangled
        i = i + 1

class DemangleSwiftFunctions(BackgroundTaskThread):
    def __init__(self, msg, bv):
        BackgroundTaskThread.__init__(self, msg, True)
        self.bv = bv

    def run(self):
        demangle_swift(self.bv)

def demangle_functions(bv):
    task = DemangleSwiftFunctions("Demangling Swift functions...", bv)
    task.start()

PluginCommand.register("Demangle Swift", "Demangles Swift functions.", demangle_functions)