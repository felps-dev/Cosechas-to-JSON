import json

FIXED_GRADE = [
    {
        "id": 1,
        "name": "TAMANHOS",
        "items": [
            {"id": 1, "name": "M"},
            {"id": 2, "name": "G"},
        ],
    }
]

FIXED_DEPARTMENTS = [
    {"id": "98", "name": "Extras"},
    {"id": "99", "name": "Bases"},
]


def parse_departments(file):
    with open(file, "r") as f:
        lines = f.readlines()
        departments = []
        for index, line in enumerate(lines):
            parts = line.strip().split(";")
            departments.append(
                {
                    "id": parts[0],
                    "name": parts[1],
                }
            )
        return departments


def parse_products(file):
    with open(file, "r") as f:
        lines = f.readlines()
        products = []
        for line in lines:
            parts = line.strip().split(";")
            product = {
                "department": parts[1],
                "name": parts[0],
                "codbarras": [
                    {
                        "code": f"{parts[0]}M",
                        "grade_items": [1],
                        "insumos": [],
                        "price": float(parts[2].replace(",", ".")),
                    },
                    {
                        "code": f"{parts[0]}G",
                        "grade_items": [2],
                        "insumos": [],
                        "price": float(parts[3].replace(",", ".")),
                    },
                ],
            }
            products.append(product)
        return products


def parse_raw_materials(file):
    with open(file, "r") as f:
        lines = f.readlines()
        materials = []
        for index, line in enumerate(lines):
            parts = line.strip().split(";")
            materials.append(
                {
                    "id": index + 1,
                    "name": parts[0],
                }
            )
        return materials


def parse_compositions(file):
    with open(file, "r") as f:
        lines = f.readlines()
        compositions = {}
        for line in lines:
            parts = line.strip().split(";")
            compositions[parts[0]] = parts[1:]
        return compositions


def assign_compositions_to_products(products, compositions, raw_materials):
    for product in products:
        product_id = product["name"]

        composition = compositions[product_id]
        for comp in composition:
            for raw_material in raw_materials:
                if raw_material["name"] == comp:
                    # The indexes here refer to the codbarras (M and G respectively) # noqa
                    product["codbarras"][0]["insumos"].append(raw_material)
                    product["codbarras"][1]["insumos"].append(raw_material)
    return products


def parse_extras(file, department="98"):
    with open(file, "r") as f:
        lines = f.readlines()
        products = []
        for line in lines:
            parts = line.strip().split(";")
            product = {
                "department": department,
                "name": parts[2],
                "codbarras": [
                    {
                        "code": parts[0],
                        "grade_items": [],
                        "insumos": [],
                        "price": float(parts[3].replace(",", ".")),
                    },
                ],
            }
            products.append(product)
        return products


def parse_waffles(file):
    with open(file, "r") as f:
        lines = f.readlines()
        products = []
        for line in lines:
            parts = line.strip().split(";")
            product = {
                "department": parts[1],
                "name": parts[0],
                "codbarras": [
                    {
                        "code": parts[0] + "M",
                        "grade_items": [],
                        "insumos": [],
                        "price": float(parts[2].replace(",", ".")),
                    },
                    {
                        "code": parts[0] + "G",
                        "grade_items": [],
                        "insumos": [],
                        "price": float(parts[3].replace(",", ".")),
                    },
                    {
                        "code": parts[0] + "T",
                        "grade_items": [],
                        "insumos": [],
                        "price": float(parts[4].replace(",", ".")),
                    },
                ],
            }
            products.append(product)
        return products


def main():
    products = parse_products("Batidos.txt")
    raw_materials = parse_raw_materials("Frutas.txt")
    compositions = parse_compositions("BatidoFrutas.txt")
    departments = parse_departments("Classes.txt")
    departments += FIXED_DEPARTMENTS
    products_with_compositions = assign_compositions_to_products(
        products, compositions, raw_materials
    )
    products_with_compositions += parse_extras("Extras.txt", department="98")
    products_with_compositions += parse_extras(
        "ExtrasBase.txt", department="99"
    )  # noqa
    products_with_compositions += parse_waffles("Waffles.txt")

    with open("output_departments.json", "w") as outfile:
        json.dump(departments, outfile, indent=4)

    with open("output_grade.json", "w") as outfile:
        json.dump(FIXED_GRADE, outfile, indent=4)

    with open("output_produtos.json", "w") as outfile:
        json.dump(products_with_compositions, outfile, indent=4)


if __name__ == "__main__":
    main()
