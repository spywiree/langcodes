import requests, json, os, io

URL = "https://raw.githubusercontent.com/nidhaloff/deep-translator/master/deep_translator/constants.py"


def tab(n: int = 1) -> str:
    return n * "\t"


def nl(n: int = 1) -> str:
    return n * "\n"


def add_consts(
    f: io.TextIOWrapper,
    langs: dict[str, str],
    type_name: str,
):
    f.write(f"type {type_name} string" + nl(2))
    f.write("const (" + nl())
    f.write(tab() + f'DETECT_LANGUAGE {type_name} = "auto"' + nl(2))
    for k, value in langs.items():
        key = k.upper().replace(" ", "_").replace("(", "").replace(")", "")
        f.write(tab() + f'{key} {type_name} = "{value}"' + nl())

    f.write(")" + nl(2))


def add_supported_langs(f: io.TextIOWrapper, langs: dict[str, str]):
    supported_langs = json.dumps(list(langs.keys()))[1:-1]
    supported_langs_go = "[]string{" + supported_langs + "}"

    f.write("func SupportedLanguages() []string {" + nl())
    f.write(tab() + f"return {supported_langs_go}" + nl())
    f.write("}" + nl(2))


def add_languages_to_codes(
    f: io.TextIOWrapper,
    langs: dict[str, str],
):
    f.write("func LanguagesToCodes() map[string]string {" + nl())
    f.write(tab() + "return map[string]string{" + nl())

    for k, value in langs.items():
        key = k.upper().replace(" ", "_").replace("(", "").replace(")", "")
        f.write(tab(2) + f'"{key}" : "{value}",' + nl())
    f.write(tab() + "}" + nl())

    f.write("}")


def main(path: str, pkg_name: str, type_name: str):
    constants = requests.get(URL).text

    variables = {}
    exec(constants, variables)
    langs: dict[str, str] = variables["GOOGLE_LANGUAGES_TO_CODES"]

    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    with open(path, mode="a", encoding="utf-8") as f:
        f.write(f"package {pkg_name}" + nl(2))

        add_consts(f, langs, type_name)
        add_supported_langs(f, langs)
        add_languages_to_codes(f, langs)

        f.write(nl())

    os.system(f'go fmt "{path}"')


if __name__ == "__main__":
    # path = os.path.join(os.path.dirname(os.getcwd()), "languages.go")
    path = "../languagecodes.go"

    main(path, "languagecodes", "LanguageCode")
