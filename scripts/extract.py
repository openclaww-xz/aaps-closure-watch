#!/usr/bin/env python3
"""Extract B01001 age bands for AAPS tracts from ACS 5yr summary files 2009-2023 (+2024 table-based).

Outputs raw/parsed_<year>.json: {geoid: {band: [est, moe]}}
Bands: total, 0-4, 5-9, 10-14, 15-17 (m/f combined at aggregation; here store m and f parts + totals).
"""
import csv, io, json, os, re, sys, zipfile

RAW = "/tmp/aaps-research/population/raw"
PARSED = os.path.join(RAW, "parsed")
os.makedirs(PARSED, exist_ok=True)

MALE = {3: "0-4", 4: "5-9", 5: "10-14", 6: "15-17"}      # B01001 lines (male)
FEMALE = {27: "0-4", 28: "5-9", 29: "10-14", 30: "15-17"}  # female lines
LINES = [1, 3, 4, 5, 6, 27, 28, 29, 30]


def band_of(ln):
    if ln == 1:
        return "total"
    suffix = "_m" if ln in MALE else "_f"
    return (MALE.get(ln) or FEMALE[ln]) + suffix


def wanted():
    s = set()
    with open("/tmp/aaps_geo/aaps_tracts.csv") as f:
        for r in csv.DictReader(f):
            s.add(r["GEOID"].strip())
    with open("/tmp/aaps_geo/aaps_tracts_2010vintage.csv") as f:
        for r in csv.DictReader(f):
            s.add(r["GEOID"].strip())
    return s


def seq_info(year):
    """(seq_str, start_pos) for B01001 from lookup txt."""
    import csv as _csv
    rows = []
    with open(f"{RAW}/lookup_{year}.txt", encoding="latin-1") as f:
        for row in _csv.reader(f):
            p = [x.strip() for x in row]
            if len(p) > 4 and p[1] == "B01001":
                rows.append(p)
    for p in rows:
        if p[3] == "" or p[3] == ".":  # table header row
            try:
                start = int(p[4]) if p[4] and p[4] != "." else 7
            except ValueError:
                start = 7
            return p[2].lstrip("0") or "0", start
    if rows:
        return rows[0][2].lstrip("0") or "0", 7
    raise ValueError(f"B01001 not found in lookup_{year}.txt")


def geo_map(year):
    """{logrecno: geoid} for Washtenaw tracts."""
    ext = "xlsx" if os.path.exists(f"{RAW}/geo_{year}.xlsx") else "xls"
    path = f"{RAW}/geo_{year}.{ext}"
    import openpyxl
    out = {}
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        header = None
        idx = None
        for r in it:
            if header is None:
                cells = [str(c).strip().upper() if c is not None else "" for c in r]
                if any("LOGRECNO" in c or "LOGICAL RECO" in c for c in cells):
                    header = cells
                    idx = {v: i for i, v in enumerate(cells) if v}
                continue
            vals = list(r)
            if not vals or idx is None:
                continue
            def get(*keys):
                for k in keys:
                    if k in idx and idx[k] < len(vals) and vals[idx[k]] is not None:
                        return str(vals[idx[k]]).strip()
                return ""
            # mini-geo format: Geography ID like 14000US26161400100
            graw = get("GEOGRAPHY ID", "GEOID", "GEO_ID")
            if graw.startswith("14000US") and "26161" in graw[7:12] + graw[7:17]:
                pass
            if graw.startswith("14000US26161"):
                g = graw.replace("14000US", "")
                out[get("LOGRECNO", "LOGICAL RECORD NUMBER")] = g
                continue
            sl = get("SUMLEV", "SUMMARY LEVEL", "SUMLEVEL")
            if sl != "140":
                continue
            # prefer explicit GEOID; fall back to state+county+tract
            g = get("GEOID", "GEO_ID")
            g = re.sub(r"\D", "", g)
            if len(g) == 11:
                lr = get("LOGRECNO", "LOGICAL RECORD NUMBER")
                out[lr] = g
                continue
            tr = get("TRACT", "TRACTCE", "CENSUS TRACT")
            if tr:
                t = tr.replace(".", "")
                t = t.ljust(6, "0") if len(t) <= 6 else t[-6:]
                lr = get("LOGRECNO", "LOGICAL RECORD NUMBER")
                out[lr] = f"26161{t}"
    return out


