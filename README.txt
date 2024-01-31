

Flask Book Review API

URL: https://github.com/PetarNikolicc/Books.git

Översikt

Denna Flask-applikation tillhandahåller en API för att hantera böcker och recensioner. Den stöder operationer för att lägga till, hämta, uppdatera och radera bokdata samt recensioner.

Installation
För att köra denna applikation behöver du Python och Flask installerat på din dator.

1. Klona detta repo:
   ```
   git clone [repo-url]
   ```
2. Installera beroenden:
   ```
   pip install flask flask_sqlalchemy
   ```
3. Starta servern:
   ```
   python app.py
   ```

Användning
Efter att ha startat servern är API:et tillgängligt på `http://127.0.0.1:5000/`.

Endpoints
1. **Lägg till en bok (POST `/books`):**
   ```
   { "title": "Bokens titel", "author": "Författare", "summary": "Sammanfattning", "genre": "Genre" }
   ```
2. **Hämta alla böcker (GET `/books`):** Hämtar en lista över alla böcker.

3. **Uppdatera en bok (PUT `/books/<book_id>`):**
   ```
   { "title": "Ny titel", "author": "Ny författare", "summary": "Ny sammanfattning", "genre": "Ny genre" }
   ```
4. **Radera en bok (DELETE `/books/<book_id>`):** Raderar den angivna boken.

5. **Lägg till en recension (POST `/books/<book_id>/reviews`):**
   ```
   { "rating": 5, "comment": "En utmärkt bok!" }
   ```
6. **Hämta recensioner för en bok (GET `/books/<book_id>/reviews`):** Hämtar alla recensioner för en specifik bok.

7. **Uppdatera en recension (PUT `/reviews/<review_id>`):**
   ```
   { "rating": 4, "comment": "Bra bok!" }
   ```
8. **Radera en recension (DELETE `/reviews/<review_id>`):** Raderar den angivna recensionen.

Tester

Applikationen innehåller en uppsättning automatiska tester för att verifiera funktionerna. För att köra dessa tester, följ dessa steg:

Navigera till Rotkatalogen:
Se till att du befinner dig i projektets rotkatalog i terminalen.

Kör Pytest:

Kör kommandot pytest för att starta testsviten. Pytest kommer automatiskt att upptäcka och köra alla testfall definierade i testfilerna.



