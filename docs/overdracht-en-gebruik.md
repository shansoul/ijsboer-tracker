# IJsboer Tracker — Overdracht en gebruikshandleiding

---

## Deel 1: Voor de ijsboer — Railway account aanmaken

De tracker draait op een server die Railway heet. Die moet op jouw naam komen te staan.
Je betaalt hiervoor **$5 per maand** (automatisch via creditcard of PayPal).

### Stap 1: Account aanmaken

1. Ga op je computer naar **railway.app**
2. Klik rechtsboven op **"Login"**
3. Klik op **"Sign up"** en maak een account aan met je e-mailadres
4. Bevestig je e-mailadres (check je inbox en klik op de link in de mail)

### Stap 2: Betaalplan activeren (Hobby plan, $5/mnd)

Dit is nodig zodat de server nooit automatisch stopt.

1. Log in op **railway.app**
2. Klik rechtsboven op je profielfoto → **"Account Settings"**
3. Klik in het linkermenu op **"Billing"**
4. Klik op **"Upgrade to Hobby Plan"**
5. Vul je creditcard- of PayPal-gegevens in en bevestig

### Stap 3: Geef je Railway e-mailadres door

Stuur het e-mailadres waarmee je je hebt aangemeld bij Railway door aan je contactpersoon (de ontwikkelaar). Die zorgt voor de overdracht van de tracker naar jouw account.

### Stap 4: Uitnodiging accepteren

Je ontvangt twee e-mails van Railway:
1. Eerst een **uitnodiging** — klik op "Accept Invite"
2. Daarna een **overdrachtsverzoek** — klik op "Accept Transfer"

Dat is alles. De tracker draait nu op jouw account en de kosten lopen via jou.

---

## Deel 2: Voor de webman — drie aanpassingen op de website

Er zijn drie dingen die op de website van de ijsboer moeten worden aangepast.

---

### Aanpassing 1: Start/Stop-knop uploaden

De ijsboer heeft een pagina nodig op zijn eigen website vanwaarop hij de tracker kan starten en stoppen. Hiervoor moet je drie bestanden uploaden naar de server.

**Upload deze bestanden** (bijgesloten) naar een map op de server, bijvoorbeeld `/tracker-app/`:
- `index.html`
- `app.js`
- `Ijsbus.png`

De ijsboer krijgt daarna de link **ijsvantijs.nl/tracker-app/** op zijn telefoon.

> Kies zelf de mapnaam — het maakt niet uit hoe die heet, zolang je de link daarna doorgeeft aan de ijsboer.

---

### Aanpassing 2: Kaart op Wijchen zetten (was Amsterdam)

In de bestaande kaartcode op `ijsvantijs.nl/ijstracker/` staat de kaart ingesteld op Amsterdam. Dit moet Wijchen worden.

Zoek in de code naar deze regel:

```js
.setView([52.3676, 4.9041], 15)
```

Vervang die door:

```js
.setView([51.8103, 5.7238], 12)
```

---

### Aanpassing 3: IJsbus-icoontje verplaatsen naar eigen server

Het icoontje van de ijsbus staat nu op een externe server. Dit moet verplaatst worden naar jullie eigen server, zodat het altijd blijft werken.

Je hebt `Ijsbus.png` al geüpload in aanpassing 1. Zoek nu in de kaartcode naar deze regel:

```js
iconUrl: "https://shansoul.github.io/ijsboer-tracker/Ijsbus.png"
```

Vervang die door het pad op jullie eigen server, bijvoorbeeld:

```js
iconUrl: "https://ijsvantijs.nl/tracker-app/Ijsbus.png"
```

> Pas het pad aan naar waar je `Ijsbus.png` hebt geüpload.

---

### Testen na de aanpassingen

1. Ga naar `ijsvantijs.nl/ijstracker/` — de kaart moet Wijchen tonen (niet Amsterdam) en het ijsbus-icoontje mag geen vraagteken zijn
2. Open `ijsvantijs.nl/tracker-app/` op een telefoon en druk op **Start** — de ijsbus moet op de kaart verschijnen
3. Druk op **Stop** — de ijsbus verdwijnt

---

## Deel 3: Gebruiksinstructie — elke zaterdag

### Wat de ijsboer doet

**Voordat je vertrekt:**

1. Open **Safari** op je iPhone
2. Ga naar de link die je van je contactpersoon hebt gekregen *(ijsvantijs.nl/tracker-app/ of vergelijkbaar)*
3. Druk op de grote blauwe **Start** knop
4. Als Safari vraagt of je je locatie wilt delen: kies **"Toestaan"**
5. De knop wordt rood — je locatie wordt nu gedeeld op de website

**Tijdens de rit:**

- Leg je telefoon in de houder met het **scherm aan**
- Laat Safari op de voorgrond staan — swipe de app niet weg
- Je hoeft verder niets te doen. De kaart op de website wordt automatisch elke 30 seconden bijgewerkt

**Na de rit:**

- Druk op de rode **Stop** knop
- De ijsbus verdwijnt van de kaart
- Je kunt Safari nu gewoon sluiten

---

### Wat klanten zien

Klanten gaan naar **ijsvantijs.nl/ijstracker/** en zien:
- De ijsbus rijdend op de kaart zolang jij onderweg bent
- De tekst *"De ijsboer is vandaag nog niet onderweg"* als je nog niet gestart bent of al gestopt bent

---

## Problemen oplossen

| Wat je ziet | Wat er aan de hand is | Wat je doet |
|---|---|---|
| Kaart toont vraagteken in plaats van ijsbus | Icoontje laadt niet | Webman controleren of `Ijsbus.png` correct geüpload is |
| Pin beweegt niet meer | Safari is op de achtergrond gezet | App opnieuw openen en op Start drukken |
| "Locatie tijdelijk niet beschikbaar" | Server even niet bereikbaar | Wacht 1 minuut en ververs de pagina |
| Safari vraagt niet om locatie | Locatie is eerder geweigerd | Instellingen → Privacy → Locatievoorzieningen → Safari → "Tijdens gebruik" |
| Kaart staat op Amsterdam | Webman heeft aanpassing 2 nog niet gedaan | Webman inschakelen |

---

## Overzicht: wie beheert wat

| Onderdeel | Wat het is | Wie beheert het |
|---|---|---|
| **Railway** | De server die de locatie bijhoudt | IJsboer (eigen account, $5/mnd) |
| **Start/Stop knop** | Pagina op ijsvantijs.nl | Webman |
| **Kaart op website** | Pagina op ijsvantijs.nl/ijstracker/ | Webman |
| **Tracker-code** | GitHub (technisch beheer) | Ontwikkelaar |
