import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk

from qr_generator import generate_qr, format_wifi
from validators import is_valid_email, is_valid_phone, is_valid_url

# UI constants
BG_COLOR = "#1e2735"  # Dark navy/charcoal background
ACCENT_COLOR = "#3b82f6"  # Blue for primary buttons
SECONDARY_COLOR = "#8b5cf6"  # Purple for secondary actions

class QRStudioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR Studio – QR Code Generator")
        self.geometry("950x600")
        self.configure(bg=BG_COLOR)

        # ttk style tweaks – dark background with light text
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TLabel', background=BG_COLOR, foreground='white')
        style.configure('TButton', padding=6, background=ACCENT_COLOR, foreground='white')
        style.map('TButton', background=[('active', ACCENT_COLOR)])
        style.configure('Header.TLabel', font=('Helvetica', 20, 'bold'))
        style.configure('Section.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('TEntry', padding=4)
        style.configure('TCombobox', padding=4)

        self._init_vars()
        self._build_ui()
        self.generated_image = None

    # ---------------------------------------------------------------------
    # Variable initialisation
    # ---------------------------------------------------------------------
    def _init_vars(self):
        self.qr_type = tk.StringVar(value="Text")
        self.input_data = tk.StringVar()
        self.wifi_ssid = tk.StringVar()
        self.wifi_password = tk.StringVar()
        self.wifi_encryption = tk.StringVar(value="WPA")
        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"
        self.box_size = tk.IntVar(value=10)
        self.error_correction = tk.StringVar(value="M (Medium)")

    # ---------------------------------------------------------------------
    # UI construction
    # ---------------------------------------------------------------------
    def _build_ui(self):
        # ----- Left navigation panel -----
        left = tk.Frame(self, bg=BG_COLOR, width=150)
        left.pack(side='left', fill='y')
        ttk.Label(left, text="QR Studio", style='Header.TLabel').pack(pady=(20,10))
        ttk.Button(left, text="Generate QR", command=self.show_generate).pack(pady=5, fill='x', padx=10)
        ttk.Button(left, text="About", command=self.show_about).pack(pady=5, fill='x', padx=10)

        # ----- Main container -----
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.generate_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.about_frame = tk.Frame(self.container, bg=BG_COLOR)
        for f in (self.generate_frame, self.about_frame):
            f.place(relwidth=1, relheight=1)

        self._build_generate_page()
        self._build_about_page()
        self.show_generate()

    # ---------------------------------------------------------------------
    # Generate page layout
    # ---------------------------------------------------------------------
    def _build_generate_page(self):
        # Use three columns – Details, (spacer), Preview
        self.generate_frame.columnconfigure(0, weight=1)
        self.generate_frame.columnconfigure(2, weight=1)

        # ---- Details (left column) ----
        details = tk.LabelFrame(self.generate_frame, text="QR Details", bg=BG_COLOR, fg='white')
        details.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        ttk.Label(details, text="QR Type:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Combobox(details, values=["Text", "URL", "Email", "Phone", "Wi‑Fi"],
                     textvariable=self.qr_type, state='readonly').grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        # Container for dynamic inputs
        self.input_container = tk.Frame(details, bg=BG_COLOR)
        self.input_container.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        self.qr_type.trace_add('write', lambda *a: self.refresh_inputs())
        self.refresh_inputs()

        # Colour selectors
        ttk.Label(details, text="Foreground colour:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.fg_btn = ttk.Button(details, text=self.fill_color, command=self.choose_fg)
        self.fg_btn.grid(row=2, column=1, sticky='ew', padx=5, pady=2)
        ttk.Label(details, text="Background colour:").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.bg_btn = ttk.Button(details, text=self.back_color, command=self.choose_bg)
        self.bg_btn.grid(row=3, column=1, sticky='ew', padx=5, pady=2)

        # Size selector
        ttk.Label(details, text="Box size (pixels):").grid(row=4, column=0, sticky='w', padx=5, pady=2)
        ttk.Combobox(details, values=[5,8,10,12,15,20], textvariable=self.box_size, state='readonly')\
            .grid(row=4, column=1, sticky='ew', padx=5, pady=2)

        # Error correction
        ttk.Label(details, text="Error correction:").grid(row=5, column=0, sticky='w', padx=5, pady=2)
        ttk.Combobox(details, values=["L (Low)", "M (Medium)", "Q (Quartile)", "H (High)"],
                     textvariable=self.error_correction, state='readonly')\
            .grid(row=5, column=1, sticky='ew', padx=5, pady=2)

        # Action buttons
        btn_frame = tk.Frame(details, bg=BG_COLOR)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Generate QR", command=self.generate_qr)\
            .grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form, style='Secondary.TButton')\
            .grid(row=0, column=1, padx=5)

        # ---- Preview (right column) ----
        preview = tk.LabelFrame(self.generate_frame, text="Preview", bg=BG_COLOR, fg='white')
        preview.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        self.preview_label = ttk.Label(preview, text="No QR generated yet", width=30, background='#2b2b2b')
        self.preview_label.pack(pady=10)
        ttk.Button(preview, text="Save QR Code", command=self.save_qr).pack(pady=5)
        self.type_display = ttk.Label(preview, text="Type: —")
        self.type_display.pack(pady=2)

    # ---------------------------------------------------------------------
    # Dynamic input fields per QR type
    # ---------------------------------------------------------------------
    def refresh_inputs(self):
        for w in self.input_container.winfo_children():
            w.destroy()
        t = self.qr_type.get()
        if t == "Text":
            ttk.Label(self.input_container, text="Text:").grid(row=0, column=0, sticky='w')
            ttk.Entry(self.input_container, textvariable=self.input_data).grid(row=0, column=1, sticky='ew')
        elif t == "URL":
            ttk.Label(self.input_container, text="URL:").grid(row=0, column=0, sticky='w')
            ttk.Entry(self.input_container, textvariable=self.input_data).grid(row=0, column=1, sticky='ew')
        elif t == "Email":
            ttk.Label(self.input_container, text="Email:").grid(row=0, column=0, sticky='w')
            ttk.Entry(self.input_container, textvariable=self.input_data).grid(row=0, column=1, sticky='ew')
        elif t == "Phone":
            ttk.Label(self.input_container, text="Phone:").grid(row=0, column=0, sticky='w')
            ttk.Entry(self.input_container, textvariable=self.input_data).grid(row=0, column=1, sticky='ew')
        elif t == "Wi‑Fi":
            ttk.Label(self.input_container, text="SSID:").grid(row=0, column=0, sticky='w')
            ttk.Entry(self.input_container, textvariable=self.wifi_ssid).grid(row=0, column=1, sticky='ew')
            ttk.Label(self.input_container, text="Password:").grid(row=1, column=0, sticky='w')
            ttk.Entry(self.input_container, textvariable=self.wifi_password, show='*').grid(row=1, column=1, sticky='ew')
            ttk.Label(self.input_container, text="Encryption:").grid(row=2, column=0, sticky='w')
            ttk.Combobox(self.input_container, values=['WPA','WEP',''], textvariable=self.wifi_encryption, state='readonly')\
                .grid(row=2, column=1, sticky='ew')
        else:
            ttk.Label(self.input_container, text="Unsupported type").grid(row=0, column=0)

    # ---------------------------------------------------------------------
    # Colour pickers
    # ---------------------------------------------------------------------
    def choose_fg(self):
        col = colorchooser.askcolor(initialcolor=self.fill_color)[1]
        if col:
            self.fill_color = col
            self.fg_btn.configure(text=col)

    def choose_bg(self):
        col = colorchooser.askcolor(initialcolor=self.back_color)[1]
        if col:
            self.back_color = col
            self.bg_btn.configure(text=col)

    # ---------------------------------------------------------------------
    # Validation helpers
    # ---------------------------------------------------------------------
    def validate(self):
        t = self.qr_type.get()
        data = self.input_data.get().strip()
        if t == "Text":
            return bool(data), ""
        if t == "URL":
            return (is_valid_url(data), "Please enter a valid URL.") if not is_valid_url(data) else (True, "")
        if t == "Email":
            return (is_valid_email(data), "Please enter a valid email address.") if not is_valid_email(data) else (True, "")
        if t == "Phone":
            return (is_valid_phone(data), "Please enter a valid phone number.") if not is_valid_phone(data) else (True, "")
        if t == "Wi‑F i":
            # we treat Wi‑Fi specially below
            return True, ""
        if t == "Wi‑Fi":
            if not self.wifi_ssid.get().strip():
                return False, "SSID cannot be empty."
            return True, ""
        return False, "Unsupported type"

    # ---------------------------------------------------------------------
    # QR generation
    # ---------------------------------------------------------------------
    def generate_qr(self):
        ok, msg = self.validate()
        if not ok:
            messagebox.showerror("Invalid input", msg)
            return
        t = self.qr_type.get()
        if t == "Wi‑Fi":
            data_str = format_wifi(self.wifi_ssid.get(), self.wifi_password.get(), self.wifi_encryption.get())
        else:
            data_str = self.input_data.get().strip()
        try:
            img = generate_qr(
                data_str,
                box_size=self.box_size.get(),
                fill_color=self.fill_color,
                back_color=self.back_color,
                error_correction=self.error_correction.get(),
            )
        except Exception as e:
            messagebox.showerror("Generation error", str(e))
            return
        self.generated_image = img
        # Resize for preview
        preview = img.copy()
        preview.thumbnail((250,250))
        self.tk_image = ImageTk.PhotoImage(preview)
        self.preview_label.configure(image=self.tk_image, text="")
        self.type_display.configure(text=f"Type: {t}")
        messagebox.showinfo("Success", "QR code generated!")

    # ---------------------------------------------------------------------
    # Save QR
    # ---------------------------------------------------------------------
    def save_qr(self):
        if not self.generated_image:
            messagebox.showwarning("No QR", "Generate a QR code first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png")])
        if not path:
            return
        try:
            self.generated_image.save(path)
            messagebox.showinfo("Saved", f"QR saved to {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    # ---------------------------------------------------------------------
    # Clear form
    # ---------------------------------------------------------------------
    def clear_form(self):
        self.input_data.set("")
        self.wifi_ssid.set("")
        self.wifi_password.set("")
        self.wifi_encryption.set("WPA")
        self.generated_image = None
        self.preview_label.configure(image="", text="No QR generated yet")
        self.type_display.configure(text="Type: —")
        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"
        self.fg_btn.configure(text=self.fill_color)
        self.bg_btn.configure(text=self.back_color)
        self.refresh_inputs()

    # ---------------------------------------------------------------------
    # Navigation helpers
    # ---------------------------------------------------------------------
    def show_generate(self):
        self.generate_frame.lift()

    def show_about(self):
        self.about_frame.lift()

    # ---------------------------------------------------------------------
    # About page
    # ---------------------------------------------------------------------
    def _build_about_page(self):
        ttk.Label(self.about_frame, text="About QR Studio", style='Header.TLabel').pack(pady=20)
        txt = (
            "QR Studio is a lightweight desktop app written in Python using tkinter.\n"
            "It generates QR codes for plain text, URLs, email addresses, phone numbers\n"
            "and Wi‑Fi credentials. Users can customise colours, size and error‑correction\n"
            "level, and save the resulting image as a PNG."
        )
        ttk.Label(self.about_frame, text=txt, justify='left').pack(padx=20)

if __name__ == "__main__":
    app = QRStudioApp()
    app.mainloop()
