import serial
import time
import sys


# ============================================================
# CAREX - BLUETOOTH RECEIVER
# ============================================================

PORT = "COM8"
BAUDRATE = 115200


print()
print("=" * 50)
print("        CAREX BLUETOOTH RECEIVER")
print("=" * 50)
print(f"Bluetooth COM Port : {PORT}")
print("Transport           : Bluetooth Classic SPP")
print("Expected frequency  : ~50 Hz")
print("-" * 50)


# ============================================================
# CONNECT
# ============================================================

try:
    ser = serial.Serial(
        port=PORT,
        baudrate=BAUDRATE,
        timeout=2
    )

except serial.SerialException as e:

    print()
    print("ERROR: Could not open Bluetooth COM port")
    print(e)

    sys.exit(1)


print("Bluetooth COM port opened successfully!")
print()
print("Waiting for ESP32 data...")
print("-" * 70)


# ============================================================
# RECEIVE DATA
# ============================================================

packet_count = 0
start_time = time.time()

try:

    while True:

        raw_line = ser.readline()

        if not raw_line:
            continue


        # ----------------------------------------------------
        # Decode Bluetooth data
        # ----------------------------------------------------

        line = raw_line.decode(
            "utf-8",
            errors="ignore"
        ).strip()


        if not line:
            continue


        # ----------------------------------------------------
        # ESP32 sends CSV:
        #
        # timestamp,ax,ay,az,gx,gy,gz
        # ----------------------------------------------------

        parts = line.split(",")


        # ----------------------------------------------------
        # Ignore non-data messages
        # ----------------------------------------------------

        if len(parts) != 7:
            print(f"[ESP32] {line}")
            continue


        try:

            timestamp = int(parts[0])

            ax = float(parts[1])
            ay = float(parts[2])
            az = float(parts[3])

            gx = float(parts[4])
            gy = float(parts[5])
            gz = float(parts[6])

        except ValueError:

            print(f"[INVALID] {line}")
            continue


        # ----------------------------------------------------
        # Valid sensor packet
        # ----------------------------------------------------

        packet_count += 1


        print(
            f"{timestamp:8d} | "
            f"A: {ax:7.3f} "
            f"{ay:7.3f} "
            f"{az:7.3f} | "
            f"G: {gx:7.3f} "
            f"{gy:7.3f} "
            f"{gz:7.3f}"
        )


except KeyboardInterrupt:

    print()
    print()
    print("Stopping receiver...")


finally:

    ser.close()

    elapsed = time.time() - start_time

    print()
    print("=" * 70)
    print("CAREX RECEIVER STOPPED")
    print("=" * 70)
    print(f"Packets received : {packet_count}")

    if elapsed > 0:
        print(
            f"Average rate     : "
            f"{packet_count / elapsed:.1f} packets/sec"
        )

    print("Bluetooth COM port closed.")