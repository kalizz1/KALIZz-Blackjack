import tkinter as tk
import random

# Kart destesi ve değerleri
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {rank: min(10, i + 2) for i, rank in enumerate(ranks)}
values['A'] = 11

class YesilinBlackJacki:
    def __init__(self, root):
        self.root = root
        self.root.title("kalizz BlackJack")
        self.root.geometry("600x400")
        self.root.configure(bg="#004d00")  # Daha koyu yeşil

        self.balance = 1000  # Başlangıç bakiyesi
        self.bet = 0
        self.player_hand = []
        self.dealer_hand = []

        self.create_menu()

    def create_menu(self):
        """Başlangıç menüsü."""
        self.clear_window()

        self.balance_label = tk.Label(self.root, text=f"Bakiye: ${self.balance} Yeşil Coin", font=("Arial", 16), bg="#004d00", fg="white")
        self.balance_label.pack(pady=10)

        self.bet_label = tk.Label(self.root, text="Bahis Miktarını Girin:", font=("Arial", 14), bg="#004d00", fg="white")
        self.bet_label.pack(pady=5)

        self.bet_entry = tk.Entry(self.root, font=("Arial", 14))
        self.bet_entry.pack(pady=5)

        self.bet_button = tk.Button(self.root, text="Bahis Yap", font=("Arial", 14), command=self.place_bet)
        self.bet_button.pack(pady=10)

        if self.balance < 5:
            self.add_coins_button = tk.Button(self.root, text="Yeşil Coin Ekle", font=("Arial", 12), bg="black", fg="white", command=self.add_coins_screen)
            self.add_coins_button.pack(pady=20)

    def add_coins_screen(self):
        """Yeşil Coin yükleme ekranı."""
        self.clear_window()

        self.panel = tk.Frame(self.root, bg="black", padx=20, pady=20)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(self.panel, text="Kalizz e Borçlusun Dostum!", font=("Arial", 16, "italic", "bold"), bg="black", fg="#00ff00")
        title.pack(pady=10)

        instruction = tk.Label(self.panel, text="Yeşil Coin Miktarını Girin (5-1000):", font=("Arial", 12), bg="black", fg="white")
        instruction.pack(pady=5)

        self.coin_entry = tk.Entry(self.panel, font=("Arial", 12))
        self.coin_entry.pack(pady=5)

        load_button = tk.Button(self.panel, text="Yükle", font=("Arial", 14), command=self.load_coins)
        load_button.pack(pady=10)

    def load_coins(self):
        """Yeşil Coin yükler."""
        try:
            amount = int(self.coin_entry.get())
            if amount < 5 or amount > 1000:
                raise ValueError
            self.balance += amount
            self.panel.destroy()
            self.show_message("Başarıyla Kalizz'e Borçlandınız o.e")
        except ValueError:
            self.show_message("Geçerli bir miktar girin! (5-1000)")

    def show_message(self, message):
        """Mesaj görüntüler."""
        message_label = tk.Label(self.root, text=message, font=("Arial", 14), bg="black", fg="white", pady=10)
        message_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.after(2000, lambda: [message_label.destroy(), self.create_menu()])

    def place_bet(self):
        """Bahis miktarını alır."""
        try:
            bet = int(self.bet_entry.get())
            if bet < 5 or bet > self.balance:
                raise ValueError
            self.bet = bet
            self.start_game()
        except ValueError:
            self.show_message("Bahis en az 5, en fazla bakiyeniz kadar olmalıdır.")

    def start_game(self):
        """Oyunu başlatır."""
        self.clear_window()
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]

        self.balance_label = tk.Label(self.root, text=f"Bakiye: ${self.balance} Yeşil Coin", font=("Arial", 16), bg="#004d00", fg="white")
        self.balance_label.pack(pady=10)

        self.dealer_label = tk.Label(self.root, text="Krupiyenin Eli: [Gizli]", font=("Arial", 14), bg="#004d00", fg="white")
        self.dealer_label.pack(pady=10)

        self.player_label = tk.Label(self.root, text=f"Eliniz: {', '.join(self.player_hand)}", font=("Arial", 14), bg="#004d00", fg="white")
        self.player_label.pack(pady=10)

        self.action_frame = tk.Frame(self.root, bg="#004d00")
        self.action_frame.pack(pady=20)

        self.hit_button = tk.Button(self.action_frame, text="Kart Çek", font=("Arial", 14), command=self.hit)
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = tk.Button(self.action_frame, text="Pas Geç", font=("Arial", 14), command=self.stand)
        self.stand_button.grid(row=0, column=1, padx=10)

    def hit(self):
        """Oyuncu kart çeker."""
        self.player_hand.append(self.deal_card())
        self.update_player_hand()

        if self.calculate_hand(self.player_hand) > 21:
            self.end_round("Eliniz 21'i geçti! Kaybettiniz.", win=False)

    def stand(self):
        """Krupiye oynar ve sonucu kontrol eder."""
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())

        self.update_dealer_hand()
        player_total = self.calculate_hand(self.player_hand)
        dealer_total = self.calculate_hand(self.dealer_hand)

        if dealer_total > 21 or player_total > dealer_total:
            self.end_round("Tebrikler! Kazandınız!", win=True)
        elif player_total < dealer_total:
            self.end_round("Kaybettiniz! Daha iyi şanslar.", win=False)
        else:
            self.end_round("Berabere!", win=None)

    def end_round(self, message, win):
        """Sonuç mesajını ve bakiye güncellemelerini yapar."""
        if win is True:
            self.balance += self.bet * 2
        elif win is False:
            self.balance -= self.bet

        self.clear_window()
        result_frame = tk.Frame(self.root, bg="black", padx=20, pady=20)
        result_frame.pack(pady=50)

        result_label = tk.Label(result_frame, text=message, font=("Arial", 14), bg="black", fg="white")
        result_label.pack(pady=10)

        replay_button = tk.Button(result_frame, text="Tekrar Oyna", font=("Arial", 14), command=self.create_menu)
        replay_button.pack(pady=10)

    def deal_card(self):
        """Deste içerisinden bir kart çeker."""
        suit = random.choice(suits)
        rank = random.choice(ranks)
        return f"{rank}{suit}"

    def calculate_hand(self, hand):
        """Bir elin toplam değerini hesaplar."""
        total = sum(values[card[:-1]] for card in hand)
        aces = sum(card.startswith('A') for card in hand)
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def update_player_hand(self):
        """Oyuncunun elini günceller."""
        self.player_label.config(text=f"Eliniz: {', '.join(self.player_hand)}")

    def update_dealer_hand(self):
        """Krupiyenin elini günceller."""
        self.dealer_label.config(text=f"Krupiyenin Eli: {', '.join(self.dealer_hand)}")

    def clear_window(self):
        """Pencereyi temizler."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = YesilinBlackJacki(root)
    root.mainloop()
