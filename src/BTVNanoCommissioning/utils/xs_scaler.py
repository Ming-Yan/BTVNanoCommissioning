import copy
import hist 
from coffea import processor
def read_xs(file):
    import json

    f = open(file)
    data = json.load(f)
    xs_dict = {}
    for obj in data:
        xs_dict[obj["process_name"]] = float(obj["cross_section"])
    return xs_dict


def scale_xs(hist, lumi, events, xsfile="xsection.json"):
    xs_dict = read_xs(xsfile)
    scales = {}
    for key in events:
        if type(key) != str or key == "Data" or "Run" in key:
            continue
        scales[key] = xs_dict[key] * lumi / events[key]
    hist.scale(scales, axis="dataset")
    return hist


def scale_xs_arr(events, lumi, xsfile="xsection.json"):
    xs_dict = read_xs(xsfile)
    scales = {}
    wei_array = {}
    for key in events:
        if type(key) != str or key == "Data" or "Run" in key:
            continue
        scales[key] = xs_dict[key] * lumi / events[key]

        wei_array[key] = scales[key]
    return wei_array
def scaleSumW(accumulator, lumi, sumw, dyscale=1.,xsfile="xsection.json"):
    scaled = {}


    xs_dict = read_xs(xsfile)
    for sample, accu in accumulator.items():
        scaled[sample] = {}
        for key, h_obj in accu.items():
            if isinstance(h_obj, hist.Hist):
                h = copy.deepcopy(h_obj)
                if sample in xs_dict.keys():
                    
                    if 'JetsToLL' in sample  and 'DY' in sample :h = h * xs_dict[sample] *lumi*dyscale/sumw[sample][sample]
                    else:h = h * xs_dict[sample] *lumi/sumw[sample][sample]
                else:
                    if not (("data" in sample) or ("Run" in sample)):
                        continue
                    else: h = h
                scaled[sample][key] = h
    return scaled


def collate(output, mergemap):
    out = {}
    if len(output.keys())>1:
        merged = {}
        for files in output.keys():
            
            for m in output[files].keys():
                merged[m]=dict(output[files][m].items())
        for group, names in mergemap.items():
            out[group] = processor.accumulate([v for k, v in merged.items() if k in names])
    else :
        for group, names in mergemap.items():
            out[group] = processor.accumulate([v for k, v in output.items() if k in names])
    return out
def getSumW(accumulator):
    sumw = {}
    for key, accus in accumulator.items():
        sumw[key] = accus['sumw']
    return sumw
