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


# UI

-


# Database


# User Management


# Department Management


Finance













UI:
Admin-Einstellungen Tab:

Abteilungen hinzufügen Tab:

Berichte Tab:

Finanzen Tab:
withdraw_money()
Known Error: Eine Fehlermeldung trotz erfolgreichem Abschluss der Operation.

