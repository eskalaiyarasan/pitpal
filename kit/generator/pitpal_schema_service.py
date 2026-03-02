import json
import re
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


JSON_TYPE_MAP = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
    "null": type(None),
}


class JsonSchemaService:

    def __init__(self, root_schema_path: str):
        self.root_schema_path = Path(root_schema_path).resolve()
        self.schemas = {}
        self.registry = Registry()
        self.root_schema = None
        self.validator = None

        self._load_schemas()
        self._build_validator()

    # -----------------------
    # Load Schemas
    # -----------------------

    def _load_schemas(self):
        directory = self.root_schema_path.parent

        for file in directory.glob("*.json"):
            with open(file) as f:
                schema_data = json.load(f)

            schema_id = schema_data.get("$id", str(file))
            self.schemas[schema_id] = schema_data

            self.registry = self.registry.with_resource(
                schema_id,
                Resource.from_contents(schema_data)
            )

            if file == self.root_schema_path:
                self.root_schema = schema_data

        if not self.root_schema:
            raise ValueError("Root schema not found")

    def _build_validator(self):
        self.validator = Draft202012Validator(
            self.root_schema,
            registry=self.registry
        )

    # -----------------------
    # Validation
    # -----------------------

    def validate(self, data: dict):
        self.validator.validate(data)

    # -----------------------
    # Path Parsing
    # -----------------------

    def _parse_path(self, path: str):
        tokens = []
        parts = path.split(".")

        for part in parts:
            while True:
                match = re.match(r"([^\[]+)\[(\d+)\]", part)
                if match:
                    tokens.append(match.group(1))
                    tokens.append(int(match.group(2)))
                    part = part[match.end():]
                    if not part:
                        break
                else:
                    tokens.append(part)
                    break

        return tokens

    # -----------------------
    # $ref Resolve
    # -----------------------

    def _resolve_ref(self, ref: str):
        schema_id, pointer = ref.split("#", 1)
        schema = self.schemas[schema_id]

        if pointer.startswith("/"):
            for part in pointer.lstrip("/").split("/"):
                schema = schema[part]

        return schema

    def _fully_resolve(self, node):
        while "$ref" in node:
            node = self._resolve_ref(node["$ref"])
        return node

    # -----------------------
    # Type Extraction
    # -----------------------

    def _extract_type(self, node):
        node = self._fully_resolve(node)

        if "oneOf" in node:
            return self._merge_types(node["oneOf"])

        if "anyOf" in node:
            return self._merge_types(node["anyOf"])

        if "allOf" in node:
            return self._merge_types(node["allOf"])

        if "type" in node:
            t = node["type"]
            if isinstance(t, list):
                return [JSON_TYPE_MAP[x] for x in t]
            return JSON_TYPE_MAP[t]

        if "properties" in node:
            return dict

        return None

    def _merge_types(self, schemas):
        types = []
        for s in schemas:
            t = self._extract_type(s)
            if isinstance(t, list):
                types.extend(t)
            else:
                types.append(t)
        return list(set(types))

    # -----------------------
    # Public API
    # -----------------------

    def get_type(self, path: str):
        tokens = self._parse_path(path)
        current = self.root_schema

        for token in tokens:
            current = self._fully_resolve(current)

            if isinstance(token, str):
                current = current["properties"][token]

            elif isinstance(token, int):
                current = current["items"]

        return self._extract_type(current)