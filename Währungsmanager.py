import tkinter as tk
from tkinter import ttk

# Daten & Konstanten
RATES = {
    "EUR": 1.0,
    "USD": 1.08,
    "GBP": 0.86,
    "CHF": 0.96,
    "JPY": 160.0,
    "CNY": 7.82,
    "SEK": 11.0,
    "BRL": 5.40,
    "RUB": 99.0,
    "ATS": 13.76,
}
SYMBOLS = {
    "EUR": "€",
    "USD": "$",
    "GBP": "£",
    "CHF": "Fr.",
    "JPY": "¥",
    "CNY": "¥",
    "SEK": "kr",
    "BRL": "R$",
    "RUB": "₽",
    "ATS": "öS",
}
FLAGS = {
    "EUR": "🇪🇺", "USD": "🇺🇸", "GBP": "🇬🇧", "CHF": "🇨🇭",
    "JPY": "🇯🇵", "CNY": "🇨🇳", "SEK": "🇸🇪", "BRL": "🇧🇷",
    "RUB": "🇷🇺", "ATS": "🇦🇹",
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
        "invalid": "Ungültige Eingabe",
        "rate_label": "Kurs:",
    },
    "EN": {
        "title": "Currency Converter",
        "subtitle": "Convert fast & easy",
        "amount": "AMOUNT",
        "from": "FROM",
        "to": "TO",
        "btn_convert": "Convert",
        "res_label": "Result",
        "invalid": "Invalid Input",
        "rate_label": "Rate:",
    }
}

# Farbpalette – modernes Teal-Grün + warme Akzente
C = {
    "bg":         "#F0F4F3",
    "card":       "#FFFFFF",
    "teal":       "#0F6E56",
    "teal_light": "#E1F5EE",
    "teal_mid":   "#5DCAA5",
    "teal_dark":  "#085041",
    "accent":     "#1D9E75",
    "text":       "#1A2E26",
    "muted":      "#6B8A7E",
    "border":     "#C8DDD7",
    "input_bg":   "#F7FAF9",
    "btn_hover":  "#0A5944",
    "white":      "#FFFFFF",
}

W = 400
H = 520
current_lang = "DE"


def format_currency(amount, code):
    sym = SYMBOLS[code]
    if code == "JPY":
        return f"{sym} {amount:,.0f}"
    return f"{sym} {amount:,.2f}"


def convert(*_):
    try:
        val = entry.get().replace(",", ".").strip()
        amount = float(val)
        rate = RATES[to_var.get()] / RATES[from_var.get()]
        result = amount * rate
        lbl_result.config(text=format_currency(result, to_var.get()))
        rate_text = f"1 {from_var.get()} = {rate:.4f} {to_var.get()}"
        lbl_rate.config(text=rate_text)
        # Grüner Akzent wenn Ergebnis da
        canvas.itemconfig(result_rect, fill=C["teal_light"])
    except Exception:
        lbl_result.config(text=LANG[current_lang]["invalid"])
        lbl_rate.config(text="")


def swap():
    f, t = from_var.get(), to_var.get()
    from_var.set(t)
    to_var.set(f)
    update_dropdowns()
    convert()


def update_dropdowns():
    # Beschriftung mit Flagge
    om_from["menu"].delete(0, "end")
    om_to["menu"].delete(0, "end")
    for code in RATES:
        label = f"{FLAGS[code]}  {code}"
        om_from["menu"].add_command(label=label, command=lambda c=code: (from_var.set(c), update_from_label(), convert()))
        om_to["menu"].add_command(label=label, command=lambda c=code: (to_var.set(c), update_to_label(), convert()))
    update_from_label()
    update_to_label()


def update_from_label():
    c = from_var.get()
    from_var_display.set(f"{FLAGS[c]}  {c}")


def update_to_label():
    c = to_var.get()
    to_var_display.set(f"{FLAGS[c]}  {c}")


