# Autor
**Robert Mesek**

# Zadanie:
1. Wyznacza relację zależności D (2 pkt.)
2. Wyznacza relację niezależności I (1 pkt.)
3. Wyznacza postać normalną Foaty FNF([w]) śladu [w] (2 pkt.)
4. Rysuje graf zależności w postaci minimalnej dla słowa w (2 pkt.)

# Rozwiązanie:
Przygotowano rozwiązanie w języku `Python` z wykorzystaniem z bibliotek `matplotlib`, `networkx`.


Zostało przetestowane w wersji `3.12.7` pod kontrolą systemu `Ubuntu 24.04 x86_64`.

## Uruchomienie

### Utworzenie wirtualnego środowiska `venv`
```bash
python -m venv venv
```

### Aktywacja wirtualnego środowiska 
#### Na systemach `POSIX`
```bash
source venv/bin/activate
```

#### Na systemach `Windows`
```bat
venv\Scripts\activate
```

### Instalacja bibliotek poprzez `PIP`
```bash
python -m pip install -r requirements.txt
```

### Uruchomienie
```bash
python main.py -h
```

### Deaktywacja wirtualnego środowiska `venv`
```bash
deactivate
```

## Opcjonalne uruchomienie bez bibliotek (brak rysowania grafu)
```bash
python main.py -h
```

## Wyniki działania dla przykładowych danych
### Dla `case0.txt`
- Zawartość pliku
```
(a) x := x + y
(b) y := y + 2z
(c) x := 3x + z
(d) z := y − z
A = {a, b, c, d}
w = baadcb
```
- Wyjście
```
D = [('a', 'a'), ('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'b'), ('b', 'd'), ('c', 'a'), ('c', 'c'), ('c', 'd'), ('d', 'b'), ('d', 'c'), ('d', 'd')]

I = [('a', 'd'), ('b', 'c'), ('c', 'b'), ('d', 'a')]

FNF([w]) = (b)(ad)(a)(bc)

digraph {
1 [label=b];
2 [label=a];
3 [label=d];
4 [label=a];
5 [label=b];
6 [label=c];
1 -> 2;
1 -> 3;
2 -> 4;
3 -> 4;
4 -> 5;
4 -> 6;
}
```

### Dla `case1.txt`
- Zawartość pliku
```
(a) x := x + 1
(b) y := y + 2z
(c) x := 3x + z
(d) w := w + v
(e) z := y - z
(f) v := x + v
A = {a, b, c, d, e, f}
w = acdcfbbe
```
- Wyjście
```
D = [('a', 'a'), ('a', 'c'), ('a', 'f'), ('b', 'b'), ('b', 'e'), ('c', 'a'), ('c', 'c'), ('c', 'e'), ('c', 'f'), ('d', 'd'), ('d', 'f'), ('e', 'b'), ('e', 'c'), ('e', 'e'), ('f', 'a'), ('f', 'c'), ('f', 'd'), ('f', 'f')]

I = [('a', 'b'), ('a', 'd'), ('a', 'e'), ('b', 'a'), ('b', 'c'), ('b', 'd'), ('b', 'f'), ('c', 'b'), ('c', 'd'), ('d', 'a'), ('d', 'b'), ('d', 'c'), ('d', 'e'), ('e', 'a'), ('e', 'd'), ('e', 'f'), ('f', 'b'), ('f', 'e')]

FNF([w]) = (abd)(bc)(c)(ef)

digraph {
1 [label=a];
2 [label=b];
3 [label=d];
4 [label=b];
5 [label=c];
6 [label=c];
7 [label=e];
8 [label=f];
1 -> 4;
1 -> 5;
2 -> 4;
2 -> 5;
3 -> 4;
3 -> 5;
4 -> 6;
5 -> 6;
6 -> 7;
6 -> 8;
}
```

### Dla `case2.txt`
- Zawartość pliku
```
(a) x := x + y
(b) y := z - v
(c) z := v * x
(d) v := x + 2y
(e) x := 3y + 2x
(f) v := v - 2z
A = {a,b,c,d,e,f}
w = afaeffbcd
```
- Wyjście
```
D = [('a', 'a'), ('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'a'), ('b', 'b'), ('b', 'c'), ('b', 'd'), ('b', 'e'), ('b', 'f'), ('c', 'a'), ('c', 'b'), ('c', 'c'), ('c', 'd'), ('c', 'e'), ('c', 'f'), ('d', 'a'), ('d', 'b'), ('d', 'c'), ('d', 'd'), ('d', 'e'), ('d', 'f'), ('e', 'a'), ('e', 'b'), ('e', 'c'), ('e', 'd'), ('e', 'e'), ('f', 'b'), ('f', 'c'), ('f', 'd'), ('f', 'f')]

I = [('a', 'f'), ('e', 'f'), ('f', 'a'), ('f', 'e')]

FNF([w]) = (af)(af)(ef)(b)(c)(d)

digraph {
1 [label=a];
2 [label=f];
3 [label=a];
4 [label=f];
5 [label=e];
6 [label=f];
7 [label=b];
8 [label=c];
9 [label=d];
1 -> 3;
1 -> 4;
2 -> 3;
2 -> 4;
3 -> 5;
3 -> 6;
4 -> 5;
4 -> 6;
5 -> 7;
6 -> 7;
7 -> 8;
8 -> 9;
}
```
