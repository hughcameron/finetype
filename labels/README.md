# FineType Labels



```
python generate_data.py --value 1000

python generate_data.py --value 10 --output "data/r1.ndjson"
python generate_data.py --value 10 --output "data/r2.ndjson"
```


To Do:
- [ ] Scientific Notation
- [ ] Move hex_color to a code section
- [ ] Move ascii & emoji to a character section
- [ ] Expand [phone number to locales](https://github.com/daviddrysdale/python-phonenumbers) using `example_number` method by format NATIONAL, INTERNATIONAL, E164
- [ ] Expand Address to locales
- [ ] Permute date & time formats [by locale](https://babel.pocoo.org/en/latest/dates.html)
- [ ] Excel Custom Number Formats
- [ ] Finance Identifiers - ISIN, CUSIP, SEDOL, SWIFT, LEI
- [ ] [Currency Formats](https://en.wikipedia.org/wiki/ISO_4217)
- [ ] [String Formats](https://mkaz.blog/working-with-python/string-formatting)
- [ ] Generate data from [CLDR releases](https://cldr.unicode.org/)
