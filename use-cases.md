# Use cases

## 1 Besucherinnen ohne Login
### 1.1 Besucherinnen besucht Seite
Bedingung: keine
1.1.1 Besucherin sieht Seite mit allen offenen Stellvertretungen, Der Bewerbungsknopf ist ausgeblendet. Unter dem Titel erscheint eine Aufforderung zum Login und Anleitung zum Antrag eines Kontos
1.1.2 Besucherin kann auf dieser Liste Suchen, falls sie ein Konto hat, kann sie sich einloggen und [Usercase 2](#2-besucherinnen-mit-login--kandidatinnen) wird relevant

## 2 Besucherinnen mit Login = Kandidatinnen
Bedingung: user hat ein Login un dist eingeloggt.
2.1 Kandidatin sucht Stellvertretung
2.1.1 Kandidatin hat Auswahl aller Stellvertretungen zur Verfügung, die nicht besetzt und noch nicht abgeschlossen sind.
2.1.2 Kandidatin setzt Filter und löst Suche aus
2.1.3 App gibt gefilterete Stellvertretungen zurück
2.1.4 Kandidaten drückt auf gewünschter Stellvertertung Bewerben-Button

2.2 Kandidatin bewirbt sich
2.2.1 Kandidatin füllt Formular-Feld aus und schickt Bewerbung ab. 
2.2.2 Adminstration erhält email, folge siehe Usecase 

2.3 Kandidatin ändert das eigene Profil
Insbesondere die möglichen Tage, an denen Stellvertretungen übernommen werden können, müssen von den Kandidatinnen selbst bewirtschaftet werden.  

2.4 Kandidatin ändert Passwort

## 3 Administation
Personen, die er Gruppe Administration zugeordnet sind, sehen neben der öffentlichen Stellvertretungsliste auch diverse ande Menueinträge und können alle Elemente editieren
3.1 Adminstration erhält Bewerbung
3.1.1 Administration erhält Bewerbung per Email
3.1.2 Sie klickt auf Link in Email und öffnet die Bewerbungs-Bearbeitungsmaske 
3.1.3 Sie klickt auf Bestägigen, und ergänzt falls nötig den Standardtext

### Administration sucht Stellvertretungen
Diese Liste erlaubt eine Suche auch über vergangene Stellvertetungen, jede Stellvertretung kann entweder 

## Superuser
Superuser haben zusätzlich die Möglichkeit, Codes zu editieren, neue Schulen anzulegen etc.


# Fragen
1.1.1 Soll der Antrag für ein Konto durch den Kandidaten selbst erfolgen können? Annahme nein, wegen potentiellem Missbrauch durch Schülerinnnen.
2.2.1 Muss hier scon eine Bwerbung per SMS möglich sein? 
3.1.3 soll eine Bestätigung automatisch erfolgen? die Idee bei der manuellen Bestätigung wäre, dass man damit sicherstellt, dass eine Person die Bewerbung gesehen hat. 