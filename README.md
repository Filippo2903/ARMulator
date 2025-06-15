# Final Project - ARMv4 Emulator

###### *University of Rome Tor Vergata<br>BSc in Computer Science<br>A.Y. 2024/2025 - Computer Architecture<br> Prof. A. Simonetta, Eng. E. Iannaccone<br>Filippo Gentili, Thomas Infascelli, Matteo Sorvillo, Alessandro Stella*

## Introduction

This project was created to meet the educational need for a native and maintainable alternative to [**CPUlator**](https://cpulator.01xz.net/), a computer systems simulator and debugger.<br>
The project is based on [**epater**](https://github.com/mgard/epater), an ARMv4 assembler and emulator.<br>
The original code has been updated, optimized, and made compatible with both Windows and Linux.

## Requirements

* Provide a native alternative to CPUlator
* Use [epater](https://github.com/mgard/epater) as a starting point

  * Make the initial project usable
  * Understand its capabilities and limitations
  * Make the software installation process clear and straightforward

## The Project

This is an educational ARM emulator, written in Python, featuring an interactive graphical interface. Instead of ***interpreting*** ARM code, this software can ***emulate*** an ARM CPU directly.<br>
Specifically, it is an assembler and simulator composed of three parts:

1. An assembler that translates ARM code into ARMv4 bytecode
2. An ARMv4 emulator
3. A graphical interface including a text editor, register table, memory address table, and various debugging and learning tools

## Supported Features

* Full support for ARMv4 instruction set
* Interrupts (software via SWI or hardware via timer using IRQ or FIQ)
* Step-by-step and continuous execution
* Integrated debugger, including reverse-debugging
* Modern and interactive graphical interface
* Save and load up to 10 sessions

## Main Changes

* **Updated dependencies** in the `requirements.txt` file
* **Parallelization of** HTTP and WebSocket **servers**
* **Optimized GUI updates**

  * **Faster text editor**
* **Compiled into an executable** using [py-to-exe](https://pypi.org/project/auto-py-to-exe)
* **Installer-based distribution**
* **Modernized GUI** and improved usability
* **Integrated multilingual support**

  * **Added Italian and English languages**
* Temporary access to the emulator via private server

## Installation

To install the emulator, simply download the installer for your operating system.<br>
[Windows]() [Linux]()<br>

### System Requirements

* Windows 11 or any Linux distribution
* Python ver. 3.12 (for developers)

### Developer Installation

```bash
git clone https://github.com/USERNAME/REPO_NAME
pip install -r requirements.txt
```

## Server Access

The emulator has been temporarily deployed on a low-performance VPS, solely for demonstrating a potential future stable deployment.<br>
To access the emulator on the private server, use the following [address](http://147.93.63.174:8888):<br>
147.93.63.174:8888

## Usage

1. Open the application
2. Load a `.txt` file containing ARM assembly code or use the built-in text editor
3. Use the GUI to:

   * Edit the code
   * Manually edit memory and registers
   * Set breakpoints
   * Run the program (step-by-step or continuously)
4. View: registers, memory, flags, output, and errors
5. The session is automatically saved
6. Export the text code

## Differences from the Original Project

| Feature      | Original Epater | Final Project Version      |
| ------------ | --------------- | -------------------------- |
| Execution    | Web-based       | Native application         |
| GUI          | Outdated        | Modernized                 |
| Server       | Non-functional  | Dual, asynchronous         |
| Build        | Not available   | Executable + installer     |
| Dependencies | Outdated        | Managed via `requirements` |

## How It Works and User Manual

The file [`howItWorks.pdf`](https://github.com/Filippo2903/ARMulator/blob/master/howItWorks.png) provides a visual overview of the emulator’s general functioning.<br>
For detailed API documentation, refer to the [documentation](http://147.93.63.174:8080).<br>
The original project manual (*to be updated*) is included: [`manuale`](https://github.com/Filippo2903/ARMulator/blob/master/manuale.pdf). It describes GUI features, registers, memory, and the supported ARMv4 instruction set.

# Future Developments

1. Implement ARMv7 features

   * ##### In `simulator.py`, the *`bytecodeToInstr`* function seems a good starting point
   * ##### [unicorn](https://www.unicorn-engine.org) could be used, but would require a complete codebase overhaul
2. Complete the translation by removing all hard-coded strings
3. Optimize client-server interaction
4. Add Thumb mode support
5. Add coprocessor instruction support
6. Accurately simulate CPU cycles
7. Ensure compatibility with macOS (Silicon/Intel)
8. Further optimize GUI updates and prevent passive behavior

   * ##### Currently uses jQuery code to react to WebSocket messages
9. Translate the `manuale` or produce a new one
10. Understand memory initialization and address errors with uninitialized cells

## License and Acknowledgments

This project was developed as a final assignment for the [Computer Science](http://www.informatica.uniroma2.it/) degree program at the University of Rome Tor Vergata.<br>
It is based on [epater](https://github.com/mgard/epater), originally developed by Marc-André Gardner, Yannick Hold-Geoffroy, and Jean-François Lalonde.<br>
The project is released under the GPLv3 license (see `LICENSE`).
