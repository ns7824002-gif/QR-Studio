# QR Studio – QR Code Generator

## About the Project

QR Studio is a desktop-based QR Code Generator developed using Python. It provides a graphical user interface that allows users to generate QR codes easily and customize their appearance.

The application is designed to provide a simple and convenient way to create QR codes without relying on online QR code generator websites.

## Features

- Generate QR codes from text and other supported information.
- Support for website URLs, email, phone and Wi-Fi QR codes.
- Customize foreground and background colours.
- Adjust QR code box size.
- Choose error correction levels (L, M, Q and H).
- Preview generated QR codes.
- Save QR codes as PNG images.
- Clear inputs and generate new QR codes.

## Technologies Used

- **Python** – Main programming language.
- **Tkinter / CustomTkinter** – Graphical user interface.
- **qrcode** – QR code generation.
- **Pillow** – Image processing.

## Installation and Setup

### Prerequisites

- Python 3 installed on your computer.
- Internet connection for installing dependencies.

### Step 1: Download the Project

Click the green **Code** button on this repository and select **Download ZIP**. Extract the downloaded ZIP file.

Alternatively, clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

### Step 2: Open the Project Folder

Open PowerShell or Command Prompt inside the extracted project folder.

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python main.py
```

The QR Studio application window should open.

## How to Use

1. Select the QR code type.
2. Enter the required information.
3. Customize foreground and background colours.
4. Select the box size and error correction level.
5. Click **Generate QR**.
6. Preview the generated QR code.
7. Click **Save QR Code** to save it as a PNG image.

## Project Structure

```text
QR-Studio/
├── main.py
├── gui.py
├── qr_generator.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Developed By

**QR Studio – Python Desktop Application**

Developed as an academic project to demonstrate Python programming, GUI development and QR code generation.
