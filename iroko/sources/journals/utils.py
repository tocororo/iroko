#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""
Helper function to several task related to Sources, sources types,
 sources fields, etc..
"""


from iroko.sources.models import Source


def _no_params(param_data):
    """aux func"""
    return param_data['title'] == 'None' and \
           param_data['description'] == 'None' and \
           param_data['url'] == 'None' and \
           param_data['issn'] == 'None' and \
           param_data['rnps'] == 'None' and \
           param_data['year_start'] == 'None' and \
           param_data['year_end'] == 'None'


def _filter_data_args(source: Source, data_args, and_op):
    """ aux func."""

    # esto es ineficiente... pero es lo que hay.. por el momento..
    # solo debe usarse para la lista de revistas que no pasa de 300
    # TODO: como optimizar...?
    #  En todo caso se puede generalizar para cualquier nombre dentro de data.... lo que habria que pasar la forma de evaluacion o algo asi (por el caso de issn)

    if source.data is None:
        return False
    if _no_params(data_args):
        return True

    title = data_args['title'].lower() in str(source.data['title']).lower() \
        if 'title' in source.data else False
    description = data_args['description'] in source.data['description'] \
        if 'description' in source.data else False
    url = data_args['url'] in source.data['url'] if 'url' in source.data else False

    issn = False
    if 'issn' in source.data:
        issn_p = data_args['issn'].lower() in source.data['issn']['p'].lower() if 'p' in source.data['issn'] else False
        issn_e = data_args['issn'].lower() in source.data['issn']['e'].lower() if 'e' in source.data['issn'] else False
        issn_l = data_args['issn'].lower() in source.data['issn']['l'].lower() if 'l' in source.data['issn'] else False
        issn = issn_p or issn_e or issn_l

    rnps = False
    if 'rnps' in source.data:
        rnps_p = data_args['rnps'].lower() in source.data['rnps']['p'].lower() if 'p' in source.data['rnps'] else False
        rnps_e = data_args['rnps'].lower() in source.data['rnps']['e'].lower() if 'e' in source.data['rnps'] else False
        rnps = rnps_p or rnps_e

    year_start = data_args['year_start'].lower() in source.data[
        'year_start'].lower() if 'year_start' in source.data else False
    year_end = data_args['year_end'].lower() in source.data['year_end'].lower() if 'year_end' in source.data else False

    if and_op:
        return title and description and url and issn and rnps and year_start and year_end
    else:
        return title or description or url or issn or rnps or year_start or year_end


def _filter_extra_args(source: Source, extra_args, and_op):
    """ aux func.
    esto es ineficiente...lo mismo que _filter_data_args"""

    if extra_args is None:
        return True

    source_type = source.source_type == extra_args['source_type']
    source_status = source.source_status == extra_args['source_status']

    if and_op:
        return source_type and source_status
    else:
        return source_type or source_status


def issn_is_in_data(data, issn: str, equal: bool):
    """Check if issn param is in any of the regular data ISSNs (print, electronic, link)
    if equal is True check exactly the value of issn param
    normally data have this structure
    {
        ...
        issn:{
            p:"XXXX-YYYY",
            e:"XXXX-YYYY",
            l:"XXXX-YYYY"
        }
        ...
    }

    param: data: data JSON of journals
    param: issn: string to compare
    param: equal: bool
    :rtype: bool
    """

    if issn and 'issn' in data:
        if equal:
            issn_p = issn.lower() == data['issn']['p'].lower() if 'p' in data['issn'] else False
            issn_e = issn.lower() == data['issn']['e'].lower() if 'e' in data['issn'] else False
            issn_l = issn.lower() == data['issn']['l'].lower() if 'l' in data['issn'] else False
        else:
            issn_p = issn.lower() in data['issn']['p'].lower() if 'p' in data['issn'] else False
            issn_e = issn.lower() in data['issn']['e'].lower() if 'e' in data['issn'] else False
            issn_l = issn.lower() in data['issn']['l'].lower() if 'l' in data['issn'] else False
        return issn_p or issn_e or issn_l
    return False


def field_is_in_data(data, field_name: str, field_value: str, equal: bool):
    """Check if field_value is in data[field_name]
    if equal is True,field_value == data[field_name]

    always check before if data[field_name] exist

    """
    result = False
    if field_value:
        if equal:
            result = field_value.lower() == data[field_name].lower() if field_name in data else False
        else:
            result = field_value.lower() in data[field_name].lower() if field_name in data else False
    return result
