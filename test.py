from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from person import Person
from expense import Expense
from calculation import Calculation


class ExpenseApp(App):
    def build(self):
        self.team = []
        self.expenses = []
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Ustawienie nagłówka
        self.header = Label(text="Program rozlicza wydatki grupowe", font_size=20, size_hint=(1, None), height=40)
        self.layout.add_widget(self.header)

        # Dodanie pola do wpisania imion
        self.name_input = TextInput(hint_text="Podaj imiona uczestników (rozdzielone przecinkami)", size_hint=(1, None),
                                    height=40)
        self.layout.add_widget(self.name_input)

        # Przycisk do potwierdzenia imion
        self.submit_names_button = Button(text="Zatwierdź uczestników", size_hint=(1, None), height=40)
        self.submit_names_button.bind(on_press=self.create_team)
        self.layout.add_widget(self.submit_names_button)

        # Dodanie pola na wyświetlanie wydatków
        self.expense_button = Button(text="Dodaj wydatek", size_hint=(1, None), height=40)
        self.expense_button.bind(on_press=self.show_add_expense)
        self.layout.add_widget(self.expense_button)

        # Dodanie przestrzeni na wyświetlanie wyników rozliczeń
        self.result_label = Label(text="Wyniki rozliczenia pojawią się tutaj", size_hint=(1, None), height=40)
        self.layout.add_widget(self.result_label)

        return self.layout

    def create_team(self, instance):
        # Tworzenie zespołu na podstawie imion
        names = self.name_input.text.split(',')
        for name in names:
            self.team.append(Person(name.strip()))
        self.name_input.text = ""  # Czyścimy pole tekstowe po wprowadzeniu
        self.header.text = f"Uczestnicy: {', '.join([person.name for person in self.team])}"

    def show_add_expense(self, instance):
        # Pokazuje okno dodawania wydatku
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Pole na nazwę wydatku
        expense_name_input = TextInput(hint_text="Podaj nazwę wydatku", size_hint=(1, None), height=40)
        content.add_widget(expense_name_input)

        # Wybór osoby, która zapłaciła
        payer_label = Label(text="Wybierz osobę, która zapłaciła:")
        content.add_widget(payer_label)

        # Lista osób do wyboru
        payer_options = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        payer_buttons = []

        # Przechodzimy przez listę osób i tworzymy przyciski
        for idx, person in enumerate(self.team):
            button = Button(text=person.name, size_hint=(None, 1), width=100)

            # Korzystamy z domknięcia, aby przypisać 'idx' poprawnie do lambda
            button.bind(on_press=lambda btn, idx=idx: self.set_payer(expense_name_input, idx))

            payer_buttons.append(button)
            payer_options.add_widget(button)
        content.add_widget(payer_options)

        # Przycisk do zatwierdzenia wydatku
        submit_expense_button = Button(text="Zatwierdź wydatek", size_hint=(1, None), height=40)

        # Przekazanie expense_name_input do funkcji add_expense
        submit_expense_button.bind(on_press=lambda btn: self.add_expense(expense_name_input))
        content.add_widget(submit_expense_button)

        # Tworzenie popup'a
        popup = Popup(title="Dodaj wydatek", content=content, size_hint=(0.7, 0.7))
        popup.open()

    def set_payer(self, expense_name_input, idx):
        # Przechowujemy indeks osoby, która zapłaciła
        self.payer_idx = idx

    def add_expense(self, expense_name_input):
        # Dodanie wydatku
        expense_name = expense_name_input.text  # Teraz możemy użyć expense_name_input
        amount = float(
            expense_name_input.text)  # Zmienna amount powinna być obliczona na podstawie innego inputu (np. TextInput)
        beneficiaries = self.team  # Można dodać kod do wyboru beneficjentów
        expense = Expense(expense_name, self.team[self.payer_idx], amount, beneficiaries)
        self.expenses.append(expense)
        self.team[self.payer_idx].expenses.append(expense)

        # Przeliczenie i wyświetlenie wyników
        refunds = Calculation(self.team)
        self.result_label.text = str(refunds)


if __name__ == '__main__':
    ExpenseApp().run()
