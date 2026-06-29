🟦 Examination

Individuell examinationsuppgift i kursen Programmering med Python.

## Uppgift  
Din uppgift är att bygga vidare på spelet "Fruit loop". Spelet kan 
spelas direkt i terminalen, och går ut på att samla frukter.
---
## Krav
### Grundkrav
A. Spelaren ska börja nära mitten av rummet.  
--> Jag har ändrat så att spelaren nu startar på x:18 y:5  

B. Förflyttningar i alla 4 riktningar. (Med tangenterna WASD.)  
--> Jag använder msvcrt så att man slipper trycka Enter vid varje förflyttning. I klassen Game 
har jag implementerat en metod act_on_player_input() som hanterar logiken kring förflyttning.

C. Man ska inte kunna gå igenom väggar.  
--< Jag har implementerat metoden can_move() i klassen player så att den returnerar True om 
den nya rutan inte är en vägg.

D. Fruktsallad - alla frukter ska vara värda 20 poäng i stället för 10.    
--> Jag har ändrat parametern value till 20 för alla items som är frukter i klassen Item.

E. Inventory - alla saker som man plockar upp ska sparas i en lista.    
--> Då spelaren hittat ett item vid förflyttning i klassen Game läggs denna till spelarens
inventorylista i klassen Player.

F. Nytt kommando: "i", skriver ut innehållet i spelarens inventory.    
--> Jag har implementerat en metod get_player_inventory() i klassen Player som returnerar  
spelarens inventarielista. Metoden är skapad i klassen Player då denna klass äger listan.
Då spelaren skriver "i" läser act_on_player_input(), i klassen Game, input och hämtar listan 
samt skriver ut den.

G. The floor is lava - för varje steg man går ska man tappa 1 poäng.   
--> Då spelaren förflyttas i klassen Game minskas spelarens poäng med 1. Om spelet
är i Grace period minskas inte poängen förrän perioden är över.

H. Använd for-loopar för att skapa flera, sammanhängande väggar på kartan.
Se till att det inte skapas några rum som man inte kan komma in i. Gör detta i filen grid.py.  
--> Jag har skapat en metod make_obstacle_walls() i klassen Grid. Metoden skapar definierade 
väggar så att den inte finns någon risk att skapa slutna rum.

### Nice to have
I. Fällor - introducera valfri fälla till spelplanen. Om man går på en ruta med 
en fälla ska man förlora 10 poäng. Fällan ska ligga kvar så att man kan falla 
i den flera gånger.    
--> Jag har lagt till fällan i listan pickups med Item("fälla", value = -10, symbol = "."). Det 
medför att rutan ser ut som en vanlig tom ruta och att spelaren får 10 poängs avdrag om man
hamnar på rutan. Det negativa värdet skrivs ut korrekt efter att en if-sats lagts till vid utskriften 
"Du har hittat en..."  
Fällan ligger kvar efter att spelaren gått vidare då rutan inte "clearas" om den innehåller en fälla. 
Fällan läggs heller inte till i spelarens inventory. Detta är löst med en if-sats i klassen Games 
metod act_on_player_input(). 

J. Spade - en ny sak man kan plocka upp. När man går in i en vägg nästa gång, 
förbrukas spaden för att ta bort väggen.  
--> Jag har lagt till spaden i Items med Item("spade", value = 0, symbol = "!"). I klassen Game 
kontrolleras om rutan spelaren är på väg mot inte är en vägg. Jag har lagt till en kontroll så 
att om spelaren har en spade får man ändå gå till väggen. Om rutan var en vägg tas spaden bort 
från spelaren inventory och den tidigare väggen görs om till en tom ruta. Därefter fortsätter 
koden som tidigare.

K. Nycklar och kistor - slumpa minst en nyckel och lika många kistor på spelplanen. 
När man går på en ruta med en nyckel plockar man upp den i sitt inventory. Om man 
kommer till en kista och har minst en nyckel, öppnar man kistan och plockar upp en 
skatt som är värd 100 poäng. (Nyckeln är förbrukad.).  
--> Jag slumpar en nyckel (⌂) och en kista ($) då spelet initieras. I klassen Game 
hanterar jag tre scenarios:  
1. Spelaren har ingen nyckel då han går till kistan
2. Spelaren har nyckel då han går till kistan
3. Spelaren hittar item som inte är kista  

Om spelaren har nyckel då han går till kistan ökas poängen med 100 poäng och meddelandet
"Du låste upp kistan med din nyckel! +100 poäng" skrivs ut. Har han inte nyckeln skrivs 
meddelandet "Kistan är låst! Du måste hitta en nyckel först.".

L. Bördig jord - efter varje 25:e drag skapas en ny frukt/grönsak någonstans på 
kartan.  
--> Då spelarikonen flyttas i klassen Game räknas en instansvariabel "fertile_soil_counter" 
upp med 1. Då räknaren når 25 anropas funktionen add_extra_fruit() i klassen Item. I anropet 
skickas argumenten "grid" och "item" med. Argumentet item skapas genom att en ny frukt tas 
från en lista. Frukten tas bort från listan efter användning. Jag har valt att de nya frukterna 
får en ny symbol "o" för att skilja dem från de ursprungliga frukterna.

