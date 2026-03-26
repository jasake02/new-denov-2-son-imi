from pathlib import Path
import pprint


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "py_school" / "app" / "templates"
OUTPUT_PATH = ROOT / "py_school" / "app" / "templates_bundle.py"


def main() -> None:
    bundle = {}

    for template_path in sorted(TEMPLATES_DIR.rglob("*.html")):
        key = template_path.relative_to(TEMPLATES_DIR).as_posix()
        bundle[key] = template_path.read_text(encoding="utf-8")

    OUTPUT_PATH.write_text(
        "TEMPLATE_BUNDLE = " + pprint.pformat(bundle, sort_dicts=True, width=120) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(bundle)} templates to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
