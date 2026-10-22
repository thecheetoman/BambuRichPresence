import json, ssl, time
import paho.mqtt.client as mqtt

# what will show up on discord
statusTable = {
    0: "Printing",
    1: "Bed leveling",
    2: "Heating bed",
    4: "Changing filament",
    8: "Heating nozzle",
    9: "Dynamic Flow Calibration",
    14: "Homing",
    15: "Purging nozzle",
    23: "Unloading filament",
    25: "Loading filament",
}

# ty google for ts
modelMap = {
    "N1": "A1 mini",
    "N2S": "A1",
    "C11": "P1P",
    "C12": "P1S",
    "BL-P001": "X1 Carbon",
    "BL-P002": "X1",
    "C13": "X1E",
}

class printerStatus:
    def __init__(self):
        self.data = {} # printer data, to be fed to drp script
        self.model = None # printer model
        self.model_raw = None # raw printer model number

    def update(self, print_report: dict):
        self.data.update(print_report)

    def set_model_from_version(self, info: dict):
        for module in info.get("module", []):
            if module.get("name") == "ota" and module.get("product_name"):
                self.model_raw = module["product_name"]
                self.model = module["product_name"].replace("Bambu Lab ", "")
                return

    def get_status(self) -> str:
        gstate = self.data.get("gcode_state", "UNKNOWN")
        stage_code = self.data.get("stg_cur")
        layer = self.data.get("layer_num")
        total = self.data.get("total_layer_num")
        percent = self.data.get("mc_percent")

        stage = statusTable.get(stage_code, f"Stage {stage_code}") if stage_code is not None else None
        layers = f"{layer}/{total} layers" if layer is not None and total else None
        progress = f"{percent}%" if percent is not None else None

        if gstate == "RUNNING":
            if stage and stage_code != 0:
                return stage
            parts = [p for p in (layers, f"({progress})" if progress else None) if p]
            return "Printing " + " ".join(parts) if parts else "Printing"

        if gstate == "PREPARE":
            return stage or "Preparing"

        if gstate == "PAUSE":
            if stage and stage_code not in (0, None):
                return f"Paused: {stage}"
            return f"Paused at {layers}" if layers else "Paused"

        if gstate == "FINISH":
            return "Finished"

        if gstate == "FAILED":
            return "Failed"

        if gstate == "IDLE":
            return "Idle"

        return "Unknown"