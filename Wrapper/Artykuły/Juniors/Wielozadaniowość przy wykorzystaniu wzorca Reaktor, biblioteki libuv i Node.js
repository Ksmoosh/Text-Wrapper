Swego czasu jedną z głównych zalet, za które chwalony był Node.js, była możliwość przeprowadzania operacji wejścia-wyjścia, nie blokując przy tym głównego wątku. W głównej mierze stoją za tym wzorzec Reaktor oraz biblioteka libuv, będące głównym tematem tego artykułu. Razem pozwalają one radzić sobie z wielozadaniowością prawie tak gładko jak robi to Xabi Alonso:


Krzysztof Zbiciński. Programista wszelkich technologii, specjalizujący się w JavaScripcie. Fan podążania za nowymi trendami pod warunkiem zachowania zdrowego rozsądku. Organizator warsztatów NodeSchool w Łodzi, od czasu do czasu prelegent i bloger. Na Just Geek IT opublikował wcześniej artykuł pt. Event Loop a kolejność wykonywania kodu w JavaScript.
Czym jest wzorzec Reaktor?
Jest to jeden z najczęściej używanych wzorców podczas tworzenia aplikacji internetowych. Istnieje duże prawdopodobieństwo, że znasz go bardzo dobrze, nie zdając sobie nawet z tego sprawy. Można go zawrzeć w jednym zdaniu: aplikacja nasłuchuje na zdarzenia wejścia-wyjścia danego typu, definiując przy okazji funkcję, która ma zostać uruchomiona jako “reakcja” na to zdarzenie. Brzmi zupełnie jak JavaScriptowe callbacki, prawda?
Dzięki temu wzorcowi możemy używać nieblokujących operacji wejścia-wyjścia, które zwykle zajmują trochę czasu i sprawiają, że aplikacja staje się nieresponsywna, jeśli użyte zostały w klasyczny, synchroniczny sposób (np. zapytanie do bazy danych, zapytanie HTTP, wczytywanie pliku z dysku).
Gdy dany fragment kodu zażąda operacji wejścia-wyjścia, żądanie to wraz z zdefiniowaną reakcją jest umieszczane w kolejce zdarzeń (Event Queue) wewnątrz demultipleksera zdarzeń (Event Demultiplexer). Następnie kod aplikacji kontynuuje swoje działanie. Dzięki temu aplikacja nie “wiesza się” i może od razu przeprowadzać kolejne operacje (np. nasłuchiwać na zdarzenia pochodzące z interfejsu użytkownika, reagować na dane wprowadzane przez użytkownika, itp.).
W międzyczasie, tzw. pętla zdarzeń (Event Loop) przetwarza żądania znajdujące się w kolejce. Iteruje po nich i wywołuje powiązane funkcje gdy dane zdarzenie miało już miejsce (np. zapytanie do bazy danych lub HTTP zwróciło dane, plik został wczytany).
Spójrzmy na przykładową pętlę zdarzeń napisaną w pseudokodzie, będącą tłumaczeniem implementacji z książki An Introduction to libuv autorstwa Nikhil Marathe:
Każdy z systemów operacyjnych (Linux, Mac OSX, Windows) posiada własną, różniącą się nieco od pozostałych implementację demultipleksera zdarzeń. Spowodowało to konieczność zbudowania warstwy abstrakcji, która zniwelowałaby te różnice.
libuv na ratunek
W początkowej fazie rozwoju Node.js korzystał z biblioteki o nazwie libev, aby zunifikować interfejsy demultiplekserów w systemach Mac OSX oraz Linux (kqueue oraz (e)poll). Wraz ze wzrostem popularności, rozwiązanie to stawało się niewystarczające i brakujące wsparcie dla systemu Windows doskwierało coraz mocniej.
Stworzono zatem bibliotekę libuv, która oprócz kqueue oraz (e)poll wspiera również demultiplekser systemu z Redmond (IOCP). Mimo że początkowo rozwijana ona była głównie z myślą o Node.js, teraz jest ona wykorzystywana również przez wiele innych projektów, włączając w to m.in. język Rust.
Jak to wszystko do siebie pasuje?
Myślę, że najlepszym pomysłem jest przedstawienie tego na diagramie. Architektura aplikacji napisanej pod Node.js może być przedstawiona w poniższy sposób:


Kod aplikacji: komentarz zbędny ;),
Core Node.js: (nazywany również node-core) jest JavaScriptową implementacją API Node’a (moduły fs, http, path itd.),
Bindingi (bindings): opakowują oraz dają dostęp JavaScriptowi do libuv oraz innych niskopoziomowych funkcjonalności,
V8: silnik JavaScript stworzony dla przeglądarki Google Chrome, użyty następnie jako podstawa środowiska Node.js,
libuv: biblioteka zapewniająca warstwę abstrakcji nad implementacjami demultiplekserów różnych systemów operacyjnych.

Podsumowanie
Mam nadzieję, że to krótkie wprowadzenie stanowi dobry punkt startowy do nauki wewnętrznych mechanizmów środowiska Node.js. Poruszane tutaj tematy to tylko wierzchołek góry lodowej, więc jeśli jesteście zainteresowani bardziej dogłębną analizą tych aspektów, zachęcam do zapoznania się ze źródłami, które posłużyły do napisania tego artykułu.
Źródła:
1. An Introduction to libuv autorstwa Nikhil Marathe.
2. Node.js Design Patterns Second Edition autorstwa Mario Casciaro oraz Luciano Mammino.
3. The Node.js System autorstwa Aman Mittal.