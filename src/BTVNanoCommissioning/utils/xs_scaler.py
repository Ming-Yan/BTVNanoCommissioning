
import copy
import hist
from coffea.processor import accumulate
import os, psutil
from BTVNanoCommissioning.helpers.xsection import xsection
import numpy as np


def scale_xs(hist, lumi, events):
    xs_dict = {}
    for obj in xsection:
        xs_dict[obj["process_name"]] = float(obj["cross_section"])
    scales = {}
    for key in events:
        if type(key) != str or "Run" in key:
            continue
        scales[key] = xs_dict[key] * lumi / events[key]
    hist.scale(scales, axis="dataset")
    return hist


def scaleSumW(output, lumi):
    scaled = {}
    xs_dict = {}
    for obj in xsection:
    
        xs_dict[obj["process_name"]] = float(obj["cross_section"])
        if "kFactor"  in obj.keys():xs_dict[obj["process_name"]] =float(obj["cross_section"])*float(obj["kFactor"])
        if "WJetsToLNu" in obj["process_name"]:
            xs_dict[obj["process_name"]]=xs_dict[obj["process_name"]]/3.
    duplicated_name = False
    sumw = {}
    flist = []


    for f in output.keys():
        flist.extend([m for m in output[f].keys() if "Run" not in m])


    for files in output.keys():
        if "sumw" not in output[files].keys() and len(flist) != len(set(flist)):
            duplicated_name = True
            for sample in output[files].keys():
                if "Run" in str(output[files][sample]):
                    continue
                if sample in sumw.keys():
                    sumw[sample] = sumw[sample] + float(output[files][sample]["sumw"])
                else:
                    sumw[sample] = float(output[files][sample]["sumw"])


    for files in output.keys():
        if "sumw" not in output[files].keys():
            scaled[files] = {}
            for sample, accu in output[files].items():
                scaled[files][sample] = {}
                scaled[files][sample]["sumw"] = output[files][sample]["sumw"]

                if duplicated_name:
                    scaled[files][sample]["sumw"] = sumw[sample]
                for key, h_obj in accu.items():
                    if isinstance(h_obj, hist.Hist):
                        h = h_obj #copy.deepcopy(h_obj)
                        if sample in xs_dict.keys():
                            
                            h = (
                                h
                                * xs_dict[sample]
                                * lumi
                                / scaled[files][sample]["sumw"]
                            )
                        else:
                            if not (("data" in sample) or ("Run" in sample)) or (
                                "Double" in sample
                            ):
                                raise KeyError(sample, "is not founded in xsection.py")
                            else:
                                h = h
                        scaled[files][sample][key] = h
        else:
            for sample, accu in output[files].items():
                scaled[sample] = {}
                for key, h_obj in accu.items():
                    scaled[sample]["sumw"] = output[files]["sumw"]
                    if isinstance(h_obj, hist.Hist):
                        h = h_obj #copy.deepcopy(h_obj)
                        if sample in xs_dict.keys():
                            h = h * xs_dict[sample] * lumi / output[files]["sumw"]
                        else:
                            if not (("data" in sample) or ("Run" in sample)) or (
                                "Double" in sample
                            ):
                                raise KeyError(sample, "is not founded in xsection.py")
                            else:
                                h = h
                    scaled[sample][key] = h


    del output,sumw, flist,xs_dict

    return scaled


## Additional rescale for MC
def additional_scale(output, scale, sample_to_scale):
    scaled = {}
    for files in output.keys():
        scaled[files] = {}
        if "sumw" not in output[files].keys():
            for sample, accu in output[files].items():
                scaled[files][sample] = {}
                for key, h_obj in accu.items():
                    if isinstance(h_obj, hist.Hist):
                        h = copy.deepcopy(h_obj)
                        if sample in sample_to_scale:
                            h = h * scale
                        else:
                            h = h
                        scaled[files][sample][key] = h
        else:
            for sample, accu in output.items():
                scaled[sample] = {}
                for key, h_obj in accu.items():
                    if isinstance(h_obj, hist.Hist):
                        h = copy.deepcopy(h_obj)
                        if sample in sample_to_scale:
                            h = h * scale
                        else:
                            h = h
                        scaled[sample][key] = h
    return scaled


import gc
def collate(output, mergemap):
    out = {}
    merged = {}
    reduced={}
    print("FIXME:")
    for f in output.keys():
        reduced[list(output[f].keys())[0]]={k:v for k,v in output[f][list(output[f].keys())[0]].items() if  'BDT' in  k or 'sumw' in k }
        #del reduced[list(output[f].keys())[0]]['jet_etaphi'],reduced[list(output[f].keys())[0]]['hltlep2_pt'],reduced[list(output[f].keys())[0]]['hltlep1_pt'],reduced[list(output[f].keys())[0]]['weight']
    merged_output=reduced
    #merged_output = accumulate([output[f] for f in output.keys()])
    # print(merged_output.keys())
    # del output
    gc.collect()
    print(
            "clean up output",
            psutil.Process(os.getpid()).memory_info().rss / 1024**2,
            "MB",
        )
    for files in merged_output.keys():
        if "sumw" not in merged_output[files].keys():
            for m in output[files].keys():

                # if skipother:
                merged[m]={k:v for k,v in merged_output[files][m].items() }
                # else:                
                # merged[m] = dict(merged_output[files][m].items())
        else:
            # if skipother:
            merged[files] = {k:v for k,v in merged_output[files].items() }
            # else:
            # merged[files] = dict(merged_output[files].items())

    del merged_output
    print(
            "clean up merged",
            psutil.Process(os.getpid()).memory_info().rss / 1024**2,
            "MB",
        )
    for group, names in mergemap.items():
        out[group] = accumulate(
            [v for k, v in merged.items() if k in names ]
        )
       
    return out


def getSumW(accumulator):
    sumw = {}
    for key, accus in accumulator.items():
        sumw[key] = accus["sumw"]
    return sumw