def switch_language():
    global current_lang
    current_lang = "EN" if current_lang == "DE" else "DE"
    l = LANG[current_lang]
    canvas.itemconfig(txt_title, text=l["title"])
    canvas.itemconfig(txt_subtitle, text=l["subtitle"])
    canvas.itemconfig(txt_amt_lbl, text=l["amount"])
    canvas.itemconfig(txt_from_lbl, text=l["from"])
    canvas.itemconfig(txt_to_lbl, text=l["to"])
    canvas.itemconfig(txt_res_header, text=l["res_label"])
    btn_convert.config(text=l["btn_convert"])
    btn_lang.config(text=f"🌐  {current_lang}")
    convert()


# ── Hauptfenster ──────────────────────────────────────────────
root = tk.Tk()
root.title("Währungsrechner")
root.configure(bg=C["bg"])
root.resizable(False, False)

canvas = tk.Canvas(root, width=W, height=H, bg=C["bg"], highlightthickness=0)
canvas.pack(padx=24, pady=24)

# ── Karte (abgerundetes Rechteck simulieren via überlappende Formen) ──
RADIUS = 18
# Hintergrund-Card
canvas.create_rectangle(RADIUS, 0, W - RADIUS, H, fill=C["card"], outline="")
canvas.create_rectangle(0, RADIUS, W, H - RADIUS, fill=C["card"], outline="")
for dx, dy in [(0, 0), (W - 2*RADIUS, 0), (0, H - 2*RADIUS), (W - 2*RADIUS, H - 2*RADIUS)]:
    canvas.create_arc(dx, dy, dx + 2*RADIUS, dy + 2*RADIUS,
                      start=[90, 0, 180, 270][[dx == 0 and dy == 0,
                                               dx != 0 and dy == 0,
                                               dx == 0 and dy != 0,
                                               dx != 0 and dy != 0].index(True)],
                      extent=90, fill=C["card"], outline="")
# Äußerer Rand
canvas.create_rectangle(1, 1, W - 1, H - 1, outline=C["border"], width=1, fill="")

# ── Header-Streifen ──
canvas.create_rectangle(0, 0, W, 72, fill=C["teal"], outline="")
# Runde Ecken oben
for x in [0, W - 2*RADIUS]:
    canvas.create_arc(x, 0, x + 2*RADIUS, 2*RADIUS, start=90 if x == 0 else 0,
                      extent=90, fill=C["teal"], outline="")

# ── Sprach-Button ──
btn_lang = tk.Button(root, text=f"🌐  {current_lang}",
                     font=("Segoe UI", 8, "bold"),
                     bg=C["teal_dark"], fg=C["teal_light"],
                     relief="flat", bd=0, padx=6, pady=3,
                     cursor="hand2", command=switch_language,
                     activebackground=C["teal_dark"], activeforeground=C["white"])
canvas.create_window(W - 46, 20, window=btn_lang, width=72, height=26)

# ── Titel ──
txt_title = canvas.create_text(
    W // 2, 30, text=LANG["DE"]["title"],
    font=("Segoe UI", 17, "bold"), fill=C["white"])
txt_subtitle = canvas.create_text(
    W // 2, 53, text=LANG["DE"]["subtitle"],
    font=("Segoe UI", 9), fill=C["teal_light"])

# ── Betrag ──
txt_amt_lbl = canvas.create_text(
    28, 92, text=LANG["DE"]["amount"],
    font=("Segoe UI", 8, "bold"), fill=C["muted"], anchor="w")

canvas.create_rectangle(20, 104, W - 20, 142,
                         fill=C["input_bg"], outline=C["border"], width=1)
entry = tk.Entry(root, font=("Segoe UI", 20, "bold"),
                 bg=C["input_bg"], fg=C["text"],
                 relief="flat", justify="left", bd=0,
                 insertbackground=C["teal"])
entry.insert(0, "100")
canvas.create_window(32, 123, window=entry, anchor="w", width=330, height=30)

