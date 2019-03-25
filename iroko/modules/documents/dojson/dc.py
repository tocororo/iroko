


def create_dict(oai_record, source_uuid):

    data = {}

    data['original_identifier'] = oai_record.header.identifier
    data['source'] = source_uuid
    
    
    data['title'] = str(oai_record.metadata['title'])

    data['keywords'] = oai_record.metadata['subject']
    data['description'] = str(oai_record.metadata['description'])
    data['language'] = str(oai_record.metadata['language'])
    data['publication_date'] = oai_record.metadata['date'][0]
    
    creators = []
    for c in oai_record.metadata['creator']:
        creators.append({'name': str(c)})
    data['creators'] = creators

    ref = []
    for c in oai_record.metadata['relation']:
        ref.append({'raw_reference': str(c)})
    data['references'] = ref

    return data