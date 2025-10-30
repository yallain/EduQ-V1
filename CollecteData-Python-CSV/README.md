# SPDC-FPGA Data Acquisition Script  
*(Python Serial Logger for FPGA Coincidence Counter Data)*

## 1. Overview

This repository contains a Python script (`CollectData-07-12-2023.py`) and an example data file (`data.csv`) used for **acquiring, decoding, and logging data** sent by an FPGA coincidence counter via a **serial (UART)** interface.

The FPGA part of the system (implemented on a **Digilent Arty A7-35 FPGA board**) continuously transmits event count data every 0.1 seconds.  
This Python script captures that serial stream, decodes it, and stores it in a **CSV file** for analysis and visualization.

This project complements the FPGA design hosted separately in the  
👉 [SPDC-FPGA-GateWare](https://github.com/yourusername/SPDC-FPGA-GateWare) repository.

---

## 2. Functional Description

### Features
- Connects to the **serial port (UART)** of the FPGA.  
- Synchronizes automatically with the **frame header (`0x12345678`)**.  
- Reads and decodes 9 × 32-bit integer values:
  - 4 single-channel counts (A, B, C, D)
  - 4 two-fold coincidences (A∧B, A∧C, D∧B, D∧C)
  - 1 three-fold coincidence (A∧B∧C)
- Logs all values with timestamps in `data.csv`.
- Adjustable serial port, baud rate, and duration.

---

## 3. Repository Structure

```
project_root/
├─ CollectData-07-12-2023.py    # Python data collection script
├─ data.csv                     # Example output from FPGA serial stream
└─ README.md                    # This documentation
```

---

## 4. How It Works

1. The FPGA sends data frames at fixed intervals (~0.1 s).  
2. Each frame starts with a 32-bit synchronization word `0x12345678`.  
3. The script:
   - Waits for this header pattern in the serial stream.  
   - Reads the next 9 × 4 bytes = 36 bytes (9 integers).  
   - Converts them into readable integers.  
   - Logs all results into `data.csv` with a timestamp.  

Each CSV row corresponds to one frame of data from the FPGA.

---

## 5. Example CSV Output

| timestamp | A | B | C | D | AB | AC | DB | DC | ABC |
|------------|---|---|---|---|----|----|----|----|-----|
| 0.0 | 13 | 12 | 10 | 12 | 2 | 3 | 1 | 1 | 0 |
| 0.1 | 14 | 11 | 11 | 13 | 3 | 2 | 1 | 1 | 0 |
| 0.2 | 13 | 12 | 9 | 12 | 2 | 3 | 1 | 0 | 0 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

Example file: [`data.csv`](./data.csv)

---

## 6. Usage Instructions

### Requirements
Install Python 3.8 or newer and the following packages:
```bash
pip install pyserial numpy pandas
```

### Running the Script
1. Connect the FPGA board (Arty A7-35) via USB.  
2. Identify the serial port (e.g., `COM3` on Windows or `/dev/ttyUSB1` on Linux).  
3. Run the script:
   ```bash
   python CollectData-07-12-2023.py
   ```
4. The program will create a new `data.csv` file and log the incoming data stream.

You can stop the script anytime with **Ctrl+C**.

---

## 7. Data Analysis

Once the data is collected, you can open `data.csv` with:
- **Pandas / NumPy** in Python for plotting or analysis.  
- **MATLAB** or **Excel** for quick inspection.  

Example (Python):
```python
import pandas as pd
data = pd.read_csv('data.csv')
data.plot(x='timestamp', y=['A','B','C','D'])
```

---

## 8. Relation to FPGA Gateware

This logger is designed to work with the FPGA bitstream developed in the  
[SPDC-FPGA-GateWare](https://github.com/yourusername/SPDC-FPGA-GateWare) project.

- Baud rate: **~19,200 bps**  
- Frame rate: **10 Hz (every 0.1 s)**  
- Header: **0x12345678**  
- Payload: **9 × 32-bit integers**

---

## 9. Acknowledgements

This work was inspired by and built upon the open educational resources of the  
[Quantum Mechanics in the Single Photon Laboratory](https://physlab.org/qmlab/)  
at **PhysLab, Department of Physics, LUMS (Lahore University of Management Sciences)**.

Original FPGA source:  
👉 [https://physlab.org/wp-content/uploads/2020/07/Commented-FPGA-code.zip](https://physlab.org/wp-content/uploads/2020/07/Commented-FPGA-code.zip)

I sincerely thank **Professor Dr. Muhammad Sabieh Anwar** and his team for making their FPGA coincidence counting system publicly available and inspiring this adaptation.

---

## 10. License

This repository is provided for educational and research purposes.  
Please cite the original PhysLab source and the FPGA project if reused or modified.

**Author (Adaptation):** Yann ALLAIN
**Date:** 2023
**Related project:** [SPDC-FPGA-GateWare](https://github.com/yourusername/SPDC-FPGA-GateWare)
