# IJsboer Tracker
## Data Governance Werkblad

**Project:** IJsboer Tracker
**Klant:** Tijsse Klasen — IJs van Tijs / Tijsse Klasen Foodtrucks
**Opgesteld door:** Shan Brunel
**Datum:** 12 juni 2026
**Versie:** 1.0

> Dit document beschrijft welke (persoons)gegevens de IJsboer Tracker verwerkt, waarom, op welke
> grondslag en hoe lang. Het maakt deel uit van het overdrachtsdossier.

---

## 1. Databronnen

| DATABRON | EIGENAAR | TYPE GEGEVENS | PERSOONSGEGEVENS? | VERWERKINGSBASIS (AVG) | DOEL & NOODZAAK |
|---|---|---|---|---|---|
| Live GPS-positie ijsboer | Tijsse Klasen | `lat`, `lng` (coördinaten), `updated_at` (tijdstip), `is_active` (rijdt ja/nee) | Ja — locatie van een identificeerbare persoon (de bestuurder) | Gerechtvaardigd belang (eigen bedrijfsvoering); de betrokkene is tevens verwerkingsverantwoordelijke en deelt zijn positie actief via de Start/Stop-knop | Klanten op de website kunnen zien waar de ijsbus nu rijdt. Alleen de huidige positie is nodig; er wordt bewust niets méér verzameld (geen naam, gedrag, identiteit van klanten of historie). |

*Verwerkingsbasis: Toestemming · Overeenkomst · Wettelijke verplichting · Gerechtvaardigd belang*

*Doel & noodzaak (dataminimalisatie, AVG art. 5): de tracker verwerkt uitsluitend de actuele coördinaten van de ijsbus tijdens een rit. Geen klantgegevens, geen identificerende gegevens van websitebezoekers, geen rithistorie. Dit is het minimum dat nodig is om de kaart te laten werken.*

**Wat het systeem nadrukkelijk NIET verwerkt:**

- Geen persoonsgegevens van websitebezoekers (klanten bekijken alleen de kaart; er worden geen accounts, cookies of bezoekersdata opgeslagen door de applicatie).
- Geen historische routes of bewegingspatronen — alleen de laatst bekende positie.
- Geen namen, adressen, betaalgegevens of contactgegevens.

---

## 2. Datakwaliteit

| DATABRON | VOLLEDIGHEID | ACTUALITEIT | NAUWKEURIGHEID | OPMERKING |
|---|---|---|---|---|
| Live GPS-positie | Goed (zolang de rit actief is) | Hoog — ververst elke 30 seconden | Afhankelijk van de GPS van de telefoon van de ijsboer | Bij slecht GPS-signaal kan de positie kort afwijken; dit corrigeert zichzelf bij de volgende update. |

**Bekende beperkingen:**

- De positie wordt alleen bijgewerkt zolang de ijsboer de PWA op de voorgrond heeft staan (Safari/Chrome). Wordt de app weggeswipet, dan stopt het bijwerken tot hij hem heropent.
- Bij herstart van de server verdwijnt de laatst bekende positie (zie §4).

---

## 3. Data-eigenaarschap

| ROL | NAAM | VERANTWOORDELIJKHEID |
|---|---|---|
| Verwerkingsverantwoordelijke / data-eigenaar | Tijsse Klasen | Beslissingsbevoegdheid over gebruik; bepaalt zelf wanneer hij deelt (Start/Stop) |
| Data-beheerder (operationeel) | Tijsse Klasen | Start en stopt het delen per rit |
| Technisch beheer | Shan Brunel | Beheer van de broncode (GitHub); geen toegang tot of opslag van de gegevens |
| Verwerker (infrastructuur) | Railway (hosting) | Draait de server waarop de positie tijdelijk in het werkgeheugen staat |

> De positie van de ijsboer is gegevens van Tijsse zélf. Hij is zowel de betrokkene als de
> verantwoordelijke en houdt via de Start/Stop-knop volledige controle over wanneer er gedeeld wordt.

---

## 4. Opslag en beveiliging

| ASPECT | BESCHRIJVING |
|---|---|
| Opslaglocatie | Uitsluitend in het werkgeheugen van de server (in-memory). Eén enkele actuele positie, die bij elke update wordt overschreven. **Geen database, geen bestand, geen logbestand met posities.** |
| Toegangsbeheer | De kaart-API (`GET /api/location`) is openbaar — dat is bewust, want de positie is bedoeld om publiek getoond te worden op de website. |
| Versleuteling | Verkeer verloopt via HTTPS (verzorgd door Railway). |
| Back-upbeleid | Geen back-up — de positie is vluchtig en hoeft niet bewaard te worden. |
| Bewaartermijn | **Geen.** Er is alleen de actuele positie. Bij `Stop` blijft de laatst bekende positie in het geheugen staan met de status "niet onderweg", waardoor de pin van de kaart verdwijnt. Bij een herstart van de server verdwijnt ook die laatste positie volledig. |
| Verwijderingsprocedure na bewaartermijn | Niet van toepassing — er wordt niets persistent opgeslagen. Een herstart wist de in-memory positie. |

---

## 5. Verversing en updates

| ASPECT | BESCHRIJVING |
|---|---|
| Hoe vaak wordt de data bijgewerkt? | Elke 30 seconden tijdens een actieve rit (de PWA stuurt de positie naar de server). |
| Wie is verantwoordelijk voor updates? | Gebeurt automatisch zolang de ijsboer de app open heeft; geen handmatige actie nodig. |
| Hoe worden wijzigingen bijgehouden? | Niet — er is geen historie. Elke nieuwe positie overschrijft de vorige. |

---

## 6. Bekende risico's

| RISICO | ERNST | MAATREGEL |
|---|---|---|
| De POST-endpoints (`/api/location`, `/api/location/stop`) zijn niet afgeschermd; in theorie kan iemand die de URL kent een valse positie sturen | Laag | Acceptabel voor deze MVP: de impact is hooguit een tijdelijk verkeerde pin op de kaart, geen datalek. Bij uitbreiding (Fase 2) een eenvoudige sleutel/token toevoegen. |
| CORS staat momenteel alle domeinen toe (`allow_origins=["*"]`) | Laag | Aanscherpen naar het echte domein (`ijsvantijs.nl`) zodra dat definitief is. |
| Locatie van de ijsboer is publiek zichtbaar tijdens een rit | Laag | Bewuste keuze en kerndoel van de app; de ijsboer bepaalt zelf met Start/Stop wanneer hij zichtbaar is. |

---

## 7. Vooruitblik Fase 2 — let op

Zodra Fase 2 wordt gebouwd (voorspelde aankomsttijd op basis van gelogde GPS-traces), **verandert dit
profiel wezenlijk**: er komt dan wél persistente opslag van rithistorie in een database. Op dat moment
moeten opnieuw worden vastgelegd:

- **Bewaartermijn** van de gelogde ritten (hoe lang worden traces bewaard?).
- **Doelbinding** — de rithistorie mag alleen gebruikt worden voor het berekenen van aankomsttijden, niet voor andere doeleinden.
- **Verwijderingsprocedure** voor oude traces.

Dit werkblad moet bij de start van Fase 2 worden herzien.

---

## 8. Akkoordverklaring

Opdrachtgever bevestigt dat bovenstaande beschrijving correct is en dat de genoemde verwerkingsgronden van toepassing zijn.

**Handtekening opdrachtgever:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ **Datum:** \_\_\_\_\_\_\_\_\_\_

*Dit document maakt deel uit van het overdrachtsdossier van de IJsboer Tracker.*
