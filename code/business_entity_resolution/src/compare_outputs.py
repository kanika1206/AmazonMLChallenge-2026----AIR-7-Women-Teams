import sys


def read_rows(path):
    with open(path, encoding="utf-8") as f:
        next(f)
        rows = (line.rstrip("\n").partition("\t") for line in f if line.strip())
        return {s1_id: [x for x in ids.split(",") if x] for s1_id, _, ids in rows}


def main():
    original, reproduced = read_rows(sys.argv[1]), read_rows(sys.argv[2])
    missing = sum(len(set(ids) - set(reproduced.get(s1_id, []))) for s1_id, ids in original.items())
    extra = sum(len(set(ids) - set(original.get(s1_id, []))) for s1_id, ids in reproduced.items())
    reordered = sum(ids != reproduced.get(s1_id) and set(ids) == set(reproduced.get(s1_id, []))
                    for s1_id, ids in original.items())
    same_rows = list(original) == list(reproduced)
    print(f"rows {len(original):,} vs {len(reproduced):,} (same order: {same_rows}) | "
          f"pairs missing {missing}, extra {extra} | rows with IDs in another order {reordered}")
    sys.exit(0 if same_rows and missing == extra == 0 else 1)


if __name__ == "__main__":
    main()
