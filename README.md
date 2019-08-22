Text Wrapper to program napisany w języku Python, który pobiera artykuły ze strony [](https://geek.justjoin.it), 
a następnie zapisuje je lokalnie na komputerze, w folderach odpowiadających kategoriom przypisanym im na stronie.

Kolejnym etapem jest prezentacja kategoryzacji pobranych artykułów za pomocą konwolucyjnej sieci neuronowej,
z wykorzystaniem biblioteki Keras oraz Wektorowych Reprezentacji Dystrybucyjnych (Word Embedding) udostępnionych
w bibliotece GloVe. Artykuły sklasyfikowane przez klasyfikator, zapisane będą w osobnym folderze "Artykuły Klasyfikacja"

Wszystkie pliki potrzebne do działania programu znajdują się w repozytorium. Dodane również zostały pliki użyteczne 
w razie potrzeby ponownego przetrenowania wektora słów z pomocą biblioteki GloVe. Przykładowo pobrane artykuły 
znajdują się w folderze "Artykuły". Aby szybko pobrać biblioteki użyte w projekcie, należy, po pobraniu wszystkich
modułów i reszty plików, wykonać poniższą komendę w terminalu projektowym:

>  $ pip install -r requirements.txt

Uaktualni ona pip o biblioteki użyte w projekcie.

Aby nauczyć ponownie wektor słów należy wykonać poniższe kroki:
1.  Włączyć terminal w folderze projektowym, następnie wykonać poniższą komendę, klonującą oficjalne repozytorium GloVe 
>  $ git clone http://github.com/stanfordnlp/glove
2.  Odpalić program oraz na zapytanie o ponowną naukę wektorów odpowiedzieć twierdząco, po stworzeniu korpusu do nauki wektorów program zada pytanie czy wyjść z programu; można odpowiedzieć twierdząco
3.  Podmienic plik "demo.sh" będący wewnątrz sklonowanego repozytorium, na plik o tej samej nazwie znajdujący się w folderze "glove" wewnątrz repozytorium tego projektu
4.  Wykonać poniższe komendy 
>  $ cd glove && make \n $ ./demo.sh
5.  Nowo utworzone wektory są gotowe do użycia w projekcie