# ── Von / Nach Labels ──
txt_from_lbl = canvas.create_text(
    28, 160, text=LANG["DE"]["from"],
    font=("Segoe UI", 8, "bold"), fill=C["muted"], anchor="w")
txt_to_lbl = canvas.create_text(
    W // 2 + 10, 160, text=LANG["DE"]["to"],
    font=("Segoe UI", 8, "bold"), fill=C["muted"], anchor="w")

# ── Dropdowns mit Flaggen ──
from_var = tk.StringVar(value="EUR")
to_var = tk.StringVar(value="USD")
from_var_display = tk.StringVar(value=f"{FLAGS['EUR']}  EUR")
to_var_display = tk.StringVar(value=f"{FLAGS['USD']}  USD")

menu_font = ("Segoe UI", 10)

om_from = tk.OptionMenu(root, from_var_display, "")
om_from.config(font=menu_font, bg=C["white"], fg=C["text"],
               relief="flat", highlightthickness=1,
               highlightbackground=C["border"], indicatoron=True,
               activebackground=C["teal_light"], activeforeground=C["teal_dark"],
               bd=0, padx=6)
canvas.create_window(110, 190, window=om_from, width=170, height=34)

swap_btn = tk.Button(root, text="⇄",
                     font=("Segoe UI", 14, "bold"),
                     bg=C["teal_light"], fg=C["teal_dark"],
                     relief="flat", bd=0, cursor="hand2",
                     activebackground=C["teal_mid"], activeforeground=C["white"],
                     command=swap)
canvas.create_window(W // 2, 190, window=swap_btn, width=40, height=34)

om_to = tk.OptionMenu(root, to_var_display, "")
om_to.config(font=menu_font, bg=C["white"], fg=C["text"],
             relief="flat", highlightthickness=1,
             highlightbackground=C["border"],
             activebackground=C["teal_light"], activeforeground=C["teal_dark"],
             bd=0, padx=6)
canvas.create_window(W - 110, 190, window=om_to, width=170, height=34)

# ── Umrechnen-Button ──
btn_convert = tk.Button(
    root, text=LANG["DE"]["btn_convert"],
    font=("Segoe UI", 11, "bold"),
    bg=C["teal"], fg=C["white"],
    relief="flat", bd=0, cursor="hand2",
    activebackground=C["btn_hover"], activeforeground=C["white"],
    command=convert)
canvas.create_window(W // 2, 245, window=btn_convert, width=W - 40, height=40)

# ── Trennlinie ──
canvas.create_line(20, 275, W - 20, 275, fill=C["border"], width=1)

# ── Ergebnis-Bereich ──
result_rect = canvas.create_rectangle(
    20, 285, W - 20, H - 20,
    fill=C["teal_light"], outline=C["border"], width=1)

txt_res_header = canvas.create_text(
    W // 2, 308, text=LANG["DE"]["res_label"],
    font=("Segoe UI", 9, "bold"), fill=C["teal"])

# Dekoratives Kreissymbol
canvas.create_oval(W // 2 - 22, 320, W // 2 + 22, 364,
                   fill=C["teal_light"], outline=C["teal_mid"], width=2)
canvas.create_text(W // 2, 342, text="=",
                   font=("Segoe UI", 18, "bold"), fill=C["teal"])

lbl_result = tk.Label(root, text="—",
                       font=("Segoe UI", 30, "bold"),
                       bg=C["teal_light"], fg=C["teal_dark"])
canvas.create_window(W // 2, 410, window=lbl_result)

lbl_rate = tk.Label(root, text="",
                     font=("Segoe UI", 9),
                     bg=C["teal_light"], fg=C["teal"])
canvas.create_window(W // 2, 458, window=lbl_rate)

# ── Menü-Einträge befüllen ──
update_dropdowns()

# ── Bindings ──
entry.bind("<Return>", convert)
entry.bind("<KeyRelease>", convert)

convert()
root.mainloop()