M. Exit - slumpa ett "E" på kartan. När man har plockat upp alla ursprungliga 
saker, kan man gå till exit för att vinna spelet. Men innan man tagit upp alla 
har inte Exit någon effekt.  
--> Jag skapar utgången i klassen Grid i metoden set_exit(). Metoden använder 
klassens befintliga metoder för att slumpa x och y och kontrollerar sedan om 
rutan är tom. Om rutan är tom placeras "E" ut på spelplanen.  
I klassen Game har jag skapat en instanvariabel som har startvärde lika med antal
utspringliga frukter. Varje gång en av dessa plockas upp minskar jag räknaren med 1.
Om räknaren når 0 sätter jag instansvariablen exit_open till True.  
I Game huvudloop har jag lagt till en kontroll av om instansvariabeln game_over blir 
True. Det blir den om exit_open är True när spelaren går till Exit (E) på spelplan.

N. Jump - om man skriver ett "J" innan något av "WASD", ska spelaren hoppa över 
en ruta. (Exempel: "JW" → två steg uppåt.) Man förflyttar sig alltså två steg, 
men kan förstås bara plocka upp eller interagera med saker där man landar. 
Hoppar man in i en vägg blir det samma effekt som om man hade gått ett steg 
på vanligt sätt.

### Extra utmaningar
O. Grace period - efter man har tagit plockat upp något, kan man gå 5 steg utan 
att det dras några poäng.  
--> Jag skapade en instansvariabel "grace_period_counter" i klassen Game med värdet 0. Då 
spelaren hittar en item sätts variabeln till 5, grace perioden startar.
Vid kontroll av spelarens rörelse har jag lagt till en if-sats som kontrollerar värdet 
på "grace_period_counter". Om värdet är 0 (inget har hänt) dras 1 poäng då spelaren 
förflyttas. Om däremot "grace_period_counter" är större än noll dras ingen straffpoäng
men grace_period_counter minskas med 1. Om spelaren hittar ytterligare ett item innan 
grace perioden nått 0 startas den om från 5. Att hitta en fälla eller kista startar inte
Grace period. 

P. AI-fiender - placera 1-3 fiender på kartan. För varje steg spelaren tar 
ska ska varje fiende ha en slumpmässig chans att flytta sig ett steg närmare 
spelaren. Minus 20 poäng om en fiende hinner ifatt. (Inte diagonalt, dvs. 
samma rörelsemönster som spelaren. Fienderna ska vara lite "långsammare" 
så att det är lagom svårt att undvika dem.)  

Q. Tryck "B" för att placera en bomb. Efter 3 drag smäller bomben och förstör 
allt på sin ruta och de åtta som gränsar till den. (fällor, väggar, m.m.) 
Om spelaren är kvar förlorar man poäng.  

R. Ett nytt kommando ("T" för trap) för att desarmera fällor.  
--> Jag har lagt till kommandot "t" i metoden act_on_player_input() i klassen Game. Jag 
valde att implementera en ny metod disarm_trap() i klassen Game som anropas vid tryck på "t".
Först hämtar jag det som finns på aktuell ruta med self.game_state.game_grid.get(). Därefter 
kontrollerar jag om det på rutan finns ett objekt (Item) och om det är en fälla. Om där var
en fälla gör jag clear på rutan med self.game_state.game_grid.clear(). Metoden returnerar True 
eller False beroende på resultat. Slutligen skriver jag ut resultatet "Du har desarmerat en fälla" 
eller om det inte var någon fälla på aktuell ruta "Ingen fälla här" i metoden act_on_player_input().

S. Använd TDD för att testa några av funktionerna i koden.  
--> Jag har använt Pytest för att testa metoden get_player_inventory() i klassen Player. 
Jag började med att ta fram krav (se testfil) som jag sen använde för att designa metoden.  
--> Jag har använt Pytest för att testa funktionaliteten för "spaden" i spelet. Jag testar 
den del av metoden act_on_player_input() som hanterar logiken. Jag började med att definiera 
krav och utökade därefter metodens funktionalitet (Refactor).  
--> Jag har använt Pytest för att testa funktionaliteten för att desarmera en "fälla". Jag 
testar metoden disarm_trap(). Metoden designades efter att jag identifierat funktionella och 
icke funktionella krav. Då kravanalysen ledde till re-design av metoden act_on_player_input()
och design av en ny metod disarm_trap() gjordes en refactor av tidigare kod.

T. Använd paketet curses för bättre hantering av terminalen, exempelvis getkey 
i stället för input.  
Jag har valt att använda msvcrt.getch() för att spelaren inte ska behöva trycka Enter 
vid varje kommando.

---
## Starta projektet

För att starta mitt projekt skriver man följande i terminalen, medan man står i projektets rotmapp.  

```commandline
python -m src.game
```
För att exekvera testerna med Pytest skriv följande i terminalen, medan man står i projektets rotmapp. 

```commandline
python -m pytest
```

---
## Vad jag har gjort

|Version 1| Status |
|---------|:------:|
|A        |   🟢   |
|B        |   🟢   |
|C        |   🟢   |
|D        |   🟢   |
|E        |   🟢   |
|F        |   🟢   |
|G        |   🟢   |
|H        |   🟢   |

|Version 2|  Status  |
|---------|:--------:|
|I        |    🟢    |
|J        |    🟢    |
|K        |    🟢    |
|L        |    🟢    |
|M        |    🟢    |
|N        |    🔴    |

| Version 3 | Status  |
|-----------|:-------:|
| O         |   🟢    |
| P         |   🔴    |
| Q         |   🔴    |
| R         |   🟢    |
| S         |   🟢    |
| T         |   🟢    |