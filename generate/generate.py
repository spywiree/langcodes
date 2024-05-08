import requests, json, os

URL = "https://raw.githubusercontent.com/nidhaloff/deep-translator/master/deep_translator/constants.py"


def main(path: str, pkg_name: str, type_name: str):
    constants = requests.get(URL).text

    g = {}
    exec(constants, g)
    langs: dict[str, str] = g["GOOGLE_LANGUAGES_TO_CODES"]

    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    with open(path, mode="a", encoding="utf-8") as f:
        f.write(f"package {pkg_name}" + "\n\n")
        f.write(f"type {type_name} string" + "\n\n")
        f.write("const (" + "\n")

        f.write("\t" + f'DETECT_LANGUAGE {type_name} = "auto"' + "\n\n")
        for k, value in langs.items():
            key = k.upper().replace(" ", "_").replace("(", "").replace(")", "")
            f.write("\t" + f'{key} {type_name} = "{value}"' + "\n")

        f.write(")" + "\n\n")

        supported_langs = json.dumps(list(langs.keys()))[1:-1]
        supported_langs_goarray = "[]string{" + supported_langs + "}"

        f.write("func SupportedLanguages() []string {" + "\n")
        f.write("\t" + f"return {supported_langs_goarray}" + "\n")
        f.write("}")

        f.write("\n")

    os.system(f'go fmt "{path}"')


if __name__ == "__main__":
    # path = os.path.join(os.path.dirname(os.getcwd()), "languages.go")
    path = "../languagecodes.go"

    main(path, "languagecodes", "LanguageCode")
