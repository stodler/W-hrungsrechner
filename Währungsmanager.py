import tkinter as tk

# Daten & Konstanten
RATES = {
    "EUR": 1.0, "JPY": 160.0, "SEK": 11.0, 
    "BRL": 5.40, "RUB": 99.0, "GBP": 0.86, "ATS": 13.76,
}
SYMBOLS = {
    "EUR": "€", "JPY": "¥", "SEK": "kr",
    "BRL": "R$", "RUB": "₽", "GBP": "£", "ATS": "öS",
}

# Sprach-Mapping
LANG = {
    "DE": {
        "title": "Währungsrechner",
        "subtitle": "Schnell & einfach umrechnen",
        "amount": "BETRAG",
        "from": "VON",
        "to": "NACH",
        "btn_convert": "Umrechnen",
        "res_label": "Ergebnis",
        "invalid": "Ungültige Eingabe"
    },
    "EN": {
        "title": "Currency Converter",
        "subtitle": "Convert fast & easy",
        "amount": "AMOUNT",
        "from": "FROM",
        "to": "TO",
        "btn_convert": "Convert",
        "res_label": "Result",
        "invalid": "Invalid Input"
    }
}

C = {"bg": "#f4f6f8", "card": "#ffffff", "teal": "#0F6E56",
     "teal_light": "#E1F5EE", "teal_dark": "#085041",
     "text": "#1a1a2e", "muted": "#6b7280", "border": "#e5e7eb"}

current_lang = "DE"

def convert(*_):
    try:
        val = entry.get().replace(",", ".")
        amount = float(val)
        rate = RATES[to_var.get()] / RATES[from_var.get()]
        result = amount * rate
        sym = SYMBOLS[to_var.get()]
        lbl_result.config(text=f"{sym} {result:,.2f}")
        lbl_rate.config(text=f"1 {from_var.get()} = {rate:.4f} {to_var.get()}")
    except:
        lbl_result.config(text=LANG[current_lang]["invalid"])
        lbl_rate.config(text="")

def swap():
    f, t = from_var.get(), to_var.get()
    from_var.set(t)
    to_var.set(f)
    convert()

def switch_language():
    global current_lang
    current_lang = "EN" if current_lang == "DE" else "DE"
    l = LANG[current_lang]
    
    # Canvas Texte aktualisieren
    canvas.itemconfig(txt_title, text=l["title"])
    canvas.itemconfig(txt_subtitle, text=l["subtitle"])
    canvas.itemconfig(txt_amt_lbl, text=l["amount"])
    canvas.itemconfig(txt_from_lbl, text=l["from"])
    canvas.itemconfig(txt_to_lbl, text=l["to"])
    canvas.itemconfig(txt_res_header, text=l["res_label"])
    
    # Widgets aktualisieren
    btn_convert.config(text=l["btn_convert"])
    btn_lang.config(text=f"🌐 {current_lang}")
    convert()

root = tk.Tk()
root.title("Währungsrechner")
root.configure(bg=C["bg"])
root.resizable(False, False)

canvas = tk.Canvas(root, width=360, height=480, bg=C["bg"], highlightthickness=0)
canvas.pack(padx=20, pady=20)

# Card Background
canvas.create_rectangle(0, 0, 360, 480, fill=C["card"], outline=C["border"], width=1)

# Sprach-Button (Oben rechts)
btn_lang = tk.Button(root, text=f"🌐 {current_lang}", font=("Segoe UI", 8, "bold"),
                     bg=C["teal_light"], fg=C["teal"], relief="flat", command=switch_language)
canvas.create_window(310, 30, window=btn_lang, width=50)

# Texte mit IDs speichern für späteren Zugriff
txt_title = canvas.create_text(180, 95, text=LANG["DE"]["title"], font=("Segoe UI", 16, "bold"), fill=C["text"])
txt_subtitle = canvas.create_text(180, 115, text=LANG["DE"]["subtitle"], font=("Segoe UI", 9), fill=C["muted"])

txt_amt_lbl = canvas.create_text(30, 145, text=LANG["DE"]["amount"], font=("Segoe UI", 8, "bold"), fill=C["muted"], anchor="w")
canvas.create_rectangle(20, 155, 340, 190, fill="#f9fafb", outline=C["border"])
entry = tk.Entry(root, font=("Segoe UI", 18, "bold"), bg="#f9fafb", fg=C["text"], relief="flat", justify="left", bd=0)
entry.insert(0, "100")
canvas.create_window(30, 172, window=entry, anchor="w", width=300, height=30)

txt_from_lbl = canvas.create_text(30, 210, text=LANG["DE"]["from"], font=("Segoe UI", 8, "bold"), fill=C["muted"], anchor="w")
txt_to_lbl = canvas.create_text(210, 210, text=LANG["DE"]["to"], font=("Segoe UI", 8, "bold"), fill=C["muted"], anchor="w")

from_var = tk.StringVar(value="EUR")
om_from = tk.OptionMenu(root, from_var, *RATES.keys(), command=convert)
om_from.config(font=("Segoe UI", 11), bg="white", relief="flat", highlightthickness=1, highlightbackground=C["border"])
canvas.create_window(90, 235, window=om_from, width=130, height=34)

swap_btn = tk.Button(root, text="⇄", font=("Segoe UI", 13), bg=C["bg"], fg=C["muted"], relief="flat", command=swap)
canvas.create_window(180, 235, window=swap_btn, width=36, height=34)

to_var = tk.StringVar(value="JPY")
om_to = tk.OptionMenu(root, to_var, *RATES.keys(), command=convert)
om_to.config(font=("Segoe UI", 11), bg="white", relief="flat", highlightthickness=1, highlightbackground=C["border"])
canvas.create_window(270, 235, window=om_to, width=130, height=34)

btn_convert = tk.Button(root, text=LANG["DE"]["btn_convert"], font=("Segoe UI", 11, "bold"),
                        bg=C["teal"], fg=C["teal_light"], relief="flat", command=convert)
canvas.create_window(180, 290, window=btn_convert, width=320, height=38)

# Ergebnis-Bereich
canvas.create_rectangle(20, 318, 340, 450, fill=C["teal_light"], outline="")
txt_res_header = canvas.create_text(180, 345, text=LANG["DE"]["res_label"], font=("Segoe UI", 9), fill=C["teal"])

lbl_result = tk.Label(root, text="—", font=("Segoe UI", 28, "bold"), bg=C["teal_light"], fg=C["teal_dark"])
canvas.create_window(180, 383, window=lbl_result)

lbl_rate = tk.Label(root, text="", font=("Segoe UI", 9), bg=C["teal_light"], fg=C["teal"])
canvas.create_window(180, 430, window=lbl_rate)

entry.bind("<Return>", convert)
convert()
root.mainloop()