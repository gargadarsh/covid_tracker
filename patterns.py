import re

from data import Data
import config

#instantiate data
data = Data(config.API_KEY, config.PROJECT_TOKEN)

# potential phrases
TOTAL_PATT = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.getTotalCases,
        re.compile("[\w\s]+ total cases "): data.getTotalCases,
        re.compile("[\w\s]+ total [\w\s]+ cases [\w\s]+"): data.getTotalCases,
        re.compile("[\w\s]+ total cases [\w\s]+"): data.getTotalCases,

        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.getTotalDeaths,
        re.compile("[\w\s]+ total deaths"): data.getTotalDeaths,
        re.compile("[\w\s]+ total [\w\s]+ deaths [\w\s]+"): data.getTotalDeaths,
        re.compile("[\w\s]+ total deaths [\w\s]+"): data.getTotalDeaths,

        re.compile("[\w\s]+ total [\w\s]+ recoveries "): data.getTotalRecovered,
        re.compile("[\w\s]+ total recoveries"): data.getTotalRecovered,
        re.compile("[\w\s]+ total [\w\s]+ recoveries [\w\s]+"): data.getTotalRecovered,
        re.compile("[\w\s]+ total recoveries [\w\s]+"): data.getTotalRecovered
}

COUNTRY_PATT = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.getCountryData(country)['total_cases'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.getCountryData(country)['total_deaths'],

}

UPDATE_PATT = "update"