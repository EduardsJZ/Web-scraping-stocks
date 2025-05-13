# Web-scraping-stocks
## Projekts Datu struktūras un algoritmi(1), 24/25-P
### Programmas uzdevums
- Ļauj lietotājam ievadīt akcijas Tikera simbolu
- Pēc lietotāja izvēles, iegūst attiecīgās akcijas informāciju :
  * jaunāko akcijas cenu attiecīgajā valūtā
  * jaunākās ziņas attiecībā uz akciju
  * pēdējo 24 stundu akcijas cenas grafiku
- Iegūtos datus saglabā Hash tabulā
- Atbalsta valūtas konvertāciju no USD uz EUR 
### Izmantotās bibliotēkas
* **selenium** - lai atomatizētu tīmekļa skrāpēšanu no Yahoo Finance, tā iegūstot akcijas pašreizējo cenu un jaunākās ziņas
* **yfinance** - lai pārbaudītu akcijas eksistenci un iegūtu akcijas cenas vēsturi grafika veidošanai
* **matplotlib** - lai izveidotu un saglabātu akcijas grafiku kā attēlu
* **requests** -  lai iegūtu reāllaika valūtas kursu no USD uz EUR
* **selenium.webdriver klases** - lai nodrošinātu programmas funkcionalitāti darbībā ar Yahoo Finance, kas ielādējas tikai pēc "Cookies" apstiprināšanas
### Pašdefinētas datu struktūras
* **HashTable** klase, kas glabā informāciju par vairākām akcijām izmantojot Stock klases objektu
* **Stock** klase, kas satur akcijas datus: simbolu, cenu, valūtu, ziņas
* **Node** klase, kas palīdz HashTable struktūras darbībai
### Programmatūras izmantošanas metodes
Programma darbojas terminālī, piedāvājot lietotājam izvēlēties darbības izmantojot ciparus
- Galvenā izvēlne  
  **1** - Ievadīt akciju - ļauj lietotājam ievadīt akcijas Tikera simbolu, un piedāvās nākamo izvēlni  
  **2** - Izvadīt - izvada iepriekš saglabātos datus  
  **3** - Beigt - beidz programmas darbību  
- Apakšizvēlne pēc izvēles "Ievadīt akciju"  
  **1** - Cena - iegūs izvēlētās akcijas cenu  
  **2** - Jaunākās ziņas - iegūs izvēlētās akcijas jaunākās 5 ziņas  
  **3** - Grafiks - saglabās akcijas cenu grafiku kā PNG failu  
  **4** - Saglabāt un Atgriezties - saglabās iegūtos datus Hash tabulā un atgriezīsies pie galvenās izvēlnes  
  **5** - Atcelt - atgriezīsies pie galvenās izvēlnes nesaglabājot iegūtos datus  
