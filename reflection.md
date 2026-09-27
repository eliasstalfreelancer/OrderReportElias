# Kodgranskning av originalprogrammet

Originalprogrammet fungerar och skapar de rapporter som efterfrågas, men flera delar gör koden svårare att testa, återanvända och vidareutveckla. Nedan är de viktigaste förbättringsområdena.

## 1 Hela programmet ligger i samma fil

**Observation:** Filinläsning, validering, datatvätt, beräkningar, rapportskapande och filsparning sker i samma kodflöde.

**Konsekvens:** Koden får flera ansvar samtidigt. Det blir svårare att förstå vilken del som gör vad och svårt att testa en enskild del utan att köra nästan hela programmet.

**Förslag:** Dela upp programmet i moduler för exempelvis inläsning/sparning, validering, bearbetning och rapporter. Behåll en tydlig `main()` som startpunkt.

## 2. Programmet körs direkt vid import

**Observation:** Originalkoden börjar köra så fort Python läser filen.

**Konsekvens:** Om man vill importera en funktion från filen i ett test eller en annan modul startar hela rapportkörningen som en sidoeffekt.

**Förslag:** Lägg körflödet i en `main()`-funktion och använd `if __name__ == "__main__":`.

## 3. `print()` används för körinformation

**Observation:** Programmet använder `print()` för start, sparade filer, fel och statusinformation.

**Konsekvens:** Det är svårt att styra detaljnivå, skilja information från varningar/fel och senare skriva loggar till fil eller annan destination.

**Förslag:** Använd Pythons `logging` och konfigurera logging centralt. Varje modul använder `logging.getLogger(__name__)`.

## 4. Felhanteringen är för bred

**Observation:** Nästan hela programmet ligger i `try/except Exception` och alla fel visas som `Något gick fel`.

**Konsekvens:** Olika fel blir svåra att skilja åt. Ett programmeringsfel kan döljas på samma sätt som en saknad CSV-fil eller felaktig data.

**Förslag:** Upptäck förväntade problem där de hör hemma och ge tydliga undantag, till exempel `FileNotFoundError` för saknad fil och `ValueError` för felaktigt innehåll.

## 5. Valideringsfelet är otydligt

**Observation:** Om en obligatorisk kolumn saknas kastas `Exception("Fel data")`.

**Konsekvens:** Användaren får inte veta vilken eller vilka kolumner som saknas, vilket gör felsökningen långsammare.

**Förslag:** Beräkna mängden saknade kolumner och inkludera deras namn i felmeddelandet.

## 6. Duplicerad rapportlogik

**Observation:** Rapporten per produktkategori och rapporten per region gör nästan exakt samma `groupby`, summering, avrundning, return rate och sortering.

**Konsekvens:** Om logiken senare ändras måste samma ändring göras på flera ställen. Det ökar risken för att rapporterna börjar bete sig olika av misstag.

**Förslag:** Lägg den gemensamma logiken i en intern hjälpfunktion som tar grupperingskolumnen som argument.

## 7. Otydliga variabelnamn

**Observation:** Namn som `result1` och `result2` beskriver inte vad variablerna innehåller.

**Konsekvens:** Läsaren måste följa hela kodblocket för att förstå skillnaden mellan resultaten.

**Förslag:** Använd beskrivande namn som `sales_by_category` och `sales_by_region` eller funktioner med motsvarande namn.

## 8. Hårdkodade sökvägar och avsaknad av konfiguration

**Observation:** `INPUT_FILE` och `OUTPUT_FOLDER` är globala strängar i samma fil som resten av programmet.

**Konsekvens:** Det blir mindre tydligt vilka värden som faktiskt är programkonfiguration och svårare att återanvända körningen med andra sökvägar.

**Förslag:** Samla sökvägar i en liten `dataclass`, till exempel `ReportConfig`, och använd `pathlib.Path` i stället för att bygga sökvägar manuellt med `os.path`.

## 9. Saknade automatiska tester

**Observation:** Det finns inga tester som kontrollerar beräkningar eller felhantering.

**Konsekvens:** Vid refaktorering finns ingen automatisk kontroll på att exempelvis `discounted_value`, grupperingar och returer fortfarande räknas på samma sätt.

**Förslag:** Lägg till `pytest`-tester för normalfall och felscenarier. Testerna bör kontrollera konkreta resultat och inte bara att programmet går att starta.
