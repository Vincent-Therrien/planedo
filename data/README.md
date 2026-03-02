# Data Directory

The script `filter_exoplanets.py` converts raw data from the
[NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) into the format expected
by the exoplanet viewer. To use the script:

1. Access the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/).
2. Click on the `Confirmed Planets` button. As I am writing this (March 2026), there are 6128
   confirmed planets.
3. In the new page, click on `Download Table`. Select `CSV Format` and confirm the download.
4. Place the file in this directory. Rename it `all_exoplanets.csv`.
5. Execute the script. It requires no dependency, so you do not need to create a virtual
   environment to use it.
   - On Linux: `python3 filter_exoplanets.py`
   - On Windows: `py filter_exoplanets.py`

The file `../viewer/exoplanets-data.js` is obtained by prepending the resulting JSON file with the
string `window.EXOPLANETS_DATA = `. The file `../viewer/home.html` loads this JS file directly as a
JavaScript object.
