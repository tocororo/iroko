# Research Organization Registry (ROR) API

The ROR API allows to retrieve, search and filter the organizations indexed in ROR. The results are returned in JSON.

A single organization record is represented by the following JSON structure:

    {
        "id": "https://ror.org/013cjyk83",
        "name": "PSL Research University",
        "types": ["Education"],
        "links": ["https://www.psl.eu/en/university"],
        "aliases": ["Université PSL"],
        "acronyms": ["PSL"],
        "wikipedia_url": "https://en.wikipedia.org/wiki/PSL_Research_University",
        "labels": [
            {
                "label": "Université de recherche Paris Sciences et Lettres",
                "iso639": "fr"
            }
        ],
        "country": {
            "country_name": "France",
            "country_code": "FR"
        },
        "external_ids": {
            "ISNI": {
                "preferred": null,
                "all": ["0000 0004 1784 3645"]
            },
            "OrgRef": {
                "preferred": null,
                "all": ["31274670"]
            },
            "Wikidata": {
                "preferred": null,
                "all": ["Q1163431"]
            },
            "GRID": {
                "preferred": "grid.440907.e",
                "all": "grid.440907.e"
            }
        }
    }
