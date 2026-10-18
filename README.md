# Wykład 4 – kody ze slajdów jako projekt PyCharm

Przykłady z wykładu 4 (Selenium WebDriver) jako uporządkowany projekt testów:
kod wielokrotnego użytku w `src/`, testy w `tests/`, przykłady ze slajdów w `examples/`.
Tam, gdzie slajd pokazuje wynik w komentarzu (np. `# jdoe@hotmail.com`), test sprawdza go asercją.

## Struktura

```text
w4_case/
├── pyproject.toml          # konfiguracja pytest: testpaths, pythonpath = src
├── requirements.txt        # przypięte wersje: selenium, pytest
├── .gitignore              # .venv, cache, reports/, .idea
├── src/webtests/           # kod wspólny dla testów (pakiet)
│   ├── config.py           # adresy i ustawienia ze zmiennych środowiskowych
│   ├── browser.py          # create_driver() – jedno miejsce tworzenia przeglądarki
│   ├── locators.py         # lokalizatory jako stałe, pogrupowane per strona
│   └── waits.py            # wait_for(), open_page(), wait_for_fonts()
├── tests/
│   ├── conftest.py         # fixture driver + zrzut ekranu przy porażce
│   ├── test_basics.py      # pytest, fixture, konfiguracja
│   ├── test_locators.py    # strategie By, XPath, względne, find_elements, stale
│   └── test_interactions.py  # send_keys/clear, klawisze, atrybut/właściwość, Select…
└── examples/               # ze slajdów, poza testami
    ├── first_script.py     # „Pierwszy skrypt”
    ├── browser_options.py  # „Opcje przeglądarki”
    └── anti_pattern_no_fixture.py  # „Test bez fixture” – czego NIE robić
```

## Otwarcie w PyCharm

1. **File ▸ Open…** → folder `w4_case` → *Trust Project*.
2. **Settings ▸ Python ▸ Interpreter ▸ Add Interpreter ▸ Add Local Interpreter**:
   *Virtualenv*, nowe `.venv` w folderze projektu, Python 3.14.
3. Terminal PyCharm (PowerShell): `pip install -r requirements.txt`
4. **Settings ▸ Tools ▸ Python Integrated Tools**: *Default test runner* = **pytest**.
5. Prawy klik na `src` ▸ **Mark Directory as ▸ Sources Root**,
   na `tests` ▸ **Mark Directory as ▸ Test Sources Root**
   (PyCharm podpowiada wtedy `import webtests…`).

Sterownika nie trzeba instalować – pobiera go Selenium Manager.

## Uruchomienie

| Co | Polecenie |
|---|---|
| wszystkie testy | `python -m pytest` → `17 passed` |
| bez okna przeglądarki | `$env:HEADLESS = "1"; python -m pytest` |
| jeden plik / test | `python -m pytest tests/test_locators.py::test_xpath_table` |
| antywzorzec (celowo) | `python -m pytest examples/anti_pattern_no_fixture.py` |
| skrypt | prawy klik na `examples/first_script.py` ▸ **Run** |

Zmienne środowiskowe (PyCharm: *Run ▸ Edit Configurations ▸ Environment variables*):
`INTERNET_URL`, `SELENIUM_WEB_URL`, `HEADLESS` (`1` = bez okna), `WINDOW_SIZE`, `TIMEOUT`.

## Dobre praktyki zastosowane w projekcie

