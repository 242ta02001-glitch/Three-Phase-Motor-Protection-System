# Three-Phase Motor Protection System
# EEE Student GitHub Project
# Python Simulation

import random
import time

# -------------------------------
# Motor Ratings
# -------------------------------

RATED_VOLTAGE = 415       # Volts
RATED_CURRENT = 10        # Amps
MAX_TEMPERATURE = 80      # °C

VOLTAGE_TOLERANCE = 0.10  # ±10%
CURRENT_IMBALANCE_LIMIT = 10  # %
VOLTAGE_IMBALANCE_LIMIT = 5   # %


# -------------------------------
# Simulate Sensor Readings
# -------------------------------

def read_motor_data():

    voltage_r = random.uniform(380, 440)
    voltage_y = random.uniform(380, 440)
    voltage_b = random.uniform(380, 440)

    current_r = random.uniform(5, 14)
    current_y = random.uniform(5, 14)
    current_b = random.uniform(5, 14)

    temperature = random.uniform(45, 90)

    return (
        voltage_r, voltage_y, voltage_b,
        current_r, current_y, current_b,
        temperature
    )


# -------------------------------
# Calculate Imbalance
# -------------------------------

def calculate_imbalance(value1, value2, value3):

    average = (value1 + value2 + value3) / 3

    if average == 0:
        return 0

    maximum_difference = max(
        abs(value1 - average),
        abs(value2 - average),
        abs(value3 - average)
    )

    imbalance = (maximum_difference / average) * 100

    return imbalance


# -------------------------------
# Protection Logic
# -------------------------------

def check_protection(
    vr, vy, vb,
    ir, iy, ib,
    temperature
):

    faults = []

    # Voltage limits
    min_voltage = RATED_VOLTAGE * (1 - VOLTAGE_TOLERANCE)
    max_voltage = RATED_VOLTAGE * (1 + VOLTAGE_TOLERANCE)

    # Check phase voltages
    if vr < min_voltage or vr > max_voltage:
        faults.append("R-PHASE VOLTAGE FAULT")

    if vy < min_voltage or vy > max_voltage:
        faults.append("Y-PHASE VOLTAGE FAULT")

    if vb < min_voltage or vb > max_voltage:
        faults.append("B-PHASE VOLTAGE FAULT")

    # Voltage imbalance
    voltage_imbalance = calculate_imbalance(vr, vy, vb)

    if voltage_imbalance > VOLTAGE_IMBALANCE_LIMIT:
        faults.append("VOLTAGE IMBALANCE")

    # Current overload
    if ir > RATED_CURRENT:
        faults.append("R-PHASE OVERCURRENT")

    if iy > RATED_CURRENT:
        faults.append("Y-PHASE OVERCURRENT")

    if ib > RATED_CURRENT:
        faults.append("B-PHASE OVERCURRENT")

    # Current imbalance
    current_imbalance = calculate_imbalance(ir, iy, ib)

    if current_imbalance > CURRENT_IMBALANCE_LIMIT:
        faults.append("CURRENT IMBALANCE")

    # Temperature protection
    if temperature > MAX_TEMPERATURE:
        faults.append("MOTOR OVERHEATING")

    return faults, voltage_imbalance, current_imbalance


# -------------------------------
# Display Motor Status
# -------------------------------

def display_status(
    vr, vy, vb,
    ir, iy, ib,
    temperature,
    voltage_imbalance,
    current_imbalance,
    faults
):

    print("\n" + "=" * 65)
    print("          THREE-PHASE MOTOR PROTECTION SYSTEM")
    print("=" * 65)

    print("\n--- PHASE VOLTAGES ---")
    print(f"R Phase : {vr:.2f} V")
    print(f"Y Phase : {vy:.2f} V")
    print(f"B Phase : {vb:.2f} V")

    print("\n--- PHASE CURRENTS ---")
    print(f"R Phase : {ir:.2f} A")
    print(f"Y Phase : {iy:.2f} A")
    print(f"B Phase : {ib:.2f} A")

    print("\n--- MOTOR CONDITION ---")
    print(f"Temperature       : {temperature:.2f} °C")
    print(f"Voltage Imbalance : {voltage_imbalance:.2f} %")
    print(f"Current Imbalance : {current_imbalance:.2f} %")

    print("\n--- PROTECTION STATUS ---")

    if len(faults) == 0:

        print("Motor Status      : NORMAL")
        print("Protection        : ACTIVE")
        print("Action            : MOTOR RUNNING")

    else:

        print("Motor Status      : FAULT DETECTED")

        for fault in faults:
            print(f"⚠ Fault           : {fault}")

        print("Protection        : TRIPPED")
        print("Action            : MOTOR STOPPED")

    print("=" * 65)


# -------------------------------
# Main Program
# -------------------------------

def main():

    print("Three-Phase Motor Protection System")
    print("------------------------------------")
    print("Monitoring motor parameters...")
    print("Press Ctrl+C to stop.")

    try:

        while True:

            # Read sensor data
            (
                vr, vy, vb,
                ir, iy, ib,
                temperature
            ) = read_motor_data()

            # Check protection
            (
                faults,
                voltage_imbalance,
                current_imbalance
            ) = check_protection(
                vr, vy, vb,
                ir, iy, ib,
                temperature
            )

            # Display results
            display_status(
                vr, vy, vb,
                ir, iy, ib,
                temperature,
                voltage_imbalance,
                current_imbalance,
                faults
            )

            time.sleep(3)

    except KeyboardInterrupt:

        print("\n\nProtection system stopped.")
        print("Motor control simulation ended.")


# -------------------------------
# Program Entry
# -------------------------------

if __name__ == "__main__":
    main()
