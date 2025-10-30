SPDC-FPGA-GateWare-readme.txt
--------------------------------

# FPGA Coincidence Counter with UART Output  
(Adapted for Digilent Arty A7-35 Board)

## 1. Overview

This FPGA project implements a multi-channel coincidence counter with serial data transmission over UART.
It detects and counts single and coincidence events across four digital input channels (A, B, C, D), then transmits the results to a PC approximately 10 times per second.

The design was adapted from the excellent work of the Quantum Mechanics in the Single Photon Laboratory at PhysLab, LUMS, originally developed for their single-photon experiments.
The original commented Verilog source code can be found here:
https://physlab.org/wp-content/uploads/2020/07/Commented-FPGA-code.zip

This version was modified and ported for use on the Digilent Arty A7-35 FPGA board (Xilinx Artix-7 XC7A35TICSG324-1L).
Additionally, the UART transmission speed was increased slightly to make serial communication more responsive.

Special thanks to Professor Dr. Muhammad Sabieh Anwar and the entire Quantum Mechanics in the Single Photon Laboratory team for their outstanding open educational work.

## 2. Functional Description

Purpose:
- Count individual pulse events on channels A, B, C, D.
- Detect two-fold coincidences: A∧B, A∧C, D∧B, D∧C.
- Detect a three-fold coincidence: A∧B∧C.
- Transmit all results via UART every 0.1 seconds.

This system is suitable for photon detection or coincidence counting experiments in quantum optics setups.

## 3. File Structure

project_root/
├─ rtl/
│  └─ rs232coincidencecounter.v     # Main Verilog source (top-level + submodules)
│
├─ constraints/
│  └─ Arty-A7-35-Master.xdc         # Pin and clock constraints for Arty A7-35 board
│
└─ SPDC-FPGA-GateWare-readme.txt    # This documentation

## 4. Verilog Modules Overview

coincidence                 : Top-level module, connects inputs, generates coincidences, counts events, triggers UART.
coincidence_pulse           : Generates one-clock pulse when two inputs overlap (two-fold coincidence).
three_detector_coincidence  : Generates pulse when three inputs overlap (three-fold coincidence).
counter_pulse               : 32-bit counter incrementing on each pulse, reset on data trigger.
baud_rate_counter           : Generates UART baud rate clock.
data_triggering             : Produces 10 Hz trigger for data transmission.
data_out                    : UART serializer sending header and counter values.

## 5. System Architecture

Clock: 100 MHz  
Baud rate: ~19,200 bps (slightly faster than original)  
Data trigger: every 0.1 s (10 Hz)

Inputs A/B/C/D are edge-synchronized and counted.  
Coincidences are detected by logic ANDs.  
At each trigger, counts are sent over UART and reset to zero.

UART data frame:
1. Header word: 0x12345678
2. A, B, C, D single counts
3. AB, AC, DB, DC two-fold coincidences
4. ABC three-fold coincidence

Each value: 32-bit unsigned integer.

## 6. Hardware Connections (Arty A7-35)

Signal   | FPGA Pin | Description
----------|-----------|-------------
clk       | onboard 100 MHz | system clock
A, B, C, D| user I/O pins   | digital pulse inputs (3.3 V)
UART_TXD  | D10             | connected to onboard USB-UART

Input pulses must be at least one clock cycle wide (10 ns).

## 7. Using the System

1. Program the Arty A7-35 FPGA with the bitstream.
2. Connect USB cable (UART interface).
3. Open serial terminal:
   - Baud: 19,200 bps (or your chosen rate)
   - Format: 8N1
4. Observe data frames every 0.1 s:
   0x12345678 <A> <B> <C> <D> <AB> <AC> <DB> <DC> <ABC>

## 8. Building with Vivado

- Device: xc7a35ticsg324-1L
- Add source: rs232coincidencecounter.v
- Add constraint: Arty-A7-35-Master.xdc
- Top module: coincidence
- Generate bitstream and program FPGA

## 9. Future Improvements

- Adjustable coincidence window (currently one clock cycle).
- PC-side receiver script (Python/MATLAB).
- Simulation testbench.
- Higher-speed UART interface.

## 10. Acknowledgements

Based on the open-source educational work of the Quantum Mechanics in the Single Photon Laboratory, PhysLab, Department of Physics, LUMS.

Original source: https://physlab.org/wp-content/uploads/2020/07/Commented-FPGA-code.zip

Sincere thanks to Professor Dr. Muhammad Sabieh Anwar and his team for sharing their FPGA educational resources with the community.

## 11. License

This adaptation is shared for educational and research purposes.
Please cite the original source if reused or modified.

Author (Adaptation): Yann ALLAIN
Board: Digilent Arty A7-35 (Xilinx Artix-7)
Date: 2023