| Praktyka | Gdzie |
|---|---|
| Układ `src/` + `tests/`; testy nie mieszają się z kodem pomocniczym | struktura, `pyproject.toml` |
| Konfiguracja poza kodem – zmiana środowiska = zmienna środowiskowa | `src/webtests/config.py` |
| Przeglądarka tworzona w jednym miejscu, te same opcje dla wszystkich testów | `src/webtests/browser.py` |
| Fixture z `yield` w `conftest.py` – sprzątanie także po błędzie | `tests/conftest.py` |
| Izolacja: nowa przeglądarka dla każdego testu (`scope="function"`) | `tests/conftest.py` |
| Lokalizatory jako stałe w jednym miejscu (id ▸ name ▸ CSS ▸ XPath) | `src/webtests/locators.py` |
| Tylko jawne oczekiwania (`implicitly_wait(0)`, bez `time.sleep`) | `src/webtests/waits.py` |
| Po nawigacji czekamy na „znacznik” strony | `open_page()` w każdym teście |
| Wzorzec Arrange – Act – Assert, jedno zachowanie na test, nazwy mówiące, co sprawdzają | `tests/test_interactions.py` |
| Asercje „zawiera” zamiast kruchego `==` tam, gdzie tekst może się różnić | `test_valid_login_shows_message_and_logout` |
| Zrzut ekranu przy porażce: `reports/screenshots/<test>.png` | hook w `tests/conftest.py` |
| Pliki tymczasowe testu w `tmp_path`, nie w projekcie | `test_button_css_and_geometry` |
| Przypięte wersje bibliotek, `.gitignore` | `requirements.txt`, `.gitignore` |

## Slajd → test

| Slajd wykładu 4 | Test / plik |
|---|---|
| Pierwszy skrypt, Opcje przeglądarki | `examples/first_script.py`, `examples/browser_options.py` |
| Test w pytest – bez fixture | `examples/anti_pattern_no_fixture.py` |
| Fixture z `yield`, `conftest.py`, Adresy w konfiguracji | `tests/conftest.py`, `test_basics.py::test_title` |
| Lokalizatory w kodzie | `test_locators.py::test_locator_strategies` |
| XPath – przykład: tabela | `test_locators.py::test_xpath_table` |
| Lokalizatory względne | `test_locators.py::test_relative_locators` |
| `find_element` a `find_elements` | `test_locators.py::test_find_elements_returns_empty_list` |
| Wyszukiwanie w kontekście elementu | `test_locators.py::test_search_in_element_context` |
| Element „nieświeży” (*stale*) | `test_locators.py::test_stale_element` |
| `click`, `send_keys`, `clear` | `test_interactions.py::test_send_keys_appends_and_clear_empties` |
| Odczyt: tekst i znacznik | `test_interactions.py::test_valid_login_shows_message_and_logout` |
| Klawisze specjalne | `test_interactions.py::test_arrow_keys_and_select_all`, `…::test_enter_in_textarea_adds_new_line` |
| Atrybut a właściwość | `test_interactions.py::test_attribute_vs_property` |
| CSS i geometria elementu | `test_interactions.py::test_button_css_and_geometry` |
| Listy rozwijane – `Select` | `test_interactions.py::test_select_option` |
| Nawigacja | `test_interactions.py::test_back_forward_refresh` |
| Czekanie na znacznik strony | `waits.py::open_page`, `test_basics.py::test_title_after_page_marker` |
| Kompletny test – Web Form | `test_interactions.py::test_submit_web_form` |

Przykład z atrybutem `data-test` jest tylko ilustracją – ani the-internet, ani Web Form,
ani SklepTO nie mają takich atrybutów.

## Uwagi

- **Lokalizatory względne** (`locate_with`) liczą położenie elementów na ekranie. Zaraz po
  `driver.get()` strona bywa jeszcze nieułożona (doładowują się czcionki) – bez czekania test
  padał w ok. 1 na 6 przebiegów. Dlatego `test_relative_locators` woła `wait_for_fonts()`.
- **Kolor przycisku**: od wersji 0.62.0 (10.2026) the-internet ma nowy wygląd –
  `rgba(25, 35, 25, 1)` zamiast dawnego `rgba(43, 166, 203, 1)`. Dobry przykład kruchości testów wyglądu.

Weryfikacja: Python 3.13, Selenium 4.49.0, pytest 9.1.1, Chromium 141 (headless), lokalne kopie
the-internet 0.62.0 i Selenium Web Form – `17 passed` w 3 kolejnych przebiegach;
`test_relative_locators` dodatkowo 20× z rzędu; zrzut ekranu przy porażce sprawdzony.
