# QR Studio – QR Code Generator

A Python-based desktop application that allows users to generate QR codes through a simple graphical user interface. QR Studio supports QR code creation with customizable appearance and input validation.

## Features

- **QR Code Generation:** Generate QR codes from user-provided information.
- **Custom Colors:** Customize QR code foreground and background colors.
- **Box Size Control:** Adjust the size of QR code modules.
- **Error Correction:** Choose between four error correction levels: L, M, Q, and H.
- **Input Validation:** Validate supported URL, email, and phone number inputs.
- **Wi-Fi QR Codes:** Generate QR codes containing Wi-Fi connection information.
- **Graphical Interface:** Easy-to-use desktop interface built with Python Tkinter.

## Technologies Used

- **Python** – Core programming language
- **Tkinter / ttk** – Graphical user interface
- **qrcode** – QR code generation
- **Pillow (PIL)** – Image processing

## Project Structure

```text
QR-Studio/
│
├── main.py             # Application entry point
├── gui.py              # Graphical user interface
├── qr_generator.py     # QR code generation logic
├── validators.py       # Input validation functions
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignored files
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ns7824002-gif/QR-Studio.git
```

### 2. Navigate to the Project Directory

```bash
cd QR-Studio
```

### 3. Install Dependencies

Make sure Python is installed, then run:

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

## How to Use

1. Launch QR Studio using `main.py`.
2. Enter the information for which you want to generate a QR code.
3. Select the desired QR code options.
4. Customize the foreground color, background color, box size, and error correction level.
5. Generate your QR code through the application interface.

## Error Correction Levels

QR Studio provides four error correction levels:

| Level | Approximate Recovery Capacity |
|---|---:|
| L | 7% |
| M | 15% |
| Q | 25% |
| H | 30% |

Higher error correction levels allow a QR code to remain readable despite more damage or obstruction, but may increase its complexity.

## Future Enhancements

- Add more QR code templates.
- Support additional data formats.
- Improve the user interface.
- Add QR code history and batch generation.

## Author

**Developed as a Python GUI project.**

## Repository

[QR Studio – GitHub](https://github.com/ns7824002-gif/QR-Studio)

---

*QR Studio – Simple, customizable QR code generation using Python.*
