from pymclevel import TAG_List, TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_Double, TAG_Float, TAG_String
import time

displayName = "Beta Kobra Fixer"

inputs = [
    ("Set Detector Rails to specific Data Value", True),
    ("Detector Rail Data Value", 8)
]

def add_minecart(level, x, y, z):
    """
    Adds a minecart entity at the given x, y, z coordinates.
    """
    minecart = TAG_Compound()
    minecart["id"] = TAG_String("Minecart")
    minecart["Pos"] = TAG_List([TAG_Double(x + 0.5), TAG_Double(y + 0.5), TAG_Double(z + 0.5)])
    minecart["Motion"] = TAG_List([TAG_Double(0), TAG_Double(0), TAG_Double(0)])
    minecart["Rotation"] = TAG_List([TAG_Float(0.0), TAG_Float(0.0)])
    minecart["FallDistance"] = TAG_Float(0.0)
    minecart["Fire"] = TAG_Short(0)
    minecart["Air"] = TAG_Short(300)
    minecart["OnGround"] = TAG_Byte(1)
    minecart["Dimension"] = TAG_Int(0)
    minecart["Invulnerable"] = TAG_Byte(0)
    minecart["PortalCooldown"] = TAG_Int(0)

    # UUID generates using system time
    current_time = int(time.time() * 1000)
    minecart["UUIDLeast"] = TAG_Int(current_time & 0x7FFFFFFF)  # Ensures within 32-bit signed integer
    minecart["UUIDMost"] = TAG_Int((current_time >> 32) & 0x7FFFFFFF)  # Ensures within 32-bit signed integer

    # Adds the minecart entity to the level
    chunk = level.getChunk(x // 16, z // 16)
    chunk.Entities.append(minecart)
    chunk.dirty = True

def perform(level, box, options):
    reset_to_flat = options["Set Detector Rails to specific Data Value"]
    rail_data_value = options["Detector Rail Data Value"]
    for y in range(box.miny, box.maxy):
        for z in range(box.minz, box.maxz):
            for x in range(box.minx, box.maxx):
                block = level.blockAt(x, y, z)
                if block == 28:  # Detector Rail ID
                    if reset_to_flat:
                          level.setBlockDataAt(x, y, z, rail_data_value)  # Sets data value of the detector rail https://minecraft.wiki/w/Detector_Rail#Data_history
                    add_minecart(level, x, y, z)  # Places minecart above the detector rail

    level.markDirtyBox(box)