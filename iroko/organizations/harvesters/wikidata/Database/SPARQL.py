#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys

from SPARQLWrapper import JSON, SPARQLWrapper

# from iroko.organizations.harvesters.wikidata.logger_base import logger

endpoint_url = "https://query.wikidata.org/sparql"


def getSparqlInstance(QID):
    try:
        # Q43229 - organization
        query = """SELECT DISTINCT ?item  ?itemLabel ?itemDescription
                   ?country  ?countryLabel

                    WHERE {
                     ?item (wdt:P31)+ wd:""" f"{QID};" """
                                      rdfs:label ?itemLabel.
                        FILTER(lang(?itemLabel) = 'en')

                        OPTIONAL { ?item  wdt:P17  ?country }
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                     }
                     ORDER BY ?item"""

        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()
    except Exception as e:
        print(f'ERROR: {e}')
        return None


def getSparqlSubclass(QID):
    try:
        # Q43229 - organization
        query = """SELECT ?item ?itemLabel
                    WHERE {
                          ?item (wdt:P279)* wd:""" f"{QID};" """
                                 rdfs:label ?itemLabel.
                          FILTER(lang(?itemLabel) = 'en')
                    }
                    ORDER BY ?item"""

        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()
    except Exception as e:
        print(f'ERROR: {e}')
        return None


def getInstanceStatements(itemLabel):
    query = """SELECT ?_prop ?propLabel ?_prop_entity ?_prop_entityLabel
                WHERE
                {
                    ?item rdfs:label """  f'"{itemLabel}"' " """"@en.
                    ?item ?_prop ?_prop_entity.

                    SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
                    ?prop wikibase:directClaim ?_prop .
                }"""
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def getInstanceDescription(itemLabel):
    try:
        # Q43229 - organization
        query = """SELECT DISTINCT ?item  ?itemLabel ?itemDescription ?itemAltLabel

                    WHERE {
                     ?item rdfs:label """  f'"{itemLabel}"' " """"@en.
                     OPTIONAL { ?item skos:altLabel ?alternative . }
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
                    }"""

        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()
    except Exception as e:
        print(f'ERROR: {e}')
        return None


if __name__ == '__main__':
    resultsSubclass = getInstanceStatements('Q43229')
    for result in resultsSubclass["results"]["bindings"]:
        print(result)

# resultsSubclass = getSparqlSubclass('Q43229')
# for result in resultsSubclass["results"]["bindings"]:
#     # subClass = Subclass(result.item.value)
#     print(result)

# resultsInstance = getSparqlInstance('Q43229')
# for result in resultsInstance["results"]["bindings"]:
#     # subClass = Subclass(result.item.value)
#     print(result)