def xls_geo_map(year):
    import xlrd
    book = xlrd.open_workbook(f"{RAW}/geo_{year}.xls")
    out = {}
    for sh in book.sheets():
        hdr, hidx, idx = None, None, {}
        for ri in range(min(sh.nrows, 15)):
            row = [str(sh.cell_value(ri, ci)).strip().upper() for ci in range(sh.ncols)]
            if "LOGRECNO" in row:
                hdr, hidx = row, ri
                idx = {v: i for i, v in enumerate(row) if v}
                break
        if hdr is None:
            continue

        def get(ri, *keys):
            for k in keys:
                if k in idx:
                    v = sh.cell_value(ri, idx[k])
                    if v != "":
                        return str(v).strip()
            return ""

        for ri in range(hidx + 1, sh.nrows):
            graw = ""
            if "GEOID" in idx:
                graw = str(sh.cell_value(ri, idx["GEOID"])).strip()
            if graw.startswith("14000US26161"):
                out[get(ri, "LOGRECNO")] = graw.replace("14000US", "")
                continue
            if get(ri, "SUMLEV", "SUMMARY LEVEL", "SUMLEVEL") != "140":
                continue
            g = re.sub(r"\D", "", get(ri, "GEOID", "GEO_ID"))
            if len(g) == 11:
                out[get(ri, "LOGRECNO")] = g
                continue
            tr = get(ri, "TRACT", "CENSUS TRACT")
            if tr:
                t = tr.replace(".", "")
                t = t.ljust(6, "0") if len(t) <= 6 else t[-6:]
                out[get(ri, "LOGRECNO")] = f"26161{t}"
    return out


def fmt(v):
    v = v.strip()
    if v in ("", "."):
        return None
    try:
        return int(v)
    except ValueError:
        try:
            return int(float(v))
        except ValueError:
            return None


def parse_seq_year(year, want):
    seq, start = seq_info(year)
    seqfile = f"{int(seq):04d}".replace(  # e.g. "10" -> "0010"
        "0", "0", 1)  # no-op keep
    seq4 = f"{int(seq):07d}"  # 7-digit like 0010000
    zf = zipfile.ZipFile(f"{RAW}/MI_{year}.zip")
    prefix = f"{year}5mi{int(seq):04d}"
    est_name = f"e{year}5mi{int(seq):04d}000.txt"
    moe_name = f"m{year}5mi{int(seq):04d}000.txt"
    # naming: e20205mi0001000.txt -> seq %04d + "000"
    cands_e = [n for n in zf.namelist() if n == est_name]
    if not cands_e:
        # try without trailing 000 group
        cands_e = [n for n in zf.namelist() if re.match(rf"e{year}5mi{int(seq):04d}\d{{3}}\.txt$", n)]
        est_name = cands_e[0]
        moe_name = est_name.replace("e" + str(year), "m" + str(year), 1)
    if year >= 2016:
        lr2g = geo_map(year)
    else:
        lr2g = xls_geo_map(year)
    res = {}
    off = start - 1  # 0-based offset of first B01001 cell
    with zf.open(est_name) as fe, zf.open(moe_name) as fm:
        te = io.TextIOWrapper(fe, encoding="latin-1")
        tm = io.TextIOWrapper(fm, encoding="latin-1")
        for le, lm in zip(te, tm):
            pe = le.rstrip("\n").split(",")
            pm = lm.rstrip("\n").split(",")
            if len(pe) < 7 or len(pm) < 7:
                continue
            lr = pe[5].strip()
            g = lr2g.get(lr)
            if g in want:
                vals = pe[off:off + 49]
                moes = pm[off:off + 49]
                if len(vals) < 49:
                    continue
                d = {}
                ok = True
                for ln in LINES:
                    e = fmt(vals[ln - 1])
                    m = fmt(moes[ln - 1])
                    if e is None:
                        ok = False
                        break
                    d[band_of(ln)] = [e, m if m is not None else 0]
                if ok:
                    res[g] = d
    return res


def parse_table_year(year, want):
    res = {}
    col = None
    with open(f"{RAW}/acsdt5y{year}-b01001.dat", encoding="latin-1") as f:
        for line in f:
            parts = line.rstrip("\n").split("|")
            if col is None:
                if parts[0] != "GEO_ID":
                    continue
                col = {c: i for i, c in enumerate(parts)}
                continue
            if not parts[0].startswith("1400000US"):
                continue
            g = parts[0].replace("1400000US", "")
            if g not in want:
                continue
            d = {}
            for ln in LINES:
                e = fmt(parts[col[f"B01001_E{ln:03d}"]])
                m = fmt(parts[col[f"B01001_M{ln:03d}"]])
                if e is None:
                    d = None
                    break
                d[band_of(ln)] = [e, m or 0]
            if d:
                res[g] = d
    return res


if __name__ == "__main__":
    want = wanted()
    years = [int(a) for a in sys.argv[1:]] or list(range(2009, 2021))
    for y in years:
        try:
            if y >= 2021:
                r = parse_table_year(y, want)
            else:
                r = parse_seq_year(y, want)
            n = len(r)
            with open(f"{PARSED}/{y}.json", "w") as f:
                json.dump(r, f)
            print(f"{y}: {n} tracts parsed")
        except Exception as ex:
            print(f"{y}: ERROR {type(ex).__name__}: {ex}")
