import flywheel
import json
import os

"""
Tag files for visual QC reader tasks in Flywheel
See README.md for usage & license

Author: Niall Bourke
"""

def tagger(T2wQC, T1wQC, FLAIRQC, ADCQC):

    # Read config.json file
    p = open('/flywheel/v0/config.json')
    config = json.loads(p.read())
    # Read API key in config file
    api_key = (config['inputs']['api-key']['key'])
    fw = flywheel.Client(api_key=api_key)

    # Get the input file id
    input_file_id = (config['inputs']['input']['hierarchy']['id'])
    print("input_file_id is : ", input_file_id)
    file_obj = fw.get(input_file_id)

    # # Get the acquisition id from the input file
    # acq_id = file_obj.parents['acquisition']
    # file_obj = fw.get(acq_id)
    # ** Note: This is not needed as the input file is the acquisition container object **

    if T2wQC == True and 'T2' in file_obj.label and 'Align' not in file_obj.label and 'Segmentation' not in file_obj.label:
        # Check if tags list is empty, if so, add 'read' tag
        if not file_obj.tags:
            file_obj.add_tag('read')
            print(file_obj.label, 'read tag added')
        else:
            # if QC tags are present, do nothing, else add 'read' tag
            for ACQtag in file_obj.tags:
                if 'read' in ACQtag or 'QC_unclear' in ACQtag or 'QC_failed' in ACQtag or 'QC_passed' in ACQtag:
                    print(file_obj.label, 'QC tag found')
                else:
                    file_obj.add_tag('read')
                    print(file_obj.label, 'read tag added')

    if T1wQC == True and 'T1' in file_obj.label:
        # Check if tags list is empty, if so, add 'read' tag
        if not file_obj.tags:
            file_obj.add_tag('read')
            print(file_obj.label, 'read tag added')
        else:
            # if QC tags are present, do nothing, else add 'read' tag
            for ACQtag in file_obj.tags:
                if 'read' in ACQtag or 'QC_unclear' in ACQtag or 'QC_failed' in ACQtag or 'QC_passed' in ACQtag:
                    print(file_obj.label, 'QC tag found')
                else:
                    file_obj.add_tag('read')
                    print(file_obj.label, 'read tag added')

    if FLAIRQC == True and 'FLAIR' in file_obj.label:
        # Check if tags list is empty, if so, add 'read' tag
        if not file_obj.tags:
            file_obj.add_tag('read')
            print(file_obj.label, 'read tag added')
        else:
            # if QC tags are present, do nothing, else add 'read' tag
            for ACQtag in file_obj.tags:
                if 'read' in ACQtag or 'QC_unclear' in ACQtag or 'QC_failed' in ACQtag or 'QC_passed' in ACQtag:
                    print(file_obj.label, 'QC tag found')
                else:
                    file_obj.add_tag('read')
                    print(file_obj.label, 'read tag added')

    if ADCQC == True and 'ADC' in file_obj.label:
        # Check if tags list is empty, if so, add 'read' tag
        if not file_obj.tags:
            file_obj.add_tag('read')
            print(file_obj.label, 'read tag added')
        else:
            # if QC tags are present, do nothing, else add 'read' tag
            for ACQtag in file_obj.tags:
                if 'read' in ACQtag or 'QC_unclear' in ACQtag or 'QC_failed' in ACQtag or 'QC_passed' in ACQtag:
                    print(file_obj.label, 'QC tag found')
                else:
                    file_obj.add_tag('read')
                    print(file_obj.label, 'read tag added')

