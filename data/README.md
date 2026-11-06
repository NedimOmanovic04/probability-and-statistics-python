# Izvorni skupovi podataka

| Notebook | Datoteka | Očekivani sadržaj |
| --- | --- | --- |
| `VIS24-TIM37.ipynb` | `spotify2023.csv` | Pjesme/izvođači, streams, datumi izdanja, audio karakteristike i platforme; pogledati kolone u notebooku |
| `VIS24-Z2-TIM37.ipynb` | `salaries.csv` | Plate, `salary_in_usd`, iskustvo, zaposlenje, lokacije, veličina kompanije, `remote_ratio`; dio analiza traži dodatnu kolonu `Sex` |

CSV datoteke nisu bile dio dostavljenog lokalnog materijala. Izvorni salaries notebook referencira timski repozitorij `samiracatic/VIS24`; dostupnost i uslove korištenja podataka potrebno je provjeriti kod izvornog tima. Za Spotify materijal ne postoji potvrđen izvorni URL u dostavljenim datotekama.

Preuzmi tačnu nastavnu verziju uz odgovarajuće pravo korištenja. Ne izmišljaj nedostajuće kolone. Kopije možeš staviti u ovaj folder i prilagoditi putanje u notebooku na `../data/spotify2023.csv` i `../data/salaries.csv`. Za Spotify neke ćelije koriste `latin1`/`ISO-8859-1` kodiranje.

Podaci se ne objavljuju automatski: `.gitignore` ih isključuje. Dodatni `examples/demo.py` koristi samo jasno označene sintetičke podatke i može se izvršiti odmah.
