__author__ = "5158850, Novgorodtseva, 8392145, Reich"

# General

Das Vereinskassensystem ist eine grafische Benutzeroberfläche (GUI) zur Verwaltung der Finanzen eines Vereins.
Es ermöglicht Administratoren, Abteilungen zu verwalten, Finanztransaktionen durchzuführen und eine Transaktionshistorie
einzusehen.

Features:
- Benutzerverwaltung (Admins können Benutzer hinzufügen)
- Abteilungsverwaltung (Neue Abteilungen erstellen, Salden verwalten)
- Einzahlungen, Abhebungen & Überweisungen zwischen Abteilungen
- Transaktionshistorie mit Export-Funktion (CSV)
- Login-System mit verschiedenen Benutzerrollen
- SQLite-Datenbank zur Speicherung der Finanzdaten


# Verwendung

Login:
1. Benutzername und Passwort eingeben
2. Rolle wird automatisch erkannt

3. Abteilungen verwalten:
- Neue Abteilungen hinzufügen
- Startsaldo festlegen

4. Finanzoperationen:
- Geld einzahlen
- Geld abheben (kein negatives Guthaben erlaubt!)
- Geld zwischen Abteilungen überweisen
- Transaktionshistorie anzeigen & exportieren

5. Transaktionshistorie
- aktualisieren
- mit der Rolle Admin als csv exportieren

!!! Achtung !!!

Alle Komma-Zahlen müsse einen Punkt statt Komma haben!


# UI #
__init__(self, db_name="app_data.db")
"Initialisiert die UI."

 center_window(self, window, width, height)
"Zentriert alle Fenster auf dem Bildschirm."

add_department_tab(self, tab)
"Fügt die Abteilungsverwaltungsfunktionen zum Tab hinzu."

create_admin_settings_tab(self, parent_tab)
"Erstellt den Tab für die Benutzerverwaltung."

show_department_balance(self)
"Diese Funktion wird für den Button verwendet, der das Guthaben eines bestimmten Abteilungskontos anzeigt."

deposit_money(self)
"Diese Funktion zahlt Geld auf das Konto einer Abteilung ein."

handle_deposit(self)
"Diese Funktion wird ausgeführt, wenn der Button 'Geld einzahlen' geklickt wird."

withdraw_money(self)
"Diese Funktion hebt Geld vom Abteilungskonto ab."

handle_withdraw(self)
"Diese Funktion wird ausgeführt, wenn der Button 'Geld abheben' geklickt wird - sie liest den Betrag aus dem Eingabefeld
und ruft die Funktion reduce_balance() aus dem Finanzmodul auf."

transfer_money(self)
"Diese Funktion überweist Geld von einer Abteilung zu einer anderen."

handle_transfer(self)
"Überweist Geld von einer Abteilung in eine andere."

create_finance_tab(self, tab)
"Erstellt die UI-Elemente für den Finanz-Tab."

create_transaction_history_tab(self, tab)
"Erstellt die UI für die Transaktionshistorie."

load_transaction_history(self)
"Lädt die Transaktionshistorie."

export_to_csv(self)
"Exportiert die Transaktionshistorie als CSV-Datei."

open_main_window(self, role)
"Erstellt und zeigt das Hauptfenster an."

get_accessible_tabs(self, role)
"Gibt die Tabs basierend auf der Benutzerrolle zurück."

open_login_window(self)
"Erstellt das Login-Fenster."


# Database #
setup_database(self)
"Initialisiert die Datenbank und baut die Tabellen."

verify_logi(self, username, password)
"Überprüft die Logindaten eines Users."

update_user_role(self, username, new_role)
"Aktualisiert die Rolle eines Users."

add_department(self, name, initial_balance)
"Fügt eine Abteilung hinzu."

debug_database(self)
"Gibt alle user im Terminal aus (für Debugging-Zwecke)"


# User Management #
add_new_user(self, db_manager)
"Initialisiert das User-Management mit einem Datenbank-Manager-Objekt."

update_user_role(self, username, new_role)
"Aktualisiert die User_Rolle. (Rolleneinstellungen haben nicht richtig funktioniert)"

verify_login(self, username, password)
"Überprüft die Login-Daten eines Users und gibt seine Rolle zurück."


# Department Management #
__init__(self, db_manager)
"Initialisiert die Abteilungsverwaltung mit einem Datenbank-Manager-Objekt."

add_department(self, name, initial_balance)
"Fügt eine neue Abteilung hinzu."

get_departments(self)
"Ruft alle Abteilungen aus der Datenbank ab."

update_department_balance(self, department_id, new_balance)
"Aktualisiert den Kontostand einer Abteilung."

# Finance
add_balance(self, department_name, amount)
"Fügt einer Abteilung einen bestimmten Betrag zum Guthaben hinzu - speichert die Transaktion in der Historie."

reduce_balance(self, department_name, amount)
"Reduziert das Guthaben einer Abteilung um einen bestimmten Betrag - stellt sicher, dass das Guthaben nicht negativ wird
- speichert die Transaktion in der Historie."

record(self, department_name, type, amount, new_balance)
"Speichert eine Transaktion in der Datenbank - erstellt die Tabelle 'history', falls sie noch nicht existiert."

get_transaction_history(self)
"Gibt die gesamte Transaktionshistorie zurück."
