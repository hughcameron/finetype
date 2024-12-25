# FineType Labels



```
python generate_data.py --value 1000

python generate_data.py --value 10 --output "data/r1.ndjson"
python generate_data.py --value 10 --output "data/r2.ndjson"
```


## Hugging Face Datasets

Data is generated in the NDJSON format, but not stored in the GitHub repository. The data is stored in the Hugging Face Datasets repository for reproducibility and sharing.


To Do:
- [ ] [Unicode Characters](https://unicode-table.com/en/)
- [ ] [Ballpark Formats](https://github.com/debrouwere/python-ballpark)
- [ ] [.NET String Formats](https://learn.microsoft.com/en-us/dotnet/standard/base-types/formatting-types)
- [ ] [Great Tables Value formatting functions](https://posit-dev.github.io/great-tables/reference/#value-formatting-functions)
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
