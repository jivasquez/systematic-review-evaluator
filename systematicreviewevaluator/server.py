#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

import boto3
from flask import Flask, request, Response, render_template
from systematicreviewevaluator.config import CONFIG
words = ["", "second", "increasing", "reported", "unit", "effective", "wing", "fir", "fit", "effects", "rt", "rv", "rp", "rr", "rs", "ha", "rf", "rg", "ra", "rb", "rc", "rn", "ro", "rh", "ri", "strati", "estimate", "ate", "ata", "ato", "atm", "ati", "att", "service", "perio", "liter", "object", "tech", "rica", "vidence", "result", "fail", "irs", "score", "rolled", "outcome", "diff", "fro", "life", "spit", "previous", "han", "ease", "east", "people", "foc", "disorder", "soc", "mbi", "son", "support", "ovid", "role", "roll", "time", "ves", "prevent", "findings", "sign", "current", "ground", "studied", "studies", "logical", "positive", "data", "stress", "ss", "sp", "sso", "su", "st", "sk", "si", "sm", "sl", "sc", "sf", "se", "years", "tte", "nation", "training", "ons", "ont", "city", "indicate", "prospect", "sat", "surgery", "um", "ants", "anti", "curr", "formed", "observe", "iva", "rest", "cantly", "inter", "refer", "ration", "ace", "het", "hei", "complete", "ac", "ab", "ae", "uid", "ag", "af", "ai", "ak", "al", "ap", "ar", "au", "sci", "sch", "sca", "scu", "scr", "tw", "tt", "tr", "tm", "ti", "te", "tc", "condition", "large", "method", "experience", "social", "action", "vie", "vis", "select", "objectives", "respective", "occur", "signi", "itt", "itu", "symptoms", "tri", "status", "reduce", "major", "number", "differ", "relationship", "cco", "plan", "ext", "exp", "impact", "factor", "dependent", "cri", "set", "ses", "ser", "potent", "lec", "sea", "rite", "improved", "community", "infect", "systematic", "receive", "cta", "levels", "euro", "person", "format", "quest", "methods", "ba", "bl", "bt", "br", "cia", "ut", "cin", "cis", "cip", "ui", "ua", "uc", "ub", "influence", "actors", "age", "train", "thin", "led", "len", "les", "great", "rds", "cts", "outcomes", "confidence", "process", "high", "bene", "ow", "ties", "ot", "operative", "activit", "meta", "meth", "system", "atic", "atis", "fact", "drug", "eti", "ll", "ck", "ch", "cc", "ce", "cs", "cr", "cu", "ct", "va", "ve", "vi", "vo", "greater", "tics", "increased", "pressure", "assess", "function", "valuation", "count", "ins", "ind", "compared", "trials", "child", "disc", "spect", "bi", "study", "gly", "total", "program", "work", "erg", "era", "provide", "lan", "lab", "lac", "lay", "arch", "las", "order", "safe", "nts", "standard", "rated", "rates", "provid", "subjects", "assessed", "sus", "dl", "dm", "dg", "dd", "de", "da", "dy", "dv", "du", "dr", "ds", "ema", "ems", "identify", "observed", "wa", "wl", "wi", "received", "cos", "ile", "ill", "ili", "cog", "air", "aim", "cons", "perform", "nic", "epr", "thr", "epo", "epi", "tha", "epa", "arat", "rna", "pose", "pla", "post", "months", "clinical", "war", "evidence", "physical", "test", "interval", "gui", "cost", "change", "trial", "prove", "live", "ibl", "cas", "cat", "cal", "ibu", "cardia", "chin", "spo", "cardio", "ended", "statistical", "discuss", "em", "el", "en", "ei", "ee", "ea", "ec", "eb", "year", "eu", "ev", "eq", "ep", "es", "er", "increase", "card", "care", "int", "blind", "xa", "fi", "xp", "xt", "size", "objective", "ratio", "import", "article", "proved", "develop", "media", "lite", "investigated", "ccu", "severe", "ci", "actor", "cl", "improvement", "verse", "treatment", "ami", "early", "amp", "ams", "benefit", "t", "nurs", "intervention", "loc", "log", "area", "los", "low", "describe", "month", "mpa", "anal", "ions", "fr", "ft", "fu", "fa", "fe", "fl", "ega", "ces", "cep", "intervent", "event", "safety", "issue", "ass", "ast", "pub", "asc", "base", "ase", "ion", "nct", "nci", "sta", "sti", "randomly", "lie", "hypo", "deter", "liver", "pact", "baseline", "evaluate", "rug", "stem", "ster", "idu", "info", "uti", "interventions", "nan", "gu", "gt", "gy", "gg", "ge", "ga", "gl", "gi", "gh", "ducation", "chang", "gene", "win", "manage", "control", "including", "measure", "special", "relate", "eca", "prospective", "ars", "quality", "management", "rse", "bei", "bed", "ber", "bes", "uri", "based", "basel", "gram", "tend", "tens", "tent", "problem", "admin", "addition", "cent", "treat", "examined", "well", "dose", "ample", "psyc", "pu", "hr", "hs", "weight", "gain", "hl", "signed", "education", "diagnosis", "vasc", "affect", "entr", "evaluated", "neo", "ned", "net", "neu", "ner", "med", "men", "met", "mes", "active", "call", "recommend", "type", "rit", "adult", "involve", "better", "weeks", "therapy", "side", "iss", "ist", "isi", "iso", "symptom", "mini", "mine", "dom", "medical", "bac", "ears", "subject", "unc", "und", "three", "efficacy", "iq", "ip", "ir", "iu", "iv", "il", "ia", "ic", "ig", "qualit", "psych", "character", "opt", "background", "opo", "plica", "disord", "statistic", "incidence", "form", "analyse", "fort", "ship", "died", "depend", "die", "round", "dis", "elect", "peri", "flu", "predict", "sample", "mas", "designed", "mai", "mal", "man", "ida", "group", "gem", "main", "views", "interview", "ort", "ors", "ori", "org", "question", "crib", "lica", "potential", "pain", "tract", "ger", "ged", "gen", "seas", "relative", "jo", "cancer", "mark", "pap", "par", "pat", "pac", "pai", "pan", "mon", "mod", "served", "general", "examine", "oral", "children", "difference", "psycho", "public", "search", "medica", "establish", "der", "des", "remain", "del", "dec", "compare", "stic", "blood", "response", "late", "association", "mental", "participants", "evaluation", "mma", "conducted", "para", "duct", "treated", "ages", "assoc", "essi", "weigh", "relation", "common", "ph", "individual", "vascular", "vent", "fun", "development", "purpose", "howe", "prevention", "ldr", "cut", "cus", "source", "bin", "bio", "bit", "ped", "pea", "pec", "patient", "nse", "nst", "articular", "lys", "single", "implement", "decrease", "cha", "chi", "chn", "cho", "tag", "sions", "lf", "le", "lc", "la", "ln", "lo", "lm", "li", "lv", "lt", "lu", "ls", "lp", "ly", "dai", "dat", "day", "identified", "res", "rep", "rev", "mate", "ren", "rem", "rea", "red", "ree", "qui", "mil", "min", "mic", "mis", "mit", "disease", "knowledge", "syst", "national", "deliver", "placebo", "ad", "rences", "cor", "multi", "av", "coronary", "practice", "con", "clinic", "add", "est", "ess", "mode", "toms", "chronic", "pin", "pid", "pit", "oac", "consider", "risk", "direct", "conduct", "pati", "path", "changes", "hospital", "tl", "asses", "assessment", "lts", "mb", "mm", "mo", "mi", "mu", "mp", "ms", "ta", "ent", "gate", "enter", "cla", "randomized", "formation", "days", "rand", "primary", "relations", "top", "serve", "ortant", "rad", "ral", "rai", "ras", "rap", "effectiveness", "bse", "random", "oca", "report", "approach", "improve", "contr", "stent", "specific", "ich", "ica", "ice", "ics", "icu", "ict", "cord", "core", "gis", "gic", "heal", "differences", "nh", "ni", "nk", "nm", "nc", "ne", "tis", "ny", "setting", "tie", "nr", "ns", "nt", "tia", "tic", "consid", "rom", "roc", "rod", "focus", "lli", "level", "port", "groups", "anda", "criteria", "cases", "mortality", "performed", "consist", "inform", "term", "opera", "factors", "place", "population", "wide", "require", "pre", "ana", "anc", "pro", "rent", "ans", "urge", "state", "sse", "detect", "review", "por", "period", "pop", "pon", "case", "vest", "participant", "week", "model", "ng", "acute", "nu", "reduced", "respect", "om", "ol", "og", "od", "oc", "ob", "oa", "stand", "os", "op", "determine", "regard", "rva", "controlled", "intra", "iga", "included", "invest", "surgical", "follow", "alt", "als", "sons", "fac", "tel", "tem", "ten", "tea", "tee", "rate", "design", "sum", "sur", "ear", "numb", "short", "developed", "health", "king", "finding", "measures", "grams", "surg", "rti", "ies", "hip", "investigate", "activity", "art", "arg", "ari", "arl", "arm", "pr", "ps", "complication", "pt", "py", "reduction", "pa", "pe", "dur", "pi", "po", "pl", "pm", "behavior", "rin", "rio", "rib", "aged", "higher", "literature", "lower", "analysis", "edge", "ipat", "pros", "prop", "prom", "range", "services", "long", "associated", "vice", "ede", "include", "graphic", "car", "find", "trans", "app", "apa", "ape", "fet", "fes", "infection", "women", "tat", "tai", "sit", "spe", "sic", "sig", "sid", "sim", "exam", "patients", "clin", "whi", "ht", "eat", "view", "limit", "ability", "table", "avi", "dual", "cross", "unity", "tco", "ski", "press", "ndi", "surge", "stab", "van", "val", "appr", "var", "vas", "demonstrate", "conclusion"]


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/analyze", methods=["POST"])
def analize():
    RIS_document = request.files.get('ris_document')
    if RIS_document is not None:
        text = RIS_document.read()
        records = parse_RIS_file(text)
        prediction = get_machine_learning_prediction(records)
        text = "Not a systematic review"
        box_class = "not-systematic-review"
        score = prediction.get('Prediction', {}).get('predictedScores', {}).values()[0]
        if score >= 0.7:
            box_class = "systematic-review"
            text = "Systematic review!!"
        if score > 0.4 and score < 0.7:
            box_class = "very-probably-systematic-review"
            text = "Very probably a systematic review"
        if score > 0.2 and score <= 0.4:
            box_class = "probably-systematic-review"
            text = "Probably a systematic review"
        if score < 0.2:
            box_class = "not-systematic-review"
            text = "Not a systematic review"
        print(prediction)
        return render_template(
            'ris-response.html',
            text=text,
            score=score,
            box_class=box_class
        )
    return Response(
        json.dumps({'message': 'No RIS file detected'}),
        mimetype='application/json',
    )

def parse_RIS_file(text):
    for line in iter(text.splitlines()):
        if "AB  - " in line:
            # This is the line that matters
            abstract = re.sub('[^a-z\ ]+', " ", line.replace("AB  - ", "").lower())
            return analize_dict_ocurrences(abstract)

def analize_dict_ocurrences(text):
    result = []
    for word in words:
        if word in text:
            result.append(1)
        else:
            result.append(0)
    return result

def get_machine_learning_prediction(records):
    data = {
        "MLModelId": CONFIG["ML_MODEL"],
        "Record": {
        },
        "PredictEndpoint": "https://realtime.machinelearning.us-east-1.amazonaws.com"
    }
    for index, word in enumerate(records):
        id_ = "Var" + str(index + 1).zfill(4)
        data.get('Record')[id_] = str(word)
    client = boto3.client('machinelearning')
    return client.predict(
        MLModelId='ml-8sV9nqYVoJ5',
        Record=data.get('Record'),
        PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'
    )



if __name__ == "__main__":
    import os
    os.environ['DEBUG'] = 'true'
    app.run(port=8080, host="0.0.0.0", threaded=True)

